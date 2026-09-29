"""
Encaminhador — Redirector local (dev/test)
Flask app que registra clique no Supabase e redireciona.
Roda em http://localhost:5000

Uso:
  python3 src/redirector.py

Teste:
  curl -L "http://localhost:5000/abc123?utm_source=ig-story"
"""
import os
import hashlib
from flask import Flask, request, redirect
import requests
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    raise SystemExit("Defina SUPABASE_URL e SUPABASE_ANON_KEY no .env")

app = Flask(__name__)


def hash_ip(ip: str) -> str:
    """Hash SHA256 do IP para LGPD-safe tracking."""
    return hashlib.sha256(ip.encode('utf-8')).hexdigest()


@app.route('/health')
def health():
    return {'status': 'ok'}


@app.route('/<short_code>')
def redirector(short_code: str):
    # 1. Busca destination no Supabase
    headers = {
        'apikey': SUPABASE_KEY,
        'Authorization': f'Bearer {SUPABASE_KEY}',
    }
    r = requests.get(
        f'{SUPABASE_URL}/rest/v1/short_links',
        params={'short_code': f'eq.{short_code}', 'active': 'eq.true'},
        headers=headers,
        timeout=5,
    )
    data = r.json()
    if not data:
        return 'Link nao encontrado', 404
    link = data[0]

    # 2. Registra clique (fire-and-forget; se falhar, redirect continua)
    try:
        click_data = {
            'short_code': short_code,
            'destination_url': link['destination'],
            'utm_source': request.args.get('utm_source'),
            'utm_medium': request.args.get('utm_medium'),
            'utm_campaign': request.args.get('utm_campaign') or link.get('campaign'),
            'utm_content': request.args.get('utm_content'),
            'utm_term': request.args.get('utm_term'),
            'ip_hash': hash_ip(request.remote_addr or ''),
            'referrer': request.referrer,
            'user_agent': request.headers.get('User-Agent'),
        }
        requests.post(
            f'{SUPABASE_URL}/rest/v1/clicks',
            headers={**headers, 'Content-Type': 'application/json', 'Prefer': 'return=minimal'},
            json=click_data,
            timeout=5,
        )
    except Exception as e:
        app.logger.warning(f"Falha ao registrar clique: {e}")

    # 3. Redirect 302
    return redirect(link['destination'], code=302)


if __name__ == '__main__':
    # threaded=True para dev com requests simultaneos
    app.run(host='0.0.0.0', port=5000, threaded=True, debug=False)
