/**
 * Encaminhador — Cloudflare Worker (produção)
 * Versão 3 — agora passa click_id na URL de destino
 *
 * Deploy:
 *   wrangler deploy --config modules/encaminhador/wrangler.toml
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const shortCode = url.pathname.split('/')[1];

    // Health check
    if (shortCode === 'health' || shortCode === '') {
      return new Response(
        JSON.stringify({ status: 'ok', service: 'encaminhador', version: '3', time: new Date().toISOString() }),
        { headers: { 'Content-Type': 'application/json' } }
      );
    }

    // 1. Busca destination no Supabase
    let link;
    try {
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
      link = data[0];
    } catch (err) {
      console.error('Supabase fetch failed:', err);
      return new Response('Erro ao buscar link', { status: 500 });
    }

    // 2. Pega o click_id (UUID que o Supabase gerou no INSERT anterior — vamos usar um novo UUID por clique)
    // Como o Supabase gera o click_id automaticamente no INSERT, precisamos fazer o INSERT primeiro
    // pra obter o click_id gerado. Vamos mudar a logica:
    // - Gerar UUID aqui (crypto.randomUUID())
    // - INSERT no Supabase com esse click_id
    // - Redirecionar pra destination?click_id=<esse_uuid>

    const clickId = crypto.randomUUID();

    // 3. Monta payload do clique
    const ip = request.headers.get('cf-connecting-ip') || '';
    const ipHash = await sha256(ip);
    const clickData = {
      click_id: clickId,  // AGORA nós definimos o click_id (antes deixava o Supabase gerar)
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

    // 4. Registra clique em background (nao bloqueia redirect)
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

    // 5. Monta URL de destino COM click_id
    const destUrl = new URL(link.destination);
    destUrl.searchParams.set('click_id', clickId);

    // 6. Redirect 302 pra destination + click_id
    return Response.redirect(destUrl.toString(), 302);
  }
};

// Helper: SHA-256 hash (LGPD-safe IP)
async function sha256(message) {
  const msgBuffer = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
