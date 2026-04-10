FROM python:3.11-slim

# Keep Python output visible and avoid .pyc files in the container.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG BUILD_REF=
ARG DEPLOYED_AT=
ENV BUILD_REF=$BUILD_REF
ENV DEPLOYED_AT=$DEPLOYED_AT

WORKDIR /workspace

# Install application dependencies first for better Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the Flask application source code.
COPY app ./app

EXPOSE 5000

# Render and many other cloud platforms provide the port as an environment variable.
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${PORT:-5000} app.main:app"]
