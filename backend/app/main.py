from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import create_db_and_tables
from app.api.routes import tickets, classify
from app.nlp.pipeline import nlp  # ensures model loads at startup

app = FastAPI(title="AI Ticket Triage", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    # access nlp to force model load once
    _ = nlp.intent_pipe, nlp.sentiment_pipe

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(classify.router)
app.include_router(tickets.router)
