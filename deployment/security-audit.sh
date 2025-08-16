#!/bin/bash

# AEON Platform Security Audit Script
# Verifies that no IP addresses are hardcoded in the codebase
# Ensures all communication uses domain names

set -e

echo "🔒 AEON Platform Security Audit"
echo "==============================="
echo "Checking for hardcoded IP addresses and security issues..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

ISSUES_FOUND=0

# Function to report issues
report_issue() {
    echo -e "${RED}❌ ISSUE:${NC} $1"
    ISSUES_FOUND=$((ISSUES_FOUND + 1))
}

# Function to report warnings
report_warning() {
    echo -e "${YELLOW}⚠️  WARNING:${NC} $1"
}

# Function to report success
report_success() {
    echo -e "${GREEN}✅ PASS:${NC} $1"
}

# Function to report info
report_info() {
    echo -e "${BLUE}ℹ️  INFO:${NC} $1"
}

# Check 1: Search for IP address patterns in all files
echo "🔍 Checking for hardcoded IP addresses..."
IP_PATTERN='[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}'

# Exclude certain directories and file types
EXCLUDE_DIRS="node_modules|\.git|\.next|build|dist|coverage|logs|\.venv|venv|__pycache__"
EXCLUDE_FILES="\.log$|\.png$|\.jpg$|\.jpeg$|\.gif$|\.svg$|\.ico$|\.woff$|\.woff2$|\.ttf$|\.eot$"

# Search for IP addresses
IP_MATCHES=$(find . -type f \
    ! -path "*/$EXCLUDE_DIRS/*" \
    ! -name "security-audit.sh" \
    ! -regex ".*($EXCLUDE_FILES)" \
    -exec grep -l -E "$IP_PATTERN" {} \; 2>/dev/null || true)

if [ -n "$IP_MATCHES" ]; then
    report_issue "Found files containing IP addresses:"
    echo "$IP_MATCHES" | while read -r file; do
        echo "  📄 $file"
        grep -n -E "$IP_PATTERN" "$file" | head -5 | sed 's/^/    /'
        echo ""
    done
else
    report_success "No hardcoded IP addresses found in codebase"
fi

# Check 2: Verify API configuration uses domain names
echo ""
echo "🌐 Checking API configuration..."

if [ -f "apps/web/lib/api-config.ts" ]; then
    if grep -q "api.aeonprotocol.com" "apps/web/lib/api-config.ts"; then
        report_success "Frontend API configuration uses domain name"
    else
        report_issue "Frontend API configuration does not use api.aeonprotocol.com"
    fi
    
    if grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" "apps/web/lib/api-config.ts"; then
        report_issue "Frontend API configuration contains IP addresses"
    else
        report_success "Frontend API configuration contains no IP addresses"
    fi
else
    report_warning "Frontend API configuration file not found"
fi

# Check 3: Verify CORS configuration uses domain names only
echo ""
echo "🔒 Checking CORS configuration..."

if [ -f "services/api/app/main.py" ]; then
    if grep -q "aeoninvestmentstechnologies.com" "services/api/app/main.py"; then
        report_success "Backend CORS uses production domain names"
    else
        report_warning "Backend CORS may not include production domains"
    fi
    
    # Check for IP addresses in CORS (excluding localhost)
    if grep -E "allow_origins.*[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" "services/api/app/main.py" | grep -v "127.0.0.1" | grep -v "0.0.0.0"; then
        report_issue "Backend CORS configuration contains non-localhost IP addresses"
    else
        report_success "Backend CORS configuration uses domain names only"
    fi
else
    report_warning "Backend main.py file not found"
fi

# Check 4: Verify deployment configurations
echo ""
echo "🚀 Checking deployment configurations..."

# Check nginx configuration
if [ -f "deployment/nginx.conf" ]; then
    if grep -q "api.aeonprotocol.com" "deployment/nginx.conf"; then
        report_success "Nginx configuration uses domain name"
    else
        report_issue "Nginx configuration does not use api.aeonprotocol.com"
    fi
