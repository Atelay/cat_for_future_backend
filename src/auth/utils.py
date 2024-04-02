import contextlib

from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_mail import FastMail, MessageSchema

from src.auth.models import User
from src.database.database import get_async_session
from src.config import mail_config, settings
from .exceptions import EMAIL_BODY, USER_EXISTS
from .manager import get_user_db, get_user_manager


get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


def add_user_data(email: str, password: str, session: AsyncSession):
    instance = User(
        email=email,
        hashed_password=PasswordHelper().hash(password),
        is_superuser=True,
        is_active=True,
        is_verified=True,
    )
    session.add(instance)


async def send_reset_email(email: str, token: str):
    message = MessageSchema(
        subject="Password Reset Request",
        recipients=[email],
        body=EMAIL_BODY % (settings.BASE_URL, token),
        subtype="html",
    )
    fm = FastMail(mail_config)
    await fm.send_message(message)
