# FastApi Project Template with jwt authentication, celery task management, kafka producer and consumer clients, mongodb database, docker-compose, and more.

## Features

- FastApi
- Pydantic
- Celery
- Kafka
- MongoDB
- Redis
- JWT
- Docker
- Docker Compose


## Requirements

- If you want to use kafka, ensure that kafka is ready to use. (you should set the external kafka server address in compose file 'KAFKA_CFG_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092,EXTERNAL://<`host_addr`>:9094'. host_addr is the host address of the kafka server) . if you do not use kafka from outside and only use it betwwen containers, you can use only  'KAFKA_CFG_ADVERTISED_LISTENERS: PLAINTEXT://kafka:9092' in compose file, no need to use EXTERNAL.

- If you want to use mongodb, ensure that mongodb is ready to use and set the  mongodb credentials in compose file. and set `MONGO_URI` in .env file with the credentials. set also `MONGO_DB_NAME` in .env file with the database name.