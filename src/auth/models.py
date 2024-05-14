from datetime import datetime
from fastapi import Depends
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyBaseOAuthAccountTable,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, Mapped, mapped_column, declared_attr
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from src.database.database import Base, get_async_session
from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTable,
)
from fastapi_users_db_sqlalchemy.generics import GUID, TIMESTAMPAware, now_utc


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String(25))
    phone = Column(String(30), unique=True)
    email = Column(String(50), nullable=False)
    hashed_password: str = Column(String(length=1024), nullable=False)
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)
    cats = relationship("Cat", back_populates="user", passive_deletes=True)
    oauth_accounts: Mapped[list["OAuthAccount"]] = relationship(lazy="joined")


class OAuthAccount(SQLAlchemyBaseOAuthAccountTable[int], Base):
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return mapped_column(
            Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
        )


class AccessToken(SQLAlchemyBaseAccessTokenTable[int], Base):
    @declared_attr
    def user_id(cls):
        return Column(
            Integer, ForeignKey("user.id", ondelete="cascade"), nullable=False
        )


class RefreshToken(Base):
    __tablename__ = "refresh_token"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[str] = mapped_column(String(1024), nullable=False, unique=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.id", ondelete="cascade")
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMPAware(timezone=True), index=True, nullable=False, default=now_utc
    )


async def get_access_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


async def get_refresh_token_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyAccessTokenDatabase(session, RefreshToken)
