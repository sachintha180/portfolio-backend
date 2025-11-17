from fastapi import APIRouter
from routes.user import router as user_router

# Create main API router
api_router = APIRouter()

# Include all route modules
api_router.include_router(user_router)
