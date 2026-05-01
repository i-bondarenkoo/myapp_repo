__all__ = (
    "ResponsePlaces",
    "ResponseEventsWithPlaces",
)
from app.schemas.place import ResponsePlaces
from app.schemas.event import ResponseEventsWithPlaces


ResponseEventsWithPlaces.model_rebuild()
