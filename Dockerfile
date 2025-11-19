# Dockerfile ultra-léger pour Donna API
FROM python:3.12-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier requirements.txt
COPY requirements.txt .

# Installer les dépendances sans cache pour réduire la taille
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source
COPY . .

# Créer le répertoire pour les logs
RUN mkdir -p logs

# Exposer le port
EXPOSE 8000

# Commande de démarrement
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]