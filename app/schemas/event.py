import uuid
from pydantic import BaseModel, ConfigDict
from app.schemas.place import ResponsePlaces
from datetime import datetime
from app.models.event import EventStatus


class ResponseEventsWithPlaces(BaseModel):
    id: uuid.UUID
    name: str
    place: "ResponsePlaces"
    event_time: datetime
    registration_deadline: datetime
    status: EventStatus
    number_of_visitors: int

    model_config = ConfigDict(from_attributes=True)
