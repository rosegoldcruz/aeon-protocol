#!/bin/bash

# AEON Platform Production Droplet Setup Script
# Domain: api.aeonprotocol.com
# This script configures the production backend infrastructure

set -e

echo "🚀 AEON Platform Production Deployment Starting..."
echo "Domain: api.aeonprotocol.com"
echo "Setting up production backend infrastructure..."

# Update system packages
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install essential packages
echo "🔧 Installing essential packages..."
sudo apt install -y \
    curl \
    wget \
    git \
    nginx \
    certbot \
    python3-certbot-nginx \
    docker.io \
    docker-compose \
    postgresql \
    postgresql-contrib \
    redis-server \
    ufw \
    htop \
    vim \
    unzip

# Install Node.js 18+
echo "📦 Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Install Python 3.11+
echo "🐍 Installing Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3-pip

# Start and enable services
echo "🔄 Starting services..."
sudo systemctl start docker
sudo systemctl enable docker
sudo systemctl start postgresql
sudo systemctl enable postgresql
sudo systemctl start redis-server
sudo systemctl enable redis-server
sudo systemctl start nginx
sudo systemctl enable nginx

# Configure firewall
echo "🔒 Configuring firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 8000  # FastAPI backend
sudo ufw --force enable

# Create application directory
echo "📁 Creating application directories..."
sudo mkdir -p /opt/aeon
sudo chown $USER:$USER /opt/aeon
cd /opt/aeon

# Clone the repository (assuming it's accessible)
echo "📥 Setting up application code..."
# Note: In production, you would clone from your repository
# git clone https://github.com/your-org/aeon-protocol.git .

# Create directory structure for now
mkdir -p services/api
mkdir -p services/worker
mkdir -p logs
mkdir -p data

# Set up Python virtual environment
echo "🐍 Setting up Python environment..."
python3.11 -m venv venv
source venv/bin/activate

# Install Python dependencies (placeholder - would be from requirements.txt)
pip install --upgrade pip
pip install \
    fastapi \
    uvicorn \
    sqlalchemy \
    asyncpg \
    redis \
    celery \
    openai \
    replicate \
    requests \
    python-multipart \
    python-jose \
    passlib \
    bcrypt \
    aiofiles \
    boto3

# Configure PostgreSQL
echo "🗄️ Configuring PostgreSQL..."
sudo -u postgres createdb aeon_production || echo "Database already exists"
sudo -u postgres psql -c "CREATE USER aeon WITH PASSWORD 'secure_password_change_me';" || echo "User already exists"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE aeon_production TO aeon;" || echo "Privileges already granted"

# Configure Redis
echo "📊 Configuring Redis..."
sudo sed -i 's/# maxmemory <bytes>/maxmemory 256mb/' /etc/redis/redis.conf
sudo sed -i 's/# maxmemory-policy noeviction/maxmemory-policy allkeys-lru/' /etc/redis/redis.conf
sudo systemctl restart redis-server

# Create environment file
echo "⚙️ Creating environment configuration..."
cat > /opt/aeon/.env << EOF
# AEON Platform Production Environment
NODE_ENV=production
ENVIRONMENT=production

# Database Configuration
DATABASE_URL=postgresql://aeon:secure_password_change_me@localhost:5432/aeon_production
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=aeon_production
POSTGRES_USER=aeon
POSTGRES_PASSWORD=secure_password_change_me

# Redis Configuration
REDIS_URL=redis://localhost:6379/0
REDIS_HOST=localhost
REDIS_PORT=6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=4

# Security
JWT_SECRET_KEY=your_jwt_secret_key_change_me
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI Service API Keys (TO BE CONFIGURED)
OPENAI_API_KEY=your_openai_api_key_here
REPLICATE_API_TOKEN=your_replicate_token_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here
RUNWAY_API_KEY=your_runway_key_here
PIKA_API_KEY=your_pika_key_here
LUMA_API_KEY=your_luma_key_here
HAILUO_API_KEY=your_hailuo_key_here

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
S3_BUCKET=aeon-media-production

