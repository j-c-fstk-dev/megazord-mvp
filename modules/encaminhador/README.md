# Encaminhador (Máquina de Links)

Redirector rastreável. Cada clique gera click_id único que casa com venda depois.

## Stack
- Local dev: Python + Flask (porta 5000)
- Produção: Cloudflare Worker (latência < 50ms global)

## Estrutura
- `src/redirector.py` — servidor Flask que registra clique e faz redirect
- `src/link_builder.py` — CLI pra gerar novo link rastreavel
- `scripts/deploy_worker.sh` — deploy pro Cloudflare Worker
- `tests/test_redirector.py` — testes básicos

## Próximos passos
Implementar a partir do Cap. 3 do blueprint.
