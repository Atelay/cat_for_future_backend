from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.middleware.base import BaseHTTPMiddleware
from sqladmin import Admin

from src.config import (
    ALLOW_HEADERS,
    ALLOW_METHODS,
    EXPOSE_HEADERS,
    ORIGINS,
    PROJECT_NAME,
    SWAGGER_PARAMETERS,
    API_PREFIX,
)
from src.admin import __all__ as views
from src.auth.routers import auth_router, oauth2
from src.user.routers import user_router
from src.hero.routers import hero_router
from src.stories.routers import stories_router
from src.cats.routers import cats_router
from src.instructions.routers import instructions_router
from src.documents.routers import documents_router
from src.contacts.routers import contacts_router, feedback_router
from src.donate.routers import donate_router
from src.utils import lifespan
from src.database.database import engine
from src.admin.auth import authentication_backend
from src.middlewares import logger_middleware, add_process_time_header


app = FastAPI(
    swagger_ui_parameters=SWAGGER_PARAMETERS,
    title=PROJECT_NAME,
    lifespan=lifespan,
)

admin = Admin(app, engine, authentication_backend=authentication_backend)

app.mount("/static", StaticFiles(directory="static"), name="static")
api_routers = [
    auth_router,
    hero_router,
    user_router,
    stories_router,
    cats_router,
    instructions_router,
    documents_router,
    contacts_router,
    feedback_router,
    donate_router,
    oauth2,
]

[app.include_router(router, prefix=API_PREFIX) for router in api_routers]

[admin.add_view(view) for view in views]

app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
app.add_middleware(BaseHTTPMiddleware, dispatch=logger_middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=ALLOW_METHODS,
    allow_headers=ALLOW_HEADERS,
    expose_headers=EXPOSE_HEADERS,
)
