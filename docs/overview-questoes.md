# Overview — Andamento das questões por ano (CACD 2003-2026)

Fonte: `data/processed/questions.parquet` (5.363 registros em 16/10/2026).
Gerado por `scripts/overview.py`.

Legenda: **M** = transcrição manual (JSONL padronizado, prioridade máxima) · **R** = extração automática (rules) · **1aF** = primeira fase (objetiva) · **2aF** = segunda fase (discursivas) · **Gab.** = % de registros com resposta preenchida.

## Visão geral

| Ano | 1ª fase (itens) | 1ª fase (questões) | Cobertura 1ª fase | Origem | 2aF itens | Gab. |
|---|---|---|---|---|---|---|
| 2003 | 117 | 26 | parcial (faixa 1-30, falta 11-14) | M | — | 0% |
| 2004 | 150 | 150 | completa (1-150) | M | — | 0% |
| 2005 | 126 | 42 | parcial (1-49, lacunas 9-11, 15-17, 43) | M | — | 0% |
| 2006 | 112 | 36 | completa (1-36) | M+R | 87 | 0% |
| 2007 | 125 | 38 | parcial (1-38) | M+R | 15 | 0% |
| 2008 | 209 | 65 | completa (1-65) | M | 6 | 0% |
| 2009 | 221 | **80** | completa (1-80) | M | 11 | **94%** |
| 2010 | 228 | 78 | quase completa (falta 38-39) | M | 10 | **95%** |
| 2011 | 122 | 65 | completa (1-65) | M(1-28)+R(29-65) | 8 | **92%** |
| 2012 | 164 | 65 | completa (1-65) | M | 8 | **90%** |
| 2013 | 161 | 65-73 | completa (1-73*, ver nota) | M(1-65)+R(66-73) | 4 | **84%** |
| 2014 | 166 | 73 | completa (1-73) | M(1-31)+R(32-73) | 52 | **78%** |
| 2015 | 293 | **73** | completa | **M** | 71 | 83% |
| 2016 | 292 | **73** | completa | **M** | 54 | 85% |
| 2017 | 298 | **73** | completa | **M** | 9 | 95% |
| 2018 | 292 | **73** | completa | **M** | 4 | 99% |
| 2019 | 292 | **73** | completa | **M** | — | **98%** |
| 2020-2021 | 292 | **73** | completa | **M** | — | **99%** |
| 2022 | 294 | **73** | completa | **M** | — | **99%** |
| 2023 | 295 | **73** | completa | **M** | — | **99%** |
| 2024 | 272 | 65 | completa (1-65) | **M** (Cebraspe) | — | **92%** |
| 2025 | 257 | itens 1-240 (nº contínuo) | **completa** (240 itens manuais) | **M** (Cebraspe) | — | **100%** |
| 2026 | 246 | itens 1-240 (nº contínuo) | **completa** (240 itens manuais) | **M** (Cebraspe) | — | **100%** |

\* 2013: o manual cobre 1-65; as regras completam 66, 67, 68, 70 e 73 (66-73 têm numeração ruidosa nas regras, ex. 173-228 = itens contados como questões — limpar).

Os % de gabarito consideram todas as linhas do ano (incl. 2ª fase); na 1ª fase manual a cobertura real é: 2015 285/292, 2016-2018 292/292, 2019 285/292, 2020-2021 288/292, 2022-2023 291/292 — as ausências são itens anulados no gabarito definitivo (X). Em 2024 faltam os itens das questões 1-5 (20 itens) e sobram ~16 respostas de uma leitura antiga a revalidar; 2025/2026 têm 240/240.

## Situação por bloco de tempo

### 2003-2007 — primeira geração (manual já padronizado)
- Transcrições manuais são a fonte principal; formatos variados de prova (2004 tinha 150 questões).
- 2aF quase inexistente no dataset (2006: 32q; 2007: 5q).
- Gabarito não preenchido.

### 2008-2014 — manuais parciais + regras complementares
- 2008-2010: 1aF completa via manual (80/78/65 questões).
- 2011: manual cobre 1-28, regras completam 29-65.
- 2013-2014: regras wayback incompletas/ruidosas; 2014 tem 2aF razoável (52 itens).### 2015-2018 — ⭐ bloco de referência
- **100% da 1a fase por transcrição manual** (73 questões × 4 itens, question_text + item_text completos).
- 2aF incompleta (4-71 itens conforme o ano).

### 2019-2023 — ⭐ bloco de referência (padrão Cespe/IADES novo)
- **100% da 1a fase por transcrição manual** (73 questões × 4 itens, com `question_text` + `item_text` completos).
- Gabaritos resgatados das regras antigas: 68-76% dos itens (o restante = as questões que o qconcursos não extraía; completar com os PDFs de gabarito de cursocacd).
- Cabeçalhos "Itens de N a M", "Área Livre/Espaço livre" e rodapés já filtrados pelo extrator.

