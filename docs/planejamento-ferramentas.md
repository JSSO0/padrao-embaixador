# CACD Forecast AI — Planejamento de Ferramentas

Mapa de ferramentas por fase do projeto, com critérios de escolha e alternativas.
Regra geral: priorizar **reprodutibilidade**, **validação temporal** e **zero custo de licença** na fase experimental.

---

## 0. Decisões de plataforma (base)

| Decisão | Escolha | Justificativa | Alternativa |
|---|---|---|---|
| Linguagem | Python 3.12+ | Ecossistema de DS/ML/NLP | — |
| Gestor de pacotes/ambientes | `uv` | Rápido, lockfile determinístico (`uv.lock`), parte do README | Poetry, conda |
| Versionamento de dados | DVC | PDFs e datasets grandes versionados fora do Git, com checksums | git-lfs |
| Experiment tracking | MLflow (local) | Registra cada backtest (params, métricas, artefatos) | Weights & Biases |
| Configuração | YAML + Pydantic (`pydantic-settings`) | Splits, janelas temporais e thresholds como config, não código | Hydra |
| Qualidade | `ruff` + `mypy` + `pytest` + pre-commit | Padrão atual | — |
| CI | GitHub Actions | Rodar testes + validação de schema a cada push | — |
| Notebooks | Jupyter + `nbstripout` | Análises exploratórias sem poluir o Git | — |

---

## 1. Coleta (scraper) — Etapas 1–3 da primeira fase

| Ferramenta | Uso | Observações |
|---|---|---|
| `httpx` | Download de páginas e PDFs | Assíncrono, timeout configurável; registrar `source_url` de cada arquivo |
| `parsel` ou BeautifulSoup4 | Extração de links de editais/provas/gabaritos | `parsel` (XPath) é mais robusto para páginas do gov.br |
| Playwright (Python) | Páginas com renderização JS | gov.br e Cebraspe às vezes exigem JS; usar como fallback, não padrão |
| `tenacity` | Retry com backoff | Respeitar servidores públicos; delay entre requisições |
| CSV/Parquet + Pydantic | Catálogo de fontes (ano, edição, fonte, URL, tipo, fase, status) | Status: `FOUND` / `NOT_FOUND` / `DUPLICATED` / `OFFICIAL_ONLY` — nunca inventar URL |

**Saída:** `data/metadata/source_catalog.csv` + PDFs em `data/raw/`, nomeados `CACD_<ano>_<fase>_<tipo>_<source_type>.pdf`.

**Prioridade de fonte** (implementar como campo ordenado): `official_mre` > `official_cebraspe` > `secondary_repository` > `unknown`.

---

## 2. Parsing de PDFs (Etapa 4)

| Ferramenta | Papel | Justificativa |
|---|---|---|
| **PyMuPDF (fitz)** — primário | Extração de texto com coordenadas e fontes | Mais rápido e preciso; as marcas de questão ("QUESTÃO 12") mantêm layout detectável |
| **pdfplumber** — fallback | Provas com layout irregular / tabelas | Complementar ao PyMuPDF |
| pytesseract + pdf2image — último recurso | PDFs escaneados sem camada de texto | Provas antigas (pré-~2010) podem ser digitalizadas; registrar `needs_ocr` no catálogo |
| Docling (opcional) | Provas com layout complexo | Avaliar só se os dois primeiros falharem |

**Métrica de qualidade:** taxa de extração por concurso (nº de questões detectadas vs. nº oficial do edital). Abaixo de 90%, inspeção manual.

---

## 3. Segmentação de questões e dataset (Etapas 5–7)

| Ferramenta | Uso |
|---|---|
| Regex + heurísticas | Detectar início/fim de questão, alternativas A–E, blocos de disciplina |
| `spaCy` (`pt_core_news_lg`) | Segmentação de enunciados, normalização |
| LLM (via API, seção 6 abaixo) | Casos ambíguos de parsing — com revisão humana |
| `pandas` + PyArrow (Parquet) | Dataset granular (1 linha = 1 questão) e dataset temático |
| **DuckDB** | Consultas analíticas sobre o Parquet (frequências, janelas, intervalos) sem servidor |
| **pandera** | Validação de schema (tipos, `question_type` ∈ {multiple_choice, certo_errado, essay}, unicidade de `question_id`) |
| `hashlib` (SHA-1) | `question_id` determinístico = hash de (`contest_id`, fase, número, disciplina) — reprodutível |

**Atenção ao `contest_id`:** ano-calendário ≠ edição (caso 2020/2021). O mapeamento edição→ano fica em `data/metadata/contest_registry.csv`, criado manualmente.

---

