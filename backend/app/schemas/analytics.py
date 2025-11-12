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
    """Model accuracy metrics with per-field breakdown"""
    # Per-field accuracy (0.0 to 1.0)
    intent_accuracy: float
    sentiment_accuracy: float
    priority_accuracy: float
    overall_accuracy: float
    
    # Per-field counts
    intent_accepted: int
    intent_corrected: int
    sentiment_accepted: int
    sentiment_corrected: int
    priority_accepted: int
    priority_corrected: int
    
    # Total feedback
    total_feedback: int
