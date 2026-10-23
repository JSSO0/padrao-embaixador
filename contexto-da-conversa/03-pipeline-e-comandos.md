# Pipeline, scripts e comandos

## Scripts de produção (9)

| Script | Função |
|---|---|
| `scripts/extract_cebraspe_linear.py` | Provas objetivas 2025/2026 do texto linear dos PDFs oficiais (240+240 itens) |
| `scripts/extract_gabaritos.py` | Gabaritos oficiais (6 formatos, 2003-2026) → cache `data/processed/gabaritos.json` + apply no parquet |
| `scripts/extract_discursivas.py` | Discursivas 2ª fase (2017/2018/2024-2026, Cebraspe) + 3ª fase (2019-2023, por disciplina) |
| `scripts/extract_objetivas_2015_2018.py` | Extrator de colunas da era 2015-2023 (NÃO rodar para 2025/2026) |
| `scripts/convert_md_transcripts.py` | Converte transcrições .md legadas para JSONL padronizado |
| `parser/import_manual.py` | Importa JSONLs manuais → questions.parquet (manual ganha de rules) |
| `scripts/clean_dup_rules.py` | Remove rules de prova objetiva substituídas por manual |
| `scripts/rescue_answers.py` | Resgata respostas das rules antigas do HEAD parquet |
| `scripts/overview.py` | Regenera `docs/overview-questoes.md` |
| `scripts/qa_validate.py` / `qa_jsonl.py` | Validação sistemática / inspeção de JSONL |

## Ordem de execução (CRÍTICA)

```bash
# 1. extração (quando houver PDF novo)
python scripts/extract_cebraspe_linear.py            # 2025/2026
python scripts/extract_discursivas.py                # 2a/3a fase

# 2. import SEMPRE antes do gabarito (o import zera answer dos manuais!)
python parser/import_manual.py

# 3. limpeza
python scripts/clean_dup_rules.py

# 4. gabaritos — SEMPRE com anos explícitos (o default sem --year é 2015-2026
#    e regravaria o cache sem 2003-2014!)
python scripts/extract_gabaritos.py --year 2003 --year 2004 --year 2005 \
  --year 2006 --year 2007 --year 2008 --year 2009 --year 2010 --year 2011 \
  --year 2012 --year 2013 --year 2014 --year 2015 --year 2016 --year 2017 \
  --year 2018 --year 2019 --year 2020 --year 2022 --year 2023 --year 2024 \
  --year 2025 --year 2026

# 5. relatório
python scripts/overview.py
```

**Pendência de robustez acordada na conversa**: o loop de anos deveria ser
o default do script (o default atual ainda é `range(2015, 2027)` — a
correção definitiva exige trocar `years = args.year or [...]`).

## Armadilhas conhecidas (Windows/PowerShell)

- **NUNCA** usar `python -c` inline com acentos/aspas complexas — PowerShell
  corrompe. Usar arquivos de script sempre.
- `&&` não existe no PowerShell — usar `;`
- Primeiro commit pode falhar com "unable to write new index file" (lock
  transitório OneDrive/antivírus) — re-executar resolve

## Formatos de gabarito suportados (extract_gabaritos.py)

1. Grade estreita "Questão N + 4 letras" (2014-2018, 2024)
2. Grade larga cursocacd mojibake "QUESTǟO" (2019-2023), `#`/X = anulada
3. Pares Item/Gabarito (2024-2026 cebraspe)
4. Grade 30 itens × 30 letras (2004; ☼ = anulada)
5. Tabela "Questão | item 1..4" (2009-2013; A-D = múltipla escolha)
6. Grade transposta TPS (2003-2008): pareamento por intervalo de coluna x

## Regras de negócio do apply (extract_gabaritos.py)

- Anuladas (X/#/☼): `answer = null` + note "item anulado no gabarito definitivo"
- CACD_2003 → gabarito de 2003 (exceção por contest_id; year=2004 nas linhas)
- CACD_2004 → item = (qn-1)*5 + itn (agrupado) ou item = qn (achatado)
- itn=null + alternatives (era TPS) → chave (qn, 0) = múltipla escolha
- itn=null + year>=2024 + certo_errado → chave (qn, 1) (formato C)
- Só preenche/override onde confia; linha sem chave confiável fica sem resposta

## Dataset no repo

- 460 PDFs · 463 entradas em `data/raw/download_manifest.csv` (SHA-256, URL,
  bytes, data — a diferença de 3 = zips não extraídos)
- `data/processed/`: questions.parquet, answer_keys.parquet, extraction_report.csv,
  text_metrics.csv, gabaritos.json, manual_import_report.csv
- `evaluation/` e `tests/` vazios (só .gitkeep) — 0 testes, 0 backtest
- `data/metadata/`: apenas catálogos de fontes (sem taxonomia temática)

## Conteúdo (plano de 31 dias)

- `conteudo/2026-11-09-backtesting-precision-k.md` (dia 19 — "como vou medir";
  o backtest não existe — evaluation/ vazio)
- `conteudo/2026-11-20-pesquisa-reprodutivel-manifesto.md` (dia 30 — pronto;
  463 entradas com SHA-256 verificadas)
- `conteudo/INDEX.md`
- Voz "Prova de Método": todo post tem métrica + frase do que NÃO prova;
  post de resultado só após os 9 folds rodarem

## Commits

- `3dd8214` 2026-10-19 — feat(data): completa gabaritos e extrai discursivas 2a/3a fase (push feito)
- Reparo de 23/10/2026 (extract_gabaritos.py: default de anos + fallback itn=1
  para formato C) — **ainda não commitado** até 23/10
