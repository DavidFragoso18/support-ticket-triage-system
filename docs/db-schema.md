# Database Schema (Draft)

**Status:** Draft — descriptive model (not SQL).  
**Last updated:** 2025-09-10

This document defines the core tables for the Support Ticket Triage system and lists placeholder future tables. Types are descriptive to guide implementation.

---

## 1) `tickets`

Represents an incoming support ticket from any channel.

### Fields
- **id**: `uuid` — Unique ticket identifier (primary key).
- **subject**: `string` — Short title/summary, ~5–150 chars.
- **body**: `string` — Full message text; may be long.
- **channel**: `enum` — Where this ticket came from.  
  _Initial values (draft)_: `web_form`, `email`, `chat_widget`, `api`, `import`.
- **customer_id**: `string` — External customer identifier (email, user ID, or CRM key). Keep flexible as string.
- **language**: `string?` — Optional BCP-47 code detected or provided (e.g., `en`, `pt-PT`). Use `null` if unknown.
- **status**: `enum` — Workflow state of the ticket.  
  _Initial values (draft)_: `open`, `pending`, `resolved`, `closed`.
- **created_at**: `timestamp` — When the ticket was created (UTC, ISO-8601).
- **updated_at**: `timestamp` — When the ticket was last updated (UTC, ISO-8601).

### Notes
- **Immutability**: `subject`/`body` can change via edits; keep `updated_at` in sync.
- **Indexing**: recommend indexes on (`created_at`), (`customer_id`), and (`channel`, `created_at`) for list views; full-text index on (`subject`, `body`) if available.
- **Language**: store a single best-guess code; additional detection metadata can live in a future `nlp_meta` column if needed.
- **PII**: `customer_id` may be an email; consider hashing or separating PII if required by policy.

---

## 2) `ticket_classifications`

Stores the results of NLP or human categorization for a ticket. Multiple rows per ticket are allowed (history over time).

### Fields
- **id**: `uuid` — Unique identifier for this classification record (primary key).
- **ticket_id**: `uuid (fk)` — References `tickets.id`.
- **intent**: `enum` — Predicted ticket topic.  
  _Initial values (draft)_: `billing_issue`, `payment_failed`, `refund_request`, `subscription_cancel`, `login_problem`, `account_change`, `bug_report`, `outage_or_service_down`, `technical_support`, `feature_request`, `general_question`, `unknown`.
- **sentiment**: `enum` — Tone of the message. Allowed: `negative`, `neutral`, `positive`.
- **priority**: `enum` — Routed priority. Allowed: `low`, `medium`, `high`, `urgent`.
- **confidence**: `float` — 0–1 confidence score for `intent` (or overall classification).
- **low_confidence**: `boolean` — Convenience flag set by our thresholds (e.g., `true` if intent below minimum or margin small).
- **source**: `enum` — Who/what produced this record. Allowed: `model`, `human`, `rule`.
- **created_at**: `timestamp` — When this classification was created (UTC, ISO-8601).

### Notes
- **History**: keep **append-only** history to audit model drift or human overrides.
- **Uniqueness**: do **not** enforce one-row per ticket; newest row is current.
- **Indexing**: indexes on (`ticket_id`, `created_at DESC`) and filters on (`intent`, `priority`, `source`).
- **Confidence flag**: `low_confidence` is derived from thresholds in `docs/nlp-decisions.md` (v0: score < 0.50 or margin < 0.10).

---

## 3) Relationships

- **tickets (1) → ticket_classifications (N)** via `ticket_classifications.ticket_id`.
- Latest state for routing/UIs is the **most recent** `ticket_classifications` row per `ticket_id` by `created_at`.

---

## 4) Future Tables (placeholders)

These are not part of the core MVP but are anticipated:

- **attachments** — Files linked to tickets.  
  _Possible fields_: `id (uuid)`, `ticket_id (fk)`, `filename`, `mime_type`, `size_bytes`, `storage_url`, `created_at`.

- **users / agents** — End-users and support agents (auth & profiles).  
  _Possible fields_: `id (uuid)`, `email`, `name`, `role` (`user`, `agent`, `admin`), `created_at`, `updated_at`.

- **articles** — Knowledge base articles for suggested replies.  
  _Possible fields_: `id (uuid)`, `title`, `body`, `language`, `tags[]`, `updated_at`.

- **resolutions** — Structured outcomes for tickets.  
  _Possible fields_: `id (uuid)`, `ticket_id (fk)`, `resolution_code`, `summary`, `closed_by (agent_id)`, `closed_at`.

- **feedback_events** — Thumbs-up/down or 5-star ratings for AI suggestions or agent replies.  
  _Possible fields_: `id (uuid)`, `ticket_id (fk)`, `actor` (`user`/`agent`), `target` (`suggestion`/`reply`), `score`, `comment`, `created_at`.

---

## 5) Data Retention & Compliance (draft)

- Keep ticket text as long as required for support/audit; consider redaction for sensitive PII.  
- Classification history should be retained to evaluate model performance; consider a 12–24 month window depending on policy.
- All timestamps stored as UTC ISO-8601; application is responsible for timezone presentation.

