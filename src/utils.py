from io import BytesIO
import os
import shutil
from uuid import uuid4

from fastapi import BackgroundTasks, FastAPI, HTTPException, UploadFile
import aiofiles

from src.config import FILE_FORMATS, MAX_FILE_SIZE_MB, PHOTO_FORMATS
from src.exceptions import INVALID_FILE, INVALID_PHOTO, OVERSIZE_FILE


def clear_media_path():
    folder_path = os.path.join("static", "media")
    if os.path.exists(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


async def save_photo(
    file: UploadFile,
    model,
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:
    if not is_file and not file.content_type in PHOTO_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_PHOTO % (file.content_type, PHOTO_FORMATS)
        )
    if file.size > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=OVERSIZE_FILE)
    if is_file and not file.content_type in FILE_FORMATS:
        raise HTTPException(
            status_code=415, detail=INVALID_FILE % (file.content_type, FILE_FORMATS)
        )

    folder_path = os.path.join(
        "static", "media", model.__tablename__.lower().replace(" ", "_")
    )
    file_name = f'{uuid4().hex}.{file.filename.split(".")[-1]}'
    file_path = os.path.join(folder_path, file_name)

    async def _save_photo(file_path: str):
        os.makedirs(folder_path, exist_ok=True)
        chunk_size = 256
        async with aiofiles.open(file_path, "wb") as buffer:
            while chunk := await file.read(chunk_size):
                await buffer.write(chunk)

    background_tasks.add_task(_save_photo, file_path)
    return file_path


async def delete_photo(path: str, background_tasks: BackgroundTasks) -> None:
    if "media" in path:
        path_exists = os.path.exists(path)
        if path_exists:
            background_tasks.add_task(os.remove, path)


async def update_photo(
    file: UploadFile,
    record,
    field_name: str,
    background_tasks: BackgroundTasks,
    is_file=False,
) -> str:
    old_photo_path = getattr(record, field_name, None)
    new_photo = await save_photo(file, record, background_tasks, is_file)
    if old_photo_path:
        await delete_photo(old_photo_path, background_tasks)
    return new_photo


# def save_photo(
#     file: str,
#     model,
#     image_extension: str,
# ) -> str:
#     folder_path = os.path.join(
#         "static", "media", model.__tablename__.lower().replace(" ", "_")
#     )
#     file_name = generate_file_name(image_extension=image_extension)
#     file_path = os.path.join(folder_path, file_name)

#     async def _save_photo(file_path: str):
#         os.makedirs(folder_path, exist_ok=True)
#         async with aiofiles.open(file_path, "wb") as buffer:
#             await buffer.write(file)

#     loop = asyncio.get_event_loop()
#     loop.create_task(_save_photo(file_path))
#     return file_path


def generate_file_name(filepath: str = None, image_extension: str = None):
    "file or image_extension with <.>"
    name = uuid4().hex
    if not image_extension:
        image_extension = "." + filepath.split("/")[-1].split(".")[-1]
    return name + image_extension


def create_file_field(file_path: str) -> UploadFile:
    file_name = generate_file_name(file_path)
    with open(file_path, "rb") as buffer:
        file_bytes = buffer.read()
    return UploadFile(file=BytesIO(file_bytes), filename=file_name)


# def delete_photo(path: str) -> None:
#     async def _delete_photo(path):
#         if path and "media" in path:
#             path_exists = os.path.exists(path)
#             if path_exists:
#                 os.remove(path)

#     loop = asyncio.get_event_loop()
#     loop.create_task(_delete_photo(path))
