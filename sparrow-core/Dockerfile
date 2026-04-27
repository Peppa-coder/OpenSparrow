FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY pyproject.toml .
RUN pip install --no-cache-dir .

# Copy source
COPY sparrow/ sparrow/

# Create data directory
RUN mkdir -p /app/data

EXPOSE 8080 8081

CMD ["uvicorn", "sparrow.main:app", "--host", "0.0.0.0", "--port", "8080"]
