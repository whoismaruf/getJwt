import jwt
from fastapi import APIRouter, HTTPException
from app.schemas.token import TokenRequest, VerifyRequest
from app.core.security import get_jwk, create_jwt_token, verify_jwt_token

router = APIRouter()

@router.get("/api/auth/jwks")
async def jwks_endpoint():
    try:
        return get_jwk()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate-token")
async def generate_token(request: TokenRequest):
    try:
        token = create_jwt_token(request.payload, request.expires_in_hours)
        return {"success": True, "token": token}
    except Exception as e:
        print(f"Detailed Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/verify-token")
async def verify_token(request: VerifyRequest):
    try:
        decoded_payload = verify_jwt_token(request.token, request.x)
        return {
            "valid": True,
            "message": "Signature and payload verified!",
            "payload": decoded_payload,
        }
    except jwt.ExpiredSignatureError:
        return {"valid": False, "message": "Token has expired"}
    except jwt.InvalidTokenError as e:
        return {"valid": False, "message": f"Invalid token: {str(e)}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")
