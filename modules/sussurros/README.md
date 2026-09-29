# Sussurros (Entrelinhas)

Analisador de DMs. Baixa conversas do IG, joga no GLM, recebe padrões em JSON.

## Stack
- Source: ManyChat API (free tier, 1000 contatos)
- IA: GLM (z.ai) free tier
- Banco: Supabase tabela leads

## Estrutura
- `src/fetch_dms.py` — pull conversas do ManyChat
- `src/analyze_dm.py` — chamada GLM com prompt estruturado
- `tests/test_prompt.py` — valida saída JSON
