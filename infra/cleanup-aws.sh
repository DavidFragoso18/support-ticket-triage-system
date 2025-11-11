#!/bin/bash
# Cleanup AWS Infrastructure
# WARNING: This will delete all created resources!

set -e

echo "⚠️  AWS Infrastructure Cleanup"
echo "=============================="
echo ""
echo "This will DELETE all AWS resources created by setup-aws.sh"
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Cleanup cancelled."
    exit 0
fi

# Load configuration
if [ ! -f "infra-config.sh" ]; then
    echo "❌ Configuration file not found. Please ensure infra-config.sh exists."
    exit 1
fi

source infra-config.sh

echo ""
echo "🗑️  Starting cleanup..."

# 1. Terminate EC2 Instance
if [ -n "$EC2_INSTANCE_ID" ]; then
    echo "🔴 Terminating EC2 instance..."
    aws ec2 terminate-instances --instance-ids $EC2_INSTANCE_ID
    aws ec2 wait instance-terminated --instance-ids $EC2_INSTANCE_ID
    echo "✅ EC2 instance terminated"
fi

# 2. Delete RDS Instance
if [ -n "$RDS_ENDPOINT" ]; then
    echo "🔴 Deleting RDS instance..."
    DB_ID=$(echo $RDS_ENDPOINT | cut -d'.' -f1)
    aws rds delete-db-instance \
        --db-instance-identifier $DB_ID \
        --skip-final-snapshot \
        --delete-automated-backups
    echo "⏳ Waiting for RDS instance to be deleted..."
    aws rds wait db-instance-deleted --db-instance-identifier $DB_ID
    echo "✅ RDS instance deleted"
fi

# 3. Delete DB Subnet Group
echo "🔴 Deleting DB subnet group..."
aws rds delete-db-subnet-group --db-subnet-group-name "triage-db-subnet" || true
echo "✅ DB subnet group deleted"

# 4. Empty and delete S3 bucket
if [ -n "$S3_BUCKET" ]; then
    echo "🔴 Emptying and deleting S3 bucket..."
    aws s3 rm s3://$S3_BUCKET --recursive
    aws s3api delete-bucket --bucket $S3_BUCKET
    echo "✅ S3 bucket deleted"
fi

# 5. Delete Security Groups
sleep 10  # Wait for dependencies to clear
if [ -n "$BACKEND_SG_ID" ]; then
    echo "🔴 Deleting backend security group..."
    aws ec2 delete-security-group --group-id $BACKEND_SG_ID || true
    echo "✅ Backend security group deleted"
fi

if [ -n "$DB_SG_ID" ]; then
    echo "🔴 Deleting database security group..."
    aws ec2 delete-security-group --group-id $DB_SG_ID || true
    echo "✅ Database security group deleted"
fi

# 6. Delete Key Pair
echo "🔴 Deleting key pair..."
aws ec2 delete-key-pair --key-name "triage-key"
rm -f triage-key.pem
echo "✅ Key pair deleted"

# 7. Detach and delete Internet Gateway
if [ -n "$IGW_ID" ] && [ -n "$VPC_ID" ]; then
    echo "🔴 Detaching and deleting Internet Gateway..."
    aws ec2 detach-internet-gateway --internet-gateway-id $IGW_ID --vpc-id $VPC_ID || true
    aws ec2 delete-internet-gateway --internet-gateway-id $IGW_ID || true
    echo "✅ Internet Gateway deleted"
fi

# 8. Delete Route Table
if [ -n "$VPC_ID" ]; then
    echo "🔴 Deleting route tables..."
    ROUTE_TABLES=$(aws ec2 describe-route-tables \
        --filters "Name=vpc-id,Values=$VPC_ID" "Name=association.main,Values=false" \
        --query 'RouteTables[*].RouteTableId' \
        --output text)
    
    for RT_ID in $ROUTE_TABLES; do
        # Disassociate subnets
        ASSOCIATIONS=$(aws ec2 describe-route-tables \
            --route-table-ids $RT_ID \
            --query 'RouteTables[0].Associations[?!Main].RouteTableAssociationId' \
            --output text)
        
        for ASSOC_ID in $ASSOCIATIONS; do
            aws ec2 disassociate-route-table --association-id $ASSOC_ID || true
        done
        
        aws ec2 delete-route-table --route-table-id $RT_ID || true
    done
    echo "✅ Route tables deleted"
fi

# 9. Delete Subnets
if [ -n "$SUBNET1_ID" ]; then
    echo "🔴 Deleting subnet 1..."
    aws ec2 delete-subnet --subnet-id $SUBNET1_ID || true
    echo "✅ Subnet 1 deleted"
fi

if [ -n "$SUBNET2_ID" ]; then
    echo "🔴 Deleting subnet 2..."
    aws ec2 delete-subnet --subnet-id $SUBNET2_ID || true
    echo "✅ Subnet 2 deleted"
fi

# 10. Delete VPC
if [ -n "$VPC_ID" ]; then
    echo "🔴 Deleting VPC..."
    aws ec2 delete-vpc --vpc-id $VPC_ID || true
    echo "✅ VPC deleted"
fi

# 11. Clean up local files
echo "🔴 Cleaning up local files..."
rm -f infra-config.sh
echo "✅ Local configuration files deleted"

echo ""
echo "🎉 Cleanup complete!"
echo ""
echo "All AWS resources have been deleted."
echo ""
