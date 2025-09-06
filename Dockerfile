FROM python:3.12-alpine AS builder

RUN apk add --no-cache \
    gcc \
    musl-dev \
    python3-dev \
    libffi-dev \
    make

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir gunicorn==23.00

FROM python:3.12-alpine AS runner

WORKDIR /app

COPY --from=builder /usr/local /usr/local
COPY . .


RUN adduser -D appuser
USER appuser

CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
