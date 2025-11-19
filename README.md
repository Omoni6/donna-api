# Donna API

Une API légère pour gérer les webhooks Telegram et Slack.

## Structure du projet

```
/app
  /core
    config.py          # Configuration de l'application
    security.py        # Sécurité et validation
    logging.py         # Configuration des logs
  /routers
    root.py            # Routes racine
    telegram.py        # Routes Telegram
    slack.py           # Routes Slack
    events.py          # Routes événements
  /services
    telegram_service.py   # Logique métier Telegram
    slack_service.py      # Logique métier Slack
    routing_service.py    # Service de routage
  /db
    database.py        # Configuration DB
    models.py          # Modèles de données
  /utils
    http.py            # Utilitaires HTTP
    validators.py      # Validateurs

main.py              # Point d'entrée
requirements.txt     # Dépendances
```

## Installation

```bash
pip install -r requirements.txt
```

## Lancement

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /v1` - Health check
- `POST /api/v1/telegram/webhook` - Webhook Telegram
- `POST /api/v1/slack/events` - Événements Slack

## Déploiement

L'application est conçue pour être déployée avec Docker sur un VPS.