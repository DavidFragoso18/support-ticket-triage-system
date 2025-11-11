# Infrastructure Configuration

This directory contains scripts and configuration files for deploying the AI Ticket Triage System to AWS.

## 📁 Files

- **setup-aws.sh**: Automated AWS infrastructure provisioning script
- **setup-ec2.sh**: EC2 instance configuration script (run on EC2)
- **cleanup-aws.sh**: Script to tear down all AWS resources
- **nginx.conf**: Nginx reverse proxy configuration with SSL
- **cloudwatch-config.json**: CloudWatch agent configuration for monitoring
- **terraform/**: Terraform infrastructure-as-code (optional alternative to shell scripts)

## 🚀 Quick Start

### Option 1: Automated Setup (Shell Scripts)

1. **Configure AWS CLI**:
   ```bash
   aws configure
   # Enter your AWS Access Key ID, Secret Access Key, and region
   ```

2. **Run infrastructure setup**:
   ```bash
   cd infra
   chmod +x setup-aws.sh
   ./setup-aws.sh
   ```

3. **SSH to EC2 instance**:
   ```bash
   ssh -i triage-key.pem ubuntu@<EC2_PUBLIC_IP>
   ```

4. **Setup EC2 instance**:
   ```bash
   # On EC2 instance
   wget https://raw.githubusercontent.com/DavidFragoso18/support-ticket-triage-system/main/infra/setup-ec2.sh
   chmod +x setup-ec2.sh
   ./setup-ec2.sh
   
   # Logout and login again
   exit
   ssh -i triage-key.pem ubuntu@<EC2_PUBLIC_IP>
   ```

5. **Deploy application**:
   ```bash
   git clone https://github.com/DavidFragoso18/support-ticket-triage-system.git
   cd support-ticket-triage-system
   
   # Create .env file
   cp .env.docker .env
   # Edit .env with your RDS endpoint, passwords, etc.
   
   docker-compose up -d
   ```

### Option 2: Manual Setup

Follow the detailed guide in [../docs/aws-deployment.md](../docs/aws-deployment.md)

### Option 3: Terraform (Coming Soon)

```bash
cd infra/terraform
terraform init
terraform plan
terraform apply
```

## 🗑️ Cleanup

To delete all AWS resources:

```bash
cd infra
chmod +x cleanup-aws.sh
./cleanup-aws.sh
```

**⚠️ WARNING**: This will permanently delete all resources including databases and backups!

## 📊 Cost Optimization Tips

1. **Use Spot Instances**: For dev/test, use EC2 spot instances to save up to 90%
2. **Right-size resources**: Start with t3.micro and scale up as needed
3. **Enable S3 lifecycle policies**: Automatically delete old files
4. **Use RDS reserved instances**: Save up to 60% for production
5. **Enable CloudWatch alarms**: Monitor costs and set billing alerts

## 🔐 Security Best Practices

1. **Never commit credentials**: Use AWS Secrets Manager or Parameter Store
2. **Enable MFA**: For AWS root and IAM users
3. **Use IAM roles**: Instead of access keys on EC2
4. **Enable VPC Flow Logs**: For network monitoring
5. **Regular updates**: Keep all systems patched
6. **Encrypt everything**: Enable encryption at rest and in transit

## 📚 Additional Resources

- [AWS Well-Architected Framework](https://aws.amazon.com/architecture/well-architected/)
- [AWS Cost Optimization](https://aws.amazon.com/pricing/cost-optimization/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)

## 🆘 Troubleshooting

### Script fails with "AccessDenied"
Ensure your IAM user has the required permissions (EC2, RDS, S3, VPC).

### EC2 instance can't connect to RDS
Check security group rules - ensure backend SG is allowed in DB SG.

### Out of disk space
Increase EBS volume size or clean up Docker:
```bash
docker system prune -af
```

### High costs
Check CloudWatch billing dashboard and set up cost alerts.

## 📞 Support

For issues or questions, please open an issue on GitHub.
