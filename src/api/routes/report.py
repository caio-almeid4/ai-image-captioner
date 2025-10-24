from http import HTTPStatus
from typing import List

from fastapi import APIRouter, File, Request, Response, UploadFile
from loguru import logger

from src.models.api import ReportError, Report
from src.settings import Settings
from src.db.conn import get_db_session
from sqlalchemy import select
from src.models.db import Image
import boto3


report_router = APIRouter(prefix='/report', tags=['report'])


@report_router.post('/{image_id}', status_code=HTTPStatus.CREATED, response_model=Report | ReportError)
async def create_report(request: Request, response: Response, image_id: str):
    
    with get_db_session() as session:
        image_exists = session.scalar(
            select(Image).where(Image.image_id == image_id)
    )
        
    if not image_exists:
        response.status_code = HTTPStatus.NOT_FOUND
        return ReportError(reason='Image not found. Verify the ID.')
        
    s3 = request.app.state.s3
    url = s3.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': Settings().BUCKET_NAME,
            'Key': f'images/{image_id}'
        },
        ExpiresIn=600
    )
    
    
    
    
    
    return Report(image_id=image_id, caption='', tags =['', ''])