from datetime import datetime
from app.services.event_provider import EventsProviderClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.models.place import Place
from sqlalchemy import select
import uuid


async def sync_events(
    client: EventsProviderClient,
    session: AsyncSession,
    changed_at: str = "2020-01-01",
):
    data = await client.get_events(changed_at=changed_at)
    events: dict = data.get("results", [])
    unique_places: dict = {}
    for item in events:
        place_data = item.get("place")
        place_id = place_data["id"]
        if place_id not in unique_places:
            unique_places[place_id] = place_data

    for place_id, place_data in unique_places.items():
        place_db = await check_place(session=session, place_id=place_id)
        if place_db is None:
            place_orm = Place(
                id=place_data["id"],
                name=place_data["name"],
                city=place_data["city"],
                address=place_data["address"],
            )
            session.add(place_orm)
    for item in events:
        place_data = item.get("place")
        event_id = item["id"]
        event_db = await check_event(session=session, event_id=event_id)
        if event_db is None:
            event_orm = Event(
                id=item["id"],
                name=item["name"],
                event_time=datetime.fromisoformat(item["event_time"]),
                registration_deadline=datetime.fromisoformat(
                    item["registration_deadline"]
                ),
                status=item["status"],
                number_of_visitors=item["number_of_visitors"],
                place_id=place_data["id"],
            )
            session.add(event_orm)

    await session.commit()
    return len(events)


async def check_place(
    session: AsyncSession,
    place_id: uuid.UUID,
):
    stmt = select(Place.id).where(Place.id == place_id)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()


async def check_event(
    session: AsyncSession,
    event_id: uuid.UUID,
):
    stmt = select(Event.id).where(Event.id == event_id)
    result = await session.execute(stmt)
    return result.scalars().one_or_none()
