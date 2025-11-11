#!/bin/bash
# EC2 Instance Setup Script
# Run this script on your EC2 instance after provisioning

set -e

echo "🛠️  Setting up EC2 instance for AI Ticket Triage System"
echo "========================================================"

# Update system
echo "📦 Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
rm get-docker.sh

# Install Docker Compose
echo "📦 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Git
echo "📦 Installing Git..."
sudo apt-get install -y git

# Install other utilities
echo "📦 Installing utilities..."
sudo apt-get install -y htop curl wget vim unzip

# Install AWS CLI
echo "☁️  Installing AWS CLI..."
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install
rm -rf aws awscliv2.zip

# Create application directory
echo "📁 Creating application directory..."
mkdir -p ~/support-ticket-triage-system

# Configure firewall
echo "🔥 Configuring firewall..."
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 3000/tcp
sudo ufw --force enable

# Set up log rotation
echo "📋 Setting up log rotation..."
sudo tee /etc/logrotate.d/docker-containers > /dev/null << EOF
/var/lib/docker/containers/*/*.log {
    rotate 7
    daily
    compress
    size=10M
    missingok
    delaycompress
    copytruncate
}
EOF

# Create swap file (for t3.medium instances)
echo "💾 Creating swap file..."
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab

# Configure Docker daemon
echo "⚙️  Configuring Docker daemon..."
sudo tee /etc/docker/daemon.json > /dev/null << EOF
{
  "log-driver": "json-file",
  "log-opts": {
    "max-size": "10m",
    "max-file": "3"
  }
}
EOF

sudo systemctl restart docker

# Install PostgreSQL client (for debugging)
echo "🗄️  Installing PostgreSQL client..."
sudo apt-get install -y postgresql-client

# Set up automatic security updates
echo "🔒 Setting up automatic security updates..."
sudo apt-get install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades

# Create systemd service for auto-start
echo "🔄 Creating systemd service..."
sudo tee /etc/systemd/system/triage.service > /dev/null << EOF
[Unit]
Description=AI Ticket Triage System
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/support-ticket-triage-system
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
User=ubuntu

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable triage.service

echo ""
echo "✅ EC2 instance setup complete!"
echo ""
echo "📋 Next Steps:"
echo "  1. Clone your repository:"
echo "     git clone https://github.com/DavidFragoso18/support-ticket-triage-system.git"
echo "     cd support-ticket-triage-system"
echo ""
echo "  2. Create .env file with your configuration"
echo ""
echo "  3. Start the application:"
echo "     docker-compose up -d"
echo ""
echo "  4. Check logs:"
echo "     docker-compose logs -f"
echo ""
echo "⚠️  IMPORTANT: Logout and login again for Docker group changes to take effect!"
echo ""
