# 🚀 Déploiement Donna API sur VPS

## 📋 Prérequis
- VPS Ubuntu 20.04+
- Docker et Docker Compose installés
- Domaine pointant vers le VPS (api.omoniprestanceholding.com)

## 🚀 Installation rapide

1. **Connectez-vous à votre VPS**
```bash
ssh votre-utilisateur@votre-vps-ip
```

2. **Téléchargez et exécutez le script de déploiement**
```bash
curl -fsSL https://raw.githubusercontent.com/Omoni6/donna-api/main/deploy.sh -o deploy.sh
chmod +x deploy.sh
./deploy.sh
```

## 🔧 Configuration manuelle (alternative)

### 1. Cloner le repository
```bash
git clone https://github.com/Omoni6/donna-api.git /opt/donna-api
cd /opt/donna-api
```

### 2. Créer le network Docker
```bash
docker network create traefik-network
```

### 3. Lancer Traefik (reverse proxy + SSL)
```bash
docker-compose -f traefik-compose.yml up -d
```

### 4. Lancer Donna API
```bash
docker-compose up -d
```

## 📊 Vérification

### Vérifier les conteneurs
```bash
docker-compose ps
```

### Voir les logs
```bash
docker-compose logs -f
```

### Tester l'API
```bash
./test-api.sh
```

## 🌐 Accès

- **API Donna**: https://api.omoniprestanceholding.com/v1
- **Dashboard Traefik**: https://traefik.omoniprestanceholding.com
- **Username**: admin
- **Password**: (généré automatiquement)

## 🔄 Mise à jour

```bash
cd /opt/donna-api
git pull
docker-compose up -d --build
```

## 🗂️ Structure des volumes

- `./logs/` : Logs de l'application
- `./data/` : Base de données SQLite
- `./letsencrypt/` : Certificats SSL

## 🔒 Sécurité

- SSL automatique avec Let's Encrypt
- Basic auth sur Traefik dashboard
- Logs centralisés
- Health checks intégrés

## 🆘 Support

En cas de problème:
1. Vérifiez les logs: `docker-compose logs`
2. Testez localement: `./test-api.sh`
3. Redémarrez le service: `docker-compose restart`