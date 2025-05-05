import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import time
import aio_pika
import uvicorn
import httpx
from elasticsearch import AsyncElasticsearch

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


# HTTP client for service-to-service communication
http_client = None
# Elasticsearch client
es_client = None


@app.on_event("startup")
async def startup_event():
    logger.info("Content service started")
    global http_client, es_client
    http_client = httpx.AsyncClient()

    # Initialize Elasticsearch connection
    logger.info("Initializing Elasticsearch connection...")
    es_client = AsyncElasticsearch([settings.ELASTICSEARCH_URL])

    # Create content index if it doesn't exist
    try:
        if not await es_client.indices.exists(index="content"):
            await es_client.indices.create(
                index="content",
                body={
                    "settings": {
                        "number_of_shards": 1,
                        "number_of_replicas": 0
                    },
                    "mappings": {
                        "properties": {
                            "id": {"type": "keyword"},
                            "title": {"type": "text"},
                            "description": {"type": "text"},
                            "content_type": {"type": "keyword"},
                            "url": {"type": "keyword"},
                            "tags": {"type": "keyword"},
                            "created_at": {"type": "date"},
                            "updated_at": {"type": "date"},
                            "author_id": {"type": "keyword"},
                            "rating": {"type": "float"},
                            "view_count": {"type": "integer"}
                        }
                    }
                }
            )
            logger.info("Created 'content' index in Elasticsearch")
    except Exception as e:
        logger.error(f"Failed to create Elasticsearch index: {e}")

    # Initialize RabbitMQ connection
    logger.info("Initializing RabbitMQ connection...")
    try:
        # Create connection to RabbitMQ
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        # Creating channel
        channel = await connection.channel()
        # Declare exchanges
        content_exchange = await channel.declare_exchange(
            "content_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Declare queue for content service
        queue = await channel.declare_queue(
            "content_service_queue",
            durable=True
        )

        app.state.rabbitmq_connection = connection
        app.state.rabbitmq_channel = channel
        app.state.rabbitmq_exchange = content_exchange
        app.state.rabbitmq_queue = queue

        logger.info("RabbitMQ connection established")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Content service shutdown")

    logger.info("Closing HTTP client...")
    if http_client:
        await http_client.aclose()

    logger.info("Closing Elasticsearch connection...")
    if es_client:
        await es_client.close()

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