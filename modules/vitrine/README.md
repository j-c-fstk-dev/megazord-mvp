# Vitrine (Linda Visão)

Painel de vendas. Responde: de onde veio, qual produto saiu, o que comprou junto.

## Stack
- Banco: Google Sheets (até ~1000 vendas/mês)
- Frontend: Looker Studio (free)
- Pipeline: n8n webhook Hotmart -> append Sheets

## Estrutura
- `scripts/setup_sheets.py` — cria abas e cabeçalhos na planilha
- `tests/test_attribution.py` — valida casamento click_id -> venda
