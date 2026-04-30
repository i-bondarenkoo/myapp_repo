from app.models.base import Base
import uuid
from sqlalchemy import UUID, String, DateTime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class Place(Base):
    __tablename__ = "places"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name: Mapped[str]
    city: Mapped[str]
    address: Mapped[str]
    seats_pattern: Mapped[str]
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now(),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now(),
    )
