from contextlib import asynccontextmanager

from fastapi import FastAPI
from app.views.event import router as event_router
from app.views.sync import router as sync_router
from app.database.db_constructor import db_constructor
from app.services.event_provider import EventsProviderClient
from app.services.sync import run_auto_sync
import asyncio
import aiohttp


async def background_sync():
    while True:
        async with db_constructor.session_factory() as session:
            async with aiohttp.ClientSession() as http_session:
                client = EventsProviderClient(session=http_session)
                await run_auto_sync(session=session, client=client)
            await asyncio.sleep(60 * 60 * 24)


@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(background_sync())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)
app.include_router(event_router)
app.include_router(sync_router)


@app.get("/{full_path:path}")
async def custom_path(full_path: str):
    return f"Hello from LMS!\nPath: /{full_path}"
