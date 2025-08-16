#!/bin/bash

# AEON Platform FastAPI Entrypoint Script

set -e

echo "🚀 Starting AEON Platform FastAPI Backend..."

# Wait for database to be ready
echo "⏳ Waiting for database connection..."
python -c "
import time
import psycopg2
import os
from urllib.parse import urlparse

db_url = os.getenv('DATABASE_URL')
if db_url:
    parsed = urlparse(db_url)
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = psycopg2.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password=parsed.password,
                database=parsed.path[1:]
            )
            conn.close()
            print('✅ Database connection successful!')
            break
        except psycopg2.OperationalError:
            retry_count += 1
            print(f'⏳ Database not ready, retrying... ({retry_count}/{max_retries})')
            time.sleep(2)
    else:
        print('❌ Could not connect to database after 30 attempts')
        exit(1)
"

# Wait for Redis to be ready
echo "⏳ Waiting for Redis connection..."
python -c "
import time
import redis
import os
from urllib.parse import urlparse

redis_url = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
parsed = urlparse(redis_url)
max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        r = redis.Redis(
            host=parsed.hostname or 'localhost',
            port=parsed.port or 6379,
            db=int(parsed.path[1:]) if parsed.path and len(parsed.path) > 1 else 0
        )
        r.ping()
        print('✅ Redis connection successful!')
        break
    except redis.ConnectionError:
        retry_count += 1
        print(f'⏳ Redis not ready, retrying... ({retry_count}/{max_retries})')
        time.sleep(2)
else:
    print('❌ Could not connect to Redis after 30 attempts')
    exit(1)
"

# Run database migrations (if any)
echo "🗄️ Running database migrations..."
# python -m alembic upgrade head

# Create necessary directories
mkdir -p /app/logs /app/uploads /app/temp

echo "✅ AEON Platform FastAPI Backend is ready!"
echo "🌐 Starting server on 0.0.0.0:8000"

# Execute the main command
exec "$@"
