# AEON Platform Production Deployment Guide

## 🚀 Quick Deployment to DigitalOcean Droplet (147.182.231.0)

### Prerequisites
- DigitalOcean droplet with Ubuntu 22.04 LTS
- Root or sudo access to the droplet
- Domain name (optional, for SSL)

### Step 1: Initial Server Setup

```bash
# SSH into your droplet
ssh root@147.182.231.0

# Run the automated setup script
curl -fsSL https://raw.githubusercontent.com/your-org/aeon-protocol/main/deployment/droplet-setup.sh | bash

# Or manually upload and run the script
scp deployment/droplet-setup.sh root@147.182.231.0:/tmp/
ssh root@147.182.231.0 "chmod +x /tmp/droplet-setup.sh && /tmp/droplet-setup.sh"
```

### Step 2: Deploy Application Code

```bash
# On your local machine, prepare the deployment
cd /path/to/aeon-protocol

# Create deployment package
tar -czf aeon-deployment.tar.gz \
  services/ \
  deployment/ \
  requirements.txt \
  --exclude="*.pyc" \
  --exclude="__pycache__" \
  --exclude=".git"

# Upload to droplet (replace with your actual server)
scp aeon-deployment.tar.gz root@your-server-ip:/opt/aeon/

# SSH into droplet and extract (replace with your actual server)
ssh root@your-server-ip
cd /opt/aeon
tar -xzf aeon-deployment.tar.gz
rm aeon-deployment.tar.gz
```

### Step 3: Configure Environment Variables

```bash
# Copy and edit the environment file
cp deployment/.env.production.example .env.production

# Edit with your actual API keys and configuration
nano .env.production

# CRITICAL: Update these values:
# - POSTGRES_PASSWORD (secure password)
# - JWT_SECRET_KEY (secure random string)
# - OPENAI_API_KEY (your OpenAI API key)
# - REPLICATE_API_TOKEN (your Replicate token)
# - AWS credentials for S3 storage
# - Other AI service API keys as needed
```

### Step 4: Start Services

```bash
# Activate Python virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Start and enable services
sudo systemctl start aeon-api
sudo systemctl start aeon-worker
sudo systemctl enable aeon-api
sudo systemctl enable aeon-worker

# Check service status
sudo systemctl status aeon-api
sudo systemctl status aeon-worker
```

### Step 5: Verify Deployment

```bash
# Test API health endpoint
curl https://api.aeonprotocol.com/health

# Test API documentation
curl https://api.aeonprotocol.com/docs

# Check logs
sudo journalctl -u aeon-api -f
sudo journalctl -u aeon-worker -f
```

## 🐳 Alternative: Docker Deployment

### Using Docker Compose

```bash
# On the droplet
cd /opt/aeon

# Copy environment file
cp deployment/.env.production.example deployment/.env.production
# Edit deployment/.env.production with your values

# Start all services
docker-compose -f deployment/docker-compose.production.yml up -d

# Check status
docker-compose -f deployment/docker-compose.production.yml ps

# View logs
docker-compose -f deployment/docker-compose.production.yml logs -f
```

## 🌐 Frontend Configuration

### Update Vercel Environment Variables

In your Vercel project settings, add/update these environment variables:

**Production Environment:**
```
NEXT_PUBLIC_API_URL=https://api.aeonprotocol.com
REPLICATE_API_TOKEN=your_replicate_token_here
REPLICATE_HAILUO_VERSION_ID=d615361988ffcbadecfe52b95dd9302a8d6e1069c908a05104f36b651aea6c95
```

**Preview Environment:**
```
NEXT_PUBLIC_API_URL=https://api.aeonprotocol.com
REPLICATE_API_TOKEN=your_replicate_token_here
REPLICATE_HAILUO_VERSION_ID=d615361988ffcbadecfe52b95dd9302a8d6e1069c908a05104f36b651aea6c95
```

**Development Environment:**
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
REPLICATE_API_TOKEN=your_replicate_token_here
REPLICATE_HAILUO_VERSION_ID=d615361988ffcbadecfe52b95dd9302a8d6e1069c908a05104f36b651aea6c95
```

### Deploy Frontend

```bash
# Trigger Vercel deployment
vercel --prod

