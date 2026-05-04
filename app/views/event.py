from fastapi import APIRouter, Query, Depends, Path, HTTPException, status
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_constructor import db_constructor
from typing import Annotated
from app.crud import event
from app.schemas.event import ResponseOutAPIWithPlaces, ResponseEventWithPlaceById
import uuid
import aiohttp
from app.models.event import EventStatus

router = APIRouter(
    tags=["Events"],
    prefix="/api",
)


@router.get("/events/", response_model=ResponseOutAPIWithPlaces)
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
    data = await event.make_response_data(
        date_from=date_from,
        session=session,
        page=page,
        page_size=page_size,
    )
    return ResponseOutAPIWithPlaces(
        count=data[0],
        next=data[1],
        previous=data[2],
        results=list_events,
    )


@router.get("/events/{event_id}", response_model=ResponseEventWithPlaceById)
async def get_events_by_id(
    event_id: Annotated[uuid.UUID, Path(description="UUID события")],
    session: AsyncSession = Depends(db_constructor.get_session),
):
    event_by_id = await event.get_events_by_id_crud(event_id=event_id, session=session)
    if event_by_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие не найдено",
        )
    return event_by_id


async def make_session_for_request():
    async with aiohttp.ClientSession() as session:
        yield session


@router.get("/events/{event_id}/seats")
async def get_info_about_seats(
    event_id: Annotated[uuid.UUID, Path(description="UUID события")],
    session: AsyncSession = Depends(db_constructor.get_session),
    http_session=Depends(make_session_for_request),
):
    current_event = await event.get_events_by_id_crud(
        event_id=event_id,
        session=session,
    )
    if current_event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Событие не найдено",
        )
    if current_event.status != EventStatus.published:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Статус события не соответствует",
        )
    local_hostname: str = (
        # "http://student-system-events-provider-web.student-system-events-provider.svc:8000"
        "http://events-provider.dev-2.python-labs.ru"
    )
    api_path: str = f"/api/events/{event_id}/seats/"
    request_url = local_hostname + api_path
    response = await http_session.get(
        url=request_url,
        headers={"x-api-key": "SpRjfkM9eTa1Wqarl0xsup4L64FH65lQKVL8i7TGX0M"},
    )
    result = await response.json()
    return result
