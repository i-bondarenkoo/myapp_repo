from datetime import datetime
from app.services.event_provider import EventsProviderClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.dependencies import get_sync_meta_obj, update_sync_meta_obj
from app.models.event import Event
from app.models.place import Place
from app.models.sync_meta_table import SyncMetaTable
from app.services.dependencies import check_place, check_event

# from sqlalchemy import select


async def sync_events(
    client: EventsProviderClient,
    session: AsyncSession,
    changed_at: str = "2020-01-01",
):
    data = await client.get_events(changed_at=changed_at)

    events: list[dict] = data.get("results", [])
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
        else:
            place_db.name = place_data["name"]
            place_db.city = place_data["city"]
            place_db.address = place_data["address"]
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
        else:
            event_db.name = item["name"]
            event_db.status = item["status"]
            event_db.event_time = datetime.fromisoformat(item["event_time"])
            event_db.registration_deadline = datetime.fromisoformat(
                item["registration_deadline"]
            )
            event_db.number_of_visitors = item["number_of_visitors"]

    await session.commit()
    return len(events)


async def run_auto_sync(
    session: AsyncSession,
    client: EventsProviderClient,
):
    meta = await get_sync_meta_obj(session=session)

    if meta is None:
        changed_at = "2020-01-01"
    else:
        changed_at = meta.last_changed_at.isoformat()

    data = await sync_events(
        client=client,
        session=session,
        changed_at=changed_at,
    )
    # upd meta
    if meta:
        await update_sync_meta_obj(
            sync_meta_obj=meta,
            session=session,
        )
    else:
        meta = SyncMetaTable(
            last_changed_at=datetime.now(),
            last_sync_time=datetime.now(),
            status="sync",
        )
        session.add(meta)
        await session.commit()
    return data
