#!/usr/bin/env python3
"""
Tools pour les agents Donna Worker
Ces tools permettent aux agents d'interagir avec les services externes
"""

import httpx
import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class AgentTools:
    """Classe pour les outils spécifiques aux agents"""
    
    def __init__(self):
        self.api_url = os.getenv("DONNA_API_URL", "http://donna-api:8000")
        self.api_key = os.getenv("DONNA_API_KEY", "donna-api-key-production")
        self.timeout = 30.0
        self.logger = logging.getLogger(__name__)
        
        # URLs des services
        self.telegram_url = f"{self.api_url}/api/v1/webhooks/telegram"
        self.stripe_url = f"{self.api_url}/api/v1/webhooks/stripe"
        self.google_url = f"{self.api_url}/api/v1/webhooks/google"
        self.analytics_url = f"{self.api_url}/api/v1/analytics"
    
    def _get_headers(self, tenant_id: Optional[str] = None) -> Dict[str, str]:
        """Obtenir les headers pour les requêtes"""
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id
        return headers
    
    async def send_telegram_message(self, chat_id: str, message: str, parse_mode: str = "HTML", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Envoyer un message Telegram"""
        try:
            self.logger.info(f"📱 Envoi message Telegram à {chat_id}")
            
            message_data = {
                "chat_id": chat_id,
                "text": message,
                "parse_mode": parse_mode,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.telegram_url}/send-message",
                    json=message_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Message Telegram envoyé")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi message Telegram: {str(e)}")
            raise
    
    async def create_stripe_payment(self, amount: int, currency: str = "eur", description: Optional[str] = None, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Créer un paiement Stripe"""
        try:
            self.logger.info(f"💳 Création paiement Stripe: {amount} {currency}")
            
            payment_data = {
                "amount": amount,
                "currency": currency,
                "description": description or "Paiement via Donna Worker",
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.stripe_url}/create-payment",
                    json=payment_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Paiement Stripe créé")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur création paiement Stripe: {str(e)}")
            raise
    
    async def track_analytics_event(self, event_type: str, event_data: Dict[str, Any], tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Tracker un événement analytics"""
        try:
            self.logger.info(f"📊 Tracking événement: {event_type}")
            
            analytics_data = {
                "event_type": event_type,
                "event_data": event_data,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.analytics_url}/events",
                    json=analytics_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Événement analytics tracké")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur tracking analytics: {str(e)}")
            raise
    
    async def get_analytics_insights(self, metric: str, timeframe: str = "7d", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Obtenir des insights analytics"""
        try:
            self.logger.info(f"📊 Récupération insights: {metric} ({timeframe})")
            
            params = {
                "metric": metric,
                "timeframe": timeframe
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.analytics_url}/insights",
                    params=params,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Insights analytics récupérés")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération insights: {str(e)}")
            raise
    
    async def process_google_webhook(self, webhook_data: Dict[str, Any], tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Traiter un webhook Google"""
        try:
            self.logger.info(f"🔍 Traitement webhook Google")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.google_url}/process",
                    json=webhook_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Webhook Google traité")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur traitement webhook Google: {str(e)}")
            raise

# Instance singleton
agent_tools = AgentTools()

# ===== FONCTIONS UTILITAIRES POUR LES AGENTS SPÉCIFIQUES =====

async def planifi_agent_task(task_description: str, deadline: str, priority: str = "medium", tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Tâche spécifique pour l'agent Planifi"""
    try:
        logger.info(f"📅 Planification tâche: {task_description}")
        
        # Créer un événement calendrier
        from .tools_omoni import create_meeting_event
        event_data = await create_meeting_event(
            title=f"Tâche: {task_description}",
            start_time=deadline,
            end_time=deadline,
            description=f"Tâche planifiée avec priorité {priority}",
            tenant_id=tenant_id
        )
        
        # Tracker l'événement
        await agent_tools.track_analytics_event(
            "task_planned",
            {
                "task_description": task_description,
                "deadline": deadline,
                "priority": priority,
                "event_id": event_data.get("id")
            },
            tenant_id
        )
        
        logger.info(f"✅ Tâche planifiée avec succès")
        return event_data
        
    except Exception as e:
        logger.error(f"❌ Erreur planification tâche: {str(e)}")
        raise

async def publie_agent_task(content: str, platform: str = "telegram", target_audience: Optional[str] = None, tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Tâche spécifique pour l'agent Publie"""
    try:
        logger.info(f"📢 Publication contenu sur {platform}")
        
        if platform == "telegram":
            # Utiliser un chat ID par défaut ou spécifique
            chat_id = target_audience or os.getenv("DEFAULT_TELEGRAM_CHAT_ID", "-1001234567890")
            result = await agent_tools.send_telegram_message(
                chat_id=chat_id,
                message=content,
                tenant_id=tenant_id
            )
        else:
            raise ValueError(f"Plateforme non supportée: {platform}")
        
        # Tracker l'événement
        await agent_tools.track_analytics_event(
            "content_published",
            {
                "platform": platform,
                "content_length": len(content),
                "target_audience": target_audience,
                "message_id": result.get("message_id")
            },
            tenant_id
        )
        
        logger.info(f"✅ Contenu publié avec succès")
        return result
        
    except Exception as e:
        logger.error(f"❌ Erreur publication contenu: {str(e)}")
        raise

async def cree_agent_task(creation_type: str, specifications: Dict[str, Any], tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Tâche spécifique pour l'agent Cree"""
    try:
        logger.info(f"🎨 Création {creation_type}")
        
        if creation_type == "document":
            # Créer un document dans le bucket
            from .tools_omoni import omoni_tools
            filename = specifications.get("filename", f"document_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt")
            content = specifications.get("content", "Document créé par Donna Worker")
            
            result = await omoni_tools.upload_to_bucket(
                filename=filename,
                content=content,
                content_type="text/plain",
                tenant_id=tenant_id
            )
            
        elif creation_type == "channel":
            # Créer un canal Slack
            from .tools_omoni import create_project_channel
            result = await create_project_channel(
                project_name=specifications.get("name", "Nouveau Projet"),
                tenant_id=tenant_id
            )
            
        else:
            raise ValueError(f"Type de création non supporté: {creation_type}")
        
        # Tracker l'événement
        await agent_tools.track_analytics_event(
            "creation_completed",
            {
                "creation_type": creation_type,
                "specifications": specifications,
                "result_id": result.get("id")
            },
            tenant_id
        )
        
        logger.info(f"✅ Création terminée avec succès")
        return result
        
    except Exception as e:
        logger.error(f"❌ Erreur création: {str(e)}")
        raise

async def commercial_agent_task(action: str, client_data: Dict[str, Any], tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Tâche spécifique pour l'agent Commercial"""
    try:
        logger.info(f"💼 Action commerciale: {action}")
        
        if action == "create_lead":
            # Créer un lead dans le CRM
            from .tools_omoni import create_client_lead
            result = await create_client_lead(
                email=client_data.get("email"),
                name=client_data.get("name"),
                phone=client_data.get("phone"),
                source="Agent Commercial",
                tenant_id=tenant_id
            )
            
        elif action == "create_payment":
            # Créer un paiement Stripe
            result = await agent_tools.create_stripe_payment(
                amount=client_data.get("amount", 0),
                currency=client_data.get("currency", "eur"),
                description=client_data.get("description"),
                tenant_id=tenant_id
            )
            
        elif action == "send_proposal":
            # Envoyer une proposition par Telegram
            message = f"🎯 Nouvelle proposition pour {client_data.get('name', 'Client')}: {client_data.get('proposal', 'Proposition')}\n\nContact: {client_data.get('email', 'Email non fourni')}"
            result = await agent_tools.send_telegram_message(
                chat_id=client_data.get("telegram_chat_id", os.getenv("DEFAULT_TELEGRAM_CHAT_ID", "-1001234567890")),
                message=message,
                tenant_id=tenant_id
            )
            
        else:
            raise ValueError(f"Action commerciale non supportée: {action}")
        
        # Tracker l'événement
        await agent_tools.track_analytics_event(
            "commercial_action_completed",
            {
                "action": action,
                "client_data": client_data,
                "result_id": result.get("id")
            },
            tenant_id
        )
        
        logger.info(f"✅ Action commerciale terminée avec succès")
        return result
        
    except Exception as e:
        logger.error(f"❌ Erreur action commerciale: {str(e)}")
        raise

# Export des fonctions
__all__ = [
    "AgentTools",
    "agent_tools",
    "planifi_agent_task",
    "publie_agent_task", 
    "cree_agent_task",
    "commercial_agent_task"
]