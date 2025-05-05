FROM python:3.12

WORKDIR /app

# Install system dependencies for web scraping
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app will run on
EXPOSE 8005

# Run the application
CMD ["python", "main.py"]
