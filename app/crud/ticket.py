from app.schemas.ticket import CreateTicket
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ticket import Ticket
import uuid
from sqlalchemy import select


async def create_ticket(data_in: CreateTicket, session: AsyncSession):
    new_ticket = Ticket(**data_in.model_dump())
    session.add(new_ticket)
    await session.commit()
    await session.refresh(new_ticket)
    return new_ticket


async def get_data_by_ticket_id_crud(
    ticket_id: uuid.UUID,
    session: AsyncSession,
):
    stmt = select(Ticket).where(Ticket.ticket_id == ticket_id)
    result = await session.execute(stmt)
    ticket = result.scalars().one_or_none()
    return ticket


async def delete_ticket_crud(
    session: AsyncSession,
    ticket_id: uuid.UUID,
):
    stmt = select(Ticket).where(Ticket.ticket_id == ticket_id)
    result = await session.execute(stmt)
    current_ticket = result.scalars().one_or_none()
    if current_ticket is None:
        return None
    else:
        await session.delete(current_ticket)
        await session.commit()
    return {"200": "ok"}
