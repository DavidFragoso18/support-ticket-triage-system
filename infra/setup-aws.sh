#!/bin/bash
# AWS Infrastructure Setup Script
# This script automates the AWS infrastructure deployment

set -e

echo "🚀 AWS Infrastructure Setup for AI Ticket Triage System"
echo "========================================================"

# Configuration
PROJECT_NAME="triage"
REGION="${AWS_REGION:-us-east-1}"
VPC_CIDR="10.0.0.0/16"
SUBNET1_CIDR="10.0.1.0/24"
SUBNET2_CIDR="10.0.2.0/24"
DB_INSTANCE_CLASS="${DB_INSTANCE_CLASS:-db.t3.micro}"
EC2_INSTANCE_TYPE="${EC2_INSTANCE_TYPE:-t3.medium}"
S3_BUCKET_PREFIX="triage-attachments"

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI is not installed. Please install it first."
    exit 1
fi

# Check if AWS credentials are configured
if ! aws sts get-caller-identity &> /dev/null; then
    echo "❌ AWS credentials are not configured. Please run 'aws configure'."
    exit 1
fi

echo "✅ AWS CLI configured for region: $REGION"
echo ""

# 1. Create VPC
echo "📦 Creating VPC..."
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block $VPC_CIDR \
    --tag-specifications "ResourceType=vpc,Tags=[{Key=Name,Value=$PROJECT_NAME-vpc}]" \
    --query 'Vpc.VpcId' \
    --output text)
echo "✅ VPC created: $VPC_ID"

# Enable DNS hostnames
aws ec2 modify-vpc-attribute --vpc-id $VPC_ID --enable-dns-hostnames

# 2. Create Internet Gateway
echo "🌐 Creating Internet Gateway..."
IGW_ID=$(aws ec2 create-internet-gateway \
    --tag-specifications "ResourceType=internet-gateway,Tags=[{Key=Name,Value=$PROJECT_NAME-igw}]" \
    --query 'InternetGateway.InternetGatewayId' \
    --output text)
aws ec2 attach-internet-gateway --vpc-id $VPC_ID --internet-gateway-id $IGW_ID
echo "✅ Internet Gateway created and attached: $IGW_ID"

# 3. Create Subnets
echo "📍 Creating subnets..."
SUBNET1_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block $SUBNET1_CIDR \
    --availability-zone ${REGION}a \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$PROJECT_NAME-subnet-1}]" \
    --query 'Subnet.SubnetId' \
    --output text)

SUBNET2_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block $SUBNET2_CIDR \
    --availability-zone ${REGION}b \
    --tag-specifications "ResourceType=subnet,Tags=[{Key=Name,Value=$PROJECT_NAME-subnet-2}]" \
    --query 'Subnet.SubnetId' \
    --output text)
echo "✅ Subnets created: $SUBNET1_ID, $SUBNET2_ID"

# 4. Create and configure route table
echo "🛣️  Configuring route table..."
ROUTE_TABLE_ID=$(aws ec2 create-route-table \
    --vpc-id $VPC_ID \
    --tag-specifications "ResourceType=route-table,Tags=[{Key=Name,Value=$PROJECT_NAME-rt}]" \
    --query 'RouteTable.RouteTableId' \
    --output text)

aws ec2 create-route --route-table-id $ROUTE_TABLE_ID --destination-cidr-block 0.0.0.0/0 --gateway-id $IGW_ID
aws ec2 associate-route-table --subnet-id $SUBNET1_ID --route-table-id $ROUTE_TABLE_ID
aws ec2 associate-route-table --subnet-id $SUBNET2_ID --route-table-id $ROUTE_TABLE_ID
echo "✅ Route table configured: $ROUTE_TABLE_ID"

