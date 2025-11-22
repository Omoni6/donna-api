from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/")
async def root():
    """Endpoint racine de l'API"""
    return {
        "message": "🚀 Donna API - Architecture O'moni",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/api/docs",
        "health": "/api/health"
    }

@router.get("/api/version")
async def get_version():
    """Récupère la version de l'API"""
    return {
        "version": settings.APP_VERSION,
        "name": settings.APP_NAME,
        "environment": "production" if not settings.DEBUG else "development"
    }