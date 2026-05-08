__all__ = (
    "ResponsePlaces",
    "ResponseEventsWithPlaces",
    "ResponseOutAPIWithPlaces",
    "ResponsePlacesModel",
    "ResponseEventWithPlaceById",
    "ResponseEventByIdAndSeats",
    "RegisterOnEvent",
    "ResponseForRegisterOnEvent",
    "CreateTicket",
)
from app.schemas.place import ResponsePlaces, ResponsePlacesModel
from app.schemas.event import (
    ResponseEventsWithPlaces,
    ResponseOutAPIWithPlaces,
    ResponseEventWithPlaceById,
    ResponseEventByIdAndSeats,
    RegisterOnEvent,
    ResponseForRegisterOnEvent,
)
from app.schemas.ticket import CreateTicket

ResponseEventsWithPlaces.model_rebuild()
ResponseOutAPIWithPlaces.model_rebuild()
ResponseEventWithPlaceById.model_rebuild()
