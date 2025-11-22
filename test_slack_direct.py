#!/usr/bin/env python3
"""
Test direct du service Slack sans passer par le serveur FastAPI
"""

import asyncio
import sys
import os

# Ajouter le répertoire parent au path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.services.slack_enhanced_service import slack_enhanced_service

async def test_slack_direct():
    """Tester directement le service Slack"""
    
    print("🧪 Test direct du service Slack...")
    
    try:
        # Test création de canal
        print("📋 Test création canal Slack...")
        
        result = await slack_enhanced_service.create_channel(
            channel_name="test-direct",
            private=False,
            description="Test création canal via service direct",
            workspace_id="T08H80B4FU0"
        )
        
        print(f"✅ Succès: {result}")
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_slack_direct())