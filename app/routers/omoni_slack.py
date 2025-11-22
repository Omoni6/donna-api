#!/usr/bin/env python3
"""
Router Slack pour création et gestion de channels
Endpoints pour créer des channels Slack depuis O'moni
"""

from fastapi import APIRouter, Depends, HTTPException, Request, BackgroundTasks
from typing import Optional, Dict, Any
import logging
from datetime import datetime

from app.models.channels import (
    SlackCreateChannelRequest, SlackCreateChannelResponse,
    SlackAddMemberRequest, SlackSendMessageRequest, SlackLinkChannelRequest
)
from app.services.slack_enhanced_service import slack_enhanced_service
from app.core.security import get_tenant_id

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/slack", tags=["Slack Channels"])

@router.post("/create-channel", response_model=SlackCreateChannelResponse)
async def create_slack_channel(
    request: SlackCreateChannelRequest,
    background_tasks: BackgroundTasks,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Créer un channel Slack
    
    Crée un channel Slack (public ou privé) et retourne les informations
    """
    try:
        logger.info(f"💬 Création channel Slack: {request.channel_name} (private: {request.private})")
        
        # Créer le channel via le service Slack
        result = await slack_enhanced_service.create_channel(
            channel_name=request.channel_name,
            private=request.private,
            description=request.description,
            workspace_id=request.workspace_id
        )
        
        response = SlackCreateChannelResponse(
            success=True,
            channel_id=result["channel_id"],
            channel_name=result["channel_name"],
            private=result["private"],
            created_at=datetime.utcnow()
        )
        
        logger.info(f"✅ Channel Slack créé avec succès: {response.channel_id}")
        return response
        
    except Exception as e:
        logger.error(f"❌ Erreur création channel Slack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur création channel: {str(e)}")

@router.post("/add-member")
async def add_member_to_slack_channel(
    request: SlackAddMemberRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Ajouter un membre à un channel Slack
    
    Ajoute un membre à un channel existant
    """
    try:
        logger.info(f"💬 Ajout membre {request.user_email} au channel {request.channel_id}")
        
        result = await slack_enhanced_service.add_member_to_channel(
            channel_id=request.channel_id,
            user_email=request.user_email,
            workspace_id=request.workspace_id
        )
        
        logger.info(f"✅ Membre ajouté avec succès")
        return {
            "success": result["success"],
            "channel_id": request.channel_id,
            "user_email": request.user_email,
            "message": result["message"]
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur ajout membre Slack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur ajout membre: {str(e)}")

@router.post("/send")
async def send_message_to_slack_channel(
    request: SlackSendMessageRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Envoyer un message à un channel Slack
    
    Envoie un message à un channel Slack spécifique
    """
    try:
        logger.info(f"💬 Envoi message au channel {request.channel}")
        
        result = await slack_enhanced_service.send_message_to_channel(
            channel=request.channel,
            message=request.message,
            agent=request.agent,
            blocks=request.blocks,
            thread_ts=request.thread_ts
        )
        
        logger.info(f"✅ Message envoyé avec succès")
        return {
            "success": True,
            "message_id": result["message_id"],
            "channel": result["channel"],
            "text": result["text"],
            "timestamp": result["timestamp"],
            "agent": result["agent"]
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur envoi message Slack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur envoi message: {str(e)}")

@router.post("/link")
async def link_slack_channel_to_workspace(
    request: SlackLinkChannelRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Lier un channel Slack à un workspace O'moni
    
    Lie un channel Slack existant à un workspace pour la gestion multi-tenant
    """
    try:
        logger.info(f"🔗 Liaison channel Slack {request.channel_id} au workspace {request.workspace_id}")
        
        result = await slack_enhanced_service.link_channel_to_workspace(
            workspace_id=request.workspace_id,
            channel_id=request.channel_id,
            channel_name=request.channel_name,
            user_id=request.user_id
        )
        
        logger.info(f"✅ Channel lié avec succès")
        return {
            "success": True,
            "workspace_id": request.workspace_id,
            "channel_id": request.channel_id,
            "channel_name": result["channel_name"],
            "linked_at": result["linked_at"],
            "linked_by": request.user_id
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur liaison channel Slack: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur liaison channel: {str(e)}")

@router.get("/channel/{channel_id}/info")
async def get_slack_channel_info(
    channel_id: str,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Obtenir les informations d'un channel Slack
    """
    try:
        logger.info(f"💬 Récupération infos channel {channel_id}")
        
        result = await slack_enhanced_service.get_channel_info(channel_id)
        
        logger.info(f"✅ Infos channel récupérées")
        return {
            "success": True,
            "channel_id": channel_id,
            "info": result
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération infos channel: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur récupération infos: {str(e)}")

@router.get("/channel/{channel_id}/members")
async def get_slack_channel_members(
    channel_id: str,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Obtenir la liste des membres d'un channel Slack
    """
    try:
        logger.info(f"💬 Récupération membres channel {channel_id}")
        
        members = await slack_enhanced_service.get_channel_members(channel_id)
        
        logger.info(f"✅ Membres récupérés: {len(members)}")
        return {
            "success": True,
            "channel_id": channel_id,
            "members_count": len(members),
            "members": members
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur récupération membres: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur récupération membres: {str(e)}")