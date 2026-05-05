from fastapi import FastAPI
from app.views.event import router as event_router
from app.views.sync import router as sync_router

app = FastAPI()
app.include_router(event_router)
app.include_router(sync_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
