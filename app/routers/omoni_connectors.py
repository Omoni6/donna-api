#!/usr/bin/env python3
"""
Router général pour la gestion des connecteurs (Slack/Telegram)
Endpoint universel pour créer des canaux, ajouter des membres, etc.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional, Dict, Any
import logging

from app.models.channels import ConnectorManageRequest, ConnectorManageResponse
from app.services.telegram_enhanced_service import telegram_enhanced_service
from app.services.slack_enhanced_service import slack_enhanced_service
from app.core.security import get_tenant_id

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/connectors", tags=["Connectors Management"])

@router.post("/manage", response_model=ConnectorManageResponse)
async def manage_connector(
    request: ConnectorManageRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Gestion universelle des connecteurs Slack et Telegram
    
    Endpoint unique pour gérer tous les connecteurs (création de canaux, ajout de membres, etc.)
    """
    try:
        logger.info(f"🔧 Gestion connecteur: {request.provider} - Action: {request.action}")
        
        if request.provider == "telegram":
            result = await _handle_telegram_action(request, tenant_id)
        elif request.provider == "slack":
            result = await _handle_slack_action(request, tenant_id)
        else:
            raise HTTPException(status_code=400, detail="Fournisseur non supporté")
        
        response = ConnectorManageResponse(
            success=True,
            provider=request.provider,
            action=request.action,
            result=result["result"],
            message=result["message"]
        )
        
        logger.info(f"✅ Action connecteur réussie: {request.provider}.{request.action}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur gestion connecteur: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur gestion connecteur: {str(e)}")

async def _handle_telegram_action(request: ConnectorManageRequest, tenant_id: Optional[str]) -> Dict[str, Any]:
    """Gérer les actions Telegram"""
    try:
        action = request.action
        data = request.data
        workspace_id = request.workspace_id
        user_id = request.user_id
        
        if action == "create_channel":
            # Créer un canal Telegram
            channel_name = data.get("channel_name")
            channel_type = data.get("type", "private")
            description = data.get("description")
            members = data.get("members", [])
            
            if not channel_name:
                raise HTTPException(status_code=400, detail="Nom du canal requis")
            
            result = await telegram_enhanced_service.create_channel(
                channel_name=channel_name,
                channel_type=channel_type,
                description=description,
                members=members
            )
            
            return {
                "result": result,
                "message": f"Canal Telegram '{channel_name}' créé avec succès"
            }
        
        elif action == "add_member":
            # Ajouter un membre
            channel_id = data.get("channel_id")
            username = data.get("username")
            
            if not channel_id or not username:
                raise HTTPException(status_code=400, detail="Channel ID et username requis")
            
            result = await telegram_enhanced_service.add_member_to_channel(channel_id, username)
            return {
                "result": result,
                "message": f"Membre @{username} ajouté au canal"
            }
        
        elif action == "send_message":
            # Envoyer un message
            channel_id = data.get("channel_id")
            message = data.get("message")
            parse_mode = data.get("parse_mode", "HTML")
            
            if not channel_id or not message:
                raise HTTPException(status_code=400, detail="Channel ID et message requis")
            
            result = await telegram_enhanced_service.send_message_to_channel(
                channel_id=channel_id,
                message=message,
                parse_mode=parse_mode
            )
            
            return {
                "result": result,
                "message": f"Message envoyé au canal Telegram"
            }
        
        elif action == "link":
            # Lier un canal au workspace
            workspace_id = workspace_id or data.get("workspace_id")
            channel_id = data.get("channel_id")
            channel_name = data.get("channel_name")
            
            if not workspace_id or not channel_id:
                raise HTTPException(status_code=400, detail="Workspace ID et Channel ID requis")
            
            result = await telegram_enhanced_service.link_channel_to_workspace(
                workspace_id=workspace_id,
                channel_id=channel_id,
                channel_name=channel_name or "Linked Channel",
                user_id=user_id
            )
            
            return {
                "result": result,
                "message": f"Canal Telegram lié au workspace {workspace_id}"
            }
        
        elif action == "sync":
            # Synchroniser les données
            channel_id = data.get("channel_id")
            
            if not channel_id:
                raise HTTPException(status_code=400, detail="Channel ID requis")
            
            info = await telegram_enhanced_service.get_channel_info(channel_id)
            member_count = await telegram_enhanced_service.get_chat_members_count(channel_id)
            
            result = {
                "channel_info": info,
                "members_count": member_count,
                "synced_at": datetime.utcnow().isoformat() + "Z"
            }
            
            return {
                "result": result,
                "message": f"Canal Telegram synchronisé: {member_count} membres"
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"Action Telegram non supportée: {action}")
            
    except Exception as e:
        logger.error(f"❌ Erreur action Telegram: {str(e)}")
        raise

