---
description: "Task list — Tasks abertas do padrao-embaixador (consolidação 2026-10-26)"
---

# Tasks: Tasks Abertas — consolidação de pendências (001)

**Input**: consolidação das pendências documentadas no vault (`projetos\pessoais\padrao-embaixador — Tasks Abertas.md`), no backlog acordado (16–23/10/2026) e nas specs de requisitos.
**Natureza**: spec de consolidação (backlog priorizado) — não cria features novas.

Legenda: `[P]` paralelizável · status: 🔨 iniciada · ⬜ planejada (não iniciada)

## Phase 1: Em andamento (iniciadas)

- [ ] T001 🔨 Commitar o reparo de 23/10 (default de anos + fallback itn=1 formato C) — implementado, ainda não commitado
- [ ] T002 🔨 Correção definitiva do default de anos em `extract_gabaritos.py`: trocar `years = args.year or range(2015, 2027)` pelo loop 2003–2026 (causa do apagamento de respostas em 23/10)

**Checkpoint**: pipeline protegido contra apagamento de respostas por default.

## Phase 2: Dados — priorizadas (planejadas)

- [ ] T010 ⬜ **1. OCR das fontes 2003–2010** (encoding quebrado / PyMuPDF perde glifos) — fecha ~19 respostas de gabarito + 13 questões de transcrição + itens de múltipla escolha
- [ ] T011 ⬜ **2.** Re-transcrição do pacote **2004** (manual com linhas duplicadas itn=qn)
- [ ] T012 ⬜ **3. 2013**: 10 linhas de rules com numeração ruidosa (qn 174–227)
- [ ] T013 ⬜ **4. 2024**: vínculo de textos-base de algumas questões (LI com passagem de outra disciplina)
- [ ] T014 ⬜ **5. 2011/2014**: completar manuais (regras hoje, texto truncado)
- [ ] T015 ⬜ **6. 2ª fase**: padrões de 2017 faltantes (só 2 baixados), 2018 (formato redação), 2019–2023 parcialmente extraído (OCR)

**Checkpoint**: dataset completo para as edições 2003–2024 (1ª fase) e 2ª fase extraída.

## Phase 3: Plano mestre — etapas 2 e 6–11 (planejadas)

- [ ] T020 ⬜ **Etapa 2**: `data/metadata/contest_registry.csv` (dados administrativos por edição, `exam_regime` A–E)
- [ ] T021 ⬜ **Etapa 6**: validação manual de amostra (5–10%, fidelidade ≥97%)
- [ ] T022 ⬜ **Etapa 7**: taxonomia temática (`taxonomy.md` + `topics.parquet`) com anti-leakage por fold
- [ ] T023 ⬜ **Etapa 8**: NLP — embeddings (multilingual-e5-large primário), similaridade, clustering
- [ ] T024 ⬜ **Etapa 9**: features estatísticas + 4 baselines em `models/baseline/`
- [ ] T025 ⬜ **Etapa 10**: ML (XGBoost principal) + Laya (calibração obrigatória) + LLM complementar
- [ ] T026 ⬜ **Etapa 11**: backtesting com folds 2017→2025 respeitando regimes de banca (Precision@K, 9 folds)

**Checkpoint**: backtesting (item 7 do backlog) implementado — hoje nada foi implementado ainda.

## Phase 4: Critérios de aceitação das specs (planejadas)

- [ ] T030 ⬜ ≥95% cobertura de extração e de gabarito por edição
- [ ] T031 ⬜ Dedup de espelhos por prioridade de fonte (`duplicate_of` registrado)
- [ ] T032 ⬜ Amostra de 5% revisada manualmente com fidelidade ≥97%
- [ ] T033 ⬜ Testes pytest com fixtures de texto real de cada família

## Phase 5: Conteúdo (planejadas)

- [ ] T040 ⬜ Posts do plano de 31 dias: dia 19 depende do backtest; post de resultado só depois dos 9 folds rodarem

**Checkpoint final**: 9 folds rodados; métricas publicadas com a frase do que não provam.
