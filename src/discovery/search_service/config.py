import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Service information
    SERVICE_NAME: str = "search_service"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Search Service for InfoHub"
    PORT: int = int(os.getenv("PORT", "8007"))

    # Database URL and schema
    DATABASE_SCHEMA: str = "search_service_schema"
    DATABASE_URL: str = "postgresql://postgres:Tomlinson91@postgres:5432/infohub"

    # Elasticsearch
    ELASTICSEARCH_HOST: str = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")
    ELASTICSEARCH_PORT: int = int(os.getenv("ELASTICSEARCH_PORT", "9200"))
    ELASTICSEARCH_URL: str = f"http://{ELASTICSEARCH_HOST}:{ELASTICSEARCH_PORT}"
    ELASTICSEARCH_INDEX_PREFIX: str = os.getenv("ELASTICSEARCH_INDEX_PREFIX", "infohub")

    # Search configuration
    MAX_SEARCH_RESULTS: int = int(os.getenv("MAX_SEARCH_RESULTS", "100"))
    DEFAULT_SEARCH_SIZE: int = int(os.getenv("DEFAULT_SEARCH_SIZE", "20"))

    # RabbitMQ
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_VHOST: str = os.getenv("RABBITMQ_VHOST", "/")
    RABBITMQ_URL: str = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"

    # Exchange and queue names
    CONTENT_EXCHANGE: str = "content_events"
    SEARCH_QUEUE: str = "search_indexing_queue"

    # External services
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
    API_GATEWAY_URL: str = os.getenv("API_GATEWAY_URL", "http://api_gateway")
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