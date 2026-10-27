# Mapa do Projeto — CACD Forecast AI

> **Fonte única da verdade** para objetivo, marcos, status e ganhos.
> Os planos antigos (plano mestre, roadmap, tasks abertas, contexto das conversas) estão em
> `docs/historico/`. Se algo aqui divergir deles, vale este arquivo.
>
> Atualizado em 27/10/2026.

---

## 1. Objetivo em uma frase

**Medir se o histórico das provas do CACD (2003–2026) permite prever quais _temas_
vão cair na próxima edição — melhor do que um chute estatístico simples.**

- **Pergunta de pesquisa:** treinando só com provas até o ano X, quantos dos temas que
  caíram em X+1 o modelo teria acertado?
- **Critério de sucesso:** um modelo supera os baselines estatísticos (frequência, recência,
  Markov) em Precision@K **por tema**, em backtesting temporal, **sem usar nada da prova X+1**.
- **Não é objetivo:** prever a questão literal.

---

## 2. Marcos (substituem "Etapas 1–12", "M1–M6" e "T0xx")

| Marco | Entrega | Status | Critério de "pronto" |
|---|---|---|---|
| **M0 — Corpus** | PDFs catalogados, baixados e convertidos em texto | ✅ concluído | 463 arquivos com SHA-256 no manifest; texto extraído de todas as edições |
| **M1 — Dataset da 1ª fase** | `questions.parquet` com questões, gabarito e disciplina | 🔄 ~90% | ≥ 97% com gabarito (ou "anulado" documentado) **e** validação manual de 50 itens com ≥ 97% de fidelidade |
| **M2 — Taxonomia de temas** | Cada questão com um tema (`topic`) | 🔄 v1 | < 15% dos itens no tema "geral" + 50 itens conferidos à mão com ≥ 90% de concordância |
| **M3 — Backtest honesto** | Baselines estatísticos avaliados por tema, 9 folds | 🔄 rodando, **precisa correção** (ver §4) | Tabela de baselines por tema sem vazamento; relatório por fold |
| **M4 — Modelo que supera o baseline** | NLP/ML (TF-IDF preditivo, embeddings, XGBoost) | ⬜ não iniciado | Precision@K por tema > melhor baseline, com intervalo de confiança |
| **M5 — Reprodutibilidade** | `verify_manifest.py` + testes pytest + pipeline de 1 comando | ⬜ não iniciado | "Clone e confira" funciona; ≥ 5 testes nos parsers |
| **M6 — Produto** | Dashboard e simulados | ⬜ futuro | Só começa depois de M4 |
| *Paralelo* — Discursivas | 2ª e 3ª fase extraídas | 🔄 parcial | Não bloqueia M1–M4 |

Ordem: **M1 → M2 → M3 → M4**. M5 pode andar em paralelo. M6 e discursivas esperam.

### O que falta em cada marco aberto

**M1 — Dataset**
- [ ] Validação manual das 50 questões (`data/processed/qa_sample/qa_validacao_manual.md`)
- [ ] Gabaritos faltantes 2005–2013 (~180 itens sem resposta; parte é anulada)
- [ ] 2004: manual duplicado (`itn = qn`) · 2013: 10 linhas com numeração ruidosa · 2024: textos-base trocados · 2025: item 235

**M2 — Taxonomia**
- [ ] Reduzir "geral" de 22% para < 15%
- [ ] Mover a taxonomia para um arquivo versionado (`data/metadata/taxonomia.yaml`)
- [ ] Conferir 50 classificações à mão

**M3 — Backtest**
- [ ] Corrigir o vazamento do TF-IDF (ver §4)
- [ ] Reportar só o nível **tema** como métrica principal (o nível disciplina está saturado)
- [ ] Gerar relatório por fold: previsto × o que caiu

---

## 3. Ganhos até agora

| Ganho | Número | Onde ver |
|---|---|---|
| Corpus | 23 edições (2003–2026), 463 arquivos rastreáveis | `data/raw/download_manifest.csv` |
| Questões da 1ª fase | **5.038 itens**, transcrição 100% | `data/processed/questions.parquet` |
| Gabarito | **96,4%** (4.858 / 5.038) | `python pipeline/overview.py` · `docs/relatorios/overview-questoes.md` |
| Disciplinas | 8 grupos canônicos, 98,6% classificados | coluna `discipline` |
| Temas | ~45 temas, 22% ainda em "geral" | coluna `topic` |
| Discursivas | 189 itens 2ª fase + 315 linhas 3ª fase | `questions.parquet` (`stage`) |
| Backtest | 9 folds × 5 métodos rodando | `evaluation/`, `data/resultados/` |

