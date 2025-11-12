# Testing Guide - Phase 4 Features

## Quick Start - Test Everything

### Option 1: Docker Compose (Recommended)
```bash
# Start all services
make docker-up

# Wait 30 seconds for services to start, then seed data
make seed

# View logs
make docker-logs
```

**Access URLs:**
- Backend API: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Database: localhost:5432

---

### Option 2: Local Development
```bash
# Start database
make up-db

# Start backend (separate terminal)
make up-api

# Start frontend (separate terminal)
make start-frontend

# Seed database (separate terminal)
make seed
```

---

## Testing Phase 4 Features

### 1. Test Database Schema ✓

```bash
# Connect to database
make db

# Check tables exist
\dt

# Should see:
# - tickets
# - ticket_classifications  
# - classification_feedback (NEW)
# - kb_articles (NEW with embedding column)
# - resolutions (NEW with embedding column)

# Check pgvector extension
\dx

# Should see: vector extension

# Check feedback table structure
\d classification_feedback

# Exit
\q
```

---

### 2. Test Vector Search Setup ✓

```bash
# Enable pgvector (first time only)
cd backend
python -m app.scripts.enable_pgvector

# Should see: ✅ pgvector extension enabled
```

---

### 3. Test Data Seeding with Embeddings ✓

```bash
# Seed KB articles (generates embeddings)
make seed-kb

# Should see:
# - Loading SentenceTransformer model
# - Encoding text... (for each article)
# - ✅ Seeded X KB articles

# Seed resolutions (generates embeddings)
make seed-resolutions

# Should see similar output with embeddings

# Seed tickets
make seed-tickets
```

**Verify embeddings in database:**
```bash
make db

# Check KB articles have embeddings
SELECT id, title, 
       CASE WHEN embedding IS NULL THEN 'NO' ELSE 'YES' END as has_embedding
FROM kb_articles LIMIT 5;

# Check resolutions have embeddings
SELECT id, title,
       CASE WHEN embedding IS NULL THEN 'NO' ELSE 'YES' END as has_embedding  
FROM resolutions LIMIT 5;

\q
```

---

### 4. Test Backend API Endpoints

#### Test Feedback API
```bash
# Create a ticket first
curl -X POST http://localhost:8000/tickets \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test ticket",
    "body": "This is a test ticket for feedback",
    "channel": "web"
  }'

# Copy the ticket ID from response

# Get classification ID
curl http://localhost:8000/tickets/{TICKET_ID}

# Copy the classification.id

# Submit feedback - Accept
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "classification_id": "{CLASSIFICATION_ID}",
    "action": "accepted",
    "agent_id": "test-agent"
  }'

# Submit feedback - Correct
curl -X POST http://localhost:8000/feedback \
  -H "Content-Type: application/json" \
  -d '{
    "classification_id": "{CLASSIFICATION_ID}",
    "action": "corrected",
    "corrected_intent": "bug_issue",
    "corrected_sentiment": "negative",
    "corrected_priority": "P1",
    "notes": "Customer is very upset",
    "agent_id": "test-agent"
  }'

# Get feedback for classification
curl http://localhost:8000/feedback/{CLASSIFICATION_ID}

# Get accuracy metrics
curl http://localhost:8000/analytics/classification-accuracy
```

#### Test Vector Search API
```bash
# Search for similar content
curl "http://localhost:8000/search/similar?query=billing%20issue&limit=5"

# Should return:
# - Array of KB articles and resolutions
# - Each with similarity score (0.0 - 1.0)
# - Sorted by similarity (highest first)

# Try different queries
curl "http://localhost:8000/search/similar?query=password%20reset&limit=3"
curl "http://localhost:8000/search/similar?query=refund%20request&limit=5"
```

**Expected Response:**
```json
[
  {
    "id": "uuid",
    "title": "How to request a refund",
    "preview": "To request a refund, please follow these steps...",
    "similarity": 0.8542,
    "type": "kb"
  },
  {
    "id": "uuid",
    "title": "Refund Policy",
    "preview": "Our refund policy allows customers to...",
    "similarity": 0.7834,
    "type": "resolution"
  }
]
```

#### Test All Endpoints with Swagger
```bash
# Open API documentation
open http://localhost:8000/docs

# Or manually: http://localhost:8000/docs
```

**Test these new endpoints:**
- `POST /feedback` - Submit feedback
- `GET /feedback/{classification_id}` - Get feedback history
- `GET /analytics/classification-accuracy` - Get metrics
- `GET /search/similar` - Semantic search

---

### 5. Test Frontend Feedback UI

#### Manual Testing Flow

1. **Open Frontend**
   ```bash
   open http://localhost:3000
   ```

2. **Navigate to Ticket Detail**
   - Click "Tickets" in navigation
   - Click on any ticket to view details
   - Scroll to classification section

3. **Test Accept Button**
   - Click green "Accept" button
   - Should see: ✓ Feedback submitted successfully!
   - Message disappears after 3 seconds

4. **Test Reject Button**
   - Refresh page or open different ticket
   - Click red "Reject" button
   - Should see success message

5. **Test Correct Button**
   - Click amber "Correct" button
   - Modal should appear with:
     - Intent dropdown (6 options)
     - Sentiment dropdown (3 options)
     - Priority dropdown (4 options)
     - Notes textarea
     - Cancel/Submit buttons

