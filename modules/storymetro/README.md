# Storymetro (StoryRocks)

Medidor de stories. Mostra qual tipo gera comentário vs qual tipo gera venda.

## Stack
- Coleta: Python script via Meta Graph API
- Banco: Google Sheets
- Frontend: Looker Studio

## Estrutura
- `src/fetch_stories.py` — pull diário das métricas
- `src/classify_stories.py` — classificação manual assistida
- `tests/test_fetch.py`
