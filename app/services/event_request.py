import uuid
from app.schemas.event import ResponseEventByIdAndSeats
from app.services.event_provider import EventsProviderClient
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)
CACHE_TTL = 30
_cache_seats = {}


async def get_seats_cached(
    event_id: uuid.UUID,
    client: EventsProviderClient,
):
    key = str(event_id)
    time_now = time.time()

    if key in _cache_seats:
        expires_at, seats = _cache_seats[key]

        if time_now < expires_at:
            logger.info("Получение данных из кэша (временного словарика)")
            return ResponseEventByIdAndSeats(
                event_id=event_id,
                available_seats=seats,
            )
    logger.info("Кэш пустой, делаем запрос в API")
    data = await get_info_outer_api(event_id=event_id, client=client)
    seats = data.available_seats
    _cache_seats[key] = (time_now + CACHE_TTL, seats)

    return data


async def get_info_outer_api(
    event_id: uuid.UUID,
    client: EventsProviderClient,
):
    data = await client.get_events_and_seats(event_id=event_id)
    # print(data)

    result = ResponseEventByIdAndSeats(
        event_id=event_id,
        available_seats=data["seats"],
    )
    return result
