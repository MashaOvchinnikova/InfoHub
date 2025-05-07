import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

service_path = os.path.dirname(os.path.abspath(__file__))
env_file = f"{service_path}\\.env"

class Settings(BaseSettings):
    # Service information
    SERVICE_NAME: str
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Administration and Moderation Service for InfoHub"
    PORT: int

    # Database
    DATABASE_URL: PostgresDsn | None = None
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # RabbitMQ
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_VHOST: str
    RABBITMQ_URL: str | None = None

    # JWT Settings
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "super_secret_jwt_key_change_in_production")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")

    # Service URLs
    AUTH_SERVICE_URL: str
    PROFILE_SERVICE_URL: str
    CONTENT_SERVICE_URL: str
    COLLECTION_SERVICE_URL: str
    PARSER_SERVICE_URL: str
    RECOMMENDATION_SERVICE_URL: str
    SEARCH_SERVICE_URL: str
    SOCIAL_SERVICE_URL: str

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

        if not self.RABBITMQ_URL:
            self.RABBITMQ_URL = f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD}@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{self.RABBITMQ_VHOST}"


settings = Settings()