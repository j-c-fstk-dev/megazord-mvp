/**
 * Encaminhador — Cloudflare Worker (produção)
 * Mesma lógica do redirector Python, mas rodando no edge da Cloudflare.
 * Latência global < 50ms, free tier: 100k requests/dia.
 *
 * Deploy:
 *   1. Instale wrangler: npm install -g wrangler
 *   2. Login: wrangler login
 *   3. Configure secrets:
 *      wrangler secret put SUPABASE_URL
 *      wrangler secret put SUPABASE_ANON_KEY
 *   4. Deploy: wrangler deploy
 *
 * Ou copie este código direto no dashboard Cloudflare > Workers.
 */

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const shortCode = url.pathname.split('/')[1];

    // Health check
    if (shortCode === 'health') {
      return new Response(JSON.stringify({ status: 'ok' }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    if (!shortCode) {
      return new Response('Encaminhador — redirector ativo', { status: 200 });
    }

    // 1. Busca destination no Supabase
    const r = await fetch(
      `${env.SUPABASE_URL}/rest/v1/short_links?short_code=eq.${shortCode}&active=eq.true`,
      {
        headers: {
          apikey: env.SUPABASE_ANON_KEY,
          Authorization: `Bearer ${env.SUPABASE_ANON_KEY}`,
        },
      }
    );
    const data = await r.json();
    if (!data || data.length === 0) {
      return new Response('Link nao encontrado', { status: 404 });
    }
    const link = data[0];

    // 2. Monta payload do clique
    const ip = request.headers.get('cf-connecting-ip') || '';
    const ipHash = await sha256(ip);
    const clickData = {
      short_code: shortCode,
      destination_url: link.destination,
      utm_source: url.searchParams.get('utm_source'),
      utm_medium: url.searchParams.get('utm_medium'),
      utm_campaign: url.searchParams.get('utm_campaign') || link.campaign,
      utm_content: url.searchParams.get('utm_content'),
      utm_term: url.searchParams.get('utm_term'),
      ip_hash: ipHash,
      referrer: request.headers.get('referer'),
      user_agent: request.headers.get('user-agent'),
    };

    // 3. Registra clique em background (nao bloqueia redirect)
    // ctx.waitUntil eh essencial aqui
    const ctx = request.ctx || { waitUntil: (p) => p };
    ctx.waitUntil(
      fetch(`${env.SUPABASE_URL}/rest/v1/clicks`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          apikey: env.SUPABASE_ANON_KEY,
          Authorization: `Bearer ${env.SUPABASE_ANON_KEY}`,
          Prefer: 'return=minimal',
        },
        body: JSON.stringify(clickData),
      }).catch((err) => console.error('click log failed:', err))
    );

    // 4. Redirect 302
    return Response.redirect(link.destination, 302);
  }
};

// Helper: SHA-256 hash (para LGPD-safe IP hashing)
async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
