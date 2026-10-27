<p align="center">
  <img src="docs/assets/banner.svg" alt="CACD Forecast AI" width="100%">
</p>

<p align="center">
  <img alt="status" src="https://img.shields.io/badge/status-pesquisa%20experimental-orange">
  <img alt="python" src="https://img.shields.io/badge/python-3.12%2B-blue">
  <img alt="licença" src="https://img.shields.io/badge/licen%C3%A7a-MIT-green">
  <img alt="dados" src="https://img.shields.io/badge/dados-CC%20BY%204.0-lightgrey">
  <img alt="PRs" src="https://img.shields.io/badge/PRs-bem--vindos-brightgreen">
</p>

# CACD Forecast AI

Sistema experimental que mede, com **backtesting temporal rigoroso**, até que ponto o
histórico das provas do **Concurso de Admissão à Carreira de Diplomata (CACD)** permite
prever a **distribuição temática** da próxima edição.

> **EN — TL;DR.** A research project on whether ~24 editions (2003–2026) of the Brazilian
> diplomat entrance exam are enough to predict the *topic distribution* of the next exam —
> not the literal question. Temporal backtesting, anti-leakage, statistical baselines first,
> then NLP/ML. The hard part, as always, is the data.

---

## O que é — e o que **não** é

| É | Não é |
|---|---|
| Um estudo científico com backtesting temporal (treino 2006–X, teste X+1) | Adivinhação da questão literal |
| Comparação honesta de baselines estatísticos, NLP e ML | "Guru" que promete tema garantido |
| Probabilidade estimada, sempre com incerteza | Certeza sobre a próxima prova |

Pergunta central: *dado todo o histórico até o ano X, quais temas teriam sido previstos
para X+1 — e o que realmente caiu?*

## Como funciona

1. **Dados** — catalogação de fontes, download dos PDFs, extração de texto e segmentação
   em questões (enunciado, alternativas, gabarito, disciplina), com proveniência completa.
2. **NLP** — embeddings multilíngues, similaridade e clustering para descobrir temas e
   recorrências reais entre edições.
3. **Modelos** — features estatísticas e 4 baselines primeiro; depois ML tabular
   (XGBoost/LightGBM), modelos de decisão probabilística (Laya) e ensemble.
4. **Backtesting** — folds expansivos 2017→2025, métricas de ranking (Precision@K, NDCG@K)
   por disciplina, relatório de previsões vs. prova real.

## Status

Objetivo, marcos, ganhos e glossário: **[docs/MAPA-DO-PROJETO.md](docs/MAPA-DO-PROJETO.md)**.

| Marco | Status |
|---|---|
| M0 — Corpus (catalogar, baixar, extrair texto) | ✅ |
| M1 — Dataset da 1ª fase (5.038 itens, 96,4% com gabarito) | 🔄 falta validação manual |
| M2 — Taxonomia de temas (~45 temas, 22% "geral") | 🔄 |
| M3 — Backtest honesto por tema (baseline Markov 0,79) | 🔄 corrigir vazamento do TF-IDF |
| M4 — Modelo que supera o baseline | ⬜ |
| M5 — Reprodutibilidade (manifest + testes) | ⬜ |
| M6 — Dashboard e simulados | ⬜ futuro |

### Qualidade do dataset por período

| Período | Banca / formato | Situação |
|---|---|---|
| 2019–2023 | IADES (certo/errado) | ✅ usável |
| 2024–2026 | Cebraspe (atual) | ✅ usável (2024 com textos-base a revisar) |
| 2003–2018 | CESPE / formatos antigos | ✅ transcrito; gabaritos 2005–2013 incompletos |

> Transparência: a maior dificuldade do projeto **não** é modelar — é **levantar os dados**.
> Bancas diferentes, provas em duas colunas, gabaritos com múltiplos cadernos e provas
> escaneadas tornam a extração a parte mais árdua. Isso está documentado, não escondido.

## Estrutura do repositório

```
├── data/
│   ├── raw/             # PDFs originais + manifest com SHA-256
│   ├── metadata/        # catálogos de fontes e proveniência
│   ├── processed/       # datasets (questions.parquet) e amostras de QA
│   └── resultados/      # saídas do backtest
├── scraper/             # download dos PDFs (M0)
├── parser/              # extração de texto e segmentação por banca (M0–M1)
├── pipeline/            # scripts de produção, em ordem — ver pipeline/README.md
├── evaluation/          # baselines, métricas @K e backtesting temporal (M3)
├── ferramentas/
│   ├── extracoes_pontuais/  # OCR e resgates feitos uma vez
│   └── diagnostico/         # inspeção e depuração
├── tests/               # pytest (M5)
└── docs/
    ├── MAPA-DO-PROJETO.md   # fonte única: objetivo, marcos, ganhos
    ├── referencia/          # requisitos, specs técnicas, formatos dos PDFs
    ├── relatorios/          # relatórios de corpus e cobertura
    └── historico/           # planos e contexto de sessões antigas
```

## Dados e proveniência

Prioridade de fonte: **MRE/IrBr > Cebraspe > Wayback (oficial arquivado) > repositórios secundários**.

- **Oficial vivo:** 2017–2018, 2024–2026 (Cebraspe)
- **Oficial arquivado:** 2013–2016 (Wayback, domínio legado)
- **Secundária:** 2003–2012 e 2019–2023 (banca IADES)

Cada questão do dataset carrega `source_type` e `source_url`. URL só é registrada após
verificação; ausências são `NOT_FOUND` explícitos. Os **PDFs originais ficam no repositório**
(`data/raw/`), para que qualquer pessoa possa conferir as fontes e reproduzir a extração —
cada arquivo é rastreável à sua URL de origem em `data/raw/download_manifest.csv`.

## Como reproduzir

```bash
pip install -r requirements.txt
python scraper/download.py --dry-run   # lista os jobs de download
python scraper/download.py             # baixa (retomável, com SHA-256)
python parser/extract_text.py          # extrai texto + métricas de qualidade
python parser/build_dataset.py         # gera questions.parquet + extraction_report
```

Pipeline completo (importação manual, gabaritos, taxonomia e backtest), na ordem certa:
[`pipeline/README.md`](pipeline/README.md).

## Princípios do projeto

- **Backtesting temporal obrigatório** — janela expansiva (treino 2006–X, teste X+1); nunca split aleatório.
- **Anti-leakage** — taxonomia, TF-IDF e embeddings re-fitados por fold; eventos filtrados por data < prova.
- **Métricas de ranking** — Precision@K, Recall@K, F1@K, MAP@K, NDCG@K (por disciplina também).
- **Baselines antes de IA** — nenhum modelo "inteligente" sem comparar com os 4 baselines estatísticos.
- **Transparência** — todo score é probabilidade estimada; conteúdo de LLM sempre marcado `GERADA POR IA`.
- **Proveniência total** — cada dado rastreável à fonte; provas de cursinho nunca tratadas como oficiais.

## Aviso

Projeto de **pesquisa e estudo**, sem qualquer vínculo com o Ministério das Relações
Exteriores, o Instituto Rio Branco, o Cebraspe ou o IADES. Não há garantia de acurácia.
Use por sua conta e risco.

## Licença

- **Código:** MIT — ver [`LICENSE`](LICENSE).
- **Dados derivados e documentação:** CC BY 4.0 — ver [`LICENSE-DATA.md`](LICENSE-DATA.md).

---

<p align="center"><sub>Feito com café, PyMuPDF e uma quantidade suspeita de paciência com PDFs.</sub></p>
