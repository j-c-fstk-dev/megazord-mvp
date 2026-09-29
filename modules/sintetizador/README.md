# Sintetizador (Megazord)

Orquestrador diário. 06:00 todo dia, puxa dados dos 4 filhotes e monta plano de conteúdo.

## Stack
- Orquestração: n8n cron workflow
- IA: GLM (z.ai) para plano + imagem
- Output: Notion + Sheets

## Estrutura
- `src/megazord_workflow.js` — código do node Code do n8n
- `src/prompts/` — system e user message templates
- `scripts/deploy_n8n.sh` — importa workflow via API n8n
