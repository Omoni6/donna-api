# 🎯 Configuration Telegram Réelle - Production Ready

## 🔑 Tokens Principaux (Réels)

```bash
# Tokens principaux Telegram
TELEGRAM_BOT_TOKEN=7933642559:AAGpYPeZj4qprwhANTK65EakAgFB326wIBk
TELEGRAM_TOKEN=7933642559:AAGpYPeZj4qprwhANTK65EakAgFB326wIBk
TELEGRAM_DONNA_BOT_TOKEN=7933642559:AAGpYPeZj4qprwhANTK65EakAgFB326wIBk

# Configuration API Telegram
TELEGRAM_API_ID=29320465
TELEGRAM_API_HASH=681eabdfdc64e20cedd5fec26171bc04
TELEGRAM_API_KEY=AAGsKAAAU4B2PZFynyBGgL1q2-_3oQJJsusOamVLhkZIYA

# Bot Username
TELEGRAM_BOT_USERNAME=@DonnaOmoniBot
```

## 📱 Channels & Groups IDs (Réels)

```bash
# Channels principaux
TELEGRAM_AUDIT_CHANNEL_ID=-10002947552752
TELEGRAM_CHAT_ID=-4832915059
TELEGRAM_CHAT_ID_ALERTS=-4832915059
TELEGRAM_CHAT_ID_SYSTEM=-4919674767
TELEGRAM_CHAT_ID_TEAM=-4907447424
TELEGRAM_CHAT_ID_REPORTS=-4964733758
TELEGRAM_CHAT_ID_MARKETING=-4964733758

# Configuration notifications
TELEGRAM_NOTIFICATIONS=true
DEFAULT_TELEGRAM_CHAT_ID=-4832915059
```

## 🚀 Endpoints Telegram Disponibles

### 1. Créer un Canal Telegram
```bash
curl -X POST "https://api.omoni.fr/api/v1/omoni/telegram/create-channel" \
  -H "X-API-Key: donna-api-key-production" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user_123",
    "channel_name": "Nouveaux Clients",
    "type": "private",
    "members": ["@username1", "@username2"],
    "description": "Canal pour les nouveaux clients"
  }'
```

**Réponse:**
```json
{
  "success": true,
  "channel_id": "-1001234567890",
  "invite_link": "https://t.me/+ABCDEFGHIJKL",
  "channel_name": "Nouveaux Clients",
  "type": "private"
}
```

### 2. Ajouter un Membre
```bash
curl -X POST "https://api.omoni.fr/api/v1/omoni/telegram/add-member" \
  -H "X-API-Key: donna-api-key-production" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "-1001234567890",
    "username": "@newmember",
    "user_id": "user_123"
  }'
```

### 3. Envoyer un Message
```bash
curl -X POST "https://api.omoni.fr/api/v1/omoni/telegram/send" \
  -H "X-API-Key: donna-api-key-production" \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "-4832915059",
    "message": "🎯 Nouveau client ajouté! Bienvenue à notre communauté.",
    "parse_mode": "HTML"
  }'
```

### 4. Lier un Canal au Workspace
```bash
curl -X POST "https://api.omoni.fr/api/v1/omoni/telegram/link" \
  -H "X-API-Key: donna-api-key-production" \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "workspace_abc123",
    "channel_id": "-1001234567890",
    "channel_name": "Équipe Marketing",
    "user_id": "user_123"
  }'
```

### 5. Obtenir les Infos d'un Canal
```bash
curl -X GET "https://api.omoni.fr/api/v1/omoni/telegram/channel/-1001234567890/info" \
  -H "X-API-Key: donna-api-key-production"
```

### 6. Compter les Membres
```bash
curl -X GET "https://api.omoni.fr/api/v1/omoni/telegram/channel/-1001234567890/members/count" \
  -H "X-API-Key: donna-api-key-production"
```

## 🔧 Connecteur Général

Utilisez l'endpoint universel pour toutes les opérations:

```bash
curl -X POST "https://api.omoni.fr/api/v1/omoni/connectors/manage" \
  -H "X-API-Key: donna-api-key-production" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "telegram",
    "action": "create_channel",
    "user_id": "user_123",
    "workspace_id": "workspace_abc123",
    "data": {
      "channel_name": "Canal Test",
      "type": "private",
      "description": "Canal de test"
    }
  }'
```

## 🤖 Communication avec les Agents

Permettez à Donna Worker de créer des canaux:

```bash
curl -X POST "https://api.omoni.fr/api/v1/agents/communicate" \
  -H "X-API-Key: donna-api-key-production" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "create_telegram_channel",
    "agent_id": "donna_agent_001",
    "user_id": "user_123",
    "workspace_id": "workspace_abc123",
    "payload": {
      "channel_name": "Canal créé par Donna",
      "type": "private",
      "description": "Ce canal a été créé automatiquement par Donna"
    }
  }'
```

## 📋 Actions Disponibles

### Via Connecteur Général:
- `create_channel` - Créer un canal
- `add_member` - Ajouter un membre
- `send_message` - Envoyer un message
- `link` - Lier au workspace
- `sync` - Synchroniser les données

### Via Agent Communication:
- `create_telegram_channel` - Créer canal Telegram
- `send_telegram_message` - Envoyer message Telegram
- `add_telegram_member` - Ajouter membre Telegram

## 🎯 Configuration Multi-Tenant

Ajoutez le header `X-Tenant-ID` pour le support multi-tenant:

```bash
curl -X POST "https://api.omoni.fr/api/v1/omoni/telegram/create-channel" \
  -H "X-API-Key: donna-api-key-production" \
  -H "X-Tenant-ID: tenant_abc123" \
  -H "Content-Type: application/json" \
  -d '{...}'
```

## ⚡ Exemples d'Utilisation Rapide

### Créer un Canal pour les Nouveaux Clients
```python
import requests

response = requests.post(
    "https://api.omoni.fr/api/v1/omoni/telegram/create-channel",
    headers={
        "X-API-Key": "donna-api-key-production",
        "Content-Type": "application/json"
    },
    json={
        "user_id": "user_123",
        "channel_name": "Nouveaux Clients VIP",
        "type": "private",
        "description": "Canal privé pour nos clients VIP"
    }
)

print(response.json())
```

### Envoyer une Notification à l'Équipe
```python
response = requests.post(
    "https://api.omoni.fr/api/v1/omoni/telegram/send",
    headers={
        "X-API-Key": "donna-api-key-production",
        "Content-Type": "application/json"
    },
    json={
        "channel_id": "-4907447424",  # TELEGRAM_CHAT_ID_TEAM
        "message": "🚀 Nouvelle mise à jour disponible!",
        "parse_mode": "HTML"
    }
)
```

## 🔒 Sécurité

- Tous les endpoints nécessitent la clé API `X-API-Key`
- Support multi-tenant via `X-Tenant-ID`
- Validation des données avec Pydantic
- Logging détaillé des opérations
- Gestion d'erreurs complète

## 📊 Monitoring

Les endpoints incluent:
- Logging détaillé de toutes les opérations
- Timestamps ISO 8601
- Gestion des erreurs avec messages clairs
- Support des webhooks pour les notifications

---

**✅ Prêt pour la production avec vos tokens réels!**