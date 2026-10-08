#!/usr/bin/env bash
# start-megazord.sh
# Sobe n8n + cloudflared em background.
# Logs em ~/.n8n/n8n.log e ~/.cloudflared/tunnel.log
# Pra parar: bash stop-megazord.sh

set -e

echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  MEGAZORD MVP — Subindo sistema                            │"
echo "└─────────────────────────────────────────────────────────────┘"

# 1. Garante Node 22
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && . "$NVM_DIR/nvm.sh"
nvm use 22 > /dev/null
echo "✅ Node $(node --version)"

# 2. Mata processos antigos (se existirem)
pkill -f "n8n start" 2>/dev/null || true
pkill -f "cloudflared tunnel" 2>/dev/null || true
sleep 2

# 3. Sobe n8n em background
mkdir -p ~/.n8n
nohup n8n start > ~/.n8n/n8n.log 2>&1 &
N8N_PID=$!
echo "✅ n8n rodando (PID: $N8N_PID) — http://localhost:5678"
echo "   log: tail -f ~/.n8n/n8n.log"

# 4. Espera n8n subir
sleep 8

# 5. Testa n8n
if curl -s http://localhost:5678/healthz > /dev/null; then
    echo "   ✅ n8n healthz OK"
else
    echo "   ⚠️ n8n ainda subindo — confere: tail -20 ~/.n8n/n8n.log"
fi

# 6. Sobe cloudflared em background
mkdir -p ~/.cloudflared
TOKEN=$(sudo cat /etc/cloudflared/token 2>/dev/null || echo "")
if [ -z "$TOKEN" ]; then
    echo "❌ Token do cloudflared não encontrado em /etc/cloudflared/token"
    echo "   Rode: sudo cloudflared service install <token-do-dashboard>"
    exit 1
fi
nohup cloudflared tunnel run --token "$TOKEN" --url http://localhost:5678 > ~/.cloudflared/tunnel.log 2>&1 &
CF_PID=$!
echo "✅ cloudflared rodando (PID: $CF_PID)"
echo "   log: tail -f ~/.cloudflared/tunnel.log"

# 7. Espera cloudflared conectar
sleep 8

# 8. Testa URL fixa
echo ""
echo "Testando URL fixa..."
if curl -s https://n8n.jardimdofazer.com.br/healthz --tlsv1.2 --tls-max 1.3 > /dev/null 2>&1; then
    echo "   ✅ https://n8n.jardimdofazer.com.br/healthz OK"
else
    echo "   ⚠️ URL fixa ainda propagando — tenta de novo em 30s"
fi

# 9. Salva PIDs pra parar depois
echo "$N8N_PID" > ~/.n8n/n8n.pid
echo "$CF_PID" > ~/.cloudflared/cloudflared.pid

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│  Sistema no ar!                                            │"
echo "│                                                            │"
echo "│  n8n local:   http://localhost:5678                        │"
echo "│  n8n público: https://n8n.jardimdofazer.com.br             │"
echo "│  Webhook:     https://n8n.jardimdofazer.com.br/webhook/...  │"
echo "│                                                            │"
echo "│  Logs:                                                     │"
echo "│    tail -f ~/.n8n/n8n.log                                  │"
echo "│    tail -f ~/.cloudflared/tunnel.log                        │"
echo "│                                                            │"
echo "│  Pra parar: bash scripts/stop-megazord.sh                  │"
echo "└─────────────────────────────────────────────────────────────┘"
