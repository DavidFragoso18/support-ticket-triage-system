from pydantic import BaseModel
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    app_env: str = "local"
    log_level: str = "INFO"
    allowed_origins: List[str] = ["http://localhost:5173"]

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/triage"

    hf_model_intent: str = "facebook/bart-large-mnli"
    hf_model_sentiment: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    intent_low_conf: float = 0.50
    sentiment_low_conf: float = 0.60
    near_tie_delta: float = 0.05

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
