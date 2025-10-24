from http import HTTPStatus
from typing import List

from fastapi import APIRouter, File, Request, Response, UploadFile
from loguru import logger

from src.models.api import UploadError, UploadResponse
from src.settings import Settings


report_router = APIRouter(prefix='/report', tags=['report'])


report_router.post('/{image_id}')
async def create_report(image_id: str):
    
    pass
