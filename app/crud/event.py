from sqlalchemy.ext.asyncio import AsyncSession

from datetime import datetime
from app.models.event import Event
from sqlalchemy import select, Result, text
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from fastapi import Request


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


async def make_response_data(
    date_from: datetime,
    session: AsyncSession,
    page: int = 1,
    page_size: int = 20,
):
    stmt = (
        select(func.count("*")).select_from(Event).where(Event.event_time >= date_from)
    )
    result: Result = await session.execute(stmt)
    count_row: int = result.scalar()

    if page * page_size > count_row:
        next = None
    else:
        next = f"https://127.0.0.1/api/events/?page={page+1}"
    if page == 1:
        previous = None
    else:
        previous = f"https://127.0.0.1/api/events/?page={page-1}"
    return (count_row, next, previous)
