from pydantic import BaseModel, Field

class TokenRequest(BaseModel):
    payload: dict = Field(
        ...,
        examples=[{"user_id": "12345", "role": "admin", "email": "maruf@example.com"}],
        description="The custom data you want to include in the JWT",
    )
    expires_in_hours: int = Field(
        default=2, examples=[2], description="How many hours until the token expires"
    )

class VerifyRequest(BaseModel):
    token: str
    x: str  # The public key string from your /jwks