# 5. Create Security Groups
echo "🔒 Creating security groups..."
# Backend Security Group
BACKEND_SG_ID=$(aws ec2 create-security-group \
    --group-name "$PROJECT_NAME-backend-sg" \
    --description "Security group for Triage Backend" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

# Add ingress rules
aws ec2 authorize-security-group-ingress --group-id $BACKEND_SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $BACKEND_SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $BACKEND_SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $BACKEND_SG_ID --protocol tcp --port 8000 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $BACKEND_SG_ID --protocol tcp --port 3000 --cidr 0.0.0.0/0
echo "✅ Backend security group created: $BACKEND_SG_ID"

# Database Security Group
DB_SG_ID=$(aws ec2 create-security-group \
    --group-name "$PROJECT_NAME-db-sg" \
    --description "Security group for Triage Database" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text)

aws ec2 authorize-security-group-ingress --group-id $DB_SG_ID --protocol tcp --port 5432 --source-group $BACKEND_SG_ID
echo "✅ Database security group created: $DB_SG_ID"

# 6. Create DB Subnet Group
echo "🗄️  Creating DB subnet group..."
aws rds create-db-subnet-group \
    --db-subnet-group-name "$PROJECT_NAME-db-subnet" \
    --db-subnet-group-description "Subnet group for Triage DB" \
    --subnet-ids $SUBNET1_ID $SUBNET2_ID \
    --tags "Key=Name,Value=$PROJECT_NAME-db-subnet"
echo "✅ DB subnet group created"

# 7. Create RDS PostgreSQL Instance
echo "💾 Creating RDS PostgreSQL instance (this may take several minutes)..."
DB_PASSWORD=$(openssl rand -base64 16 | tr -d "=+/" | cut -c1-16)
aws rds create-db-instance \
    --db-instance-identifier "$PROJECT_NAME-db" \
    --db-instance-class $DB_INSTANCE_CLASS \
    --engine postgres \
    --engine-version 16.1 \
    --master-username postgres \
    --master-user-password "$DB_PASSWORD" \
    --allocated-storage 20 \
    --vpc-security-group-ids $DB_SG_ID \
    --db-subnet-group-name "$PROJECT_NAME-db-subnet" \
    --backup-retention-period 7 \
    --publicly-accessible false \
    --storage-encrypted \
    --tags "Key=Name,Value=$PROJECT_NAME-db" \
    --no-cli-pager

echo "⏳ Waiting for RDS instance to be available..."
aws rds wait db-instance-available --db-instance-identifier "$PROJECT_NAME-db"

RDS_ENDPOINT=$(aws rds describe-db-instances \
    --db-instance-identifier "$PROJECT_NAME-db" \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text)
echo "✅ RDS instance created: $RDS_ENDPOINT"

# 8. Create S3 Bucket
echo "📦 Creating S3 bucket..."
TIMESTAMP=$(date +%s)
S3_BUCKET="${S3_BUCKET_PREFIX}-${TIMESTAMP}"
aws s3api create-bucket \
    --bucket $S3_BUCKET \
    --region $REGION \
    $(if [ "$REGION" != "us-east-1" ]; then echo "--create-bucket-configuration LocationConstraint=$REGION"; fi)

# Enable versioning
aws s3api put-bucket-versioning \
    --bucket $S3_BUCKET \
    --versioning-configuration Status=Enabled

# Set lifecycle policy (optional)
cat > /tmp/lifecycle.json << EOF
{
  "Rules": [
    {
      "Id": "DeleteOldVersions",
      "Status": "Enabled",
      "NoncurrentVersionExpiration": {
        "NoncurrentDays": 30
      }
    }
  ]
}
EOF
aws s3api put-bucket-lifecycle-configuration \
    --bucket $S3_BUCKET \
    --lifecycle-configuration file:///tmp/lifecycle.json

echo "✅ S3 bucket created: $S3_BUCKET"

# 9. Create Key Pair
echo "🔑 Creating EC2 key pair..."
aws ec2 create-key-pair \
    --key-name "$PROJECT_NAME-key" \
    --query 'KeyMaterial' \
    --output text > "$PROJECT_NAME-key.pem"
chmod 400 "$PROJECT_NAME-key.pem"
echo "✅ Key pair created: $PROJECT_NAME-key.pem"

# 10. Get latest Ubuntu AMI
echo "🖼️  Finding latest Ubuntu 22.04 AMI..."
AMI_ID=$(aws ec2 describe-images \
    --owners 099720109477 \
    --filters "Name=name,Values=ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*" \
    --query 'sort_by(Images, &CreationDate)[-1].ImageId' \
    --output text)
echo "✅ Using AMI: $AMI_ID"

# 11. Launch EC2 Instance
echo "🚀 Launching EC2 instance..."
EC2_INSTANCE_ID=$(aws ec2 run-instances \
    --image-id $AMI_ID \
    --instance-type $EC2_INSTANCE_TYPE \
    --key-name "$PROJECT_NAME-key" \
    --security-group-ids $BACKEND_SG_ID \
    --subnet-id $SUBNET1_ID \
    --associate-public-ip-address \
    --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$PROJECT_NAME-backend}]" \
    --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":30}}]' \
    --query 'Instances[0].InstanceId' \
    --output text)

