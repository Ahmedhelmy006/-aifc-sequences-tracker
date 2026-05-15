# Use a slim Python image for efficiency
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Prevent Python from writing .pyc files and enable unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies if needed (none currently required for your imports)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Ensure the logs directory exists
RUN mkdir -p logs

# Use a shell script or entrypoint to allow switching between tasks
# Usage: docker run <image_name> python -m core.main approved
# Usage: docker run <image_name> python -m core.main fomo
ENTRYPOINT ["python", "-m"]