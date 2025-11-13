from typing import List

from pydantic import BaseModel


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
    total_feedback: int


class AgentPerformance(BaseModel):
    """Agent performance metrics"""

    agent_id: str
    tickets_claimed: int
    tickets_resolved: int
    avg_resolution_time_seconds: float
    total_active_time_seconds: float
    feedback_given: int
    avg_feedback_rating: float


class TrendData(BaseModel):
    """Ticket trends over time"""

    date: str
    total_tickets: int
    high_priority: int
    resolved: int
    avg_resolution_time: float


class AnalyticsDashboard(BaseModel):
    """Complete analytics dashboard data"""

    overview: AnalyticsOverview
    intent_distribution: List[IntentDistribution]
    sentiment_distribution: List[SentimentDistribution]
    priority_distribution: List[PriorityDistribution]
    trends: List[TrendData]
    top_agents: List[AgentPerformance]
    model_accuracy: ClassificationAccuracy

    # Total feedback
    total_feedback: int