### 2019-2023 (bloco anterior de extração automática — substituído)

### 2024-2026 — Cebraspe oficial (formato novo)

- **2024: 1aF completa via manual** (65 questões × 4 itens = 260 itens).
- **2025-2026: 1aF COMPLETA via manual** (240 itens por ano, numerados continuamente, sem "Questão N") — extraídos por `scripts/extract_cebraspe_linear.py`, que parseia o texto linear dos PDFs oficiais (a ordem nativa dos PDFs Cebraspe é a ordem de leitura): cada item = "<num> <comando>"; os textos-base/citações/instruções acumulam em buffer e vinculam ao 1º item de cada bloco.
- Gabaritos 2025/2026: 240/240 itens (formato "Item/Gabarito" dos PDFs cebraspe + cursocacd).
- Seções por disciplina em maiúsculas, capa, cabeçalhos de página e rodapés filtrados.

## Gabaritos (16/10/2026)

`scripts/extract_gabaritos.py` extrai os gabaritos oficiais dos PDFs (`data/processed/gabaritos.json`) e sobrescreve as respostas das linhas de 1ª fase (manual e rules):
- Cinco formatos suportados: grade estreita "Questão N + 4 letras" (2014-2018, 2024), grade larga cursocacd com mojibake "QUESTǟO" (2019-2023, `#`/X = anulada), pares Item/Gabarito (2024-2026 cebraspe), grade de 30 itens x 30 letras (2004, ☼=anulada) e tabela "Questão | item 1..4" (2009-2013, com A-D = múltipla escolha).
- Células anuladas (X/#/☼) ficam com `answer` null + nota.
- **Importante**: as respostas resgatadas das regras antigas (2019-2023) estavam rotacionadas em 1 posição dentro da questão — o gabarito oficial corrigiu 564 respostas.
- Cobertura 1ª fase (ausências = itens anulados): 2009 217/221 · 2010 226/228 · 2011 82/85 · 2012 155/164 · 2013 121/128 · 2014 122/124 · 2015 285/292 · 2016 285/292 · 2017 281/292 · 2018 283/292 · 2019 285/292 · 2020-2021 288/292 · 2022-2023 291/292 · 2024 243/260 · 2025 224/240 · 2026 226/240.
- **2005-2008**: os gabaritos disponíveis são do TPS (pré-seleção, grade transposta linha=item × coluna=questão) — não correspondem à prova objetiva do dataset; o parser os ignora (`re.search(r"\bTPS\b|PRÉ-SELEÇÃO")` + rejeição de linhas com >6 letras).
- **2004**: gabarito extraído (150 itens) mas NÃO aplicado — o manual de 2004 tem estrutura quebrada (qn duplicados, dois esquemas de itn); as 27 respostas aplicadas por engano foram desfeitas (`scripts/fix_2004.py`).
- **2003**: o gabarito disponível não casou com nenhum formato conhecido (a investigar).

## Próximos passos sugeridos (prioridade)

1. **2004**: o manual tem estrutura quebrada (qn duplicados: q1-24 com itn 1-5 e q4-150 com itn=qn) — re-transcrever do PDF (`prova 2004.json`) e então aplicar o gabarito já extraído (150 itens em `gabaritos.json`).
2. **2003**: o gabarito disponível (`cursocacd/gabarito__326d9ed0.pdf`) não casou com nenhum formato — investigar o layout.
3. **2005-2008**: sem gabarito de prova objetiva disponível (só o do TPS) — baixar o gabarito correto de wayback/qconcursos.
4. **Completar manuais**: 2014 (falta prova 2, qn 32-73) e 2011 (falta qn 29-65) — PDFs disponíveis; hoje cobertos só por regras (texto dos itens truncado). O gabarito desses anos já está aplicado nas linhas de regras.
5. **2013**: corrigir numeração ruidosa das regras (qn 173-228 são itens, não questões).
6. **2024**: resolver o vínculo de textos-base de algumas questões (question_text de LI com texto de outra disciplina).
7. **2025-2026**: revisar o item 235/2025 (grupo de "completar frase" da CF88: o enunciado do comando ficou no item 234 e o item 236 absorveu a 1ª linha da instrução seguinte).
8. **2003-2010**: pequenas lacunas de itens (2003 11-14; 2005 9-11/15-17/43; 2010 38-39) — transcrever dos PDFs.
9. **2ª fase (discursivas)**: cobertura ainda irregular (4-87 itens/ano) — extrair das PDFs de discursiva.
