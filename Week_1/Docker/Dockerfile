
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script into the container
COPY data_ingestion.py .

# Set the command to run the Python script
CMD ["python", "data_ingestion.py"]
