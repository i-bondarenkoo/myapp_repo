import asyncio
from app.database.db_constructor import db_constructor
from app.models.event import Event, EventStatus
from app.models.place import Place
import uuid
from datetime import datetime


async def main():
    async with db_constructor.session_factory() as session:
        place1 = Place(
            name="Площадка в Сокольниках",
            city="Москва",
            address="ул. Ленина, д. 1",
            seats_pattern="A1-250",
        )
        session.add(place1)
        await session.flush()
        event1 = Event(
            place_id=place1.id,
            name="Тестовое событие 1",
            event_time=datetime.now(),
            registration_deadline=datetime.now(),
            status=EventStatus.published,
            number_of_visitors=3,
        )
        session.add(event1)
        await session.flush()
        await session.commit()


if __name__ == "__main__":
    asyncio.run(main())
