from transformers import pipeline
from app.core.config import settings
from typing import Tuple

INTENT_LABELS = [
    "billing", "auth_login", "bug_issue", "feature_request",
    "account_management", "shipping_delivery", "refund_cancellation",
    "usage_howto", "outage_status", "other"
]

class NLPService:
    def __init__(self) -> None:
        self.intent_pipe = pipeline(
            "zero-shot-classification",
            model=settings.hf_model_intent
        )
        self.sentiment_pipe = pipeline(
            "sentiment-analysis",
            model=settings.hf_model_sentiment
        )

    def classify_text(self, text: str) -> Tuple[str, float, str, float, bool]:
        # Intent (zero-shot)
        intent_result = self.intent_pipe(text, candidate_labels=INTENT_LABELS, multi_label=False)
        intent = intent_result["labels"][0]
        intent_score = float(intent_result["scores"][0])

        # Handle near-tie: if top two very close, mark as low confidence
        near_tie = False
        if len(intent_result["scores"]) >= 2:
            delta = abs(intent_result["scores"][0] - intent_result["scores"][1])
            near_tie = delta < settings.near_tie_delta

        # Sentiment
        s = self.sentiment_pipe(text)[0]  # {'label': 'Negative', 'score': 0.98}
        sentiment_label = s["label"].lower()
        sentiment_score = float(s["score"])

        # low_confidence heuristic
        low_conf = (intent_score < settings.intent_low_conf) or (sentiment_score < settings.sentiment_low_conf) or near_tie

        return intent, intent_score, sentiment_label, sentiment_score, low_conf

nlp = NLPService()
