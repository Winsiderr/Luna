#!/bin/bash
set -e

echo "Running migrations..."
max_attempts=30
for i in $(seq 1 $max_attempts); do
    if alembic upgrade head; then
        echo "Migrations applied."
        break
    fi
    if [ $i -eq $max_attempts ]; then
        echo "Database unavailable after $max_attempts attempts"
        exit 1
    fi
    echo "Attempt $i/$max_attempts - retrying in 2s..."
    sleep 2
done

echo "Starting application..."
exec "$@"
