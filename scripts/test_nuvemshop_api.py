#!/usr/bin/env python3
"""
test_nuvemshop_api.py
Valida o access token da Nuvemshop fazendo um GET /store info.

Uso:
  python3 scripts/test_nuvemshop_api.py
"""
import os
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

STORE_ID = os.getenv('NUVEMSHOP_STORE_ID', '')
ACCESS_TOKEN = os.getenv('NUVEMSHOP_ACCESS_TOKEN', '')
USER_AGENT = os.getenv('NUVEMSHOP_USER_AGENT', 'Megazord-MVP')

print('─' * 60)
print('Nuvemshop API connection test')
print('─' * 60)

# Valida variaveis
errors = []
if not STORE_ID or 'cole' in STORE_ID.lower():
    errors.append('NUVEMSHOP_STORE_ID nao definido no .env')
if not ACCESS_TOKEN or 'cole' in ACCESS_TOKEN.lower():
    errors.append('NUVEMSHOP_ACCESS_TOKEN nao definido no .env')

if errors:
    print('\n❌ Erros:')
    for e in errors:
        print(f'   - {e}')
    sys.exit(1)

print(f'Store ID     : {STORE_ID}')
print(f'Access token : {ACCESS_TOKEN[:15]}...{ACCESS_TOKEN[-8:]}')
print(f'User-Agent   : {USER_AGENT}')
print()

# Teste 1 — GET /store (info da loja)
print('[1/3] Testando GET /store (info da loja)...')
url = f'https://api.nuvemshop.com.br/2025-03/{STORE_ID}/store'
headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'User-Agent': USER_AGENT,
    'Content-Type': 'application/json',
}
try:
    r = requests.get(url, headers=headers, timeout=10)
    if r.status_code == 200:
        data = r.json()
        print(f'   ✅ Loja conectada: {data.get("name", "?")} (id={data.get("id", "?")})')
        print(f'   URL: {data.get("url", "?")}')
        print(f'   Country: {data.get("country", "?")}')
    elif r.status_code == 401:
        print(f'   ❌ 401 Unauthorized — token invalido ou expirado')
        sys.exit(1)
    elif r.status_code == 403:
        print(f'   ❌ 403 Forbidden — token sem permissao pra /store')
        print(f'      Body: {r.text[:200]}')
    else:
        print(f'   ⚠️ Status {r.status_code}: {r.text[:200]}')
except Exception as e:
    print(f'   ❌ Erro de conexao: {e}')
    sys.exit(1)

# Teste 2 — GET /orders (lista ultimos 5 pedidos)
print()
print('[2/3] Testando GET /orders (ultimos 5)...')
url2 = f'https://api.nuvemshop.com.br/2025-03/{STORE_ID}/orders?per_page=5'
try:
    r = requests.get(url2, headers=headers, timeout=10)
    if r.status_code == 200:
        orders = r.json()
        print(f'   ✅ {len(orders)} pedidos retornados')
        if len(orders) > 0:
            print(f'   Ultimo pedido:')
            print(f'     - id: {orders[0].get("id", "?")}')
            print(f'     - number: {orders[0].get("number", "?")}')
            print(f'     - status: {orders[0].get("status", "?")}')
            print(f'     - payment_status: {orders[0].get("payment_status", "?")}')
            print(f'     - total: {orders[0].get("total", "?")} {orders[0].get("currency", "?")}')
            print(f'     - buyer: {orders[0].get("customer", {}).get("name", "?")}')
            print(f'     - email: {orders[0].get("contact_email", orders[0].get("customer", {}).get("email", "?"))}')
    else:
        print(f'   ⚠️ Status {r.status_code}: {r.text[:200]}')
except Exception as e:
    print(f'   ❌ Erro: {e}')

# Teste 3 — GET /webhooks (lista webhooks existentes)
print()
print('[3/3] Testando GET /webhooks (lista webhooks configurados)...')
url3 = f'https://api.nuvemshop.com.br/2025-03/{STORE_ID}/webhooks'
try:
    r = requests.get(url3, headers=headers, timeout=10)
    if r.status_code == 200:
        webhooks = r.json()
        print(f'   ✅ {len(webhooks)} webhooks ja configurados')
        for w in webhooks:
            print(f'     - id={w.get("id")}, event={w.get("event")}, url={w.get("url", "")[:60]}')
    else:
        print(f'   ⚠️ Status {r.status_code}: {r.text[:200]}')
except Exception as e:
    print(f'   ❌ Erro: {e}')

print()
print('─' * 60)
print('Se os 3 testes passaram, Nuvemshop API OK.')
print('Proximo passo: criar webhook order/paid apontando pro seu n8n.')
print('─' * 60)