## 4. NLP: embeddings, similaridade, clustering (seção 8 da descrição)

| Ferramenta | Uso | Justificativa |
|---|---|---|
| `sentence-transformers` | Embeddings das questões | — |
| **`intfloat/multilingual-e5-large`** — candidato primário | Embeddings multilingual com forte desempenho em PT | Boa relação qualidade/custo; testar com prefixos `query:`/`passage:` |
| **`BAAI/bge-m3`** — candidato alternativo | Alternativa forte para PT + retrieval | Comparar no benchmark |
| `LaBSE` — baseline leve | Referência rápida | Menor custo, qualidade menor |
| UMAP + HDBSCAN | Clustering não-paramétrico dos embeddings | Não exige definir K; permite ruído (questões atípicas) |
| BERTopic (opcional) | Clusters + rótulos interpretáveis | Usar só como apoio na construção da taxonomia; taxonomia final sempre revisada manualmente |
| `scikit-learn` | c-TF-IDF, TF-IDF como baseline lexical | Comparar "descoberta por vocabulário" vs. embeddings |

**Anti-leakage NLP:** o vocabulário do TF-IDF e a taxonomia derivada de clustering devem ser construídos **somente com provas ≤ ano de treino** dentro de cada fold do backtesting (documentar como materializar isso: re-fit por fold).

---

## 5. Features estatísticas e baselines (seções 9–10)

| Ferramenta | Uso |
|---|---|
| DuckDB + pandas | Cálculo de `frequency_*`, `years_since_last_occurrence`, `mean_interval`, `std_interval`, `recent_trend`, por disciplina |
| `statsmodels` | Teste de tendência (Mann-Kendall simples / regressão em janela) |
| Python puro | Baselines 1–4 (frequência, frequência recente, recência, combinação) — são rankings triviais, sem ML |

Cada baseline é um "modelo" registrado no MLflow com as mesmas métricas dos modelos de ML.

---

## 6. Machine Learning (seções 11 e 19)

| Ferramenta | Uso |
|---|---|
| `scikit-learn` | Logistic Regression, Random Forest, matriz de métricas, calibração |
| `xgboost` | Modelo principal tabular |
| `lightgbm` | Alternativa mais rápida; comparar |
| **Optuna** | Hyperparameter search **dentro** de cada janela temporal (nunca usando o fold de teste) |
| MLflow | Comparação de modelos (tabela da seção 19) |

**Target:** binário por (concurso, tema): apareceu / não apareceu. Cada tema vira uma linha por fold com o vetor de features da seção 11.

---

## 7. Laya / Jev — modelos de decisão tipada (seções 12–13)

### O que a pesquisa confirmou (fontes verificadas em 10/2026)

- **Laya** (Convai Innovations, HF: `convaiinnovations/laya`): open-source **Apache 2.0**, modelo de decisão "System 1" **não-autorregressivo**. Backbone ModernBERT-large (395M) + decision head = 421M params. Recebe um **state** (texto/JSON) + questões tipadas e devolve respostas tipadas com **probabilidades calibradas**. Não gera texto.
- **Checkpoints disponíveis:** inglês, **multilingual (100+ idiomas)** e fine-tuned. → Resposta à dúvida da seção 12: **sim, existe checkpoint multilingual**; usá-lo como padrão para PT-BR.
- **Limitação arquitetural crítica: orçamento de 512 tokens por questão** (state + pergunta + opções juntos). O state `"historical_exam_data"` precisará ser **resumido/comprimido** para caber.
- Benchmarks independentes (Zylver, 09/2026): Laya supera o Jev publicado em acurácia, calibração (ECE 0.081 vs 0.246) e latência (~33ms vs ~236–276ms p50) na maioria das tarefas; **Jev ganha em espaços de 50+ opções**. Nosso caso (ranking entre dezenas de temas) fica na faixa do Laya, mas **shortlist via embeddings antes do Laya** é a arquitetura recomendada se a lista de opções crescer muito.
- **Caveats fortes:** (a) checkpoints base pontuam **perto do acaso zero-shot** em tarefas fora do domínio de treino; (b) **ambos saem superconfiantes** — recalibração (temperature refit) é obrigatória; (c) modelo muito novo, sem literatura consolidada — tratar como experimento, não como aposta principal.

### Jev (TypeSafe)
- API fechada, early access, paga. Tratar como **baseline comparativo opcional** (publicado por terceiros), não como dependência do pipeline.

### Integração no pipeline

```
features estatísticas + embeddings
        ↓  (estado serializado, ≤512 tokens)
Laya (checkpoint multilingual)
        ↓
ranking / probabilidade por tema
```