echo "⏳ Waiting for EC2 instance to be running..."
aws ec2 wait instance-running --instance-ids $EC2_INSTANCE_ID

EC2_PUBLIC_IP=$(aws ec2 describe-instances \
    --instance-ids $EC2_INSTANCE_ID \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)
echo "✅ EC2 instance created: $EC2_PUBLIC_IP"

# 12. Save configuration
echo ""
echo "📝 Saving configuration..."
cat > infra-config.sh << EOF
# AWS Infrastructure Configuration
export AWS_REGION="$REGION"
export VPC_ID="$VPC_ID"
export SUBNET1_ID="$SUBNET1_ID"
export SUBNET2_ID="$SUBNET2_ID"
export BACKEND_SG_ID="$BACKEND_SG_ID"
export DB_SG_ID="$DB_SG_ID"
export RDS_ENDPOINT="$RDS_ENDPOINT"
export RDS_PASSWORD="$DB_PASSWORD"
export S3_BUCKET="$S3_BUCKET"
export EC2_INSTANCE_ID="$EC2_INSTANCE_ID"
export EC2_PUBLIC_IP="$EC2_PUBLIC_IP"
EOF

echo "✅ Configuration saved to infra-config.sh"

# Summary
echo ""
echo "🎉 Infrastructure Setup Complete!"
echo "=================================="
echo ""
echo "📊 Summary:"
echo "  VPC ID: $VPC_ID"
echo "  Subnets: $SUBNET1_ID, $SUBNET2_ID"
echo "  RDS Endpoint: $RDS_ENDPOINT"
echo "  RDS Password: $DB_PASSWORD"
echo "  S3 Bucket: $S3_BUCKET"
echo "  EC2 Instance: $EC2_INSTANCE_ID"
echo "  EC2 Public IP: $EC2_PUBLIC_IP"
echo "  SSH Key: $PROJECT_NAME-key.pem"
echo ""
echo "🔐 Database Connection String:"
echo "  postgresql://postgres:$DB_PASSWORD@$RDS_ENDPOINT:5432/triage"
echo ""
echo "🔑 SSH to EC2:"
echo "  ssh -i $PROJECT_NAME-key.pem ubuntu@$EC2_PUBLIC_IP"
echo ""
echo "📋 Next Steps:"
echo "  1. SSH to EC2 instance"
echo "  2. Install Docker and Docker Compose"
echo "  3. Clone the repository"
echo "  4. Configure .env file with the above credentials"
echo "  5. Run: docker-compose up -d"
echo ""
echo "💾 Configuration saved to: infra-config.sh"
echo "   Source this file to load environment variables:"
echo "   source infra-config.sh"
echo ""
