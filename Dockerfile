FROM python:3.10.12-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn sqlmodel pyotp

COPY main.py model.py index.html ./

EXPOSE 17787

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "17787"]
