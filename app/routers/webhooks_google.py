from fastapi import APIRouter, HTTPException, Request, Depends
from typing import Dict, Any, Optional
import json
import logging
from datetime import datetime
from ..services.google_service import google_service
from ..core.security import get_tenant_id

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/webhooks/google", tags=["webhooks"])

@router.post("/calendar")
async def google_calendar_webhook(request: Request, tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Webhook pour les événements Google Calendar"""
    try:
        # Récupérer les headers importants
        headers = dict(request.headers)
        
        # Pour Google Calendar, le webhook est souvent une notification de changement
        # Le corps peut être vide, les détails sont récupérés via l'API
        body = await request.body()
        
        logger.info(
            "Google Calendar webhook reçu",
            extra={
                "tenant_id": tenant_id,
                "headers": headers,
                "body_size": len(body),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        # Traiter le webhook via le service Google
        result = await google_service.process_calendar_webhook(
            headers=headers,
            body=body.decode('utf-8') if body else "",
            tenant_id=tenant_id
        )
        
        return {
            "status": "success",
            "message": "Webhook Google Calendar traité",
            "result": result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors du traitement du webhook Google Calendar: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur webhook: {str(e)}")

@router.post("/gmail")
async def google_gmail_webhook(request: Request, tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Webhook pour les événements Gmail"""
    try:
        headers = dict(request.headers)
        body = await request.body()
        
        logger.info(
            "Gmail webhook reçu",
            extra={
                "tenant_id": tenant_id,
                "headers": headers,
                "body_size": len(body),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        # Traiter le webhook Gmail
        result = await google_service.process_gmail_webhook(
            headers=headers,
            body=body.decode('utf-8') if body else "",
            tenant_id=tenant_id
        )
        
        return {
            "status": "success", 
            "message": "Webhook Gmail traité",
            "result": result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors du traitement du webhook Gmail: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur webhook: {str(e)}")

@router.post("/drive")
async def google_drive_webhook(request: Request, tenant_id: Optional[str] = Depends(get_tenant_id)):
    """Webhook pour les événements Google Drive"""
    try:
        headers = dict(request.headers)
        body = await request.body()
        
        logger.info(
            "Google Drive webhook reçu",
            extra={
                "tenant_id": tenant_id,
                "headers": headers,
                "body_size": len(body),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        # Traiter le webhook Google Drive
        result = await google_service.process_drive_webhook(
            headers=headers,
            body=body.decode('utf-8') if body else "",
            tenant_id=tenant_id
        )
        
        return {
            "status": "success",
            "message": "Webhook Google Drive traité", 
            "result": result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors du traitement du webhook Google Drive: {str(e)}",
            extra={
                "tenant_id": tenant_id,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur webhook: {str(e)}")

@router.get("/verify")
async def verify_google_webhook(request: Request):
    """Endpoint pour vérifier la validité du domaine pour Google Webhooks"""
    try:
        # Google vérifie souvent le domaine avec une requête GET
        headers = dict(request.headers)
        
        logger.info(
            "Vérification Google webhook",
            extra={
                "headers": headers,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        
        # Retourner une réponse de vérification
        return {
            "status": "verified",
            "message": "Domaine vérifié pour Google Webhooks",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
    except Exception as e:
        logger.error(
            f"Erreur lors de la vérification Google webhook: {str(e)}",
            extra={
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        )
        raise HTTPException(status_code=500, detail=f"Erreur vérification: {str(e)}")