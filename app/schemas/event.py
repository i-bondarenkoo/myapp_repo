import uuid
from pydantic import BaseModel, ConfigDict
from app.schemas.place import ResponsePlaces, ResponsePlacesModel
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


class ResponseOutAPIWithPlaces(BaseModel):
    count: int
    next: str | None
    previous: str | None
    results: list[ResponseEventsWithPlaces]

    model_config = ConfigDict(from_attributes=True)


class ResponseEventWithPlaceById(BaseModel):
    id: uuid.UUID
    name: str
    place: "ResponsePlacesModel"
    event_time: datetime
    registration_deadline: datetime
    status: EventStatus
    number_of_visitors: int
