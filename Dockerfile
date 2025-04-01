FROM python:3.10-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn sqlmodel pyotp

COPY main.py model.py index.html ./

EXPOSE 17787

CMD ["python", "main.py"]