- Formato de entrada do Laya **coincide** com o JSON proposto na seção 13 (`state` + `question` + `criteria`) — a estrutura já está correta.
- **Calibração:** refit de temperatura/isotônico nos anos de validação (nunca no ano de teste).
- **Benchmark obrigatório** (seção 12): Laya zero-shot multilingual, Laya fine-tuned, XGBoost, LogReg, RF, XGBoost+embeddings, Laya+features.
- **Fine-tuning ("Laya-CACD"):** só após verificar no repositório oficial o código/método de treino (RLCD) e se a quantidade de dados justifica (~20 concursos × dezenas de temas ⇒ poucas centenas de exemplos rotulados; provavelmente insuficiente → preferir poucas épocas em cima do checkpoint multilingual ou abortar). Gate explícito antes de treinar.

---

## 8. LLM complementar (seção 14)

| Tarefa | Ferramenta | Observação |
|---|---|---|
| Classificação temática (questão → disciplina/tema/subtema) | LLM via API com **saída estruturada** (`instructor` + Pydantic) | Custo baixo, rodar em lote, amostrar % para revisão manual |
| Explicação de score | LLM com os features como contexto | Texto gerado sempre rotulado |
| Geração de questões/simulados | LLM com few-shot de questões reais | Marca obrigatória **"GERADA POR IA"**; nunca apresentar como oficial |
| Escolha do provedor | Configurável (`litellm`) | Evitar lock-in; permitir trocar GPT/Claude/Gemini/open via vLLM sem mudar código |

**Anti-leakage para classificação:** usar snapshots de prompt/classificador por ano quando a classificação alimentar features de treino.

---

## 9. Backtesting e avaliação (seções 16–19)

| Ferramenta | Uso |
|---|---|
| Splitter custom (Python) | Janela expansiva: treino 2006–X, teste X+1, X de 2017 a 2025 |
| Métricas implementadas em `evaluation/` | Precision@K, Recall@K, F1@K, MAP@K, NDCG@K — implementação própria testada com `pytest` (K calibrado ao nº médio de temas por prova) |
| `matplotlib` / `plotly` | Gráficos de evolução de métricas por fold |
| MLflow | Tabela comparativa final (seção 19) |

Restrições codificadas no splitter: (1) nenhum dado pós-X no treino; (2) taxonomia/embeddings/TF-IDF re-fitados por fold; (3) eventos contemporâneos (seção 22) filtrados por data < prova.

---

## 10. Dashboard / API / Infra (futuro — seção 24)

| Camada | Ferramenta |
|---|---|
| Backend | FastAPI + Uvicorn |
| DB | PostgreSQL + SQLAlchemy + Alembic |
| Frontend | Next.js (React) + Tailwind + shadcn/ui |
| Servindo modelos | Laya via `transformers` + torch (GPU T4 ou superior; ~38ms/questão viabiliza batch); XGBoost/LightGBM serializados (`.json`/`.joblib`) |
| Contêineres | Docker + docker-compose (api, db, frontend) |

---

## 11. Matriz resumida — fase → ferramentas principais

| Fase | Principal | Alternativas/Fallback |
|---|---|---|
| Coleta | httpx + parsel | Playwright |
| Parsing PDF | PyMuPDF | pdfplumber → OCR |
| Dataset | pandas + Parquet + DuckDB + pandera | — |
| Embeddings | multilingual-e5-large | bge-m3, LaBSE |
| Clustering | UMAP + HDBSCAN | BERTopic |
| Baselines | Python puro | — |
| ML tabular | XGBoost | LightGBM, RF, LogReg |
| Decisão probabilística | Laya multilingual | Jev (API paga, opcional) |
| LLM auxiliar | litellm + instructor | vLLM + modelo aberto |
| Backtesting | splitter custom + métricas próprias | — |
| Tracking | MLflow | W&B |
| Dados | DVC | git-lfs |
| API/Dashboard | FastAPI + PostgreSQL + Next.js | — |

---

## 12. Riscos técnicos registrados

1. **Laya é muito recente (set/2026)** — sem literatura consolidada; checkpoints base quase aleatórios zero-shot no domínio CACD. Mitigação: benchmark obrigatório e gate antes de fine-tuning.
2. **Limite de 512 tokens do Laya** — state histórico precisa de compressão/resumo testável.
3. **Calibração** — refit obrigatório em anos de validação; sem isso, "confiança alta/baixa" do relatório final não significa nada.
4. **Provas antigas escaneadas** — OCR degradará o dataset pré-~2010; marcar no catálogo e possivelmente excluir do corpus quantitativo.
5. **Mudança de banca/formato** — o campo `exam_regime` (seção 21) vira feature e filtro de comparabilidade.
