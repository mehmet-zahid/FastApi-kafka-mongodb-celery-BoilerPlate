from loguru import logger
import aiokafka
import json
from config import kafka_config


class KafkaClient:
    def __init__(self, bootstrap_servers: str, consumer_topic: str = None) -> None:
        self.bootstrap_servers = bootstrap_servers
        self.consumer_topic = consumer_topic
        self.producer = None

    async def setup_kafka_consumer(self):
        try:
            logger.info("Starting Kafka Consumer ...")
            consumer = aiokafka.AIOKafkaConsumer(
                self.consumer_topic,
                bootstrap_servers=self.bootstrap_servers,
                # value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                # auto_offset_reset="earliest",
            )
            await consumer.start()
            logger.info("Kafka Consumer started")
            self.consumer = consumer

        except aiokafka.errors.KafkaConnectionError as e:
            logger.error(f"Kafka Connection Error: {e}")
            await consumer.stop()

    async def setup_kafka_producer(self):
        try:
            logger.info("Starting Kafka Producer ...")
            producer = aiokafka.AIOKafkaProducer(
                bootstrap_servers=self.bootstrap_servers,
            )
            await producer.start()
            logger.info("Kafka Producer started")
            self.producer = producer

        except aiokafka.errors.KafkaConnectionError as e:
            logger.error(f"Kafka Connection Error: {e}")
            await producer.stop()
            logger.info("Kafka Producer stopped")
            raise e

    async def produce(
        self, topic: str, jsonMessage: str = None, messageAsObject: dict = None
    ):
        if messageAsObject:
            msg: bytes = json.dumps(messageAsObject).encode("utf-8")
        elif jsonMessage:
            msg: bytes = jsonMessage.encode("utf-8")
        else:
            raise ValueError("Either jsonMessage or messageAsObject must be provided")

        await self.producer.send_and_wait(topic, msg)
        await self.producer.flush()
        logger.info("Message sent to kafka")

    async def consume(self):
        async for msg in self.consumer:
            yield msg.value.decode("utf-8")
            # logger.info(type(msg.value)) # <class 'aiokafka.structs.ConsumerRecord'>

    async def consume_with_count(self, count: int):
        """
        Consumes `count` messages from the topic and then returns"""
        for i in range(count):
            msg = await self.consumer.getone()
            yield msg.value.decode("utf-8")
            # logger.info(f'Consumed: {msg.value}')
            # logger.info(type(msg.value)) # <class 'aiokafka.structs.ConsumerRecord'>


# as an example of how to use kafka producer client in our fastapi application
# we create an instance of KafkaClient for producer setup
# we will call setup call for producer in our init_services hook
kafkam = KafkaClient(kafka_config.KAFKA_BOOTSTRAP_SERVER)
