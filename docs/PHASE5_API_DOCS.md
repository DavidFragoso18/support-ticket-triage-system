# Phase 5 API Documentation

Complete API reference for Phase 5 features: WebSocket real-time updates, advanced analytics, semantic search, and AI-powered response generation.

## Table of Contents

- [WebSocket Endpoints](#websocket-endpoints)
- [Analytics Endpoints](#analytics-endpoints)
- [Search Endpoints](#search-endpoints)
- [LLM/AI Response Endpoints](#llmai-response-endpoints)
- [Ticket Management Updates](#ticket-management-updates)

---

## WebSocket Endpoints

### Connect to Ticket Updates

**Endpoint:** `ws://localhost:8000/ws/tickets`

**Description:** Real-time notifications for ticket events (creation, claim, release, updates)

**Connection:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/tickets');

ws.onopen = () => {
  console.log('Connected to ticket updates');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};
```

**Message Types Received:**

1. **Connection Established**
```json
{
  "type": "connection_established",
  "connection_id": "uuid-here"
}
```

2. **Ticket Created**
```json
{
  "type": "ticket_update",
  "event": "ticket_created",
  "data": {
    "id": "ticket-uuid",
    "subject": "Password reset needed",
    "status": "open",
    "priority": "P2",
    "created_at": "2025-11-12T10:30:00Z"
  }
}
```

3. **Ticket Claimed**
```json
{
  "type": "ticket_update",
  "event": "ticket_claimed",
  "data": {
    "id": "ticket-uuid",
    "assigned_agent_id": "agent-123",
    "status": "in_progress",
    "claimed_at": "2025-11-12T10:35:00Z"
  }
}
```

4. **Ticket Released**
```json
{
  "type": "ticket_update",
  "event": "ticket_released",
  "data": {
    "id": "ticket-uuid",
    "assigned_agent_id": null,
    "status": "open",
    "released_at": "2025-11-12T10:40:00Z"
  }
}
```

**Ping/Pong Keep-Alive:**
```javascript
// Send ping to keep connection alive
ws.send(JSON.stringify({ type: 'ping' }));

// Receive pong response
{
  "type": "pong"
}
```

---

### Connect to Agent Updates

**Endpoint:** `ws://localhost:8000/ws/agents/{agent_id}`

**Description:** Agent-specific updates and presence tracking

**Example:**
```bash
wscat -c "ws://localhost:8000/ws/agents/agent-123"
```

**Connection Message:**
```json
{
  "type": "connection_established",
  "agent_id": "agent-123",
  "connection_id": "uuid-here"
}
```

---

### WebSocket Status

**Endpoint:** `GET /ws/status`

**Description:** Get WebSocket server status and connection count

**Response:**
```json
{
  "active_connections": 5,
  "agent_subscriptions": 3,
  "redis_connected": true
}
```

**cURL Example:**
```bash
curl http://localhost:8000/ws/status
```

---

## Analytics Endpoints

### Analytics Dashboard

**Endpoint:** `GET /analytics/dashboard`

**Description:** Comprehensive analytics dashboard with overview, accuracy, and distributions

**Query Parameters:**
- `days` (optional, default: 30) - Number of days to include in analysis

**Response:**
```json
{
  "overview": {
    "total_tickets": 1247,
    "high_priority": 89,
    "avg_confidence": 0.87,
    "low_confidence_count": 43
  },
  "accuracy": {
    "total_feedback": 312,
    "accepted": 287,
    "corrected": 25,
    "acceptance_rate": 91.99
  },
  "distributions": {
    "by_intent": {
      "billing": 423,
      "technical_issue": 567,
      "account_access": 189,
      "general_inquiry": 68
    },
    "by_sentiment": {
      "positive": 234,
      "neutral": 678,
      "negative": 335
    },
    "by_priority": {
      "P1": 67,
      "P2": 456,
      "P3": 567,
      "P4": 157
    }
  }
}
```

**cURL Example:**
```bash
curl "http://localhost:8000/analytics/dashboard?days=7"
```

---

### Analytics Trends

**Endpoint:** `GET /analytics/trends`

**Description:** Daily ticket trends over time

**Query Parameters:**
- `days` (optional, default: 30) - Number of days of historical data

**Response:**
```json
[
  {
    "date": "2025-11-12",
    "total_tickets": 47,
    "high_priority": 8,
    "resolved": 39
  },
  {
    "date": "2025-11-11",
    "total_tickets": 52,
    "high_priority": 6,
    "resolved": 44
  }
]
```

**cURL Example:**
```bash
curl "http://localhost:8000/analytics/trends?days=14"
```

---

### Agent Performance

**Endpoint:** `GET /analytics/agents/performance`

**Description:** Performance metrics for all agents

**Query Parameters:**
- `days` (optional, default: 30) - Time period for metrics

**Response:**
```json
[
  {
    "agent_id": "agent-456",
    "tickets_claimed": 78,
    "tickets_resolved": 72,
    "resolution_rate": 92.31,
    "avg_resolution_time": 3600.5
  },
  {
    "agent_id": "agent-123",
    "tickets_claimed": 65,
    "tickets_resolved": 58,
    "resolution_rate": 89.23,
    "avg_resolution_time": 4200.3
  }
]
```

**Notes:**
- Results sorted by `resolution_rate` (descending)
- `avg_resolution_time` in seconds (nullable if no resolutions)

**cURL Example:**
```bash
curl "http://localhost:8000/analytics/agents/performance?days=7"
```

---

## Search Endpoints

### Semantic Search

**Endpoint:** `GET /search/tickets`

**Description:** Advanced hybrid search combining vector similarity and full-text search

**Query Parameters:**
- `q` (required) - Search query
- `mode` (optional, default: "hybrid") - Search mode: `semantic`, `keyword`, or `hybrid`
- `threshold` (optional, default: 0.3) - Minimum similarity threshold (0.0-1.0)
- `limit` (optional, default: 10) - Maximum results to return

**Response:**
```json
[
  {
    "id": "ticket-uuid-1",
    "subject": "Cannot reset my password",
    "body": "I forgot my password and the reset link isn't working...",
    "customer_id": "customer-789",
    "channel": "email",
    "status": "open",
    "created_at": "2025-11-12T09:15:00Z",
    "classification": {
      "intent": "account_access",
      "sentiment": "negative",
      "priority": "P2",
      "confidence": 0.92
    },
    "similarity_score": 0.87,
    "keyword_score": 0.75,
    "combined_score": 0.83
  }
]
```

**Search Modes:**

1. **Semantic Mode** - Vector similarity only (best for conceptual matches)
```bash
curl "http://localhost:8000/search/tickets?q=login+issues&mode=semantic&limit=5"
```

2. **Keyword Mode** - Full-text search only (best for exact word matches)
```bash
curl "http://localhost:8000/search/tickets?q=password+reset&mode=keyword&limit=5"
```

3. **Hybrid Mode** - Combined (60% semantic + 40% keyword, best overall)
```bash
curl "http://localhost:8000/search/tickets?q=billing+problem&mode=hybrid&limit=10"
```

**Score Breakdown:**
- `similarity_score`: Cosine similarity (0.0-1.0)
- `keyword_score`: Full-text search rank
- `combined_score`: Weighted average (hybrid mode only)

**Advanced Example:**
```bash
# High-threshold semantic search for very similar tickets
curl "http://localhost:8000/search/tickets?q=forgot+password&mode=semantic&threshold=0.7&limit=3"
```

---

## LLM/AI Response Endpoints

### Generate AI Response Suggestion

**Endpoint:** `GET /llm/suggest-response/{ticket_id}`

**Description:** Generate AI-powered response using RAG (Retrieval-Augmented Generation) with context from similar tickets, KB articles, and resolutions

**Path Parameters:**
- `ticket_id` (required) - UUID of the ticket

**Query Parameters:**
- `tone` (optional, default: "professional") - Response tone: `professional`, `friendly`, `technical`, or `empathetic`

**Response:**
```json
{
  "response": "Thank you for reaching out. I understand you're having trouble accessing your account. To reset your password, please follow these steps:\n\n1. Visit our password reset page at...",
  "tone": "professional",
  "model": "llama3.2:latest",
  "context": {
    "similar_tickets": 3,
    "kb_articles": 2,
    "resolutions": 2
  }
}
```

**Tones Available:**

1. **Professional** - Formal and business-appropriate
```bash
curl "http://localhost:8000/llm/suggest-response/abc-123?tone=professional"
```

2. **Friendly** - Warm and approachable
```bash
curl "http://localhost:8000/llm/suggest-response/abc-123?tone=friendly"
```

3. **Technical** - Detailed with technical explanations
```bash
curl "http://localhost:8000/llm/suggest-response/abc-123?tone=technical"
```

4. **Empathetic** - Understanding and supportive
```bash
curl "http://localhost:8000/llm/suggest-response/abc-123?tone=empathetic"
```

**Error Responses:**

- `404` - Ticket not found
```json
{
  "detail": "Ticket not found"
}
```

- `422` - Invalid tone parameter
```json
{
  "detail": [
    {
      "loc": ["query", "tone"],
      "msg": "value is not a valid enumeration member",
      "type": "type_error.enum"
    }
  ]
}
```

- `503` - LLM service unavailable (returns fallback template)
```json
{
  "response": "Thank you for contacting support regarding: [subject]...",
  "tone": "professional",
  "model": "fallback",
  "context": {}
}
```

---

### Save AI Response

**Endpoint:** `POST /llm/save-response`

**Description:** Save a generated AI response with edit tracking

**Request Body:**
```json
{
  "ticket_id": "ticket-uuid",
  "response_text": "Thank you for reaching out. I understand...",
  "tone": "professional",
  "context_used": {
    "similar_tickets": 3,
    "kb_articles": 2,
    "resolutions": 2
  },
  "model": "llama3.2:latest",
  "agent_id": "agent-123",
  "was_edited": false,
  "was_sent": false
}
```

**Response:**
```json
{
  "id": "response-uuid",
  "ticket_id": "ticket-uuid",
  "response_text": "Thank you for reaching out...",
  "tone": "professional",
  "model": "llama3.2:latest",
  "agent_id": "agent-123",
  "was_edited": false,
  "was_sent": false,
  "created_at": "2025-11-12T10:30:00Z"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/llm/save-response" \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "abc-123",
    "response_text": "Thank you for your patience...",
    "tone": "friendly",
    "context_used": {},
    "model": "llama3.2:latest",
    "agent_id": "agent-456",
    "was_edited": true,
    "was_sent": false
  }'
```

**Edit Tracking:**
- `was_edited: false` - Response used as-is from LLM
- `was_edited: true` - Agent modified the response before saving

---

### Get Saved Responses

**Endpoint:** `GET /llm/saved-responses/{ticket_id}`

**Description:** Retrieve all saved AI responses for a ticket

**Path Parameters:**
- `ticket_id` (required) - UUID of the ticket

**Response:**
```json
[
  {
    "id": "response-uuid-1",
    "ticket_id": "ticket-uuid",
    "response_text": "Thank you for reaching out...",
    "tone": "professional",
    "model": "llama3.2:latest",
    "agent_id": "agent-123",
    "was_edited": false,
    "was_sent": true,
    "created_at": "2025-11-12T10:30:00Z"
  },
  {
    "id": "response-uuid-2",
    "ticket_id": "ticket-uuid",
    "response_text": "Hi there! Thanks for contacting us...",
    "tone": "friendly",
    "model": "llama3.2:latest",
    "agent_id": "agent-123",
    "was_edited": true,
    "was_sent": false,
    "created_at": "2025-11-12T10:25:00Z"
  }
]
```

**Notes:**
- Responses ordered by `created_at` (newest first)
- Returns empty array if no responses saved
- Includes metadata about editing and sending status

**cURL Example:**
```bash
curl "http://localhost:8000/llm/saved-responses/abc-123"
```

---

## Ticket Management Updates

### Claim Ticket

**Endpoint:** `POST /tickets/{ticket_id}/claim`

**Description:** Claim a ticket and broadcast to WebSocket clients

**Query Parameters:**
- `agent_id` (required) - ID of the claiming agent

**Response:**
```json
{
  "success": true,
  "ticket": {
    "id": "ticket-uuid",
    "assigned_agent_id": "agent-123",
    "status": "in_progress",
    "claimed_at": "2025-11-12T10:30:00Z"
  }
}
```

**Error Response (409 Conflict):**
```json
{
  "detail": "Ticket is already claimed by another agent"
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/tickets/abc-123/claim?agent_id=agent-456"
```

---

### Release Ticket

**Endpoint:** `POST /tickets/{ticket_id}/release`

**Description:** Release a claimed ticket back to open status

**Response:**
```json
{
  "success": true,
  "ticket": {
    "id": "ticket-uuid",
    "assigned_agent_id": null,
    "status": "open",
    "released_at": "2025-11-12T10:35:00Z"
  }
}
```

**cURL Example:**
```bash
curl -X POST "http://localhost:8000/tickets/abc-123/release"
```

---

## Rate Limits

**Current Limits:**
- WebSocket connections: 100 per IP
- API requests: 1000 per hour per IP
- LLM generation: 10 per minute per agent (to manage Ollama load)

---

## Error Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 400 | Bad Request |
| 404 | Not Found |
| 409 | Conflict (e.g., ticket already claimed) |
| 422 | Validation Error |
| 500 | Internal Server Error |
| 503 | Service Unavailable (e.g., Ollama down) |

---

## Best Practices

### WebSocket Connections

1. **Implement reconnection logic:**
```javascript
function connectWebSocket() {
  const ws = new WebSocket('ws://localhost:8000/ws/tickets');
  
  ws.onclose = () => {
    console.log('Disconnected, reconnecting in 5s...');
    setTimeout(connectWebSocket, 5000);
  };
  
  return ws;
}
```

2. **Send periodic pings to keep connection alive:**
```javascript
setInterval(() => {
  if (ws.readyState === WebSocket.OPEN) {
    ws.send(JSON.stringify({ type: 'ping' }));
  }
}, 30000); // Every 30 seconds
```

### AI Response Generation

1. **Always handle fallback responses:**
```javascript
const response = await fetch(`/llm/suggest-response/${ticketId}?tone=professional`);
if (response.ok) {
  const data = await response.json();
  if (data.model === 'fallback') {
    console.warn('Using fallback template - LLM unavailable');
  }
}
```

2. **Track edits for quality metrics:**
```javascript
const wasEdited = originalResponse !== editedResponse;
await saveResponse({
  ...responseData,
  was_edited: wasEdited
});
```

### Search Optimization

1. **Use hybrid mode for general searches:**
```javascript
const results = await searchTickets(query, { mode: 'hybrid' });
```

2. **Use semantic mode for conceptual matches:**
```javascript
// Find tickets about "authentication" even if they say "login" or "password"
const results = await searchTickets('authentication issues', { mode: 'semantic' });
```

3. **Use keyword mode for exact phrases:**
```javascript
// Find tickets mentioning specific error codes
const results = await searchTickets('ERR_CONNECTION_REFUSED', { mode: 'keyword' });
```

---

## Additional Resources

- [Architecture Documentation](./architecture.md)
- [Deployment Guide](./PHASE5_DEPLOYMENT.md)
- [User Guide](./PHASE5_USER_GUIDE.md)
- [Database Schema](./db-schema.md)