# Or push to main branch if auto-deployment is configured
git add .
git commit -m "Configure production backend endpoint"
git push origin main
```

## 🔒 SSL Configuration (Recommended)

### Using Let's Encrypt with Certbot

```bash
# Install certbot (if not already installed)
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate for API domain
sudo certbot --nginx -d api.aeonprotocol.com

# Test automatic renewal
sudo certbot renew --dry-run
```

### Update Nginx Configuration for SSL

The certbot will automatically update your Nginx configuration, but verify:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

## 📊 Monitoring Setup

### Access Monitoring Dashboards

- **Grafana**: https://api.aeonprotocol.com:3000 (admin/password from .env.production)
- **Prometheus**: https://api.aeonprotocol.com:9090

### Set Up Log Monitoring

```bash
# View real-time logs
sudo tail -f /var/log/aeon/*.log

# Set up log rotation (already configured by setup script)
sudo logrotate -d /etc/logrotate.d/aeon
```

## 🧪 Testing the Deployment

### API Testing

```bash
# Test video generation endpoint
curl -X POST https://api.aeonprotocol.com/video/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "a beautiful sunset over mountains", "duration": 6}'

# Test AI agent endpoints
curl -X POST https://api.aeonprotocol.com/agents/content/screenwriter \
  -H "Content-Type: application/json" \
  -d '{"task": "generate", "parameters": {"concept": "space adventure", "genre": "sci-fi"}}'
```

### Frontend Testing

1. Visit your Vercel deployment URL
2. Test video generation functionality
3. Verify AI agent interactions
4. Check workflow builder functionality

## 🔧 Troubleshooting

### Common Issues

**Service won't start:**
```bash
# Check logs
sudo journalctl -u aeon-api -n 50
sudo journalctl -u aeon-worker -n 50

# Check configuration
sudo systemctl status aeon-api
```

**Database connection issues:**
```bash
# Test PostgreSQL connection
sudo -u postgres psql -c "SELECT version();"

# Check database exists
sudo -u postgres psql -l | grep aeon
```

**Redis connection issues:**
```bash
# Test Redis
redis-cli ping

# Check Redis status
sudo systemctl status redis-server
```

### Performance Tuning

**For high traffic:**
```bash
# Increase API workers
sudo systemctl edit aeon-api
# Add: Environment="API_WORKERS=8"

# Scale Celery workers
sudo systemctl edit aeon-worker
# Add: Environment="CELERY_WORKERS=4"
```

## 🔄 Updates and Maintenance

### Updating the Application

```bash
# Pull latest code
cd /opt/aeon
git pull origin main

# Update dependencies
source venv/bin/activate
pip install -r requirements.txt

# Restart services
sudo systemctl restart aeon-api
sudo systemctl restart aeon-worker
```

### Database Backups

```bash
# Create backup script
sudo tee /opt/aeon/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/opt/aeon/backups"
mkdir -p $BACKUP_DIR
pg_dump -h localhost -U aeon aeon_production > $BACKUP_DIR/aeon_$(date +%Y%m%d_%H%M%S).sql
find $BACKUP_DIR -name "aeon_*.sql" -mtime +7 -delete
EOF

# Make executable and add to cron
chmod +x /opt/aeon/backup.sh
echo "0 2 * * * /opt/aeon/backup.sh" | sudo crontab -
```

## ✅ Success Validation Checklist

- [ ] Droplet accessible at 147.182.231.0
- [ ] API health check returns 200: `curl http://147.182.231.0/health`
- [ ] Video generation API works with Token authorization
- [ ] Frontend deployed to Vercel with correct API endpoint
- [ ] Environment variables set in all Vercel environments
- [ ] SSL certificate configured (if using domain)
- [ ] Monitoring dashboards accessible
- [ ] Database and Redis connections working
- [ ] All services running and enabled
- [ ] Log rotation configured
- [ ] Backup system in place

Your AEON Platform is now ready for production! 🚀
