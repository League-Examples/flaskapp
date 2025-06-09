# Flask App Development Guide

This document provides information about the development setup and workflows for the Flask application.

## Development Environment Setup

### Prerequisites

- Python 3.13 or higher
- Docker (for database services)
- Git

### Initial Setup

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies:
   ```bash
   pip install -e .
   ```

## CLI Commands

The application provides several CLI commands to help with development tasks. These commands are accessible via the `flask` command-line interface.

### Basic Commands

- `flask cmd1` - Example command that prints "command 1"
- `flask cmd2` - Example command that prints "command 2"

### Development Commands

The application provides a set of development-specific commands under the `flask dev` namespace.

#### Database Management

The `flask dev db` commands manage a PostgreSQL database in Docker for development:

- `flask dev db start` - Start the PostgreSQL database in Docker
  - Creates and starts a Docker container running PostgreSQL
  - If the container already exists but is not running, it will start it
  - If the container is already running, it will report that fact
  - After starting, it displays connection details

- `flask dev db stop` - Stop the PostgreSQL database container
  - Stops the Docker container running PostgreSQL
  - The container is not removed, so data is preserved

- `flask dev db status` - Check the status of the PostgreSQL database
  - Shows whether the database container exists and is running
  - Displays port mapping information if the container is running

#### Database Connection Details

When using the development database, the following connection details are used:

- **Host**: localhost
- **Port**: 5432
- **User**: postgres
- **Password**: postgres
- **Database**: flaskapp_dev
- **URI**: postgresql://postgres:postgres@localhost:5432/flaskapp_dev

These settings are configured in `flaskapp/config/development.py` and can be overridden using environment variables:

- `DEV_DB_USER`
- `DEV_DB_PASSWORD`
- `DEV_DB_NAME`
- `DEV_DB_HOST`
- `DEV_DB_PORT`
- `DEV_DATABASE_URI` (to override the entire connection string)

## Development Workflow

1. Start the development database:
   ```bash
   PYTHONPATH=. flask dev db start
   ```

2. Run the application in development mode:
   ```bash
   PYTHONPATH=. flask run --debug
   ```

3. When finished, stop the database:
   ```bash
   PYTHONPATH=. flask dev db stop
   ```

## Testing

Tests can be run using pytest:

```bash
pytest
```

For running specific tests:

```bash
pytest test/test_module.py
```

## Docker Deployment

For testing the Docker deployment locally:

```bash
cd docker
docker-compose up --build
```

This will build and start both the web application and a PostgreSQL database.