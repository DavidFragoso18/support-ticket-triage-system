# Phase 5 Deployment Guide

Complete deployment guide for Phase 5 features including Ollama setup, environment configuration, and production considerations.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Ollama Installation](#ollama-installation)
- [Environment Configuration](#environment-configuration)
- [Docker Compose Setup](#docker-compose-setup)
- [Database Migrations](#database-migrations)
- [Redis Configuration](#redis-configuration)
- [Production Deployment](#production-deployment)
- [Monitoring and Troubleshooting](#monitoring-and-troubleshooting)

---

## Prerequisites

### System Requirements

**Minimum:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 20GB (for Ollama models)
- OS: Linux, macOS, or Windows with WSL2

**Recommended (with GPU):**
- CPU: 8+ cores
- RAM: 16GB+
- GPU: NVIDIA GPU with 8GB+ VRAM
- Storage: 50GB+ SSD

### Software Requirements

- Docker 24.0+
- Docker Compose 2.20+
- Python 3.11+ (for local development)
- Node.js 18+ (for frontend)

---

## Ollama Installation

### Option 1: Docker Container (Recommended for Production)

**1. Pull Ollama Image:**
```bash
docker pull ollama/ollama
```

**2. Run Ollama Container:**
```bash
# CPU-only version
docker run -d \
  --name ollama \
  --network support-ticket-triage-system_triage-network \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama

# With GPU support (NVIDIA)
docker run -d \
  --name ollama \
  --network support-ticket-triage-system_triage-network \
  --gpus all \
  -p 11434:11434 \
  -v ollama_data:/root/.ollama \
  ollama/ollama
```

**3. Pull Language Model:**
```bash
# Recommended: llama3.2 (2GB)
docker exec ollama ollama pull llama3.2

# Alternative: llama3.2:3b (lighter, faster)
docker exec ollama ollama pull llama3.2:3b

# Alternative: mistral (7GB, higher quality)
docker exec ollama ollama pull mistral
```

**4. Verify Installation:**
```bash
# List installed models
docker exec ollama ollama list

# Test generation
docker exec ollama ollama run llama3.2 "Hello, how are you?"
```

---

### Option 2: Native Installation (Development)

**macOS:**
```bash
# Install via Homebrew
brew install ollama

# Start Ollama service
ollama serve

# Pull model
ollama pull llama3.2
```

**Linux:**
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start service
systemctl start ollama

# Pull model
ollama pull llama3.2
```

**Windows:**
- Download installer from https://ollama.com/download
- Run installer
- Open command prompt and run: `ollama pull llama3.2`

---

## Environment Configuration

### Backend Environment Variables

Create or update `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@triage-pg:5432/triage

# Redis (for WebSocket pub/sub)
REDIS_URL=redis://triage-redis:6379/0

# LLM Configuration
OLLAMA_URL=http://ollama:11434  # Use 'ollama' hostname in Docker network
LLM_MODEL=llama3.2:latest        # Model name from 'ollama list'
USE_OLLAMA=true                   # Enable Ollama (set to false to disable)
OPENAI_API_KEY=                   # Optional fallback (leave empty if not using)

# Application Settings
LOG_LEVEL=INFO
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
```

### Frontend Environment Variables

Create or update `frontend/.env`:

```bash
# API Base URL
NUXT_PUBLIC_API_BASE=http://localhost:8000

# WebSocket URL
NUXT_PUBLIC_WS_BASE=ws://localhost:8000
```

---

## Docker Compose Setup

### Update docker-compose.yml

Add Ollama service and environment variables:

```yaml
version: '3.8'

services:
  # Existing services...
  
  # Ollama LLM Service
  ollama:
    image: ollama/ollama
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    networks:
      - triage-network
    restart: unless-stopped
    # Uncomment for GPU support:
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - driver: nvidia
    #           count: 1
    #           capabilities: [gpu]

  backend:
    # ... existing configuration ...
    environment:
      # ... existing env vars ...
      - OLLAMA_URL=${OLLAMA_URL:-http://ollama:11434}
      - LLM_MODEL=${LLM_MODEL:-llama3.2:latest}
      - USE_OLLAMA=${USE_OLLAMA:-true}
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - REDIS_URL=redis://triage-redis:6379/0
    depends_on:
      - triage-pg
      - triage-redis
      - ollama

volumes:
  ollama_data:
    driver: local
  # ... other volumes ...

networks:
  triage-network:
    driver: bridge
```

### Deploy All Services

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f backend ollama triage-redis
```

### Pull Model After First Deploy

```bash
# Pull the model inside the container
docker exec ollama ollama pull llama3.2

# Verify
docker exec ollama ollama list
```

---

## Database Migrations

### AI Responses Table

Run the migration to create the `ai_responses` table:

```bash
# Option 1: Using Docker exec
docker exec triage-backend python -c "
from app.scripts.migrate_ai_responses import run_migration
run_migration()
"

# Option 2: Direct SQL
docker exec triage-pg psql -U postgres -d triage -c "
CREATE TABLE IF NOT EXISTS ai_responses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticket_id UUID NOT NULL REFERENCES tickets(id) ON DELETE CASCADE,
    response_text TEXT NOT NULL,
    tone VARCHAR(50) NOT NULL,
    context_used JSONB,
    model VARCHAR(100),
    agent_id VARCHAR(100),
    was_edited BOOLEAN DEFAULT false,
    was_sent BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_ai_responses_ticket_id 
    ON ai_responses(ticket_id);
CREATE INDEX IF NOT EXISTS idx_ai_responses_agent_id 
    ON ai_responses(agent_id);
CREATE INDEX IF NOT EXISTS idx_ai_responses_created_at 
    ON ai_responses(created_at DESC);
"
```

### Verify Migration

```bash
# Check table exists
docker exec triage-pg psql -U postgres -d triage -c "\d ai_responses"

# Check indexes
docker exec triage-pg psql -U postgres -d triage -c "\di ai_responses*"
```

---

## Redis Configuration

### Redis for WebSocket Pub/Sub

Redis is used for broadcasting WebSocket messages across multiple backend instances.

**Configuration in docker-compose.yml:**
```yaml
triage-redis:
  image: redis:7-alpine
  container_name: triage-redis
  ports:
    - "6379:6379"
  volumes:
    - redis_data:/data
  networks:
    - triage-network
  command: redis-server --appendonly yes
  restart: unless-stopped
```

**Verify Redis Connection:**
```bash
# Test connection
docker exec triage-redis redis-cli ping
# Should output: PONG

# Monitor pub/sub messages
docker exec triage-redis redis-cli MONITOR
```

---

## Production Deployment

### Security Considerations

**1. Environment Variables:**
```bash
# Use strong passwords
DATABASE_URL=postgresql://user:STRONG_PASSWORD@host:5432/db

# Restrict CORS origins
CORS_ORIGINS=https://yourdomain.com

# Set secure Redis password
REDIS_URL=redis://:REDIS_PASSWORD@host:6379/0
```

**2. Update docker-compose for Production:**
```yaml
backend:
  environment:
    - LOG_LEVEL=WARNING  # Reduce logging noise
    - CORS_ORIGINS=https://yourdomain.com
  restart: always

ollama:
  restart: always
  # Limit resources if needed
  deploy:
    resources:
      limits:
        cpus: '4'
        memory: 8G
```

**3. HTTPS/WSS Configuration:**

Use nginx or Traefik as reverse proxy:

```nginx
# WebSocket upgrade
location /ws/ {
    proxy_pass http://backend:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}

# Regular API
location /api/ {
    proxy_pass http://backend:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
}
```

---

### Performance Tuning

**1. Ollama Model Selection:**

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| llama3.2:1b | 1.3GB | Fast | Good | High volume, simple responses |
| llama3.2 (3b) | 2.0GB | Medium | Better | **Recommended for production** |
| mistral | 4.1GB | Slower | Best | Premium support, complex responses |

**2. Backend Workers:**
```yaml
backend:
  command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

**3. Redis Persistence:**
```yaml
triage-redis:
  command: redis-server --appendonly yes --save 60 1000
```

**4. Database Connection Pooling:**
```python
# backend/app/db/base.py
engine = create_engine(
    DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

---

### Scaling Considerations

**Horizontal Scaling (Multiple Backend Instances):**

```yaml
backend:
  deploy:
    replicas: 3
  environment:
    - REDIS_URL=redis://triage-redis:6379/0  # Shared Redis for WebSocket
```

**Load Balancer Configuration:**
```nginx
upstream backend {
    least_conn;
    server backend1:8000;
    server backend2:8000;
    server backend3:8000;
}
```

**Ollama Load Balancing:**
```bash
# Run multiple Ollama instances on different GPUs
docker run -d --name ollama1 --gpus '"device=0"' ollama/ollama
docker run -d --name ollama2 --gpus '"device=1"' ollama/ollama
```

---

## Monitoring and Troubleshooting

### Health Checks

**1. Backend Health:**
```bash
curl http://localhost:8000/health
# Should return: {"status": "ok"}
```

**2. Ollama Health:**
```bash
curl http://localhost:11434/api/tags
# Should return list of models
```

**3. WebSocket Status:**
```bash
curl http://localhost:8000/ws/status
# Returns: {"active_connections": N, "redis_connected": true}
```

**4. Redis Health:**
```bash
docker exec triage-redis redis-cli ping
# Should return: PONG
```

---

### Common Issues

**Issue 1: "Cannot connect to Ollama"**

**Symptoms:**
- AI responses return fallback templates
- Logs show: `Failed to connect to Ollama`

**Solution:**
```bash
# Check Ollama is running
docker ps | grep ollama

# Check network connectivity
docker exec triage-backend ping ollama

# Verify OLLAMA_URL uses container hostname
# Should be: http://ollama:11434
# NOT: http://localhost:11434
```

---

**Issue 2: "Model not found"**

**Symptoms:**
- Error: `model 'llama3.2:latest' not found`

**Solution:**
```bash
# List available models
docker exec ollama ollama list

# Pull the model
docker exec ollama ollama pull llama3.2

# Restart backend
docker-compose restart backend
```

---

**Issue 3: "WebSocket disconnects frequently"**

**Symptoms:**
- WebSocket connections drop after 30-60 seconds
- No reconnection

**Solution:**
```bash
# Check Redis connection
docker exec triage-redis redis-cli ping

# Enable WebSocket ping/pong in frontend
# See PHASE5_API_DOCS.md for implementation

# Check nginx/proxy timeout settings
proxy_read_timeout 3600s;
proxy_send_timeout 3600s;
```

---

**Issue 4: "Slow AI response generation"**

**Symptoms:**
- Responses take >30 seconds
- Timeout errors

**Solution:**
```bash
# Check Ollama resource usage
docker stats ollama

# Use smaller/faster model
docker exec ollama ollama pull llama3.2:1b

# Update LLM_MODEL in .env
LLM_MODEL=llama3.2:1b

# Enable GPU acceleration (if available)
# See Ollama Installation section
```

---

### Logs and Debugging

**View Backend Logs:**
```bash
docker-compose logs -f backend
```

**View Ollama Logs:**
```bash
docker logs -f ollama
```

**View Redis Logs:**
```bash
docker logs -f triage-redis
```

**Enable Debug Logging:**
```bash
# Update .env
LOG_LEVEL=DEBUG

# Restart services
docker-compose restart backend
```

---

### Performance Monitoring

**Database Queries:**
```sql
-- Slowest queries
SELECT query, mean_exec_time, calls 
FROM pg_stat_statements 
ORDER BY mean_exec_time DESC 
LIMIT 10;

-- AI responses statistics
SELECT 
    tone,
    COUNT(*) as count,
    AVG(CASE WHEN was_edited THEN 1 ELSE 0 END) * 100 as edit_rate
FROM ai_responses
GROUP BY tone;
```

**WebSocket Connections:**
```bash
# Real-time connection count
watch -n 1 'curl -s http://localhost:8000/ws/status | jq'
```

**Ollama Performance:**
```bash
# Monitor model memory usage
docker exec ollama ollama ps

# Test generation speed
time docker exec ollama ollama run llama3.2 "Generate a support response"
```

---

## Backup and Recovery

### Database Backup

```bash
# Backup
docker exec triage-pg pg_dump -U postgres triage > backup_$(date +%Y%m%d).sql

# Restore
docker exec -i triage-pg psql -U postgres triage < backup_20251112.sql
```

### Ollama Models Backup

```bash
# Backup models volume
docker run --rm \
  -v ollama_data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/ollama_models.tar.gz /data

# Restore
docker run --rm \
  -v ollama_data:/data \
  -v $(pwd):/backup \
  alpine tar xzf /backup/ollama_models.tar.gz -C /
```

---

## Upgrade Guide

### Upgrading Ollama Models

```bash
# Pull new model version
docker exec ollama ollama pull llama3.2:latest

# Test new model
docker exec ollama ollama run llama3.2:latest "Test message"

# Update environment variable if needed
# No restart required - changes take effect on next request
```

### Upgrading Backend

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build backend

# Restart services
docker-compose up -d backend
```

---

## Additional Resources

- [API Documentation](./PHASE5_API_DOCS.md)
- [User Guide](./PHASE5_USER_GUIDE.md)
- [Architecture Overview](./architecture.md)
- [Ollama Documentation](https://ollama.com/docs)
- [Redis Pub/Sub Guide](https://redis.io/docs/manual/pubsub/)
