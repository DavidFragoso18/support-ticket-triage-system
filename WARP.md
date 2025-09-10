# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is an AI-powered support ticket triage system that automatically classifies, prioritizes, and suggests responses for incoming support tickets using NLP/ML models. Built with FastAPI backend, Hugging Face transformers, PostgreSQL database, and React frontend.

## Development Commands

### Setup
```powershell
# Python development setup
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"

# Install pre-commit hooks (optional but recommended)
pre-commit install

# For other tech stacks
# npm install  # for frontend React app
# docker-compose up --build  # for full stack with Docker
```

### Running the Application
```powershell
# Start FastAPI backend
cd backend
uvicorn main:app --reload

# Start React frontend (separate terminal)
cd frontend
npm run dev

# Run full stack with Docker
docker-compose up --build
```

### Testing
```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_classification.py

# Run tests with specific markers
pytest -m "not slow"  # skip slow tests
pytest -m integration  # run integration tests only
```

### Linting and Formatting
```powershell
# Format code with Black
black .

# Lint with Ruff
ruff check .

# Auto-fix linting issues
ruff check . --fix

# Run pre-commit hooks manually
pre-commit run --all-files

# Frontend linting (when in frontend directory)
npm run lint
npm run format
```

## Architecture Overview

### Core Components
- **FastAPI Backend** (`backend/`): REST API, authentication, ticket endpoints
- **ML Pipeline** (`ml/`): NLP models for classification, sentiment analysis, suggestion engine  
- **React Dashboard** (`frontend/`): Support agent interface with ticket management
- **Infrastructure** (`infra/`): Docker configs, AWS deployment scripts

### Data Flow
1. **Ticket Ingestion**: Tickets arrive via API, email webhooks, or Slack integration
2. **NLP Processing**: Hugging Face models classify intent/topic and analyze sentiment
3. **Priority Assignment**: Rule-based system assigns priority based on classification + sentiment
4. **Smart Suggestions**: Vector search finds similar past resolutions and KB articles
5. **Agent Review**: Support agents review AI predictions and suggestions in React dashboard
6. **Feedback Loop**: Agent corrections are stored to retrain and improve models

### Key Technologies
- **AI/ML**: Hugging Face Transformers, spaCy, PyTorch, vector embeddings
- **Backend**: FastAPI, PostgreSQL, SQLAlchemy, Pydantic
- **Frontend**: React, TailwindCSS, Axios
- **Infrastructure**: Docker, AWS (EC2, RDS, S3, Lambda), GitHub Actions

## Development Guidelines

### Code Organization
- `backend/`: FastAPI application with clear separation of routes, models, and services
- `ml/`: ML pipeline with training scripts, model inference, and evaluation
- `frontend/`: React components organized by feature (tickets, dashboard, analytics)
- `tests/`: Unit and integration tests mirroring source structure

### ML Model Management
- Models stored in `ml/models/` with version tracking
- Training data and evaluation scripts in `ml/training/`
- Model inference wrapped in FastAPI services for scalability
- Feedback data collection for continuous model improvement

### Database Schema
- **tickets**: Core ticket data (id, content, status, priority, timestamps)
- **classifications**: AI predictions (ticket_id, topic, sentiment, confidence)
- **suggestions**: Smart suggestions (ticket_id, suggestion_type, content, relevance_score)
- **feedback**: Agent corrections (prediction_id, agent_id, correction, timestamp)

### API Design
- RESTful endpoints following FastAPI best practices
- Async/await for I/O operations (DB queries, ML inference)
- Pydantic models for request/response validation
- Authentication via JWT tokens

## Key Integration Points

### External Services
- **Hugging Face Hub**: Pre-trained NLP models for classification
- **Email/Slack APIs**: Ticket ingestion from multiple channels  
- **Translation APIs**: Multi-language support (DeepL, Google Translate)
- **Vector Databases**: Similarity search for smart suggestions (Pinecone, Weaviate)

### AWS Services
- **EC2**: FastAPI backend hosting
- **RDS PostgreSQL**: Primary database
- **S3**: Model artifacts, file attachments, logs
- **Lambda**: Serverless ML inference for peak loads

## Performance Considerations

### ML Pipeline
- Async model inference to handle multiple tickets simultaneously
- Model caching to avoid repeated loading
- Batch processing for similar tickets
- GPU acceleration for transformer models when available

### Database Optimization  
- Indexes on frequently queried fields (status, priority, created_at)
- Connection pooling for concurrent requests
- Read replicas for analytics queries
- Archiving strategy for old tickets

### Caching Strategy
- Redis for session data and frequent model predictions
- CDN for static frontend assets
- Model prediction caching with TTL

## Security Requirements

### Data Protection
- Encrypt sensitive ticket content at rest and in transit
- PII detection and masking in logs
- GDPR compliance for data retention and deletion
- Secure model artifact storage

### API Security
- JWT authentication with proper expiration
- Rate limiting on all endpoints
- Input validation and sanitization
- CORS configuration for frontend integration

## Testing Strategy

### Unit Tests
- ML model accuracy and performance tests
- FastAPI endpoint testing with test database
- React component testing with Jest/Testing Library

### Integration Tests  
- End-to-end ticket processing workflow
- ML pipeline integration with API
- Database migration and schema validation

### Performance Tests
- Load testing for concurrent ticket processing
- ML model inference latency benchmarks
- Database query performance under load

## Monitoring and Observability

### Key Metrics
- **ML Performance**: Classification accuracy, prediction confidence, suggestion relevance
- **System Performance**: API response times, throughput, error rates
- **Business Metrics**: Ticket resolution time, agent efficiency, customer satisfaction

### Logging Strategy
- Structured logging with correlation IDs for request tracing
- ML prediction logging for model evaluation and debugging  
- Agent feedback logging for continuous improvement
- Security event logging for audit trails

### Health Checks
- API endpoint health monitoring
- Database connectivity checks
- ML model availability verification
- External service dependency monitoring

---

*This system demonstrates real-world AI + backend + frontend + cloud deployment skills for portfolio showcase.*
