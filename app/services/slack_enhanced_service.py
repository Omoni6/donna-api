#!/usr/bin/env python3
"""
Service Slack amélioré avec création de channels
"""

import logging
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

class SlackEnhancedService:
    """Service Slack avec support création de channels et gestion avancée"""
    
    def __init__(self):
        self.bot_token = settings.SLACK_BOT_TOKEN
        self.signing_secret = settings.SLACK_SIGNING_SECRET
        self.app_id = settings.SLACK_APP_ID
        self.api_base = "https://slack.com/api"
        self.timeout = 30.0
        self.logger = logging.getLogger(__name__)
    
    def _get_headers(self) -> Dict[str, str]:
        """Obtenir les headers pour les requêtes Slack"""
        return {
            "Authorization": f"Bearer {self.bot_token}",
            "Content-Type": "application/json"
        }
    
    async def create_channel(self, channel_name: str, private: bool = False, 
                           description: Optional[str] = None, workspace_id: Optional[str] = None) -> Dict[str, Any]:
        """Créer un channel Slack"""
        try:
            self.logger.info(f"💬 Création channel Slack: {channel_name} (private: {private})")
            
            # Nettoyer le nom du channel (remplacer espaces par tirets, en minuscule)
            clean_name = channel_name.lower().replace(" ", "-").replace("_", "-")
            if not clean_name.startswith("#"):
                clean_name = f"#{clean_name}"
            
            # Enlever le # pour l'API et s'assurer que le nom est valide
            api_name = clean_name.lstrip("#")
            
            self.logger.info(f"📋 Channel name original: {channel_name}")
            self.logger.info(f"📋 Channel name nettoyé: {clean_name}")
            self.logger.info(f"📋 Channel name pour API: {api_name}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                create_data = {
                    "name": api_name,
                    "is_private": private
                }
                
                if description:
                    create_data["description"] = description
                
                self.logger.info(f"📤 Données envoyées à Slack API: {create_data}")
                
                response = await client.post(
                    f"{self.api_base}/conversations.create",
                    json=create_data,
                    headers=self._get_headers()
                )
                
                self.logger.info(f"📊 Status code: {response.status_code}")
                self.logger.info(f"📨 Response: {response.text}")
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        channel_info = result["channel"]
                        
                        self.logger.info(f"✅ Channel Slack créé: {channel_info.get('id')}")
                        return {
                            "channel_id": channel_info.get("id"),
                            "channel_name": channel_info.get("name"),
                            "private": channel_info.get("is_private", private),
                            "created": channel_info.get("created"),
                            "description": description,
                            "workspace_id": workspace_id
                        }
                    else:
                        error_msg = result.get("error", "Erreur inconnue")
                        self.logger.error(f"❌ Erreur Slack: {error_msg}")
                        
                        # Gestion des erreurs spécifiques Slack
                        if error_msg == "missing_scope":
                            raise Exception(
                                f"Slack API error: {error_msg}. "
                                "Le bot n'a pas les permissions nécessaires. "
                                "Vérifiez que votre bot a les scopes: channels:manage, groups:write, "
                                "channels:write, conversations.create"
                            )
                        elif error_msg == "name_taken":
                            raise Exception(
                                f"Slack API error: {error_msg}. "
                                f"Le nom de canal '{api_name}' est déjà utilisé. "
                                "Essayez un nom différent."
                            )
                        elif error_msg == "invalid_name":
                            raise Exception(
                                f"Slack API error: {error_msg}. "
                                f"Le nom de canal '{api_name}' n'est pas valide. "
                                "Les noms de canal doivent être en minuscules, sans espaces, "
                                "et peuvent contenir des lettres, chiffres, tirets et underscores."
                            )
                        else:
                            raise Exception(f"Slack API error: {error_msg}")
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur création channel Slack: {str(e)}")
            raise
    
    async def add_member_to_channel(self, channel_id: str, user_email: str, workspace_id: Optional[str] = None) -> Dict[str, Any]:
        """Ajouter un membre à un channel Slack"""
        try:
            self.logger.info(f"💬 Ajout membre {user_email} au channel {channel_id}")
            
            # Étape 1: Obtenir l'ID utilisateur à partir de l'email
            user_id = await self._get_user_id_by_email(user_email)
            if not user_id:
                raise Exception(f"Utilisateur non trouvé avec l'email: {user_email}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                invite_data = {
                    "channel": channel_id,
                    "users": user_id
                }
                
                response = await client.post(
                    f"{self.api_base}/conversations.invite",
                    json=invite_data,
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        self.logger.info(f"✅ Membre {user_email} ajouté au channel")
                        return {
                            "success": True,
                            "channel_id": channel_id,
                            "user_id": user_id,
                            "user_email": user_email,
                            "message": "Membre ajouté avec succès"
                        }
                    else:
                        error_msg = result.get("error", "Erreur inconnue")
                        self.logger.warning(f"⚠️ Avertissement Slack: {error_msg}")
                        return {
                            "success": False,
                            "channel_id": channel_id,
                            "user_email": user_email,
                            "message": f"Avertissement: {error_msg}"
                        }
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur ajout membre Slack: {str(e)}")
            raise
    
    async def send_message_to_channel(self, channel: str, message: str, 
                                    agent: str = "donna", blocks: Optional[List[dict]] = None,
                                    thread_ts: Optional[str] = None) -> Dict[str, Any]:
        """Envoyer un message à un channel Slack"""
        try:
            self.logger.info(f"💬 Envoi message au channel {channel}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                message_data = {
                    "channel": channel,
                    "text": message,
                    "username": agent,
                    "icon_emoji": ":robot_face:" if agent == "donna" else ":gear:"
                }
                
                if blocks:
                    message_data["blocks"] = blocks
                
                if thread_ts:
                    message_data["thread_ts"] = thread_ts
                
                response = await client.post(
                    f"{self.api_base}/chat.postMessage",
                    json=message_data,
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        message_info = result["message"]
                        self.logger.info(f"✅ Message envoyé au channel: {message_info.get('ts')}")
                        return {
                            "message_id": message_info.get("ts"),
                            "channel": message_info.get("channel"),
                            "text": message_info.get("text"),
                            "timestamp": datetime.utcnow().isoformat() + "Z",
                            "agent": agent
                        }
                    else:
                        error_msg = result.get("error", "Erreur inconnue")
                        self.logger.error(f"❌ Erreur Slack: {error_msg}")
                        raise Exception(f"Slack API error: {error_msg}")
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi message Slack: {str(e)}")
            raise
    
    async def link_channel_to_workspace(self, workspace_id: str, channel_id: str, 
                                      channel_name: str, user_id: str) -> Dict[str, Any]:
        """Lier un channel Slack à un workspace O'moni"""
        try:
            self.logger.info(f"🔗 Liaison channel Slack {channel_id} au workspace {workspace_id}")
            
            # Obtenir les informations du channel
            channel_info = await self.get_channel_info(channel_id)
            
            # Créer l'objet de liaison
            link_data = {
                "workspace_id": workspace_id,
                "channel_id": channel_id,
                "channel_name": channel_name or channel_info.get("name", "Unknown"),
                "channel_type": "private" if channel_info.get("is_private") else "public",
                "linked_by": user_id,
                "linked_at": datetime.utcnow().isoformat() + "Z",
                "channel_info": channel_info
            }
            
            self.logger.info(f"✅ Channel Slack lié au workspace: {link_data['channel_name']}")
            return link_data
            
        except Exception as e:
            self.logger.error(f"❌ Erreur liaison channel Slack: {str(e)}")
            raise
    
    async def _get_user_id_by_email(self, email: str) -> Optional[str]:
        """Obtenir l'ID Slack d'un utilisateur par son email"""
        try:
            self.logger.info(f"🔍 Recherche utilisateur par email: {email}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                lookup_data = {
                    "email": email
                }
                
                response = await client.post(
                    f"{self.api_base}/users.lookupByEmail",
                    json=lookup_data,
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok") and result.get("user"):
                        user_id = result["user"]["id"]
                        self.logger.info(f"✅ Utilisateur trouvé: {user_id}")
                        return user_id
                    else:
                        self.logger.warning(f"⚠️ Utilisateur non trouvé: {email}")
                        return None
                else:
                    self.logger.error(f"❌ Erreur HTTP: {response.status_code}")
                    return None
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur recherche utilisateur: {str(e)}")
            return None
    
    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Obtenir les informations d'un channel"""
        try:
            self.logger.info(f"💬 Récupération infos channel {channel_id}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/conversations.info",
                    json={"channel": channel_id},
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        return result["channel"]
                    else:
                        error_msg = result.get("error", "Erreur inconnue")
                        self.logger.error(f"❌ Erreur Slack: {error_msg}")
                        raise Exception(f"Slack API error: {error_msg}")
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération infos channel: {str(e)}")
            raise
    
    async def get_channel_members(self, channel_id: str) -> List[str]:
        """Obtenir la liste des membres d'un channel"""
        try:
            self.logger.info(f"💬 Récupération membres channel {channel_id}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/conversations.members",
                    json={"channel": channel_id},
                    headers=self._get_headers()
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        return result["members"]
                    else:
                        return []
                else:
                    return []
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération membres: {str(e)}")
            return []

# Instance singleton
slack_enhanced_service = SlackEnhancedService()