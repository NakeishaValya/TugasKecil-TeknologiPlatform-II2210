FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY main.py model.py index.html ./

RUN mkdir -p /app/data

EXPOSE 17787

CMD ["python", "main.py"]
