# FastAPI JWT Generator & Verifier

A lightweight, robust microservice built with FastAPI to manually generate and verify JSON Web Tokens (JWT) using EdDSA (Ed25519) cryptographic signatures.

## Features

- **EdDSA (Ed25519) Signatures**: High-security, high-performance asymmetric cryptographic keys.
- **FastAPI Core**: Fast, modern API with automatic JSON Schema and interactive documentation via Swagger UI.
- **JWKS Endpoint**: Dynamically expose your public key via the `/jwks` route.
- **Docker Ready**: Fully containerized using multi-stage builds and best security practices.

## Prerequisites

- [Docker](https://www.docker.com/) & Docker Compose
- *Optional*: Python 3.12+ if running locally on your hardware.

## Setup Instructions

### 1. Key Generation (Automatic in Docker)

**If using Docker:** You are securely set! The `Dockerfile` automatically generates a fresh, container-scoped `getJwt` Ed25519 keypair safely inside the container during the build process, isolating it from your local system.

**If running locally (without Docker):** This application expects an Ed25519 SSH keypair (`getJwt` and `getJwt.pub`) located in the root directory. You can generate them by running:

```bash
ssh-keygen -t ed25519 -f ./getJwt -N "" -q
```
*(The `.gitignore` is already configured to prevent these from being checked into version control).*

### 2. Running With Docker (Recommended)

**Development Environment** (with live code reloading):
```bash
docker-compose up --build
```

**Production Environment** (uses Uvicorn workers, restarts automatically, and does not mount source code dynamically):
```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

### 3. Running Locally without Docker

1. Create a virtual environment: `python -m venv .venv`
2. Activate the virtual environment:
   - Windows: `.venv\Scripts\activate`
   - Linux/Mac: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Run the development server: `uvicorn main:app --reload`

## API Reference

Once the application starts, navigate to the interactive OpenAPI docs:  
**➡ [http://localhost:8000/docs](http://localhost:8000/docs)**

### Endpoints

* **`GET /`**: Health-check endpoint.
* **`GET /jwks`**: Returns the JSON Web Key Set (JWKS), useful for other clients and microservices that need to verify your tokens independently.
* **`POST /generate-token`**: Takes a JSON `payload` and an `expires_in_hours` value to cryptographically sign and return a new JWT.
* **`POST /verify-token`**: Takes the `token` and the `x` component of your public key. Decodes and verifies the signature and expiration timestamp.

## Security Practices

* The `Dockerfile` creates a non-root User (`appuser`) to ensure the container acts with least-privilege principles.
* Private keys are granted strict Linux file permissions (`600`) within the Docker image.
* For enterprise-grade production, it's recommended to mount your keys into the production container dynamically (e.g. through Docker Secrets or read-only volume mounts) rather than building them into the image using `COPY`.
