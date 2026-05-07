__all__ = (
    "ResponsePlaces",
    "ResponseEventsWithPlaces",
    "ResponseOutAPIWithPlaces",
    "ResponsePlacesModel",
    "ResponseEventWithPlaceById",
    "ResponseEventByIdAndSeats",
)
from app.schemas.place import ResponsePlaces, ResponsePlacesModel
from app.schemas.event import (
    ResponseEventsWithPlaces,
    ResponseOutAPIWithPlaces,
    ResponseEventWithPlaceById,
    ResponseEventByIdAndSeats,
)

ResponseEventsWithPlaces.model_rebuild()
ResponseOutAPIWithPlaces.model_rebuild()
ResponseEventWithPlaceById.model_rebuild()
