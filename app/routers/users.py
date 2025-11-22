from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional, Dict, Any
import jwt
import logging
from datetime import datetime, timedelta
from ..models.user import User, UserCreateRequest, UserLoginResponse, UserLoginRequest, UserProfile
from ..core.config import settings
from ..core.security import verify_jwt_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

# Clé secrète pour JWT (dans la vraie vie, utiliser une clé plus sécurisée)
JWT_SECRET = settings.API_KEY
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

def create_jwt_token(user_id: str, email: str) -> str:
    """Créer un token JWT pour NextAuth"""
    payload = {
        "sub": user_id,
        "email": email,
        "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.utcnow()
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@router.post("/auth/signin", response_model=UserLoginResponse)
async def signin(credentials: Dict[str, Any]):
    """Endpoint de connexion compatible NextAuth"""
    try:
        email = credentials.get("email")
        password = credentials.get("password")
        
        if not email or not password:
            raise HTTPException(status_code=400, detail="Email et mot de passe requis")
        
        # Ici, vous devriez vérifier les identifiants dans votre base de données
        # Pour cette implémentation, nous utilisons un mock
        logger.info(f"Tentative de connexion pour: {email}")
        
        # Mock user - dans la vraie vie, vérifier en base de données
        if email == "admin@omoni.fr" and password == "admin123":
            user_id = "user_123456"
            token = create_jwt_token(user_id, email)
            
            logger.info(
                "Connexion réussie",
                extra={
                    "user_id": user_id,
                    "email": email,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )
            
            return UserLoginResponse(
                access_token=token,
                token_type="bearer",
                expires_in=JWT_EXPIRATION_HOURS * 3600,
                user={
                    "id": user_id,
                    "email": email,
                    "name": "Administrateur O'moni",
                    "image": None
                }
            )
        else:
            logger.warning(
                "Échec de connexion",
                extra={
                    "email": email,
                    "timestamp": datetime.utcnow().isoformat() + "Z"
                }
            )
            raise HTTPException(status_code=401, detail="Identifiants invalides")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors de la connexion: {str(e)}",
            extra={
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur serveur: {str(e)}")

@router.post("/auth/callback/credentials")
async def auth_callback(credentials: Dict[str, Any]):
    """Callback NextAuth pour l'authentification par identifiants"""
    try:
        # Cet endpoint est appelé par NextAuth après la soumission du formulaire
        return await signin(credentials)
        
    except Exception as e:
        logger.error(
            f"Erreur dans le callback auth: {str(e)}",
            extra={
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur callback: {str(e)}")

@router.get("/auth/session")
async def get_session(authorization: Optional[str] = Header(None)):
    """Récupérer la session utilisateur actuelle (NextAuth)"""
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")
        
        token = authorization.split(" ")[1]
        
        # Vérifier le token JWT
        payload = verify_jwt_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        logger.info(
            "Session récupérée",
            extra={
                "user_id": user_id,
                "email": email,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "user": {
                "id": user_id,
                "email": email,
                "name": "Utilisateur O'moni",
                "image": None
            },
            "expires": payload.get("exp")
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération de la session: {str(e)}",
            extra={
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur session: {str(e)}")

@router.post("/auth/signout")
async def signout():
    """Déconnexion de l'utilisateur (NextAuth)"""
    try:
        logger.info(
            "Déconnexion réussie",
            extra={
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return {
            "message": "Déconnexion réussie",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors de la déconnexion: {str(e)}",
            extra={
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur déconnexion: {str(e)}")

@router.get("/me", response_model=UserProfile)
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Récupérer les informations de l'utilisateur connecté"""
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")
        
        token = authorization.split(" ")[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        user_id = payload.get("sub")
        email = payload.get("email")
        
        # Mock user - dans la vraie vie, récupérer depuis la base de données
        user = UserProfile(
            id=user_id,
            email=email,
            name="Utilisateur O'moni",
            first_name=None,
            last_name=None,
            avatar=None,
            role="user",
            status="active",
            created_at=datetime.utcnow(),
            last_login=None,
            email_verified=True,
            preferences={},
            updated_at=datetime.utcnow()
        )
        
        logger.info(
            "Informations utilisateur récupérées",
            extra={
                "user_id": user_id,
                "email": email,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        return user
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors de la récupération de l'utilisateur: {str(e)}",
            extra={
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur utilisateur: {str(e)}")

@router.put("/me")
async def update_current_user(
    user_update: Dict[str, Any],
    authorization: Optional[str] = Header(None)
):
    """Mettre à jour les informations de l'utilisateur connecté"""
    try:
        if not authorization or not authorization.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Token manquant")
        
        token = authorization.split(" ")[1]
        payload = verify_jwt_token(token)
        
        if not payload:
            raise HTTPException(status_code=401, detail="Token invalide")
        
        user_id = payload.get("sub")
        
        logger.info(
            "Mise à jour utilisateur",
            extra={
                "user_id": user_id,
                "update_data": user_update,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        # Ici, vous devriez mettre à jour l'utilisateur en base de données
        # Pour cette implémentation, nous retournons un mock
        return {
            "id": user_id,
            "email": payload.get("email"),
            "name": user_update.get("name", "Utilisateur O'moni"),
            "image": user_update.get("image"),
            "updated_at": datetime.utcnow(),
            "message": "Utilisateur mis à jour avec succès"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Erreur lors de la mise à jour de l'utilisateur: {str(e)}",
            extra={
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur mise à jour: {str(e)}")