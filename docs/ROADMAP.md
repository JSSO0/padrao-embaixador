# Roadmap até o fim do projeto

> O que falta, em que ordem e como saber que acabou.
> Status atual e ganhos: [`MAPA-DO-PROJETO.md`](MAPA-DO-PROJETO.md). Elaborado em 27/10/2026.

---

## 1. Quando o projeto está **finalizado**

O projeto acaba quando a pergunta de pesquisa tiver uma resposta defensável, **seja ela sim ou não**:

> *Treinando só com provas até o ano X, um modelo prevê os temas da prova X+1 melhor que um
> baseline estatístico simples?*

| # | Critério de conclusão | Marco |
|---|---|---|
| 1 | Dataset da 1ª fase com ≥ 97% de fidelidade numa amostra revisada à mão | M1 |
| 2 | Todo item com um tema, numa taxonomia versionada e validada (≥ 90% de concordância) | M2 |
| 3 | Protocolo de backtest único e sem vazamento, com intervalo de confiança | M3 |
| 4 | Pelo menos 2 modelos comparados ao melhor baseline nesse protocolo | M4 |
| 5 | Qualquer pessoa reproduz os números com um comando; testes passando | M5 |
| 6 | Relatório final publicado com a resposta e as limitações; versão `v1.0` marcada | M6 |

Resultado negativo ("o histórico não prevê melhor que o baseline") **também conclui o projeto**,
desde que esteja medido com rigor.

---

## 2. Visão geral

```
 M1 Dados confiáveis ──► M2 Temas ──► M3 Avaliação honesta ──► M4 Modelos ──► M6 Fechamento
                                                     ▲
 M5 Reprodutibilidade ───────────────────────────────┘  (em paralelo, termina antes do M6)
```

| Marco | Objetivo | Estado | Esforço estimado |
|---|---|---|---|
| **M1 — Dados confiáveis** | Dataset da 1ª fase sem lixo e com gabarito documentado | 🔄 88% de fidelidade na amostra | 4–6 sessões |
| **M2 — Temas** | Cada item com um tema confiável e sem vazamento | 🔄 60 temas, 243 itens sem tema, sem validação | 2–3 sessões |
| **M3 — Avaliação honesta** | Um único protocolo de backtest, confiável | 🔄 3 scripts, 1 com vazamento | 2 sessões |
| **M4 — Modelos** | Testar se ML supera o baseline | ⬜ | 3–5 sessões |
| **M5 — Reprodutibilidade** | Clone, rode, confira | ⬜ | 2 sessões |
| **M6 — Fechamento** | Relatório final e `v1.0` | ⬜ | 1 sessão |
| | | **Total** | **~14–19 sessões** |

Categorias das tarefas: 🗂️ Dados · 🏷️ Taxonomia · 📏 Avaliação · 🤖 Modelagem · 🔧 Engenharia · 📝 Documentação

---

## 3. Marcos em detalhe

### M1 — Dados confiáveis

**Objetivo:** só entram no modelo questões reais da 1ª fase, com texto, disciplina e gabarito corretos.
**Por que importa:** a validação manual mostrou 6 de 50 questões com defeito, e todas vêm de linhas
extraídas automaticamente (`rules`). Prever temas com lixo no dado invalida o resto.

| ID | Cat. | Tarefa | Critério de aceite |
|---|---|---|---|
| M1.1 | 🔧 | Corrigir o default de anos do `pipeline/extract_gabaritos.py` (hoje apaga 2003–2014 quando rodado sem `--year`) | Rodar sem argumentos não altera respostas de 2003–2014 |
| M1.2 | 🗂️ | Remover da 1ª fase as linhas que vieram de PDFs de **discursiva** (`source_file` com `discursiva_*`) | 0 linhas de discursiva com `stage = primeira_fase` |
| M1.3 | 🗂️ | Transcrever à mão **2014, questões 32–73** (hoje 42 linhas `rules` sem itens e sem disciplina) | 2014 com 73 questões `manual`, 4 itens cada |
| M1.4 | 🗂️ | Revisar as demais linhas `rules` da 1ª fase: 2011 (37), 2024 (12), 2025 (17), 2026 (6), 2006, 2007, 2015, 2017, 2023 | Cada linha `rules` restante é substituída por `manual` ou tem justificativa em `notes` |
| M1.5 | 🗂️ | Registrar anulados: `notes = "anulado"` em todo item com X/#/☼ no gabarito oficial; QA passa a exibir "anulado" em vez de `nan` | 100% dos itens sem resposta têm o motivo em `notes` |
| M1.6 | 🗂️ | Gabaritos faltantes 2005–2013 via OCR (`ferramentas/extracoes_pontuais/ocr_gabaritos*.py`) | Itens sem resposta e sem motivo = 0 |
| M1.7 | 🗂️ | Defeitos pontuais: 2004 (manual duplicado `itn = qn`), 2013 (qn 174–227), 2024 (textos-base trocados), 2025 (item 235), 2018 Q40 (sufixo "Text V") | Cada caso corrigido ou documentado |
| M1.8 | 🗂️ | Teste de duplicidade: `contest + stage + discipline + qn + itn` único | `duplicated().sum() == 0` |
| M1.9 | 📏 | **Nova amostra de 50** questões (outra seed) e revisão manual | ≥ 97% OK |

