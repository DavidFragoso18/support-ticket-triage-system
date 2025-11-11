# 🎟️ AI-Powered Support Ticket Triage System

[![Build Status](https://github.com/DavidFragoso18/support-ticket-triage-system/actions/workflows/ci.yml/badge.svg)](https://github.com/DavidFragoso18/support-ticket-triage-system/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linter-ruff-success)](https://github.com/astral-sh/ruff)

An intelligent helpdesk tool that automatically triages incoming support tickets, prioritizes them, and suggests responses using **AI/NLP**.  
Built with **FastAPI, Hugging Face, PostgreSQL, and React** — this project demonstrates real-world **AI + backend + frontend + cloud deployment** skills.

---

## 🚧 Current Phase

**Phase 3 – Cloud + DevOps (In progress 🚀)**  
✅ Docker containerization (multi-stage builds).  
✅ Docker Compose orchestration.  
✅ CI/CD with GitHub Actions.  
✅ AWS deployment automation scripts.  
🚧 Production deployment verification.  

*Next: Phase 4 – Advanced AI Features  

---

## ✨ Features (current + planned)

- **AI-Powered Classification (Phase 1)**  
  - Hugging Face zero-shot for **intent classification**.  
  - Sentiment analysis (negative/neutral/positive).  
  - Deterministic **priority rules** layered on model outputs.  
  - Confidence thresholds + near-tie detection.  

- **Ticket Persistence (Phase 1)**  
  - FastAPI endpoints store tickets in PostgreSQL.  
  - Classifications saved alongside tickets.  
  - Pagination and retrieval endpoints.  

- **Smart Suggestions (Phase 2+)**  
  - Suggest KB articles or past resolutions using embeddings.  

- **Feedback Loop (Phase 4)**  
  - Agents can accept/reject/edit suggestions for retraining.  

- **Multi-Language Support (Phase 4)**  
  - Auto-detect ticket language, route to bilingual agent or translate.  

- **Agent Dashboard (Phase 2+)**  
  - Ticket list + filters (intent, sentiment, priority).  
  - Ticket detail with AI classification + suggestions.  
  - Analytics (trends, model accuracy).  

- **Cloud Deployment (Phase 3+)**  
  - Dockerized backend + DB.  
  - AWS (EC2, RDS, S3, Lambda).  
  - CI/CD with GitHub Actions.  

---

## 🛠 Tech Stack

**Backend:** FastAPI, SQLModel, PostgreSQL  
**AI/ML:** Hugging Face Transformers (zero-shot + sentiment), PyTorch  
**Frontend:** React (or Vue), TailwindCSS  
**DevOps:** Docker, AWS, GitHub Actions, Makefile for local workflow  
**Testing:** pytest, httpx  

---

## 📂 Project Structure

```
support-ticket-triage-system/
├── backend/         # FastAPI app (APIs, models, NLP pipeline)
│   ├── app/
│   ├── tests/       # pytest smoke tests
│   └── .venv/       # Python virtual environment
├── frontend/        # React/Vue dashboard (Phase 2)
├── infra/           # Dockerfiles, CI/CD, AWS configs
├── docs/            # API contracts, DB schema, architecture
├── Makefile         # Dev workflow commands
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone repo
```bash
git clone https://github.com/DavidFragoso18/support-ticket-triage-system.git
cd support-ticket-triage-system
```

### 2. Start Postgres (Docker)
```bash
make up-db
```

### 3. Backend setup
```bash
cd backend
py -3.11 -m venv .venv
.\.venv\Scriptsctivate
pip install -U pip
pip install -e .
```

### 4. Run API
```bash
make up-api
```
Visit: [http://localhost:8000/docs](http://localhost:8000/docs)

### 5. Run tests
```bash
make test
```

---

## � Docker Deployment

### Quick Start with Docker Compose

The easiest way to run the entire stack (backend + frontend + database):

```bash
# Clone repository
git clone https://github.com/DavidFragoso18/support-ticket-triage-system.git
cd support-ticket-triage-system

# Copy environment file and configure
cp .env.docker .env
# Edit .env if needed

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
# Backend API: http://localhost:8000/docs
# Frontend: http://localhost:3000
# Database: localhost:5432
```

### Docker Commands

```bash
# Build images
docker-compose build

# Start services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Stop services
docker-compose down

# Stop and remove volumes (clean state)
docker-compose down -v

# Rebuild and restart specific service
docker-compose up -d --build backend

# Execute commands in running containers
docker-compose exec backend python -m app.scripts.seed_kb
docker-compose exec backend pytest tests/

# Check service status
docker-compose ps
```

### Build Individual Images

```bash
# Build backend image
cd backend
docker build -t triage-backend:latest .

# Build frontend image
cd frontend
docker build -t triage-frontend:latest .

# Run backend container
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql+psycopg://postgres:postgres@host.docker.internal:5432/triage \
  triage-backend:latest
```

---

## ☁️ AWS Cloud Deployment

Deploy the complete system to AWS with automated scripts.

### Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured (`aws configure`)
- Docker installed locally (for building images)

### Automated Deployment

```bash
# 1. Configure AWS CLI
aws configure

# 2. Run infrastructure setup (creates VPC, EC2, RDS, S3)
cd infra
chmod +x setup-aws.sh
./setup-aws.sh

# This will create:
# - VPC with subnets and security groups
# - RDS PostgreSQL 16 with pgvector
# - S3 bucket for attachments
# - EC2 instance (t3.medium)
# - SSH key pair (triage-key.pem)

# 3. SSH to EC2 instance
ssh -i triage-key.pem ubuntu@<EC2_PUBLIC_IP>

# 4. Setup EC2 instance
wget https://raw.githubusercontent.com/DavidFragoso18/support-ticket-triage-system/main/infra/setup-ec2.sh
chmod +x setup-ec2.sh
./setup-ec2.sh

# Logout and login again
exit
ssh -i triage-key.pem ubuntu@<EC2_PUBLIC_IP>

# 5. Deploy application
git clone https://github.com/DavidFragoso18/support-ticket-triage-system.git
cd support-ticket-triage-system

# Configure environment
cp .env.docker .env
# Edit .env with RDS endpoint and credentials from setup-aws.sh output

# Start services
docker-compose up -d

# Initialize database
docker-compose exec backend python -m app.scripts.seed_kb
docker-compose exec backend python -m app.scripts.seed_tickets
```

### CI/CD with GitHub Actions

The repository includes automated CI/CD pipeline that:

1. **Runs tests** on every push and pull request
2. **Builds Docker images** and pushes to GitHub Container Registry
3. **Deploys to AWS EC2** automatically on push to `main` branch

To enable automatic deployment, add these secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: Your AWS region (e.g., us-east-1)
- `EC2_HOST`: Your EC2 public IP or domain
- `EC2_USER`: ubuntu
- `EC2_SSH_KEY`: Contents of your triage-key.pem file

### Manual AWS Setup

For detailed manual setup instructions, see: **[docs/aws-deployment.md](docs/aws-deployment.md)**

### Cleanup AWS Resources

To delete all AWS resources and avoid charges:

```bash
cd infra
chmod +x cleanup-aws.sh
./cleanup-aws.sh
```

**⚠️ WARNING**: This will permanently delete all resources including databases!

---

## �📊 Roadmap

### Phase 1 – Foundations (Done ✅)  
- Repo hygiene, FastAPI setup, Hugging Face NLP, DB schema, smoke tests.  

### Phase 2 – Core Features (In progress 🚀)  
✅ Ticket filters (intent/sentiment/priority).  
✅ Agent dashboard (Vue/Nuxt).  
🚧 Smart Suggestions MVP.  

### Phase 3 – Cloud + DevOps (In progress 🚀)  
✅ Multi-stage Dockerfiles for backend + frontend.  
✅ Docker Compose orchestration.  
✅ GitHub Actions CI/CD pipeline.  
✅ AWS deployment scripts (EC2, RDS, S3).  
✅ Infrastructure automation (shell scripts).  
🚧 Terraform/CloudFormation templates (optional).  
⬜ Production deployment and monitoring.  

### Phase 4 – Advanced AI Features  
- Feedback loop.  
- Vector search for better suggestions.  
- Multi-language support.  
- Fine-tune NLP model.  

### Phase 5 – Portfolio Polish  
- Analytics dashboard.  
- API docs & diagrams.  
- Demo video + resume bullets.  

---

## 📝 Resume Pitch

> Built an **AI-powered support triage platform** (FastAPI + Hugging Face + PostgreSQL + AWS) with automatic classification, sentiment analysis, and priority rules.  
> Designed modular architecture with NLP + business rules, validated via smoke tests, and prepared for cloud-native deployment.  
> Demonstrated ~90% classification accuracy and designed for a 50% reduction in first-response time.  

---

## 📜 License
MIT License — free to use, adapt, and share.  
