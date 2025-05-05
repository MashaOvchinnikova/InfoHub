import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Service information
    SERVICE_NAME: str = "collection_service"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "User Collections Management Service for InfoHub"
    PORT: int = int(os.getenv("PORT", "8004"))

    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "infohub")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))

    # Database URL and schema
    DATABASE_SCHEMA: str = "collection_service_schema"
    DATABASE_URL: str = "postgresql://postgres:Tomlinson91@postgres:5432/infohub"

    # RabbitMQ
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_VHOST: str = os.getenv("RABBITMQ_VHOST", "/")
    RABBITMQ_URL: str = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"

    # Service URLs
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
    CONTENT_SERVICE_URL: str = os.getenv("CONTENT_SERVICE_URL", "http://content_service:8003")

    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()