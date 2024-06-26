from fastapi_mail import ConnectionConfig
from pydantic_settings import BaseSettings, SettingsConfigDict
from httpx_oauth.clients.google import GoogleOAuth2


PHOTO_FORMATS = [
    "image/webp",
    "image/png",
    "image/jpeg",
]

FILE_FORMATS = [
    "application/pdf",
]

MAX_FILE_SIZE_MB = 3


class Settings(BaseSettings):
    POSTGRES_PORT: str
    POSTGRES_HOST: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    EMAIL_HOST: str
    EMAIL_PORT: int
    EMAIL_USER: str
    EMAIL_PASSWORD: str

    SECRET_AUTH: str
    ADMIN_USERNAME: str
    ADMIN_PASSWORD: str

    MERCHANT_ACCOUNT: str
    MERCHANT_SECRET: str

    REDIS_HOST: str
    REDIS_PORT: str
    REDIS_PASS: str

    BASE_URL: str
    SITE_URL: str

    CLIENT_ID: str
    CLIENT_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

google_oauth_client = GoogleOAuth2(settings.CLIENT_ID, settings.CLIENT_SECRET)

settings.POSTGRES_PORT = "5432"
settings.REDIS_PORT = "6379"

PROJECT_NAME = "Cat for future "
API_PREFIX = "/api/v1"
DATABASE_URL = f"postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

REDIS_URL = (
    f"redis://default:{settings.REDIS_PASS}@{settings.REDIS_HOST}:{settings.REDIS_PORT}"
)
CACHE_PREFIX = "fastapi-cache"
HOUR = 3600
DAY = HOUR * 24
HALF_DAY = HOUR * 12
MONTH = DAY * 30

mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.EMAIL_USER,
    MAIL_PASSWORD=settings.EMAIL_PASSWORD,
    MAIL_FROM=settings.EMAIL_USER,
    MAIL_PORT=settings.EMAIL_PORT,
    MAIL_SERVER=settings.EMAIL_HOST,
    MAIL_FROM_NAME=PROJECT_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)

ALLOW_METHODS = ["GET", "POST", "PUT", "OPTIONS", "DELETE", "PATCH"]
ALLOW_HEADERS = [
    "Content-Type",
    "Set-Cookie",
    "Access-Control-Allow-Headers",
    "Access-Control-Allow-Origin",
    "Authorization",
    "If-None-Match",
]
EXPOSE_HEADERS = [
    "ETag",
]
ORIGINS = ["*"]

SWAGGER_PARAMETERS = {
    "syntaxHighlight.theme": "obsidian",
    "tryItOutEnabled": True,
    "displayOperationId": True,
    "filter": True,
    "requestSnippets": True,
    "defaultModelsExpandDepth": -1,
    "docExpansion": "none",
    "persistAuthorization": True,
    "displayRequestDuration": True,
}
