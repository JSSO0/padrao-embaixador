# CACD Forecast AI — Especificação Original (requisitos)

> Fonte da verdade dos requisitos. Escrita pelo autor do projeto em 06/10/2026.
> Toda decisão de implementação deve poder ser rastreada até uma seção deste documento.
> O plano de execução (`docs/plano-mestre.md`) operacionaliza estas especificações.

---

# CACD Forecast AI — Previsão de temas e questões do Concurso de Admissão à Carreira de Diplomata

## 1. Objetivo do projeto

Desenvolver um projeto de Data Science / Machine Learning / NLP para analisar o histórico das provas do CACD e tentar prever quais temas, subtemas, conceitos e formatos de questão têm maior probabilidade de aparecer nas próximas provas.

O objetivo **não é** afirmar que podemos prever exatamente a próxima questão. O objetivo científico é:

> Avaliar até que ponto o histórico das provas do CACD permite prever a distribuição temática da próxima prova e quais técnicas de estatística, Machine Learning, NLP e LLM apresentam melhor desempenho.

O projeto deverá utilizar backtesting temporal, evitando data leakage.

## 2. Corpus histórico

Coletar o máximo possível de provas históricas, priorizando ~20–26 concursos.

**Fontes prioritárias:**

1. **Fonte oficial — MRE / Instituto Rio Branco**: https://www.gov.br/mre/pt-br/instituto-rio-branco/carreira-diplomatica/editais-cacd-1 — páginas por edição (CACD 2003–2026). Pesquisar também anos anteriores a 2003.
2. **Cebraspe**: páginas oficiais por concurso com edital, caderno de prova, provas objetivas/discursivas, gabarito preliminar e definitivo, padrões de resposta, resultados, recursos. Ex.: `https://www.cebraspe.org.br/concursos/irbr_26_diplomacia`, `.../irbr_25_diplomacia`, e edições anteriores.
3. **Lutz CACD**: https://lutzcacd.com.br/todas-as-provas-anteriores-cacd/ — coleção 2003–2026; fonte complementar para arquivos difíceis de achar.
4. **Curso CACD**: https://www.cursocacd.com/conteudo — fonte complementar.
5. **Nabuco CACD**: https://nabucocacd.com.br/provas-antigas/ e https://nabucocacd.com.br/guias-de-estudos/ — documentos históricos e checagem de lacunas.

## 3. Regra de confiabilidade das fontes

Registrar a origem de cada arquivo:

```
source_type:
    official_mre
    official_cebraspe
    secondary_repository
    unknown
```

Prioridade: MRE/IrBr > Cebraspe > repositórios especializados > outras.
Se houver dois arquivos da mesma prova, preferir o oficial. Não assumir que a prova de um cursinho é idêntica ao documento oficial.

## 4. Não confundir ano-calendário com edição

Criar identificador próprio por concurso: `contest_id = CACD_2026`, `CACD_2025`, … `CACD_2020_2021`.
A edição 2020 começou em 2020 e teve etapas posteriores. Não usar o ano do PDF como identificador.

## 5. O que coletar de cada concurso

- **Informações administrativas:** ano, banca, edital, nº de vagas, cargo, fases, disciplinas, pesos, nº de questões, duração, critérios de aprovação.
- **Provas** (separadamente): objetiva, discursiva, segunda fase, terceira fase.
- **Gabaritos:** preliminar **e** definitivo (não substituir um pelo outro).
- **Padrões de resposta:** resposta esperada, padrão de correção, critérios de pontuação, espelho quando disponível.

## 6. Dataset principal

Granular — 1 linha por questão:

```
question_id, contest_id, year, phase, stage, discipline, question_number,
question_type, question_text, alternative_A..E, answer,
source_url, source_type, source_file, page
```

`question_type`: `multiple_choice` | `certo_errado` | `essay`.

## 7. Dataset temático

Classificação hierárquica: `discipline → topic → subtopic → concept`.
Ex.: História do Brasil → Era Vargas → Estado Novo → Política externa brasileira.

Não criar taxonomia arbitrariamente sem documentar critérios. Usar: editais, livros/ementas, análise das questões, classificação por LLM, revisão manual/amostragem.

## 8. NLP

Embeddings por questão; similaridade entre questões; clustering → temas/subtemas. Testar modelos adequados para português/multilingual.

Pipeline: questão → normalização → embedding → similaridade → clustering → temas/subtemas. Objetivo: descobrir agrupamentos sem depender só de palavras-chave (duas questões podem tratar do mesmo assunto com vocabulário diferente).

## 9. Análise estatística

Por tema/subtema: frequência histórica, por disciplina, 10/5/3 anos, tempo desde última ocorrência, intervalo médio, desvio, tendência temporal, nº médio de questões por ocorrência.

## 10. Baselines (antes de qualquer IA)

1. Frequência histórica
2. Frequência recente (5 anos)
3. Recência (há mais tempo sem aparecer)
4. Combinação: frequência + recência + tendência + peso no edital

## 11. Machine Learning

Vetor de features por tema (frequências, recência, intervalos, tendência, questões por exame, peso no edital). Testar no mínimo: Logistic Regression, Random Forest, XGBoost, LightGBM. Target: `1 = tema apareceu na próxima prova`, `0 = não`.

## 12. Laya / Jev

Investigar o modelo **Laya** como componente de **decisão probabilística estruturada** (não substituto do pipeline). Fluxo desejado: `features históricas → Laya → ranking/probabilidade/score`. Investigar o checkpoint multilingual. Benchmark obrigatório: Laya · XGBoost · LogReg · RF · Laya+features · XGBoost+embeddings. Não assumir que funcionará bem apenas por ser open-weight.

## 13. Fine-tuning do Laya (Laya-CACD)

