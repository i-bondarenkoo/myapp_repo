from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.database.db_constructor import db_constructor
from app.services.event_provider import EventsProviderClient
from app.services.sync import sync_events
from app.views.helpers import get_http_session

router = APIRouter(
    tags=["Sync Data"],
)


@router.post("/api/sync/trigger/")
async def sync_trigger(
    session: AsyncSession = Depends(db_constructor.get_session),
    http_session=Depends(get_http_session),
    changed_at=Query(default="2000-01-01"),
):
    client = EventsProviderClient(http_session)

    count = await sync_events(
        client=client,
        session=session,
        changed_at=changed_at,
    )

    return {
        "status": "ok",
        "synced": count,
    }
