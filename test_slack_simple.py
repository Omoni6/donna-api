#!/usr/bin/env python3
"""
Test simple de création de canal Slack avec nom basique
"""

import asyncio
import httpx
import json
from datetime import datetime

API_BASE_URL = "http://localhost:8000"

async def test_simple_slack_channel():
    """Tester la création d'un canal Slack avec un nom simple"""
    
    client = httpx.AsyncClient(timeout=30.0)
    
    try:
        print("🧪 Test création canal Slack avec nom simple...")
        
        # Test avec un nom très simple
        channel_data = {
            "workspace_id": "T08H80B4FU0",
            "channel_name": "test-simple",
            "private": False,
            "description": "Channel créé via API O'moni pour tests",
            "user_id": "test-user-123"
        }
        
        print(f"📤 Données envoyées: {json.dumps(channel_data, indent=2)}")
        
        response = await client.post(
            f"{API_BASE_URL}/api/v1/omoni/slack/create-channel",
            json=channel_data
        )
        
        print(f"📊 Status code: {response.status_code}")
        print(f"📨 Response: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Succès: {json.dumps(result, indent=2)}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(test_simple_slack_channel())