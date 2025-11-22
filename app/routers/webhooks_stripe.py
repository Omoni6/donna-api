from fastapi import APIRouter, HTTPException, Header, Request
from typing import Dict, Any
import logging

from app.models.payloads import StripeWebhookPayload
from app.services.stripe_service import stripe_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None, alias="Stripe-Signature")
):
    """
    Webhook pour recevoir les événements Stripe
    
    Args:
        request: Requête HTTP
        stripe_signature: Signature Stripe pour la vérification
    
    Returns:
        Résultat du traitement
    """
    try:
        # Récupérer le corps brut de la requête
        body = await request.body()
        
        # Parser le JSON
        import json
        payload_dict = json.loads(body)
        
        # Créer l'objet payload
        payload = StripeWebhookPayload(**payload_dict)
        
        logger.info(f"💳 Webhook Stripe reçu: {payload.type} - {payload.id}")
        
        # Traiter le webhook
        result = await stripe_service.process_webhook(payload, stripe_signature)
        
        logger.info(f"✅ Webhook Stripe traité avec succès: {result.get('status', 'unknown')}")
        
        return result
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Erreur de parsing JSON Stripe: {str(e)}")
        raise HTTPException(status_code=400, detail="Payload JSON invalide")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur lors du traitement du webhook Stripe: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors du traitement: {str(e)}")

@router.get("/stripe")
async def stripe_webhook_verification():
    """
    Endpoint pour la vérification du webhook Stripe
    
    Returns:
        Confirmation de disponibilité
    """
    try:
        logger.info("🔍 Vérification du webhook Stripe")
        
        return {
            "status": "ready",
            "message": "Webhook Stripe prêt à recevoir des événements",
            "timestamp": "2024-01-01T00:00:00Z"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la vérification du webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur lors de la vérification: {str(e)}")