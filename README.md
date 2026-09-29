# Megazord MVP

Reconstrucao zero-custo do ecossistema de 5 ferramentas que puxa dados de stories,
links, vendas e DMs e devolve o conteudo da manha pronto.

## Status atual

| Filhote | Status | URL / Nota |
|---------|--------|-----------|
| Encaminhador | ✅ Deploy Cloudflare Worker | `https://encaminhador.jardimdofazer.workers.dev` |
| Vitrine | ⏳ Pendente | - |
| Storymetro | ⏳ Pendente | - |
| Sussurros | ⏳ Pendente | - |
| Sintetizador | ⏳ Pendente | - |

## Filhotes (modulos)

| Apelido       | Original        | Funcao                                       |
|---------------|-----------------|----------------------------------------------|
| encaminhador  | Maquina Links   | Redirector rastreavel (Cloudflare Worker)    |
| vitrine       | Linda Visao     | Painel de vendas (Sheets + Looker)           |
| storymetro    | StoryRocks      | Medidor de stories (Meta Graph API)          |
| sussurros     | Entrelinhas     | Analisador de DMs (GLM)                      |
| sintetizador  | Megazord        | Orquestrador diario (n8n cron)               |

## Estrutura

megazord-mvp/
├── docs/ # Documentacao (blueprint PDF, diagrams)
├── modules/ # Um dir por filhote
│ ├── encaminhador/ # ✅ src/ tests/ scripts/ wrangler.toml
│ ├── vitrine/ # src/ tests/ scripts/
│ ├── storymetro/
│ ├── sussurros/
│ └── sintetizador/
├── shared/ # Assets reusaveis
│ ├── db/ # SQL migrations Supabase
│ ├── prompts/ # Prompts GLM
│ ├── n8n/ # Workflows JSON
│ ├── looker/ # Templates Looker
│ └── manychat/ # Fluxos ManyChat JSON
└── scripts/ # Scripts setup/utilitarios


## Setup rapido

1. `cp .env.example .env` e preencha credenciais (Supabase + SHORT_DOMAIN)
2. `python3 -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. `bash scripts/setup_local.sh`
5. `python3 scripts/test_supabase_connection.py` (valida Supabase)
6. Siga `docs/blueprint.md` para o proximo filhote

## Deploy do Encaminhador (Cloudflare Worker)

```bash
# 1. Configure Wrangler (uma vez)
export CLOUDFLARE_API_TOKEN=...
export CLOUDFLARE_ACCOUNT_ID=...

# 2. Deploy
wrangler deploy --config modules/encaminhador/wrangler.toml

# 3. Seta secrets do Supabase
wrangler secret put SUPABASE_URL --config modules/encaminhador/wrangler.toml
wrangler secret put SUPABASE_ANON_KEY --config modules/encaminhador/wrangler.toml

Stack
n8n (local) — orchestracao
Supabase free — banco
Google Sheets — dados ad-hoc
Looker Studio — dashboards
ManyChat free — automacao IG
GLM (z.ai) free — IA
Cloudflare Workers/Pages — redirector + dominio
Hotmart — checkout
Custo
R
0,00ateatingirlimites.Primeirogatilhodecusto:provavelmenteManyChatPro(R
 45/mes) quando lista IG passar de 1000.
