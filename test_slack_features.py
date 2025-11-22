#!/usr/bin/env python3
"""
Test des différentes fonctionnalités Slack avec le token actuel
"""

import asyncio
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.slack_enhanced_service import slack_enhanced_service

async def test_slack_features():
    """Tester différentes fonctionnalités Slack"""
    
    print("🧪 Test des fonctionnalités Slack...")
    
    try:
        # Test 1: Envoi de message (nécessite chat:write)
        print("\n📤 Test envoi de message...")
        try:
            result = await slack_enhanced_service.send_message_to_channel(
                channel="C08LA65EX1P",  # SLACK_CHANNEL_TEAM
                message="Test message from O'moni API"
            )
            print(f"✅ Message envoyé: {result}")
        except Exception as e:
            print(f"❌ Erreur message: {str(e)}")
        
        # Test 2: Récupération d'infos de canal (nécessite channels:read)
        print("\n📋 Test récupération infos canal...")
        try:
            result = await slack_enhanced_service.get_channel_info("C08LA65EX1P")
            print(f"✅ Infos canal: {result}")
        except Exception as e:
            print(f"❌ Erreur infos: {str(e)}")
        
        # Test 3: Liste des membres (nécessite channels:read)
        print("\n👥 Test récupération membres...")
        try:
            result = await slack_enhanced_service.get_channel_members("C08LA65EX1P")
            print(f"✅ Membres: {len(result)} membres trouvés")
        except Exception as e:
            print(f"❌ Erreur membres: {str(e)}")
            
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_slack_features())