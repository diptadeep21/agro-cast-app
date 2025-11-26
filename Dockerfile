# Use the official Python image as the base image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app files into the container
COPY . .

# Expose the port that the app will run on
EXPOSE 8080

# Use gunicorn for production (WSGI HTTP Server)
# Workers: 2 * CPU cores + 1 (for 1 CPU, that's 3 workers)
# Bind to 0.0.0.0 to accept connections from outside the container
# Timeout increased for API calls
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "3", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
