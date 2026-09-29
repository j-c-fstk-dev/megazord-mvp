# Megazord MVP

Reconstrucao zero-custo do ecossistema de 5 ferramentas que puxa dados de stories,
links, vendas e DMs e devolve o conteudo da manha pronto.

## Filhotes (modulos)

| Apelido       | Original        | Funcao                                       |
|---------------|-----------------|----------------------------------------------|
| encaminhador  | Maquina Links   | Redirector rastreavel (Cloudflare Worker)    |
| vitrine       | Linda Visao     | Painel de vendas (Sheets + Looker)           |
| storymetro    | StoryRocks      | Medidor de stories (Meta Graph API)          |
| sussurros     | Entrelinhas     | Analisador de DMs (GLM)                      |
| sintetizador  | Megazord        | Orquestrador diario (n8n cron)               |

## Estrutura

```
megazord-mvp/
├── docs/                  # Documentacao (blueprint PDF, diagrams)
├── modules/               # Um dir por filhote
│   ├── encaminhador/      # src/ tests/ scripts/
│   ├── vitrine/
│   ├── storymetro/
│   ├── sussurros/
│   └── sintetizador/
├── shared/                # Assets reusaveis
│   ├── db/                 # SQL migrations Supabase
│   ├── prompts/           # Prompts GLM
│   ├── n8n/               # Workflows JSON
│   ├── looker/            # Templates Looker
│   └── manychat/          # Fluxos ManyChat JSON
└── scripts/               # Scripts setup/utilitarios
```

## Setup rapido

1. `cp .env.example .env` e preencha credenciais
2. `python3 -m venv .venv && source .venv/bin/activate`
3. `pip install -r requirements.txt`
4. Siga `docs/blueprint.pdf` capitulo por capitulo

## Stack

- n8n (local) — orchestracao
- Supabase free — banco
- Google Sheets — dados ad-hoc
- Looker Studio — dashboards
- ManyChat free — automacao IG
- GLM (z.ai) free — IA
- Cloudflare Workers/Pages — redirector + dominio
- Hotmart — checkout

## Custo

R$ 0,00 ate atingir limites. Primeiro gatilho de custo:
provavelmente ManyChat Pro (R$ 45/mes) quando lista IG passar de 1000.
