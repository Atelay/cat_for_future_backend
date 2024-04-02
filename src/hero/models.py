from sqlalchemy import Column, Integer, String
from fastapi_storages.integrations.sqlalchemy import FileType
from fastapi_storages import FileSystemStorage

from src.database.database import Base


storage = FileSystemStorage(path="static/media/hero")


class Hero(Base):
    __tablename__ = "hero"

    id: int = Column(Integer, primary_key=True)
    title: str = Column(String(length=120), nullable=False)
    sub_title: str = Column(String(length=120), nullable=False)
    media_path: str = Column(FileType(storage=storage), nullable=False)
    left_text: str = Column(String(length=100), nullable=False)
    right_text: str = Column(String(length=200), nullable=False)
