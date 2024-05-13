from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import router as auth_router
from routes.job import router as job_router

from loguru import logger
from services.hooks import init_services, stop_services


logger.add("../logs/server.error.log", rotation="500 MB", level="ERROR")
logger.add("../logs/server.log", rotation="500 MB", level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await init_services()
        yield
        await stop_services()
    except Exception as e:
        await stop_services()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"mesaj": "Merhaba, FastAPI'ye hoşgeldiniz!"}


app.include_router(auth_router)
app.include_router(job_router)
