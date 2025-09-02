# ---------- Builder stage ----------
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# ---------- Final stage ----------
FROM python:3.11-slim

WORKDIR /app

RUN useradd -m appuser \
    && apt-get update \
    && apt-get install -y --no-install-recommends libpq5 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

COPY . .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
