# Prompts GLM reusáveis

Cada prompt fica em arquivo `.txt` separado:
- `entrelinhas_system.txt` — prompt system do Sussurros
- `entrelinhas_user_template.txt` — template user message
- `megazord_system.txt` — prompt system do Sintetizador
- `megazord_user_template.txt` — template user message
- `story_classify_system.txt` — classificação assistida
- `vendas_insights_system.txt` — insights Linda Visão

Formato: primeira linha = `system` ou `user_template`.
Restante do arquivo = conteúdo do prompt.
