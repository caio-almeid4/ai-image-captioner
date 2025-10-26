from typing import List

from pydantic import BaseModel


class UploadResponse(BaseModel):
    image_id: str
    url: str
    status: str = 'Done'


class UploadError(BaseModel):
    image_name: str
    status: str = 'Failed'
    reason: str


class Report(BaseModel):
    image_id: str
    caption: str
    tags: List[str]


class ReportError(BaseModel):
    reason: str
