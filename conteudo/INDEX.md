# INDEX — Conteúdo do plano de 31 dias (CACD Forecast AI)

Posts gerados a partir do estado real do repo em 22/10/2026
(commits 3dd8214 / 0666266; 5.487 registros no questions.parquet).

| Dia | Data | Slug | Território | CTA | Status |
|---|---|---|---|---|---|
| 19 | 2026-11-09 | [backtesting-precision-k](2026-11-09-backtesting-precision-k.md) | LinkedIn + X + IG | ler o repo | depende de mudança (post "como vou medir") |
| 30 | 2026-11-20 | [pesquisa-reprodutivel-manifesto](2026-11-20-pesquisa-reprodutivel-manifesto.md) | LinkedIn + X + IG | "Clone e confira" | pronto (com pré-requisito) |

## Fatos-chave usados (todos verificados em 22/10/2026)

| Número | Fonte |
|---|---|
| 5.487 registros / 5.020 itens 1ª fase | `data/processed/questions.parquet` |
| 4.677 itens com gabarito (93,2%) | saída de verificação da cadeia `extract_gabaritos.py` |
| 460 PDFs no repo | contagem recursiva de `*.pdf` |
| 463 entradas com SHA-256 | `data/raw/download_manifest.csv` |
| 9 folds (X = 2017 a 2025) / 4 baselines | `docs/plano-mestre.md` §1 |

## Pendências que bloqueiam posts de resultado

1. Taxonomia temática dos itens — não existe em `data/metadata/`.
2. Módulo `evaluation/` (Precision@K, 9 folds) — diretório vazio.
3. 4 baselines estatísticos — não implementados.
4. Testes mínimos — `tests/` vazio (0 testes).
5. OCR das fontes 2003-2010 (gabaritos faltantes + 13 questões de transcrição).

## Regra ativa em todos os posts

Toda métrica vem acompanhada de uma frase explícita do que ela **não** prova.
Post de resultado só após os 9 folds rodarem de verdade.
