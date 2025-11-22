# Donna API - Architecture O'moni

API FastAPI principale pour l'architecture O'moni - Multi-service avec agents.

## 🏗️ Architecture

```
app/
├── main.py              # Point d'entrée principal
├── core/                # Configuration et utilitaires
│   ├── config.py        # Configuration de l'application
│   ├── security.py      # Middleware de sécurité (API Key + JWT)
│   └── logging.py       # Configuration du logging JSON
├── models/              # Modèles Pydantic
│   ├── agent.py         # Modèles pour les agents
│   ├── user.py          # Modèles utilisateurs
│   └── analytics.py     # Modèles d'analytics
├── services/            # Services métiers
│   ├── agent_zero.py    # Service Donna Worker
│   ├── telegram.py      # Service Telegram
│   ├── stripe.py        # Service Stripe
│   ├── google.py        # Service Google
│   └── analytics.py     # Service Analytics
└── routers/             # Routes API
    ├── root.py          # Routes racine
    ├── health.py        # Routes de santé
    ├── agents.py        # Routes agents
    ├── users.py         # Routes utilisateurs
    ├── uploads.py       # Routes uploads
    ├── modules.py       # Routes modules
    └── webhooks/        # Routes webhooks
        ├── telegram.py
        ├── stripe.py
        └── google.py
```

## 🚀 Installation

### Prérequis

- Python 3.12+
- pip ou poetry

### Installation rapide

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd donna-api

# Installer les dépendances
pip install -r requirements.txt

# Démarrer l'API en développement
python start_api.py --mode dev
```

### Installation avec Docker

```bash
# Construire l'image
docker build -t donna-api .

# Démarrer le conteneur
docker run -p 8000:8000 \
  -e API_KEY=your-api-key \
  -e DONNA_WORKER_URL=http://donna:8001/api/donna/run \
  -e JWT_SECRET_KEY=your-jwt-secret \
  donna-api
```

## 📡 Endpoints API

### Endpoints publics

- `GET /api/health` - Vérification de santé
- `GET /api/version` - Version de l'API
- `GET /api/docs` - Documentation Swagger
- `GET /api/redoc` - Documentation ReDoc

### Agents

- `POST /api/v1/agents/execute` - Exécuter un agent
- `GET /api/v1/agents/status/{task_id}` - Vérifier le statut d'une tâche

### Utilisateurs (NextAuth compatible)

- `POST /api/v1/users/auth/signin` - Connexion
- `POST /api/v1/users/auth/callback/credentials` - Callback NextAuth
- `GET /api/v1/users/auth/session` - Session actuelle
- `POST /api/v1/users/auth/signout` - Déconnexion
- `GET /api/v1/users/me` - Profil utilisateur
- `PUT /api/v1/users/me` - Mise à jour du profil

### Uploads

- `POST /api/v1/uploads/file` - Uploader un fichier
- `POST /api/v1/uploads/files` - Uploader plusieurs fichiers
- `GET /api/v1/uploads/files` - Lister les fichiers
- `DELETE /api/v1/uploads/files/{filename}` - Supprimer un fichier
- `GET /api/v1/uploads/config` - Configuration des uploads

### Modules

- `GET /api/v1/modules/status` - Statut de tous les modules
- `GET /api/v1/modules/health/{module_name}` - Santé d'un module
- `POST /api/v1/modules/restart/{module_name}` - Redémarrer un module
- `GET /api/v1/modules/metrics` - Métriques système
- `GET /api/v1/modules/dependencies` - Dépendances entre modules

### Webhooks

#### Telegram
- `POST /api/v1/webhooks/telegram` - Webhook Telegram

#### Stripe
- `POST /api/v1/webhooks/stripe` - Webhook Stripe

#### Google
- `POST /api/v1/webhooks/google/calendar` - Webhook Google Calendar
- `POST /api/v1/webhooks/google/gmail` - Webhook Gmail
- `POST /api/v1/webhooks/google/drive` - Webhook Google Drive
- `GET /api/v1/webhooks/google/verify` - Vérification Google

## 🔐 Sécurité

### API Key

Les endpoints sensibles nécessitent une API Key dans le header `X-API-Key`:

```bash
curl -H "X-API-Key: your-api-key" http://localhost:8000/api/v1/agents/execute
```

### JWT NextAuth

Les endpoints utilisateurs utilisent des tokens JWT compatibles NextAuth:

```bash
# Connexion
curl -X POST http://localhost:8000/api/v1/users/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@omoni.fr", "password": "admin123"}'

# Utiliser le token
curl -H "Authorization: Bearer your-jwt-token" \
  http://localhost:8000/api/v1/users/me
```

### Multi-tenant

Support multi-tenant via le header `X-Tenant-ID`:

```bash
curl -H "X-Tenant-ID: client-123" http://localhost:8000/api/v1/uploads/files
```

## 📝 Configuration

### Variables d'environnement

| Variable | Description | Défaut |
|----------|-------------|---------|
| `API_KEY` | Clé API pour les endpoints sensibles | `donna-api-key-production` |
| `DONNA_WORKER_URL` | URL du service Donna Worker | `http://donna:8001/api/donna/run` |
| `JWT_SECRET_KEY` | Clé secrète JWT | `your-jwt-secret-key` |
| `CORS_ORIGINS` | Origines CORS autorisées | `http://localhost:3000` |
| `LOG_LEVEL` | Niveau de logging | `INFO` |

### Types d'agents

- **Planifi**: Agent de planification
- **Publie**: Agent de publication
- **Cree**: Agent de création
- **Commercial**: Agent commercial

## 🧪 Tests

### Tests manuels

```bash
# Démarrer le serveur
python start_api.py --mode dev

# Lancer les tests
python test_api.py
```

### Tests avec curl

```bash
# Test santé
curl http://localhost:8000/api/health

# Test agents
curl -X POST http://localhost:8000/api/v1/agents/execute \
  -H "X-API-Key: donna-api-key-production" \
  -H "Content-Type: application/json" \
  -d '{
    "instruction": "Créer un plan marketing",
    "context": {"produit": "SaaS"},
    "user_id": "test_user",
    "agent_type": "Planifi"
  }'
```

## 🚀 Déploiement

### Production avec Gunicorn

```bash
# Installation
gunicorn --bind 0.0.0.0:8000 \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --timeout 120 \
  app.main:app
```

### Docker Production

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app/

USER nobody
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "app.main:app"]
```

## 📊 Monitoring

### Logs

L'API utilise un format de logging JSON structuré:

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "logger": "donna.api",
  "message": "Agent exécuté avec succès",
  "user_id": "user_123",
  "agent_type": "Planifi",
  "task_id": "task_456"
}
```

### Métriques

Accéder aux métriques système:

```bash
curl http://localhost:8000/api/v1/modules/metrics
```

## 🤝 Intégrations

### Donna Worker

L'API communique avec Donna Worker via HTTP:

```python
# Configuration
DONNA_WORKER_URL = "http://donna:8001/api/donna/run"

# Appel
response = await httpx.post(DONNA_WORKER_URL, json={
    "instruction": "Créer un plan...",
    "context": {...},
    "user_id": "user_123",
    "agent_type": "Planifi"
})
```

### Webhooks

Les webhooks sont vérifiés et traités de manière asynchrone:

- **Stripe**: Vérification de signature
- **Telegram**: Traitement des messages
- **Google**: Notifications de changements

## 📝 License

Propriétaire - O'moni Architecture

## 🆘 Support

Pour les questions ou problèmes, veuillez contacter l'équipe technique.