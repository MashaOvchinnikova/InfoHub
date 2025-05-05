import sqlalchemy
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base

from config import settings


class Database:
    def __init__(self, url: str):
        self.engine: Engine = create_engine(url=url, connect_args={"client_encoding": "utf8"})
        self.session_factory: sessionmaker = sessionmaker(
            bind=self.engine, autoflush=False, autocommit=False, expire_on_commit=False
        )

    def get_session(self) -> Session:
        with self.session_factory() as session:
            yield session


db_url = settings.DATABASE_URL
database = Database(db_url)

Base = declarative_base()