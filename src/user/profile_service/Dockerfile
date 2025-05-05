FROM python:3.12

WORKDIR /app

# Copy requirements first for better layer caching
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port the app will run on
EXPOSE 8002

# Run the application
CMD ["python", "main.py"]