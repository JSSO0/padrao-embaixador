# Pipeline de dados

Scripts que geram e mantêm `data/processed/questions.parquet`. Todos rodam a
partir da raiz do repositório. A **ordem importa**.

Scripts usados uma única vez (OCR de um ano, resgate de uma questão) ficam em
`ferramentas/extracoes_pontuais/`; scripts de inspeção ficam em
`ferramentas/diagnostico/`. Nenhum dos dois faz parte da execução normal.

## Ordem de execução

| # | Passo | Comando | Marco |
|---|---|---|---|
| 1 | Baixar PDFs | `python scraper/download.py` | M0 |
| 2 | Extrair texto dos PDFs | `python parser/extract_text.py` | M0 |
| 3 | Segmentar questões (parsers por banca) | `python parser/build_dataset.py` | M1 |
| 4 | Extrair objetivas 2025/2026 | `python pipeline/extract_cebraspe_linear.py` | M1 |
| 5 | Extrair discursivas | `python pipeline/extract_discursivas.py` | Discursivas |
| 6 | Converter transcrições `.md` legadas | `python pipeline/convert_md_transcripts.py` | M1 |
| 7 | Importar transcrições manuais (**sempre antes do gabarito**: zera `answer` dos manuais) | `python parser/import_manual.py` | M1 |
| 8 | Remover linhas `rules` substituídas por `manual` | `python pipeline/clean_dup_rules.py` | M1 |
| 9 | Aplicar gabaritos | `python pipeline/extract_gabaritos.py` | M1 |
| 10 | Canonizar disciplinas (8 grupos) | `python pipeline/canon_disc.py` | M1 |
| 11 | Aplicar taxonomia do YAML | `python pipeline/build_taxonomy.py` | M2 |
| 12 | Relatório por ano | `python pipeline/overview.py` | — |
| 13 | Backtest (baselines por disciplina / por tema / TF-IDF) | `python evaluation/backtest.py` · `backtest_temas.py` · `backtest_tfidf.py` | M3 |
| 14 | Relatório e gráfico do backtest | `python evaluation/report.py` · `python evaluation/grafico.py` | M3 |

Saídas do backtest vão para `data/resultados/`; o gráfico vai para `docs/assets/`.

> A taxonomia vem de `data/metadata/taxonomia.yaml` (regras fixas, a priori —
> sem vazamento temporal). O antigo `refine_taxonomy_tfidf.py` (TF-IDF sobre
> o corpus inteiro) foi removido do fluxo. Teste de não-vazamento:
> `tests/test_taxonomia_nao_vazamento.py`.

### Passo 9 — detalhes

```bash
python pipeline/extract_gabaritos.py            # default: todos os anos (2003-2026, exceto 2021)
python pipeline/extract_gabaritos.py --year 2015 --debug   # run parcial (só o ano indicado)
```

> O default processa **todos os anos** e o cache (`data/processed/gabaritos.json`)
> preserva os anos fora do run: nem um run completo nem um parcial deixam o
> cache incompleto (correção do incidente de 23/10, task M1.1).

## Validação e QA

| Script | Função |
|---|---|
| `parser/qa.py --n 5` | Amostra aleatória para revisão |
| `pipeline/qa_ampliado.py` | Gera as 50 questões da validação manual (`data/processed/qa_sample/`) |
| `pipeline/qa_validate.py` | Validação sistemática do parquet |
| `pipeline/qa_jsonl.py` | Inspeção dos JSONL de transcrição manual |
| `pipeline/rescue_answers.py` | Resgata respostas de `rules` antigas do parquet no `HEAD` (uso em recuperação) |

## Armadilhas conhecidas (Windows/PowerShell)

- **NUNCA** usar `python -c` inline com acentos/aspas complexas — PowerShell
  corrompe. Usar arquivos de script sempre.
- `&&` não existe no PowerShell 5 — usar `;`
- Primeiro commit pode falhar com "unable to write new index file" (lock
  transitório OneDrive/antivírus) — re-executar resolve

## Formatos de gabarito suportados (`extract_gabaritos.py`)

1. Grade estreita "Questão N + 4 letras" (2014-2018, 2024)
2. Grade larga cursocacd mojibake "QUESTǟO" (2019-2023), `#`/X = anulada
3. Pares Item/Gabarito (2024-2026 cebraspe)
4. Grade 30 itens × 30 letras (2004; ☼ = anulada)
5. Tabela "Questão | item 1..4" (2009-2013; A-D = múltipla escolha)
6. Grade transposta TPS (2003-2008): pareamento por intervalo de coluna x

## Regras de negócio do apply (`extract_gabaritos.py`)

- Anuladas (X/#/☼): `answer = null` + note "item anulado no gabarito definitivo"
- CACD_2003 → gabarito de 2003 (exceção por contest_id; year=2004 nas linhas)
- CACD_2004 → item = (qn-1)*5 + itn (agrupado) ou item = qn (achatado)
- itn=null + alternatives (era TPS) → chave (qn, 0) = múltipla escolha
- itn=null + year>=2024 + certo_errado → chave (qn, 1) (formato C)
- Só preenche/override onde confia; linha sem chave confiável fica sem resposta

## Arquivos de dados

| Pasta | Conteúdo |
|---|---|
| `data/raw/` | PDFs originais + `download_manifest.csv` (SHA-256, URL, bytes, data) |
| `data/metadata/` | Catálogos de fontes |
| `data/processed/` | Datasets: `questions.parquet`, `answer_keys.parquet`, `gabaritos.json`, relatórios de extração, `text/` |
| `data/processed/qa_sample/` | Amostras para validação manual |
| `data/resultados/` | Saídas do backtest (`backtest_*.json`, `backtest_summary.md`) |
