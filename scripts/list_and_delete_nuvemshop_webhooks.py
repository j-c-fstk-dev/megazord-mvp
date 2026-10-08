#!/usr/bin/env python3
"""
list_and_delete_nuvemshop_webhooks.py
Lista todos os webhooks da Nuvemshop e opcionalmente deleta os antigos.

Uso:
  python3 scripts/list_and_delete_nuvemshop_webhooks.py          # só lista
  python3 scripts/list_and_delete_nuvemshop_webhooks.py --delete # deleta todos
"""
import os, sys, json, requests
from dotenv import load_dotenv
load_dotenv()

STORE_ID = os.getenv('NUVEMSHOP_STORE_ID', '')
ACCESS_TOKEN = os.getenv('NUVEMSHOP_ACCESS_TOKEN', '')
USER_AGENT = os.getenv('NUVEMSHOP_USER_AGENT', 'Megazord-MVP')

if not STORE_ID or not ACCESS_TOKEN:
    print('❌ Credenciais Nuvemshop nao definidas no .env')
    sys.exit(1)

headers = {
    'Authorization': f'Bearer {ACCESS_TOKEN}',
    'User-Agent': USER_AGENT,
    'Content-Type': 'application/json',
}
base_url = f'https://api.nuvemshop.com.br/2025-03/{STORE_ID}/webhooks'

# Lista webhooks
print('─' * 60)
print('Webhooks configurados na Nuvemshop:')
print('─' * 60)
r = requests.get(base_url, headers=headers, timeout=10)
if r.status_code != 200:
    print(f'❌ Erro {r.status_code}: {r.text[:200]}')
    sys.exit(1)

webhooks = r.json()
if not webhooks:
    print('   (nenhum webhook configurado)')
else:
    for w in webhooks:
        print(f'  id: {w.get("id")}')
        print(f'    event: {w.get("event")}')
        print(f'    url: {w.get("url", "")[:80]}')
        print()

# Se --delete, deleta todos
if '--delete' in sys.argv:
    print('─' * 60)
    print('Deletando todos os webhooks...')
    print('─' * 60)
    for w in webhooks:
        wid = w.get('id')
        rd = requests.delete(f'{base_url}/{wid}', headers=headers, timeout=10)
        if rd.status_code in (200, 204):
            print(f'  ✅ Deletado webhook id={wid}')
        else:
            print(f'  ❌ Erro ao deletar id={wid}: {rd.status_code}')
    print()
    print('🎉 Todos os webhooks antigos foram deletados.')
    print('Agora rode: python3 scripts/create_nuvemshop_webhook.py')
else:
    print()
    print('Pra deletar todos os webhooks antigos, rode:')
    print(f'  python3 {sys.argv[0]} --delete')
