import re
from typing import Literal

Priority = Literal["P1","P2","P3"]

CRITICAL_INTENTS = {"billing", "auth_login", "outage_status"}
ESCALATION_KEYWORDS = [
    "urgent", "immediately", "can't access", "cant access", "service down",
    "locked out", "double charged", "payment failed"
]

def choose_priority(intent: str, sentiment: str, low_confidence: bool, text: str) -> Priority:
    text_lower = text.lower()

    # P1 hard rules
    if intent == "outage_status":
        return "P1"
    if sentiment == "negative" and intent in {"billing", "auth_login"}:
        return "P1"
    if any(k in text_lower for k in ESCALATION_KEYWORDS):
        return "P1"

    # P2
    if sentiment == "negative" and intent in {"bug_issue", "refund_cancellation"}:
        return "P2"
    if sentiment == "neutral" and intent in {"billing", "auth_login"}:
        return "P2"
    if low_confidence and intent != "feature_request":
        return "P2"

    # Else P3
    return "P3"
