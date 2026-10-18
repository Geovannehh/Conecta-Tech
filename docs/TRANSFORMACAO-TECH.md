# Conecta Campus Tech

Transformação da página pública para orientação de carreiras em tecnologia. Preserva Flask, SQLite, endpoints existentes e o painel administrativo. O painel conserva os dados antigos de acolhimento; não mede as novas jornadas locais.

## Executar

Na pasta do projeto, use o Python do ambiente virtual: `.venv\Scripts\python.exe flask_app.py`. Abra `http://127.0.0.1:5000`. Instale `requirements.txt` em um ambiente Python válido se o ambiente virtual tiver sido movido de outra máquina.

## Recursos

- Catálogo de 23 áreas, cargos, tecnologias e práticas, com busca sem distinção de acentos e filtros por grupo.
- 6 missões por área, incluindo projeto final, com desbloqueio sequencial, XP e conquistas calculados a partir das conclusões.
- Desfazer uma etapa reabre as etapas seguintes daquela trilha.
- Progresso local com exportação e importação JSON. Não há conta, validação de entregas ou sincronização na nuvem.
- Radar salarial brasileiro, com busca, senioridade, percentis, data e links diretos às fontes.
- Layout responsivo, controles rotulados, navegação por teclado e avisos acessíveis.

## Conteúdo e limites

`static/tech-data.json` concentra o catálogo e os salários. `build_data.js`, entregue em `docs/tech-source/`, gera os dados e pode ser editado para expansão. O setor não tem uma relação finita de todas as stacks e cargos: esta é uma cobertura editorial ampla, não uma promessa de exaustividade.

Pesquisa consultada em 16/10/2026:

- https://roadmap.sh/ — referência de organização por carreiras e habilidades, sem copiar sua identidade.
- https://www.roberthalf.com/br/pt/vagas-detalhes/desenvolvedora-back-end-pleno — 17 combinações de cargos e níveis, tabela principal e relacionados.
- https://www.roberthalf.com/br/pt/insights/salary-guide — contexto e metodologia de projeções baseadas em contratações intermediadas pela consultoria.

Valores nacionais mensais em BRL, P25/P50/P75. P50 é percentil, não média. São salários de entrada na contratação; não representam salário líquido, remuneração total ou equivalência PJ. Não há ajuste regional ou atualização automática. Dados não disponíveis não foram inventados.

## Arquivos da transformação

`templates/index.html`, `static/css/tech.css`, `static/js/tech.js`, `static/tech-data.json` e este documento. Os CSS e JS anteriores são preservados para compatibilidade com as telas administrativas.

Fontes web são opcionais: a interface usa fontes do sistema quando não há conexão com Google Fonts. Recursos de estudo podem estar em inglês.
