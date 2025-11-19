#!/bin/bash

# Script de déploiement Donna API sur VPS
# Ce script configure Traefik + Donna API avec SSL automatique

set -e

echo "🚀 Déploiement Donna API sur VPS..."

# Variables
DOMAIN="api.omoniprestanceholding.com"
EMAIL="contact@omoniprestanceholding.com"
REPO_URL="https://github.com/Omoni6/donna-api.git"
PROJECT_DIR="/opt/donna-api"

# Mise à jour du système
echo "📦 Mise à jour du système..."
sudo apt update && sudo apt upgrade -y

# Installation de Docker et Docker Compose
echo "🐳 Installation Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
fi

# Installation Docker Compose
echo "🐳 Installation Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Création du répertoire du projet
echo "📁 Création du répertoire du projet..."
sudo mkdir -p $PROJECT_DIR
sudo chown $USER:$USER $PROJECT_DIR

# Clonage du repository
echo "📥 Clonage du repository..."
cd $PROJECT_DIR
git clone $REPO_URL .

# Création du répertoire pour les données
echo "📂 Création des répertoires de données..."
mkdir -p data logs letsencrypt

# Création du fichier .env
echo "⚙️ Création du fichier .env..."
cp .env.example .env

# Création du network Traefik
echo "🌐 Création du network Traefik..."
docker network create traefik-network || true

# Lancement de Traefik
echo "🚀 Lancement de Traefik..."
docker-compose -f traefik-compose.yml up -d

# Attente du démarrage de Traefik
echo "⏳ Attente du démarrage de Traefik..."
sleep 10

# Lancement de Donna API
echo "🚀 Lancement de Donna API..."
docker-compose up -d

# Vérification du statut
echo "🔍 Vérification du statut..."
docker-compose ps

# Test de l'API
echo "🧪 Test de l'API..."
sleep 5
curl -f http://localhost:8000/v1 || echo "⚠️ API non accessible localement"

echo "✅ Déploiement terminé !"
echo "📍 API accessible sur: https://$DOMAIN/v1"
echo "📊 Dashboard Traefik: https://traefik.$DOMAIN"
echo ""
echo "📋 Commandes utiles:"
echo "  - Voir les logs: docker-compose logs -f"
echo "  - Redémarrer: docker-compose restart"
echo "  - Mettre à jour: git pull && docker-compose up -d --build"