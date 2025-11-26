import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", 8000))
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
]
RELOAD = ENVIRONMENT == "development"
