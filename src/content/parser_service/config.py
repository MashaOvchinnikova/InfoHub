import os

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings

service_path = os.path.dirname(os.path.abspath(__file__))
env_file = f"{service_path}\\.env"


class Settings(BaseSettings):
    # Service information
    SERVICE_NAME: str
    VERSION: str = "0.1.0"
    DESCRIPTION: str = "Content Parser and Aggregation Service for InfoHub"
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

    # Parser settings
    PARSER_CONCURRENT_TASKS: int
    PARSER_REQUEST_TIMEOUT: int
    PARSER_USER_AGENT: str
    PARSER_CRAWL_DELAY: int

    # External services
    CONTENT_SERVICE_URL: str

    # CORS
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]

    class Config:
        env_file = ".env"
        case_sensitive = True

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