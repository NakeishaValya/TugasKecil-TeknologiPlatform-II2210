# Menggunakan image dasar Python 3.10.12
FROM python:3.10.12-slim

# Menetapkan working directory ke /app
WORKDIR /app

# Menyalin semua file dari direktori lokal ke dalam container
COPY . .

# Menginstal dependensi yang dibutuhkan
RUN pip install --no-cache-dir \
    fastapi>=0.95.0 \
    uvicorn>=0.21.1 \
    sqlmodel>=0.0.8 \
    pyotp>=2.8.0 \
    python-multipart>=0.0.6

# Mengekspos port yang digunakan oleh aplikasi
EXPOSE 17787

# Menjalankan server Uvicorn untuk aplikasi FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "17787"]

