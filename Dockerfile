# Use Python base image
FROM python:latest

# Set work directory in container
WORKDIR /workspace

# Copy requirements and install
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy all project files
COPY . /workspace

# Default command
CMD ["bash"]
