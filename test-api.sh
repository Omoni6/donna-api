#!/bin/bash

# Script de test Donna API
# Teste les endpoints principaux et les webhooks

API_URL="https://api.omoniprestanceholding.com"

echo "🧪 Test de l'API Donna..."
echo "URL: $API_URL"
echo ""

# Test health check
echo "1️⃣ Test health check (GET /v1)..."
response=$(curl -s -w "\nHTTP_CODE:%{http_code}" "$API_URL/v1")
http_code=$(echo "$response" | grep "HTTP_CODE:" | cut -d: -f2)
body=$(echo "$response" | grep -v "HTTP_CODE:")

echo "   Status: $http_code"
echo "   Response: $body"
echo ""

# Test Telegram webhook
echo "2️⃣ Test Telegram webhook (POST /api/v1/telegram/webhook)..."
telegram_response=$(curl -s -X POST "$API_URL/api/v1/telegram/webhook" \
  -H "Content-Type: application/json" \
  -d '{"update_id": 123456789, "message": {"text": "test"}}' \
  -w "\nHTTP_CODE:%{http_code}")

telegram_http_code=$(echo "$telegram_response" | grep "HTTP_CODE:" | cut -d: -f2)
telegram_body=$(echo "$telegram_response" | grep -v "HTTP_CODE:")

echo "   Status: $telegram_http_code"
echo "   Response: $telegram_body"
echo ""

# Test Slack events
echo "3️⃣ Test Slack events (POST /api/v1/slack/events)..."
slack_response=$(curl -s -X POST "$API_URL/api/v1/slack/events" \
  -H "Content-Type: application/json" \
  -d '{"type": "url_verification", "challenge": "test_challenge_123"}' \
  -w "\nHTTP_CODE:%{http_code}")

slack_http_code=$(echo "$slack_response" | grep "HTTP_CODE:" | cut -d: -f2)
slack_body=$(echo "$slack_response" | grep -v "HTTP_CODE:")

echo "   Status: $slack_http_code"
echo "   Response: $slack_body"
echo ""

# Résumé
echo "📊 Résumé des tests:"
echo "   Health check: $([ "$http_code" = "200" ] && echo "✅ PASS" || echo "❌ FAIL")"
echo "   Telegram webhook: $([ "$telegram_http_code" = "200" ] && echo "✅ PASS" || echo "❌ FAIL")"
echo "   Slack events: $([ "$slack_http_code" = "200" ] && echo "✅ PASS" || echo "❌ FAIL")"

echo ""
echo "✅ Tests terminés !"