import logging
import asyncio
import aiohttp
import uvicorn
import aio_pika
import time
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any
from bs4 import BeautifulSoup
import httpx
from datetime import datetime
from sqlalchemy.orm import Session

from config import settings

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    root_path='/api',
    title=settings.SERVICE_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)


# Define models
class SourceRequest(BaseModel):
    url: HttpUrl
    category_id: int
    subcategory_id: Optional[int] = None
    source_type: str  # "article", "video", "book", etc.
    priority: int = 1


class ParsedContent(BaseModel):
    url: str
    title: str
    description: Optional[str] = None
    content: Optional[str] = None
    author: Optional[str] = None
    published_date: Optional[datetime] = None
    image_url: Optional[str] = None
    tags: List[str] = []
    metadata: Dict[str, Any] = {}
    source_type: str
    category_id: int
    subcategory_id: Optional[int] = None


# Parser class
class ContentParser:
    def __init__(self):
        self.session = None
        self.headers = {
            "User-Agent": settings.PARSER_USER_AGENT
        }

    async def initialize(self):
        self.session = aiohttp.ClientSession(headers=self.headers)

    async def close(self):
        if self.session:
            await self.session.close()
            self.session = None

    async def parse_url(self, request: SourceRequest) -> ParsedContent:
        """Parse content from a given URL"""
        if not self.session:
            await self.initialize()

        try:
            async with self.session.get(
                    str(request.url),
                    timeout=settings.PARSER_REQUEST_TIMEOUT
            ) as response:
                response.raise_for_status()
                html = await response.text()

                # Use BeautifulSoup to parse HTML
                soup = BeautifulSoup(html, 'html.parser')

                # Extract basic metadata
                title = soup.title.string.strip() if soup.title else ""

                # Try to find description in meta tags
                description = ""
                desc_meta = soup.find("meta", attrs={"name": "description"})
                if desc_meta and "content" in desc_meta.attrs:
                    description = desc_meta["content"]

                # Try to find main content (this is a simplistic approach)
                # In real implementation, you would need more sophisticated content extraction
                content_elem = soup.find("article") or soup.find("main") or soup.find("div", class_=["content",
                                                                                                     "article-content"])
                content = content_elem.get_text(strip=True) if content_elem else ""

                # Try to find author
                author_elem = soup.find("meta", attrs={"name": ["author", "article:author"]})
                author = author_elem["content"] if author_elem and "content" in author_elem.attrs else ""

                # Try to find published date
                date_elem = soup.find("meta", attrs={"property": ["article:published_time", "datePublished"]})
                published_date = None
                if date_elem and "content" in date_elem.attrs:
                    try:
                        published_date = datetime.fromisoformat(date_elem["content"].replace("Z", "+00:00"))
                    except (ValueError, TypeError):
                        pass

                # Try to find image
                image_url = None
                og_image = soup.find("meta", attrs={"property": "og:image"})
                if og_image and "content" in og_image.attrs:
                    image_url = og_image["content"]

                # Try to find tags/keywords
                tags = []
                keywords_meta = soup.find("meta", attrs={"name": "keywords"})
                if keywords_meta and "content" in keywords_meta.attrs:
                    tags = [tag.strip() for tag in keywords_meta["content"].split(",")]

                return ParsedContent(
                    url=str(request.url),
                    title=title,
                    description=description,
                    content=content,
                    author=author,
                    published_date=published_date,
                    image_url=image_url,
                    tags=tags,
                    source_type=request.source_type,
                    category_id=request.category_id,
                    subcategory_id=request.subcategory_id,
                    metadata={}
                )

        except (aiohttp.ClientError, asyncio.TimeoutError) as e:
            logger.error(f"Error parsing {request.url}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to parse content: {str(e)}")


# Initialize parser
parser = ContentParser()


# Background task for parsing
async def process_parse_request(request: SourceRequest):
    try:
        # Parse the content
        parsed_content = await parser.parse_url(request)

        # Send the parsed content to the content service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{settings.CONTENT_SERVICE_URL}/sources/",
                json=parsed_content.dict(),
                timeout=30
            )
            response.raise_for_status()

        # Publish event to RabbitMQ
        if hasattr(app.state, "rabbitmq_exchange"):
            message = aio_pika.Message(
                body=parsed_content.json().encode(),
                content_type="application/json"
            )
            await app.state.rabbitmq_exchange.publish(
                message,
                routing_key="content.source.created"
            )

        logger.info(f"Successfully parsed and stored content from {request.url}")
    except Exception as e:
        logger.error(f"Error processing parse request for {request.url}: {str(e)}")


@app.post("/parse/")
async def parse_url(request: SourceRequest, background_tasks: BackgroundTasks):
    """Queue a URL for parsing"""
    background_tasks.add_task(process_parse_request, request)
    return {"status": "parsing_queued", "url": str(request.url)}


@app.post("/parse/sync/")
async def parse_url_sync(request: SourceRequest):
    """Parse a URL synchronously"""
    parsed_content = await parser.parse_url(request)
    return parsed_content


@app.on_event("startup")
async def startup_event():
    logger.info("Parser service started")

    # Initialize parser
    await parser.initialize()

    # Initialize RabbitMQ connection
    logger.info("Initializing RabbitMQ connection...")
    try:
        # Create connection to RabbitMQ
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        # Creating channel
        channel = await connection.channel()
        # Declare exchange
        exchange = await channel.declare_exchange(
            "content_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Declare queue for parser requests
        queue = await channel.declare_queue(
            "parser_requests",
            durable=True
        )

        # Bind queue to exchange
        await queue.bind(exchange, routing_key="content.parse.request")

        # Set up consumer
        async def process_message(message):
            async with message.process():
                try:
                    data = SourceRequest.parse_raw(message.body)
                    await process_parse_request(data)
                except Exception as e:
                    logger.error(f"Error processing message: {str(e)}")

        await queue.consume(process_message)

        app.state.rabbitmq_connection = connection
        app.state.rabbitmq_channel = channel
        app.state.rabbitmq_exchange = exchange
        logger.info("RabbitMQ connection established")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Parser service shutdown")

    # Close parser resources
    await parser.close()

    # Close RabbitMQ connection
    logger.info("Closing RabbitMQ connection...")
    if hasattr(app.state, "rabbitmq_connection") and app.state.rabbitmq_connection:
        await app.state.rabbitmq_connection.close()


# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)