---

## 4. Leitura honesta dos resultados do backtest

| Métrica publicada | Leitura |
|---|---|
| **0,97** Precision@K por **disciplina** (Markov/recência) | Quase todas as 8 disciplinas caem em todas as provas, então acertar a lista é trivial. **Não mede capacidade preditiva.** |
| **0,79** Precision@K por **tema** (Markov) | Este é o baseline de verdade, o número a superar. |
| **0,90** Precision@K por **tema** (TF-IDF) | **Não é previsão.** `evaluation/backtest_tfidf.py` lê os textos da prova X+1 e classifica cada questão por tema; ele *rotula* a prova que já aconteceu em vez de *prever* a próxima. O número mede a qualidade da classificação, não da previsão. |

**Consequência:** hoje **nenhum modelo supera o baseline**. O ganho real do projeto até aqui
é o **dataset**; o ganho preditivo ainda não foi demonstrado. É isso que o M4 precisa provar.

---

## 5. Glossário (nomes usados no código)

| Termo | Significado |
|---|---|
| **CACD** | Concurso de Admissão à Carreira de Diplomata |
| `contest_id` | Edição do concurso, ex.: `CACD_2017` (edição ≠ ano-calendário) |
| `stage` | Fase da prova: `primeira_fase` (objetiva), `segunda_fase` (redação/português), `terceira_fase` (discursivas por disciplina) |
| `qn` / `question_number` | Número da questão na prova |
| `itn` / `item_number` | Número do item dentro da questão (provas de certo/errado têm vários itens por questão) |
| `discipline` | Uma das 8 matérias canônicas (História do Brasil, Política Internacional…) |
| `topic` | Tema dentro da disciplina — **é isto que o projeto tenta prever** |
| `source_type` | Origem da linha: **`rules`** = extraída automaticamente por parser · **`manual`** = transcrita/revisada à mão (vence `rules` em conflito) |
| **Banca / era** | Quem aplicou a prova: CESPE antigo (2003–2016), Cebraspe (2017–18, 2024–26), IADES (2019–23). Muda o formato do PDF |
| **Fold X** | Rodada do backtest: treina com provas até X, testa em X+1 (X = 2017…2025) |
| **Precision@K** | Dos K temas que o modelo apostou, quantos realmente caíram |
| **Baseline** | Regra estatística simples (frequência, recência, recência ponderada, Markov) usada como piso |
| **Vazamento (leakage)** | Usar informação da prova X+1 para "prever" a X+1; invalida o resultado |
| **Laya / Jev** | Modelos de decisão probabilística planejados para o M4 (ainda não usados) |

---

## 6. Onde está cada coisa

| Quero… | Onde |
|---|---|
| Ver objetivo, marcos e ganhos | **este arquivo** |
| Rodar o pipeline de dados (ordem é crítica) | `pipeline/README.md` |
| Rodar o backtest | `evaluation/` → resultados em `data/resultados/` |
| Ver números por ano | `docs/relatorios/overview-questoes.md` |
| Ver o dashboard visual | `docs/dashboard.html` |
| Requisitos originais e specs técnicas | `docs/referencia/` |
| Histórico de decisões e planos antigos | `docs/historico/` |
| Scripts usados uma vez (OCR, resgates) | `ferramentas/extracoes_pontuais/` |
| Scripts de inspeção e depuração | `ferramentas/diagnostico/` |

### Equivalência com os planos antigos

| Antigo | Novo |
|---|---|
| Etapas 1, 3, 4 | M0 |
| Etapa 5, Etapa 6, roadmap "M1", T010–T015, T030–T032 | M1 |
| Etapa 7, roadmap "M1 taxonomia", T022 | M2 |
| Etapas 9 e 11, roadmap "M2/M3", T024, T026 | M3 |
| Etapas 8 e 10, T023, T025 | M4 |
| `verify_manifest.py` (roadmap "M4"), T033 | M5 |
| Etapa 12, roadmap "M6" | M6 |
| Etapa 2 (dados administrativos) | backlog — só entra se o M4 precisar de "regime de banca" como feature |
| `plano-discursivas.md`, roadmap "M5", T015 | Paralelo — Discursivas |
| Posts (roadmap "M3/M4 post", T040, `conteudo/`) | fora dos marcos |
