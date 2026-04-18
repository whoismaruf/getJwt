# Use a slim, secure python base image
FROM python:3.12-slim AS requirements-stage

# Set working directory for the builder stage
WORKDIR /tmp

# Copy requirements file (we assume pure python packages for now)
COPY ./requirements.txt /tmp/requirements.txt

# Install dependencies (this installs them into the image)
RUN pip install --no-cache-dir --prefix=/install -r /tmp/requirements.txt

# --- Final Stage ---
FROM python:3.12-slim

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Set environment variables (prevent python from writing pyc, keep stdout unbuffered)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Copy minimal installed packages from the builder stage
COPY --from=requirements-stage /install /usr/local

# Explicitly copy your private and public keys first
COPY --chown=appuser:appuser getJwt getJwt
COPY --chown=appuser:appuser getJwt.pub getJwt.pub
RUN chmod 600 getJwt

# Copy the rest of the application files
COPY --chown=appuser:appuser . .

# Switch to the non-root user
USER appuser

# Expose the API port
EXPOSE 8000

# Start Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
