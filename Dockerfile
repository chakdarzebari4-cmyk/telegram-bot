# استخدام نسخة بايثون رسمية وخفيفة
FROM python:3.10-slim

# تثبيت أدوات البناء اللازمة للنظام
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# تحديد مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات وتثبيته
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ باقي ملفات المشروع
COPY . .

# أمر تشغيل البوت (تأكد من تغيير bot.py لاسم ملفك الأساسي)
CMD ["python", "bot.py"]
