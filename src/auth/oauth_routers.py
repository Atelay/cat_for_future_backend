from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Depends, Request
from src.auth.schemas import UserRead
from src.config import google_oauth_client as client
from .auth_config import auth_backend, fastapi_users

oauth_router = APIRouter(prefix="/oauth", tags=["OAuth2"])
templates = Jinja2Templates(directory="templates")
REDIRECT_URL = "http://localhost:8000/api/v1/oauth/auth/callgoogle"


@oauth_router.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@oauth_router.get("/auth/callgoogle")
async def google_callback(request: Request):
    return templates.TemplateResponse(
        "google_oauth_response.html", {"request": request}
    )


oauth_router.include_router(
    fastapi_users.get_oauth_router(
        client, auth_backend, "SECRET", redirect_url=REDIRECT_URL
    ),
    prefix="/auth/google",
)

oauth_router.include_router(
    fastapi_users.get_oauth_associate_router(client, UserRead, "SECRET"),
    prefix="/auth/associate/google",
)
