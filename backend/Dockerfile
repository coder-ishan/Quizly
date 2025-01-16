# Use the official Python image from the Docker Hub
FROM python:3.11.6

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download the cacert.pem file
RUN curl -o /etc/ssl/certs/cacert.pem https://curl.se/ca/cacert.pem

# Set the SSL_CERT_FILE environment variable
ENV SSL_CERT_FILE=/etc/ssl/certs/cacert.pem

# Copy the rest of the application code into the container
COPY . .

# Set the PORT environment variable
ENV PORT=9000

# Expose the port FastAPI is running on
EXPOSE 9000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "9000"]