import uuid
from app.models.base import Base
from sqlalchemy.orm import Mapped, mapped_column


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)

    ticket_id: Mapped[uuid.UUID]
    event_id: Mapped[uuid.UUID]
