#!/usr/bin/env python3
"""
Test de création de canal Telegram avec API hash (Telegram Core API)
"""

import asyncio
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.telegram_enhanced_service import telegram_enhanced_service

async def test_telegram_channel_creation():
    """Tester la création de canal Telegram avec API hash"""
    
    print("🧪 Test création canal Telegram avec API hash...")
    
    try:
        # Test création de canal avec API hash (Telegram Core API)
        print("📋 Test création canal avec Telegram Core API (MTProto)...")
        
        result = await telegram_enhanced_service.create_channel(
            channel_name="test-omoni-hash",
            channel_type="private",
            description="Canal créé via API hash Telegram Core API",
            members=["@testuser"]
        )
        
        print(f"✅ Succès création canal: {result}")
        
    except Exception as e:
        print(f"❌ Erreur création canal: {str(e)}")
        
        # Test si Telethon est disponible
        print(f"📊 Telethon disponible: {telegram_enhanced_service.telethon_available}")
        if telegram_enhanced_service.telethon_available:
            print("✅ Telethon est bien installé et configuré")
        else:
            print("⚠️  Telethon n'est pas disponible - vérifier l'installation")

if __name__ == "__main__":
    asyncio.run(test_telegram_channel_creation())