# CORS Configuration
ALLOWED_ORIGINS=https://aeoninvestmentstechnologies.com,https://www.aeoninvestmentstechnologies.com
FRONTEND_URL=https://aeoninvestmentstechnologies.com

# Backend Configuration
BACKEND_DOMAIN=api.aeonprotocol.com
BACKEND_PORT=443
USE_HTTPS=true

# Monitoring
LOG_LEVEL=INFO
SENTRY_DSN=your_sentry_dsn_here
EOF

# Create systemd service for FastAPI backend
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/aeon-api.service > /dev/null << EOF
[Unit]
Description=AEON Platform FastAPI Backend
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/aeon
Environment=PATH=/opt/aeon/venv/bin
EnvironmentFile=/opt/aeon/.env
ExecStart=/opt/aeon/venv/bin/uvicorn services.api.main:app --host 0.0.0.0 --port 8000 --workers 4
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Create systemd service for Celery worker
sudo tee /etc/systemd/system/aeon-worker.service > /dev/null << EOF
[Unit]
Description=AEON Platform Celery Worker
After=network.target postgresql.service redis.service

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/aeon
Environment=PATH=/opt/aeon/venv/bin
EnvironmentFile=/opt/aeon/.env
ExecStart=/opt/aeon/venv/bin/celery -A services.worker.worker worker --loglevel=info
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Configure Nginx
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/sites-available/aeon > /dev/null << EOF
server {
    listen 80;
    server_name api.aeonprotocol.com;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;

    # CORS headers for API
    location /api/ {
        if (\$request_method = 'OPTIONS') {
            add_header 'Access-Control-Allow-Origin' '*';
            add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE';
            add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization';
            add_header 'Access-Control-Max-Age' 1728000;
            add_header 'Content-Type' 'text/plain; charset=utf-8';
            add_header 'Content-Length' 0;
            return 204;
        }

        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, OPTIONS, PUT, DELETE' always;
        add_header 'Access-Control-Allow-Headers' 'DNT,User-Agent,X-Requested-With,If-Modified-Since,Cache-Control,Content-Type,Range,Authorization' always;

        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        
        # WebSocket support
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    # Default response for non-API requests
    location / {
        return 200 'AEON Platform Backend - API available at /api/';
        add_header Content-Type text/plain;
    }
}
EOF

# Enable the site
sudo ln -sf /etc/nginx/sites-available/aeon /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl reload nginx

# Create log directories
echo "📝 Setting up logging..."
sudo mkdir -p /var/log/aeon
sudo chown $USER:$USER /var/log/aeon

# Set up log rotation
sudo tee /etc/logrotate.d/aeon > /dev/null << EOF
/var/log/aeon/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $USER $USER
}
EOF

echo "✅ Basic infrastructure setup complete!"
echo ""
echo "🔧 NEXT STEPS:"
echo "1. Update environment variables in /opt/aeon/.env with your actual API keys"
echo "2. Deploy your application code to /opt/aeon/"
echo "3. Run database migrations"
echo "4. Start the services:"
echo "   sudo systemctl start aeon-api"
echo "   sudo systemctl start aeon-worker"
echo "   sudo systemctl enable aeon-api"
echo "   sudo systemctl enable aeon-worker"
echo ""
echo "🌐 Your backend will be available at:"
echo "   HTTPS: https://api.aeonprotocol.com/"
echo "   Health Check: https://api.aeonprotocol.com/health"
echo ""
echo "🔒 SECURITY REMINDERS:"
echo "- Change all default passwords in /opt/aeon/.env"
echo "- Set up SSL certificates with: sudo certbot --nginx -d api.aeonprotocol.com"
echo "- Configure proper firewall rules"
echo "- Set up monitoring and backups"
echo ""
echo "🚀 AEON Platform infrastructure is ready for deployment!"
