# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Install Supervisord to manage multiple processes
RUN apt-get update && apt-get install -y --no-install-recommends \
    supervisor && apt-get clean

# Copy supervisord configuration file
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Set environment variables to prevent Python from buffering output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Command to start supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
