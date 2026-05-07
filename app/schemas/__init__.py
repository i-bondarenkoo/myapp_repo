__all__ = (
    "ResponsePlaces",
    "ResponseEventsWithPlaces",
    "ResponseOutAPIWithPlaces",
    "ResponsePlacesModel",
    "ResponseEventWithPlaceById",
    "ResponseEventByIdAndSeats",
    "RegisterOnEvent",
    "ResponseForRegisterOnEvent",
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

ResponseEventsWithPlaces.model_rebuild()
ResponseOutAPIWithPlaces.model_rebuild()
ResponseEventWithPlaceById.model_rebuild()
