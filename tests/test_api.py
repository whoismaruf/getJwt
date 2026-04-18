# import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "FastAPI JWT Generator is running"}


def test_get_jwks():
    response = client.get("/api/auth/jwks")
    assert response.status_code == 200
    data = response.json()
    assert "keys" in data
    assert len(data["keys"]) == 1
    key = data["keys"][0]
    assert key["alg"] == "EdDSA"
    assert key["crv"] == "Ed25519"
    assert "x" in key
    assert key["kty"] == "OKP"


def test_generate_and_verify_token():
    # 1. Get JWKS to get the public key 'x'
    jwks_response = client.get("/api/auth/jwks")
    assert jwks_response.status_code == 200
    x_value = jwks_response.json()["keys"][0]["x"]

    # 2. Generate a new Token
    payload = {"user_id": "test_123", "role": "admin"}
    gen_response = client.post(
        "/generate-token", json={"payload": payload, "expires_in_hours": 1}
    )
    assert gen_response.status_code == 200
    data = gen_response.json()
    assert data["success"] is True
    assert "token" in data
    token = data["token"]

    # 3. Verify the generated Token
    verify_response = client.post("/verify-token", json={"token": token, "x": x_value})
    assert verify_response.status_code == 200
    verify_data = verify_response.json()
    assert verify_data["valid"] is True
    assert verify_data["payload"]["user_id"] == "test_123"
    assert verify_data["payload"]["role"] == "admin"
    assert "exp" in verify_data["payload"]


def test_verify_invalid_token():
    # Attempt to verify a malformed token
    verify_response = client.post(
        "/verify-token", json={"token": "invalid.jwt.token", "x": "some_random_x_value"}
    )
    # Since we catch `InvalidTokenError` in the router, it should return 200 with valid=False
    if verify_response.status_code == 200:
        data = verify_response.json()
        assert data["valid"] is False
        assert "message" in data
    else:
        # In case the exception fallback kicks in
        assert verify_response.status_code == 400
