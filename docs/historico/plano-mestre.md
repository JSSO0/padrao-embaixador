# CACD Forecast AI — Plano Mestre (handoff)

> **Documento de transferência.** Escrito para permitir que qualquer pessoa (ou modelo de IA) assuma o projeto a partir daqui. Complementa a especificação original de requisitos (`docs/spec-requisitos.md`) — aquele define **o quê e por quê**; este define **como e em que ordem**, com o estado atual.
>
> Snapshot: 2026-10-06 · Repositório: `padrao-embaixador/` (branch `main`)

---

## 1. Contexto e objetivo

Analisar o histórico das provas do CACD (Terceiro-Secretário), ~24 edições (2003–2026), e medir empiricamente se é possível prever a **distribuição temática** da próxima prova.

**NÃO é objetivo** prever a questão literal. É um estudo científico: backtesting temporal, comparação de métodos, métricas de ranking, transparência. Todo output é "probabilidade estimada", nunca certeza.

Pergunta central: *"Dado todo o histórico disponível até o ano X, quais temas teriam sido previstos para X+1 — e o que realmente caiu?"*

### Requisitos invioláveis (de qualquer etapa que vier)

1. **Backtesting temporal obrigatório**: janela expansiva — treino 2006–X, teste X+1, X de 2017 a 2025. Nunca split aleatório.
2. **Anti-leakage**: taxonomia, TF-IDF, embeddings e classificação temática **re-fitados dentro de cada fold** usando apenas provas ≤ X. Eventos contemporâneos (se usados) filtrados por data < prova. Documentar todo risco de leakage encontrado.
3. **Proveniência total**: cada questão no dataset carrega `source_type` e `source_url`. Nunca registrar URL não verificada. Ausência = `NOT_FOUND` explícito.
4. **Baselines antes de IA**: nenhum modelo "inteligente" vale nada sem comparar com os 4 baselines estatísticos.
5. **Marcas**: saída de LLM sempre rotulada `GERADA POR IA`; relatórios usam linguagem de score/probabilidade, nunca certeza.

---

## 2. Estado atual (o que já existe no repo)

| Item | Local | Status |
|---|---|---|
| Catálogo de fontes oficiais (granular, URLs verificadas) | `data/metadata/source_catalog.csv` | ✅ |
| Catálogo Wayback (oficial arquivado 2013–2018) | `data/metadata/wayback_archive.csv` | ✅ |
| Fontes secundárias (Archive.org, PCI, Qconcursos, Gabarite, Clipping) | `data/metadata/secondary_sources.csv` | ✅ |
| Curso CACD completo (279 PDFs por tipo/disciplina, 2003–2026) | `data/metadata/curso_cacd_full.csv` | ✅ |
| Pacotes por edição (SharePoint Nabuco, 2003–2026) | `data/metadata/nabuco_sharepoint.csv` | ✅ |
| Relatório da catalogação + matriz de cobertura | `docs/etapa1-relatorio-catalogacao.md` | ✅ |
| Planejamento de ferramentas com justificativas | `docs/planejamento-ferramentas.md` | ✅ |
| Downloader retomável com SHA-256 | `scraper/download.py` → `data/raw/download_manifest.csv` | 🔄 rodando |
| Extrator de texto + métricas de qualidade | `parser/extract_text.py` → `data/processed/text_metrics.csv` | ✅ script pronto |

**Cobertura de fontes (nada ficou sem fonte):**
- Oficial viva: 2017–2018, 2024–2026 (Cebraspe)
- Oficial arquivada: 2013–2016 (Wayback, domínio legado `cespe.unb.br`)
- Secundária: 2003–2012 e 2019–2023 (banca IADES nestes 4 anos!)

**Fatos estruturais descobertos (afetam o modelo):**
- Banca: CESPE (2003–2018, 2024–2026) vs. **IADES (2019–2023)** — quebra de comparabilidade
- 2010–2011: 1ª fase = prova da Bolsa-prêmio de Vocação para a Diplomacia
- CACD 2007 existiu (ausente apenas do site do MRE)
- Padrões de resposta oficiais por questão só existem desde 2017
- Gabaritos preliminares sobreviveram apenas para 2018 (no vivo) e 2013/2016/2017/2018 (na Wayback)

---

## 3. Plano por etapas (o que fazer daqui para frente)

### ETAPA 2 — Dados administrativos por edição ⏳
- **Input:** editais PDF já baixados (`data/raw/*/cebraspe/edital*`, `data/raw/*/mre/`)
- **Output:** `data/metadata/contest_registry.csv` — colunas: `contest_id`, `ano_aplicacao`, `banca` (CESPE/IADES/Cebraspe), `vagas`, `fases`, `disciplinas` (lista), `pesos`, `num_questoes_fase1`, `num_questoes_por_disciplina`, `criterios_aprovacao`, `exam_regime` (A–E), `edital_url`
- **Ferramentas:** leitura manual/LLM-assistida dos editais; 24 registros
- **Aceitação:** todo `contest_id` com regime e nº de questões preenchidos; mudanças de edital anotadas (retificações)
- **Cuidado:** usar o edital **atualizado/retificado** quando houver; não confundir ano-calendário com edição (`CACD_2020_2021`)

