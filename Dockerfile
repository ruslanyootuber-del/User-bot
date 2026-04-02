# 3.9 ni 3.10 ga almashtiramiz
FROM python:3.10-slim

# Tizim kutubxonalarini o'rnatish (instagrapi uchun kerak)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Barcha fayllarni ko'chirish (shu jumladan insta_session.json ni ham)
COPY . .

# Kutubxonalarni o'rnatish
RUN pip install --no-cache-dir -r requirements.txt

# Botni ishga tushirish
CMD ["python", "main.py"]
