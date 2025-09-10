# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a support ticket triage system designed to automatically categorize, prioritize, and route support tickets based on content analysis and business rules.

## Development Commands

*Note: Commands will be updated as the project structure is established*

### Setup
```powershell
# Install dependencies (to be updated based on chosen tech stack)
# npm install  # for Node.js projects
# pip install -r requirements.txt  # for Python projects
# go mod tidy  # for Go projects
```

### Running the Application
```powershell
# Start development server (to be updated)
# npm run dev  # for Node.js
# python app.py  # for Python
# go run main.go  # for Go
```

### Testing
```powershell
# Run all tests (to be updated)
# npm test  # for Node.js
# pytest  # for Python
# go test ./...  # for Go

# Run specific test file (to be updated)
# npm test -- filename.test.js  # for Node.js
# pytest tests/test_filename.py  # for Python
# go test ./pkg/module  # for Go
```

### Linting and Formatting
```powershell
# Lint code (to be updated)
# npm run lint  # for Node.js
# flake8 .  # for Python
# golangci-lint run  # for Go

# Format code (to be updated)
# npm run format  # for Node.js
# black .  # for Python
# gofmt -w .  # for Go
```

## Architecture Considerations

Based on the project name, this system should be designed with the following key components:

### Core Components
- **Ticket Ingestion**: System to receive tickets from various sources (email, web forms, API)
- **Content Analysis**: NLP/ML components to analyze ticket content for categorization
- **Triage Engine**: Business logic to prioritize and route tickets
- **Routing System**: Logic to assign tickets to appropriate teams/individuals
- **Notification System**: Alerts and updates for stakeholders
- **Reporting/Analytics**: Metrics and insights on ticket patterns

### Data Flow
1. Tickets enter through various channels
2. Content is analyzed for keywords, sentiment, and urgency indicators
3. Triage engine applies business rules and ML models
4. Tickets are categorized, prioritized, and routed
5. Stakeholders receive notifications
6. Progress is tracked and reported

## Key Integration Points

The system should be designed to integrate with:
- **Ticketing Systems**: ServiceNow, Zendesk, Jira Service Management
- **Communication Platforms**: Slack, Microsoft Teams, email
- **Monitoring Tools**: For system health and performance metrics
- **Authentication Systems**: SSO, LDAP integration

## Development Guidelines

### Code Organization
- Separate concerns: ingestion, analysis, triage, routing, notifications
- Use dependency injection for testability
- Implement proper error handling and logging
- Design with scalability in mind (queue-based processing)

### Performance Considerations
- Async processing for ticket analysis
- Caching for frequently accessed data
- Database indexing for ticket queries
- Rate limiting for API endpoints

### Security Requirements
- Secure handling of potentially sensitive ticket content
- API authentication and authorization
- Data encryption at rest and in transit
- Audit logging for compliance

## Environment Setup

### Required Services
- Database (PostgreSQL, MongoDB, etc.)
- Message Queue (RabbitMQ, Apache Kafka, etc.)
- Cache (Redis, Memcached)
- ML/NLP Services (if using external APIs)

### Configuration Management
- Environment-specific configuration files
- Secure secret management (Azure Key Vault, AWS Secrets Manager, etc.)
- Feature flags for gradual rollouts

## Monitoring and Observability

### Key Metrics
- Ticket processing throughput
- Triage accuracy rates
- Response time SLAs
- System resource utilization

### Logging Strategy
- Structured logging for better searchability
- Different log levels (DEBUG, INFO, WARN, ERROR)
- Request/response logging for debugging
- Performance metrics logging

---

*This WARP.md file will be updated as the project structure and implementation details are established.*
