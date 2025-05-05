import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aio_pika
import uvicorn

from src.social.social_service.config import settings

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


@app.on_event("startup")
async def startup_event():
    logger.info("Social service started")

    # Initialize RabbitMQ connection
    logger.info("Initializing RabbitMQ connection...")
    try:
        # Create connection to RabbitMQ
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        # Creating channel
        channel = await connection.channel()
        # Declare exchanges
        social_exchange = await channel.declare_exchange(
            "social_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        # Create queue for social activity events
        activity_queue = await channel.declare_queue(
            "social_activity_queue",
            durable=True
        )
        await activity_queue.bind(social_exchange, routing_key="social.activity.#")

        # Also listen to user events
        user_exchange = await channel.declare_exchange(
            "user_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        user_events_queue = await channel.declare_queue(
            "social_user_events_queue",
            durable=True
        )
        await user_events_queue.bind(user_exchange, routing_key="user.#")

        # Store RabbitMQ objects in app state
        app.state.rabbitmq_connection = connection
        app.state.rabbitmq_channel = channel
        app.state.rabbitmq_exchange = social_exchange
        logger.info("RabbitMQ connection established")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Social service shutdown")

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