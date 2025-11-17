from typing import Generator
from sqlmodel import SQLModel, Session, create_engine

# TODO: Replace with actual database URL from environment variable
DATABASE_URL = "sqlite:///./database.db"

engine = create_engine(
    DATABASE_URL, echo=True, connect_args={"check_same_thread": False}
)


def create_db_and_tables():
    """Create database tables."""
    SQLModel.metadata.create_all(engine)


def get_db_session() -> Generator[Session, None, None]:
    """Dependency factory for database sessions."""
    with Session(engine) as session:
        yield session
