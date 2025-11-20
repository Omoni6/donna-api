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
Dockerfile          # Image Docker
```

## Installation locale

```bash
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Endpoints

- `GET /v1` - Health check
- `POST /api/v1/telegram/webhook` - Webhook Telegram
- `POST /api/v1/slack/events` - Événements Slack

## 🚀 Déploiement VPS avec Docker

**⚠️ Procédure propre : Ce projet utilise le docker-compose principal du VPS**

### 1. Sur le VPS

```bash
# Clone du repo
git clone https://github.com/Omoni6/donna-api.git /opt/donna-api

# Build depuis le docker-compose principal du VPS
cd /root  # ou où est ton docker-compose.yml principal
docker compose build donna-api
docker compose up -d donna-api
```

### 2. Configuration Traefik

Le service est automatiquement configuré via labels dans le docker-compose principal :
- Domaine : `api.omoniprestanceholding.com`
- SSL : Let's Encrypt automatique
- Reverse proxy : Traefik

### 3. Tester le déploiement

```bash
# Test health check
curl https://api.omoniprestanceholding.com/v1

# Test webhooks
curl -X POST https://api.omoniprestanceholding.com/api/v1/telegram/webhook \
  -H "Content-Type: application/json" \
  -d '{"update_id": 123, "message": {"text": "test"}}'
```

## 📁 Fichiers de déploiement

- `Dockerfile` - Image ultra-légère
- `traefik-compose.yml` - Configuration Traefik (si besoin)
- `deploy.sh` - Script d'installation VPS
- `test-api.sh` - Script de test
- `DEPLOYMENT.md` - Guide complet de déploiement

## 🔧 Pourquoi pas de docker-compose.yml interne ?

Pour suivre les bonnes pratiques de production :
- ✅ Utilisation du docker-compose principal du VPS
- ✅ Meilleure gestion des réseaux et labels Traefik
- ✅ Configuration centralisée
- ✅ Déploiement plus propre et maintenable