# Use a Python base image
FROM python:3.11-slim

# Install dependencies including ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean

# Set working directory
WORKDIR /app

# Copy your project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the correct port
ENV PORT=10000
EXPOSE 10000

# Run the Flask app
CMD ["python", "main.py"]
