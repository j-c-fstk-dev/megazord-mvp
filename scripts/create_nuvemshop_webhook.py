#!/usr/bin/env python3
"""
create_nuvemshop_webhook.py
Cria webhook order/paid na Nuvemshop apontando pro seu n8n.
Salva o secret gerado em webhook_secret.txt (que esta no .gitignore).

Como usar:
1. Edita WEBHOOK_URL abaixo
2. Roda: python3 scripts/create_nuvemshop_webhook.py
3. O secret gerado fica em webhook_secret.txt
4. Copia o secret pro Code 1 do n8n (substitui COLE_SEU_SECRET_AQUI)
"""
import os
import sys
import json
import secrets
import requests
from dotenv import load_dotenv

load_dotenv()

# ════════════════════════════════════════════════════════════════
# CONFIGURACAO — edita essa linha
# ════════════════════════════════════════════════════════════════
WEBHOOK_URL = 'https://potatoes-ours-backing-lexington.trycloudflare.com/webhook/nuvemshop-vendas'

# ════════════════════════════════════════════════════════════════
# Credenciais (vem do .env)
# ════════════════════════════════════════════════════════════════
STORE_ID = os.getenv('NUVEMSHOP_STORE_ID', '')
ACCESS_TOKEN = os.getenv('NUVEMSHOP_ACCESS_TOKEN', '')
USER_AGENT = os.getenv('NUVEMSHOP_USER_AGENT', 'Megazord-MVP')

if not STORE_ID or not ACCESS_TOKEN:
    print('❌ NUVEMSHOP_STORE_ID ou NUVEMSHOP_ACCESS_TOKEN nao definidos no .env')
    sys.exit(1)

# Gera secret aleatório (32 chars)
WEBHOOK_SECRET = secrets.token_urlsafe(32)

# Salva em arquivo (que esta no .gitignore)
with open('webhook_secret.txt', 'w') as f:
    f.write(WEBHOOK_SECRET)

print(f'🔑 Webhook secret gerado e salvo em webhook_secret.txt')
print(f'   Tamanho: {len(WEBHOOK_SECRET)} chars')
print(f'   (arquivo protegido pelo .gitignore, nao vai pro git)')
print()

# URL final com secret na query string
full_url = f'{WEBHOOK_URL}?secret={WEBHOOK_SECRET}'

print('─' * 60)
print('Criando webhook order/paid na Nuvemshop')
print('─' * 60)
print(f'Store ID     : {STORE_ID}')
print(f'Webhook URL  : {WEBHOOK_URL}')
print(f'Full URL     : {full_url[:80]}...')
print(f'Event        : order/paid')
print()

# POST /webhooks
url = f'https://api.nuvemshop.com.br/2025-03/{STORE_ID}/webhooks'
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'User-Agent': USER_AGENT,
    'Content-Type': 'application/json',
}
payload = {
    'event': 'order/paid',
    'url': full_url,
}

print('[1/2] Enviando POST /webhooks...')
r = requests.post(url, headers=headers, json=payload, timeout=15)

if r.status_code == 201:
    data = r.json()
    print(f'   ✅ Webhook criado!')
    print(f'     id: {data.get("id")}')
    print(f'     event: {data.get("event")}')
    print(f'     url: {data.get("url")[:80]}...')
    print()
    print('─' * 60)
    print('🎉 WEBHOOK CRIADO!')
    print('─' * 60)
    print()
    print('PROXIMOS PASSOS:')
    print(f'1. Copia o secret de webhook_secret.txt:')
    print(f'   cat webhook_secret.txt')
    print(f'2. Edita o Code 1 do n8n e substitui COLE_SEU_SECRET_AQUI')
    print(f'3. Faz venda de teste na loja')
    print(f'4. Verifica a linha aparecer na planilha Google Sheets')
else:
    print(f'   ❌ Erro {r.status_code}: {r.text[:300]}')
    sys.exit(1)#!/usr/bin/env python3
