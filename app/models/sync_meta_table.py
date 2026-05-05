from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from sqlalchemy.sql import func


class SyncMetaTable(Base):
    __tablename__ = "sync_meta_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    last_changed_at: Mapped[datetime]
    last_sync_time: Mapped[datetime] = mapped_column(server_default=func.now())
    status: Mapped[str]
