# Post Dia 19 — 09/11/2026 (segunda)

## Metadados

| Campo | Valor |
|---|---|
| Dia | 19 |
| Data | 2026-11-09 (segunda) |
| Projeto | CACD Forecast AI (padrao-embaixador) |
| Território | LinkedIn + X (thread) + Instagram (carrossel) |
| Formato | Gráfico + métrica (post de método: "como vou medir") |
| CTA | Ler o repo |
| Status | **depende de mudança** — o backtest ainda não existe; post é "como vou medir" |

## Post LinkedIn

4.677 respostas extraídas de 23 edições do CACD. Quantas métricas de
previsão publiquei até hoje? Nenhuma.

O gráfico que acompanha este post não tem resultado — tem método. Antes
de rodar qualquer modelo, eu preciso provar que sei medir:

**Precision@K com backtesting temporal.** Para cada ano X entre 2017 e
2025, treino só com as provas de 2006 a X e testo em X+1. São 9 folds
expansivos. A métrica: dos K temas que o sistema teria sugerido para
X+1, quantos realmente apareceram.

Três regras invioláveis:

1. Anti-leakage — a taxonomia e a classificação são refitadas a cada
   fold, usando apenas provas anteriores àquela edição.
2. Baselines estatísticos antes de qualquer IA. Se o Precision@K do
   modelo não bater o do padrão histórico de frequências, o modelo
   não vale nada.
3. Cada item do dataset tem origem registrada — sem URL verificada, o
   item é marcado NOT_FOUND.

O que isso NÃO prova: que uma questão literal pode ser prevista. E
Precision@K alto pode ser só o padrão de sempre — por isso o baseline
vem primeiro.

Hoje o repo tem 5.020 itens da 1ª fase e 4.677 com gabarito oficial
(93,2%). O que falta para o gráfico ficar real: taxonomia temática,
módulo de avaliação e os 4 baselines. Zero testes escritos até agora.

Acompanho o método, não o resultado. Você mediria antes de acreditar?

Repo: https://github.com/JSSO0/padrao-embaixador

## Thread X

1/4.677 respostas extraídas de 23 edições do CACD. Métricas de previsão publicadas: zero. E é isso que vou mudar — medindo, não adivinhando. 🧪
2/ O método: backtesting temporal com janela expansiva. Treino 2006–X, teste X+1, para X de 2017 a 2025. Nove folds. Nenhum split aleatório.
3/ A métrica: Precision@K — dos K temas sugeridos para X+1, quantos caíram. Anti-leakage: taxonomia refitada a cada fold, só com provas ≤ X.
4/ O que isso NÃO prova: a questão literal. E Precision@K alto pode ser só base rate — por isso os 4 baselines estatísticos vêm antes de qualquer modelo.
5/ Estado real hoje: 5.020 itens da 1ª fase, 4.677 com gabarito (93,2%), 0 testes escritos, 0 gráficos. O post do resultado só sai quando os 9 folds rodarem.
Repo: https://github.com/JSSO0/padrao-embaixador

## Carrossel Instagram

**Slide 1**
- Título: 24 anos de prova, zero previsões
- Corpo: Extraí 4.677 respostas de 23 edições do CACD. Nenhuma métrica publicada ainda. E isso é proposital.
- Texto de imagem: fundo escuro, "4.677" em destaque
- Alt text: Cartão escuro com o número 4.677 em destaque e a frase "23 edições do CACD catalogadas".

**Slide 2**
- Título: O que o sistema é
- Corpo: Um estudo com backtesting temporal: treino 2006–X, teste X+1. Não adivinho questão literal.
- Texto de imagem: método > resultado
- Alt text: Frase sobre backtesting temporal com janela expansiva.

**Slide 3**
- Título: A métrica
- Corpo: Precision@K — dos K temas sugeridos para a edição X+1, quantos de fato caíram. Medido em 9 folds (X = 2017 a 2025).
- Texto de imagem: Precision@K
- Alt text: Esquema de treino até o ano X e teste no ano X+1.

**Slide 4**
- Título: Anti-leakage
- Corpo: A taxonomia é refitada a cada fold, usando só provas anteriores à edição testada. Sem isso, qualquer gráfico é propaganda.
- Texto de imagem: sem vazamento de futuro
- Alt text: Diagrama com separação entre dados de treino e dados de teste.

**Slide 5**
- Título: O que isso não prova
- Corpo: Não prova que a questão literal pode ser adivinhada. Precision@K alto pode ser só o padrão histórico.
- Texto de imagem: o que não é provado
- Alt text: Texto explicando os limites da métrica.

**Slide 6**
- Título: O estado real
- Corpo: 5.020 itens, 4.677 com gabarito, 0 testes escritos. O gráfico de resultados não existe ainda — e é esse o ponto.
- Texto de imagem: 0 testes
- Alt text: Número zero em destaque representando testes ainda não escritos.

**Slide 7**
- Título: Próximo passo
- Corpo: Taxonomia, 9 folds, 4 baselines. Quando rodar, publico gráfico, erro e o que falhou.
- Texto de imagem: método antes de resultado
- Alt text: Frase sobre medir antes de prometer.

## Hashtags

#CACD #DataScience #Backtesting #NLP #MétodoCientífico #ConcursosPúblicos #Pesquisa #AprendizadoDeMáquina

## Assets

1. **Gráfico de método (principal)** — 1.200×1.500 px, fundo escuro. Mostrar o esquema dos 9 folds: barras "treino 2006–X" crescendo + "teste X+1". Sem números de resultado.
2. **Print do terminal** com a contagem do parquet (`python -c "..."` mostrando 5.020 itens / 4.677 com gabarito) — terminal sem caminho de usuário visível.
3. **Screenshot do diretório `evaluation/` vazio** — evidência da honestidade ("a medir").

## Fatos e números

| Número | Fonte |
|---|---|
| 5.487 registros | `data/processed/questions.parquet` (commit 3dd8214 + reparo de pipeline de 22/10) |
| 5.020 itens da 1ª fase, 2003-2026 | saída do `python -c` sobre o parquet (22/10/2026) |
| 4.677 itens com gabarito (93,2%) | mesma saída, após re-execução da cadeia de gabaritos |
| 23 edições (2003-2026, sem 2021) | commit 49c8d05 "corpus completo v0.1 (23 edicoes 2003-2026)" |
| 9 folds (X = 2017 a 2025) | `docs/plano-mestre.md` §1 "Backtesting temporal obrigatório" |
| 4 baselines estatísticos | `docs/plano-mestre.md` §1 "Baselines antes de IA" |
| 0 testes / 0 avaliação | `tests/` e `evaluation/` contêm apenas `.gitkeep` (verificação de diretório) |

## Checklist

- [x] Sem credenciais, tokens, chaves, URLs internas, dados de usuário
- [x] Sem promessa de resultado ("vai prever") — verbo no futuro/método
- [x] Sem repetição dos 2 posts já publicados
- [x] Métrica (Precision@K) + "o que isso NÃO prova" presentes
- [x] 1 CTA (ler o repo), ≤ 3 emojis, sem jargão decorativo

## Pré-requisitos

1. Taxonomia temática dos itens (não existe em `data/metadata/`) — prereq para o Precision@K.
2. Módulo `evaluation/` com a métrica implementada e 9 folds rodando.
3. 4 baselines estatísticos implementados e comparados.
4. Testes mínimos (`tests/` está vazio).
5. Gráfico de folds gerado a partir do relatório real (asset do post).
