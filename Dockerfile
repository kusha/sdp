FROM python:3.9-slim

ARG FEATURE_A=""
ARG FEATURE_B=""
ARG FEATURE_C=""

ENV FEATURE_A=$FEATURE_A
ENV FEATURE_B=$FEATURE_B
ENV FEATURE_C=$FEATURE_C

WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl && apt-get clean && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
