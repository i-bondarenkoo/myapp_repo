from sqlalchemy import select
from app.models.sync_meta_table import SyncMetaTable
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from app.models.event import Event
from app.models.place import Place
from datetime import datetime


async def get_sync_meta_obj(
    session: AsyncSession,
):
    stmt = select(SyncMetaTable)
    result = await session.execute(stmt)
    sync_meta_obj = result.scalars().first()
    return sync_meta_obj


async def update_sync_meta_obj(
    sync_meta_obj: SyncMetaTable,
    session: AsyncSession,
):
    update_dict: dict = {}
    update_dict["last_changed_at"] = datetime.now()
    update_dict["last_sync_time"] = datetime.now()
    update_dict["status"] = "ok"
    for k, v in update_dict.items():
        setattr(sync_meta_obj, k, v)
    await session.commit()
    return sync_meta_obj


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
