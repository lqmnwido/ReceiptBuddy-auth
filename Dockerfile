FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc git && \
    rm -rf /var/lib/apt/lists/*

# Copy local common library (avoids dependency on GitHub repo for schema changes)
COPY common/ /app/common/

# Copy service code
COPY services/auth/ /app/services/auth/

# Install dependencies (common is now installed from local copy)
RUN pip install --no-cache-dir -r /app/services/auth/requirements.txt && \
    pip install -e /app/common

ENV PYTHONPATH=/app

EXPOSE 8001

CMD ["uvicorn", "services.auth.app.main:app", "--host", "0.0.0.0", "--port", "8001"]
