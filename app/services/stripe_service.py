import logging
import stripe
from typing import Dict, Any, Optional

from app.models.payloads import StripeWebhookPayload
from app.core.config import settings

logger = logging.getLogger(__name__)

class StripeService:
    """Service pour gérer les webhooks Stripe"""
    
    def __init__(self):
        self.stripe_secret_key = settings.STRIPE_SECRET_KEY
        self.webhook_secret = settings.STRIPE_WEBHOOK_SECRET
        
        if self.stripe_secret_key:
            stripe.api_key = self.stripe_secret_key
        
        self.logger = logging.getLogger(__name__)
    
    async def process_webhook(self, payload: StripeWebhookPayload, signature: str) -> Dict[str, Any]:
        """
        Traite un webhook Stripe
        
        Args:
            payload: Données du webhook Stripe
            signature: Signature du webhook pour vérification
        
        Returns:
            Dict contenant le résultat du traitement
        """
        try:
            self.logger.info(f"💳 Webhook Stripe reçu: {payload.type} - {payload.id}")
            
            # Vérifier la signature si configurée
            if self.webhook_secret and signature:
                try:
                    stripe.Webhook.construct_event(
                        payload=json.dumps(payload.dict()),
                        sig_header=signature,
                        secret=self.webhook_secret
                    )
                    self.logger.info("✅ Signature Stripe vérifiée")
                except stripe.error.SignatureVerificationError as e:
                    self.logger.error(f"❌ Signature Stripe invalide: {str(e)}")
                    return {
                        "status": "error",
                        "error": "Signature invalide"
                    }
            
            # Traiter l'événement selon son type
            event_type = payload.type
            
            if event_type == "payment_intent.succeeded":
                return await self._handle_payment_intent_succeeded(payload)
            
            elif event_type == "payment_intent.payment_failed":
                return await self._handle_payment_intent_failed(payload)
            
            elif event_type == "customer.subscription.created":
                return await self._handle_subscription_created(payload)
            
            elif event_type == "customer.subscription.updated":
                return await self._handle_subscription_updated(payload)
            
            elif event_type == "customer.subscription.deleted":
                return await self._handle_subscription_deleted(payload)
            
            elif event_type == "invoice.payment_succeeded":
                return await self._handle_invoice_payment_succeeded(payload)
            
            elif event_type == "invoice.payment_failed":
                return await self._handle_invoice_payment_failed(payload)
            
            elif event_type == "checkout.session.completed":
                return await self._handle_checkout_session_completed(payload)
            
            else:
                self.logger.info(f"📋 Événement Stripe non traité: {event_type}")
                return {
                    "status": "ignored",
                    "event_id": payload.id,
                    "event_type": event_type,
                    "reason": "Event type not handled"
                }
                
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du traitement du webhook Stripe: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    async def _handle_payment_intent_succeeded(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite un paiement réussi"""
        payment_intent = payload.data.get("object", {})
        amount = payment_intent.get("amount")
        currency = payment_intent.get("currency")
        customer_id = payment_intent.get("customer")
        
        self.logger.info(f"💰 Paiement réussi: {amount} {currency} - Customer: {customer_id}")
        
        # Ici, on pourrait:
        # - Mettre à jour la base de données
        # - Envoyer un email de confirmation
        # - Activer un service
        # - Appeler un agent pour traiter le paiement
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "payment_succeeded",
            "amount": amount,
            "currency": currency,
            "customer_id": customer_id
        }
    
    async def _handle_payment_intent_failed(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite un paiement échoué"""
        payment_intent = payload.data.get("object", {})
        customer_id = payment_intent.get("customer")
        error = payment_intent.get("last_payment_error", {})
        
        self.logger.warning(f"❌ Paiement échoué - Customer: {customer_id}, Error: {error.get('message')}")
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "payment_failed",
            "customer_id": customer_id,
            "error": error
        }
    
    async def _handle_subscription_created(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite la création d'un abonnement"""
        subscription = payload.data.get("object", {})
        customer_id = subscription.get("customer")
        subscription_id = subscription.get("id")
        status = subscription.get("status")
        
        self.logger.info(f"🎉 Abonnement créé: {subscription_id} - Customer: {customer_id} - Status: {status}")
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "subscription_created",
            "subscription_id": subscription_id,
            "customer_id": customer_id,
            "status": status
        }
    
    async def _handle_subscription_updated(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite la mise à jour d'un abonnement"""
        subscription = payload.data.get("object", {})
        customer_id = subscription.get("customer")
        subscription_id = subscription.get("id")
        previous_attributes = payload.data.get("previous_attributes", {})
        
        self.logger.info(f"🔄 Abonnement mis à jour: {subscription_id} - Customer: {customer_id}")
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "subscription_updated",
            "subscription_id": subscription_id,
            "customer_id": customer_id,
            "previous_attributes": previous_attributes
        }
    
    async def _handle_subscription_deleted(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite la suppression d'un abonnement"""
        subscription = payload.data.get("object", {})
        customer_id = subscription.get("customer")
        subscription_id = subscription.get("id")
        
        self.logger.info(f"🗑️ Abonnement supprimé: {subscription_id} - Customer: {customer_id}")
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "subscription_deleted",
            "subscription_id": subscription_id,
            "customer_id": customer_id
        }
    
    async def _handle_invoice_payment_succeeded(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite un paiement de facture réussi"""
        invoice = payload.data.get("object", {})
        customer_id = invoice.get("customer")
        amount_paid = invoice.get("amount_paid")
        invoice_id = invoice.get("id")
        
        self.logger.info(f"📄 Paiement de facture réussi: {invoice_id} - {amount_paid} - Customer: {customer_id}")
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "invoice_payment_succeeded",
            "invoice_id": invoice_id,
            "customer_id": customer_id,
            "amount_paid": amount_paid
        }
    
    async def _handle_invoice_payment_failed(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite un paiement de facture échoué"""
        invoice = payload.data.get("object", {})
        customer_id = invoice.get("customer")
        invoice_id = invoice.get("id")
        
        self.logger.warning(f"📄 Paiement de facture échoué: {invoice_id} - Customer: {customer_id}")
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "invoice_payment_failed",
            "invoice_id": invoice_id,
            "customer_id": customer_id
        }
    
    async def _handle_checkout_session_completed(self, payload: StripeWebhookPayload) -> Dict[str, Any]:
        """Traite une session de checkout complétée"""
        session = payload.data.get("object", {})
        customer_id = session.get("customer")
        session_id = session.get("id")
        payment_status = session.get("payment_status")
        
        self.logger.info(f"🛒 Session de checkout complétée: {session_id} - Customer: {customer_id} - Status: {payment_status}")
        
        return {
            "status": "processed",
            "event_id": payload.id,
            "event_type": payload.type,
            "action": "checkout_session_completed",
            "session_id": session_id,
            "customer_id": customer_id,
            "payment_status": payment_status
        }
    
    async def create_customer(self, email: str, metadata: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Crée un client Stripe"""
        try:
            customer = stripe.Customer.create(
                email=email,
                metadata=metadata or {}
            )
            
            self.logger.info(f"👤 Client Stripe créé: {customer.id} - {email}")
            
            return {
                "customer_id": customer.id,
                "email": email,
                "status": "created"
            }
            
        except stripe.error.StripeError as e:
            self.logger.error(f"❌ Erreur lors de la création du client Stripe: {str(e)}")
            return {"error": str(e)}
    
    async def create_checkout_session(self, customer_id: str, price_id: str, 
                                    success_url: str, cancel_url: str) -> Dict[str, Any]:
        """Crée une session de checkout"""
        try:
            session = stripe.checkout.Session.create(
                customer=customer_id,
                payment_method_types=["card"],
                line_items=[{"price": price_id, "quantity": 1}],
                mode="subscription",
                success_url=success_url,
                cancel_url=cancel_url
            )
            
            self.logger.info(f"🛒 Session de checkout créée: {session.id} - Customer: {customer_id}")
            
            return {
                "session_id": session.id,
                "url": session.url,
                "status": "created"
            }
            
        except stripe.error.StripeError as e:
            self.logger.error(f"❌ Erreur lors de la création de la session: {str(e)}")
            return {"error": str(e)}

# Singleton instance
stripe_service = StripeService()