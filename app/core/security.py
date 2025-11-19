from fastapi import HTTPException
import secrets

def generate_api_key():
    return secrets.token_urlsafe(32)

def validate_api_key(api_key: str):
    if not api_key or len(api_key) < 32:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True