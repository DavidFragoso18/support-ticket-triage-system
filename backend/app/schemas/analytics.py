from pydantic import BaseModel
from typing import Dict, List
from datetime import datetime

class AnalyticsOverview(BaseModel):
    """Overall system metrics"""
    total_tickets: int
    tickets_today: int
    avg_confidence: float
    low_confidence_count: int
    feedback_count: int

class IntentDistribution(BaseModel):
    """Distribution of intents"""
    intent: str
    count: int
    percentage: float

class SentimentDistribution(BaseModel):
    """Distribution of sentiments"""
    sentiment: str
    count: int
    percentage: float

class PriorityDistribution(BaseModel):
    """Distribution of priorities"""
    priority: str
    count: int
    percentage: float

class TimeSeriesData(BaseModel):
    """Time series data point"""
    date: str
    count: int

class ClassificationAccuracy(BaseModel):
    """Model accuracy metrics"""
    total_classifications: int
    with_feedback: int
    accepted: int
    rejected: int
    corrected: int
    accuracy_rate: float  # % accepted / (accepted + rejected + corrected)
