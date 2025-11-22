#!/usr/bin/env python3
"""
Service Telegram amélioré avec création de canaux
"""

import logging
import httpx
from typing import Dict, Any, Optional, List
from datetime import datetime
from app.core.config import settings

# Import pour Telegram Core API (MTProto)
try:
    from telethon import TelegramClient
    from telethon.sessions import StringSession
    from telethon.tl.types import InputChannel, InputPeerChannel
    from telethon.tl.functions.channels import CreateChannelRequest
    TELETHON_AVAILABLE = True
except ImportError:
    TELETHON_AVAILABLE = False

logger = logging.getLogger(__name__)

class TelegramEnhancedService:
    """Service Telegram avec support création de canaux et gestion avancée"""
    
    def __init__(self):
        self.bot_token = settings.TELEGRAM_BOT_TOKEN
        self.bot_username = settings.TELEGRAM_BOT_USERNAME
        self.api_base = f"https://api.telegram.org/bot{self.bot_token}"
        self.timeout = 30.0
        self.logger = logging.getLogger(__name__)
        
        # Configuration pour Telegram Core API (MTProto)
        self.api_id = settings.TELEGRAM_API_ID
        self.api_hash = settings.TELEGRAM_API_HASH
        self.telethon_available = TELETHON_AVAILABLE and self.api_id and self.api_hash
    
    async def create_channel_with_core_api(self, channel_name: str, channel_type: str = "private", 
                                         description: Optional[str] = None, members: List[str] = None) -> Dict[str, Any]:
        """Créer un canal Telegram via Telegram Core API (MTProto) avec hash"""
        if not self.telethon_available:
            raise Exception("Telethon n'est pas disponible ou API credentials manquants")
        
        try:
            self.logger.info(f"📱 Création canal Telegram via Core API: {channel_name} ({channel_type})")
            
            # NOTE: Telegram Core API (MTProto) nécessite un compte utilisateur, pas un bot
            # Les bots ne peuvent pas créer de canaux via l'API Core
            # Cette méthode nécessiterait un numéro de téléphone et une authentification utilisateur
            
            raise Exception(
                "La création de canaux via Telegram Core API nécessite un compte utilisateur. "
                "Les bots ne peuvent pas créer de canaux via MTProto. "
                "Utilisez la méthode Bot API avec admin rights sur un canal existant."
            )
            
            # Initialiser le client Telegram avec API hash
            async with TelegramClient(session, self.api_id, self.api_hash) as client:
                # S'authentifier avec le bot token
                await client.start(bot_token=self.bot_token)
                
                # Créer le canal
                result = await client(CreateChannelRequest(
                    title=channel_name,
                    about=description or f"Canal créé via O'moni - {channel_name}",
                    megagroup=channel_type == "megagroup",
                    broadcast=channel_type == "broadcast"
                ))
                
                # Extraire l'ID du canal créé
                channel_id = None
                if hasattr(result, 'chats') and result.chats:
                    channel = result.chats[0]
                    channel_id = str(channel.id)
                    
                    self.logger.info(f"✅ Canal créé avec succès: {channel_name} (ID: {channel_id})")
                    
                    # Créer un lien d'invitation
                    invite_link = await client.export_invite_link(channel_id)
                    
                    return {
                        "channel_id": channel_id,
                        "invite_link": invite_link,
                        "channel_name": channel_name,
                        "type": channel_type,
                        "description": description or f"Canal créé via O'moni - {channel_name}",
                        "created_at": datetime.utcnow().isoformat() + "Z",
                        "method": "core_api"
                    }
                else:
                    raise Exception("Impossible de récupérer l'ID du canal créé")
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur création canal via Core API: {str(e)}")
            raise
    
    async def create_channel(self, channel_name: str, channel_type: str = "private", 
                           description: Optional[str] = None, members: List[str] = None) -> Dict[str, Any]:
        """Créer un canal/supergroupe Telegram via Bot API"""
        try:
            self.logger.info(f"📱 Création canal Telegram: {channel_name} ({channel_type})")
            
            # NOTE IMPORTANTE: Les bots Telegram ne peuvent pas créer de canaux/supergroupes
            # Ils peuvent uniquement créer des liens d'invitation pour des canaux existants
            # Pour créer un canal, il faut:
            # 1. Un compte utilisateur (pas un bot) avec Telegram Core API
            # 2. Ou utiliser un canal existant et créer des liens d'invitation
            
            self.logger.warning(
                "⚠️ Les bots Telegram ne peuvent pas créer de canaux. "
                "Création d'un lien d'invitation personnalisé à la place."
            )
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Utiliser le canal système par défaut (doit exister et le bot doit être admin)
                channel_id = settings.TELEGRAM_CHAT_ID_SYSTEM or "-4919674767"
                
                # Créer un lien d'invitation personnalisé comme alternative
                invite_data = {
                    "chat_id": channel_id,
                    "name": channel_name.replace(" ", "_").lower()[:32],  # Max 32 chars
                    "expire_date": int((datetime.utcnow().timestamp() + 86400 * 7)),  # 7 jours
                    "member_limit": 100  # Limite de membres
                }
                
                response = await client.post(
                    f"{self.api_base}/createChatInviteLink",
                    json=invite_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        invite_link = result["result"].get("invite_link", "")
                        
                        self.logger.info(f"✅ Lien d'invitation créé: {invite_link}")
                        return {
                            "channel_id": channel_id,
                            "invite_link": invite_link,
                            "channel_name": channel_name,
                            "type": channel_type,
                            "description": description or f"Lien pour canal {channel_name}",
                            "created_at": datetime.utcnow().isoformat() + "Z",
                            "method": "invite_link",
                            "note": "Les bots ne peuvent pas créer de canaux, lien d'invitation créé"
                        }
                    else:
                        error_msg = result.get("description", "Erreur inconnue")
                        self.logger.error(f"❌ Erreur Telegram: {error_msg}")
                        raise Exception(f"Telegram API error: {error_msg}")
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur création canal Telegram: {str(e)}")
            raise
    
    async def add_member_to_channel(self, channel_id: str, username: str) -> Dict[str, Any]:
        """Ajouter un membre à un canal Telegram"""
        try:
            self.logger.info(f"📱 Ajout membre {username} au canal {channel_id}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                # Promouvoir le membre en administrateur (nécessite permissions)
                promote_data = {
                    "chat_id": channel_id,
                    "user_id": username,  # Peut être @username ou user_id
                    "can_manage_chat": True,
                    "can_post_messages": True,
                    "can_edit_messages": True,
                    "can_delete_messages": True,
                    "can_manage_voice_chats": True,
                    "can_restrict_members": True,
                    "can_promote_members": True,
                    "can_change_info": True,
                    "can_invite_users": True
                }
                
                response = await client.post(
                    f"{self.api_base}/promoteChatMember",
                    json=promote_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        self.logger.info(f"✅ Membre {username} ajouté au canal")
                        return {
                            "success": True,
                            "channel_id": channel_id,
                            "username": username,
                            "message": "Membre ajouté avec succès"
                        }
                    else:
                        error_msg = result.get("description", "Erreur inconnue")
                        self.logger.warning(f"⚠️ Avertissement Telegram: {error_msg}")
                        # Ne pas lever d'exception pour les avertissements
                        return {
                            "success": False,
                            "channel_id": channel_id,
                            "username": username,
                            "message": f"Avertissement: {error_msg}"
                        }
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur ajout membre Telegram: {str(e)}")
            raise
    
    async def send_message_to_channel(self, channel_id: str, message: str, 
                                    parse_mode: str = "HTML", disable_notification: bool = False) -> Dict[str, Any]:
        """Envoyer un message à un canal Telegram"""
        try:
            self.logger.info(f"📱 Envoi message au canal {channel_id}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                message_data = {
                    "chat_id": channel_id,
                    "text": message,
                    "parse_mode": parse_mode,
                    "disable_notification": disable_notification
                }
                
                response = await client.post(
                    f"{self.api_base}/sendMessage",
                    json=message_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        message_info = result["result"]
                        self.logger.info(f"✅ Message envoyé au canal: {message_info.get('message_id')}")
                        return {
                            "message_id": message_info.get("message_id"),
                            "chat_id": message_info.get("chat", {}).get("id"),
                            "text": message_info.get("text"),
                            "timestamp": datetime.utcnow().isoformat() + "Z"
                        }
                    else:
                        error_msg = result.get("description", "Erreur inconnue")
                        self.logger.error(f"❌ Erreur Telegram: {error_msg}")
                        raise Exception(f"Telegram API error: {error_msg}")
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur envoi message Telegram: {str(e)}")
            raise
    
    async def link_channel_to_workspace(self, workspace_id: str, channel_id: str, 
                                      channel_name: str, user_id: str) -> Dict[str, Any]:
        """Lier un canal Telegram à un workspace O'moni"""
        try:
            self.logger.info(f"🔗 Liaison canal Telegram {channel_id} au workspace {workspace_id}")
            
            # Obtenir les informations du canal
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                chat_info_data = {
                    "chat_id": channel_id
                }
                
                response = await client.post(
                    f"{self.api_base}/getChat",
                    json=chat_info_data
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        chat_info = result["result"]
                        
                        # Créer l'objet de liaison
                        link_data = {
                            "workspace_id": workspace_id,
                            "channel_id": channel_id,
                            "channel_name": channel_name or chat_info.get("title", "Unknown"),
                            "channel_type": chat_info.get("type", "channel"),
                            "linked_by": user_id,
                            "linked_at": datetime.utcnow().isoformat() + "Z",
                            "chat_info": chat_info
                        }
                        
                        self.logger.info(f"✅ Canal Telegram lié au workspace: {link_data['channel_name']}")
                        return link_data
                    else:
                        error_msg = result.get("description", "Erreur inconnue")
                        self.logger.error(f"❌ Erreur Telegram: {error_msg}")
                        raise Exception(f"Telegram API error: {error_msg}")
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur liaison canal Telegram: {str(e)}")
            raise
    
    async def get_channel_info(self, channel_id: str) -> Dict[str, Any]:
        """Obtenir les informations d'un canal"""
        try:
            self.logger.info(f"📱 Récupération infos canal {channel_id}")
            
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/getChat",
                    json={"chat_id": channel_id}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        return result["result"]
                    else:
                        error_msg = result.get("description", "Erreur inconnue")
                        self.logger.error(f"❌ Erreur Telegram: {error_msg}")
                        raise Exception(f"Telegram API error: {error_msg}")
                else:
                    error_msg = f"HTTP {response.status_code}: {response.text}"
                    self.logger.error(f"❌ Erreur HTTP: {error_msg}")
                    raise Exception(error_msg)
                    
        except Exception as e:
            self.logger.error(f"❌ Erreur récupération infos canal: {str(e)}")
            raise
    
    async def get_chat_members_count(self, channel_id: str) -> int:
        """Obtenir le nombre de membres d'un chat"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.api_base}/getChatMembersCount",
                    json={"chat_id": channel_id}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if result.get("ok"):
                        return result["result"]
                    else:
                        return 0
                else:
                    return 0
                    
        except Exception:
            return 0

# Instance singleton
telegram_enhanced_service = TelegramEnhancedService()