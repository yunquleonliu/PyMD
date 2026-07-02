# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /build

# Install only the server-required Python packages
RUN pip install --no-cache-dir \
    "fastapi>=0.100.0" \
    "uvicorn[standard]>=0.23.0" \
    "python-multipart>=0.0.6" \
    "markdown2>=2.4.0" \
    "python-docx>=1.1.0" \
    "httpx>=0.25.0" \
    "python-dateutil>=2.8.2"

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy source (no Qt deps, no PDF deps needed for the web server)
COPY src/ ./src/

# Make pymd_editor importable
ENV PYTHONPATH=/app/src

EXPOSE 8765

# /data is volume-mounted to the user's document folder
VOLUME ["/data"]

CMD ["python", "-m", "pymd_editor", "serve", \
     "--dir", "/data", \
     "--host", "0.0.0.0", \
     "--port", "8765", \
     "--no-browser"]