6. **Test Correction Modal**
   - Select different intent: "bug_issue"
   - Select different sentiment: "negative"
   - Select different priority: "P1"
   - Add notes: "Customer is upset"
   - Click "Submit Correction"
   - Modal closes
   - Success message appears

7. **Test Error Handling**
   - Stop backend: `Ctrl+C` in backend terminal
   - Try submitting feedback
   - Should see error message: ✗ Failed to submit feedback

8. **Verify in Database**
   ```bash
   make db
   
   # Check feedback was saved
   SELECT 
     id, 
     action, 
     corrected_intent, 
     corrected_sentiment,
     corrected_priority,
     notes,
     created_at 
   FROM classification_feedback 
   ORDER BY created_at DESC 
   LIMIT 5;
   
   \q
   ```

---

### 6. Test Vector Search UI (Search Endpoint)

```bash
# Test from command line
curl "http://localhost:8000/search/similar?query=how%20to%20change%20password&limit=5" | jq

# Expected: Array of results with similarity scores

# Test with different queries
curl "http://localhost:8000/search/similar?query=billing%20problem&limit=3" | jq
curl "http://localhost:8000/search/similar?query=account%20locked&limit=5" | jq
```

---

### 7. Run Automated Tests

```bash
# Run all backend tests
make test

# Run specific test file
cd backend
python -m pytest tests/test_smoke.py -v

# Run with coverage
python -m pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html
```

---

## Troubleshooting

### Database Connection Issues
```bash
# Check database is running
docker ps | grep triage-pg

# Restart database
make down-db
make up-db

# Check logs
make logs
```

### Backend Not Starting
```bash
# Check Python environment
cd backend
source .venv/bin/activate  # macOS/Linux
# OR
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Check for errors
python -m app.main
```

### Embeddings Not Generating
```bash
# Check sentence-transformers is installed
pip list | grep sentence-transformers

# Re-install if needed
pip install sentence-transformers

# Test embeddings module
cd backend
python -c "from app.nlp.embeddings import emb; print(emb.encode_to_list('test'))"

# Should print: array of 384 floats
```

### Vector Search Not Working
```bash
# Ensure pgvector extension is enabled
make db
CREATE EXTENSION IF NOT EXISTS vector;
\q

# Re-run seed scripts
make seed-kb
make seed-resolutions

# Check embeddings exist
make db
SELECT COUNT(*) FROM kb_articles WHERE embedding IS NOT NULL;
SELECT COUNT(*) FROM resolutions WHERE embedding IS NOT NULL;
\q
```

### Frontend Not Connecting to Backend
```bash
# Check backend is running
curl http://localhost:8000/health

# Should return: {"status":"ok"}

# Check Nuxt proxy configuration
cat frontend/nuxt.config.ts | grep nitro

# Should proxy /api to http://localhost:8000
```

---

## Performance Testing

### Test Embedding Generation Speed
```bash
cd backend
python -c "
from app.nlp.embeddings import emb
import time

text = 'This is a test ticket about billing issues'
start = time.time()
emb.encode_to_list(text)
end = time.time()
print(f'Embedding generated in {end-start:.3f}s')
"

# Expected: 0.010-0.050s (after model loaded)
```

### Test Vector Search Speed
```bash
# Time the search endpoint
time curl -s "http://localhost:8000/search/similar?query=billing&limit=10" > /dev/null

# Expected: < 200ms
```

---

## Complete Test Checklist

- [ ] Database tables created (5 tables)
- [ ] pgvector extension enabled
- [ ] KB articles seeded with embeddings
- [ ] Resolutions seeded with embeddings
- [ ] Tickets seeded
- [ ] POST /feedback accepts feedback
- [ ] GET /feedback/{id} returns feedback
- [ ] GET /analytics/classification-accuracy works
- [ ] GET /search/similar returns results
- [ ] Frontend shows feedback buttons
- [ ] Accept button works
- [ ] Reject button works
- [ ] Correct button opens modal
- [ ] Modal submits corrections
- [ ] Success/error messages display
- [ ] Feedback saves to database
- [ ] Vector search returns relevant results
- [ ] Similarity scores are accurate (>0.5)
- [ ] Backend tests pass (pytest)

---

## Next Steps After Testing

1. **If everything works:**
   - Move to Task 5: Similar Tickets Feature
   - Add embeddings to Ticket table
   - Create similar tickets endpoint
   - Add UI for similar tickets

2. **If issues found:**
   - Document issues in PHASE4-PROGRESS.md
   - Fix critical bugs
   - Re-run tests

3. **Push changes to GitHub:**
   ```bash
   git add .
   git commit -m "feat: Phase 4 - Feedback loop + Vector search"
   git push origin main
   ```

---

## Quick Commands Reference

```bash
# Start everything
make docker-up

# Seed data
make seed

# View logs
make docker-logs

# Stop everything
make docker-down

# Run tests
make test

# Connect to database
make db

# Enable pgvector
cd backend && python -m app.scripts.enable_pgvector
```

---

**Testing Priority:**
1. ✅ Database schema (5 min)
2. ✅ Data seeding with embeddings (10 min)
3. ✅ Backend API endpoints (15 min)
4. ✅ Frontend feedback UI (15 min)
5. ✅ Vector search (10 min)

**Total Testing Time:** ~60 minutes for comprehensive testing

