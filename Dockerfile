# Use the official Python image
FROM python:3.12.3-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Prevent Python from writing .pyc files and buffer output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Install dependencies
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /usr/src/app/requirements.txt

# Copy the entire project into the container
COPY . /usr/src/app/