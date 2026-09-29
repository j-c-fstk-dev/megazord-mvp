#!/usr/bin/env bash
# Setup inicial do ambiente Python
set -e
cd "$(dirname "$0")/.."

if [ ! -d ".venv" ]; then
    echo "Criando venv..."
    python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "Criei .env a partir do .env.example — edite com suas credenciais."
fi

echo "OK. Ambiente pronto. Ative com: source .venv/bin/activate"
