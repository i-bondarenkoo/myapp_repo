from fastapi import APIRouter, Query, Depends, Path, HTTPException, status, Body
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db_constructor import db_constructor
from typing import Annotated
from app.crud import event
from app.services.event_provider import EventsProviderClient
from app.schemas.event import ResponseOutAPIWithPlaces, ResponseEventWithPlaceById
import uuid
import aiohttp
from app.schemas.event import (
    ResponseEventByIdAndSeats,
    RegisterOnEvent,
    ResponseForRegisterOnEvent,
)
from app.services.event_request import get_seats_cached
from app.views.helpers import get_http_session

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


@router.get("/events/{event_id}/seats/", response_model=ResponseEventByIdAndSeats)
async def get_info_about_seats(
    event_id: Annotated[uuid.UUID, Path(description="UUID события")],
    http_session: aiohttp.ClientSession = Depends(get_http_session),
):
    client = EventsProviderClient(http_session)
    result = await get_seats_cached(
        event_id=event_id,
        client=client,
    )
    return result


@router.post("/events/{event_id}/register/", response_model=ResponseForRegisterOnEvent)
async def register_on_event(
    event_id: Annotated[uuid.UUID, Path(description="UUID события")],
    data_in: Annotated[RegisterOnEvent, Body(description="Данные для запроса в API")],
    http_session: aiohttp.ClientSession = Depends(get_http_session),
):
    client = EventsProviderClient(http_session)
    register_event = await client.register_on_events(event_id=event_id, data_in=data_in)
    return register_event