### ETAPA 3: download dos PDFs 🔄 (em execução)
- Script: `scraper/download.py` — 463 jobs, retomável, validação de magic bytes, SHA-256
- Manifest: `data/raw/download_manifest.csv` (ok/falha por URL)
- **Ao terminar:** checar falhas; para cada falha, tentar fonte alternativa do catálogo; PDFs sem fallback ficam `NOT_FOUND` documentados
- Pendências conhecidas (não bloqueantes): objetiva manhã 2019 no blob do Clipping (existe via Curso CACD); PCI/Gabarite exigem captcha (Playwright se necessário); SharePoint do Nabuco exige JS (redundante — cobertura já garantida)

### ETAPA 4: extração de texto ✅ script pronto
- `python parser/extract_text.py` — PyMuPDF; grava `data/processed/text/<contest_id>/<familia>/*.txt` + métricas
- Métricas por arquivo: páginas, chars, chars/página, questões detectadas (regex `QUESTÃO N`), `needs_ocr`
- **Aceitação:** ≥90% das provas com nº de questões detectadas compatível com o nº oficial do edital; PDFs escaneados (pré-~2010) marcados `needs_ocr` para OCR posterior (tesseract)
- **Risco:** provas antigas (2003–2012) podem ser escaneadas → decidir OCR por amostra

### ETAPA 5: segmentação de questões + dataset granular ⏳ (próxima)
- **Output:** `data/processed/questions.parquet` — 1 linha por questão, schema:
  `question_id` (SHA-1 de contest_id+fase+disciplina+numero), `contest_id`, `year`, `phase`, `stage`, `discipline`, `question_number`, `question_type` (multiple_choice | certo_errado | essay), `question_text`, `alternative_A..E`, `answer`, `source_url`, `source_type`, `source_file`, `page`
- **Pipeline:** regex de marcadores de questão por família de fonte (Cebraspe/Iades/Wix têm layouts diferentes) → heurísticas → LLM só para casos ambíguos (via `litellm` + `instructor`, saída Pydantic) → amostra revisada manualmente
- **Validação:** por edição, nº de questões extraídas vs. nº do edital; exigir ≥95% antes de prosseguir; amostra de ~5% revisada à mão
- **Dois jeitos de obter gabarito:** PDF de gabarito separado (merge por nº da questão + turno) ou gabarito embutido no caderno (Iades costuma vir separado)
- Ferramentas: pandas, PyArrow, pandera (schema), DuckDB para QA
- **Cuidado especial:** questão certo/errado da IADES tem 4–5 itens por questão → decidir granularidade (questão vs. item) **antes** de gerar o dataset; recomendação: 1 linha por item com `item_id`, herdando `question_id` pai

### ETAPA 6: validação manual de amostra ⏳
- Amostra estratificada: ~10% das questões, mínimo 20 por edição, todas as disciplinas
- Ferramenta: revisão via notebook/CSV (Label Studio é overkill nesta fase)
- Critério de aprovação: ≥97% de fidelidade texto-alternativa-gabarito; senão, corrigir heurísticas e reprocessar

### ETAPA 7: taxonomia temática ⏳
- **Fontes para construir** (documentar critérios, não criar arbitrariamente): programas/ementas dos editais, bibliografias, análise das questões, clustering de embeddings (Etapa 8), classificação por LLM, revisão manual
- **Output:** `data/metadata/taxonomy.md` + `data/processed/topics.parquet` — hierarquia `discipline → topic → subtopic → concept`
- **Anti-leakage crítico:** a taxonomia usada no fold do ano X deve poder ser re-construída só com provas ≤ X. Estratégia: taxonomia-base versionada + cláusula de re-fit por fold (ou versões datadas da taxonomia)
- **Por disciplina** (composição mudou ao longo dos anos): História do Brasil, História Mundial/Teoria das RI (verificar nomenclatura por edital), Geografia, Política Internacional, Economia, Direito e Direito Internacional Público, Português, Inglês, Espanhol+Francês

### ETAPA 8: NLP — embeddings, similaridade, clustering ⏳
- Ferramentas: `sentence-transformers` com `intfloat/multilingual-e5-large` (primário), `BAAI/bge-m3` e LaBSE como comparação; UMAP+HDBSCAN; TF-IDF como baseline lexical
- **Outputs:** `data/embeddings/*.npz`, mapa de clusters em `data/processed/clusters.parquet`
- Requisito: benchmark entre os 3 modelos de embedding em tarefa proxy (ex.: agrupar questões re-aplicadas nos anos seguintes — "recorrência real" como ground truth)
- Anti-leakage: vocabulário TF-IDF e clusters re-fitados por fold

### ETAPA 9: features estatísticas + 4 baselines ⏳
- Features por (tema, ano): `frequency_total/10y/5y/3y`, `years_since_last_occurrence`, `mean_interval`, `std_interval`, `recent_trend`, `questions_last_exam/3exams/5exams`, `syllabus_weight` (do contest_registry), `banca_is_iades`, `exam_regime`
- Baselines (em `models/baseline/`): B1 frequência total · B2 frequência 5 anos · B3 recência · B4 combinação (frequência+recência+tendência+peso edital)
- **Aceitação:** os 4 baselines rodando em todos os folds com métricas registradas no MLflow

