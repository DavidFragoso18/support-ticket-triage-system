from typing import Tuple

from transformers import pipeline

from app.core.config import settings
from app.nlp.intent_rules import normalize, rule_intent  # <-- already imported

INTENT_LABELS = [
    "billing",
    "refund_cancellation",
    "account_management",
    "auth_login",
    "bug_issue",
    "usage_howto",
    "feature_request",
    "other",
]


class NLPService:
    def __init__(self) -> None:
        self.intent_pipe = pipeline("zero-shot-classification", model=settings.hf_model_intent)
        self.sentiment_pipe = pipeline("sentiment-analysis", model=settings.hf_model_sentiment)

    INTENT_CONF_THRESHOLD = 0.55  # used to decide when rules override

    def classify_text(self, text: str) -> Tuple[str, float, str, float, bool]:
        # --- Normalize for both rules & model (helps with regex and tokenization) ---
        norm_text = normalize(text)

        # --- Intent via zero-shot model ---
        intent_result = self.intent_pipe(
            norm_text, candidate_labels=INTENT_LABELS, multi_label=False
        )
        model_intent = intent_result["labels"][0]
        model_intent_score = float(intent_result["scores"][0])

        # Check near-tie between top-2 intent scores
        near_tie = False
        if len(intent_result["scores"]) >= 2:
            delta = abs(intent_result["scores"][0] - intent_result["scores"][1])
            near_tie = delta < settings.near_tie_delta

        # --- Sentiment ---
        s = self.sentiment_pipe(norm_text)[0]  # e.g. {'label': 'NEGATIVE', 'score': 0.98}
        sentiment_label_raw = str(s["label"]).lower()
        # normalize common HF outputs to our schema
        sentiment_label = (
            "negative"
            if "neg" in sentiment_label_raw
            else (
                "positive" if "pos" in sentiment_label_raw else sentiment_label_raw
            )  # if the model can output 'neutral'
        )
        sentiment_score = float(s["score"])

        # --- Rule-based intent (domain overrides/fallbacks) ---
        rule = rule_intent(norm_text)

        # Default to model; override when confidence is low or clear rule hit
        if rule:
            if model_intent != rule and model_intent_score < self.INTENT_CONF_THRESHOLD:
                final_intent = rule
                rule_override_low = True
            else:
                # if model is confident, keep it; if not, prefer the rule
                final_intent = (
                    model_intent if model_intent_score >= self.INTENT_CONF_THRESHOLD else rule
                )
                rule_override_low = model_intent_score < self.INTENT_CONF_THRESHOLD
        else:
            final_intent = model_intent
            rule_override_low = model_intent_score < self.INTENT_CONF_THRESHOLD

        # --- Low-confidence flag (any of these conditions makes it low) ---
        low_conf = (
            (model_intent_score < settings.intent_low_conf)
            or (sentiment_score < settings.sentiment_low_conf)
            or near_tie
            or rule_override_low
        )

        return final_intent, model_intent_score, sentiment_label, sentiment_score, low_conf


nlp = NLPService()
