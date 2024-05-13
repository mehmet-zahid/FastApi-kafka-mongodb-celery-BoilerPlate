from beanie import init_beanie
from loguru import logger
import asyncio

from services.kafka_service import kafkam
from config import mongo_config
from models.user import UserModel
from mongohelper import mongoo_instance as mymongoo


async def init_services(use_kafka=False):
    logger.info("Initializing services")
    try:
        logger.info(f"[1] Connecting to the mongodb with {mongo_config.MONGO_URI}")
        await mymongoo.init_mongoo(mongo_config.MONGO_URI)
        mymongoo.motor_client.get_io_loop = asyncio.get_running_loop
        logger.success("[1] MONGODB - READY")
        logger.info("[2] Initializing Beanie")
        await init_beanie(
            database=mymongoo.get_db(mongo_config.DB_NAME),
            document_models=[UserModel],
        )
        logger.success("[2] Beanie initialized")
        if use_kafka:
            logger.info("[3] Initializing Kafka Producer")
            await kafkam.setup_kafka_producer()
            logger.success("[3] Kafka Producer - READY")

    except Exception as e:
        logger.error(e)
        raise e


async def stop_services():
    logger.info("Stopping services")
    try:
        logger.info("Shutting down")
        logger.info("[-] Closing connection to Mongodb")
        mymongoo.close_connection()
        logger.success("[-] Connection to Mongodb closed")

        if hasattr(kafkam, "producer"):
            if kafkam.producer:
                logger.info("[-] Detected Active Producer, Closing Kafka Producer")
                await kafkam.producer.stop()
                logger.success("[-] Kafka Producer stopped")
    except Exception as e:
        logger.error(e)
        raise e
