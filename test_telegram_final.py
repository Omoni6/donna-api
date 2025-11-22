#!/usr/bin/env python3
"""
Test final de création de canal Telegram (création de lien d'invitation)
"""

import asyncio
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.telegram_enhanced_service import telegram_enhanced_service

async def test_telegram_final():
    """Test final de la fonctionnalité Telegram"""
    
    print("🧪 Test final Telegram...")
    
    try:
        # Test création de lien d'invitation (alternative à la création de canal)
        print("📋 Test création lien d'invitation Telegram...")
        
        result = await telegram_enhanced_service.create_channel(
            channel_name="test-omoni-invite",
            channel_type="private",
            description="Lien d'invitation créé via O'moni API",
            members=["@testuser"]
        )
        
        print(f"✅ Succès: {result}")
        
        # Test envoi de message
        print("\n📤 Test envoi de message...")
        message_result = await telegram_enhanced_service.send_message_to_channel(
            channel_id="-1002491351825",  # TELEGRAM_CHAT_ID
            message="Test message from O'moni API - Canal fonctionnel!"
        )
        print(f"✅ Message envoyé: {message_result}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_telegram_final())