# AWS Deployment Guide

This guide walks you through deploying the AI-Powered Support Ticket Triage System to AWS using EC2, RDS, and S3.

## 📋 Prerequisites

- AWS Account with appropriate permissions
- AWS CLI installed and configured
- Docker and Docker Compose installed locally
- Domain name (optional, for production)
- SSH key pair for EC2 access

## 🏗️ Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                        AWS Cloud                            │
│                                                             │
│  ┌──────────────┐      ┌──────────────┐                    │
│  │   Route 53   │─────▶│  CloudFront  │ (Optional)         │
│  └──────────────┘      └──────────────┘                    │
│                              │                              │
│                              ▼                              │
│  ┌──────────────────────────────────────────┐              │
│  │         Application Load Balancer         │              │
│  └──────────────────────────────────────────┘              │
│                    │                 │                      │
│         ┌──────────┴──────────┐     │                      │
│         ▼                     ▼     │                      │
│  ┌─────────────┐       ┌─────────────┐                    │
│  │  EC2 (API)  │       │EC2 (Frontend)│                   │
│  │   Backend   │       │   Nuxt.js    │                   │
│  │   FastAPI   │       │              │                   │
│  └─────────────┘       └─────────────┘                    │
│         │                                                   │
│         ▼                                                   │
│  ┌─────────────┐       ┌─────────────┐                    │
│  │   RDS PG    │       │     S3      │                    │
│  │  (pgvector) │       │ (Attachments)│                   │
│  └─────────────┘       └─────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Deployment Steps

### 1. Set Up AWS Infrastructure

#### 1.1 Create VPC and Security Groups

```bash
# Create VPC
aws ec2 create-vpc \
  --cidr-block 10.0.0.0/16 \
  --tag-specifications 'ResourceType=vpc,Tags=[{Key=Name,Value=triage-vpc}]'

# Create subnets
aws ec2 create-subnet \
  --vpc-id <vpc-id> \
  --cidr-block 10.0.1.0/24 \
  --availability-zone us-east-1a

aws ec2 create-subnet \
  --vpc-id <vpc-id> \
  --cidr-block 10.0.2.0/24 \
  --availability-zone us-east-1b

# Create Internet Gateway
aws ec2 create-internet-gateway \
  --tag-specifications 'ResourceType=internet-gateway,Tags=[{Key=Name,Value=triage-igw}]'

# Attach Internet Gateway to VPC
aws ec2 attach-internet-gateway \
  --vpc-id <vpc-id> \
  --internet-gateway-id <igw-id>

# Create Security Group for Backend
aws ec2 create-security-group \
  --group-name triage-backend-sg \
  --description "Security group for Triage Backend" \
  --vpc-id <vpc-id>

# Allow HTTP, HTTPS, and SSH
aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> \
  --protocol tcp \
  --port 8000 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id <sg-id> \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0
```

#### 1.2 Launch RDS PostgreSQL Instance

```bash
# Create DB subnet group
aws rds create-db-subnet-group \
  --db-subnet-group-name triage-db-subnet \
  --db-subnet-group-description "Subnet group for Triage DB" \
  --subnet-ids <subnet-1-id> <subnet-2-id>

# Create RDS instance with pgvector support
aws rds create-db-instance \
  --db-instance-identifier triage-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --engine-version 16.1 \
  --master-username postgres \
  --master-user-password <strong-password> \
  --allocated-storage 20 \
  --vpc-security-group-ids <sg-id> \
  --db-subnet-group-name triage-db-subnet \
  --backup-retention-period 7 \
  --publicly-accessible false \
  --storage-encrypted \
  --tags Key=Name,Value=triage-db

# After instance is created, install pgvector extension
# Connect to RDS and run:
# CREATE EXTENSION IF NOT EXISTS vector;
```

#### 1.3 Create S3 Bucket for Attachments

```bash
# Create S3 bucket
aws s3api create-bucket \
  --bucket triage-attachments-${RANDOM} \
  --region us-east-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket <bucket-name> \
  --versioning-configuration Status=Enabled

# Set CORS configuration
cat > cors.json << EOF
{
  "CORSRules": [
    {
      "AllowedOrigins": ["*"],
      "AllowedMethods": ["GET", "POST", "PUT", "DELETE"],
      "AllowedHeaders": ["*"],
      "ExposeHeaders": ["ETag"],
      "MaxAgeSeconds": 3000
    }
  ]
}
EOF

aws s3api put-bucket-cors \
  --bucket <bucket-name> \
  --cors-configuration file://cors.json
```

### 2. Launch EC2 Instance

#### 2.1 Create EC2 Instance

```bash
# Create key pair
aws ec2 create-key-pair \
  --key-name triage-key \
  --query 'KeyMaterial' \
  --output text > triage-key.pem

chmod 400 triage-key.pem

# Launch EC2 instance (Ubuntu 22.04 LTS)
aws ec2 run-instances \
  --image-id ami-0c7217cdde317cfec \
  --instance-type t3.medium \
  --key-name triage-key \
  --security-group-ids <sg-id> \
  --subnet-id <subnet-id> \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=triage-backend}]' \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":30}}]'
```

#### 2.2 Set Up EC2 Instance

SSH into the instance:

```bash
ssh -i triage-key.pem ubuntu@<ec2-public-ip>
```

Install Docker and Docker Compose:

```bash
# Update system
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
sudo apt-get install -y git

# Logout and login again to apply docker group
exit
```

### 3. Deploy Application

#### 3.1 Clone Repository

```bash
ssh -i triage-key.pem ubuntu@<ec2-public-ip>

# Clone repository
git clone https://github.com/DavidFragoso18/support-ticket-triage-system.git
cd support-ticket-triage-system
```