Investigar se permite fine-tuning e a metodologia recomendada atual. Dataset de treino no formato:

```json
{
  "state": {"historical_exam_data": "...", "discipline": "História", "recent_topics": "..."},
  "question": {"type": "choice", "instructions": "Qual tema possui maior probabilidade de aparecer?",
               "criteria": {"A": "Era Vargas", "B": "Guerra Fria", "C": "República Velha", "D": "Brasil Império"}},
  "answer": "A"
}
```

**NÃO fazer fine-tuning automaticamente** — primeiro avaliar se a quantidade e qualidade dos dados justificam.

## 14. LLM como camada complementar

- **Classificação:** questão → disciplina → tema → subtema
- **Explicação:** por que um tema recebeu score elevado?
- **Geração:** TOP 20 temas → LLM → questões inéditas, sempre marcadas **"GERADA POR IA"**, nunca apresentadas como oficiais.

## 15. Previsão do formato da questão

Prever também: tipo, dificuldade, forma de cobrança (conceitual, histórica, comparativa, cronológica, interpretação, exceção, legislação/tratado, relação causal). Objetivo: **TEMA + FORMATO** (ex.: Guerra Fria, alta probabilidade; formato mais recorrente: comparação entre eventos + RIs).

## 16. Backtesting temporal — obrigatório

Nunca split aleatório. Janela expansiva:

```
Treino 2006–2017 → teste 2018
Treino 2006–2018 → teste 2019
...
Treino 2006–2025 → teste 2026
```

Simula: "se eu estivesse vivendo naquele ano, o que o modelo teria previsto?"

## 17. Evitar data leakage

Cuidado com: informações de concursos futuros; taxonomia criada com todas as provas antes do split; embeddings com dados futuros; classificação temática olhando provas futuras; gabaritos/comentários publicados depois; notícias posteriores; alterações de edital posteriores. Documentar todos os casos de possível leakage.

## 18. Métricas

Não usar só accuracy. Calcular: **Precision@K, Recall@K, F1@K, MAP@K, NDCG@K** + métricas por disciplina.

## 19. Comparação dos modelos

Tabela: Modelo × Precision@10 / Recall@10 / NDCG@10 para: frequência histórica, frequência 5 anos, recência, LogReg, RF, XGBoost, embeddings+ML, Laya, Laya+estatística.

## 20. Avaliar por disciplina

Resultados separados por: História do Brasil, História Mundial, Política Internacional, Geografia, Economia, Direito, Língua Portuguesa, Língua Inglesa, demais disciplinas conforme o edital de cada edição (a composição mudou ao longo dos anos).

## 21. Mudanças de banca / formato / edital

Registrar alterações estruturais — prova de 2005 não é diretamente comparável a 2026. Criar `exam_regime` (regime_A, regime_B, regime_C…) para períodos com formatos diferentes; o modelo pode usar só concursos comparáveis ou o regime como feature.

## 22. Relação com acontecimentos contemporâneos

Testar empiricamente se eventos internacionais aumentam a probabilidade de certos temas. Se usado: coletar somente informação disponível **antes** da prova correspondente no backtesting (nunca notícia posterior).

## 23. Resultado final

Sistema produz relatório por disciplina: tema, score, confiança, última ocorrência, frequência histórica, tendência. Usar linguagem de *score / probabilidade estimada / ranking / evidência histórica* — nunca certeza.

## 24. Dashboard (futuro)

Backend Python+FastAPI, PostgreSQL, ML: scikit-learn/XGBoost/LightGBM, NLP: sentence-transformers/spaCy/transformers, LLM: Laya + outros por benchmark, Frontend React/Next.js, Infra Docker. Visual: barras de % por tema dentro de cada disciplina.

## 25. Geração de simulados

previsão → TOP 20 temas → seleção de distribuição → LLM → simulado CACD reproduzindo: distribuição de disciplinas, quantidade de questões, estilo, dificuldade, formato, proporção de temas.

## 26. Estrutura do repositório

```
cacd-forecast/
├── data/{raw, processed, embeddings, metadata}
├── scraper/  parser/  nlp/  features/
├── models/{baseline, xgboost, laya, ensemble}
├── evaluation/  notebooks/  api/  frontend/
├── tests/  docs/  README.md
```

## 27. Primeira fase — NÃO treinar modelo ainda

1. Catalogar todas as provas disponíveis
2. Tabela: ano, edição, fonte, URL, tipo, fase, disciplina, arquivo, status
3. Baixar os PDFs
4. Extrair o texto
5. Identificar automaticamente as questões
6. Validar manualmente uma amostra
7. Construir o dataset final
→ Só depois iniciar os modelos.

## 28. Entregáveis esperados da primeira etapa

Lista de concursos encontrados; URLs de cada fonte; URL direta dos PDFs; identificação oficial vs. não-oficial; provas faltantes; gabaritos; editais; padrões de resposta; nº de questões por concurso; disciplinas de cada concurso; dataset inicial estruturado; relatório de problemas; proposta de taxonomia; estratégias para NLP, ML, Laya e backtesting.

## 29. Regra importante sobre pesquisa

**Não inventar URLs.** Quando uma fonte for encontrada: abrir a página, confirmar que o documento existe, verificar ano/edição/tipo, registrar URL e origem. Se não encontrar: marcar `NOT_FOUND` — nunca assumir que existe.

## 30. Objetivo final

Responder empiricamente: *"Dado todo o histórico disponível do CACD até determinado ano, quais temas teriam sido previstos para o concurso seguinte?"* — e comparar com o que realmente aconteceu:

```
modelo → previsões → prova real → acertos → erros → métricas
```

Priorizar reprodutibilidade, validação temporal, transparência e análise estatística — não uma lista de "possíveis questões".
