import base64
import os
import datetime
import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from app.core.config import settings

def get_jwk():
    if not os.path.exists(settings.PRIVATE_KEY_PATH):
        raise FileNotFoundError("Key file not found")

    with open(settings.PRIVATE_KEY_PATH, "rb") as f:
        key_data = f.read()

    try:
        private_key = serialization.load_ssh_private_key(key_data, password=None)
        public_key = private_key.public_key()
        raw_pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw
        )
        x_value = base64.urlsafe_b64encode(raw_pub_bytes).decode("utf-8").rstrip("=")

        return {
            "keys": [
                {
                    "alg": "EdDSA",
                    "crv": "Ed25519",
                    "x": x_value,
                    "kty": "OKP",
                    "kid": "get-jwt-manual-key-01",
                }
            ]
        }
    except Exception as e:
        print(f"Error loading key: {e}")
        raise e

def get_private_key():
    if not os.path.exists(settings.PRIVATE_KEY_PATH):
        raise FileNotFoundError(f"Private key not found at {settings.PRIVATE_KEY_PATH}")
    with open(settings.PRIVATE_KEY_PATH, "r") as f:
        return f.read()

def create_jwt_token(payload: dict, expires_in_hours: int) -> str:
    with open(settings.PRIVATE_KEY_PATH, "rb") as f:
        key_data = f.read()

    private_key_obj = serialization.load_ssh_private_key(key_data, password=None)

    data_to_encode = payload.copy()
    now = datetime.datetime.now(datetime.timezone.utc)
    data_to_encode.update(
        {
            "exp": now + datetime.timedelta(hours=expires_in_hours),
            "iat": now,
            "iss": "fastapi-jwt-provider",
        }
    )

    token = jwt.encode(
        data_to_encode,
        private_key_obj,  
        algorithm="EdDSA",
        headers={"kid": "get-jwt-manual-key-01"},
    )
    return token

def verify_jwt_token(token: str, x: str) -> dict:
    padding = "=" * (4 - len(x) % 4)
    public_key_bytes = base64.urlsafe_b64decode(x + padding)

    public_key_obj = ed25519.Ed25519PublicKey.from_public_bytes(public_key_bytes)

    decoded_payload = jwt.decode(
        token,
        public_key_obj,
        algorithms=["EdDSA"],
        issuer="fastapi-jwt-provider",
    )
    return decoded_payload
