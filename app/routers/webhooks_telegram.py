from fastapi import APIRouter, HTTPException, Header, Request
from typing import Dict, Any
import logging

from app.models.payloads import TelegramWebhookPayload
from app.services.telegram_service import telegram_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/telegram")
async def telegram_webhook(
    request: Request,
    payload: TelegramWebhookPayload,
    x_telegram_bot_api_secret_token: str = Header(None, alias="X-Telegram-Bot-Api-Secret-Token")
):
    """
    Webhook pour recevoir les mises à jour de Telegram
    
    Args:
        request: Requête HTTP
        payload: Données du webhook Telegram
        x_telegram_bot_api_secret_token: Token secret pour la sécurité
    
    Returns:
        Résultat du traitement
    """
    try:
        logger.info(f"📨 Webhook Telegram reçu: Update ID {payload.update_id}")
        
        # Vérifier le token secret si configuré
        # if settings.TELEGRAM_SECRET_TOKEN and x_telegram_bot_api_secret_token != settings.TELEGRAM_SECRET_TOKEN:
        #     logger.warning("❌ Token secret Telegram invalide")
        #     raise HTTPException(status_code=401, detail="Token invalide")
        
        # Traiter le webhook
        result = await telegram_service.process_webhook(payload)
        
        logger.info(f"✅ Webhook Telegram traité avec succès: {result.get('status', 'unknown')}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement du webhook Telegram: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@router.get("/telegram")
async def telegram_webhook_verification(request: Request):
    """
    Endpoint pour la vérification du webhook Telegram
    
    Args:
        request: Requête HTTP
    
    Returns:
        Confirmation de disponibilité
    """
    try:
        logger.info("🔍 Vérification du webhook Telegram")
        
        # Telegram envoie parfois une requête GET pour vérifier le webhook
        return {
            "status": "ready",
            "message": "Webhook Telegram prêt à recevoir des mises à jour",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification du webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification: {str(e)}")