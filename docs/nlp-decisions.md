# NLP Decisions (Draft)

**Status:** Locked for v0 (Hugging Face pipelines).  
**Last updated:** 2025-09-10

## 1) Summary
We will use Hugging Face pipelines for the initial release (v0) to ship faster and support multilingual inputs (EN/PT). We may migrate selected parts to spaCy later for lower latency once labels are stable and traffic increases.

- **Intent (zero‑shot):** `facebook/bart-large-mnli`
- **Sentiment:** `cardiffnlp/twitter-roberta-base-sentiment-latest`

## 2) Target Outputs
Every classification returns:
- `intent` (one of our labels; or `unknown`)
- `intent_confidence` (0–1)
- `sentiment` (`negative`, `neutral`, `positive`)
- `sentiment_confidence` (0–1)
- `priority` (`low`, `medium`, `high`, `urgent`)
- `priority_score` (0–1)

## 3) Intent Labels (v0 set)
These labels are used with the zero‑shot classifier (BART‑MNLI). They can be revised as data grows.

- `billing_issue`
- `payment_failed`
- `refund_request`
- `subscription_cancel`
- `login_problem`
- `account_change`
- `bug_report`
- `outage_or_service_down`
- `technical_support`
- `feature_request`
- `general_question`

### Label wording guidance for zero‑shot
Use human‑readable templates mapped to the label ids above, e.g.:
- *"This ticket is about a billing issue."* → `billing_issue`
- *"This ticket is about a failed payment."* → `payment_failed`
- *"This ticket requests a refund."* → `refund_request`
- *"This ticket is about canceling a subscription."* → `subscription_cancel`
- *"This ticket is about login problems."* → `login_problem`
- *"This ticket is about changing account details."* → `account_change`
- *"This ticket reports a software bug."* → `bug_report`
- *"This ticket reports an outage or service being down."* → `outage_or_service_down`
- *"This ticket asks for technical support."* → `technical_support`
- *"This ticket asks for a new feature."* → `feature_request`
- *"This ticket is a general question."* → `general_question`

## 4) Thresholds & Confidence Rules
**Intent (zero‑shot via BART‑MNLI):**
- `min_intent_score` = **0.50**
- `min_margin_over_second_best` = **0.10** (winner score minus runner‑up score)
- If either condition fails → set `intent = "unknown"` and keep `intent_confidence = winner_score`.

**Sentiment (Twitter RoBERTa latest):**
- Use the top label of `{negative, neutral, positive}` and its probability as `sentiment_confidence`.
- No additional thresholding (always emit a sentiment).

**Language hint:**
- If input language is obviously PT (heuristic or UI hint), still use the same models; both are reasonably robust on EN/PT for v0.

## 5) Priority Logic (Deterministic Rules)
We compute both a categorical `priority` and a numeric `priority_score` (0–1).  
Start from a **base** score using sentiment, then **adjust** with intent and keywords.

### 5.1 Base priority from sentiment
- `negative` → base = **0.70**
- `neutral`  → base = **0.50**
- `positive` → base = **0.30**

### 5.2 Adjustments by intent (add to base)
- `outage_or_service_down` → **+0.25**; min priority at least **high**
- `payment_failed` → **+0.20**
- `billing_issue` → **+0.15**
- `refund_request` → **+0.10**
- `bug_report` or `technical_support` → **+0.10**
- `subscription_cancel` → **+0.05**
- `feature_request` → **-0.10**
- `general_question` → **-0.05**
- `unknown` → **0.00**

### 5.3 Keyword escalations (case‑insensitive; anywhere in text)
- If contains any of: "down", "outage", "offline", "critical", "production" → **+0.10**
- If contains any of: "charged twice", "duplicate charge", "payment declined", "invoice error" → **+0.10**
- If contains any of: "security", "data leak", "breach", "fraud" → **+0.20** and min priority **urgent**
- If contains profanity/abuse (basic lexicon) → **+0.05** (indicates heat/urgency)

### 5.4 Clamp and map to categorical levels
- Clamp `priority_score` to [0.0, 1.0].
- Map to `priority`:
  - `>= 0.85` → **urgent**
  - `>= 0.70` → **high**
  - `>= 0.50` → **medium**
  - else → **low**

## 6) Failure / Fallback Behavior
- Empty or very short text (< 5 tokens): set `intent = "unknown"`, `intent_confidence = 0`, keep sentiment; set `priority` from sentiment only.
- If model call fails: return `intent = "unknown"`, `sentiment = "neutral"`, `priority = "medium"`, `priority_score = 0.50` and log error.

## 7) Re‑classification Policy
- Re‑run classification on edits to ticket `subject` or `body`.
- Keep a history in `ticket_classifications` (append only) with timestamps to track changes over time.

## 8) Versioning
- **NLP profile id:** `nlp_v0_hf`
- Intent model: `facebook/bart-large-mnli`
- Sentiment model: `cardiffnlp/twitter-roberta-base-sentiment-latest`
- Changing thresholds or labels increments profile (`nlp_v1_*`).

## 9) Future (when moving parts to spaCy)
- Train a spaCy `textcat` on our intent labels once we have ≥ 500 labeled tickets per high‑traffic intent.
- Swap in spaCy for NER and rule‑based cleaning to cut latency and memory usage.
