from contextlib import asynccontextmanager
from dotenv import load_dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

# NOTE: Load environment variables before importing modules that use them
load_dotenv(".env.local")

from fastapi import FastAPI
from routes import api_router
from config.database import create_db_and_tables


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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router, prefix="/api")


@app.get("/")
def index():
    """Root endpoint."""
    return {"message": "Portfolio Backend API", "version": "1.0.0"}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    # NOTE: When reload=True, the application instance must be assigned as a string in the format "<module>:<app>"
