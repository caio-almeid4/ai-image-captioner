from contextlib import asynccontextmanager

import boto3
from fastapi import FastAPI
from loguru import logger

from src.api.routes.upload import upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.s3 = boto3.client('s3')
    logger.info('Cliente S3 criado')
    yield

    app.state.s3.close()
    logger.info('Cliente S3 encerrado')


app = FastAPI(lifespan=lifespan)
app.include_router(upload_router)
