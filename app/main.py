from fastapi import FastAPI
from app.views.event import router as event_router

app = FastAPI()
app.include_router(event_router)


@app.get("/health")
async def health():
    return {"status": "ok"}
