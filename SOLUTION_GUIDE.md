# 🔧 GUIDE DE RÉSOLUTION - ÉTAPES CONCRÈTES

## 📋 PHASE 1: RÉSOLUTION TELEGRAM (30 minutes)

### Étape 1.1: Créer un Canal de Test Manuellement
```bash
# 1. Ouvrir Telegram
# 2. Créer un nouveau canal: "Omoni-Test-Channel"
# 3. Le rendre public (pour tests)
# 4. Ajouter @DonnaOmoniBot comme administrateur
# 5. Copier l'ID du canal (commence par -100)
```

### Étape 1.2: Mettre à Jour la Configuration
```bash
# Dans .env, ajouter:
TELEGRAM_TEST_CHANNEL_ID=-100XXXXXXXXX  # Remplace par le vrai ID
```

### Étape 1.3: Tester l'Envoi de Message
```bash
curl -X POST http://localhost:8000/api/v1/omoni/telegram/send \
  -H "Content-Type: application/json" \
  -d '{
    "channel_id": "-100XXXXXXXXX",
    "message": "✅ Test réussi - Canal fonctionnel!"
  }'
```

## 📋 PHASE 2: RÉSOLUTION SLACK (45 minutes)

### Étape 2.1: Configurer les Permissions Slack
```bash
# 1. Aller sur https://api.slack.com/apps
# 2. Sélectionner votre app Omoni
# 3. Aller dans "OAuth & Permissions"
# 4. Dans "Bot Token Scopes", ajouter:
```

**Scopes à ajouter:**
```
channels:manage      # Gérer les canaux publics
groups:write         # Gérer les canaux privés
channels:write        # Créer des canaux
conversations.create  # Créer des conversations
channels:read        # Lire les infos des canaux
chat:write           # Envoyer des messages
```

### Étape 2.2: Réinstaller l'App
```bash
# 1. Après ajout des scopes
# 2. Cliquer sur "Reinstall to Workspace"
# 3. Autoriser les nouvelles permissions
# 4. Le token va être régénéré avec les nouveaux scopes
```

### Étape 2.3: Tester la Création de Canal
```bash
curl -X POST http://localhost:8000/api/v1/omoni/slack/create-channel \
  -H "Content-Type: application/json" \
  -d '{
    "workspace_id": "T08H80B4FU0",
    "channel_name": "test-omoni-success",
    "private": false,
    "description": "Canal créé via API Omoni - Test réussi!"
  }'
```

## 📋 PHASE 3: VALIDATION COMPLETE (15 minutes)

### Script de Validation Final
```python
#!/usr/bin/env python3
import asyncio
import httpx

async def validation_complete():
    client = httpx.AsyncClient(timeout=30)
    
    tests = [
        {
            "name": "Telegram - Envoi message",
            "method": "POST",
            "url": "http://localhost:8000/api/v1/omoni/telegram/send",
            "data": {
                "channel_id": "-100XXXXXXXXX",  # Remplace par ID réel
                "message": "🎉 Validation Omoni complète!"
            }
        },
        {
            "name": "Slack - Création canal",
            "method": "POST", 
            "url": "http://localhost:8000/api/v1/omoni/slack/create-channel",
            "data": {
                "workspace_id": "T08H80B4FU0",
                "channel_name": "omoni-validation",
                "private": false,
                "description": "Canal de validation Omoni"
            }
        },
        {
            "name": "Slack - Envoi message",
            "method": "POST",
            "url": "http://localhost:8000/api/v1/omoni/slack/send", 
            "data": {
                "channel": "C08LA65EX1P",
                "message": "✅ Slack fonctionnel!"
            }
        }
    ]
    
    print("🧪 VALIDATION COMPLETE")
    print("=" * 40)
    
    for test in tests:
        try:
            print(f"\n📋 {test['name']}...")
            
            if test['method'] == 'POST':
                response = await client.post(test['url'], json=test['data'])
            else:
                response = await client.get(test['url'])
            
            if response.status_code == 200:
                print(f"   ✅ SUCCÈS")
            else:
                print(f"   ❌ ÉCHEC: {response.status_code}")
                print(f"   📄 {response.text}")
                
        except Exception as e:
            print(f"   ❌ ERREUR: {e}")
    
    await client.aclose()
    print("\n" + "=" * 40)
    print("✅ Validation terminée!")

if __name__ == "__main__":
    asyncio.run(validation_complete())
```

## 🚨 SOLUTIONS DE SECOURS

### Si Telegram ne fonctionne toujours pas:
```python
# Alternative: Utiliser les webhooks entrants
# 1. Configurer un webhook Telegram
# 2. Créer un canal de test manuellement
# 3. Utiliser l'ID du canal pour tous les tests
```

### Si Slack ne fonctionne toujours pas:
```python
# Alternative: Utiliser l'API incoming webhooks
# 1. Créer un webhook entrant Slack
# 2. Utiliser le webhook URL pour envoyer des messages
# 3. Implémenter une solution hybride
```

## 📊 CHECKLIST DE SUIVI

### Telegram ✅/❌
- [ ] Canal créé manuellement
- [ ] Bot ajouté comme admin
- [ ] Test envoi message réussi
- [ ] Test info canal réussi
- [ ] Test membres réussi

### Slack ✅/❌
- [ ] Scopes ajoutés dans l'app
- [ ] App réinstallée dans workspace
- [ ] Test création canal réussi
- [ ] Test envoi message réussi
- [ ] Test info canal réussi

### Global ✅/❌
- [ ] Script validation complet exécuté
- [ ] Tous les tests passent
- [ ] Documentation mise à jour
- [ ] Procédure documentée

## ⏰ TIMELINE ESTIMÉE

- **Phase 1 (Telegram):** 30 minutes
- **Phase 2 (Slack):** 45 minutes  
- **Phase 3 (Validation):** 15 minutes
- **Documentation:** 15 minutes

**Total:** ~2 heures pour résolution complète

## 🎯 PROCHAINES ACTIONS IMMÉDIATES

1. **Exécuter le script de test des fonctionnalités qui marchent**
2. **Créer canal Telegram de test manuellement**
3. **Ajouter les scopes Slack manquants**
4. **Tester validation complète**

Commencer par exécuter: `python test_working_features.py`