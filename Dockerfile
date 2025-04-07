# Menggunakan image dasar Python 3.10.12
FROM python:3.10.12-slim

# Menetapkan working directory ke /app
WORKDIR /app

# Menyalin semua file dari direktori lokal ke dalam container
COPY . .

# Menginstal dependensi yang dibutuhkan
RUN pip install --no-cache-dir -r requirements.txt

# RUN python -c "from main import init_db; init_db()"

# Mengekspos port yang digunakan oleh aplikasi
EXPOSE 17787

# Menjalankan server Uvicorn untuk aplikasi FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "17787"]

