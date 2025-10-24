import uuid
from datetime import datetime, timezone
from http import HTTPStatus
from typing import List

from fastapi import APIRouter, File, Request, Response, UploadFile
from loguru import logger

from src.db.conn import get_db_session
from src.models.api import UploadError, UploadResponse
from src.models.db import Image
from src.settings import Settings

upload_router = APIRouter(prefix='/upload', tags=['upload'])


@upload_router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=List[UploadResponse | UploadError],
)
async def upload_image(
    request: Request, response: Response, images: List[UploadFile] = File(...)
) -> List[UploadResponse | UploadError]:
    s3 = request.app.state.s3
    uploaded_images = []
    settings = Settings()

    for image in images:
        image_name = image.filename
        file_extension = image_name.split('.')[-1].lower()

        if file_extension not in settings.ALLOWED_EXTENSIONS:
            logger.warning(f'Invalid format for {image_name}')
            uploaded_images.append(
                UploadError(image_name=image_name, reason='Invalid format')
            )
            continue

        try:
            image_id = str(uuid.uuid4())
            file_key = f'images/{image_id}'
            contents = await image.read()
            metadata = {
                'OriginalFilename': image.filename,
                'UploadTimestamp': str(datetime.now(timezone.utc).isoformat()),
                'ContentLength': str(len(contents)),
            }

            logger.info(f'Starting upload from {image_name}')

            s3.put_object(
                Bucket=settings.BUCKET_NAME,
                Key=file_key,
                Body=contents,
                ContentType=image.content_type,
                Metadata=metadata,
            )

            image_url = f'https://{settings.BUCKET_NAME}.s3.{settings.AWS_DEFAULT_REGION}.amazonaws.com/{file_key}'
            uploaded_images.append(
                UploadResponse(image_id=image_id, url=image_url)
            )
            logger.info(f'Upload finished for {image_name}')

            db_image = Image(
                image_name=image_name, image_id=image_id, url=image_url
            )
            
            with get_db_session() as s:
                s.add(db_image)

        except Exception as e:
            logger.error(f'Upload failed for {image_name}: {str(e)}')
            uploaded_images.append(
                UploadError(image_name=image_name, reason='Internal error')
            )

    has_errors = any(isinstance(r, UploadError) for r in uploaded_images)
    if has_errors:
        response.status_code = HTTPStatus.MULTI_STATUS

    return uploaded_images
