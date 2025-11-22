from pydantic import BaseModel, Field, HttpUrl
from typing import Dict, Any, Optional, List, Union
from datetime import datetime
from enum import Enum

class WebhookType(str, Enum):
    TELEGRAM = "telegram"
    STRIPE = "stripe"
    GOOGLE = "google"

class TelegramWebhookPayload(BaseModel):
    update_id: int
    message: Optional[Dict[str, Any]] = None
    edited_message: Optional[Dict[str, Any]] = None
    channel_post: Optional[Dict[str, Any]] = None
    edited_channel_post: Optional[Dict[str, Any]] = None
    inline_query: Optional[Dict[str, Any]] = None
    chosen_inline_result: Optional[Dict[str, Any]] = None
    callback_query: Optional[Dict[str, Any]] = None
    shipping_query: Optional[Dict[str, Any]] = None
    pre_checkout_query: Optional[Dict[str, Any]] = None
    poll: Optional[Dict[str, Any]] = None
    poll_answer: Optional[Dict[str, Any]] = None
    my_chat_member: Optional[Dict[str, Any]] = None
    chat_member: Optional[Dict[str, Any]] = None
    chat_join_request: Optional[Dict[str, Any]] = None

class StripeWebhookPayload(BaseModel):
    id: str = Field(..., description="Stripe event ID")
    object: str = Field(default="event", description="Type d'objet Stripe")
    api_version: Optional[str] = Field(None, description="Version API Stripe")
    created: int = Field(..., description="Timestamp de création")
    data: Dict[str, Any] = Field(..., description="Données de l'événement")
    livemode: bool = Field(..., description="Mode production")
    pending_webhooks: int = Field(..., description="Webhooks en attente")
    request: Optional[Dict[str, Any]] = Field(None, description="Informations de requête")
    type: str = Field(..., description="Type d'événement Stripe")

class GoogleWebhookPayload(BaseModel):
    kind: str = Field(..., description="Type de ressource Google")
    id: str = Field(..., description="ID unique")
    token: Optional[str] = Field(None, description="Token de synchronisation")
    resource_id: Optional[str] = Field(None, description="ID de ressource")
    resource_uri: Optional[HttpUrl] = Field(None, description="URI de la ressource")
    channel_id: Optional[str] = Field(None, description="ID du canal")
    channel_token: Optional[str] = Field(None, description="Token du canal")
    channel_expiration: Optional[datetime] = Field(None, description="Expiration du canal")
    payload: Optional[Dict[str, Any]] = Field(None, description="Données supplémentaires")

class UploadRequest(BaseModel):
    user_id: str = Field(..., description="ID utilisateur")
    file_type: str = Field(..., description="Type de fichier")
    file_name: str = Field(..., description="Nom du fichier")
    file_size: int = Field(..., description="Taille du fichier en bytes")
    mime_type: str = Field(..., description="Type MIME")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexte additionnel")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Métadonnées")

class UploadResponse(BaseModel):
    upload_id: str = Field(..., description="ID de l'upload")
    url: HttpUrl = Field(..., description="URL de téléchargement")
    expires_at: datetime = Field(..., description="Date d'expiration")
    file_info: Dict[str, Any] = Field(..., description="Informations sur le fichier")

class OnboardingSubmitRequest(BaseModel):
    user_id: str = Field(..., description="ID utilisateur")
    business_name: str = Field(..., description="Nom de l'entreprise")
    business_type: str = Field(..., description="Type d'entreprise")
    website: Optional[HttpUrl] = Field(None, description="Site web")
    phone: Optional[str] = Field(None, description="Téléphone")
    address: Optional[Dict[str, Any]] = Field(None, description="Adresse")
    preferences: Optional[Dict[str, Any]] = Field(None, description="Préférences")
    goals: Optional[List[str]] = Field(None, description="Objectifs")
    tools: Optional[List[str]] = Field(None, description="Outils utilisés")

class OnboardingSubmitResponse(BaseModel):
    success: bool = Field(..., description="Succès de l'opération")
    message: str = Field(..., description="Message de confirmation")
    next_steps: Optional[List[str]] = Field(None, description="Prochaines étapes")

class ModuleStatus(BaseModel):
    module_name: str = Field(..., description="Nom du module")
    status: str = Field(..., description="Statut du module")
    version: Optional[str] = Field(None, description="Version")
    last_updated: Optional[datetime] = Field(None, description="Dernière mise à jour")
    dependencies: Optional[List[str]] = Field(None, description="Dépendances")
    config: Optional[Dict[str, Any]] = Field(None, description="Configuration")

class ModulesStatusResponse(BaseModel):
    modules: List[ModuleStatus] = Field(default_factory=list, description="Statut des modules")
    system_status: str = Field(..., description="Statut global du système")
    last_check: datetime = Field(default_factory=datetime.utcnow, description="Dernière vérification")

class AnalyticsEventRequest(BaseModel):
    event_name: str = Field(..., description="Nom de l'événement")
    user_id: Optional[str] = Field(None, description="ID utilisateur")
    session_id: Optional[str] = Field(None, description="ID de session")
    properties: Optional[Dict[str, Any]] = Field(None, description="Propriétés de l'événement")
    timestamp: Optional[datetime] = Field(None, description="Timestamp de l'événement")
    context: Optional[Dict[str, Any]] = Field(None, description="Contexte")

class AnalyticsQueryRequest(BaseModel):
    start_date: Optional[datetime] = Field(None, description="Date de début")
    end_date: Optional[datetime] = Field(None, description="Date de fin")
    event_names: Optional[List[str]] = Field(None, description="Noms d'événements à filtrer")
    user_ids: Optional[List[str]] = Field(None, description="IDs utilisateur à filtrer")
    group_by: Optional[str] = Field(None, description="Grouper par (day, week, month)")
    metrics: Optional[List[str]] = Field(None, description="Métriques à calculer")

class AnalyticsResponse(BaseModel):
    events: List[Dict[str, Any]] = Field(default_factory=list, description="Événements")
    metrics: Optional[Dict[str, Any]] = Field(None, description="Métriques calculées")
    summary: Optional[Dict[str, Any]] = Field(None, description="Résumé")
    period: Dict[str, datetime] = Field(..., description="Période analysée")