# Dockerfile production-ready pour l'architecture O'moni FastAPI
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Créer un utilisateur non-root pour la sécurité
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier le fichier requirements s'il existe, sinon créer un fichier temporaire
COPY requirements.txt* ./

# Si requirements.txt n'existe pas, créer un fichier avec les dépendances nécessaires
RUN if [ ! -f requirements.txt ]; then \
    echo "fastapi==0.104.1" > requirements.txt && \
    echo "uvicorn[standard]==0.24.0" >> requirements.txt && \
    echo "pydantic==2.5.0" >> requirements.txt && \
    echo "python-multipart==0.0.6" >> requirements.txt && \
    echo "httpx==0.25.2" >> requirements.txt && \
    echo "python-jose[cryptography]==3.3.0" >> requirements.txt && \
    echo "passlib[bcrypt]==1.7.4" >> requirements.txt && \
    echo "stripe==7.8.0" >> requirements.txt && \
    echo "psutil==5.9.6" >> requirements.txt && \
    echo "python-telegram-bot==20.7" >> requirements.txt && \
    echo "google-api-python-client==2.109.0" >> requirements.txt; \
    fi

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Installer gunicorn pour la production
RUN pip install gunicorn==21.2.0

# Copier l'application
COPY app/ ./app/

# Créer le répertoire pour les uploads
RUN mkdir -p uploads && chown -R appuser:appuser uploads

# Changer l'utilisateur vers non-root
USER appuser

# Exposer le port
EXPOSE 8000

# Variables d'environnement par défaut
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV API_KEY=donna-api-key-production
ENV DONNA_WORKER_URL=http://donna:8001/api/donna/run
ENV JWT_SECRET_KEY=your-jwt-secret-key-change-in-production
ENV CORS_ORIGINS=https://omoni.fr,https://www.omoni.fr

# Commande pour démarrer l'application avec gunicorn en production
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--timeout", "120", "--keep-alive", "5", "--max-requests", "1000", "--max-requests-jitter", "100", "--preload", "--access-logfile", "-", "--error-logfile", "-", "app.main:app"]

# Alternative avec uvicorn directement (décommenter si préféré)
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4", "--timeout-keep-alive", "5"]