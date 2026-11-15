# felipeganho.github.io

Site-currículo de uma página do Felipe Silva Ganho, publicado no GitHub Pages: https://felipeganho.github.io/

## Como atualizar
1. Edite o arquivo da seção em `data/`:
   - `perfil.json`: nome, cargo, local, links e resumo do topo
   - `experiencia.json`, `projetos.json`, `competencias.json`, `formacao.json`, `certificacoes.json`, `idiomas.json`
2. Rode `python build.py` (só biblioteca padrão). Ele gera o `index.html` a partir de `modelo.html`.
3. Faça commit de `data/` e `index.html` juntos.

## Decisões
- **HTML estático gerado no build:** a página funciona sem JavaScript e os buscadores leem tudo.
- **Dados separados da página:** um JSON por seção, a mesma fonte do currículo em PDF.
- **Sem telefone, e-mail ou data de nascimento expostos:** o contato é pelo LinkedIn.
- **Sem rastreadores** (Analytics, GTM).
- Tema claro e escuro automáticos (`prefers-color-scheme`).
