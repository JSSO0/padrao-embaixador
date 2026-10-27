# CACD Forecast AI — Contexto da conversa (27/10/2026)

> Projeto: pesquisa experimental que mede, com backtesting temporal, se o histórico das provas do CACD (2003-2026) permite estimar a distribuição temática da próxima edição. Não prevê a questão literal.

## Estado final consolidado (27/10/2026)

| Bloco | Situação |
|---|---|
| Parquet | `data/processed/questions.parquet` — **5.038 itens 1ª fase** + 189 2ª fase + 315 3ª fase |
| 1ª fase | 2003-2026 (23 edições), transcrição 100% (incluindo q38-39/2010 via OCR) |
| Gabarito 1ª fase | **96,4%** (4.858/5.038) — ausências = anulados + itens não extraídos |
| Disciplinas | Canonizadas em 8 grupos (4.951/5.038 = 98,6%) |
| Taxonomia | 45 temas (`topic` column) — 22% em "geral" |
| Backtesting | 9 folds, 5 métodos — TF-IDF 0.90, Markov 0.79 |
| Discursivas | 2ª fase 189 itens (61 com padrão), 3ª fase 315 linhas |
| Commits | `39f5787` (27/10) e anteriores — tudo em `origin/main` |

## Arquivos

- `01-sessoes-e-decisoes.md` — cronologia das sessões, bugs e decisões
- `02-estado-atual-e-lacunas.md` — números por ano, o que falta e as pendências
- `03-pipeline-e-comandos.md` — scripts de produção, ordem de execução e armadilhas

## Pendências priorizadas

1. **Taxonomia refinada**: reduzir o tema "geral" (22% dos itens) — adicionar subtemas e keywords
2. **TF-IDF refinado**: rodar o backtest com a taxonomia refinada para melhorar o Precision@K
3. **2013**: 10 linhas de rules com numeração ruidosa (qn 174-227) — removidas em 22/10
4. **2024**: vínculo de textos-base de algumas questões (LI com passagem de outra disciplina)
5. **2025**: item 235 (grupo "completar frase" da CF88 — enunciado no 234, item 236 absorveu instrução)
6. **2011/2014**: completar manuais (regras hoje, texto truncado)
7. **Discursivas 2003-2016**: 161 PDFs por disciplina baixados, muitos com encoding quebrado → OCR
8. **Padrões de resposta 2003-2016**: não baixados

## Commits principais

| Commit | Data | O que fez |
|---|---|---|
| `49c8d05` | 06/10 | Corpus completo v0.1 (463 arquivos, 23 edições 2003-2026) |
| `5c66f6b` 2026-10-06 | Parsers por família funcionando (1703 questões) |
| `e6fef12` 2026-10-07 | questions.parquet regenerado (validação 2026: 239 itens, 100% gabarito) |
| `c9f52d0` 2026-10-07 | Parsers IADES 2019-2023 (+691 itens) |
| `3dd8214` 2026-10-19 | Completa gabaritos e extrai discursivas 2a/3a fase |
| `6664abf` 2026-10-20 | Gabarito 95,9% da 1a fase (MC 2009-2013) e limpeza 2013 |
| `ca8a61b` 2026-10-21 | Transcreve 12 das 13 questões faltantes da 1a fase (2003 e 2005) |
| `d529ddc` 2026-10-23 | Discursivas 2013-2016 extraídas (196 registros 3a fase) |
| `3fc089c` 2026-10-23 | Fase 3 — provas escritas por disciplina extraídas dos zips 2003-2012 |
| `a183e63` 2026-10-23 | OCR da 3a fase 2009 em progresso — filtro de rascunho corrigido |
| `020c44a` 2026-10-27 | 2010 q38-39 transcritas via OCR do PARTE_I |
| `39f5787` 2026-10-27 | Etapa 6 — 50 questões aleatórias para validação manual |
| `484da74` 2026-10-24 | Backtesting temporal — 9 folds, 4 baselines, 5 métricas |
| `ee57de8` 2026-10-24 | Baseline TF-IDF — 0.90 Precision@K |
| `4c08a08` 2026-10-24 | Backtesting temático — Precision@K por tema (0.82) |
| `5ed9099` 2026-10-26 | Taxonomia refinada — 45+ temas |
| `da4eaaa` 2026-10-26 | Backtest temático refinado — TF-IDF 0.90 |
| `bfe0cf6` 2026-10-27 | Restaura gabaritos após re-import (96,4% 1aF) |
