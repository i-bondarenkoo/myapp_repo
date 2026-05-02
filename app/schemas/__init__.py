__all__ = (
    "ResponsePlaces",
    "ResponseEventsWithPlaces",
    "ResponseOutAPIWithPlaces",
    "ResponsePlacesModel",
    "ResponseEventWithPlaceById",
)
from app.schemas.place import ResponsePlaces, ResponsePlacesModel
from app.schemas.event import (
    ResponseEventsWithPlaces,
    ResponseOutAPIWithPlaces,
    ResponseEventWithPlaceById,
)

ResponseEventsWithPlaces.model_rebuild()
ResponseOutAPIWithPlaces.model_rebuild()
ResponseEventWithPlaceById.model_rebuild()
