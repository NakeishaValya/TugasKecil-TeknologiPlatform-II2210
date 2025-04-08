FROM python:3.10.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir \
    fastapi>=0.0.7 \
    uvicorn>=0.23.2 \
    sqlmodel>=0.0.8 \
    pydantic>=2.3.0 \
    jinja2>=3.1.2 \
    pyotp>=2.8.0 \
    python-multipart>=0.0.6

EXPOSE 17787

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "17787"]
