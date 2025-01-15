# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies using pip from the setup.py and requirements.txt
RUN pip install --upgrade pip \
    && pip install setuptools \
    && pip install -e .


# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define the environment variable for the container
ENV PYTHONUNBUFFERED=1

# Run the application when the container starts
CMD ["python", "app/main.py"]