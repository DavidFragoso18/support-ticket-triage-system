# Architecture Overview

**Status:** Production - Phase 5 Complete  
**Last updated:** 2025-11-12

This document describes the complete architecture of the Support Ticket Triage System including all Phase 5 real-time, analytics, search, and AI features.

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

## Phase 5 Architecture Additions

### Real-Time Communication Layer

#### WebSocket Manager (`app/api/routes/websocket.py`)
- Manages persistent WebSocket connections for real-time updates
- **Connection Pool**: Tracks active connections by connection ID
- **Agent Subscriptions**: Maps agent IDs to their connections
- **Redis Pub/Sub**: Broadcasts messages across multiple backend instances

**Flow:**
```
Client → WebSocket Connect → Connection Manager → Redis Subscribe
                                     ↓
Ticket Event → Redis Publish → All Subscribers → WebSocket Send → Clients
```

#### Redis Pub/Sub Channels
- `ticket_updates`: Broadcasts ticket creation, claims, releases
- `agent_presence`: Tracks agent online/offline status
- `system_events`: Application-wide notifications

**Message Format:**
```json
{
  "type": "ticket_update",
  "event": "ticket_claimed",
  "data": { "id": "uuid", "agent_id": "agent-123" }
}
```

### Analytics Engine

#### Analytics Aggregation (`app/api/routes/analytics.py`)
- **Dashboard Endpoint**: Combines multiple metrics into single response
  - Overview: Ticket counts, confidence metrics
  - Accuracy: Feedback statistics and acceptance rates
  - Distributions: Breakdown by intent, sentiment, priority

- **Trends Endpoint**: Time-series data for daily ticket metrics
  - Generates data points for each day in range
  - Tracks: total tickets, high priority count, resolved count

- **Agent Performance**: Individual agent productivity metrics
  - Calculates: tickets claimed, resolved, resolution rate
  - Computes: average resolution time from claim to closure

**Caching Strategy:**
- Analytics queries cached for 5 minutes
- Real-time updates bypass cache
- Cache invalidation on ticket state changes

### Semantic Search Architecture

#### Hybrid Search Pipeline
```
Query Input
    ↓
Text Embedding (sentence-transformers)
    ↓
Parallel Processing:
├─ Vector Similarity (pgvector cosine distance)
│  └─ Searches ticket embeddings
└─ Full-Text Search (PostgreSQL tsvector)
   └─ Searches weighted text (subject:A body:B)
    ↓
Score Combination (60% semantic + 40% keyword)
    ↓
Ranked Results
```

#### Search Modes
1. **Semantic**: Pure vector similarity using embeddings
2. **Keyword**: PostgreSQL full-text search with GIN index
3. **Hybrid**: Weighted combination of both (recommended)

#### Indexing Strategy
- **Vector Index**: IVFFlat index on `embedding` column (384 dimensions)
- **Text Index**: GIN index on `search_vector` generated column
- **Generated Column**: `to_tsvector('english', subject || ' ' || body)`

### AI Response Generation (RAG Pipeline)

#### LLM Service Architecture (`app/services/llm.py`)

**Provider Support:**
- **Primary**: Ollama (local, llama3.2:latest)
- **Fallback**: OpenAI GPT-3.5-turbo (optional)
- **Graceful Degradation**: Template responses if both unavailable

**RAG Context Retrieval:**
```
Ticket → Extract embedding
    ↓
Parallel Queries:
├─ Similar Tickets (3 most similar by embedding)
├─ KB Articles (2 relevant by topic)
└─ Past Resolutions (2 similar solutions)
    ↓
Context Aggregation
    ↓
Prompt Construction (with tone instructions)
    ↓
LLM Generation
    ↓
Response + Metadata
```

**Tone Handling:**
- Professional: Formal business language
- Friendly: Warm, conversational tone
- Technical: Detailed with explanations
- Empathetic: Understanding, supportive

**Response Persistence:**
- Saves to `ai_responses` table
- Tracks: edit status, sending status, context used
- Links to ticket via foreign key

#### Ollama Integration
- **Connection**: HTTP requests to Ollama API server
- **Endpoint**: `POST /api/generate` with streaming support
- **Model**: Configurable (default: llama3.2:latest)
- **Timeout**: 30 seconds per generation
- **Error Handling**: Falls back to OpenAI or templates

---

## System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Nuxt.js)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Ticket List │  │   Analytics  │  │  Search UI   │      │
│  │ + WebSocket  │  │  Dashboard   │  │  (3 modes)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────┬───────────────┬────────────────┬───────────────┘
             │               │                │
         WebSocket         HTTP            HTTP
             │               │                │
