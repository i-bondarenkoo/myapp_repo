import uuid
from pydantic import BaseModel, ConfigDict, EmailStr
from app.schemas.place import ResponsePlaces, ResponsePlacesModel
from datetime import datetime


class ResponseEventsWithPlaces(BaseModel):
    id: uuid.UUID
    name: str
    place: "ResponsePlaces"
    event_time: datetime
    registration_deadline: datetime
    status: str
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
    status: str
    number_of_visitors: int


class ResponseEventByIdAndSeats(BaseModel):
    event_id: uuid.UUID
    available_seats: list[str]

    model_config = ConfigDict(from_attributes=True)


class RegisterOnEvent(BaseModel):
    # event_id: uuid.UUID
    first_name: str
    last_name: str
    email: EmailStr
    seat: str


class ResponseForRegisterOnEvent(BaseModel):
    ticked_id: uuid.UUID
