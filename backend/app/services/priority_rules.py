from typing import Literal, Optional

Priority = Literal["P1", "P2", "P3"]

_P1_PHRASES = {
    "double charge",
    "charged twice",
    "duplicate charge",
    "fraud",
    "unauthorized charge",
    "down",
    "outage",
    "service down",
    "status page",
    "cannot login",
    "can't login",
    "locked out",
    "data leak",
    "breach",
    "security incident",
}


def _contains(text: str, phrases: set[str]) -> bool:
    t = text.lower()
    return any(ph in t for ph in phrases)


def choose_priority(intent: Optional[str], sentiment: Optional[str], text: str) -> Priority:
    t = text.lower()
    intent = (intent or "other").lower()
    sentiment = (sentiment or "neutral").lower()

    # Hard P1: safety/availability/financial + explicit phrasing
    if _contains(t, _P1_PHRASES):
        return "P1"
    if intent in {"outage_status"}:
        return "P1"
    if intent == "auth_login" and ("cannot" in t or "can't" in t or "locked out" in t):
        return "P1"
    if intent == "billing" and _contains(
        t, {"double charge", "charged twice", "fraud", "unauthorized"}
    ):
        return "P1"

    # Negative sentiment escalates
    if sentiment == "negative":
        if intent in {"billing", "auth_login", "bug_issue", "outage_status"}:
            return "P1"
        return "P2"

    # Neutral/positive defaults by domain
    if intent in {"billing", "auth_login", "bug_issue"}:
        return "P2"
    return "P3"
