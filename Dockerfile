# Use an official lightweight Python image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install build dependencies (if any) and pip upgrade
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency manifest
COPY pyproject.toml /app/

# Install pip tools and dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir "flask>=3.0.0" "Pillow>=9.0.0"

# Copy application files
COPY . /app

# Ensure static/images and database file are present and writable
RUN mkdir -p /app/static/images
RUN touch /app/projects.db || true
RUN chmod -R a+rw /app/static /app/projects.db

# Expose port
EXPOSE 5000

# Default command — run the Flask app
CMD ["python", "app.py"]
