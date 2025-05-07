import os

from pydantic import RedisDsn, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

service_path = os.path.dirname(os.path.abspath(__file__))
env_file = f"{service_path}\\.env"


class Settings(BaseSettings):
    # Service information
    SERVICE_NAME: str
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Content Recommendation Service for InfoHub"
    PORT: int

    # Database
    DATABASE_URL: PostgresDsn | None = None
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # Redis
    CONNECTION_METHOD: str
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DB: int
    REDIS_URL: RedisDsn | None = None

    # RabbitMQ
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_VHOST: str
    RABBITMQ_URL: str | None = None

    # Service URLs
    CONTENT_SERVICE_URL: str
    PROFILE_SERVICE_URL: str
    SOCIAL_SERVICE_URL: str
    AUTH_SERVICE_URL: str

    # Recommendation settings
    RECOMMENDATION_CACHE_TTL: int = int(os.getenv("RECOMMENDATION_CACHE_TTL", "3600"))  # 1 hour
    MAX_RECOMMENDATIONS: int = int(os.getenv("MAX_RECOMMENDATIONS", "20"))

    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    model_config = SettingsConfigDict(
        env_file=env_file, extra="ignore", env_file_encoding="utf-8"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.DATABASE_URL:
            self.DATABASE_URL = PostgresDsn.build(
                scheme="postgresql+psycopg2",
                username=self.POSTGRES_USER,
                password=self.POSTGRES_PASSWORD,
                host=self.POSTGRES_HOST,
                port=self.POSTGRES_PORT,
                path=self.POSTGRES_DB,
            )

        if not self.REDIS_URL:
            self.REDIS_URL = RedisDsn.build(
                scheme=self.CONNECTION_METHOD,
                host=self.REDIS_HOST,
                port=self.REDIS_PORT,
                path=str(self.REDIS_DB)
            )

        if not self.RABBITMQ_URL:
            self.RABBITMQ_URL = f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"


settings = Settings()
