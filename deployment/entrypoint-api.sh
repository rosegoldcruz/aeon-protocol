set -e
echo "Waiting for Postgres and Redis..."
/wait-for-it.sh ${DATABASE_HOST:-postgres}:5432 -t 60
/wait-for-it.sh ${REDIS_HOST:-redis}:6379 -t 60
echo "Running migrations..."
alembic upgrade head
echo "Starting API..."
uvicorn services.api.app.main:app --host 0.0.0.0 --port 8000
