import asyncio
from random import choice
from typing import Any

from sqlalchemy import func, select

from src.hero.models import Hero
from src.admin.commons.exceptions import AFTER_MODEL_CREATE
from src.auth.models import User
from src.config import settings
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.database import async_session_maker
from src.database.fake_data import (
    HERO_DATA,
    DOCUMENTS_DATA,
    INSTRUCTIONS_DATA,
    CONTACTS_DATA,
    CAT_DATA,
    STORY_DATA,
)
from src.auth.utils import add_user_data


fake_data = [
    {"data": HERO_DATA, "model": Hero},
    # {"data": FAKE_FOOTER, "model": Footer},
]


def add_instances(model: Any, data: dict | list, session: AsyncSession):
    try:
        instances_list = []
        if isinstance(data, dict):
            data = [data]
        for item_data in data:
            instance = model(**item_data)
            instances_list.append(instance)
        session.add_all(instances_list)
        print(AFTER_MODEL_CREATE % model.__tablename__)
        return instances_list
    except Exception as exc:
        raise exc


async def create_initial_data():
    async with async_session_maker() as s:
        user_count = await s.scalar(select(func.count()).select_from(User))
        if user_count == 0:
            add_user_data(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD, s)

            for initial_data in fake_data:
                add_instances(**initial_data, session=s)

            await s.commit()


if __name__ == "__main__":
    asyncio.run(create_initial_data())
