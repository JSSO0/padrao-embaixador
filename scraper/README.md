# Scraper — CACD Forecast AI

## `download.py` — Etapa 3 (coleta)

Baixa os PDFs catalogados em `data/metadata/` para `data/raw/<contest_id>/<familia>/`.

```bash
python scraper/download.py --dry-run   # lista jobs sem baixar
python scraper/download.py             # baixa (retomavel)
```

Características:
- **Fontes (familia)**: `cebraspe` (CDN oficial), `mre` (gov.br), `wayback` (archive oficial), `archive` (ZIPs 2003–2012), `cursocacd`, `qconcursos`, `clipping`, `secondary`
- **Validação**: magic bytes (`%PDF-` ou `PK` para ZIP) + HTTP 200; conteúdo inválido é descartado e registrado
- **Integridade**: SHA-256 por arquivo no manifest
- **Retomável**: `data/raw/download_manifest.csv` registra URL baixada com `ok=1`; re-execuções pulam o que já foi baixado
- **Rate limiting**: delay por fonte (0.4s Cebraspe até 1.5s Archive.org) + retry com backoff (3 tentativas)
- **Não baixa**: páginas com captcha (PCI), login (Qconcursos via página, SharePoint do Nabuco), páginas que só renderizam com JS

## Pendências conhecidas (não resolvidas por este downloader)

- Provas objetivas manhã 2019 (só tarde no blob do Clipping) → disponível via Curso CACD/Gabarite
- PDFs diretos de PCI/Gabarite (captcha) — se necessário, usar Playwright
- Pastas SharePoint do Nabuco — exigem navegação JS; alternativa: já cobrimos tudo via Curso CACD/Archive.org
- Editais 2016 e anteriores por página do MRE (não amostrados individualmente no catálogo)
