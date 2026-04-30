from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import UUID, String, DateTime, ForeignKey
from datetime import datetime
from enum import Enum
from sqlalchemy import Enum as sql_alchEnum
from sqlalchemy import func


class EventStatus(str, Enum):
    new = "new"
    published = "published"
    deprecated = "deprecated"


class Event(Base):
    __tablename__ = "events"
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    place_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("places.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(
        String(60),
    )
    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )
    registration_deadline: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
    )
    status: Mapped[EventStatus] = mapped_column(sql_alchEnum(EventStatus))
    number_of_visitors: Mapped[int] = mapped_column(default=0)
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
    status_changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now,
        server_default=func.now(),
    )
