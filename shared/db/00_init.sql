-- ════════════════════════════════════════════════════════════════
-- MEGAZORD MVP — Schema Supabase inicial
-- Rodar tudo de uma vez no SQL Editor do Supabase
-- ════════════════════════════════════════════════════════════════

-- Tabela: clicks (Encaminhador)
CREATE TABLE IF NOT EXISTS clicks (
  click_id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  short_code      TEXT NOT NULL,
  destination_url TEXT NOT NULL,
  utm_source      TEXT,
  utm_medium      TEXT,
  utm_campaign    TEXT,
  utm_content     TEXT,
  utm_term        TEXT,
  clicked_at      TIMESTAMPTZ DEFAULT now(),
  ip_hash         TEXT,
  referrer        TEXT,
  user_agent      TEXT
);

CREATE INDEX IF NOT EXISTS idx_clicks_short_code  ON clicks(short_code);
CREATE INDEX IF NOT EXISTS idx_clicks_clicked_at  ON clicks(clicked_at DESC);
CREATE INDEX IF NOT EXISTS idx_clicks_utm_campaign ON clicks(utm_campaign);

-- Tabela: short_links (Encaminhador)
CREATE TABLE IF NOT EXISTS short_links (
  short_code  TEXT PRIMARY KEY,
  destination TEXT NOT NULL,
  campaign    TEXT,
  product     TEXT,
  created_at  TIMESTAMPTZ DEFAULT now(),
  active      BOOLEAN DEFAULT true
);

-- Tabela: leads (Sussurros)
CREATE TABLE IF NOT EXISTS leads (
  lead_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  instagram_handle TEXT,
  first_dm_at      TIMESTAMPTZ,
  last_dm_at       TIMESTAMPTZ,
  dm_count         INTEGER DEFAULT 0,
  full_conversation TEXT,
  analysis_json    JSONB,
  primary_pain     TEXT,
  trigger_words    TEXT[],
  objection        TEXT,
  ready_to_buy_score INTEGER,
  suggested_offer_hook TEXT,
  created_at       TIMESTAMPTZ DEFAULT now(),
  updated_at       TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_leads_handle ON leads(instagram_handle);
CREATE INDEX IF NOT EXISTS idx_leads_pain   ON leads(primary_pain);

-- Tabela: stories (Storymetro — mirror do Sheets)
CREATE TABLE IF NOT EXISTS stories (
  story_id           TEXT PRIMARY KEY,
  posted_at          TIMESTAMPTZ,
  tipo               TEXT,
  produto_mencionado TEXT,
  impressions       INTEGER,
  replies           INTEGER,
  link_clicks       INTEGER,
  sales_attributed  INTEGER,
  revenue_brl       NUMERIC(10,2),
  UNIQUE(story_id)
);

CREATE INDEX IF NOT EXISTS idx_stories_posted ON stories(posted_at DESC);
CREATE INDEX IF NOT EXISTS idx_stories_tipo   ON stories(tipo);
