# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Add the application directory to the Python path
ENV PYTHONPATH=/app

# Define environment variable
ENV FLASK_APP=server.py

# Run server.py when the container launches
CMD ["python", "core/server.py"]