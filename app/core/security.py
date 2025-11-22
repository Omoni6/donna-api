import jwt
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.config import settings

logger = logging.getLogger(__name__)

security_bearer = HTTPBearer()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log toutes les requêtes
        logger.info(f"{request.method} {request.url.path} - IP: {request.client.host}")
        
        # Vérifier les endpoints sensibles
        if any(path in request.url.path for path in ["/agents/execute", "/uploads", "/analytics"]):
            api_key = request.headers.get("X-API-Key")
            if not api_key or api_key != settings.API_KEY:
                logger.warning(f"API Key manquante ou invalide pour {request.url.path}")
                return Response(
                    content='{"error": "API Key requise"}',
                    status_code=401,
                    media_type="application/json"
                )
        
        response = await call_next(request)
        return response

def verify_jwt_token(credentials: HTTPAuthorizationCredentials = Security(security_bearer)) -> Dict[str, Any]:
    """Vérifie le token JWT NextAuth"""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        
        # Vérifier l'expiration
        if payload.get("exp") and datetime.fromtimestamp(payload["exp"]) < datetime.utcnow():
            raise HTTPException(status_code=401, detail="Token expiré")
        
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expiré")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Token invalide")

def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Vérifie l'API Key pour les services internes"""
    if not api_key:
        raise HTTPException(status_code=401, detail="API Key requise")
    
    if api_key != settings.API_KEY:
        logger.warning(f"API Key invalide fournie: {api_key[:10]}...")
        raise HTTPException(status_code=401, detail="API Key invalide")
    
    return api_key

def get_current_user(token_data: Dict[str, Any] = Depends(verify_jwt_token)) -> Dict[str, Any]:
    """Récupère l'utilisateur actuel depuis le token JWT"""
    user_id = token_data.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="User ID manquant dans le token")
    
    return {
        "id": user_id,
        "email": token_data.get("email"),
        "name": token_data.get("name"),
        "role": token_data.get("role", "user")
    }

def get_tenant_id(request: Request) -> str:
    """Récupère le tenant ID depuis les headers"""
    tenant_id = request.headers.get(settings.TENANT_ID_HEADER, settings.DEFAULT_TENANT)
    return tenant_id

def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Crée un token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=24)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    
    return encoded_jwt