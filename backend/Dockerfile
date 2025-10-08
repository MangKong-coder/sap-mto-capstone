# ──────────────
# 1. Base Stage
# ──────────────
FROM python:3.11-slim

WORKDIR /app

# Prevent Python from writing pyc files & buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*d
# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app with uvicorn
# You can adjust the module path if your entrypoint is different
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
