# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the requirements.txt file into the container at /app
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . /app

# Make port 5051 available to the world outside this container
EXPOSE 5051

# Define the environment variable for Python
ENV PYTHONUNBUFFERED=1

# Run email.py when the container launches
CMD ["python", "email_service.py"]
