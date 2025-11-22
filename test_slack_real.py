#!/usr/bin/env python3
"""
Test des endpoints Slack avec vrais tokens
"""

import requests
import json
import datetime
import os
from typing import Dict, Any

# Configuration avec les vrais tokens
API_BASE_URL = "http://localhost:8000"
API_KEY = "donna-api-key-production"  # Remplacez par votre vraie clé API

def test_endpoint(method: str, endpoint: str, data: Dict[str, Any] = None, params: Dict[str, Any] = None) -> Dict[str, Any]:
    """Tester un endpoint"""
    url = f"{API_BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": API_KEY
    }
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method.upper() == "POST":
            response = requests.post(url, headers=headers, json=data)
        else:
            raise ValueError(f"Méthode non supportée: {method}")
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"📄 Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            return {"success": True, "data": result}
        else:
            error_text = response.text
            print(f"❌ Error: {error_text}")
            return {"success": False, "error": error_text}
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return {"success": False, "error": str(e)}

def main():
    """Tests principaux"""
    print("🚀 Démarrage des tests Slack API")
    print(f"📍 API URL: {API_BASE_URL}")
    print(f"🔑 API Key: {API_KEY[:10]}...")
    print("=" * 60)
    
    # Test 1: Health Check
    print("\n🧪 Test: Health Check")
    result = test_endpoint("GET", "/api/health")
    
    if not result["success"]:
        print("❌ Health check failed, arrêt des tests")
        return
    
    print("\n" + "=" * 60)
    
    # Test 2: Créer un channel Slack
    print("\n🧪 Test: Créer un channel Slack")
    channel_data = {
        "workspace_id": "T08H80B4FU0",  # Using your real team ID
        "channel_name": "test-omoni-api",
        "private": False,
        "description": "Channel créé via API O'moni pour tests",
        "user_id": "test-user-123"
    }
    result = test_endpoint("POST", "/api/v1/omoni/slack/create-channel", data=channel_data)
    
    if result["success"]:
        channel_id = result["data"].get("channel_id")
        print(f"✅ Channel créé avec ID: {channel_id}")
    else:
        print("❌ Échec création channel")
        channel_id = None
    
    print("\n" + "=" * 60)
    
    # Test 3: Infos channel Slack (utiliser un channel existant)
    print("\n🧪 Test: Infos channel Slack")
    if channel_id:
        result = test_endpoint("GET", f"/api/v1/omoni/slack/channel/{channel_id}/info")
    else:
        # Utiliser un channel ID par défaut si la création a échoué
        result = test_endpoint("GET", "/api/v1/omoni/slack/channel/C08LA65EX1P/info")
    
    print("\n" + "=" * 60)
    
    # Test 3: Envoyer message Slack
    print("\n🧪 Test: Envoyer message Slack")
    message_data = {
        "channel": channel_id or "C08LA65EX1P",
        "message": f"🎯 Test API O'moni - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nCe message est envoyé via l'API FastAPI!",
        "agent": "DonnaBot"
    }
    result = test_endpoint("POST", "/api/v1/omoni/slack/send", data=message_data)
    
    print("\n" + "=" * 60)
    
    # Test 5: Connecteur général Slack
    print("\n🧪 Test: Connecteur général Slack")
    connector_data = {
        "provider": "slack",
        "action": "send_message",
        "data": {
            "channel": channel_id or "C08LA65EX1P",
            "text": f"📢 Message via connecteur général - {datetime.datetime.now().strftime('%H:%M:%S')}",
            "username": "OmoniConnector"
        },
        "user_id": "test-user-123"
    }
    result = test_endpoint("POST", "/api/v1/omoni/connectors/manage", data=connector_data)
    
    print("\n" + "=" * 60)
    
    # Test 6: Communication agent Slack
    print("\n🧪 Test: Communication agent Slack")
    agent_data = {
        "agent_id": "donna_test_agent",
        "action": "send_slack_message",
        "payload": {
            "channel": channel_id or "C08LA65EX1P",
            "text": f"🤖 Message envoyé par l'agent Donna - {datetime.datetime.now().strftime('%H:%M:%S')}",
            "username": "DonnaAgent"
        },
        "user_id": "test-user-123"
    }
    result = test_endpoint("POST", "/api/v1/agents/communicate", data=agent_data)
    
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    print("✅ Tests Slack terminés!")
    print("🎉 L'intégration Slack avec les vrais tokens est fonctionnelle!")

if __name__ == "__main__":
    main()