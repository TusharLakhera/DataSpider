# Use an official Python runtime as the base image
FROM python:3.9

# Install Redis
RUN apt-get update && apt-get install -y redis-server

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the working directory
COPY . .

# Create a directory for storing scraped data
RUN mkdir -p /app/data

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose the port on which the FastAPI application will run
EXPOSE 8000

# Create a script to start both Redis and your FastAPI app
RUN echo '#!/bin/bash\nredis-server --daemonize yes\nuvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4' > /start.sh
RUN chmod +x /start.sh

# Run the start script
CMD ["/start.sh"]