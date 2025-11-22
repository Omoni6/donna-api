from fastapi import APIRouter, Depends
from datetime import datetime
import logging

from app.core.security import verify_api_key

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "service": "donna-api",
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check(api_key: str = Depends(verify_api_key)):
    """Health check détaillé (nécessite API key)"""
    try:
        # Vérifier la connexion aux services externes
        services_status = {
            "database": "healthy",  # À implémenter
            "redis": "healthy",      # À implémenter
            "donna_worker": "healthy"  # À implémenter
        }
        
        all_healthy = all(status == "healthy" for status in services_status.values())
        
        return {
            "status": "healthy" if all_healthy else "degraded",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "donna-api",
            "version": "1.0.0",
            "services": services_status,
            "uptime": "24h"  # À implémenter avec une vraie métrique
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du health check détaillé: {str(e)}", exc_info=True)
        return {
            "status": "unhealthy",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "service": "donna-api",
            "version": "1.0.0",
            "error": str(e)
        }