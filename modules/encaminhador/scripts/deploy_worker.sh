#!/usr/bin/env bash
# deploy_worker.sh — deploy do Encaminhador para Cloudflare Worker
# Pré-requisitos:
#   1. npm install -g wrangler
#   2. wrangler login
#   3. Variaveis SUPABASE_URL e SUPABASE_ANON_KEY no .env

set -e
cd "$(dirname "$0")/.."
source .env 2>/dev/null || true

if ! command -v wrangler &>/dev/null; then
    echo "Instale wrangler primeiro: npm install -g wrangler"
    exit 1
fi

if [ -z "$SUPABASE_URL" ] || [ -z "$SUPABASE_ANON_KEY" ]; then
    echo "Defina SUPABASE_URL e SUPABASE_ANON_KEY no .env"
    exit 1
fi

# Cria wrangler.toml se nao existe
if [ ! -f "modules/encaminhador/wrangler.toml" ]; then
    cat > modules/encaminhador/wrangler.toml <<WRANGLER
name = "encaminhador"
main = "src/worker.js"
compatibility_date = "2024-09-23"
WRANGLER
fi

# Copia o worker.js para modules/encaminhador/src/
mkdir -p modules/encaminhador/src
cp scripts/encaminhador_worker.js modules/encaminhador/src/worker.js

# Seta secrets
echo "$SUPABASE_URL" | wrangler secret put SUPABASE_URL --config modules/encaminhador/wrangler.toml
echo "$SUPABASE_ANON_KEY" | wrangler secret put SUPABASE_ANON_KEY --config modules/encaminhador/wrangler.toml

# Deploy
wrangler deploy --config modules/encaminhador/wrangler.toml

echo ""
echo "Worker deployed. URL sera algo como:"
echo "  https://encaminhador.<seu-subdominio>.workers.dev"
echo ""
echo "Para usar em producao, configure um dominio customizado:"
echo "  - Cloudflare Dashboard > Workers > encaminhador > Triggers > Custom Domains"
echo "  - Adicione ex: link.seudominio.com"
