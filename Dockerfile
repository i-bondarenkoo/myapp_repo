# FROM python:3.11-slim

# # RUN addgroup --system --gid 1000 appuser && \
# #     adduser --system --uid 1000 --ingroup appuser appuser

# WORKDIR /app
# COPY --chown=appuser:appuser app.py .

# USER appuser

# CMD ["python", "app.py"]

FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
