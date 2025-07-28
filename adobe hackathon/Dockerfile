

FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && \
    apt-get install -y libglib2.0-0 libsm6 libxrender1 libxext6 && \
    pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]

