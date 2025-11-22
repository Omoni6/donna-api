#!/usr/bin/env python3
"""
Router pour la communication avec les agents Donna
Endpoint permettant aux agents de créer des canaux, envoyer des messages, etc.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional, Dict, Any
import logging

from app.models.channels import AgentCommunicateRequest, AgentCommunicateResponse
from app.services.telegram_enhanced_service import telegram_enhanced_service
from app.services.slack_enhanced_service import slack_enhanced_service
from app.core.security import get_tenant_id

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/communicate", tags=["Agent Communication"])

@router.post("", response_model=AgentCommunicateResponse)
async def agent_communicate(
    request: AgentCommunicateRequest,
    tenant_id: Optional[str] = Depends(get_tenant_id)
):
    """
    Communication avec les agents pour exécuter des actions
    
    Permet aux agents Donna de créer des canaux, envoyer des messages, etc.
    """
    try:
        logger.info(f"🤖 Communication agent: {request.agent_id} - Action: {request.action}")
        
        result = await _handle_agent_action(request, tenant_id)
        
        response = AgentCommunicateResponse(
            success=True,
            action=request.action,
            result=result["result"],
            message=result["message"]
        )
        
        logger.info(f"✅ Action agent réussie: {request.action}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Erreur communication agent: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur communication agent: {str(e)}")

async def _handle_agent_action(request: AgentCommunicateRequest, tenant_id: Optional[str]) -> Dict[str, Any]:
    """Gérer les actions des agents"""
    try:
        action = request.action
        payload = request.payload
        agent_id = request.agent_id
        user_id = request.user_id
        workspace_id = request.workspace_id
        
        if action == "create_slack_channel":
            return await _handle_create_slack_channel(payload, agent_id, user_id, workspace_id)
        
        elif action == "create_telegram_channel":
            return await _handle_create_telegram_channel(payload, agent_id, user_id, workspace_id)
        
        elif action == "send_slack_message":
            return await _handle_send_slack_message(payload, agent_id, user_id, workspace_id)
        
        elif action == "send_telegram_message":
            return await _handle_send_telegram_message(payload, agent_id, user_id, workspace_id)
        
        elif action == "add_slack_member":
            return await _handle_add_slack_member(payload, agent_id, user_id, workspace_id)
        
        elif action == "add_telegram_member":
            return await _handle_add_telegram_member(payload, agent_id, user_id, workspace_id)
        
        else:
            raise HTTPException(status_code=400, detail=f"Action agent non supportée: {action}")
            
    except Exception as e:
        logger.error(f"❌ Erreur traitement action agent: {str(e)}")
        raise

async def _handle_create_slack_channel(payload: Dict[str, Any], agent_id: str, user_id: str, workspace_id: Optional[str]) -> Dict[str, Any]:
    """Créer un channel Slack via agent"""
    try:
        channel_name = payload.get("channel_name")
        private = payload.get("private", False)
        description = payload.get("description")
        
        if not channel_name:
            raise HTTPException(status_code=400, detail="Nom du channel requis")
        
        result = await slack_enhanced_service.create_channel(
            channel_name=channel_name,
            private=private,
            description=description,
            workspace_id=workspace_id
        )
        
        return {
            "result": {
                "channel_id": result["channel_id"],
                "channel_name": result["channel_name"],
                "private": result["private"],
                "created_by_agent": agent_id,
                "created_at": result.get("created", datetime.utcnow().isoformat() + "Z")
            },
            "message": f"Channel Slack '{channel_name}' créé par l'agent {agent_id}"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur création channel Slack par agent: {str(e)}")
        raise

async def _handle_create_telegram_channel(payload: Dict[str, Any], agent_id: str, user_id: str, workspace_id: Optional[str]) -> Dict[str, Any]:
    """Créer un canal Telegram via agent"""
    try:
        channel_name = payload.get("channel_name")
        channel_type = payload.get("type", "private")
        description = payload.get("description")
        members = payload.get("members", [])
        
        if not channel_name:
            raise HTTPException(status_code=400, detail="Nom du canal requis")
        
        result = await telegram_enhanced_service.create_channel(
            channel_name=channel_name,
            channel_type=channel_type,
            description=description,
            members=members
        )
        
        return {
            "result": {
                "channel_id": result["channel_id"],
                "channel_name": result["channel_name"],
                "type": result["type"],
                "invite_link": result.get("invite_link"),
                "created_by_agent": agent_id,
                "created_at": datetime.utcnow().isoformat() + "Z"
            },
            "message": f"Canal Telegram '{channel_name}' créé par l'agent {agent_id}"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur création canal Telegram par agent: {str(e)}")
        raise

async def _handle_send_slack_message(payload: Dict[str, Any], agent_id: str, user_id: str, workspace_id: Optional[str]) -> Dict[str, Any]:
    """Envoyer un message Slack via agent"""
    try:
        channel = payload.get("channel")
        message = payload.get("message")
        blocks = payload.get("blocks")
        thread_ts = payload.get("thread_ts")
        
        if not channel or not message:
            raise HTTPException(status_code=400, detail="Channel et message requis")
        
        result = await slack_enhanced_service.send_message_to_channel(
            channel=channel,
            message=message,
            agent=agent_id,  # Utiliser l'ID de l'agent comme sender
            blocks=blocks,
            thread_ts=thread_ts
        )
        
        return {
            "result": {
                "message_id": result["message_id"],
                "channel": result["channel"],
                "text": result["text"],
                "sent_by_agent": agent_id,
                "timestamp": result["timestamp"]
            },
            "message": f"Message envoyé au channel Slack par l'agent {agent_id}"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur envoi message Slack par agent: {str(e)}")
        raise

async def _handle_send_telegram_message(payload: Dict[str, Any], agent_id: str, user_id: str, workspace_id: Optional[str]) -> Dict[str, Any]:
    """Envoyer un message Telegram via agent"""
    try:
        channel_id = payload.get("channel_id")
        message = payload.get("message")
        parse_mode = payload.get("parse_mode", "HTML")
        disable_notification = payload.get("disable_notification", False)
        
        if not channel_id or not message:
            raise HTTPException(status_code=400, detail="Channel ID et message requis")
        
        result = await telegram_enhanced_service.send_message_to_channel(
            channel_id=channel_id,
            message=message,
            parse_mode=parse_mode,
            disable_notification=disable_notification
        )
        
        return {
            "result": {
                "message_id": result["message_id"],
                "chat_id": result["chat_id"],
                "text": result["text"],
                "sent_by_agent": agent_id,
                "timestamp": result["timestamp"]
            },
            "message": f"Message envoyé au canal Telegram par l'agent {agent_id}"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur envoi message Telegram par agent: {str(e)}")
        raise

async def _handle_add_slack_member(payload: Dict[str, Any], agent_id: str, user_id: str, workspace_id: Optional[str]) -> Dict[str, Any]:
    """Ajouter un membre Slack via agent"""
    try:
        channel_id = payload.get("channel_id")
        user_email = payload.get("user_email")
        
        if not channel_id or not user_email:
            raise HTTPException(status_code=400, detail="Channel ID et email requis")
        
        result = await slack_enhanced_service.add_member_to_channel(
            channel_id=channel_id,
            user_email=user_email,
            workspace_id=workspace_id
        )
        
        return {
            "result": {
                "success": result["success"],
                "channel_id": result["channel_id"],
                "user_email": result["user_email"],
                "added_by_agent": agent_id
            },
            "message": f"Membre {user_email} ajouté au channel par l'agent {agent_id}"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur ajout membre Slack par agent: {str(e)}")
        raise

async def _handle_add_telegram_member(payload: Dict[str, Any], agent_id: str, user_id: str, workspace_id: Optional[str]) -> Dict[str, Any]:
    """Ajouter un membre Telegram via agent"""
    try:
        channel_id = payload.get("channel_id")
        username = payload.get("username")
        
        if not channel_id or not username:
            raise HTTPException(status_code=400, detail="Channel ID et username requis")
        
        result = await telegram_enhanced_service.add_member_to_channel(
            channel_id=channel_id,
            username=username
        )
        
        return {
            "result": {
                "success": result["success"],
                "channel_id": result["channel_id"],
                "username": result["username"],
                "added_by_agent": agent_id
            },
            "message": f"Membre @{username} ajouté au canal par l'agent {agent_id}"
        }
        
    except Exception as e:
        logger.error(f"❌ Erreur ajout membre Telegram par agent: {str(e)}")
        raise