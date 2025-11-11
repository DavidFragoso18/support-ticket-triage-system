#!/bin/bash
# Docker Compose Test Script
# Verifies that all services start correctly

set -e

echo "🧪 Testing Docker Compose Deployment"
echo "===================================="
echo ""

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ docker-compose.yml not found!"
    exit 1
fi

# Check if .env exists, if not copy from .env.docker
if [ ! -f ".env" ]; then
    echo "📝 Creating .env from .env.docker..."
    cp .env.docker .env
fi

echo "🐳 Building Docker images..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Check if services are running
echo ""
echo "📊 Checking service status..."
docker-compose ps

# Test database connection
echo ""
echo "🗄️  Testing database connection..."
docker-compose exec -T db pg_isready -U postgres || {
    echo "❌ Database connection failed!"
    docker-compose logs db
    exit 1
}
echo "✅ Database is ready"

# Wait for backend to be ready
echo ""
echo "⏳ Waiting for backend to be ready (may take 1-2 minutes for model loading)..."
MAX_RETRIES=30
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend is healthy!"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Attempt $RETRY_COUNT/$MAX_RETRIES - Backend not ready yet, waiting..."
    sleep 5
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "❌ Backend failed to start within expected time!"
    echo ""
    echo "Backend logs:"
    docker-compose logs backend
    exit 1
fi

# Test backend API
echo ""
echo "🔍 Testing backend API..."
HEALTH_RESPONSE=$(curl -s http://localhost:8000/health)
echo "Health check response: $HEALTH_RESPONSE"

# Test classification endpoint
echo ""
echo "🤖 Testing classification endpoint..."
CLASSIFY_RESPONSE=$(curl -s -X POST http://localhost:8000/classify \
    -H "Content-Type: application/json" \
    -d '{"text":"My internet is not working"}')
echo "Classification response: $CLASSIFY_RESPONSE"

if echo "$CLASSIFY_RESPONSE" | grep -q "intent"; then
    echo "✅ Classification endpoint working!"
else
    echo "❌ Classification endpoint failed!"
    exit 1
fi

# Test frontend (if running)
echo ""
echo "🌐 Testing frontend..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    echo "✅ Frontend is accessible!"
else
    echo "⚠️  Frontend not accessible (this is OK if frontend is not built)"
fi

echo ""
echo "📊 Resource Usage:"
docker stats --no-stream

echo ""
echo "🎉 All tests passed!"
echo ""
echo "📝 Access URLs:"
echo "  Backend API: http://localhost:8000/docs"
echo "  Frontend: http://localhost:3000"
echo "  Database: localhost:5432"
echo ""
echo "🛠️  Useful commands:"
echo "  View logs: docker-compose logs -f"
echo "  Stop services: docker-compose down"
echo "  Clean everything: docker-compose down -v"
echo ""
