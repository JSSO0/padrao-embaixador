# Contexto da conversa — padrao-embaixador (CACD Forecast AI)

Gerado em 23/10/2026. Resume tudo o que foi feito e decidido nas sessões de
trabalho de 16/10/2026 a 22/10/2026 sobre o dataset de questões do CACD.

## Estado final consolidado (23/10/2026)

| Bloco | Situação |
|---|---|
| Parquet | `data/processed/questions.parquet` — **5.487 registros** (5.020 itens 1ª fase, 193 2ª fase, 274 3ª fase) |
| 1ª fase | 2003-2026 (23 edições), transcrição completa exceto **13 questões** (rascunhos de OCR prontos) |
| Gabarito 1ª fase | **4.677 itens (93,2%)** com gabarito oficial — ausências = anulados + itens que o PyMuPDF não extrai |
| 2ª fase | **193 itens** (2017/2024-2026 = 80 questões discursivas, 61 com padrão de resposta oficial) |
| 3ª fase | 274 linhas (legado das rules 2006-2018 + 48 questões estruturadas 2019-2023) |
| Commits | `3dd8214` (19/10) e anteriores — push feito para `JSSO0/padrao-embaixador` |
| Testes / avaliação | **0 testes** (`tests/` vazio), **0 backtest** (`evaluation/` vazio) |

## Arquivos desta pasta

- `01-sessoes-e-decisoes.md` — cronologia das sessões, bugs encontrados e decisões técnicas
- `02-estado-atual-e-lacunas.md` — números por ano, o que falta e as pendências priorizadas
- `03-pipeline-e-comandos.md` — scripts de produção, ordem de execução e armadilhas

## Pendências prioritárias (acordadas na conversa)

1. **OCR** das fontes 2003-2010 com encoding quebrado (fecha ~19 respostas de gabarito + 13 questões de transcrição + itens de múltipla escolha)
2. Re-transcrição do pacote **2004** (manual com linhas duplicadas itn=qn)
3. **2013**: 10 linhas de rules com numeração ruidosa (qn 174-227)
4. **2024**: vínculo de textos-base de algumas questões (LI com passagem de outra disciplina)
5. **2011/2014**: completar manuais (regras hoje, texto truncado)
6. **2ª fase**: padrões de 2017 faltantes (só 2 baixados), 2018 (formato redação), 2019-2023 parcialmente extraído (OCR)
7. **Backtesting** (plano mestre): taxonomia temática, módulo `evaluation/` com Precision@K (9 folds 2017-2025), 4 baselines — nada implementado ainda
8. Posts do plano de 31 dias: `conteudo/` gerado (dias 19 e 30) — dia 19 depende do backtest
