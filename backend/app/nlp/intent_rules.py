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
        re.compile(r"\b(billing|invoice|payment|charged?|charge|declined|card|subscription|membership|cost|price|fee)\b"),
        re.compile(r"\b(double[-\s]?charge|charged\s+twice|duplicate\s+charge)\b"),
        re.compile(r"\b(credit card|debit|paypal|payment method|visa|mastercard|amex)\b"),
        re.compile(r"\b(monthly|annual|plan|tier|upgrade|discount|student)\b"),
    ],
    "refund_cancellation": [
        re.compile(r"\b(refund|cancel(?:led|lation)?|chargeback|money back)\b"),
        re.compile(r"\b(pause|freeze|suspend|hold|stop)\b"),
        re.compile(r"\b(delete|remove|close)\s+(account|membership)\b"),
    ],
    "auth_login": [
        re.compile(r"\b(log ?in|sign ?in|password|2fa|mfa|authenticator|locked out)\b"),
        re.compile(r"\b(cannot|can't)\s+(log|sign)\s*in\b"),
        re.compile(r"\b(reset|forgot|change)\s+password\b"),
        re.compile(r"\b(account\s+locked|suspended|blocked|unauthorized|hacked|compromised)\b"),
    ],
    "account_management": [
        re.compile(r"\b(change|update|edit)\s+(email|account|profile|name)\b"),
        re.compile(r"\b(delete|remove|close)\s+(account|profile)\b"),
        re.compile(r"\b(family\s+plan|multiple\s+profiles|upgrade|downgrade)\b"),
        re.compile(r"\b(privacy|sharing|notification)\s+settings\b"),
    ],
    "bug_issue": [
        re.compile(r"\b(bug|error|crash|exception|500|timeout|stacktrace|broken|not working|does not work|doesnt work)\b"),
        re.compile(r"\b(slow|laggy|freezing|loading|performance)\b"),
        re.compile(r"\b(data\s+(lost|missing|disappeared)|workout\s+tracker|not\s+recording)\b"),
        re.compile(r"\b(app\s+crash|wont\s+(play|load|sync)|will not\s+(play|load|sync)|notifications?\s+not\s+working)\b"),
        re.compile(r"\b(barcode\s+scanner|video\s+wont\s+play|video\s+will not\s+play|cache|offline)\b"),
    ],
    "usage_howto": [
        re.compile(r"\b(how\s+do\s+i|how to|where can i|steps to|guide|tutorial)\b"),
        re.compile(r"\b(track|log|create|book|share|sync)\b"),
        re.compile(r"\b(workout|exercise|class|gym|location|hours|amenities)\b"),
        re.compile(r"\b(nutrition|calories|meal\s+plan|barcode)\b"),
        re.compile(r"\b(devices|compatibility|offline|personal\s+trainer)\b"),
        re.compile(r"\b(parking|equipment|video\s+tutorial|demonstration)\b"),
    ],
    "feature_request": [
        re.compile(r"\b(feature|roadmap|request|please add|can you add|suggestion|improvement)\b"),
        re.compile(r"\b(webhooks?|integration|dark ?mode|idea)\b"),
    ],
}

def rule_intent(text: str) -> Optional[str]:
    t = normalize(text)
    for intent, patterns in _INTENT_PATTERNS.items():
        for p in patterns:
            if p.search(t):
                return intent
    return None
