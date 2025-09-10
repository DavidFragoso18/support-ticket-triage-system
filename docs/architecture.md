# Architecture Overview

**Status:** Draft — high-level intentions only.  
**Last updated:** 2025-09-10

This document describes the planned structure of the backend application and the purpose of each component. It is not code, only a map of where things will live.

---

## Components

### `app/main.py`
- Entry point for the FastAPI app.  
- Creates the application, configures middleware, mounts routers, and sets up startup/shutdown events.

### `api/routes/tickets.py`
- Defines endpoints for ticket CRUD operations.  
- Connects HTTP requests to database models and services.

### `api/routes/classify.py`
- Defines the classification endpoint.  
- Accepts ticket text or ID, runs through NLP pipeline, and returns classification results.

### `schemas/`
- Contains Pydantic models that mirror the API contracts.  
- Ensures request/response validation and serialization.

### `db/models/`
- Holds ORM entities for tickets and ticket classifications.  
- Maps database tables into Python classes for CRUD operations.

### `nlp/pipeline.py`
- Wraps Hugging Face models (intent & sentiment).  
- Provides a simple function `classify(text)` used by the `/classify` endpoint.

### `services/priority_rules.py`
- Reads rules from `rules.yml`.  
- Applies thresholds and keyword logic to compute priority level and score (P1/P2/P3 → urgent/high/medium/low).

---

## Notes
- Directory layout follows a modular design: routes → schemas → services → db → nlp.  
- Phase 2 will expand with additional services (auth, users, feedback).  
