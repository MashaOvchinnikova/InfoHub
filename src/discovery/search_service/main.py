import logging
import asyncio
import uvicorn
import json
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import FastAPI, Depends, HTTPException, Query, status, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import aio_pika
from datetime import datetime

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


# Models
class SearchQuery(BaseModel):
    query: str
    categories: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    types: Optional[List[str]] = None
    page: int = 1
    size: int = 20


class SearchResult(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    url: Optional[str] = None
    type: str
    categories: List[str] = []
    tags: List[str] = []
    created_at: datetime
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total: int
    page: int
    size: int
    pages: int


# Elasticsearch client
es_client = None


# Function to initialize Elasticsearch indices
async def init_elasticsearch():
    global es_client
    # Create source index
    sources_index = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_sources"

    try:
        if not await es_client.indices.exists(index=sources_index):
            await es_client.indices.create(
                index=sources_index,
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0,
                        "analysis": {
                            "analyzer": {
                                "content_analyzer": {
                                    "type": "custom",
                                    "tokenizer": "standard",
                                    "filter": ["lowercase", "stop", "snowball"]
                                }
                            }
                        }
                    },
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "title": {
                                "type": "text",
                                "analyzer": "content_analyzer",
                                "fields": {
                                    "keyword": {"type": "keyword"}
                                }
                            },
                            "description": {
                                "type": "text",
                                "analyzer": "content_analyzer"
                            },
                            "content": {
                                "type": "text",
                                "analyzer": "content_analyzer"
                            },
                            "url": {"type": "keyword"},
                            "type": {"type": "keyword"},
                            "categories": {"type": "keyword"},
                            "tags": {"type": "keyword"},
                            "created_at": {"type": "date"},
                            "updated_at": {"type": "date"},
                            "user_id": {"type": "keyword"},
                            "rating": {"type": "float"}
                        }
                    }
                }
            )
            logger.info(f"Created index {sources_index}")
    except Exception as e:
        logger.error(f"Error creating Elasticsearch index: {e}")
        raise


# RabbitMQ message handler for indexing content
async def process_content_messages(message: aio_pika.IncomingMessage):
    async with message.process():
        try:
            logger.info(f"Received message: {message.routing_key}")
            payload = json.loads(message.body.decode())
            event_type = message.routing_key.split(".")[-1]

            if event_type == "created" or event_type == "updated":
                # Index the content
                await index_content(payload)
            elif event_type == "deleted":
                # Remove the content from index
                await delete_content(payload["id"])

        except Exception as e:
            logger.error(f"Error processing message: {e}")


async def index_content(content_data: Dict[str, Any]):
    """Index content in Elasticsearch"""
    index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_sources"

    try:
        # Prepare document
        doc = {
            "id": content_data["id"],
            "title": content_data["title"],
            "description": content_data.get("description", ""),
            "url": content_data.get("url", ""),
            "type": content_data.get("type", "article"),
            "categories": content_data.get("categories", []),
            "tags": content_data.get("tags", []),
            "created_at": content_data.get("created_at", datetime.now().isoformat()),
            "updated_at": content_data.get("updated_at", datetime.now().isoformat()),
            "user_id": content_data.get("user_id", ""),
            "rating": content_data.get("rating", 0.0)
        }

        # If there's content, add it to the document
        if "content" in content_data:
            doc["content"] = content_data["content"]

        # Index the document
        await es_client.index(
            index=index_name,
            id=content_data["id"],
            document=doc,
            refresh=True
        )
        logger.info(f"Indexed content with ID {content_data['id']}")
    except Exception as e:
        logger.error(f"Error indexing content: {e}")
        raise


async def delete_content(content_id: str):
    """Delete content from Elasticsearch index"""
    index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_sources"
    try:
        await es_client.delete(
            index=index_name,
            id=content_id,
            refresh=True
        )
        logger.info(f"Deleted content with ID {content_id} from index")
    except NotFoundError:
        logger.warning(f"Content with ID {content_id} not found in index")
    except Exception as e:
        logger.error(f"Error deleting content: {e}")
        raise