**Pronto quando:** M1.9 ≥ 97% e nenhuma linha `rules` sem justificativa na 1ª fase.

---

### M2 — Temas

**Objetivo:** cada item da 1ª fase tem **um** tema, vindo de uma taxonomia escrita e versionada.
**Situação:** existem 60 temas e 243 itens (4,8%) sem tema. O "geral" sumiu porque o
`refine_taxonomy_tfidf.py` força cada item ao tema mais próximo. Isso foi feito usando **todos os anos
de uma vez**, o que é um vazamento leve: a definição dos temas "conhece" o futuro.

| ID | Cat. | Tarefa | Critério de aceite |
|---|---|---|---|
| M2.1 | 🏷️ | Escrever a taxonomia em `data/metadata/taxonomia.yaml`: disciplina → tema → palavras-chave → descrição | Arquivo versionado; os scripts leem dele (nada hardcoded) |
| M2.2 | 🏷️ | Classificar os 243 itens sem tema | 0 itens sem tema na 1ª fase |
| M2.3 | 🏷️ | Classificação **sem olhar o futuro**: regras fixas do YAML (definidas a priori) ou centroides recalculados por fold | Documentado qual método; teste prova que o fold X não usa itens > X |
| M2.4 | 🏷️ | Balancear a granularidade: nenhum tema com > 8% dos itens nem com < 0,5% (juntar ou dividir) | Distribuição publicada em `docs/relatorios/` |
| M2.5 | 📏 | Validar 50 classificações à mão | ≥ 90% de concordância |

**Pronto quando:** M2.5 ≥ 90% e o M2.3 provado por teste.

---

### M3 — Avaliação honesta

**Objetivo:** um único jeito de medir, que valha para todos os modelos do M4.
**Situação:** há 3 scripts (`backtest.py`, `backtest_temas.py`, `backtest_tfidf.py`). O nível
disciplina está saturado (0,97) e o TF-IDF lê a prova X+1 (vazamento). Hoje o baseline real é o
**Markov por tema, 0,79**.

| ID | Cat. | Tarefa | Critério de aceite |
|---|---|---|---|
| M3.1 | 📏 | Retirar o `backtest_tfidf.py` da comparação (é um classificador, não um previsor) e marcar o 0,90 como inválido nos resultados | Nenhum relatório compara o 0,90 com os baselines |
| M3.2 | 📏 | Escrever o **protocolo** em `docs/referencia/protocolo-avaliacao.md`: folds X = 2017…2025, unidade = tema, K fixo, métricas (Precision@K, Recall@K, NDCG@K, MAP@K) | Documento aprovado antes do M4 |
| M3.3 | 🔧 | Unificar em `evaluation/run.py --metodo <nome>`: a mesma função de folds e métricas para todos os métodos | Um script; uma tabela de saída em `data/resultados/` |
| M3.4 | 📏 | Adicionar o **piso** (aleatório) e o **teto** (oráculo) para dar escala aos números | Tabela com aleatório < baselines < oráculo |
| M3.5 | 📏 | Intervalo de confiança (bootstrap sobre os folds) e teste de diferença vs. o melhor baseline | Todo número publicado tem IC 95% |
| M3.6 | 📝 | Relatório por fold: temas previstos × temas que caíram | `data/resultados/relatorio_folds.md` |

**Pronto quando:** os 4 baselines (+ aleatório e oráculo) rodam por tema no `run.py`, com IC.

---

### M4 — Modelos

**Objetivo:** testar se algo além de "repetir o passado" prevê melhor.
**Formulação:** para cada par (tema, ano X+1), prever a probabilidade de o tema cair, e ranquear o top-K.

