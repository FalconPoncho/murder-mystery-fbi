FROM ubuntu:latest

# Install Python and Git
RUN apt update && \
    apt install -y python3.12 python3.12-venv python3-pip git && \
    apt clean

# Set working directory
WORKDIR /app

# Copy requirements first for layer caching
# COPY requirements.txt .

# Create and activate virtual environment, and install dependencies
ENV VIRTUAL_ENV=venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin/:$PATH"

RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# # CMD ["python3", "main.py"]