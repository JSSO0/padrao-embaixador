# Overview — Andamento das questões por ano (CACD 2003-2026)

Fonte: `data/processed/questions.parquet` (5.363 registros em 16/10/2026).
Gerado por `scripts/overview.py`.

Legenda: **M** = transcrição manual (JSONL padronizado, prioridade máxima) · **R** = extração automática (rules) · **1aF** = primeira fase (objetiva) · **2aF** = segunda fase (discursivas) · **Gab.** = % de registros com resposta preenchida.

## Visão geral

| Ano | 1ª fase (itens) | 1ª fase (questões) | Cobertura 1ª fase | Origem | 2aF itens | Gab. |
|---|---|---|---|---|---|---|
| 2003 | 117 | 26 | parcial (faixa 1-30, falta 11-14) | M | — | **97%** |
| 2004 | 150 | 150 | completa (1-150) | M | — | **99%** |
| 2005 | 126 | 42 | parcial (1-49, lacunas 9-11, 15-17, 43) | M | - | **86%** |
| 2006 | 112 | 36 | completa (1-36) | M+R | 87 | **80%** |
| 2007 | 125 | 38 | parcial (1-38) | M+R | 15 | **87%** |
| 2008 | 209 | 65 | completa (1-65) | M | 6 | **90%** |
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

## Gabaritos (19/10/2026)