@app.on_event("startup")
async def startup_event():
    logger.info("Search service starting...")

    # Initialize Elasticsearch client
    global es_client
    logger.info("Connecting to Elasticsearch...")
    es_client = AsyncElasticsearch([settings.ELASTICSEARCH_URL])

    # Initialize indices
    await init_elasticsearch()

    # Initialize RabbitMQ connection
    logger.info("Connecting to RabbitMQ...")
    try:
        # Create connection
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        # Creating channel
        channel = await connection.channel()

        # Declare exchange
        exchange = await channel.declare_exchange(
            settings.CONTENT_EXCHANGE,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Declare queue
        queue = await channel.declare_queue(
            settings.SEARCH_QUEUE,
            durable=True
        )

        # Bind queue to exchange with routing keys
        await queue.bind(exchange, "content.created")
        await queue.bind(exchange, "content.updated")
        await queue.bind(exchange, "content.deleted")

        # Start consuming messages
        await queue.consume(process_content_messages)

        # Store connection and channel in app state
        app.state.rabbitmq_connection = connection
        app.state.rabbitmq_channel = channel

        logger.info("RabbitMQ connection established")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")

    logger.info("Search service started successfully")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down search service...")

    # Close Elasticsearch connection
    if es_client is not None:
        await es_client.close()

    # Close RabbitMQ connection
    if hasattr(app.state, "rabbitmq_connection"):
        await app.state.rabbitmq_connection.close()

    logger.info("Search service shutdown complete")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    health_status = {
        "status": "healthy",
        "service": settings.SERVICE_NAME,
        "version": settings.VERSION,
    }

    # Check Elasticsearch connection
    try:
        es_status = await es_client.info()
        health_status["elasticsearch"] = "connected"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["elasticsearch"] = str(e)

    return health_status


@app.post("/search", response_model=SearchResponse)
async def search(query: SearchQuery):
    """Search for content based on query parameters"""
    index_name = f"{settings.ELASTICSEARCH_INDEX_PREFIX}_sources"

    # Build query
    must_conditions = [
        {"match": {"title": {"query": query.query, "boost": 2.0}}},
        {"match": {"description": {"query": query.query}}}
    ]

    # Add search in content if it exists
    must_conditions.append({"match": {"content": {"query": query.query, "boost": 0.5}}})

    # Add filters if provided
    filter_conditions = []

    if query.categories:
        filter_conditions.append({"terms": {"categories": query.categories}})

    if query.tags:
        filter_conditions.append({"terms": {"tags": query.tags}})

    if query.types:
        filter_conditions.append({"terms": {"type": query.types}})

    # Calculate pagination
    from_value = (query.page - 1) * query.size

    # Build the query
    search_query = {
        "from": from_value,
        "size": min(query.size, settings.MAX_SEARCH_RESULTS),
        "query": {
            "bool": {
                "must": must_conditions,
                "filter": filter_conditions
            }
        },
        "sort": [
            "_score",
            {"created_at": {"order": "desc"}}
        ]
    }

    try:
        # Execute search
        search_results = await es_client.search(
            index=index_name,
            body=search_query
        )

        # Process results
        total_hits = search_results["hits"]["total"]["value"]
        results = []

        for hit in search_results["hits"]["hits"]:
            source = hit["_source"]
            results.append(
                SearchResult(
                    id=source["id"],
                    title=source["title"],
                    description=source.get("description"),
                    url=source.get("url"),
                    type=source["type"],
                    categories=source.get("categories", []),
                    tags=source.get("tags", []),
                    created_at=datetime.fromisoformat(source["created_at"]),
                    score=hit["_score"]
                )
            )

        # Calculate total pages
        total_pages = (total_hits + query.size - 1) // query.size

        return SearchResponse(
            results=results,
            total=total_hits,
            page=query.page,
            size=query.size,
            pages=total_pages
        )

    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search error: {str(e)}"
        )


@app.post("/reindex/{content_id}")
async def reindex_content(content_id: str):
    """Endpoint to trigger reindexing of a specific content"""
    try:
        # Fetch content from content service
        # In a real implementation, you'd call the content service API
        # For this example, we'll just return a success message

        return {"status": "success", "message": f"Reindexing of content {content_id} triggered"}
    except Exception as e:
        logger.error(f"Reindex error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Reindex error: {str(e)}"
        )


@app.post("/reindex-all")
async def reindex_all_content():
    """Endpoint to trigger reindexing of all content"""
    try:
        # In a real implementation, you'd call the content service to get all content
        # and reindex everything, possibly as a background task

        return {"status": "success", "message": "Full reindexing triggered"}
    except Exception as e:
        logger.error(f"Full reindex error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Full reindex error: {str(e)}"
        )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=settings.PORT, reload=True)