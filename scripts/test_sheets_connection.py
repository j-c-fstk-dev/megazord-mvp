#!/usr/bin/env python3
"""
test_sheets_connection.py
Valida que a service account Google consegue:
  1. Ler o JSON de credenciais
  2. Autenticar no Google Sheets API
  3. Ler a primeira linha da planilha (cabeçalhos)
  4. Inserir uma linha de teste e remover

Uso:
  python3 scripts/test_sheets_connection.py
"""
import os
import sys
import time
from dotenv import load_dotenv

load_dotenv()

# Instala dependencia se faltar
try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print('Instalando dependencias do Google...')
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install',
                          'google-api-python-client', 'google-auth'])
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

SHEETS_ID = os.getenv('SHEETS_ID', '')
SA_FILE = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', './service-account.json')

print('─' * 60)
print('Google Sheets connection test')
print('─' * 60)

# 1. Valida variaveis
errors = []
if not SHEETS_ID or 'SUA-PLANILHA' in SHEETS_ID or 'XXXX' in SHEETS_ID:
    errors.append('SHEETS_ID nao definido no .env')
if not os.path.exists(SA_FILE):
    errors.append(f'Arquivo da service account nao encontrado: {SA_FILE}')

if errors:
    print('\n❌ Erros:')
    for e in errors:
        print(f'   - {e}')
    sys.exit(1)

print(f'SHEETS_ID            : {SHEETS_ID[:15]}...')
print(f'Service account file : {SA_FILE}')
print()

# 2. Carrega credenciais
print('[1/4] Carregando credenciais da service account...')
try:
    creds = Credentials.from_service_account_file(
        SA_FILE,
        scopes=['https://www.googleapis.com/auth/spreadsheets',
                'https://www.googleapis.com/auth/drive.metadata.readonly'],
    )
    print(f'   ✅ Credenciais carregadas — client_email: {creds.service_account_email}')
except Exception as e:
    print(f'   ❌ Erro ao carregar JSON: {e}')
    sys.exit(1)

# 3. Conecta no Sheets
print()
print('[2/4] Conectando no Google Sheets API...')
try:
    service = build('sheets', 'v4', credentials=creds, static_discovery=False)
    print('   ✅ Servico Sheets v4 conectado')
except Exception as e:
    print(f'   ❌ Erro ao conectar: {e}')
    sys.exit(1)

# 4. Le primeira linha (cabeçalhos)
print()
print('[3/4] Lendo primeira linha da aba "vendas" (cabeçalhos)...')
try:
    result = service.spreadsheets().values().get(
        spreadsheetId=SHEETS_ID,
        range='vendas!A1:N1',
    ).execute()
    values = result.get('values', [])
    if not values:
        print('   ❌ Aba "vendas" nao encontrada ou vazia na linha 1')
        print('   Verifique: renomeou a aba de "Sheet1" pra "vendas"?')
        print('   E colocou os 14 cabecalhos na linha 1?')
        sys.exit(1)
    headers = values[0]
    print(f'   ✅ {len(headers)} colunas encontradas:')
    print(f'      {", ".join(headers[:5])}...')
except HttpError as e:
    print(f'   ❌ Erro HTTP {e.status_code}: {e._get_reason()}')
    if e.status_code == 403:
        print('   ⚠️  Verifique se compartilhou a planilha com a service account (Editor)')
        print(f'       Email da service account: {creds.service_account_email}')
    sys.exit(1)

# 5. Insere linha de teste e remove
print()
print('[4/4] Inserindo linha de teste e removendo...')
test_row = [
    '2026-09-29T12:00:00Z',  # data
    'TEST-TXN-001',          # transaction_id
    'TEST-PROD-001',         # product_id
    'Produto Teste',         # product_name
    197.00,                  # value_brl
    'Maria Teste',           # buyer_name
    'maria.teste@example.com',  # buyer_email
    'test-click-id-001',     # click_id
    'ig-story',              # utm_source
    'social',                # utm_medium
    'teste-sheets-conn',     # utm_campaign
    'test-conn',             # utm_content
    '',                      # utm_term
    '',                      # bundle_id
]
try:
    # Insert
    service.spreadsheets().values().append(
        spreadsheetId=SHEETS_ID,
        range='vendas!A1',
        valueInputOption='RAW',
        body={'values': [test_row]},
    ).execute()
    print('   ✅ Linha de teste inserida')

    # Espera 1s pro Google propagar
    time.sleep(1)

    # Acha a linha de teste e remove
    find_result = service.spreadsheets().values().get(
        spreadsheetId=SHEETS_ID,
        range='vendas!B:B',  # transaction_id coluna B
    ).execute()
    rows = find_result.get('values', [])
    test_row_index = None
    for i, row in enumerate(rows):
        if row and row[0] == 'TEST-TXN-001':
            test_row_index = i + 1  # sheets 1-indexed
            break

    if test_row_index:
        # Limpa a linha (Delete via batchUpdate clear)
        service.spreadsheets().values().clear(
            spreadsheetId=SHEETS_ID,
            range=f'vendas!A{test_row_index}:N{test_row_index}',
        ).execute()
        print(f'   🧹 Linha {test_row_index} (teste) removida')
    else:
        print('   ⚠️ Linha de teste nao encontrada pra remocao (limpe manualmente)')

except HttpError as e:
    print(f'   ❌ Erro HTTP {e.status_code}: {e._get_reason()}')
    sys.exit(1)

print()
print('─' * 60)
print('🎉 TUDO OK! Google Sheets pronto pra receber vendas via n8n.')
print('─' * 60)
print('Proximo passo: configurar webhook Hotmart + workflow n8n.')
print(f'Email da service account (ja configurado): {creds.service_account_email}')
