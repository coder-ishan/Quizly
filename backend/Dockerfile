# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port FastAPI is running on
EXPOSE 8080

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "localhost", "--port", "8080"]

# Add Chroma server setup
RUN apt-get update && apt-get install -y \
    chroma-server

# Add PostgreSQL setup
RUN apt-get install -y postgresql postgresql-contrib

# Set environment variables for PostgreSQL
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=ABCD1234
ENV POSTGRES_DB=quizzlyDB

# Start PostgreSQL service
RUN service postgresql start

# Expose the PostgreSQL port
EXPOSE 5432