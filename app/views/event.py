from fastapi import APIRouter, Query, Depends
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_constructor import db_constructor
from typing import Annotated
from app.crud import event
from app.schemas.event import ResponseOutAPIWithPlaces
from fastapi import Request

router = APIRouter(
    tags=["Events"],
    prefix="/api",
)


@router.get("/events/", response_model=ResponseOutAPIWithPlaces)
async def get_events(
    request: Request,
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
    data = await event.make_response_data(
        date_from=date_from,
        session=session,
        page=page,
        page_size=page_size,
        request=request,
    )
    return ResponseOutAPIWithPlaces(
        count=data[0],
        next=data[1],
        previous=data[2],
        results=list_events,
    )
