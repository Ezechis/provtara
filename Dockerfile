FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app/phase1/src:/app/phase0/src \
    FLASK_DEBUG=0

COPY phase1/requirements.txt /tmp/phase1-requirements.txt
RUN pip install --no-cache-dir -r /tmp/phase1-requirements.txt

COPY phase0 /app/phase0
COPY phase1 /app/phase1

EXPOSE 7860
CMD ["sh", "-c", "gunicorn --chdir phase1 -b 0.0.0.0:${PORT:-7860} run:app --threads 4 --timeout 120"]
