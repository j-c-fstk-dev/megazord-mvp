#!/usr/bin/env python3
"""
gerar_credentials_file.py
Decodifica o token JWT do cloudflared e gera o arquivo de credentials JSON.

Uso:
  python3 scripts/gerar_credentials_file.py
"""
import os
import sys
import json
import base64

# Token do cloudflared (lido de /etc/cloudflared/token)
TOKEN_PATH = '/etc/cloudflared/token'
OUTPUT_PATH = os.path.expanduser('~/.cloudflared/7e718134-4bdf-434b-8b2d-a0cad82b8c76.json')

print('─' * 60)
print('Gerar credentials file do cloudflared a partir do token')
print('─' * 60)

# 1. Ler o token (precisa de sudo)
print(f'[1/4] Lendo token de {TOKEN_PATH}...')
import subprocess
try:
    result = subprocess.run(['sudo', 'cat', TOKEN_PATH], capture_output=True, text=True, check=True)
    token = result.stdout.strip()
except subprocess.CalledProcessError as e:
    print(f'   ❌ Erro ao ler token: {e}')
    sys.exit(1)

if not token:
    print('   ❌ Token vazio')
    sys.exit(1)

print(f'   ✅ Token lido ({len(token)} chars)')

# 2. Decodificar o JWT (header.payload.signature)
print('\n[2/4] Decodificando JWT...')
parts = token.split('.')
if len(parts) != 3:
    print(f'   ❌ Token não é JWT válido (esperado 3 partes, tem {len(parts)})')
    sys.exit(1)

def b64decode_jwt(part):
    # JWT usa base64url (sem padding)
    padding = 4 - len(part) % 4
    if padding != 4:
        part += '=' * padding
    return base64.urlsafe_b64decode(part)

try:
    payload = json.loads(b64decode_jwt(parts[1]))
except Exception as e:
    print(f'   ❌ Erro ao decodificar: {e}')
    sys.exit(1)

print(f'   ✅ Payload decodificado:')
print(f'      - account_tag: {payload.get("a")}')
print(f'      - tunnel_id:   {payload.get("t")}')
print(f'      - tunnel_secret: {payload.get("s")[:20]}...')

# 3. Montar o credentials file
print('\n[3/4] Montando credentials file...')
credentials = {
    'AccountTag': payload.get('a'),
    'TunnelID': payload.get('t'),
    'TunnelSecret': payload.get('s'),
}

# 4. Salvar
print(f'\n[4/4] Salvando em {OUTPUT_PATH}...')
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w') as f:
    json.dump(credentials, f, indent=2)

# Confere
print(f'\n✅ Arquivo criado:')
print(f'   {OUTPUT_PATH}')
with open(OUTPUT_PATH) as f:
    print(f'\nConteúdo:')
    print(f.read())

# Permissões seguras
os.chmod(OUTPUT_PATH, 0o600)
print(f'\nPermissões: 600 (apenas você)')

print('\n─' * 30)
print('Pronto! Agora rode:')
print('  cloudflared tunnel --config ~/.cloudflared/config.yml run megazord-n8n')
print('─' * 30)
