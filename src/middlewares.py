from fastapi import Request
from time import time

from src.logger import logger


async def add_process_time_header(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    process_time = (time() - start_time) * 1000
    response.headers["X-Process-Time"] = f"{round(process_time)} ms"
    return response


async def logger_middleware(request: Request, call_next):
    log_dict = {"url": request.url.path, "method": request.method}
    logger.info(log_dict)
    response = await call_next(request)
    return response
