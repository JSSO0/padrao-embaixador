# Relatório de Saúde do Corpus — Etapas 3 e 4

Data: 2026-10-06 · Tags: `v0.1-corpus`

## Números gerais

| Métrica | Valor |
|---|---|
| Downloads | **463/463 (100%), 0 falhas** (10 ZIPs do Archive.org + 453 PDFs) |
| Tamanho do corpus bruto | 386,6 MB (`data/raw/`) |
| Textos extraídos | 453 arquivos → `data/processed/text/` |
| Falhas de extração | 0 |
| PDFs escaneados (`needs_ocr`) | 8 |
| Texto total | ~22,3 milhões de caracteres |

## Cobertura por edição (texto extraído)

| Edição | Arquivos | Chars | Questões detectadas* | Observação |
|---|---|---|---|---|
| 2003 | 11 | 400k | 37 | ⚠️ baixa detecção — formato antigo, marcadores diferentes |
| 2004 | 10 | 368k | 5 | ⚠️ idem |
| 2005 | 13 | 445k | 85 | 7 discursivas escaneadas (needs_ocr) |
| 2006 | 12 | 447k | 32 | ⚠️ baixa detecção |
| 2007 | 12 | 444k | 88 | |
| 2008 | 12 | 383k | 102 | |
| 2009 | 12 | 438k | 113 | |
| 2010 | 13 | 437k | 107 | |
| 2011 | 13 | 366k | 94 | |
| 2012 | 13 | 407k | 117 | |
| 2013 | 26 | 892k | 174 | inclui espelho Wayback |
| 2014 | 24 | 927k | 478 | contagem inflada por espelhos duplicados |
| 2015 | 28 | 1.100k | 574 | idem |
| 2016 | 23 | 921k | 490 | idem |
| 2017 | 30 | 1.259k | 414 | inclui 48 padrões por questão |
| 2018 | 36 | 1.656k | 434 | |
| 2019 | 15 | 1.211k | 176 | banca IADES |
| 2020/21 | 13 | 1.299k | 178 | banca IADES |
| 2022 | 15 | 1.629k | 217 | banca IADES |
| 2023 | 14 | 1.630k | 175 | banca IADES |
| 2024 | 36 | 1.944k | 326 | |
| 2025 | 36 | 1.681k | 72 | ⚠️ investigar marcadores no caderno Cebraspe |
| 2026 | 36 | 988k | 64 | ⚠️ idem |

\* "Questões detectadas" = contagem bruta de marcadores `QUESTÃO N` em todos os arquivos da edição, **sem deduplicação** (espelhos oficial+secundário contam em dobro). É um proxy de sanidade da extração, não o nº oficial de questões.

## Casos `needs_ocr` (8)

- 7 discursivas da edição 2005 (fonte cursocacd) — PDFs escaneados sem camada de texto
- 1 prova objetiva 2019 tarde (fonte Clipping) — espelho alternativo da mesma prova existe extraível via cursocacd/gabarite

**Decisão:** não bloquear o pipeline; na Etapa 5, essas 8 provas só entram se forem re-obtidas de fonte com texto ou se rodarmos OCR (tesseract). Anotado como pendência.

## QA pendente para a Etapa 5 (segmentação)

1. **2003, 2004 e 2006**: marcadores de questão no formato antigo não casaram com o regex `QUESTÃO N` — inspecionar os TXTs dessas edições e adaptar as heurísticas (possivelmente "QUESTÃO" sem numeração separada, ou itens por bloco de disciplina)
2. **2025 e 2026 (Cebraspe)**: chars elevados mas poucas questões detectadas — provável uso de espaço não-separável ou formatação diferente nos cadernos recentes; verificar
3. **Deduplicação**: 2013–2017 têm o mesmo documento em 2+ fontes (oficial + secundária) — na montagem do dataset, priorizar oficial (regra §3 da spec) e usar a secundária como backup de comparação
4. **10 ZIPs do Archive.org** (2003–2012) baixados mas não extraídos — na Etapa 5, descompactar e comparar com os PDFs do cursocacd para validar fidelidade

## Próximo passo

Etapa 2 (registro administrativo por edital) e Etapa 5 (segmentação de questões → `questions.parquet`), conforme `docs/plano-mestre.md`.
