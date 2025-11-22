import logging
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List

from app.models.analytics import (
    AnalyticsEvent, AnalyticsMetric, EventType,
    UserAnalytics, TenantAnalytics, AnalyticsSummary,
    RealTimeAnalytics, FunnelAnalysis, CohortAnalysis
)
from app.core.config import settings

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Service pour gérer l'analytique"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        # Dans une vraie implémentation, on utiliserait une base de données
        # ou un service comme BigQuery, Mixpanel, etc.
    
    async def track_event(self, event_name: str, user_id: Optional[str] = None,
                         session_id: Optional[str] = None, tenant_id: str = None,
                         properties: Optional[Dict[str, Any]] = None,
                         context: Optional[Dict[str, Any]] = None) -> AnalyticsEvent:
        """
        Enregistre un événement analytique
        
        Args:
            event_name: Nom de l'événement
            user_id: ID de l'utilisateur
            session_id: ID de session
            tenant_id: ID du tenant
            properties: Propriétés de l'événement
            context: Contexte additionnel
        
        Returns:
            L'événement créé
        """
        try:
            # Déterminer le type d'événement
            event_type = self._get_event_type(event_name)
            
            # Créer l'événement
            event = AnalyticsEvent(
                id=str(uuid.uuid4()),
                event_name=event_name,
                event_type=event_type,
                user_id=user_id,
                session_id=session_id or self._generate_session_id(),
                tenant_id=tenant_id or settings.DEFAULT_TENANT,
                properties=properties or {},
                context=context or {}
            )
            
            self.logger.info(f"📊 Événement tracké: {event_name} - User: {user_id} - Tenant: {tenant_id}")
            
            # Dans une vraie implémentation, on sauvegarderait dans la base de données
            # await self._save_event(event)
            
            return event
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors du tracking de l'événement: {str(e)}", exc_info=True)
            raise e
    
    def _get_event_type(self, event_name: str) -> EventType:
        """Détermine le type d'événement à partir du nom"""
        event_name_lower = event_name.lower()
        
        if "page_view" in event_name_lower or "view" in event_name_lower:
            return EventType.PAGE_VIEW
        elif "click" in event_name_lower or "button" in event_name_lower:
            return EventType.BUTTON_CLICK
        elif "submit" in event_name_lower or "form" in event_name_lower:
            return EventType.FORM_SUBMIT
        elif "login" in event_name_lower or "signin" in event_name_lower:
            return EventType.LOGIN
        elif "logout" in event_name_lower or "signout" in event_name_lower:
            return EventType.LOGOUT
        elif "signup" in event_name_lower or "register" in event_name_lower:
            return EventType.SIGNUP
        elif "purchase" in event_name_lower or "buy" in event_name_lower:
            return EventType.PURCHASE
        elif "upgrade" in event_name_lower or "subscription" in event_name_lower:
            return EventType.UPGRADE
        elif "agent" in event_name_lower and "execute" in event_name_lower:
            return EventType.AGENT_EXECUTION
        elif "webhook" in event_name_lower:
            return EventType.WEBHOOK_RECEIVED
        elif "upload" in event_name_lower or "file" in event_name_lower:
            return EventType.FILE_UPLOAD
        elif "error" in event_name_lower or "exception" in event_name_lower:
            return EventType.ERROR
        else:
            return EventType.FEATURE_USED
    
    def _generate_session_id(self) -> str:
        """Génère un ID de session"""
        return f"session_{uuid.uuid4().hex[:12]}"
    
    async def get_user_analytics(self, user_id: str, tenant_id: str,
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> UserAnalytics:
        """
        Récupère les analytics pour un utilisateur spécifique
        
        Args:
            user_id: ID de l'utilisateur
            tenant_id: ID du tenant
            start_date: Date de début
            end_date: Date de fin
        
        Returns:
            Analytics de l'utilisateur
        """
        try:
            # Définir la période par défaut
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            self.logger.info(f"📈 Récupération des analytics pour l'utilisateur: {user_id}")
            
            # Dans une vraie implémentation, on irait chercher dans la base de données
            # Simuler des données pour l'instant
            analytics = UserAnalytics(
                user_id=user_id,
                total_events=150,
                first_seen=start_date,
                last_seen=end_date,
                session_count=25,
                avg_session_duration=180.5,
                top_events=[
                    {"event_name": "page_view", "count": 50},
                    {"event_name": "button_click", "count": 30},
                    {"event_name": "agent_execution", "count": 20}
                ],
                conversion_rate=0.15,
                lifetime_value=299.99
            )
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération des analytics utilisateur: {str(e)}", exc_info=True)
            raise e
    
    async def get_tenant_analytics(self, tenant_id: str,
                                 start_date: Optional[datetime] = None,
                                 end_date: Optional[datetime] = None) -> TenantAnalytics:
        """
        Récupère les analytics pour un tenant
        
        Args:
            tenant_id: ID du tenant
            start_date: Date de début
            end_date: Date de fin
        
        Returns:
            Analytics du tenant
        """
        try:
            # Définir la période par défaut
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            self.logger.info(f"📊 Récupération des analytics pour le tenant: {tenant_id}")
            
            # Simuler des données pour l'instant
            analytics = TenantAnalytics(
                tenant_id=tenant_id,
                total_users=1250,
                active_users=850,
                total_events=15000,
                events_today=500,
                events_this_week=3500,
                events_this_month=12000,
                top_events=[
                    {"event_name": "page_view", "count": 8000},
                    {"event_name": "login", "count": 2000},
                    {"event_name": "agent_execution", "count": 1500}
                ],
                user_growth=[
                    {"date": "2024-01-01", "users": 1000},
                    {"date": "2024-01-15", "users": 1125},
                    {"date": "2024-01-30", "users": 1250}
                ],
                revenue=15000.50,
                mrr=2500.00
            )
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération des analytics tenant: {str(e)}", exc_info=True)
            raise e
    
    async def get_real_time_analytics(self, tenant_id: str) -> RealTimeAnalytics:
        """
        Récupère les analytics en temps réel
        
        Args:
            tenant_id: ID du tenant
        
        Returns:
            Analytics en temps réel
        """
        try:
            self.logger.info(f"⚡ Récupération des analytics en temps réel pour le tenant: {tenant_id}")
            
            # Simuler des données en temps réel
            analytics = RealTimeAnalytics(
                active_users=45,
                events_last_5min=125,
                events_last_hour=850,
                top_pages=[
                    {"page": "/dashboard", "views": 250},
                    {"page": "/agents", "views": 180},
                    {"page": "/analytics", "views": 120}
                ],
                top_events=[
                    {"event": "page_view", "count": 300},
                    {"event": "button_click", "count": 200},
                    {"event": "agent_execution", "count": 150}
                ],
                geographic_data=[
                    {"country": "France", "users": 25},
                    {"country": "USA", "users": 15},
                    {"country": "UK", "users": 5}
                ],
                device_breakdown={
                    "desktop": 30,
                    "mobile": 12,
                    "tablet": 3
                }
            )
            
            return analytics
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération des analytics temps réel: {str(e)}", exc_info=True)
            raise e
    
    async def get_summary_analytics(self, tenant_id: str,
                                  start_date: Optional[datetime] = None,
                                  end_date: Optional[datetime] = None) -> AnalyticsSummary:
        """
        Récupère un résumé des analytics
        
        Args:
            tenant_id: ID du tenant
            start_date: Date de début
            end_date: Date de fin
        
        Returns:
            Résumé des analytics
        """
        try:
            # Définir la période par défaut
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            self.logger.info(f"📋 Récupération du résumé des analytics pour le tenant: {tenant_id}")
            
            # Simuler un résumé
            summary = AnalyticsSummary(
                total_events=25000,
                unique_users=1200,
                avg_events_per_user=20.8,
                conversion_rate=0.12,
                revenue=25000.00,
                growth_rate=0.15,
                top_performing_content=[
                    {"content": "Landing Page", "views": 5000, "conversion": 0.08},
                    {"content": "Pricing Page", "views": 3000, "conversion": 0.12},
                    {"content": "Blog Post", "views": 2000, "conversion": 0.05}
                ],
                period={
                    "start": start_date,
                    "end": end_date
                }
            )
            
            return summary
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la récupération du résumé: {str(e)}", exc_info=True)
            raise e
    
    async def create_funnel_analysis(self, tenant_id: str, funnel_name: str,
                                   steps: List[str], start_date: Optional[datetime] = None,
                                   end_date: Optional[datetime] = None) -> FunnelAnalysis:
        """
        Crée une analyse de funnel
        
        Args:
            tenant_id: ID du tenant
            funnel_name: Nom du funnel
            steps: Étapes du funnel
            start_date: Date de début
            end_date: Date de fin
        
        Returns:
            Analyse du funnel
        """
        try:
            # Définir la période par défaut
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)
            
            self.logger.info(f"🔄 Création de l'analyse de funnel: {funnel_name}")
            
            # Simuler une analyse de funnel
            funnel_steps = []
            total_users = 1000
            
            for i, step in enumerate(steps):
                users_at_step = int(total_users * (0.8 ** i))  # 80% de conversion par étape
                conversion_rate = 0.8 if i > 0 else 1.0
                drop_off_rate = 0.2 if i > 0 else 0.0
                
                funnel_steps.append({
                    "name": f"Étape {i+1}: {step}",
                    "event_name": step,
                    "count": users_at_step,
                    "conversion_rate": conversion_rate,
                    "drop_off_rate": drop_off_rate
                })
            
            analysis = FunnelAnalysis(
                name=funnel_name,
                steps=funnel_steps,
                total_conversion_rate=0.8 ** (len(steps) - 1) if len(steps) > 1 else 1.0,
                period={
                    "start": start_date,
                    "end": end_date
                }
            )
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la création de l'analyse de funnel: {str(e)}", exc_info=True)
            raise e
    
    async def create_cohort_analysis(self, tenant_id: str, period_type: str = "week",
                                   periods: int = 12) -> CohortAnalysis:
        """
        Crée une analyse de cohorte
        
        Args:
            tenant_id: ID du tenant
            period_type: Type de période (day, week, month)
            periods: Nombre de périodes
        
        Returns:
            Analyse de cohorte
        """
        try:
            self.logger.info(f"📊 Création de l'analyse de cohorte: {period_type} - {periods} périodes")
            
            # Simuler une analyse de cohorte
            cohorts = []
            average_retention = []
            
            for i in range(min(5, periods)):  # Limiter à 5 cohortes pour la démo
                cohort_date = datetime.utcnow() - timedelta(
                    days=i*7 if period_type == "week" else i*30 if period_type == "month" else i
                )
                
                cohort_size = 100 - (i * 10)  # Taille décroissante
                retention_rates = []
                
                for j in range(periods):
                    # Taux de rétention décroissant
                    retention = max(0.0, 1.0 - (j * 0.1) - (i * 0.05))
                    retention_rates.append(retention)
                
                cohorts.append({
                    "cohort_date": cohort_date,
                    "cohort_size": cohort_size,
                    "retention_rates": retention_rates,
                    "periods": [f"{period_type}_{j}" for j in range(periods)]
                })
            
            # Calculer la rétention moyenne
            for j in range(periods):
                avg_retention = sum(cohort["retention_rates"][j] for cohort in cohorts) / len(cohorts)
                average_retention.append(avg_retention)
            
            analysis = CohortAnalysis(
                cohorts=cohorts,
                average_retention=average_retention,
                period_type=period_type
            )
            
            return analysis
            
        except Exception as e:
            self.logger.error(f"❌ Erreur lors de la création de l'analyse de cohorte: {str(e)}", exc_info=True)
            raise e

# Singleton instance
analytics_service = AnalyticsService()