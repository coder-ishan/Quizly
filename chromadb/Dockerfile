# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port ChromaDB is running on
EXPOSE 8001

# Set the environment variable for the port
ENV PORT 8001

# Command to run the ChromaDB application
CMD ["chroma", "run", "--host", "0.0.0.0", "--port", "8001"]