| ID | Cat. | Tarefa | Critério de aceite |
|---|---|---|---|
| M4.1 | 🤖 | Tabela de features por (tema, ano) com dados só ≤ X: frequência acumulada, caiu nos últimos 1/2/3 anos, anos desde a última vez, tendência, banca/era, peso da disciplina | `features/` + teste de não-vazamento |
| M4.2 | 🤖 | Modelo 1: **regressão logística** (simples, interpretável) | Rodado no protocolo M3 |
| M4.3 | 🤖 | Modelo 2: **XGBoost ou LightGBM** | Rodado no protocolo M3 |
| M4.4 | 🤖 | *(Opcional)* Similaridade semântica com embeddings (sentence-transformers) como feature: "o assunto do ano passado se aproxima deste tema?" | Só entra se melhorar no protocolo |
| M4.5 | 📏 | Calibração (Brier score, curva de confiabilidade) | Probabilidades calibradas ou o desvio documentado |
| M4.6 | 📏 | Tabela final: modelos × baselines, por tema e por disciplina, com IC | `data/resultados/comparacao_final.md` |
| M4.7 | 📝 | Interpretação: quais features importam e em quais disciplinas o modelo ganha ou perde | Seção no relatório final |

**Pronto quando:** M4.6 publicado, ganhe ou perca do baseline.

---

### M5 — Reprodutibilidade *(em paralelo)*

| ID | Cat. | Tarefa | Critério de aceite |
|---|---|---|---|
| M5.1 | 🔧 | `verify_manifest.py`: recalcula os SHA-256 dos 463 arquivos de `data/raw/` | Falha em qualquer divergência |
| M5.2 | 🔧 | Acertar o `requirements.txt`: incluir o que é usado (`pytesseract`, `Pillow`, `matplotlib`, `pydantic`) e remover o que não é (`pdfplumber`, `duckdb`, `optuna`, `mlflow` até serem usados) e fixar versões | `pip install` limpo roda o pipeline |
| M5.3 | 🔧 | Testes pytest: parsers (1 por banca), aplicação de gabarito, métricas @K e não-vazamento | ≥ 8 testes passando |
| M5.4 | 🔧 | Um comando para tudo: `python -m pipeline.run` (dados → taxonomia → backtest) | Gera os mesmos números do relatório |
| M5.5 | 🔧 | CI no GitHub Actions rodando os testes | Badge verde no README |
| M5.6 | 📝 | Documentar a instalação do Tesseract 5 + `por.traineddata` (só para quem for refazer OCR) | Seção em `pipeline/README.md` |

---

### M6 — Fechamento

| ID | Cat. | Tarefa | Critério de aceite |
|---|---|---|---|
| M6.1 | 📝 | `docs/relatorio-final.md`: pergunta, dados, método, resultados com IC, limitações, resposta | Revisado por você |
| M6.2 | 📝 | Card do dataset (`data/README.md`): colunas, cobertura por ano, licença, defeitos conhecidos | Publicado |
| M6.3 | 📝 | README e MAPA com o estado final | Sem pendências abertas |
| M6.4 | 🔧 | Tag `v1.0` + release no GitHub | Release criado |

---

## 4. Ordem sugerida

| Sessão | Foco |
|---|---|
| 1 | M1.1 (bug do gabarito) + M1.2 (remover discursivas) + M1.5 (anulados) + M5.2 (requirements) |
| 2–3 | M1.3 (transcrever 2014 Q32–73) |
| 4 | M1.4 + M1.7 (linhas `rules` restantes e defeitos pontuais) |
| 5 | M1.6 (OCR de gabaritos) + M1.8 + M1.9 (nova amostra) |
| 6–7 | M2 completo (taxonomia YAML, classificação, validação) |
| 8–9 | M3 completo (protocolo, `run.py`, IC) + M5.3 (testes) |
| 10–13 | M4 (features, logística, XGBoost, comparação) |
| 14 | M5.1, M5.4, M5.5 (manifest, comando único, CI) |
| 15 | M6 (relatório final e `v1.0`) |

---

## 5. Fora do escopo da v1.0

Ficam registrados para depois. Nenhum bloqueia o fim do projeto.

| Item | Por quê |
|---|---|
| Discursivas (2ª e 3ª fase) | Não fazem parte da pergunta de pesquisa (1ª fase) |
| Dados administrativos por edição (antiga Etapa 2) | Só entra se o M4 precisar de "regime de banca" como feature; a era da banca já cobre isso |
| Laya / Jev e LLM complementar | Só faz sentido se o M4 mostrar sinal preditivo |
| Dashboard e simulados | Produto, não pesquisa |
| Posts | Fora dos marcos, por decisão de 27/10 |

---

## 6. Riscos

| Risco | Impacto | Mitigação |
|---|---|---|
| Só 9 folds | IC largo; diferenças pequenas não são significativas | Bootstrap (M3.5) e relatar por disciplina |
| Mudança de banca (CESPE → IADES → Cebraspe) muda o estilo das questões | O passado prevê pior | Feature de era (M4.1) e análise por era |
| Taxonomia subjetiva | Os resultados dependem de como os temas foram definidos | YAML versionado + validação manual (M2) |
| Transcrição manual de 2014 é trabalhosa | Atrasa o M1 | Pode ser feita em paralelo ao M2.1 e M3.2 |
