#!/usr/bin/env python3
"""
Modèles pour les endpoints Telegram et Slack
"""

from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime

# ===== TELEGRAM MODELS =====

class TelegramCreateChannelRequest(BaseModel):
    user_id: str = Field(..., description="ID utilisateur")
    channel_name: str = Field(..., description="Nom du canal")
    type: Literal["public", "private", "group"] = Field(default="private", description="Type de canal")
    members: List[str] = Field(default_factory=list, description="Membres à ajouter")
    description: Optional[str] = Field(None, description="Description du canal")

class TelegramCreateChannelResponse(BaseModel):
    success: bool = Field(..., description="Succès de l'opération")
    channel_id: str = Field(..., description="ID du canal créé")
    invite_link: Optional[str] = Field(None, description="Lien d'invitation")
    channel_name: str = Field(..., description="Nom du canal")
    type: str = Field(..., description="Type de canal")

class TelegramAddMemberRequest(BaseModel):
    channel_id: str = Field(..., description="ID du canal")
    username: str = Field(..., description="Nom d'utilisateur à ajouter")
    user_id: str = Field(..., description="ID utilisateur effectuant l'action")

class TelegramSendMessageRequest(BaseModel):
    channel_id: str = Field(..., description="ID du canal")
    message: str = Field(..., description="Message à envoyer")
    parse_mode: Literal["HTML", "Markdown", "MarkdownV2"] = Field(default="HTML", description="Mode de parsing")
    disable_notification: bool = Field(default=False, description="Désactiver les notifications")

class TelegramLinkChannelRequest(BaseModel):
    workspace_id: str = Field(..., description="ID du workspace O'moni")
    channel_id: str = Field(..., description="ID du canal Telegram")
    channel_name: str = Field(..., description="Nom du canal")
    user_id: str = Field(..., description="ID utilisateur")

# ===== SLACK MODELS =====

class SlackCreateChannelRequest(BaseModel):
    workspace_id: str = Field(..., description="ID du workspace")
    channel_name: str = Field(..., description="Nom du channel")
    private: bool = Field(default=False, description="Channel privé ou non")
    description: Optional[str] = Field(None, description="Description du channel")
    user_id: str = Field(..., description="ID utilisateur créant le channel")

class SlackCreateChannelResponse(BaseModel):
    success: bool = Field(..., description="Succès de l'opération")
    channel_id: str = Field(..., description="ID du channel créé")
    channel_name: str = Field(..., description="Nom du channel")
    private: bool = Field(..., description="Si le channel est privé")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date de création")

class SlackAddMemberRequest(BaseModel):
    channel_id: str = Field(..., description="ID du channel")
    user_email: str = Field(..., description="Email de l'utilisateur à ajouter")
    workspace_id: str = Field(..., description="ID du workspace")

class SlackSendMessageRequest(BaseModel):
    channel: str = Field(..., description="ID ou nom du channel")
    message: str = Field(..., description="Message à envoyer")
    agent: str = Field(default="donna", description="Agent envoyant le message")
    blocks: Optional[List[dict]] = Field(None, description="Blocks Slack pour formatting avancé")
    thread_ts: Optional[str] = Field(None, description="Thread timestamp pour répondre à un message")

class SlackLinkChannelRequest(BaseModel):
    workspace_id: str = Field(..., description="ID du workspace O'moni")
    channel_id: str = Field(..., description="ID du channel Slack")
    channel_name: str = Field(..., description="Nom du channel")
    user_id: str = Field(..., description="ID utilisateur")

# ===== CONNECTOR MANAGEMENT MODELS =====

class ConnectorManageRequest(BaseModel):
    provider: Literal["slack", "telegram"] = Field(..., description="Fournisseur de service")
    action: Literal["create_channel", "add_member", "send_message", "sync", "link"] = Field(..., description="Action à effectuer")
    data: dict = Field(..., description="Données spécifiques à l'action")
    workspace_id: Optional[str] = Field(None, description="ID du workspace")
    user_id: str = Field(..., description="ID utilisateur")

class ConnectorManageResponse(BaseModel):
    success: bool = Field(..., description="Succès de l'opération")
    provider: str = Field(..., description="Fournisseur")
    action: str = Field(..., description="Action effectuée")
    result: dict = Field(..., description="Résultat de l'action")
    message: str = Field(..., description="Message de retour")

# ===== AGENT COMMUNICATION MODELS =====

class AgentCommunicateRequest(BaseModel):
    action: Literal["create_slack_channel", "create_telegram_channel", "send_slack_message", "send_telegram_message", "add_slack_member", "add_telegram_member"] = Field(..., description="Action demandée")
    payload: dict = Field(..., description="Données de l'action")
    agent_id: str = Field(..., description="ID de l'agent")
    user_id: str = Field(..., description="ID utilisateur")
    workspace_id: Optional[str] = Field(None, description="ID du workspace")

class AgentCommunicateResponse(BaseModel):
    success: bool = Field(..., description="Succès de l'opération")
    action: str = Field(..., description="Action effectuée")
    result: dict = Field(..., description="Résultat")
    message: str = Field(..., description="Message de retour")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp de la réponse")