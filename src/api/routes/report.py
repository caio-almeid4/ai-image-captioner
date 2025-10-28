from http import HTTPStatus

from fastapi import APIRouter, Request, Response
from sqlalchemy import select

from src.db.connection import get_db_session
from src.graph.graph import graph_app
from src.models.api import Report, ReportError
from src.models.db import Image
from src.settings import Settings

report_router = APIRouter(prefix='/report', tags=['report'])


@report_router.post(
    '/{image_id}',
    status_code=HTTPStatus.CREATED,
    response_model=Report | ReportError,
)
async def create_report(request: Request, response: Response, image_id: str):
    with get_db_session() as session:
        image_exists = session.scalar(
            select(Image).where(Image.image_id == image_id)
        )

    if not image_exists:
        response.status_code = HTTPStatus.NOT_FOUND
        return ReportError(reason='Image not found. Verify the ID.')

    s3 = request.app.state.s3
    temp_url = s3.generate_presigned_url(
        'get_object',
        Params={'Bucket': Settings().BUCKET_NAME, 'Key': f'images/{image_id}'},
        ExpiresIn=600,
    )

    response = graph_app.invoke({'image_url': temp_url})
    report = response['report']
    report.image_id = image_id

    return report
