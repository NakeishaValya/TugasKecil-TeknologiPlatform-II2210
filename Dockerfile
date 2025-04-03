FROM python:3.10.12-slim

WORKDIR /app

RUN pip install --no-cache-dir \
    fastapi>=0.95.0 \
    uvicorn>=0.21.1 \
    sqlmodel>=0.0.8 \
    pyotp>=2.8.0 \
    python-multipart>=0.0.6

COPY . .

RUN mkdir -p static

RUN if [ ! -f static/index.html ]; then \
    echo '<!DOCTYPE html><html><head><title>Message of the Day</title></head><body><h1>Message of the Day</h1><p>Use /motd endpoint to get or post messages.</p></body></html>' > static/index.html; \
    fi

EXPOSE 17787

CMD ["python", "main.py"]
