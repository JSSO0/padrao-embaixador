# Contexto da conversa — padrao-embaixador

**Data:** 2025-10-23  
**Repo:** `C:\Users\sjoel\Desktop\Projetos\padrao-embaixador` (`main`, https://github.com/JSSO0/padrao-embaixador.git)  
**Estado:** privado (~350MB; PDFs versionados)

## Objetivo
Deixar o repo público-pronto (README/banner/licenças) e avançar Etapa 5: extrair todas as provas/gabaritos, resolvendo ambiguidade multi-caderno (Cebraspe) e integrando transcrições manuais.

## Feito nesta sessão
- **PDFs mantidos:** revertido destrackeamento de `data/raw/` e `data/processed/text/` (no `.gitignore`); PDFs permanecem versionados. Licenças: `LICENSE` (MIT), `LICENSE-DATA.md` (CC-BY-4.0). README/banner atualizados.
- **Parser/merge:** `parser/document_loader.py` adiciona `words_per_page`; `parser/answer_merger.py` parseia matriz multi-caderno Cebraspe (`parse_cebraspe_matrix`/`extract_answer_keys`); `parser/build_dataset.py` unifica gabaritos (prioriza `definitivo`, guarda todos os cadernos), usa caderno 0 no merge. `parser/schemas.py` (pandera), `parser/qa.py` (amostragem p/manual caderno). 
- **Dataset atual:** `data/processed/questions.parquet` **3236** linhas. `answer_keys.parquet` com gabaritos multi-caderno. Cobertura: IADES 90–92%, 2025–26 100%, 2024 90%, 2003–2018 ainda com lacunas.
- **Transcrições manuais:** criadas em `data/raw/CACD_2003–2007/cursocacd/` (6 arquivos: `prova2003.json`, `prova 2004.json`, `prova 2005.json`, `prova 2006 - 1.txt`, `prova 2006-2.json`, `prova 2007 - 1.json`).
- **Importador:** `parser/import_manual.py` — lê JSON/JSONL concatenado, **repara aspas não escapadas automaticamente**, normaliza tipo/idioma, resolve `source_file` (basename → caminho real), deriva contest_id do caminho do PDF, valida Pydantic, calcula `question_id`. Manual **substitui rules** do mesmo documento. 
- **Importado:** 2003–2007 → **638 questões manuais**. 2003/2004/2005 100% manual; 2006 objetivo 100% manual (restam discursivas em rules); 2007 objetivo 78 manual (restam outras docs em rules). Relatório: `data/processed/manual_import_report.csv`.

## Pendências / Incertos
- **Ambiguidade multi-caderno:** 2013–2018, 2024 (multi-caderno) sem ID de caderno na prova. Resolver via `python parser/qa.py --only-multi` (amostragem manual).
- **Lacunas legado:** objetivas 2008–2018 e 2024 com parsing fraco/truncado; discursivas largamente mal rotuladas em regras.
- **2003 contest_id:** `prova2003.json` tinha `contest_id: CACD_2004` mas PDF está em `CACD_2003` — importador usou caminho (2003). Confirmar se correto.
- **2007 reparado:** auto-reparado por aspas internas não escapadas (funcionou). Melhor exigir JSONL válido e aspas escapadas na próxima geração.

## Próximos passos (propostos)
1. **Atualizar README** com status (2003–2007 manuais, total 3236) se desejado.
2. **Continuar transcrições** 2008–2018 + 2024 geradas pela IA seguindo formato corrigido.
3. **Resolver cadernos multi-caderno** com amostragem `qa.py --only-multi` e popular resposta correta.
4. **Avançar Etapa 2**: `data/raw/contest_registry.csv` e iniciar baselines (backtest anti-leakage).

## Arquivos-chave
- `parser/import_manual.py`, `parser/answer_merger.py`, `parser/build_dataset.py`, `parser/document_loader.py`, `parser/qa.py`
- `data/processed/questions.parquet` (3236), `data/processed/answer_keys.parquet`, `data/processed/manual_import_report.csv`
- `data/raw/CACD_2003–2007/cursocacd/*`, `README.md`, `LICENSE`, `LICENSE-DATA.md`
