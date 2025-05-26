# Use official Python image as base
FROM python:3.10-slim

# Upgrade pip and setuptools to latest versions to reduce vulnerabilities
RUN pip install --upgrade pip setuptools

# Update system packages to reduce vulnerabilities
RUN apt-get update && apt-get upgrade -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements if present
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port (change if your API uses a different port)
EXPOSE 8000

# Set default command (adjust if your API uses a different entrypoint)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]