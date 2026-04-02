# 3.9 o'rniga 3.10-slim yoki 3.11-slim ishlatamiz
FROM python:3.10-slim

# Kerakli tizim paketlarini o'rnatish
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