else
    report_warning "Nginx configuration file not found"
fi

# Check deployment scripts
if [ -f "deployment/droplet-setup.sh" ]; then
    if grep -q "api.aeonprotocol.com" "deployment/droplet-setup.sh"; then
        report_success "Deployment script uses domain name"
    else
        report_issue "Deployment script does not use api.aeonprotocol.com"
    fi
else
    report_warning "Deployment setup script not found"
fi

# Check 5: Verify environment templates
echo ""
echo "⚙️ Checking environment configuration..."

if [ -f ".env.example" ]; then
    if grep -q "api.aeonprotocol.com" ".env.example"; then
        report_success "Environment template uses domain name"
    else
        report_warning "Environment template may not include domain configuration"
    fi
    
    # Check for non-localhost IP addresses in env template
    if grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" ".env.example" | grep -v "localhost" | grep -v "127.0.0.1" | grep -v "0.0.0.0"; then
        report_issue "Environment template contains non-localhost IP addresses"
    else
        report_success "Environment template uses appropriate addresses"
    fi
else
    report_warning "Environment template file not found"
fi

# Check 6: Verify documentation
echo ""
echo "📚 Checking documentation..."

DOC_FILES=$(find . -name "*.md" -type f ! -path "./node_modules/*" ! -path "./.git/*")
DOC_IP_MATCHES=""

for doc in $DOC_FILES; do
    if grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" "$doc" | grep -v "localhost" | grep -v "127.0.0.1" | grep -v "0.0.0.0" >/dev/null 2>&1; then
        DOC_IP_MATCHES="$DOC_IP_MATCHES $doc"
    fi
done

if [ -n "$DOC_IP_MATCHES" ]; then
    report_warning "Documentation files may contain IP addresses:"
    for doc in $DOC_IP_MATCHES; do
        echo "  📄 $doc"
    done
else
    report_success "Documentation uses domain names appropriately"
fi

# Check 7: Verify Docker configurations
echo ""
echo "🐳 Checking Docker configurations..."

DOCKER_FILES=$(find . -name "docker-compose*.yml" -o -name "Dockerfile*" ! -path "./node_modules/*" ! -path "./.git/*")

for docker_file in $DOCKER_FILES; do
    if [ -f "$docker_file" ]; then
        # Check for non-localhost IP addresses
        if grep -E "[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}" "$docker_file" | grep -v "localhost" | grep -v "127.0.0.1" | grep -v "0.0.0.0" >/dev/null 2>&1; then
            report_warning "Docker file $docker_file may contain IP addresses"
        fi
    fi
done

report_success "Docker configuration check completed"

# Summary
echo ""
echo "📊 Security Audit Summary"
echo "========================="

if [ $ISSUES_FOUND -eq 0 ]; then
    echo -e "${GREEN}🎉 SECURITY AUDIT PASSED!${NC}"
    echo "✅ No hardcoded IP addresses found"
    echo "✅ All configurations use domain names"
    echo "✅ CORS properly configured"
    echo "✅ Deployment scripts use domains"
    echo ""
    echo "🔒 Security Recommendations:"
    echo "• Ensure DNS A record: api.aeonprotocol.com → your_server_ip"
    echo "• Configure SSL certificate for api.aeonprotocol.com"
    echo "• Set up proper firewall rules"
    echo "• Use environment variables for all configuration"
    echo "• Regularly audit for new IP address references"
    echo ""
    exit 0
else
    echo -e "${RED}⚠️  SECURITY AUDIT FAILED${NC}"
    echo "Found $ISSUES_FOUND security issues that need to be addressed."
    echo ""
    echo "🔧 Required Actions:"
    echo "• Remove all hardcoded IP addresses from the codebase"
    echo "• Update configurations to use domain names only"
    echo "• Verify CORS settings use proper domains"
    echo "• Update deployment scripts and documentation"
    echo ""
    exit 1
fi
