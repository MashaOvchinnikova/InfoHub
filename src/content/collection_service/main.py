import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aio_pika
import uvicorn
import httpx

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


@app.on_event("startup")
async def startup_event():
    logger.info("Collection service started")
    global http_client
    http_client = httpx.AsyncClient()

    # Initialize RabbitMQ connection
    logger.info("Initializing RabbitMQ connection...")
    try:
        # Create connection to RabbitMQ
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        # Creating channel
        channel = await connection.channel()
        # Declare exchanges
        collection_exchange = await channel.declare_exchange(
            "collection_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Subscribe to content events
        content_exchange = await channel.declare_exchange(
            "content_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Declare queue for collection service
        queue = await channel.declare_queue(
            "collection_service_queue",
            durable=True
        )

        # Bind queue to content exchange with routing key
        await queue.bind(content_exchange, routing_key="content.#")

        app.state.rabbitmq_connection = connection
        app.state.rabbitmq_channel = channel
        app.state.rabbitmq_exchange = collection_exchange
        app.state.rabbitmq_queue = queue

        logger.info("RabbitMQ connection established")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Collection service shutdown")

    logger.info("Closing HTTP client...")
    if http_client:
        await http_client.aclose()

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