#### 3.2 Configure Environment

```bash
# Create .env file
cat > .env << EOF
APP_ENV=production
LOG_LEVEL=INFO

# Database (RDS endpoint)
POSTGRES_USER=postgres
POSTGRES_PASSWORD=<your-rds-password>
POSTGRES_DB=triage
DATABASE_URL=postgresql+psycopg://postgres:<password>@<rds-endpoint>:5432/triage

# Backend API
API_PORT=8000
ALLOWED_ORIGINS=http://<ec2-public-ip>:3000,https://<your-domain>

# Hugging Face Models
HF_MODEL_INTENT=facebook/bart-large-mnli
HF_MODEL_SENTIMENT=cardiffnlp/twitter-roberta-base-sentiment-latest

# Classification Thresholds
INTENT_LOW_CONF=0.50
SENTIMENT_LOW_CONF=0.60
NEAR_TIE_DELTA=0.05

# Frontend
FRONTEND_PORT=3000
NUXT_PUBLIC_API_BASE_URL=http://<ec2-public-ip>:8000

# AWS S3 (if using)
AWS_S3_BUCKET=<bucket-name>
AWS_REGION=us-east-1
EOF
```

#### 3.3 Build and Run with Docker Compose

```bash
# Build and start services
docker-compose up -d --build

# Check logs
docker-compose logs -f

# Verify services are running
docker-compose ps
```

#### 3.4 Initialize Database

```bash
# Run database migrations and seed data
docker-compose exec backend python -m app.scripts.enable_pgvector
docker-compose exec backend python -m app.scripts.seed_kb
docker-compose exec backend python -m app.scripts.seed_tickets
```

### 4. Set Up Domain and SSL (Optional)

#### 4.1 Configure Route 53

```bash
# Create hosted zone
aws route53 create-hosted-zone \
  --name example.com \
  --caller-reference $(date +%s)

# Create A record pointing to EC2
cat > change-batch.json << EOF
{
  "Changes": [
    {
      "Action": "CREATE",
      "ResourceRecordSet": {
        "Name": "triage.example.com",
        "Type": "A",
        "TTL": 300,
        "ResourceRecords": [{"Value": "<ec2-public-ip>"}]
      }
    }
  ]
}
EOF

aws route53 change-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --change-batch file://change-batch.json
```

#### 4.2 Install Certbot for SSL

```bash
# Install Certbot
sudo apt-get install -y certbot

# Get SSL certificate
sudo certbot certonly --standalone -d triage.example.com

# Set up Nginx as reverse proxy with SSL
sudo apt-get install -y nginx

# Configure Nginx (see nginx.conf in infra/)
sudo cp infra/nginx.conf /etc/nginx/sites-available/triage
sudo ln -s /etc/nginx/sites-available/triage /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### 5. Set Up Auto-Deployment with GitHub Actions

Add the following secrets to your GitHub repository:

- `AWS_ACCESS_KEY_ID`: Your AWS access key
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret key
- `AWS_REGION`: Your AWS region (e.g., us-east-1)
- `EC2_HOST`: Your EC2 public IP or domain
- `EC2_USER`: ubuntu
- `EC2_SSH_KEY`: Contents of your triage-key.pem file

The CI/CD pipeline will automatically deploy on push to main branch.

## 📊 Monitoring and Maintenance

### CloudWatch Logs

```bash
# Install CloudWatch agent
wget https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb
sudo dpkg -i amazon-cloudwatch-agent.deb

# Configure CloudWatch agent (see cloudwatch-config.json in infra/)
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config \
  -m ec2 \
  -s \
  -c file:///opt/aws/cloudwatch-config.json
```

### Backup Strategy

```bash
# Automated RDS snapshots are enabled by default
# Manual snapshot:
aws rds create-db-snapshot \
  --db-instance-identifier triage-db \
  --db-snapshot-identifier triage-db-snapshot-$(date +%Y%m%d)

# Backup S3 bucket
aws s3 sync s3://<bucket-name> s3://<backup-bucket-name>
```

### Scaling

- **Vertical Scaling**: Upgrade EC2 instance type (t3.medium → t3.large)
- **Horizontal Scaling**: Use Auto Scaling Group with Application Load Balancer
- **Database Scaling**: Upgrade RDS instance class or enable read replicas

## 💰 Cost Estimation (Monthly)

- EC2 t3.medium: ~$30
- RDS db.t3.micro: ~$15
- S3 storage (10GB): ~$0.23
- Data transfer: ~$5
- **Total**: ~$50/month

## 🔒 Security Best Practices

1. Use IAM roles instead of access keys on EC2
2. Enable encryption at rest for RDS and S3
3. Regularly update system packages and Docker images
4. Use AWS Secrets Manager for sensitive credentials
5. Enable AWS GuardDuty for threat detection
6. Set up VPC Flow Logs for network monitoring
7. Use AWS WAF if exposing to public internet

## 📚 Additional Resources

- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [AWS RDS PostgreSQL](https://docs.aws.amazon.com/rds/postgresql/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 🐛 Troubleshooting

### Application won't start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart

# Rebuild if needed
docker-compose down
docker-compose up -d --build
```

### Database connection issues

```bash
# Test RDS connection
docker run --rm postgres:16 psql postgresql://postgres:<password>@<rds-endpoint>:5432/triage

# Check security group rules
aws ec2 describe-security-groups --group-ids <sg-id>
```

### Out of memory

```bash
# Check memory usage
free -h
docker stats

# Upgrade instance type or add swap
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

## 📞 Support

For issues or questions, please open an issue on GitHub or contact the maintainer.