### ETAPA 10: ML + Laya + ensemble ⏳
- **ML tabular:** Logistic Regression, Random Forest, XGBoost (principal), LightGBM; Optuna dentro de cada fold (nunca vendo o teste); target binário (tema apareceu na próxima prova: 1/0)
- **Laya** (`convaiinnovations/laya`, HF, Apache 2.0 — ModernBERT-large 421M, decisão tipada não-autorregressiva):
  - Usar **checkpoint multilingual** (PT-BR); en-only como comparação
  - **Caveats medidos** (fonte: benchmark Zylver 09/2026): base checkpoints ≈ acaso zero-shot fora do domínio; saem **superconfiantes** → **calibração (temperature refit) obrigatória nos folds de validação**; limite de **512 tokens por questão** (state + pergunta + opções) → estado histórico precisa ser comprimido/resumido
  - Formato de entrada = JSON `state`/`question`/`criteria` (a estrutura da descrição original já bate)
  - Benchmark obrigatório: Laya zero-shot, Laya fine-tuned (só se dados justificarem — gate explícito), XGBoost, LogReg, RF, XGBoost+embeddings, Laya+features
  - Jev (TypeSafe) é API fechada/paga — apenas baseline de terceiros publicado, não dependência
  - GPU: T4 suficiente (~38ms/questão); CPU viável para o volume do projeto
- **Fine-tuning "Laya-CACD":** só depois de verificar o código de treino no repo oficial; gate: dados (~20 concursos × dezenas de temas) provavelmente insuficientes → decidir com dado na mão
- **LLM complementar** (`litellm` + `instructor`): classificação temática (questão→tema/subtema), explicação de scores, geração de questões inéditas e simulados (sempre marcadas `GERADA POR IA`, reproduzindo distribuição/dificuldade/estilo do edital)

### ETAPA 11: backtesting + avaliação ⏳
- Splitter em `evaluation/`: folds 2017→2025 (treino 2006–X, teste X+1), respeitando regimes de banca
- Métricas **implementadas e testadas com pytest** (não confiar em lib): Precision@K, Recall@K, F1@K, MAP@K, NDCG@K — calibrar K ao nº médio de temas por prova; recortes por disciplina
- Tabela final comparativa (MLflow): 4 baselines + LogReg + RF + XGBoost + XGBoost+emb + Laya + Laya+estatística
- Relatório final por fold: previsões vs. prova real, acertos, erros, evidência histórica — linguagem de score/probabilidade

### ETAPA 12: dashboard + simulados (futuro) ⏳
- FastAPI + PostgreSQL (SQLAlchemy/Alembic) · Next.js + Tailwind + shadcn/ui · Docker
- Features: ranking por disciplina com barras de score, evolução histórica por tema, alerta de temas "vencidos" (longo tempo sem aparecer + tendência), simulados gerados por LLM

---

## 4. Convenções técnicas

- **IDs determinísticos:** `question_id` = SHA-1(`contest_id|fase|disciplina|número|item`); `topic_id` = slug estável
- **Datasets**: Parquet em `data/processed/`; consultas analíticas com DuckDB; schemas com pandera
- **Config**: YAML em `configs/` (splits, janelas, K, thresholds) — nada de parâmetros mágicos no código
- **Experimentos**: MLflow local (`mlruns/`), um run por (modelo, fold)
- **Estilo**: ruff + mypy + pytest; commits convencionais (`feat:`, `fix:`, `docs:`…)
- **Python 3.12+**, deps em `requirements.txt`

## 5. Riscos registrados (não esquecer)

1. Provas 2003–2012 e 2019–2023 são de origem **secundária** — fielidade ao original deve ser checada por amostra (um cursinho pode ter errata)
2. OCR das provas antigas escaneadas pode degradar o dataset → métrica `needs_ocr` + decisão por ano
3. IADES (2019–2023) muda formato (certo/errado em itens) → granularidade do dataset deve acomodar os dois formatos
4. Gabaritos preliminares não sobreviveram para a maioria das edições — usar sempre o definitivo (e registrar quando só houver preliminar)
5. Laya é modelo novo e quase sem literatura: tratar como experimento, calibrar sempre, nunca substituir o pipeline estatístico
6. `curso_cacd_full.csv` foi extraído da página viva — re-validar URLs com HEAD na hora do download (15/15 amostra OK em 06/10/2026)

## 6. Checklist imediato (próxima sessão de trabalho)

- [ ] Conferir término do download (463 jobs) e resolver falhas com fallback
- [ ] Rodar `parser/extract_text.py` e revisar `text_metrics.csv` (casos `needs_ocr`)
- [ ] Etapa 2: preencher `contest_registry.csv` a partir dos editais
- [ ] Etapa 5: heurísticas de segmentação por família de fonte (começar pelo Cebraspe, formato mais estável)
- [ ] Decidir granularidade item-vs-questão para o formato IADES
- [ ] Commit + tag `v0.1-corpus`
