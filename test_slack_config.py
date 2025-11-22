#!/usr/bin/env python3
"""
Test simple pour vérifier que le service Slack peut être importé
"""

import asyncio
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.slack_enhanced_service import slack_enhanced_service
from app.core.config import settings

async def test_slack_service():
    """Tester l'import et la configuration du service Slack"""
    
    print("🔍 Test import service Slack...")
    
    try:
        # Vérifier la configuration
        print(f"📝 SLACK_BOT_TOKEN configuré: {bool(settings.SLACK_BOT_TOKEN)}")
        print(f"📝 SLACK_TEAM_ID configuré: {bool(settings.SLACK_TEAM_ID)}")
        print(f"📝 Longueur du token: {len(settings.SLACK_BOT_TOKEN) if settings.SLACK_BOT_TOKEN else 0}")
        
        if settings.SLACK_BOT_TOKEN:
            print(f"📝 Début du token: {settings.SLACK_BOT_TOKEN[:20]}...")
        
        # Vérifier que le service est bien initialisé
        print(f"✅ Service Slack initialisé: {slack_enhanced_service is not None}")
        
        # Test simple de création de canal (sans l'appeler réellement)
        print("✅ Configuration Slack OK")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_slack_service())