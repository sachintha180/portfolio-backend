import os

# JWT configuration constants
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

ACCESS_TOKEN_COOKIE_NAME = "access_token"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"

COOKIE_MAX_AGE_ACCESS = int(os.getenv("COOKIE_MAX_AGE_ACCESS", 900))  # 15 minutes
COOKIE_MAX_AGE_REFRESH = int(os.getenv("COOKIE_MAX_AGE_REFRESH", 604800))  # 7 days

COOKIE_HTTP_ONLY = True
# NOTE: Set to True in production (requires HTTPS), False for local development
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
COOKIE_SAME_SITE = "lax"

# Environment configuration constants
PORT = int(os.getenv("PORT", 8000))
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
]
RELOAD = os.getenv("ENVIRONMENT", "development") == "development"