"""
create_nuvemshop_webhook.py
Cria webhook order/paid na Nuvemshop apontando pro seu n8n.

Como usar:
1. Edita as variaveis WEBHOOK_URL e WEBHOOK_SECRET abaixo
2. Roda: python3 scripts/create_nuvemshop_webhook.py
"""
import os
import sys
import json
import secrets
import requests
from dotenv import load_dotenv

load_dotenv()

# ════════════════════════════════════════════════════════════════
# CONFIGURACAO — edita essas 2 linhas
# ════════════════════════════════════════════════════════════════

# URL do seu n8n (quick tunnel ou tunnel fixo depois que tiver cartao)
# Substitua pela URL ATUAL do trycloudflare
WEBHOOK_URL = 'https://potatoes-ours-backing-lexington.trycloudflare.com/webhook/nuvemshop-vendas'

# Secret aleatorio pra proteger o webhook (nao usar HMAC da Nuvemshop porque
# estamos no Forma B - sem app OAuth)
WEBHOOK_SECRET = secrets.token_urlsafe(32)
print(f'🔑 Webhook secret gerado: {WEBHOOK_SECRET}')
print(f'   Anote esse secret — você vai precisar no Code 1 do n8n')
print()

# ════════════════════════════════════════════════════════════════
# Credenciais (vem do .env)
# ════════════════════════════════════════════════════════════════
STORE_ID = os.getenv('NUVEMSHOP_STORE_ID', '')
ACCESS_TOKEN = os.getenv('NUVEMSHOP_ACCESS_TOKEN', '')
USER_AGENT = os.getenv('NUVEMSHOP_USER_AGENT', 'Megazord-MVP')

if not STORE_ID or not ACCESS_TOKEN:
    print('❌ NUVEMSHOP_STORE_ID ou NUVEMSHOP_ACCESS_TOKEN nao definidos no .env')
    sys.exit(1)

# URL final com secret na query string
full_url = f'{WEBHOOK_URL}?secret={WEBHOOK_SECRET}'

print('─' * 60)
print('Criando webhook order/paid na Nuvemshop')
print('─' * 60)
print(f'Store ID     : {STORE_ID}')
print(f'Webhook URL  : {WEBHOOK_URL}')
print(f'Full URL     : {full_url[:80]}...')
print(f'Event        : order/paid')
print()

# POST /webhooks
url = f'https://api.nuvemshop.com.br/2025-03/{STORE_ID}/webhooks'
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'User-Agent': USER_AGENT,
    'Content-Type': 'application/json',
}
payload = {
    'event': 'order/paid',
    'url': full_url,
}

print('[1/2] Enviando POST /webhooks...')
r = requests.post(url, headers=headers, json=payload, timeout=15)

if r.status_code == 201:
    data = r.json()
    print(f'   ✅ Webhook criado!')
    print(f'     id: {data.get("id")}')
    print(f'     event: {data.get("event")}')
    print(f'     url: {data.get("url")[:80]}...')
    print()
    print('─' * 60)
    print('🎉 WEBHOOK CRIADO!')
    print('─' * 60)
    print()
    print('PROXIMOS PASSOS:')
    print(f'1. Atualize o Code 1 do n8n pra verificar o secret:')
    print(f'   - No inicio do codigo, adicione:')
    print(f'     const secret = $input.first().json.query?.secret || "";')
    print(f'     if (secret !== "{WEBHOOK_SECRET}") return [{JSON.stringify({json: {error: "unauthorized"}})}];')
    print()
    print(f'2. Anote o secret em lugar seguro: {WEBHOOK_SECRET}')
    print(f'3. Faça uma venda de teste na loja')
    print(f'4. Verifique a linha aparecer na planilha Google Sheets')
else:
    print(f'   ❌ Erro {r.status_code}: {r.text[:300]}')
    sys.exit(1)
