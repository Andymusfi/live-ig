FROM python:3.10-slim

# Instal ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirement dan install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy sisa kode
COPY main.py .

# Jalankan skrip tanpa buffering log
CMD ["python", "-u", "main.py"]
