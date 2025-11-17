from fastapi import APIRouter

from routes.user import router as user_router
from routes.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(user_router)
