# Use an official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY requirements.txt .
COPY bot.py .
COPY email_sender.py .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# RUN chown -R 1000:1000 /app

# USER 1000

# Expose no network ports (bot connects to Discord via outgoing traffic)
CMD ["python3", "bot.py"]
