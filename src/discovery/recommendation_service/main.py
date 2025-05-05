import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import aio_pika
import redis
import uvicorn
import asyncio

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

# Redis client
redis_client = None


@app.on_event("startup")
async def startup_event():
    logger.info("Recommendation service started")

    # Initialize Redis connection
    global redis_client
    logger.info("Initializing Redis connection...")
    redis_client = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB,
        decode_responses=True,
    )

    # Initialize RabbitMQ connection
    logger.info("Initializing RabbitMQ connection...")
    try:
        # Create connection to RabbitMQ
        connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
        # Creating channel
        channel = await connection.channel()

        # Declare recommendation exchange
        recommendation_exchange = await channel.declare_exchange(
            "recommendation_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )

        # Listen to content events
        content_exchange = await channel.declare_exchange(
            "content_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        content_queue = await channel.declare_queue(
            "recommendation_content_queue",
            durable=True
        )
        await content_queue.bind(content_exchange, routing_key="content.#")

        # Listen to user/profile events
        user_exchange = await channel.declare_exchange(
            "user_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        user_queue = await channel.declare_queue(
            "recommendation_user_queue",
            durable=True
        )
        await user_queue.bind(user_exchange, routing_key="user.profile.#")

        # Listen to social activity events
        social_exchange = await channel.declare_exchange(
            "social_events",
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        social_queue = await channel.declare_queue(
            "recommendation_social_queue",
            durable=True
        )
        await social_queue.bind(social_exchange, routing_key="social.activity.#")

        # Store RabbitMQ objects in app state
        app.state.rabbitmq_connection = connection
        app.state.rabbitmq_channel = channel
        app.state.rabbitmq_exchange = recommendation_exchange
        logger.info("RabbitMQ connection established")
    except Exception as e:
        logger.error(f"Failed to connect to RabbitMQ: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Recommendation service shutdown")

    logger.info("Closing Redis connection...")
    if redis_client:
        redis_client.close()

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