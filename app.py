from typing import Union
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


# hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
# hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
# hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)


# engine = create_engine("sqlite:///database.db")


# SQLModel.metadata.create_all(engine)

# with Session(engine) as session:
#     session.add(hero_1)
#     session.add(hero_2)
#     session.add(hero_3)
#     session.commit()


# with Session(engine) as session:
#     statement = select(Hero).where(Hero.name == "Spider-Boy")
#     hero = session.exec(statement).first()
#     print(hero)


# from typing import Generator
# from sqlmodel import SQLModel, Session, create_engine
# from fastapi import Depends

# # TODO: Replace with actual database URL from environment variable
# DATABASE_URL = "sqlite:///./database.db"

# engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})


# def create_db_and_tables():
#     """Create database tables."""
#     SQLModel.metadata.create_all(engine)


# def get_session() -> Generator[Session, None, None]:
#     """FastAPI dependency factory for database sessions."""
#     with Session(engine) as session:
#         yield session


# # Type alias for dependency injection
# SessionDep = Depends(get_session)
