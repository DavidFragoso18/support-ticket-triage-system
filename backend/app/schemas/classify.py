from pydantic import BaseModel
from typing import Optional

class ClassifyIn(BaseModel):
    text: str
    language: Optional[str] = None

class ClassifyOut(BaseModel):
    intent: str
    sentiment: str
    priority: str
    confidence: float
    low_confidence: bool
