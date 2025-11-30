import os
from typing import Literal, cast

# General configuration
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
PORT = int(os.getenv("PORT", 8000))
CORS_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
]
RELOAD = ENVIRONMENT == "development"

# Cookie security configuration
COOKIE_HTTP_ONLY = True
# NOTE: "True" in production, "False" in development
COOKIE_SECURE = (
    os.getenv(
        "COOKIE_SECURE", "true" if ENVIRONMENT == "production" else "false"
    ).lower()
    == "true"
)
# NOTE: "none" in production, "lax" in development
cookie_same_site = os.getenv(
    "COOKIE_SAME_SITE", "none" if ENVIRONMENT == "production" else "lax"
)
if cookie_same_site not in ["lax", "strict", "none"]:
    raise ValueError(
        f"COOKIE_SAME_SITE must be either lax, strict, or none, got {cookie_same_site}"
    )
COOKIE_SAME_SITE = cast(Literal["lax", "strict", "none"], cookie_same_site)
