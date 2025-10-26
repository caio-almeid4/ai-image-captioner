from contextlib import asynccontextmanager

import boto3
from botocore.config import Config
from fastapi import FastAPI
from loguru import logger

from src.api.routes.report import report_router
from src.api.routes.upload import upload_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
    logger.info('Cliente S3 criado')
    yield

    app.state.s3.close()
    logger.info('Cliente S3 encerrado')


app = FastAPI(lifespan=lifespan)
app.include_router(upload_router)
app.include_router(report_router)
