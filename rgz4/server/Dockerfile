FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y clamav && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]
