from celery import Celery, states
from celery.result import AsyncResult
from celery.signals import worker_init, worker_process_init, worker_shutdown
import functools
from loguru import logger
from pathlib import Path
from beanie import init_beanie
from mongohelper import mongoo_instance as mymongoo
from config import mongo_config, celery_extra_config
import asyncio


logger.info(f"REDIS_URL: {celery_extra_config.REDIS_URL}")

celery_app = Celery(
    __name__,
    broker=celery_extra_config.REDIS_URL,
    backend=celery_extra_config.REDIS_URL,
)


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]


celery_app.config_from_object(CeleryConfig)


def async_to_sync(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return wrapped


@worker_init.connect()
@async_to_sync
async def on_worker_start(sender, **kwargs):
    logger.info("Worker is starting...")
    logger.info("Initializing MongoDB...")
    try:
        logger.info("[1] Initializing MongoDB")
        logger.info(f"Mongo URI: {mongo_config.MONGO_URI}")
        await mymongoo.init_mongoo(mongo_config.MONGO_URI)
        mymongoo.motor_client.get_io_loop = asyncio.get_running_loop
        logger.info("MongoDB initialized.")

        logger.info("[2] Initializing Beanie")
        await init_beanie(
            database=mymongoo.get_db(mongo_config.DB_NAME),
            document_models=[],
        )
        logger.success("[2] Beanie initialized")
    except Exception as e:
        logger.error(f"Error: {e}")


@worker_shutdown.connect()
def on_worker_shutdown(sender, **kwargs):
    logger.info("Worker is shutting down...")
    logger.info("Closing MongoDB connection...")
    mymongoo.close_connection()
    logger.info("MongoDB connection closed.")

    # Perform shutdown tasks here, like closing database connections


# @worker_process_init.connect()
# def on_process_start(sender, **kwargs):
#    print(f"Process {os.getpid()} is starting...")
#    # Per-process initialization, like thread-local variables
