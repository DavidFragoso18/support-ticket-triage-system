
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import (
    analytics,
    classify,
    feedback,
    kb,
    llm,
    resolutions,
    search,
    suggestions,
    tickets,
    websocket,
)
from app.core.config import settings
from app.db.base import create_db_and_tables
from app.nlp.pipeline import nlp  # ensures model loads at startup
from app.services.websocket_manager import manager

app = FastAPI(title="AI Ticket Triage", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()
    # access nlp to force model load once
    _ = nlp.intent_pipe, nlp.sentiment_pipe
    # Initialize Redis for WebSocket pub/sub
    await manager.connect_redis()

@app.on_event("shutdown")
async def on_shutdown():
    # Clean up Redis connection
    await manager.disconnect_redis()

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(classify.router)
app.include_router(tickets.router)
app.include_router(suggestions.router)
app.include_router(kb.router)
app.include_router(resolutions.router)
app.include_router(feedback.router)
app.include_router(analytics.router)
app.include_router(search.router)
app.include_router(websocket.router)
app.include_router(llm.router)
