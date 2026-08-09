# ============================================================
# Face Authentication System - Dockerfile (Optimized)
# Python 3.11 with face_recognition library
# ============================================================

FROM python:3.11-slim

# ── Labels ──────────────────────────────────────────────────
LABEL maintainer="Face Auth System"
LABEL description="Face Authentication System with face_recognition"
LABEL python.version="3.11"

# ── Build-time args ─────────────────────────────────────────
ARG DEBIAN_FRONTEND=noninteractive

# ── System dependencies for dlib compilation ─────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        libopenblas-dev \
        liblapack-dev \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender-dev \
        libgomp1 \
        libssl-dev \
        libffi-dev \
        vim \
        nano \
        curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# ── Working directory ────────────────────────────────────────
WORKDIR /app


# ── Upgrade pip ──────────────────────────────────────────────
RUN pip install --upgrade pip setuptools wheel

# ── Install numpy first (compatible version) ─────────────────
# CRITICAL: Must be <2.0.0 for face_recognition compatibility
# Pin to specific version to avoid numpy 2.x issues
RUN pip install --no-cache-dir "numpy==1.26.4"

# ── Install opencv-python-headless (compatible with numpy 1.x) ─
# Specify version to ensure compatibility
RUN pip install --no-cache-dir "opencv-python-headless==4.9.0.80"

# ── Install face_recognition with pre-built wheels ────────────
# Using specific versions that have pre-built wheels to avoid compilation
# This installs dlib and face_recognition without needing to compile
RUN pip install --no-cache-dir "face-recognition==1.3.0" || \
    (echo "WARNING: face_recognition installation failed, will use OpenCV fallback" && true)

# ── Copy requirements and install remaining dependencies ─────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ── Copy application source ──────────────────────────────────
COPY . .

# ── Create required directories with proper permissions ──────
RUN mkdir -p logs instance ai_service/data && \
    chmod -R 777 logs instance ai_service/data

# ── Environment variables ────────────────────────────────────
ENV FLASK_ENV=production
ENV FLASK_HOST=0.0.0.0
ENV FLASK_PORT=5000
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# ── Expose port ──────────────────────────────────────────────
EXPOSE 5000

# ── Health check ─────────────────────────────────────────────
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f -k https://localhost:5000/health || exit 1

# ── Entrypoint ───────────────────────────────────────────────
 CMD ["python", "run.py"]
# CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]

