# ==========================================
# Stage 1: Build dependencies
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools for Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

# Copy dependency file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ==========================================
# Stage 2: Production runtime
# ==========================================
FROM python:3.11-slim AS runtime

WORKDIR /app

# Runtime environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy backend source code
COPY . .

# Create non-root user
RUN useradd --create-home appuser && \
    chown -R appuser:appuser /app

USER appuser

# FastAPI default port
EXPOSE 8000

# Start FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 