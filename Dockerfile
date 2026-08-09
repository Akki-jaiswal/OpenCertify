FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port for Flask
EXPOSE 5000

# Set environment variables for production
ENV FLASK_ENV=production
ENV PYTHONUNBUFFERED=1

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "server:app"]
