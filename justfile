# Justfile for League Labs Scheduler

# Set environment variables
set export
FLASK_APP := "wsgi:app"

# Run the Flask development server
dev:
    flask run --host=0.0.0.0 --debug

# Recreate the database (deletes and recreates)
recreate-db: 
    python3 init_db.py

build:
    docker build -t flaskapp .

# Run the Docker application with all services
run:
    docker compose up --build

# Run Docker in detached mode
run-detached:
    docker compose up -d --build

# Stop Docker containers
stop:
    docker compose down

# Run Docker for development with local MongoDB access
dev-docker:
    docker compose -f docker-compose.dev.yml up --build


######
# Database migration commands
# Initialize migrations (run once when setting up the project)
migrate-init:
    flask db init

# Create a new migration
migrate-create message="database changes":
    flask db migrate -m "{{message}}"

# Apply migrations in development environment
migrate-dev:
    flask db upgrade

# Apply migrations in production environment
migrate-prod:
    FLASK_ENV=production flask db upgrade

# Downgrade database to previous migration
migrate-down:
    flask db downgrade

# Show migration history
migrate-history:
    flask db history

# Show current migration
migrate-current:
    flask db current
