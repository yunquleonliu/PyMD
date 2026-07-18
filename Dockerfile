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
    "pdf2docx>=0.5.6" \
    "openpyxl>=3.1" \
    "python-pptx>=0.6.23" \
    "pymupdf>=1.22.5" \
    "python-dateutil>=2.8.2"

# ── Runtime stage ─────────────────────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copy source. The web server image includes backend PDF/document conversion deps.
COPY src/ ./src/

# Make pymd_editor importable
ENV PYTHONPATH=/app/src
ENV PYMD_DEPLOYMENT_MODE=cloud

EXPOSE 8765

# /data is volume-mounted to the user's document folder
VOLUME ["/data"]

CMD ["python", "-m", "pymd_editor", "serve", \
     "--dir", "/data", \
     "--host", "0.0.0.0", \
     "--port", "8765", \
     "--no-browser"]
