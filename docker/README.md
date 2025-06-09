# Flask App Docker Deployment Guide

This guide provides instructions for deploying the Flask application using Docker and Docker Compose.

## Prerequisites

- Docker and Docker Compose installed on your system
- Basic knowledge of Docker and Docker Compose commands

## Setup and Deployment

1. **Build and Start the Containers**

   From the project root directory, run:

   ```bash
   cd docker
   docker-compose up --build -d
   ```

   This will build the Docker images and start the containers in detached mode.

2. **Check Container Status**

   ```bash
   docker-compose ps
   ```

   You should see both the web application and PostgreSQL database containers running.

3. **Access the Application**

   The application will be available at:

   ```
   http://localhost:8000
   ```

4. **View Logs**

   To view the logs from the application container:

   ```bash
   docker-compose logs -f web
   ```

## Container Configuration

- **Web Application**: Runs on port 8000 using Gunicorn as the WSGI server
- **PostgreSQL Database**: Runs on port 5432 with the following credentials:
  - Username: postgres
  - Password: postgres
  - Database: flaskapp

## Environment Variables

You can customize the application by setting environment variables in the `.env` file or passing them to docker-compose:

- `SECRET_KEY`: Secret key for session management
- `DATABASE_URI`: Override the default database connection string

## Deployment to Remote Servers

When deploying to remote servers:

1. Build the Docker images locally:
   ```bash
   docker-compose build
   ```

2. Push the images to a container registry:
   ```bash
   docker tag flaskapp [your-registry]/flaskapp:latest
   docker push [your-registry]/flaskapp:latest
   ```

3. On the remote server, pull the images and start the containers:
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

## Troubleshooting

- **Database Connection Issues**: Ensure the database container is running and the `DATABASE_URI` environment variable is correctly set
- **Application Errors**: Check the application logs with `docker-compose logs web`
