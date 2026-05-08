from pydantic import BaseModel
import uuid


class CreateTicket(BaseModel):
    event_id: uuid.UUID
    ticket_id: uuid.UUID
