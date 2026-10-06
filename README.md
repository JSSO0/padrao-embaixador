# CACD Forecast AI

> **Handoff:** o documento de referência para qualquer pessoa/modelo que assumir o projeto é [`docs/plano-mestre.md`](docs/plano-mestre.md) — contexto, decisões, schemas, protocolo de backtesting e checklist imediato. Os **requisitos originais** (fonte da verdade) estão em [`docs/spec-requisitos.md`](docs/spec-requisitos.md).

Sistema experimental de previsão de temas, subtemas e formatos de questão do **Concurso de Admissão à Carreira de Diplomata (CACD)** — Terceiro-Secretário — baseado em ~24 edições de histórico (2003–2026).

> **O objetivo NÃO é prever a próxima questão literal.** O objetivo científico é medir, com backtesting temporal rigoroso, até que ponto o histórico das provas permite prever a distribuição temática da próxima edição — e comparar baselines estatísticos, ML tabular, NLP (embeddings) e modelos de decisão probabilística (Laya).

## Estrutura do repositório

```
├── data/
│   ├── metadata/        # catalogos de fontes e proveniencia (versionado)
│   ├── raw/             # PDFs baixados por edicao e familia de fonte (versionado)
│   ├── processed/       # texto extraido, datasets, metricas (versionado)
│   └── embeddings/      # vetores de questoes (versionado)
├── scraper/             # Etapa 3: download dos PDFs catalogados
├── parser/              # Etapa 4: extracao de texto e segmentacao de questoes
├── nlp/                 # Etapa 5: embeddings, similaridade, clustering
├── features/            # Etapa 6: features estatisticas por tema
├── models/              # baselines, xgboost, laya, ensemble
├── evaluation/          # metricas @K, backtesting temporal
├── notebooks/           # analises exploratorias
├── api/                 # FastAPI (futuro)
├── frontend/            # dashboard (futuro)
├── tests/               # pytest
└── docs/                # relatorios e planejamento
```

## Pipeline (etapas)

| Etapa | Status | Artefato |
|---|---|---|
| 1. Catalogar fontes | ✅ | `docs/etapa1-relatorio-catalogacao.md` |
| 2. Dados administrativos por edital | ⏳ | `data/metadata/contest_registry.csv` |
| 3. Baixar PDFs | 🔄 | `scraper/download.py` + `data/raw/download_manifest.csv` |
| 4. Extrair texto | ✅ script pronto | `parser/extract_text.py` → `data/processed/text/` |
| 5. Segmentar questões + dataset | ⏳ | `parser/` |
| 6. Validação manual de amostra | ⏳ | — |
| 7. Taxonomia temática | ⏳ | `data/metadata/taxonomy.md` |
| 8. Embeddings + clustering | ⏳ | `nlp/` |
| 9. Features estatísticas + baselines | ⏳ | `features/`, `models/baseline/` |
| 10. ML + backtesting temporal | ⏳ | `models/`, `evaluation/` |

## Fontes e confiabilidade

Prioridade: MRE/IrBr > Cebraspe > Wayback (oficial arquivado) > repositórios secundários.

- **Oficial vivo:** 2017–2018, 2024–2026 (Cebraspe; scraper consome a API `apis.cebraspe.org.br`)
- **Oficial arquivado:** 2013–2016 (Wayback, domínio legado `cespe.unb.br`)
- **Secundária:** 2003–2012 e 2019–2023 (banca **IADES** nestes; Archive.org, Curso CACD, Qconcursos, PCI, Gabarite, Nabuco)
- Cada linha do dataset final carrega `source_type` e `source_url` — nada foi registrado sem verificação por fetch; ausências são `NOT_FOUND` explícitos

Regimes de prova relevantes (`exam_regime`): 2003–2005 (1 objetiva) · 2006–2018 (2 objetivas + fases separadas, CESPE) · 2010–2011 (1ª fase = Bolsa-prêmio) · 2019–2023 (banca IADES, certo/errado) · 2024–2026 (formato atual, Cebraspe).

## Reproduzir a coleta

```bash
pip install -r requirements.txt
python scraper/download.py --dry-run   # lista os jobs
python scraper/download.py             # baixa (retomável, com SHA-256)
python parser/extract_text.py          # extrai texto + métricas de qualidade
```

O manifest `data/raw/download_manifest.csv` permite retomar execução interrompida e auditar proveniência (URL → arquivo → checksum).

## Princípios do projeto

- **Backtesting temporal obrigatório** — janela expansiva (treino 2006–X, teste X+1); nunca split aleatório
- **Anti-leakage** — taxonomia, TF-IDF e embeddings re-fitados por fold; eventos contemporâneos filtrados por data < prova
- **Métricas de ranking** — Precision@K, Recall@K, F1@K, MAP@K, NDCG@K (por disciplina também), não só accuracy
- **Baselines antes de IA** — frequência histórica, frequência recente, recência e combinação estatística como piso de comparação
- **Transparência** — todo score reportado como probabilidade estimada, nunca como certeza; conteúdo gerado por LLM sempre marcado `GERADA POR IA`
- **Regras de fonte** — URL só registrada depois de verificada; `NOT_FOUND` quando não existe; provas de cursinho nunca tratadas como oficiais

## Ferramentas principais

Python 3.12+ · requests · PyMuPDF · pandas/DuckDB/PyArrow · pandera · sentence-transformers (multilingual-e5-large) · scikit-learn · XGBoost/LightGBM · Optuna · MLflow · Laya (checkpoint multilingual) · FastAPI + PostgreSQL + Next.js (dashboard futuro)

Detalhes e justificativas: `docs/planejamento-ferramentas.md`
