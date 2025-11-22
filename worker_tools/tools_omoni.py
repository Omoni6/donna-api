#!/usr/bin/env python3
"""
Tools OMONI pour Donna Worker
Ces tools permettent au Worker d'appeler les endpoints FastAPI OMONI
"""

import httpx
import os
import json
import logging
from typing import Dict, Any, Optional, List
from datetime import datetime

logger = logging.getLogger(__name__)

class OmoniTools:
    """Classe pour interagir avec l'API OMONI depuis Donna Worker"""
    
    def __init__(self):
        self.api_url = os.getenv("OMONI_API_URL", "http://donna-api:8000")
        self.api_key = os.getenv("OMONI_API_KEY", "donna-api-key-production")
        self.timeout = 30.0
        self.logger = logging.getLogger(__name__)
        
        # URLs des services
        self.calendar_url = f"{self.api_url}{os.getenv('OMONI_CALENDAR_URL', '/api/v1/omoni/calendar')}"
        self.crm_url = f"{self.api_url}{os.getenv('OMONI_CRM_URL', '/api/v1/omoni/crm')}"
        self.chat_url = f"{self.api_url}{os.getenv('OMONI_CHAT_URL', '/api/v1/omoni/chat')}"
        self.bucket_url = f"{self.api_url}{os.getenv('OMONI_BUCKET_URL', '/api/v1/omoni/bucket')}"
        self.slack_url = f"{self.api_url}{os.getenv('OMONI_SLACK_URL', '/api/v1/omoni/slack')}"
        self.notifications_url = f"{self.api_url}{os.getenv('OMONI_NOTIFICATIONS_URL', '/api/v1/omoni/notifications')}"
        self.workflows_url = f"{self.api_url}{os.getenv('OMONI_WORKFLOWS_URL', '/api/v1/omoni/workflows')}"
        self.analytics_url = f"{self.api_url}{os.getenv('OMONI_ANALYTICS_URL', '/api/v1/omoni/analytics')}"
    
    def _get_headers(self, tenant_id: Optional[str] = None) -> Dict[str, str]:
        """Obtenir les headers pour les requêtes"""
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key
        }
        if tenant_id:
            headers["X-Tenant-ID"] = tenant_id
        return headers
    
    async def create_calendar_event(self, event_data: Dict[str, Any], tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Créer un événement dans le calendrier OMONI"""
        try:
            self.logger.info(f"📅 Création d'événement calendrier: {event_data.get('title', 'Sans titre')}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.calendar_url}/events",
                    json=event_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Événement créé: {result.get('data', {}).get('id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur création événement: {str(e)}")
            raise
    
    async def get_calendar_events(self, tenant_id: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """Récupérer les événements du calendrier"""
        try:
            self.logger.info(f"📅 Récupération des événements calendrier")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.calendar_url}/events?limit={limit}",
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    events = result.get('data', [])
                    self.logger.info(f"✅ {len(events)} événements récupérés")
                    return events
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération événements: {str(e)}")
            raise
    
    async def create_slack_channel(self, channel_name: str, description: Optional[str] = None, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Créer un canal Slack"""
        try:
            self.logger.info(f"💬 Création du canal Slack: {channel_name}")
            
            channel_data = {
                "name": channel_name,
                "description": description or f"Canal créé par Donna Worker"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.slack_url}/create-channel",
                    json=channel_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Canal Slack créé: {result.get('data', {}).get('id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur création canal Slack: {str(e)}")
            raise
    
    async def send_slack_message(self, channel: str, text: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Envoyer un message Slack"""
        try:
            self.logger.info(f"💬 Envoi message Slack au canal {channel}")
            
            message_data = {
                "channel": channel,
                "text": text,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.slack_url}/send-message",
                    json=message_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Message Slack envoyé: {result.get('data', {}).get('id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi message Slack: {str(e)}")
            raise
    
    async def upload_to_bucket(self, filename: str, content: str, content_type: str = "text/plain", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Uploader un fichier vers le bucket OMONI"""
        try:
            self.logger.info(f"📁 Upload du fichier vers bucket: {filename}")
            
            file_data = {
                "filename": filename,
                "content": content,
                "content_type": content_type,
                "size": len(content.encode('utf-8'))
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.bucket_url}/upload",
                    json=file_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Fichier uploadé: {result.get('data', {}).get('id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur upload fichier: {str(e)}")
            raise
    
    async def create_crm_lead(self, email: str, name: str, phone: Optional[str] = None, source: str = "Donna Worker", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Créer un lead dans le CRM"""
        try:
            self.logger.info(f"👤 Création lead CRM: {name} ({email})")
            
            lead_data = {
                "email": email,
                "name": name,
                "phone": phone,
                "source": source,
                "created_at": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.crm_url}/leads",
                    json=lead_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Lead CRM créé: {result.get('data', {}).get('id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur création lead CRM: {str(e)}")
            raise
    
    async def get_crm_leads(self, status: Optional[str] = None, tenant_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Récupérer les leads du CRM"""
        try:
            self.logger.info(f"👤 Récupération des leads CRM")
            
            params = {}
            if status:
                params["status"] = status
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.crm_url}/leads",
                    params=params,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    leads = result.get('data', [])
                    self.logger.info(f"✅ {len(leads)} leads récupérés")
                    return leads
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération leads CRM: {str(e)}")
            raise
    
    async def send_chat_message(self, message: str, sender: str = "Donna Worker", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Envoyer un message dans le chat"""
        try:
            self.logger.info(f"💬 Envoi message chat: {message[:50]}...")
            
            message_data = {
                "message": message,
                "sender": sender,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.chat_url}/send",
                    json=message_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Message chat envoyé: {result.get('data', {}).get('id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi message chat: {str(e)}")
            raise
    
    async def send_notification(self, title: str, message: str, notification_type: str = "info", tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Envoyer une notification"""
        try:
            self.logger.info(f"🔔 Envoi notification: {title}")
            
            notification_data = {
                "title": title,
                "message": message,
                "type": notification_type,
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.notifications_url}/send",
                    json=notification_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Notification envoyée: {result.get('data', {}).get('id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi notification: {str(e)}")
            raise
    
    async def execute_workflow(self, workflow_id: str, parameters: Optional[Dict[str, Any]] = None, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Exécuter un workflow"""
        try:
            self.logger.info(f"⚙️ Exécution du workflow: {workflow_id}")
            
            workflow_data = {
                "workflow_id": workflow_id,
                "parameters": parameters or {},
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.workflows_url}/execute",
                    json=workflow_data,
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Workflow exécuté: {result.get('data', {}).get('workflow_id')}")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur exécution workflow: {str(e)}")
            raise
    
    async def get_analytics_dashboard(self, tenant_id: Optional[str] = None) -> Dict[str, Any]:
        """Récupérer le dashboard analytics"""
        try:
            self.logger.info(f"📊 Récupération du dashboard analytics")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.analytics_url}/dashboard",
                    headers=self._get_headers(tenant_id)
                )
                
                if response.status_code == 200:
                    result = response.json()
                    self.logger.info(f"✅ Dashboard analytics récupéré")
                    return result.get('data', {})
                else:
                    error_msg = f"Erreur {response.status_code}: {response.text}"
                    self.logger.error(f"❌ {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération dashboard: {str(e)}")
            raise

# Instance singleton
omoni_tools = OmoniTools()

# ===== FONCTIONS UTILITAIRES POUR LES AGENTS =====

async def create_meeting_event(title: str, start_time: str, end_time: str, description: Optional[str] = None, tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Créer un événement de réunion"""
    event_data = {
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "description": description or f"Réunion: {title}"
    }
    return await omoni_tools.create_calendar_event(event_data, tenant_id)

async def create_client_lead(email: str, name: str, phone: Optional[str] = None, source: str = "Agent Conversation", tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Créer un lead client"""
    return await omoni_tools.create_crm_lead(email, name, phone, source, tenant_id)

async def notify_team(message: str, title: str = "Notification Donna", tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Notifier l'équipe"""
    return await omoni_tools.send_notification(title, message, "info", tenant_id)

async def create_project_channel(project_name: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Créer un canal Slack pour un projet"""
    channel_name = project_name.lower().replace(" ", "-")
    return await omoni_tools.create_slack_channel(channel_name, f"Canal pour le projet {project_name}", tenant_id)

async def log_activity(activity: str, tenant_id: Optional[str] = None) -> Dict[str, Any]:
    """Logger une activité dans le chat"""
    return await omoni_tools.send_chat_message(activity, "Donna Worker", tenant_id)

# Export des fonctions
__all__ = [
    "OmoniTools",
    "omoni_tools",
    "create_meeting_event",
    "create_client_lead", 
    "notify_team",
    "create_project_channel",
    "log_activity"
]