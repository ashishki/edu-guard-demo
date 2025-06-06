# Use official Python 3.12 slim image as base
FROM python:3.12-slim

# Set working directory inside the container to /app
WORKDIR /app

# Copy only pyproject.toml and poetry.lock to leverage build cache
COPY pyproject.toml poetry.lock* /app/

# Install Poetry and project dependencies without installing the current project itself
RUN pip install --no-cache-dir "poetry>=1.5.1" \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy the rest of the application code into /app
COPY . /app

# Ensure the chroma_db directory exists
RUN mkdir -p /app/chroma_db

# Expose port 8000 for Uvicorn
EXPOSE 8000

# Default command to run the FastAPI application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