`scripts/extract_gabaritos.py` extrai os gabaritos oficiais dos PDFs (`data/processed/gabaritos.json`) e sobrescreve as respostas das linhas de 1ª fase (manual e rules):
- Formatos suportados: grade estreita "Questão N + 4 letras" (2014-2018, 2024), grade larga cursocacd com mojibake "QUESTǟO" (2019-2023, `#`/X = anulada), pares Item/Gabarito (2024-2026 cebraspe), grade de 30 itens x 30 letras (2004, ☼=anulada), tabela "Questão | item 1..4" (2009-2013, A-D = múltipla escolha) e grade TRANSPOSTA da era TPS (2003-2008: colunas=questões, linhas=itens; pareamento por INTERVALO de coluna x, robusto a células mescladas; os gabaritos vêm dos zips do archive.org já baixados em data/raw/*/archive/).
- Células anuladas (X/#/☼) ficam com `answer` null + nota.
- **Importante**: as respostas resgatadas das regras antigas (2019-2023) estavam rotacionadas em 1 posição dentro da questão — o gabarito oficial corrigiu 564 respostas.
- Cobertura 1ª fase: **4.827/5.024 (96,1%)** — 2003 114/117 · 2004 148/150 · **2005 117/126 · 2006 89/90 · 2007 110/110 · 2008 206/209** · 2009 217/221 · 2010 226/228 · 2011 82/85 · 2012 155/164 · 2013 121/128 · 2014 122/124 · 2015 285/292 · 2016 285/292 · 2017 281/292 · 2018 283/292 · 2019 285/292 · 2020-2021 288/292 · 2022-2023 291/292 · 2024 243/260 · 2025 224/240 · 2026 226/240.
- **2005-2008**: o TPS ERA a prova objetiva da época ("QUESTÕES OBJETIVAS DO TPS (1.ª FASE)") — os gabaritos oficiais dos zips do archive.org foram aplicados. Não preenchidos: itens anulados, os itens de múltipla escolha cuja letra não saiu na extração de texto (PyMuPDF perde glifos dessas fontes quebradas) e as linhas itn=null sem alternatives.
- **Itens de múltipla escolha da era TPS**: armazenados no cache com a chave (qn, 0) e aplicados nas linhas com `itn=null` + `alternatives` preenchido.
- **2004**: 30 questões × 5 itens; o manual tem linhas duplicadas (esquema agrupado qn+itn e linhas achatadas itn=qn) — o apply mapeia item = (qn-1)*5+itn ou item=qn respectivamente.
- **CACD_2003**: as linhas têm `year=2004` no parquet (o TPS de out/2003 era a pré-seleção do concurso 2004); o apply usa o gabarito de 2003 para elas via exceção por contest_id.

## Próximos passos sugeridos (prioridade)

1. **Questões faltantes (13)**: localizadas nos PDFs do archive.org já extraídos em data/raw/*/archive/ (2003: Primeira_Fase_Objetiva .pdf; 2005: CESPE-2005-IRBR-Diplomata.pdf; 2010: IRBR_PARTE_I_2010_CAD_A_manha.pdf). Rascunhos automáticos salvos como questoes_faltantes.md em cada pasta archive — a extração de texto do PyMuPDF perde os glifos dos marcadores de item e parte das letras dessas fontes quebradas, então os rascunhos estão incompletos (2003: 2 de 5 itens por questão; 2005: só o comando) e NÃO foram importados. Fechamento exige OCR da página ou revisão manual.
2. **Completar manuais**: 2014 (falta prova 2, qn 32-73) e 2011 (falta qn 29-65) — PDFs disponíveis; hoje cobertos só por regras (texto dos itens truncado). O gabarito desses anos já está aplicado nas linhas de regras.
3. **2013**: corrigir numeração ruidosa das regras (qn 173-228 são itens, não questões).
4. **2024**: resolver o vínculo de textos-base de algumas questões (question_text de LI com texto de outra disciplina).
5. **2025-2026**: revisar o item 235/2025 (grupo de "completar frase" da CF88: o enunciado do comando ficou no item 234 e o item 236 absorveu a 1ª linha da instrução seguinte).
6. **2003-2010**: pequenas lacunas de itens (2003 11-14; 2005 9-11/15-17/43; 2010 38-39) — transcrever dos PDFs.


## 2ª fase — discursivas (19/10/2026)

`scripts/extract_discursivas.py` extrai as questões discursivas dos PDFs Cebraspe (`prova_discursiva__*.pdf`, texto limpo) e casa com o **padrão de resposta oficial** (`padrao_resposta__*.pdf`) no campo `answer`:
- Cabeçalhos reconhecidos: `-- PROVA ESCRITA DE <DISCIPLINA> --` (com ou sem travessões) e os blocos `QUESTÃO N` (qualquer capitalização).
- **2024-2026: 20 questões por ano, todas com o padrão de resposta** (questões por disciplina: LP, LI, HB, GEO, PI, Economia, Direito, Espanhol/Francês).
- **2017: 20 questões extraídas, 1 com padrão** (apenas 2 arquivos de padrão existem para 2017: Direito Q1 da 3ª fase e Inglês Summary da 2ª) — os demais padrões de 2017 não foram baixados.
- **2018: 0 questões** — os dois PDFs disponíveis (LP e LI) são de redação/exercícios, sem marcadores QUESTÃO N; as demais disciplinas de 2018 não estão no pacote cebraspe (estão na família discursiva_<materia> do repositório secundário).
- **2019-2023 e 2003-2016**: provas discursivas por disciplina baixadas (161 PDFs) mas com encoding quebrado — exigem OCR/tratamento específico.
- Estado no parquet: **193 itens de 2ª fase (60 com padrão de resposta)**. A 3ª fase (226 linhas, 2006-2018) segue como extraída pelas regras antigas.

## Próximos passos (2ª fase)

1. **2017**: os padrões restantes não estão baixados (só 2 arquivos: Direito Q1 e Inglês Summary).
2. **2018**: os PDFs de prova são de redação/exercícios (sem marcadores QUESTÃO N); as 8 disciplinas da 3ª fase têm padrão de resposta baixado mas as questões estão na família discursiva_<materia> (encoding quebrado).
3. **2019-2023**: 3ª fase extraída parcialmente (12+12+16+8 = 48 questões de ~160 possíveis) — as demais linhas foram perdidas pela extração de texto (fonte quebrada) → OCR.
