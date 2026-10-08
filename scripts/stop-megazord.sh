#!/usr/bin/env bash
# stop-megazord.sh
# Para n8n + cloudflared que estao rodando em background.

echo "Parando Megazord..."

# Para n8n
pkill -f "n8n start" 2>/dev/null && echo "✅ n8n parado" || echo "ℹ️ n8n não estava rodando"

# Para cloudflared (mas NÃO para o service systemd)
pkill -f "cloudflared tunnel run" 2>/dev/null && echo "✅ cloudflared (manual) parado" || echo "ℹ️ cloudflared manual não estava rodando"

# Aviso sobre service
if systemctl is-active --quiet cloudflared 2>/dev/null; then
    echo "⚠️ cloudflared está rodando como SERVICE (systemd)"
    echo "   Pra parar: sudo systemctl stop cloudflared"
fi

echo ""
echo "Sistema parado. Pra subir de novo: bash scripts/start-megazord.sh"
