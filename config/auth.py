import os

# JWT configuration
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")

# Cookie name configuration
ACCESS_TOKEN_COOKIE_NAME = "access_token"
REFRESH_TOKEN_COOKIE_NAME = "refresh_token"

# Cookie max age configuration
COOKIE_MAX_AGE_ACCESS = int(os.getenv("COOKIE_MAX_AGE_ACCESS", 900))  # 15 minutes
COOKIE_MAX_AGE_REFRESH = int(os.getenv("COOKIE_MAX_AGE_REFRESH", 604800))  # 7 days
