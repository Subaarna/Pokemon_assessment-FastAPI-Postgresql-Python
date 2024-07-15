FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code and wait-for-it script
COPY . .

# Make wait-for-it.sh executable
RUN chmod +x /app/wait-for-it.sh

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["./wait-for-it.sh", "db", "--", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
