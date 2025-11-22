import logging
import json
from typing import Dict, Any, Optional

from app.models.payloads import TelegramWebhookPayload
from app.core.config import settings

logger = logging.getLogger(__name__)

class TelegramService:
    """Service pour gérer les webhooks Telegram"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.logger = logging.getLogger(__name__)
    
    async def process_webhook(self, payload: TelegramWebhookPayload) -> Dict[str, Any]:
        """
        Traite un webhook Telegram
        
        Args:
            payload: Données du webhook Telegram
        
        Returns:
            Dict contenant le résultat du traitement
        """
        try:
            self.logger.info(f"📨 Webhook Telegram reçu: {payload.update_id}")
            
            # Extraire les informations pertinentes
            message_info = self._extract_message_info(payload)
            
            if message_info:
                self.logger.info(f"💬 Message de {message_info['from_user']}: {message_info['text'][:50]}...")
                
                # Ici, on pourrait appeler un agent pour traiter le message
                # Par exemple, agent_zero_service pour une réponse intelligente
                
                return {
                    "status": "processed",
                    "update_id": payload.update_id,
                    "message_info": message_info,
                    "action": "message_received"
                }
            
            # Gérer d'autres types de mises à jour
            if payload.callback_query:
                return await self._handle_callback_query(payload.callback_query)
            
            if payload.inline_query:
                return await self._handle_inline_query(payload.inline_query)
            
            return {
                "status": "ignored",
                "update_id": payload.update_id,
                "reason": "No actionable content"
            }
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du traitement du webhook Telegram: {str(e)}", exc_info=True)
            return {
                "status": "error",
                "error": str(e)
            }
    
    def _extract_message_info(self, payload: TelegramWebhookPayload) -> Optional[Dict[str, Any]]:
        """Extrait les informations du message"""
        if not payload.message:
            return None
        
        message = payload.message
        
        return {
            "message_id": message.get("message_id"),
            "from_user": message.get("from", {}).get("username", "Unknown"),
            "user_id": message.get("from", {}).get("id"),
            "chat_id": message.get("chat", {}).get("id"),
            "text": message.get("text", ""),
            "date": message.get("date"),
            "chat_type": message.get("chat", {}).get("type")
        }
    
    async def _handle_callback_query(self, callback_query: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une callback query"""
        query_id = callback_query.get("id")
        from_user = callback_query.get("from", {}).get("username", "Unknown")
        data = callback_query.get("data", "")
        
        self.logger.info(f"🔘 Callback query de {from_user}: {data}")
        
        # Ici, on pourrait traiter la callback query
        # Par exemple, mettre à jour un état, envoyer une réponse, etc.
        
        return {
            "status": "processed",
            "query_id": query_id,
            "action": "callback_handled",
            "data": data
        }
    
    async def _handle_inline_query(self, inline_query: Dict[str, Any]) -> Dict[str, Any]:
        """Traite une inline query"""
        query_id = inline_query.get("id")
        from_user = inline_query.get("from", {}).get("username", "Unknown")
        query = inline_query.get("query", "")
        
        self.logger.info(f"🔍 Inline query de {from_user}: {query}")
        
        # Ici, on pourrait générer des résultats inline
        # Par exemple, rechercher dans une base de données, appeler une API, etc.
        
        return {
            "status": "processed",
            "query_id": query_id,
            "action": "inline_query_handled",
            "query": query
        }
    
    async def send_message(self, chat_id: int, text: str, 
                          parse_mode: str = "HTML", 
                          reply_markup: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Envoie un message via l'API Telegram
        
        Args:
            chat_id: ID du chat
            text: Texte du message
            parse_mode: Mode de parsing (HTML, Markdown)
            reply_markup: Clavier de réponse
        
        Returns:
            Réponse de l'API Telegram
        """
        if not self.bot_token:
            self.logger.warning("🤖 Token Telegram non configuré")
            return {"error": "Bot token not configured"}
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
            
            payload = {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": parse_mode
            }
            
            if reply_markup:
                payload["reply_markup"] = reply_markup
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                
                if response.status_code == 200:
                    self.logger.info(f"✅ Message envoyé au chat {chat_id}")
                    return response.json()
                else:
                    self.logger.error(f"❌ Erreur lors de l'envoi du message: {response.text}")
                    return {"error": response.text}
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de l'envoi du message Telegram: {str(e)}", exc_info=True)
            return {"error": str(e)}
    
    async def answer_callback_query(self, callback_query_id: str, 
                                   text: Optional[str] = None,
                                   show_alert: bool = False) -> Dict[str, Any]:
        """
        Répond à une callback query
        
        Args:
            callback_query_id: ID de la callback query
            text: Texte à afficher
            show_alert: Afficher une alerte
        
        Returns:
            Réponse de l'API Telegram
        """
        if not self.bot_token:
            return {"error": "Bot token not configured"}
        
        try:
            url = f"https://api.telegram.org/bot{self.bot_token}/answerCallbackQuery"
            
            payload = {
                "callback_query_id": callback_query_id,
                "show_alert": show_alert
            }
            
            if text:
                payload["text"] = text
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                
                if response.status_code == 200:
                    self.logger.info(f"✅ Callback query répondue: {callback_query_id}")
                    return response.json()
                else:
                    self.logger.error(f"❌ Erreur lors de la réponse à la callback: {response.text}")
                    return {"error": response.text}
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la réponse à la callback: {str(e)}", exc_info=True)
            return {"error": str(e)}

# Singleton instance
telegram_service = TelegramService()