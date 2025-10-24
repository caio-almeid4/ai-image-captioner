from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Image:
    __tablename__ = 'images'

    image_id: Mapped[str] = mapped_column(primary_key=True)
    image_name: Mapped[str]
    url: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
