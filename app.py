from contextlib import asynccontextmanager
from fastapi import FastAPI
from config.database import create_db_and_tables
from routes import api_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="Portfolio Backend API",
    description="Backend API for portfolio and CS class management",
    version="1.0.0",
    lifespan=lifespan,
)


app.include_router(api_router, prefix="/api")


@app.get("/")
def index():
    """Root endpoint."""
    return {"message": "Portfolio Backend API", "version": "1.0.0"}
