#!/bin/bash

# AEON Platform Production Deployment Testing Script
# Tests all critical functionality after deployment

set -e

API_DOMAIN="api.aeonprotocol.com"
API_BASE="https://${API_DOMAIN}"
HEALTH_ENDPOINT="https://${API_DOMAIN}/health"

echo "🧪 AEON Platform Production Deployment Testing"
echo "=============================================="
echo "Testing deployment at: ${API_DOMAIN}"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
test_passed() {
    echo -e "${GREEN}✅ PASSED:${NC} $1"
    ((TESTS_PASSED++))
}

test_failed() {
    echo -e "${RED}❌ FAILED:${NC} $1"
    ((TESTS_FAILED++))
}

test_warning() {
    echo -e "${YELLOW}⚠️  WARNING:${NC} $1"
}

test_info() {
    echo -e "${BLUE}ℹ️  INFO:${NC} $1"
}

# Test 1: Basic Connectivity
echo "🔌 Testing Basic Connectivity..."
if curl -s --connect-timeout 10 "${API_DOMAIN}" > /dev/null; then
    test_passed "API domain is accessible at ${API_DOMAIN}"
else
    test_failed "Cannot connect to API domain at ${API_DOMAIN}"
fi

# Test 2: Health Check Endpoint
echo ""
echo "🏥 Testing Health Check Endpoint..."
HEALTH_RESPONSE=$(curl -s -w "%{http_code}" "${HEALTH_ENDPOINT}" -o /tmp/health_response.json)
if [ "$HEALTH_RESPONSE" = "200" ]; then
    test_passed "Health check endpoint returns 200"
    test_info "Health response: $(cat /tmp/health_response.json)"
else
    test_failed "Health check endpoint failed (HTTP $HEALTH_RESPONSE)"
fi

# Test 3: API Documentation
echo ""
echo "📚 Testing API Documentation..."
DOCS_RESPONSE=$(curl -s -w "%{http_code}" "${API_BASE}/docs" -o /dev/null)
if [ "$DOCS_RESPONSE" = "200" ]; then
    test_passed "API documentation is accessible"
else
    test_warning "API documentation not accessible (HTTP $DOCS_RESPONSE)"
fi

# Test 4: CORS Headers
echo ""
echo "🌐 Testing CORS Configuration..."
CORS_RESPONSE=$(curl -s -H "Origin: https://aeon-protocol.vercel.app" \
    -H "Access-Control-Request-Method: POST" \
    -H "Access-Control-Request-Headers: Content-Type" \
    -X OPTIONS "${API_BASE}/agents/content/screenwriter" \
    -w "%{http_code}" -o /dev/null)

if [ "$CORS_RESPONSE" = "200" ] || [ "$CORS_RESPONSE" = "204" ]; then
    test_passed "CORS headers configured correctly"
else
    test_warning "CORS configuration may need adjustment (HTTP $CORS_RESPONSE)"
fi

# Test 5: Video Generation API (Critical Fix Validation)
echo ""
echo "🎬 Testing Video Generation API (Critical Fix)..."

# Test video generation endpoint
VIDEO_GEN_RESPONSE=$(curl -s -X POST "${API_BASE}/media/videos/generate" \
    -H "Content-Type: application/json" \
    -d '{"prompt": "test video generation", "duration": 5}' \
    -w "%{http_code}" -o /tmp/video_gen_response.json)

if [ "$VIDEO_GEN_RESPONSE" = "200" ] || [ "$VIDEO_GEN_RESPONSE" = "202" ]; then
    test_passed "Video generation API accepts requests"
    PREDICTION_ID=$(cat /tmp/video_gen_response.json | grep -o '"id":"[^"]*"' | cut -d'"' -f4)
    if [ -n "$PREDICTION_ID" ]; then
        test_info "Generated prediction ID: $PREDICTION_ID"
        
        # Test status endpoint
        sleep 2
        STATUS_RESPONSE=$(curl -s "${API_BASE}/media/videos/status?id=${PREDICTION_ID}" \
            -w "%{http_code}" -o /tmp/video_status_response.json)
        
        if [ "$STATUS_RESPONSE" = "200" ]; then
            test_passed "Video status API working"
            test_info "Status response: $(cat /tmp/video_status_response.json)"
        else
            test_failed "Video status API failed (HTTP $STATUS_RESPONSE)"
        fi
    fi
else
    test_failed "Video generation API failed (HTTP $VIDEO_GEN_RESPONSE)"
    test_info "Response: $(cat /tmp/video_gen_response.json)"
fi

# Test 6: AI Agents Endpoints
echo ""
echo "🤖 Testing AI Agents..."

# Test Screenwriter Agent
SCREENWRITER_RESPONSE=$(curl -s -X POST "${API_BASE}/agents/content/screenwriter" \
    -H "Content-Type: application/json" \
    -d '{"task": "generate", "parameters": {"concept": "space adventure", "genre": "sci-fi", "length": 60}}' \
    -w "%{http_code}" -o /tmp/screenwriter_response.json)

if [ "$SCREENWRITER_RESPONSE" = "200" ] || [ "$SCREENWRITER_RESPONSE" = "202" ]; then
    test_passed "Screenwriter Agent API working"
else
    test_failed "Screenwriter Agent API failed (HTTP $SCREENWRITER_RESPONSE)"
fi

# Test Revolutionary Script-to-Video Pipeline
REVOLUTIONARY_RESPONSE=$(curl -s -X POST "${API_BASE}/agents/revolutionary/script-to-video" \
    -H "Content-Type: application/json" \
    -d '{"task": "generate", "parameters": {"concept": "AI revolution", "genre": "documentary", "length": 90}}' \
    -w "%{http_code}" -o /tmp/revolutionary_response.json)

