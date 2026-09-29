#!/usr/bin/env python3
"""
debug_redirector_query.py
Reproduz EXATAMENTE a query que o redirector faz, com output verboso.
Roda e me cola a saída — vamos ver o que o Supabase está retornando.
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', '')

# Substitua pelo short_code que você acabou de gerar
SHORT_CODE = '2n0vw8'

print('─' * 60)
print('DEBUG — query do redirector')
print('─' * 60)
print(f'SUPABASE_URL  : "{SUPABASE_URL}"')
print(f'SUPABASE_KEY  : "{SUPABASE_KEY[:20]}...{SUPABASE_KEY[-8:]}"')
print(f'SHORT_CODE    : "{SHORT_CODE}"')
print()

# Query exatamente como o redirector faz
url = f'{SUPABASE_URL}/rest/v1/short_links'
params = {'short_code': f'eq.{SHORT_CODE}', 'active': 'eq.true'}
headers = {
    'apikey': SUPABASE_KEY,
    'Authorization': f'Bearer {SUPABASE_KEY}',
}

print(f'URL final     : {url}')
print(f'Params        : {params}')
print(f'Headers       : apikey={headers["apikey"][:20]}...')
print()

r = requests.get(url, params=params, headers=headers, timeout=10)

print(f'Status        : {r.status_code}')
print(f'URL chamada   : {r.url}')
print(f'Response body:')
print(r.text)
print()

# Agora testa SEM o filtro active (só pra ver se o active filter é o problema)
print('─' * 60)
print('TESTE B — sem filtro active')
print('─' * 60)
params_b = {'short_code': f'eq.{SHORT_CODE}'}
r_b = requests.get(url, params=params_b, headers=headers, timeout=10)
print(f'Status  : {r_b.status_code}')
print(f'URL     : {r_b.url}')
print(f'Body    : {r_b.text}')
print()

# Teste C — sem nenhum filtro, vê todos os links
print('─' * 60)
print('TESTE C — todos os short_links')
print('─' * 60)
r_c = requests.get(url, headers=headers, timeout=10)
print(f'Status  : {r_c.status_code}')
print(f'Body    : {r_c.text}')
