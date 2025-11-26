import os
from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"sslmode": "allow"},
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_db_session() -> Generator[Session, None, None]:
    """Dependency factory for database sessions."""
    with Session(engine) as db_session:
        yield db_session
