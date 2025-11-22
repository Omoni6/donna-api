#!/usr/bin/env python3
"""
Script de test pour vérifier les endpoints Telegram avec vos tokens réels
"""

import asyncio
import requests
import json
import os
from datetime import datetime

# Configuration avec vos tokens réels
API_BASE_URL = "http://localhost:8000"
API_KEY = "donna-api-key-production"

# Vos tokens Telegram réels
TELEGRAM_BOT_TOKEN = "7933642559:AAGpYPeZj4qprwhANTK65EakAgFB326wIBk"
TELEGRAM_CHAT_ID = "-4832915059"
TELEGRAM_CHAT_ID_TEAM = "-4907447424"
TELEGRAM_CHAT_ID_SYSTEM = "-4919674767"

def test_create_channel():
    """Tester la création d'un canal Telegram"""
    print("🧪 Test: Création canal Telegram")
    
    url = f"{API_BASE_URL}/api/v1/omoni/telegram/create-channel"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "user_id": "user_test_123",
        "channel_name": f"Test Canal {datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "type": "private",
        "description": "Canal de test créé via API",
        "members": ["@testuser1", "@testuser2"]
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 200:
            result = response.json()
            return result.get("channel_id"), result.get("invite_link")
        else:
            print(f"❌ Erreur: {response.text}")
            return None, None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None, None

def test_send_message():
    """Tester l'envoi d'un message"""
    print("\n🧪 Test: Envoi message Telegram")
    
    url = f"{API_BASE_URL}/api/v1/omoni/telegram/send"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "channel_id": TELEGRAM_CHAT_ID,
        "message": f"🎯 Test API O'moni - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\nCe message est envoyé via l'API FastAPI!",
        "parse_mode": "HTML",
        "disable_notification": False
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_get_channel_info():
    """Tester la récupération des infos d'un canal"""
    print(f"\n🧪 Test: Infos canal Telegram {TELEGRAM_CHAT_ID}")
    
    url = f"{API_BASE_URL}/api/v1/omoni/telegram/channel/{TELEGRAM_CHAT_ID}/info"
    headers = {
        "X-API-Key": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_get_members_count():
    """Tester le comptage des membres"""
    print(f"\n🧪 Test: Nombre de membres canal {TELEGRAM_CHAT_ID}")
    
    url = f"{API_BASE_URL}/api/v1/omoni/telegram/channel/{TELEGRAM_CHAT_ID}/members/count"
    headers = {
        "X-API-Key": API_KEY
    }
    
    try:
        response = requests.get(url, headers=headers)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_connector_manage():
    """Tester le connecteur général"""
    print("\n🧪 Test: Connecteur général Telegram")
    
    url = f"{API_BASE_URL}/api/v1/omoni/connectors/manage"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "provider": "telegram",
        "action": "send_message",
        "user_id": "user_test_123",
        "workspace_id": "workspace_test_123",
        "data": {
            "channel_id": TELEGRAM_CHAT_ID_TEAM,
            "message": f"📢 Message via connecteur général - {datetime.now().strftime('%H:%M:%S')}",
            "parse_mode": "HTML"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_agent_communicate():
    """Tester la communication avec les agents"""
    print("\n🧪 Test: Communication agent")
    
    url = f"{API_BASE_URL}/api/v1/agents/communicate"
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    data = {
        "action": "send_telegram_message",
        "agent_id": "donna_test_agent",
        "user_id": "user_test_123",
        "workspace_id": "workspace_test_123",
        "payload": {
            "channel_id": TELEGRAM_CHAT_ID,
            "message": f"🤖 Message envoyé par l'agent Donna - {datetime.now().strftime('%H:%M:%S')}",
            "parse_mode": "HTML"
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_health_check():
    """Tester le health check"""
    print("\n🧪 Test: Health Check")
    
    url = f"{API_BASE_URL}/api/health"
    
    try:
        response = requests.get(url)
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    """Exécuter tous les tests"""
    print("🚀 Démarrage des tests Telegram API")
    print(f"📍 API URL: {API_BASE_URL}")
    print(f"🤖 Bot Token: {TELEGRAM_BOT_TOKEN[:20]}...")
    print(f"💬 Chat ID: {TELEGRAM_CHAT_ID}")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Envoi Message", test_send_message),
        ("Infos Canal", test_get_channel_info),
        ("Nombre Membres", test_get_members_count),
        ("Connecteur Général", test_connector_manage),
        ("Communication Agent", test_agent_communicate),
        ("Création Canal", test_create_channel),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"\n{'='*60}")
            result = test_func()
            results.append((test_name, result))
            print(f"{'='*60}")
            
            # Petite pause entre les tests
            import time
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Erreur dans le test {test_name}: {e}")
            results.append((test_name, False))
    
    # Résumé
    print(f"\n{'='*60}")
    print("📊 RÉSUMÉ DES TESTS")
    print(f"{'='*60}")
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    total_tests = len(results)
    passed_tests = sum(1 for _, success in results if success)
    
    print(f"\n📈 Total: {passed_tests}/{total_tests} tests passés")
    
    if passed_tests == total_tests:
        print("🎉 Tous les tests ont réussi!")
    else:
        print("⚠️  Certains tests ont échoué - vérifiez la configuration")

if __name__ == "__main__":
    # Vérifier que l'API est accessible
    try:
        response = requests.get(f"{API_BASE_URL}/api/health", timeout=5)
        if response.status_code != 200:
            print(f"❌ L'API n'est pas accessible à {API_BASE_URL}")
            print("Assurez-vous que le serveur FastAPI est en cours d'exécution")
            exit(1)
    except Exception as e:
        print(f"❌ Impossible de contacter l'API: {e}")
        print("Assurez-vous que le serveur FastAPI est en cours d'exécution")
        exit(1)
    
    main()