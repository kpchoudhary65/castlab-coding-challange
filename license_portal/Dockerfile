FROM python:3.10

RUN mkdir -p /app
COPY license_portal/requirements.txt /app
# COPY .env.dev /app/
RUN pip install -r /app/requirements.txt

WORKDIR /app