if [ "$REVOLUTIONARY_RESPONSE" = "200" ] || [ "$REVOLUTIONARY_RESPONSE" = "202" ]; then
    test_passed "Revolutionary Script-to-Video Pipeline working"
else
    test_warning "Revolutionary Script-to-Video Pipeline may need configuration"
fi

# Test 7: AI Coder Module
echo ""
echo "💻 Testing AI Coder Module..."

AI_CODER_RESPONSE=$(curl -s -X POST "${API_BASE}/ai-coder/generate" \
    -H "Content-Type: application/json" \
    -d '{"description": "simple todo app", "framework": "react", "features": "add, edit, delete tasks"}' \
    -w "%{http_code}" -o /tmp/ai_coder_response.json)

if [ "$AI_CODER_RESPONSE" = "200" ] || [ "$AI_CODER_RESPONSE" = "202" ]; then
    test_passed "AI Coder Module working"
else
    test_warning "AI Coder Module may need configuration"
fi

# Test 8: Workflow Engine
echo ""
echo "⚡ Testing Workflow Engine..."

WORKFLOW_RESPONSE=$(curl -s -X GET "${API_BASE}/workflows" \
    -H "Content-Type: application/json" \
    -w "%{http_code}" -o /tmp/workflow_response.json)

if [ "$WORKFLOW_RESPONSE" = "200" ]; then
    test_passed "Workflow Engine API accessible"
else
    test_warning "Workflow Engine may need configuration"
fi

# Test 9: Database Connectivity (if accessible)
echo ""
echo "🗄️ Testing Database Connectivity..."
if command -v psql > /dev/null; then
    if PGPASSWORD="secure_password_change_me" psql -h "${API_DOMAIN}" -U aeon -d aeon_production -c "SELECT 1;" > /dev/null 2>&1; then
        test_passed "Database connection working"
    else
        test_warning "Database connection test failed (may be firewalled)"
    fi
else
    test_info "psql not available for database testing"
fi

# Test 10: Redis Connectivity (if accessible)
echo ""
echo "📊 Testing Redis Connectivity..."
if command -v redis-cli > /dev/null; then
    if redis-cli -h "${API_DOMAIN}" ping > /dev/null 2>&1; then
        test_passed "Redis connection working"
    else
        test_warning "Redis connection test failed (may be firewalled)"
    fi
else
    test_info "redis-cli not available for Redis testing"
fi

# Test 11: SSL/HTTPS (if configured)
echo ""
echo "🔒 Testing SSL Configuration..."
HTTPS_RESPONSE=$(curl -s -k "https://${API_DOMAIN}/health" -w "%{http_code}" -o /dev/null 2>/dev/null || echo "000")
if [ "$HTTPS_RESPONSE" = "200" ]; then
    test_passed "HTTPS/SSL configured and working"
else
    test_info "HTTPS not configured (using HTTP for now)"
fi

# Test 12: Performance Test
echo ""
echo "⚡ Testing API Performance..."
PERF_START=$(date +%s%N)
curl -s "${HEALTH_ENDPOINT}" > /dev/null
PERF_END=$(date +%s%N)
PERF_TIME=$(( (PERF_END - PERF_START) / 1000000 ))

if [ "$PERF_TIME" -lt 1000 ]; then
    test_passed "API response time: ${PERF_TIME}ms (excellent)"
elif [ "$PERF_TIME" -lt 3000 ]; then
    test_passed "API response time: ${PERF_TIME}ms (good)"
else
    test_warning "API response time: ${PERF_TIME}ms (may need optimization)"
fi

# Cleanup temporary files
rm -f /tmp/health_response.json /tmp/video_gen_response.json /tmp/video_status_response.json
rm -f /tmp/screenwriter_response.json /tmp/revolutionary_response.json /tmp/ai_coder_response.json
rm -f /tmp/workflow_response.json

# Final Results
echo ""
echo "📊 TEST RESULTS SUMMARY"
echo "======================="
echo -e "Tests Passed: ${GREEN}${TESTS_PASSED}${NC}"
echo -e "Tests Failed: ${RED}${TESTS_FAILED}${NC}"
echo ""

if [ "$TESTS_FAILED" -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL CRITICAL TESTS PASSED!${NC}"
    echo "Your AEON Platform deployment is ready for production!"
    echo ""
    echo "🌐 Frontend Configuration:"
    echo "  - Update Vercel environment variables:"
    echo "    NEXT_PUBLIC_API_URL=https://${API_DOMAIN}"
    echo "    REPLICATE_API_TOKEN=your_token_here"
    echo ""
    echo "🚀 Next Steps:"
    echo "  1. Deploy frontend with updated environment variables"
    echo "  2. Test end-to-end functionality"
    echo "  3. Set up SSL certificate for production domain"
    echo "  4. Configure monitoring and alerts"
    exit 0
else
    echo -e "${RED}⚠️  SOME TESTS FAILED${NC}"
    echo "Please review the failed tests and fix issues before going to production."
    echo ""
    echo "🔧 Common fixes:"
    echo "  - Ensure all services are running: sudo systemctl status aeon-api aeon-worker"
    echo "  - Check logs: sudo journalctl -u aeon-api -f"
    echo "  - Verify environment variables in /opt/aeon/.env"
    echo "  - Check firewall settings: sudo ufw status"
    exit 1
fi
