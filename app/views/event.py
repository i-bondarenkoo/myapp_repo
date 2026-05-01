from fastapi import APIRouter, Query, Depends
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_constructor import db_constructor
from typing import Annotated
from app.crud import event
from app.schemas.event import ResponseEventsWithPlaces

router = APIRouter(
    tags=["Events"],
    prefix="/api",
)


@router.get("/events/", response_model=list[ResponseEventsWithPlaces])
async def get_events(
    date_from: Annotated[datetime, Query()],
    session: AsyncSession = Depends(db_constructor.get_session),
    page: Annotated[int | None, Query(ge=1)] = 1,
    page_size: Annotated[int | None, Query(ge=1)] = 20,
):
    list_events = await event.get_events_crud(
        date_from=date_from,
        session=session,
        page=page,
        page_size=page_size,
    )
    return list_events
