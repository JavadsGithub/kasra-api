# Dockerfile
# استفاده از تصویر پایه Python
FROM python:3.12

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل‌های مورد نیاز به دایرکتوری کاری
COPY requirements.txt ./

# نصب وابستگی‌ها
RUN pip install --no-cache-dir -r requirements.txt

# کپی کد برنامه به دایرکتوری کاری
COPY . .

# اجرای برنامه با uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]