┌────────────┴───────────────┴────────────────┴───────────────┐
│                    Backend (FastAPI)                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  WebSocket Manager                                   │   │
│  │  - Connection pool                                   │   │
│  │  - Agent presence tracking                          │   │
│  │  - Redis pub/sub integration                        │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Tickets    │  │  Analytics   │  │    Search    │     │
│  │   Routes     │  │   Routes     │  │   Routes     │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
│  ┌──────┴──────────────────┴──────────────────┴───────┐   │
│  │              NLP Pipeline                           │   │
│  │  - Embeddings (sentence-transformers)              │   │
│  │  - Classification (intent, sentiment)              │   │
│  │  - Priority rules engine                           │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              LLM Service (RAG)                      │   │
│  │  - Context retrieval (similar tickets, KB, etc)    │   │
│  │  - Prompt construction with tone                   │   │
│  │  - Ollama/OpenAI integration                       │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────┬───────────────┬────────────────┬──────────┬──────┘
           │               │                │          │
      ┌────┴────┐     ┌────┴────┐     ┌────┴────┐  ┌──┴────┐
      │ Postgres│     │  Redis  │     │ Ollama  │  │ OpenAI│
      │  +       │     │ Pub/Sub │     │  LLM    │  │  API  │
      │ pgvector│     │         │     │ (local) │  │(backup)│
      └─────────┘     └─────────┘     └─────────┘  └───────┘
```

---

## Data Flow Examples

### Ticket Creation with Real-Time Broadcast

```
1. Client → POST /tickets → Backend
2. Backend → Create ticket in database
3. Backend → Generate embedding
4. Backend → Run classification
5. Backend → Publish to Redis: "ticket_created"
6. Redis → Broadcast to all subscribed backends
7. Backend → Send via WebSocket to all connected clients
8. Clients → Display notification
```

### AI Response Generation

```
1. Agent → GET /llm/suggest-response/{id}?tone=friendly
2. Backend → Fetch ticket from database
3. Backend → Query similar tickets (vector similarity)
4. Backend → Query relevant KB articles
5. Backend → Query past resolutions
6. Backend → Construct context string
7. Backend → Build prompt with tone instructions
8. Backend → POST to Ollama API
9. Ollama → Generate response (streaming)
10. Backend → Return response + metadata
11. Agent → Review, edit, save response
12. Client → POST /llm/save-response
13. Backend → Insert into ai_responses table
```

### Semantic Search

```
1. User → Search query: "login problems"
2. Frontend → GET /search/tickets?q=login+problems&mode=hybrid
3. Backend → Generate embedding for query
4. Backend → Parallel execution:
   a. Vector similarity query (cosine distance)
   b. Full-text search query (ts_rank)
5. Backend → Combine scores (60% vector + 40% text)
6. Backend → Order by combined_score DESC
7. Backend → Return results with all scores
8. Frontend → Display with relevance indicators
```

---

## Performance Optimizations

### Database Indexing
- **B-tree indexes**: ticket_id, created_at, status, priority
- **GIN index**: Full-text search on `search_vector`
- **IVFFlat index**: Vector similarity on `embedding` column
- **Composite indexes**: (status, priority), (agent_id, created_at)

### Caching Strategy
- **Analytics**: 5-minute cache for dashboard data
- **Embeddings**: Cached per ticket, regenerated on update
- **Search results**: No caching (real-time accuracy priority)

### Connection Pooling
- **Database**: Pool size 10, max overflow 20
- **Redis**: Connection pool with health checks
- **Ollama**: HTTP client with connection reuse

---

## Security Considerations

### WebSocket Security
- Connection authentication via query parameters
- Rate limiting: 100 connections per IP
- Automatic connection cleanup on timeout

### API Security
- CORS configuration for allowed origins
- Request validation via Pydantic schemas
- SQL injection prevention via SQLAlchemy ORM

### Data Privacy
- AI responses include no customer PII in prompts
- Context retrieval filters by ticket access permissions
- Audit trail for all AI-generated responses

---

## Scalability

### Horizontal Scaling
- **Backend**: Stateless, can run multiple instances
- **WebSocket**: Redis pub/sub enables multi-instance broadcasting
- **Database**: Read replicas for analytics queries
- **Ollama**: Can run multiple instances with load balancer

### Vertical Scaling
- **Ollama**: Benefits from more RAM and GPU
- **PostgreSQL**: Increase shared_buffers for vector operations
- **Redis**: Increase memory for more pub/sub channels

---

## Monitoring Points

### Application Metrics
- WebSocket connection count
- Active agent count
- AI generation success rate
- Search query performance
- Analytics query latency

### Infrastructure Metrics
- Database connection pool usage
- Redis pub/sub message rate
- Ollama request queue length
- Memory usage per service

---

## Notes
- Architecture follows modular design: routes → services → db
- WebSocket layer enables real-time collaboration
- RAG pipeline provides context-aware AI responses
- Hybrid search combines best of semantic and keyword approaches  
