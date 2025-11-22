# Donna Worker Tools

Cette bibliothèque fournit des outils Python pour permettre à Donna Worker (Agent Zero) d'interagir avec l'API FastAPI OMONI.

## Architecture

```
Donna Worker (Agent Zero) → Worker Tools → FastAPI OMONI → Services
```

## Installation

```bash
pip install httpx
```

## Configuration

Configurez les variables d'environnement suivantes :

```bash
# URL et clé API de l'API FastAPI
OMONI_API_URL=http://donna-api:8000
OMONI_API_KEY=donna-api-key-production
DONNA_API_URL=http://donna-api:8000
DONNA_API_KEY=donna-api-key-production

# Configuration optionnelle
DEFAULT_TELEGRAM_CHAT_ID=-1001234567890
```

## Utilisation rapide

```python
import asyncio
from worker_tools import (
    omoni_tools,
    create_meeting_event,
    create_client_lead,
    planifi_agent_task,
    publie_agent_task
)

async def main():
    # Créer un événement calendrier
    event = await create_meeting_event(
        title="Réunion client",
        start_time="2024-12-01T14:00:00Z",
        end_time="2024-12-01T15:00:00Z",
        description="Présentation produit"
    )
    
    # Créer un lead CRM
    lead = await create_client_lead(
        email="client@example.com",
        name="Jean Dupont",
        phone="+33612345678"
    )
    
    # Planifier une tâche (Agent Planifi)
    task = await planifi_agent_task(
        task_description="Préparer présentation",
        deadline="2024-12-02T10:00:00Z",
        priority="high"
    )
    
    # Publier du contenu (Agent Publie)
    post = await publie_agent_task(
        content="Nouvelle offre spéciale!",
        platform="telegram"
    )

asyncio.run(main())
```

## Tools disponibles

### OMONI Tools (`tools_omoni.py`)

#### Calendrier
- `create_calendar_event(event_data, tenant_id=None)` - Créer un événement
- `get_calendar_events(tenant_id=None, limit=10)` - Récupérer les événements

#### CRM
- `create_crm_lead(email, name, phone=None, source="Donna Worker", tenant_id=None)` - Créer un lead
- `get_crm_leads(status=None, tenant_id=None)` - Récupérer les leads

#### Slack
- `create_slack_channel(channel_name, description=None, tenant_id=None)` - Créer un canal
- `send_slack_message(channel, text, tenant_id=None)` - Envoyer un message

#### Bucket (Stockage)
- `upload_to_bucket(filename, content, content_type="text/plain", tenant_id=None)` - Uploader un fichier

#### Chat
- `send_chat_message(message, sender="Donna Worker", tenant_id=None)` - Envoyer un message chat

#### Notifications
- `send_notification(title, message, notification_type="info", tenant_id=None)` - Envoyer une notification

#### Workflows
- `execute_workflow(workflow_id, parameters=None, tenant_id=None)` - Exécuter un workflow

#### Analytics
- `get_analytics_dashboard(tenant_id=None)` - Récupérer le dashboard analytics

### Agent Tools (`tools_agents.py`)

#### Telegram
- `send_telegram_message(chat_id, message, parse_mode="HTML", tenant_id=None)` - Envoyer un message Telegram

#### Stripe
- `create_stripe_payment(amount, currency="eur", description=None, tenant_id=None)` - Créer un paiement

#### Analytics
- `track_analytics_event(event_type, event_data, tenant_id=None)` - Tracker un événement
- `get_analytics_insights(metric, timeframe="7d", tenant_id=None)` - Obtenir des insights

#### Google
- `process_google_webhook(webhook_data, tenant_id=None)` - Traiter un webhook Google

### Fonctions utilitaires pour agents spécifiques

#### Agent Planifi
- `planifi_agent_task(task_description, deadline, priority="medium", tenant_id=None)` - Planifier une tâche

#### Agent Publie
- `publie_agent_task(content, platform="telegram", target_audience=None, tenant_id=None)` - Publier du contenu

#### Agent Cree
- `cree_agent_task(creation_type, specifications, tenant_id=None)` - Créer quelque chose (document, canal, etc.)

#### Agent Commercial
- `commercial_agent_task(action, client_data, tenant_id=None)` - Effectuer une action commerciale

## Support multi-tenant

Tous les tools supportent le paramètre `tenant_id` pour le multi-tenant :

```python
# Pour un tenant spécifique
event = await create_meeting_event(
    title="Réunion tenant",
    start_time="2024-12-01T14:00:00Z",
    end_time="2024-12-01T15:00:00Z",
    tenant_id="tenant_abc123"
)
```

## Gestion des erreurs

Les tools lèvent des exceptions en cas d'erreur :

```python
try:
    result = await create_meeting_event(event_data)
    print(f"Succès: {result}")
except Exception as e:
    print(f"Erreur: {e}")
```

## Logging

Les tools utilisent le module `logging` de Python. Configurez le niveau de log :

```python
import logging
logging.getLogger('worker_tools').setLevel(logging.DEBUG)
```

## Exemple complet

Voir `example_usage.py` pour des exemples complets d'utilisation.

## Architecture des services

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  Donna Worker   │───▶│   Worker Tools   │───▶│   FastAPI       │
│  (Agent Zero)   │    │   (HTTP Client)  │    │   OMONI API     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                                        │
                                                        ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Services      │◀───│   OMONI Router   │◀───│   Webhooks      │
│   (Calendar,    │    │   Endpoints      │    │   (Telegram,    │
│    CRM, Slack,  │    │                  │    │    Stripe,      │
│    etc.)        │    │                  │    │    Google)      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

## Sécurité

- Toutes les requêtes utilisent l'authentification par API Key
- Support du multi-tenant via headers X-Tenant-ID
- Communication sécurisée entre services
- Validation des données côté FastAPI

## Tests

Pour tester les tools, assurez-vous que l'API FastAPI est en cours d'exécution :

```bash
# Démarrer l'API FastAPI
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

# Dans un autre terminal, tester les tools
cd worker_tools
python example_usage.py
```

## Contribution

Pour ajouter de nouveaux tools :

1. Créer la fonction dans le fichier approprié (`tools_omoni.py` ou `tools_agents.py`)
2. Ajouter la fonction à la liste `__all__`
3. Mettre à jour ce README
4. Ajouter des exemples dans `example_usage.py`

## Support

Pour toute question ou problème, veuillez consulter la documentation de l'API FastAPI ou créer une issue.