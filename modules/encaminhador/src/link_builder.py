"""
Encaminhador — CLI para gerar novo link rastreavel
Insere na tabela short_links do Supabase e devolve URL final com UTMs.

Uso:
  python3 src/link_builder.py \
      --destination "https://hotmart.com/br/checkout/XXX" \
      --campaign "lancamento-curso-maes" \
      --product "curso-mae-confeiteira" \
      --utm-source ig-story --utm-content story-2026-09-28-prova
"""
import argparse
import os
import secrets
import string
import sys
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY')  # service key (RLS bypass)
SHORT_DOMAIN = os.getenv('SHORT_DOMAIN', 'http://localhost:5000')

if not SUPABASE_URL or not SUPABASE_KEY:
    sys.exit("Defina SUPABASE_URL e SUPABASE_SERVICE_KEY no .env")


def gen_short_code(length: int = 6) -> str:
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))


def create_link(destination: str,
                 campaign: str,
                 product: str,
                 utm_source: str = 'ig-story',
                 utm_medium: str = 'social',
                 utm_content: str = '',
                 utm_term: str = '') -> dict:
    short = gen_short_code()
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
        'Content-Type': 'application/json',
        'Prefer': 'return=representation',
    }
    # Insere short_link
    payload = {
        'short_code': short,
        'destination': destination,
        'campaign': campaign,
        'product': product,
    }
    r = requests.post(f'{SUPABASE_URL}/rest/v1/short_links',
                     headers=headers, json=payload, timeout=10)
    if r.status_code != 201:
        raise RuntimeError(f"Supabase erro {r.status_code}: {r.text}")

    # Monta URL final com UTMs
    params = {
        'utm_source': utm_source,
        'utm_medium': utm_medium,
        'utm_campaign': campaign,
    }
    if utm_content:
        params['utm_content'] = utm_content
    if utm_term:
        params['utm_term'] = utm_term
    query = '&'.join(f'{k}={v}' for k, v in params.items() if v)
    final_url = f'{SHORT_DOMAIN}/{short}?{query}'
    return {'short_code': short, 'final_url': final_url, 'destination': destination}


def main():
    p = argparse.ArgumentParser(description='Encaminhador — gerador de links rastreaveis')
    p.add_argument('--destination', required=True, help='URL final (Hotmart/Kiwify/etc.)')
    p.add_argument('--campaign', required=True, help='Nome da campanha (utm_campaign)')
    p.add_argument('--product', required=True, help='Nome do produto')
    p.add_argument('--utm-source', default='ig-story')
    p.add_argument('--utm-medium', default='social')
    p.add_argument('--utm-content', default='', help='Ex: story-2026-09-28-prova')
    p.add_argument('--utm-term', default='', help='Ex: maes-primeira-renda')
    args = p.parse_args()

    result = create_link(
        destination=args.destination,
        campaign=args.campaign,
        product=args.product,
        utm_source=args.utm_source,
        utm_medium=args.utm_medium,
        utm_content=args.utm_content,
        utm_term=args.utm_term,
    )
    print(f'\nLink criado!')
    print(f'  Short code : {result["short_code"]}')
    print(f'  Destination: {result["destination"]}')
    print(f'\n>>> URL rastreavel <<<')
    print(f'{result["final_url"]}\n')


if __name__ == '__main__':
    main()
