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
            if response.status != 200:
                raise Exception("Ошибка на стороне внешнего API")
            return await response.json()

    async def register_on_events(self, event_id: uuid.UUID, data_in):
        url = f"{self.base_url}/api/events/{event_id}/register/"

        json_data = {
            "first_name": data_in.first_name,
            "last_name": data_in.last_name,
            "email": data_in.email,
            "seat": data_in.seat,
        }

        async with self.session.post(
            url=url,
            json=json_data,
            headers={"x-api-key": self.api_key},
        ) as response:

            text = await response.text()

            if response.status != 201:
                raise Exception(f"API error {response.status}: {text}")

            return await response.json()
