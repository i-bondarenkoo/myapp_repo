import asyncio
from app.services.sync import run_auto_sync
from app.database.db_constructor import db_constructor

# from app.views.helpers import get_http_session
from app.services.event_provider import EventsProviderClient


from contextlib import asynccontextmanager
import aiohttp


@asynccontextmanager
async def get_http_session():
    async with aiohttp.ClientSession() as session:
        yield session


async def test():
    async with db_constructor.session_factory() as session:
        async with get_http_session() as http:
            client = EventsProviderClient(http)
            result = await run_auto_sync(session, client)
            print(result)


asyncio.run(test())
