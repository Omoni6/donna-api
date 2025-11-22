#!/usr/bin/env python3
"""
Exemple d'utilisation des tools Donna Worker
Ce script montre comment utiliser les tools pour interagir avec l'API FastAPI
"""

import asyncio
import os
import logging
from typing import Dict, Any, Optional

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import des tools
from worker_tools import (
    omoni_tools,
    agent_tools,
    create_meeting_event,
    create_client_lead,
    notify_team,
    create_project_channel,
    log_activity,
    planifi_agent_task,
    publie_agent_task,
    cree_agent_task,
    commercial_agent_task
)

async def example_omoni_tools():
    """Exemple d'utilisation des tools OMONI"""
    logger.info("🚀 Démarrage exemple OMONI Tools")
    
    try:
        # Exemple 1: Créer un événement calendrier
        logger.info("📅 Création d'un événement calendrier...")
        event_data = {
            "title": "Réunion avec client",
            "start_time": "2024-12-01T14:00:00Z",
            "end_time": "2024-12-01T15:00:00Z",
            "description": "Présentation du nouveau produit"
        }
        
        event = await omoni_tools.create_calendar_event(event_data)
        logger.info(f"✅ Événement créé: {event.get('id')}")
        
        # Exemple 2: Créer un lead CRM
        logger.info("👤 Création d'un lead CRM...")
        lead = await create_client_lead(
            email="client@example.com",
            name="Jean Dupont",
            phone="+33612345678",
            source="Appel entrant"
        )
        logger.info(f"✅ Lead créé: {lead.get('id')}")
        
        # Exemple 3: Envoyer une notification
        logger.info("🔔 Envoi d'une notification...")
        notification = await notify_team(
            title="Nouveau lead",
            message="Un nouveau lead a été créé par l'agent"
        )
        logger.info(f"✅ Notification envoyée: {notification.get('id')}")
        
        # Exemple 4: Créer un canal Slack
        logger.info("💬 Création d'un canal Slack...")
        channel = await create_project_channel(
            project_name="Projet Alpha"
        )
        logger.info(f"✅ Canal créé: {channel.get('id')}")
        
        # Exemple 5: Logger une activité
        logger.info("💭 Logging d'une activité...")
        activity = await log_activity(
            activity="Agent a traité la demande du client"
        )
        logger.info(f"✅ Activité loggée: {activity.get('id')}")
        
    except Exception as e:
        logger.error(f"❌ Erreur OMONI Tools: {str(e)}")
        raise

async def example_agent_tools():
    """Exemple d'utilisation des tools Agent"""
    logger.info("🚀 Démarrage exemple Agent Tools")
    
    try:
        # Exemple 1: Planifier une tâche (Agent Planifi)
        logger.info("📅 Planification d'une tâche...")
        task = await planifi_agent_task(
            task_description="Préparer la présentation client",
            deadline="2024-12-02T10:00:00Z",
            priority="high"
        )
        logger.info(f"✅ Tâche planifiée: {task.get('id')}")
        
        # Exemple 2: Publier du contenu (Agent Publie)
        logger.info("📢 Publication de contenu...")
        publication = await publie_agent_task(
            content="🎯 Nouvelle offre spéciale! Contactez-nous pour plus d'informations.",
            platform="telegram",
            target_audience="-1001234567890"
        )
        logger.info(f"✅ Contenu publié: {publication.get('message_id')}")
        
        # Exemple 3: Créer un document (Agent Cree)
        logger.info("🎨 Création d'un document...")
        document = await cree_agent_task(
            creation_type="document",
            specifications={
                "filename": "rapport_ventes.txt",
                "content": "Rapport de ventes du mois de novembre 2024..."
            }
        )
        logger.info(f"✅ Document créé: {document.get('id')}")
        
        # Exemple 4: Action commerciale (Agent Commercial)
        logger.info("💼 Action commerciale...")
        commercial_action = await commercial_agent_task(
            action="create_lead",
            client_data={
                "email": "prospect@entreprise.com",
                "name": "Marie Martin",
                "phone": "+33687654321"
            }
        )
        logger.info(f"✅ Lead commercial créé: {commercial_action.get('id')}")
        
        # Exemple 5: Créer un paiement
        logger.info("💳 Création d'un paiement...")
        payment = await commercial_agent_task(
            action="create_payment",
            client_data={
                "amount": 15000,  # 150.00 EUR en centimes
                "currency": "eur",
                "description": "Paiement pour service premium"
            }
        )
        logger.info(f"✅ Paiement créé: {payment.get('id')}")
        
    except Exception as e:
        logger.error(f"❌ Erreur Agent Tools: {str(e)}")
        raise

