# 🚀 Quick Reference - Docker & AWS Commands

## Docker Development

### Local Development
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs -f backend
docker-compose logs -f frontend

# Restart specific service
docker-compose restart backend

# Rebuild and restart
docker-compose up -d --build backend

# Stop all services
docker-compose down

# Stop and remove volumes (clean slate)
docker-compose down -v

# Check service status
docker-compose ps

# Execute command in container
docker-compose exec backend python -m app.scripts.seed_kb
docker-compose exec backend pytest tests/
docker-compose exec db psql -U postgres -d triage
```

### Build Individual Images
```bash
# Backend
docker build -f backend/Dockerfile -t triage-backend backend/

# Frontend
docker build -f frontend/Dockerfile -t triage-frontend frontend/
```

### Docker Debugging
```bash
# Interactive shell in container
docker-compose exec backend bash
docker-compose exec frontend sh

# Check resource usage
docker stats

# Inspect container
docker inspect triage-backend

# View container logs
docker logs triage-backend -f

# Clean up system
docker system prune -af
docker volume prune -f
```

## AWS Deployment

### Initial Setup
```bash
# Configure AWS CLI
aws configure

# Create infrastructure
cd infra
chmod +x setup-aws.sh
./setup-aws.sh

# SSH to EC2
ssh -i triage-key.pem ubuntu@<EC2_PUBLIC_IP>
```

### EC2 Setup
```bash
# On EC2 instance
wget https://raw.githubusercontent.com/DavidFragoso18/support-ticket-triage-system/main/infra/setup-ec2.sh
chmod +x setup-ec2.sh
./setup-ec2.sh

# Clone repository
git clone https://github.com/DavidFragoso18/support-ticket-triage-system.git
cd support-ticket-triage-system

# Configure environment
cp .env.docker .env
nano .env  # Edit with your RDS endpoint, passwords, etc.

# Deploy
docker-compose up -d
```

### AWS Monitoring
```bash
# View EC2 instances
aws ec2 describe-instances --query 'Reservations[].Instances[].[InstanceId,State.Name,PublicIpAddress]' --output table

# View RDS instances
aws rds describe-db-instances --query 'DBInstances[].[DBInstanceIdentifier,DBInstanceStatus,Endpoint.Address]' --output table

# View S3 buckets
aws s3 ls

# Check logs (CloudWatch)
aws logs tail /aws/ec2/triage/backend --follow

# Create RDS snapshot
aws rds create-db-snapshot --db-instance-identifier triage-db --db-snapshot-identifier triage-backup-$(date +%Y%m%d)
```

### AWS Cleanup
```bash
cd infra
chmod +x cleanup-aws.sh
./cleanup-aws.sh
```

## GitHub Actions

### Trigger Manual Deployment
```bash
git add .
git commit -m "Deploy to production"
git push origin main
```

### View Workflow Logs
- Go to: https://github.com/YOUR_USERNAME/support-ticket-triage-system/actions

### Required Secrets
```
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
AWS_REGION
EC2_HOST
EC2_USER
EC2_SSH_KEY
CODECOV_TOKEN (optional)
```

## Common Tasks

### Seed Database
```bash
# Local
docker-compose exec backend python -m app.scripts.seed_kb
docker-compose exec backend python -m app.scripts.seed_tickets

# AWS (via SSH)
ssh -i triage-key.pem ubuntu@<EC2_IP>
cd support-ticket-triage-system
docker-compose exec backend python -m app.scripts.seed_kb
```

### Run Tests
```bash
# Local
docker-compose exec backend pytest tests/ -v

# With coverage
docker-compose exec backend pytest tests/ --cov=app --cov-report=html
```

### Database Access
```bash
# Local
docker-compose exec db psql -U postgres -d triage

# AWS
psql "postgresql://postgres:PASSWORD@RDS_ENDPOINT:5432/triage"
```

### Update Application
```bash
# Local
git pull
docker-compose up -d --build

# AWS (via SSH)
ssh -i triage-key.pem ubuntu@<EC2_IP>
cd support-ticket-triage-system
git pull
docker-compose down
docker-compose up -d --build
```

### View API Documentation
- Local: http://localhost:8000/docs
- AWS: http://<EC2_IP>:8000/docs

### Backup & Restore

#### Backup Database
```bash
# Local
docker-compose exec db pg_dump -U postgres triage > backup.sql

# AWS
pg_dump "postgresql://postgres:PASSWORD@RDS_ENDPOINT:5432/triage" > backup.sql
```

#### Restore Database
```bash
# Local
docker-compose exec -T db psql -U postgres triage < backup.sql

# AWS
psql "postgresql://postgres:PASSWORD@RDS_ENDPOINT:5432/triage" < backup.sql
```

## Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Check if port is in use
lsof -i :8000

# Rebuild image
docker-compose build --no-cache backend
docker-compose up -d backend
```

### Database connection issues
```bash
# Check if database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Test connection
docker-compose exec db pg_isready -U postgres
```

### Out of memory
```bash
# Check Docker resources
docker stats

# Increase Docker memory limit in Docker Desktop settings

# On AWS, check instance metrics
aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name CPUUtilization --dimensions Name=InstanceId,Value=<INSTANCE_ID> --start-time 2024-01-01T00:00:00Z --end-time 2024-01-02T00:00:00Z --period 3600 --statistics Average
```

### Frontend not accessible
```bash
# Check if frontend is running
docker-compose ps frontend

# Check frontend logs
docker-compose logs frontend

# Rebuild frontend
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

## Environment Variables

### Required for Docker Compose
```bash
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/triage
ALLOWED_ORIGINS=http://localhost:3000
HF_MODEL_INTENT=facebook/bart-large-mnli
HF_MODEL_SENTIMENT=cardiffnlp/twitter-roberta-base-sentiment-latest
```

### Required for AWS
```bash
DATABASE_URL=postgresql+psycopg://postgres:PASSWORD@RDS_ENDPOINT:5432/triage
ALLOWED_ORIGINS=https://your-domain.com
AWS_S3_BUCKET=your-bucket-name
AWS_REGION=us-east-1
```

## Performance Tips

1. **Cache HuggingFace models**: Volume mounted at `/home/appuser/.cache/huggingface`
2. **Use Docker layer caching**: Build images incrementally
3. **Enable Docker BuildKit**: `export DOCKER_BUILDKIT=1`
4. **Prune regularly**: `docker system prune -af`
5. **Monitor resources**: `docker stats`

## Security Checklist

- [ ] Change default passwords
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS/SSL
- [ ] Configure firewall rules
- [ ] Regular security updates
- [ ] Use non-root containers
- [ ] Enable RDS encryption
- [ ] Use IAM roles instead of access keys
- [ ] Regular backups
- [ ] Monitor CloudWatch logs

## Links

- **Backend API**: http://localhost:8000/docs
- **Frontend**: http://localhost:3000
- **GitHub Actions**: https://github.com/YOUR_USERNAME/support-ticket-triage-system/actions
- **AWS Console**: https://console.aws.amazon.com/
- **Docker Hub**: https://hub.docker.com/
- **GitHub Container Registry**: https://ghcr.io
