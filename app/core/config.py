import os

class Settings:
    PROJECT_NAME: str = "JWT Generator & Verifier Microservice"
    PROJECT_DESCRIPTION: str = "A robust API to securely generate and verify JSON Web Tokens (JWT) using EdDSA (Ed25519) cryptographic signatures."
    PROJECT_VERSION: str = "1.0.0"
    PRIVATE_KEY_PATH: str = os.getenv("PRIVATE_KEY_PATH", "getJwt")

settings = Settings()
