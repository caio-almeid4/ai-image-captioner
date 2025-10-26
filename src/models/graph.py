from typing_extensions import TypedDict

from src.models.api import Report


class State(TypedDict):
    image_url: str
    report: Report
