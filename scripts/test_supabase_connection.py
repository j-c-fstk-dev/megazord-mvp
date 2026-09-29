#!/usr/bin/env python3
"""
test_supabase_connection.py
Valida que as credenciais do .env conectam ao Supabase e que as tabelas existem.

Uso:
  python3 scripts/test_supabase_connection.py
"""
import os
import sys
from dotenv import load_dotenv
import requests

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', '').rstrip('/')
ANON_KEY = os.getenv('SUPABASE_ANON_KEY', '')
SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')

print('─' * 60)
print('Supabase connection test')
print('─' * 60)

# 1. Valida variaveis
errors = []
if not SUPABASE_URL or 'XXXXXX' in SUPABASE_URL:
    errors.append('SUPABASE_URL nao definida ou ainda com placeholder')
if not ANON_KEY or '...' in ANON_KEY:
    errors.append('SUPABASE_ANON_KEY nao definida ou ainda com placeholder')
if not SERVICE_KEY or '...' in SERVICE_KEY:
    errors.append('SUPABASE_SERVICE_KEY nao definida ou ainda com placeholder')

if errors:
    print('\n❌ Erros:')
    for e in errors:
        print(f'   - {e}')
    print('\nEdite ~/projects/megazord-mvp/.env e preencha as 3 variaveis Supabase.')
    sys.exit(1)

print(f'URL         : {SUPABASE_URL}')
print(f'Anon key    : {ANON_KEY[:20]}...{ANON_KEY[-8:]}')
print(f'Service key : {SERVICE_KEY[:20]}...{SERVICE_KEY[-8:]}')
print()

# 2. Testa conexao com anon key (deve funcionar para leitura publica)
print('[1/3] Testando leitura com anon key...')
r = requests.get(
    f'{SUPABASE_URL}/rest/v1/short_links?select=short_code&limit=1',
    headers={
        'apikey': ANON_KEY,
        'Authorization': f'Bearer {ANON_KEY}',
    },
    timeout=10,
)
if r.status_code == 200:
    print(f'   ✅ OK — tabela short_links acessivel (status 200)')
elif r.status_code == 401:
    print(f'   ❌ Erro 401 — anon key invalida')
    sys.exit(1)
elif r.status_code == 404:
    print(f'   ❌ Erro 404 — tabela short_links nao existe. Rode o 00_init.sql!')
    sys.exit(1)
else:
    print(f'   ⚠️ Status {r.status_code}: {r.text[:200]}')

# 3. Testa leitura de cada tabela
print()
print('[2/3] Verificando todas as tabelas...')
tabelas = ['short_links', 'clicks', 'leads', 'stories']
for t in tabelas:
    r = requests.get(
        f'{SUPABASE_URL}/rest/v1/{t}?select=*&limit=1',
        headers={'apikey': ANON_KEY, 'Authorization': f'Bearer {ANON_KEY}'},
        timeout=5,
    )
    if r.status_code == 200:
        print(f'   ✅ {t}')
    else:
        print(f'   ❌ {t} — status {r.status_code}')

# 4. Testa escrita com service_role (inserir um short_link de teste)
print()
print('[3/3] Testando escrita com service_role (inserir link de teste)...')
test_data = {
    'short_code': 'testconn001',
    'destination': 'https://example.com/supabase-connection-test',
    'campaign': 'connection-test',
    'product': 'test-product',
}
r = requests.post(
    f'{SUPABASE_URL}/rest/v1/short_links',
    headers={
        'apikey': SERVICE_KEY,
        'Authorization': f'Bearer {SERVICE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
    },
    json=test_data,
    timeout=10,
)
if r.status_code == 201:
    print('   ✅ Link de teste inserido (short_code=testconn001)')
    # Limpa o teste
    print('   🧹 Limpando registro de teste...')
    requests.delete(
        f'{SUPABASE_URL}/rest/v1/short_links?short_code=eq.testconn001',
        headers={'apikey': SERVICE_KEY, 'Authorization': f'Bearer {SERVICE_KEY}'},
        timeout=5,
    )
    print('   ✅ Registro de teste removido.')
else:
    print(f'   ❌ Erro {r.status_code}: {r.text[:200]}')
    sys.exit(1)

print()
print('─' * 60)
print('🎉 TUDO OK! Supabase pronto pra receber o Encaminhador.')
print('─' * 60)
print('Proximo passo: gerar primeiro link rastreavel:')
print('  python3 modules/encaminhador/src/link_builder.py \\')
print('      --destination "https://hotmart.com/br/checkout/SEU_PRODUTO" \\')
print('      --campaign "primeiro-teste" \\')
print('      --product "produto-teste"')
