from fastapi import FastAPI
from app.views.event import router as event_router
from app.views.sync import router as sync_router

# from app.services.sync import run_auto_sync
# from app.database.db_constructor import db_constructor
# from app.views.helpers import get_http_session
# from contextlib import asynccontextmanager
# import asyncio
# from app.services.event_provider import EventsProviderClient

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     app.state.sync_task = asyncio.create_task(background_sync_loop())
#     yield

#     app.state.sync_task.cancel()
#     try:
#         await app.state.sync_task
#     except asyncio.CancelledError:
#         pass


# async def background_sync_loop():
#     """
#     Фоновая синхронизация раз в сутки
#     """
#     while True:
#         async with db_constructor.session_factory() as session:
#             async with get_http_session() as http_session:
#                 client = EventsProviderClient(http_session)

#                 try:
#                     await run_auto_sync(session, client)
#                 except Exception as e:
#                     print(f"[SYNC ERROR]: {e}")

#         await asyncio.sleep(60 * 60 * 24)


# app = FastAPI(lifespan=lifespan)
app = FastAPI()
app.include_router(event_router)
app.include_router(sync_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
