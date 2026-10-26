# Roadmap — CACD Forecast AI

> Timeline de objetivos para alcançar o resultado do projeto: medir se o
> histórico das provas permite estimar a distribuição temática da próxima
> edição, com backtesting temporal e comparação de baselines.

Estado em 26/10/2026: **5.572 registros**, 5.038 itens 1ª fase (96% gabarito),
disciplinas canonizadas, taxonomia v0 (45 temas), backtesting v0
(Precision@K 0.97 disciplina / 0.82 tema).

---

## MILESTONE 1 — Corpus completo e limpo
**Meta: 1ª fase e discursivas com cobertura máxima e qualidade auditável.**

| # | Tarefa | Critério de aceite | Esforço |
|---|---|---|---|
| 1.1 | OCR das letras de gabarito faltantes (2005-2013) | 0 itens com `answer=null` e `notes` sem "anulado" | 1 sessão |
| 1.2 | OCR das 2 questões de 2010 (q38-39 já feitas via OCR; validar gabarito) | q38 e q39 com resposta preenchida | 1 sessão |
| 1.3 | Transcrição 2009-2012 3ª fase (provas escritas em scan) | ≥ 12 registros/ano na 3ª fase | 1-2 sessões |
| 1.4 | 2013-2016: rodar gabaritos no parquet atual | answer preenchida nas 3ª fase 2013-2016 | incluído em 1.1 |
| 1.5 | Dedup final: nenhuma questão duplicada | `df.duplicated(subset=[contest,phase,stage,subdisc,qn,itn]).sum() == 0` | incluído |

**Dependências:** tesseract ✅ instalado · por.traineddata ✅ · zips extraídos ✅

---

## MILESTONE 2 — Taxonomia temática v1
**Refinar de 45 temas (v0) para ~80-120 temas, eliminando o tema "geral".**

| # | Tarefa | Critério de aceite | Esforço |
|---|---|---|---|
| 2.1 | Definir taxonomia YAML por disciplina (subtemas explícitos) | `data/metadata/taxonomia.yaml` com 10-15 temas/disciplina | 1 sessão |
| 1.2 | Classificar os 4.951 itens (keyword + TF-IDF) | < 15% dos itens com topic="geral" | 1 sessão |
| 2.3 | Validar amostra manual (50 itens aleatórios) | ≥ 90% de concordância na classificação | incluído |

**Dependências:** nenhum. Pode começar agora.

**Por que importa:** o Precision@K atual (0.82) mede disciplinas+temas, mas
25% dos itens caem em "geral". Reduzir isso aumenta a granularidade e a
qualidade do backtest temático.

---

## MILESTONE 2 — Baselines NLP (Etapa 8 do plano mestre)

**Meta: comparar os 4 baselines estatísticos (já rodando) com um baseline de
similaridade de texto (TF-IDF) — o primeiro "modelo inteligente" do projeto.**

| # | Tarefa | Critério de aceite | Esforço |
|---|---|---|---|
| 2.1 | TF-IDF por fold (anti-leakage: fit só com provas ≤ X) | vetorizador salvo por fold | 1 sessão |
| 2.2 | Similaridade cosseno: temas do histórico vs os textos de X+1 | ranking de temas por similaridade | incluído |
| 2.3 | Comparar Precision@K do TF-IDF vs os 4 baselines estatísticos | relatório comparativo gerado | incluído |

**Dependências:** Milestone 1 (taxonomia refinada) · sklearn instalado

**Insight esperado:** o TF-IDF pode superar os baselines estatísticos se o
texto dos enunciados contiver sinais temáticos que a frequência de
disciplina não captura.

---

## MILESTONE 3 — Backtesting completo (Etapa 9-11)

**Meta: rodar os 9 folds com TODOS os métodos e gerar o relatório final.**

| # | Tarefa | Critério de aceite | Esforço |
|---|---|---|---|
| 3.1 | Backtesting temático com a taxonomia refinada (M1) | 9 folds com Precision@K, Recall@K, F1@K, NDCG@K, MAP@K | incluído |
| 2.2 | 4 baselines + TF-IDF + XGBoost | tabela comparativa com 6+ modelos | 1-2 sessões |
| 2.3 | Relatório por fold: previsões vs prova real | markdown com gráfico por fold | incluído |
| 2.4 | Gráfico Precision@K por fold (matplotlib) | PNG salvo em `docs/assets/` | incluído |

**Dependências:** Milestone 1 (taxonomia) · Milestone 2 (TF-IDF)

**Este milestone entrega o conteúdo do post do dia 19.**

---

## MILESTONE 3 — Post do dia 19 (Precision@K)

| # | Tarefa | Critério |
|---|---|---|
| 3.1 | Gerar o gráfico de Precision@K por fold | PNG pronto |
| 3.2 | Escrever o post com os números reais | 600-1.200 chars |
| 3.3 | Validar o checklist de compliance | sem promessa, com "NÃO prova" |

**Dependências:** Milestone 2 completo.

---

## MILESTONE 4 — Post do dia 30 (reprodutibilidade)

| # | Tarefa | Critério |
|---|---|---|
| 4.1 | Implementar `verify_manifest.py` | recalcula 463 SHA-256, falha em divergência |
| 4.2 | Rodar no repo atual e confirmar 100% ok | output verificado |
| 4.3 | Atualizar o README com a seção de reprodução | comando documentado |

**Dependências:** nenhuma — pode ser feito em paralelo com M1-M3.

---

## MILESTONE 5 — Discursivas (refinamento, pode esperar)

| # | Tarefa | Esforço |
|---|---|---|
| 5.1 | Padrões de resposta 2017+ (baixar os faltantes) | 1 sessão |
| 5.2 | OCR das discursivas 2019-2023 restantes | 1-2 sessões |
| 5.3 | 2003-2007: extrair as provas escritas restantes | 1-2 sessões |
| 5.4 | 2018: modelar redação/exercícios | 1 sessão |

---

## MILESTONE 6 — Dashboard + simulados (Etapa 12, futuro)

FastAPI + Next.js — fora do escopo até o backtesting estar estável.

---

## Timeline sugerida (ordem de execução)

```
Sessão 1 (agora):  M1 (taxonomia refinada) → M2 (TF-IDF baseline) → M3 (backtest completo)
Sessão 2:          M4 (post dia 30) + M5 (padrões 2017)
Sessão 3:          M2 (restante das discursivas) + M6 (testes pytest)
Sessão 4:          post do dia 19 com gráfico real + relatório final
```

## Definição de "projeto completo"

- [ ] 1ª fase: 5.020 itens, 100% com gabarito ou "anulado" documentado
- [ ] Taxonomia: < 15% "geral"
- [ ] Backtesting: 9 folds × 6+ modelos comparados
- [ ] Post do dia 19: publicado com gráfico real
- [ ] Post do dia 30: "Clone e confira" funcionando
- [ ] Testes: ≥ 5 testes pytest cobrindo os parsers críticos
