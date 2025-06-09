FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=flaskapp.wsgi:app \
    FLASK_ENV=production \
    FLASK_DEBUG=0

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml setup.py README.md /app/
COPY flaskapp/ /app/flaskapp/
COPY test/ /app/test/

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -e .

# Create a non-root user and switch to it
RUN useradd -m appuser
USER appuser

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "flaskapp.wsgi:app"]
