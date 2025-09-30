import re
from typing import Optional

# Normalize text a bit (lower/punct/whitespace)
def normalize(text: str) -> str:
    t = text.lower()
    t = re.sub(r"[_\-\.,:;!?\(\)\[\]\{\}<>#\$%&/\\]+", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t

# Domain patterns → intent
_INTENT_PATTERNS: dict[str, list[re.Pattern]] = {
    "billing": [
        re.compile(r"\b(billing|invoice|payment|charged|charge|declined|card|subscription)\b"),
        re.compile(r"\b(double[-\s]?charge|charged\s+twice|duplicate\s+charge)\b"),
    ],
    "refund_cancellation": [
        re.compile(r"\b(refund|cancel(?:led|lation)?|chargeback|money back)\b"),
    ],
    "auth_login": [
        re.compile(r"\b(log ?in|sign ?in|password|2fa|mfa|authenticator|locked out)\b"),
        re.compile(r"\b(cannot|can't)\s+(log|sign)\s*in\b"),
    ],
    "bug_issue": [
        re.compile(r"\b(bug|error|crash|exception|500|timeout|stacktrace|broken|not working|doesn'?t work)\b"),
        re.compile(r"\b(data leak|breach|security|exposed)\b"),  # treat security incidents as bug/issue
    ],
    "outage_status": [
        re.compile(r"\b(outage|down|unavailable|status\s*page|incident|major incident|all users)\b"),
    ],
    "usage_howto": [
        re.compile(r"\b(how\s+do\s+i|how to|where can i|steps to|guide|tutorial|export|download)\b"),
    ],
    "feature_request": [
        re.compile(r"\b(feature|roadmap|request|please add|can you add|webhooks?|integration|dark ?mode)\b"),
    ],
    "account_management": [
        re.compile(r"\b(change|update|edit)\s+(email|account|profile|name)\b"),
    ],
    "shipping_delivery": [
        re.compile(r"\b(shipping|delivery|package|tracking|order)\b"),
    ],
}

def rule_intent(text: str) -> Optional[str]:
    t = normalize(text)
    for intent, patterns in _INTENT_PATTERNS.items():
        for p in patterns:
            if p.search(t):
                return intent
    return None
