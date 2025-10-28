from fastapi import APIRouter

from src.api.routes.report import report_router
from src.api.routes.upload import upload_router

router = APIRouter()
router.include_router(report_router)
router.include_router(upload_router)
