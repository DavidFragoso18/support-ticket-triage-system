from pydantic import BaseModel, field_validator
from pydantic_settings import BaseSettings
from typing import List, Union

class Settings(BaseSettings):
    app_env: str = "local"
    log_level: str = "INFO"
    allowed_origins: Union[List[str], str] = ["http://localhost:5173", "http://localhost:3000"]

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/triage"
    
    @field_validator("allowed_origins", mode="before")
    @classmethod
    def parse_allowed_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    hf_model_intent: str = "facebook/bart-large-mnli"
    hf_model_sentiment: str = "cardiffnlp/twitter-roberta-base-sentiment-latest"

    intent_low_conf: float = 0.50
    sentiment_low_conf: float = 0.60
    near_tie_delta: float = 0.05

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
