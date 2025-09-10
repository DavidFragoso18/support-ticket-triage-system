# Seeding Plan

**Status:** Draft — describes how we'll create initial synthetic data for local development and demos.  
**Last updated:** 2025-09-10

---

## Goal

Create a balanced synthetic dataset of ~150 support tickets to exercise the API, UI filters, and NLP pipeline.  
Target file: `data/seeds/tickets_seed.csv`

- **Volume:** ~150 rows
- **Balance:** ~10–12% per intent label (11 labels total)
- **Diversity:** Include a mix of tones (negative/neutral/positive), channels, and languages (EN/PT).

---

## Intents & Target Counts (≈150 total)

- `billing_issue` — 14
- `payment_failed` — 14
- `refund_request` — 14
- `subscription_cancel` — 14
- `login_problem` — 14
- `account_change` — 14
- `bug_report` — 14
- `outage_or_service_down` — 14
- `technical_support` — 14
- `feature_request` — 14
- `general_question` — 10 (slightly fewer to round to ~150)

> Note: We accept ±1 variation while curating examples; aim for ~10–12% share per label overall.

---

## CSV Schema (descriptive)

File: `data/seeds/tickets_seed.csv`

Columns (header row included):

- `subject` — short title (string)
- `body` — ticket text (string; 1–8 sentences)
- `channel` — enum: `web_form`, `email`, `chat_widget`, `api`, `import`
- `customer_id` — string (synthetic identifier, e.g., `user_123`, not real email)
- `language` — optional BCP-47 (e.g., `en`, `pt-PT`)
- `status` — enum: `open`, `pending`, `resolved`, `closed`
- `intent` — enum (one of the 11 labels above)
- `sentiment` — enum: `negative`, `neutral`, `positive` (optional for seed; can be inferred)
- `created_at` — ISO-8601 timestamp (UTC)
- `updated_at` — ISO-8601 timestamp (UTC)

> Optional extra columns allowed (ignored by importer): `tags`, `notes`

---

## Generation Approach

1. **Templates:** Draft 5–8 base templates per intent (EN/PT) to vary subject/body.  
2. **Perturbations:** Randomize names, amounts, order IDs, plan types, device/OS, and dates.  
3. **Tone Mix:** For each intent, include ~40% negative, ~40% neutral, ~20% positive messages.  
4. **Channels:** Distribute roughly: 35% web_form, 35% email, 20% chat_widget, 5% api, 5% import.  
5. **Status:** Bias toward `open` and `pending`; include some `resolved`/`closed` for realism.

---

## PII Redaction Policy (for any real samples)

- **No real emails, names, phone numbers, order IDs, or card details.**  
- Replace with placeholders (e.g., `user_042`, `ORDER-XXXX`, `CARD-**** **** **** 1234`).  
- If importing real logs for testing, run a redaction pass first and store only redacted text.  
- Do **not** commit raw real-world data to the repository.

---

## Validation

- Verify class balance (10–12% per label) and channel distribution as above.  
- Spot-check 10–20 rows to ensure intent/subject/body alignment and language tags are plausible.  
- Ensure timestamps are within recent months and `updated_at >= created_at`.

---

## Import Strategy (later)

- Provide a one-off CLI/script to read `tickets_seed.csv`, insert into `tickets`, and write corresponding rows to `ticket_classifications` when known or leave blank to let `/classify` backfill.