async def _handle_slack_action(request: ConnectorManageRequest, tenant_id: Optional[str]) -> Dict[str, Any]:
    """Gérer les actions Slack"""
    try:
        action = request.action
        data = request.data
        workspace_id = request.workspace_id
        user_id = request.user_id
        
        if action == "create_channel":
            # Créer un channel Slack
            channel_name = data.get("channel_name")
            private = data.get("private", False)
            description = data.get("description")
            
            if not channel_name:
                raise HTTPException(status_code=400, detail="Nom du channel requis")
            
            result = await slack_enhanced_service.create_channel(
                channel_name=channel_name,
                private=private,
                description=description,
                workspace_id=workspace_id
            )
            
            return {
                "result": result,
                "message": f"Channel Slack '{channel_name}' créé avec succès"
            }
        
        elif action == "add_member":
            # Ajouter un membre
            channel_id = data.get("channel_id")
            user_email = data.get("user_email")
            
            if not channel_id or not user_email:
                raise HTTPException(status_code=400, detail="Channel ID et email requis")
            
            result = await slack_enhanced_service.add_member_to_channel(
                channel_id=channel_id,
                user_email=user_email,
                workspace_id=workspace_id
            )
            
            return {
                "result": result,
                "message": f"Membre {user_email} ajouté au channel"
            }
        
        elif action == "send_message":
            # Envoyer un message
            channel = data.get("channel")
            message = data.get("message")
            agent = data.get("agent", "donna")
            blocks = data.get("blocks")
            
            if not channel or not message:
                raise HTTPException(status_code=400, detail="Channel et message requis")
            
            result = await slack_enhanced_service.send_message_to_channel(
                channel=channel,
                message=message,
                agent=agent,
                blocks=blocks
            )
            
            return {
                "result": result,
                "message": f"Message envoyé au channel Slack"
            }
        
        elif action == "link":
            # Lier un channel au workspace
            workspace_id = workspace_id or data.get("workspace_id")
            channel_id = data.get("channel_id")
            channel_name = data.get("channel_name")
            
            if not workspace_id or not channel_id:
                raise HTTPException(status_code=400, detail="Workspace ID et Channel ID requis")
            
            result = await slack_enhanced_service.link_channel_to_workspace(
                workspace_id=workspace_id,
                channel_id=channel_id,
                channel_name=channel_name or "Linked Channel",
                user_id=user_id
            )
            
            return {
                "result": result,
                "message": f"Channel Slack lié au workspace {workspace_id}"
            }
        
        elif action == "sync":
            # Synchroniser les données
            channel_id = data.get("channel_id")
            
            if not channel_id:
                raise HTTPException(status_code=400, detail="Channel ID requis")
            
            info = await slack_enhanced_service.get_channel_info(channel_id)
            members = await slack_enhanced_service.get_channel_members(channel_id)
            
            result = {
                "channel_info": info,
                "members_count": len(members),
                "members": members,
                "synced_at": datetime.utcnow().isoformat() + "Z"
            }
            
            return {
                "result": result,
                "message": f"Channel Slack synchronisé: {len(members)} membres"
            }
        
        else:
            raise HTTPException(status_code=400, detail=f"Action Slack non supportée: {action}")
            
    except Exception as e:
        logger.error(f"❌ Erreur action Slack: {str(e)}")
        raise