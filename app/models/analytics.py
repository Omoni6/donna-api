from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

class EventType(str, Enum):
    PAGE_VIEW = "page_view"
    BUTTON_CLICK = "button_click"
    FORM_SUBMIT = "form_submit"
    LOGIN = "login"
    LOGOUT = "logout"
    SIGNUP = "signup"
    PURCHASE = "purchase"
    UPGRADE = "upgrade"
    AGENT_EXECUTION = "agent_execution"
    WEBHOOK_RECEIVED = "webhook_received"
    FILE_UPLOAD = "file_upload"
    ERROR = "error"
    FEATURE_USED = "feature_used"

class AnalyticsEvent(BaseModel):
    id: str = Field(..., description="ID unique de l'événement")
    event_name: str = Field(..., description="Nom de l'événement")
    event_type: EventType = Field(..., description="Type d'événement")
    user_id: Optional[str] = Field(None, description="ID utilisateur")
    session_id: Optional[str] = Field(None, description="ID de session")
    tenant_id: str = Field(..., description="ID du tenant")
    properties: Dict[str, Any] = Field(default_factory=dict, description="Propriétés de l'événement")
    context: Dict[str, Any] = Field(default_factory=dict, description="Contexte")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Date de création")

class AnalyticsMetric(BaseModel):
    name: str = Field(..., description="Nom de la métrique")
    value: float = Field(..., description="Valeur de la métrique")
    unit: Optional[str] = Field(None, description="Unité de mesure")
    period: str = Field(..., description="Période (day, week, month)")
    start_date: datetime = Field(..., description="Date de début")
    end_date: datetime = Field(..., description="Date de fin")
    dimensions: Optional[Dict[str, Any]] = Field(None, description="Dimensions")

class UserAnalytics(BaseModel):
    user_id: str = Field(..., description="ID utilisateur")
    total_events: int = Field(..., description="Nombre total d'événements")
    first_seen: datetime = Field(..., description="Première visite")
    last_seen: datetime = Field(..., description="Dernière visite")
    session_count: int = Field(..., description="Nombre de sessions")
    avg_session_duration: float = Field(..., description="Durée moyenne de session")
    top_events: List[Dict[str, Any]] = Field(default_factory=list, description="Top événements")
    conversion_rate: Optional[float] = Field(None, description="Taux de conversion")
    lifetime_value: Optional[float] = Field(None, description="Valeur vie client")

class TenantAnalytics(BaseModel):
    tenant_id: str = Field(..., description="ID du tenant")
    total_users: int = Field(..., description="Nombre total d'utilisateurs")
    active_users: int = Field(..., description="Nombre d'utilisateurs actifs")
    total_events: int = Field(..., description="Nombre total d'événements")
    events_today: int = Field(..., description="Événements aujourd'hui")
    events_this_week: int = Field(..., description="Événements cette semaine")
    events_this_month: int = Field(..., description="Événements ce mois")
    top_events: List[Dict[str, Any]] = Field(default_factory=list, description="Top événements")
    user_growth: List[Dict[str, Any]] = Field(default_factory=list, description="Croissance utilisateurs")
    revenue: Optional[float] = Field(None, description="Revenu total")
    mrr: Optional[float] = Field(None, description="MRR (Monthly Recurring Revenue)")

class FunnelStep(BaseModel):
    name: str = Field(..., description="Nom de l'étape")
    event_name: str = Field(..., description="Nom de l'événement")
    count: int = Field(..., description="Nombre d'événements")
    conversion_rate: float = Field(..., description="Taux de conversion depuis l'étape précédente")
    drop_off_rate: float = Field(..., description="Taux d'abandon")

class FunnelAnalysis(BaseModel):
    name: str = Field(..., description="Nom du funnel")
    steps: List[FunnelStep] = Field(..., description="Étapes du funnel")
    total_conversion_rate: float = Field(..., description="Taux de conversion total")
    period: Dict[str, datetime] = Field(..., description="Période analysée")

class CohortData(BaseModel):
    cohort_date: datetime = Field(..., description="Date de la cohorte")
    cohort_size: int = Field(..., description="Taille de la cohorte")
    retention_rates: List[float] = Field(..., description="Taux de rétention par période")
    periods: List[str] = Field(..., description="Périodes (day, week, month)")

class CohortAnalysis(BaseModel):
    cohorts: List[CohortData] = Field(..., description="Données des cohortes")
    average_retention: List[float] = Field(..., description="Rétention moyenne")
    period_type: str = Field(..., description="Type de période")

class RealTimeAnalytics(BaseModel):
    active_users: int = Field(..., description="Utilisateurs actifs en temps réel")
    events_last_5min: int = Field(..., description="Événements des 5 dernières minutes")
    events_last_hour: int = Field(..., description="Événements de la dernière heure")
    top_pages: List[Dict[str, Any]] = Field(default_factory=list, description="Pages les plus visitées")
    top_events: List[Dict[str, Any]] = Field(default_factory=list, description="Événements les plus fréquents")
    geographic_data: List[Dict[str, Any]] = Field(default_factory=list, description="Données géographiques")
    device_breakdown: Dict[str, int] = Field(default_factory=dict, description="Répartition par appareil")

class AnalyticsSummary(BaseModel):
    total_events: int = Field(..., description="Total des événements")
    unique_users: int = Field(..., description="Utilisateurs uniques")
    avg_events_per_user: float = Field(..., description="Moyenne d'événements par utilisateur")
    conversion_rate: Optional[float] = Field(None, description="Taux de conversion global")
    revenue: Optional[float] = Field(None, description="Revenu total")
    growth_rate: float = Field(..., description="Taux de croissance")
    top_performing_content: List[Dict[str, Any]] = Field(default_factory=list, description="Contenu le plus performant")
    period: Dict[str, datetime] = Field(..., description="Période analysée")