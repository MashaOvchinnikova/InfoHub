import os
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Service information
    SERVICE_NAME: str = "admin_service"
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Administration and Moderation Service for InfoHub"
    PORT: int = int(os.getenv("PORT", "8009"))

    # Database
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "infohub")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT: int = int(os.getenv("POSTGRES_PORT", "5432"))

    # Database URL and schema
    DATABASE_SCHEMA: str = "admin_service_schema"
    DATABASE_URL: str = "postgresql://postgres:Tomlinson91@postgres:5432/infohub"

    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super_secret_jwt_key_change_in_production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    # RabbitMQ
    RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", "guest")
    RABBITMQ_PASSWORD: str = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", "rabbitmq")
    RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", "5672"))
    RABBITMQ_VHOST: str = os.getenv("RABBITMQ_VHOST", "/")
    RABBITMQ_URL: str = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"

    # Service URLs
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
    PROFILE_SERVICE_URL: str = os.getenv("PROFILE_SERVICE_URL", "http://profile_service:8002")
    CONTENT_SERVICE_URL: str = os.getenv("CONTENT_SERVICE_URL", "http://content_service:8003")
    COLLECTION_SERVICE_URL: str = os.getenv("COLLECTION_SERVICE_URL", "http://collection_service:8004")
    PARSER_SERVICE_URL: str = os.getenv("PARSER_SERVICE_URL", "http://parser_service:8005")
    RECOMMENDATION_SERVICE_URL: str = os.getenv("RECOMMENDATION_SERVICE_URL", "http://recommendation_service:8006")
    SEARCH_SERVICE_URL: str = os.getenv("SEARCH_SERVICE_URL", "http://search_service:8007")
    SOCIAL_SERVICE_URL: str = os.getenv("SOCIAL_SERVICE_URL", "http://social_service:8008")

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