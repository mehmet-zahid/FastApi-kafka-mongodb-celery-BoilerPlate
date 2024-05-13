from os import getenv
from utils.envutil import check_var_env
from loguru import logger


## checks env if not exists load it from local .env file
APP_ENV = check_var_env("APP_ENV")
logger.info(f"APP_ENV: {APP_ENV}")


class KafkaConfig:
    def __init__(self) -> None:
        # write your required kafka config here
        self.KAFKA_BOOTSTRAP_SERVER = getenv("KAFKA_BOOTSTRAP_SERVER")
        self.KAFKA_PRODUCER_TOPIC = getenv("KAFKA_PRODUCER_TOPIC")


class MongoConfig:
    def __init__(self) -> None:
        MONGO_URI = getenv("MONGO_URI")
        if not MONGO_URI:
            raise ValueError("MONGO_URI environment variable not set")

        self.MONGO_URI = MONGO_URI
        self.DB_NAME = getenv("MONGO_DB_NAME", "exampl_db")


class CeleryConfig:
    def __init__(self) -> None:
        REDIS_URL = getenv("REDIS_URL")
        if REDIS_URL:
            self.REDIS_URL = REDIS_URL
        else:
            if not APP_ENV:
                raise ValueError(
                    "APP_ENV environment variable not set, please set it in .env file"
                )
            if APP_ENV.startswith("COMPOSE_"):
                self.REDIS_URL = "redis://redis:6379"
            else:
                self.REDIS_URL = "redis://localhost:6379"


kafka_config = KafkaConfig()
mongo_config = MongoConfig()
celery_extra_config = CeleryConfig()