async def example_analytics_tracking():
    """Exemple de tracking analytics"""
    logger.info("📊 Démarrage exemple Analytics")
    
    try:
        # Tracker différents types d'événements
        events = [
            ("agent_executed", {"agent_type": "planifi", "task_count": 5}),
            ("webhook_received", {"source": "telegram", "message_type": "text"}),
            ("user_action", {"action": "login", "user_id": "user_123"}),
            ("payment_processed", {"amount": 10000, "currency": "eur", "status": "success"})
        ]
        
        for event_type, event_data in events:
            logger.info(f"📈 Tracking événement: {event_type}")
            result = await agent_tools.track_analytics_event(event_type, event_data)
            logger.info(f"✅ Événement tracké: {result.get('id')}")
        
        # Obtenir des insights
        logger.info("📊 Récupération d'insights...")
        insights = await agent_tools.get_analytics_insights("user_engagement", "30d")
        logger.info(f"✅ Insights récupérés: {insights}")
        
    except Exception as e:
        logger.error(f"❌ Erreur Analytics: {str(e)}")
        raise

async def example_multi_tenant():
    """Exemple d'utilisation multi-tenant"""
    logger.info("🏢 Démarrage exemple Multi-Tenant")
    
    try:
        tenant_id = "tenant_abc123"
        
        # Créer des ressources pour un tenant spécifique
        logger.info(f"🔧 Création ressources pour tenant: {tenant_id}")
        
        # Créer un événement calendrier
        event = await omoni_tools.create_calendar_event(
            {
                "title": "Réunion tenant spécifique",
                "start_time": "2024-12-03T09:00:00Z",
                "end_time": "2024-12-03T10:00:00Z",
                "description": "Réunion pour tenant spécifique"
            },
            tenant_id=tenant_id
        )
        logger.info(f"✅ Événement tenant créé: {event.get('id')}")
        
        # Créer un lead CRM
        lead = await create_client_lead(
            email="tenant@company.com",
            name="Tenant User",
            source="Tenant Portal",
            tenant_id=tenant_id
        )
        logger.info(f"✅ Lead tenant créé: {lead.get('id')}")
        
        # Envoyer une notification
        notification = await notify_team(
            title="Activité tenant",
            message=f"Nouvelle activité détectée pour tenant {tenant_id}",
            tenant_id=tenant_id
        )
        logger.info(f"✅ Notification tenant envoyée: {notification.get('id')}")
        
    except Exception as e:
        logger.error(f"❌ Erreur Multi-Tenant: {str(e)}")
        raise

async def main():
    """Fonction principale pour exécuter tous les exemples"""
    logger.info("🎯 Démarrage des exemples Donna Worker Tools")
    
    try:
        # Exécuter les exemples
        await example_omoni_tools()
        logger.info("✅ Exemples OMONI Tools terminés")
        
        await example_agent_tools()
        logger.info("✅ Exemples Agent Tools terminés")
        
        await example_analytics_tracking()
        logger.info("✅ Exemples Analytics terminés")
        
        await example_multi_tenant()
        logger.info("✅ Exemples Multi-Tenant terminés")
        
        logger.info("🎉 Tous les exemples ont été exécutés avec succès!")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'exécution des exemples: {str(e)}")
        raise

if __name__ == "__main__":
    # Configuration des variables d'environnement (à adapter selon votre configuration)
    os.environ.setdefault("OMONI_API_URL", "http://donna-api:8000")
    os.environ.setdefault("OMONI_API_KEY", "donna-api-key-production")
    os.environ.setdefault("DONNA_API_URL", "http://donna-api:8000")
    os.environ.setdefault("DONNA_API_KEY", "donna-api-key-production")
    os.environ.setdefault("DEFAULT_TELEGRAM_CHAT_ID", "-1001234567890")
    
    # Lancer l'exemple
    asyncio.run(main())