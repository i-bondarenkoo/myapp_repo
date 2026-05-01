from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from app.models.event import Event
from sqlalchemy import select, Result
from sqlalchemy.orm import joinedload


async def get_events_crud(
    date_from: datetime,
    session: AsyncSession,
    page: int = 1,
    page_size: int = 20,
):
    stmt = (
        select(Event)
        .where(Event.event_time >= date_from)
        .order_by(Event.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .options(joinedload(Event.place))
    )
    result: Result = await session.execute(stmt)
    list_events: list[Event] = result.scalars().all()
    return list_events
