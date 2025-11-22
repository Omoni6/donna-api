#!/usr/bin/env python3
"""
Router Telegram pour création et gestion de canaux
Endpoints pour créer des canaux Telegram depuis O'moni
"""

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from app.models.channels import (
    TelegramCreateChannelRequest, TelegramCreateChannelResponse,
    TelegramAddMemberRequest, TelegramSendMessageRequest, TelegramLinkChannelRequest
)
from app.services.telegram_enhanced_service import telegram_enhanced_service
from app.core.security import get_tenant_id

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/telegram", tags=["Telegram Channels"])

@router.post("/create-channel", response_model=TelegramCreateChannelResponse)
async def create_telegram_channel(
    request: TelegramCreateChannelRequest,
    background_tasks: BackgroundTasks,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Créer un canal Telegram
    
    Crée un canal Telegram (public, privé ou groupe) et retourne les informations
    """
    try:
        logger.info(f"📱 Création canal Telegram: {request.channel_name} (type: {request.type})")
        
        # Créer le canal via le service Telegram
        result = await telegram_enhanced_service.create_channel(
            channel_name=request.channel_name,
            channel_type=request.type,
            description=request.description,
            members=request.members
        )
        
        # Ajouter les membres en background si spécifiés
        if request.members:
            for member in request.members:
                background_tasks.add_task(
                    telegram_enhanced_service.add_member_to_channel,
                    result["channel_id"],
                    member
                )
        
        response = TelegramCreateChannelResponse(
            success=True,
            channel_id=result["channel_id"],
            invite_link=result.get("invite_link"),
            channel_name=request.channel_name,
            type=request.type
        )
        
        logger.info(f"✅ Canal Telegram créé avec succès: {response.channel_id}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Erreur création canal Telegram: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur création canal: {str(e)}")

@router.post("/add-member")
async def add_member_to_telegram_channel(
    request: TelegramAddMemberRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Ajouter un membre à un canal Telegram
    
    Ajoute un membre à un canal existant (le bot doit être admin)
    """
    try:
        logger.info(f"📱 Ajout membre {request.username} au canal {request.channel_id}")
        
        result = await telegram_enhanced_service.add_member_to_channel(
            channel_id=request.channel_id,
            username=request.username
        )
        
        logger.info(f"✅ Membre ajouté avec succès")
        return {
            "success": result["success"],
            "channel_id": request.channel_id,
            "username": request.username,
            "message": result["message"]
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur ajout membre Telegram: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur ajout membre: {str(e)}")

@router.post("/send")
async def send_message_to_telegram_channel(
    request: TelegramSendMessageRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Envoyer un message à un canal Telegram
    
    Envoie un message à un canal Telegram spécifique
    """
    try:
        logger.info(f"📱 Envoi message au canal {request.channel_id}")
        
        result = await telegram_enhanced_service.send_message_to_channel(
            channel_id=request.channel_id,
            message=request.message,
            parse_mode=request.parse_mode,
            disable_notification=request.disable_notification
        )
        
        logger.info(f"✅ Message envoyé avec succès")
        return {
            "success": True,
            "message_id": result["message_id"],
            "channel_id": result["chat_id"],
            "text": result["text"],
            "timestamp": result["timestamp"]
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur envoi message Telegram: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur envoi message: {str(e)}")

@router.post("/link")
async def link_telegram_channel_to_workspace(
    request: TelegramLinkChannelRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Lier un canal Telegram à un workspace O'moni
    
    Lie un canal Telegram existant à un workspace pour la gestion multi-tenant
    """
    try:
        logger.info(f"🔗 Liaison canal Telegram {request.channel_id} au workspace {request.workspace_id}")
        
        result = await telegram_enhanced_service.link_channel_to_workspace(
            workspace_id=request.workspace_id,
            channel_id=request.channel_id,
            channel_name=request.channel_name,
            user_id=request.user_id
        )
        
        logger.info(f"✅ Canal lié avec succès")
        return {
            "success": True,
            "workspace_id": request.workspace_id,
            "channel_id": request.channel_id,
            "channel_name": result["channel_name"],
            "linked_at": result["linked_at"],
            "linked_by": request.user_id
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur liaison canal Telegram: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur liaison canal: {str(e)}")

@router.get("/channel/{channel_id}/info")
async def get_telegram_channel_info(
    channel_id: str,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Obtenir les informations d'un canal Telegram
    """
    try:
        logger.info(f"📱 Récupération infos canal {channel_id}")
        
        result = await telegram_enhanced_service.get_channel_info(channel_id)
        
        logger.info(f"✅ Infos canal récupérées")
        return {
            "success": True,
            "channel_id": channel_id,
            "info": result
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération infos canal: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur récupération infos: {str(e)}")

@router.get("/channel/{channel_id}/members/count")
async def get_telegram_channel_members_count(
    channel_id: str,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Obtenir le nombre de membres d'un canal Telegram
    """
    try:
        logger.info(f"📱 Récupération nombre membres canal {channel_id}")
        
        count = await telegram_enhanced_service.get_chat_members_count(channel_id)
        
        logger.info(f"✅ Nombre membres récupéré: {count}")
        return {
            "success": True,
            "channel_id": channel_id,
            "members_count": count
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération nombre membres: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur récupération nombre membres: {str(e)}")