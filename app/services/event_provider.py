import aiohttp
from app.core.config import settings
import uuid

# http://events-provider.dev-2.python-labs.ru


class EventsProviderClient:

    def __init__(
        self,
        session: aiohttp.ClientSession,
    ):
        self.session = session
        self.api_key = settings.events_api_key
        self.base_url = settings.events_base_url

    async def get_events(
        self,
        changed_at: str = "2020-01-01",
    ):

        url = f"{self.base_url}/api/events/"
        params = {"changed_at": changed_at}

        async with self.session.get(
            url=url,
            params=params,
            headers={"x-api-key": self.api_key},
        ) as response:

            return await response.json()

    async def get_events_and_seats(
        self,
        event_id: uuid.UUID,
    ):
        url = f"{self.base_url}/api/events/{event_id}/seats/"
        async with self.session.get(
            url=url,
            headers={"x-api-key": self.api_key},
        ) as response:
            return await response.json()
