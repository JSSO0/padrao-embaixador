# Etapa 1 — Relatório de Catalogação das Fontes (CACD)

Data: 2026-10-06 · Status: catálogo inicial concluído (verificação por fetch real; nenhuma URL inventada)

## 1. Fontes mapeadas

| Fonte | URL | Status | Papel no projeto |
|---|---|---|---|
| MRE/IrBr — índice de editais | https://www.gov.br/mre/pt-br/instituto-rio-branco/carreira-diplomatica/editais-cacd-1 | ✅ verificada | Editais + resultados oficiais (2003–2025; sem 2026 e sem 2007) |
| MRE/IrBr — arquivo de provas antigas | https://www.gov.br/mre/pt-br/instituto-rio-branco/arquivos/cacd/provas-antigas-cacd | ⚠️ página existe mas **vazia publicamente** | Era a fonte oficial esperada para 2003–2016 |
| Cebraspe | https://www.cebraspe.org.br/concursos/irbr_XX_diplomacia | ✅ só para 2017, 2018, 2024, 2025, 2026 | Provas + gabaritos + padrões oficiais |
| Curso CACD | https://www.cursocacd.com/conteudo | ✅ verificada | Provas por disciplina/tipo, gabaritos, padrões e guias (2003–2026) |
| Nabuco CACD | https://nabucocacd.com.br/provas-antigas/ | ✅ verificada | Pacotes por edição (SharePoint), 2003–2026 |
| Lutz CACD | https://lutzcacd.com.br/todas-as-provas-anteriores-cacd/ | ✅ verificada | Hub agregador que aponta para as fontes oficiais |

**Detalhe técnico importante (Cebraspe):** o site é uma SPA React; o conteúdo vem da API oficial `https://apis.cebraspe.org.br/cebraspe/eventos/<slug>` e os PDFs do CDN `https://cdn.cebraspe.org.br/concursos/<EVENTO>/arquivos/`. O scraper deve consumir a **API**, não o HTML.

## 2. Edições encontradas (24 edições, 2003–2026)

`CACD_2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, CACD_2020_2021, 2022, 2023, 2024, 2025, 2026`

Disponibilidade de provas (não só editais):

| Período | Provas objetivas | Gabaritos | Discursivas | Padrões de resposta | Fonte viva principal |
|---|---|---|---|---|---|
| 2024–2026 | ✅ Cebraspe | ✅ definitivo (preliminar não publicado) | ✅ 8 provas/ano | ✅ 8–9 arquivos/ano | Cebraspe (API) |
| 2017–2018 | ✅ Cebraspe | ✅ preliminar (2018) + definitivo | ✅ 2ª e 3ª fases | ✅ por questão (2017: 48 arquivos) | Cebraspe (API) |
| 2019–2023 | ❌ oficial | ❌ oficial | ❌ oficial | ❌ oficial | **Secundárias** (Curso CACD, Nabuco) |
| 2003–2016 | ❌ (arquivo MRE vazio) | ❌ | ❌ | ❌ (padrões só existem desde 2017) | **Secundárias** (Curso CACD por disciplina, Nabuco) |

Editais oficiais: completos para quase todas as edições no índice do MRE (2003 tem 11 PDFs; 2019 tem 17; 2022/2023 com editais de resultado verificados). Exceções: **CACD_2007 sem página no MRE** e **CACD_2012 com página vazia**.

## 3. Lacunas encontradas (NOT_FOUND)

1. **Arquivo oficial de provas antigas do MRE está vazio** para usuário anônimo — nenhum PDF público de 2003–2016. Consequência: o corpus antigo dependerá de fontes secundárias (regra de confiabilidade: marcar `secondary_repository` e nunca tratar como oficial).
2. **Cebraspe perdeu as edições 2019, 2020/21, 2022 e 2023** (API retorna 204; listagem de concursos encerrados salta de 2018 para 2024). As provas dessas edições só existem hoje nas fontes secundárias.
3. **Gabaritos preliminares não estão mais listados** nas páginas atuais de 2024–2026 (só definitivos + justificativas de alteração). Para 2018 existem os preliminares. Regra "guardar ambos" ficará limitada ao que sobreviveu.
4. **CACD_2007**: sem página no MRE, sem resultado em buscas web. Fonte conhecida: apenas secundária (Nabuco/Curso CACD). Confirmar se o concurso da edição 2007 ocorreu e em que formato (possível regime diferente).
5. **Padrões de resposta oficiais por questão existem somente a partir de 2017** (2017: 48 arquivos por questão; 2018–2026: por disciplina). Antes disso, o "padrão" é a melhor resposta dos aprovados (guias) — não oficial.
6. Domínio legado `security.cespe.unb.br` (consulta individual de gabaritos 2018) está com TLS expirado — inacessível.

## 4. Estruturas de prova detectadas (para `exam_regime`)

- **2003–2005:** 1 prova objetiva única (sem 2ª objetiva de tarde) + discursivas por disciplina (sem Esp/Fra em 2003 e 2004).
- **2006–2018:** 2 provas objetivas (manhã/tarde) + discursivas em 2ª/3ª fases separadas (2017: 2ª fase PT/EN; 3ª fase HB/GEO/PI/ECO/DIR/ESF).
- **2024–2026:** 2 provas objetivas + segunda fase com as 8 provas escritas unificadas.
- Confirmar com os editais de cada ano (coluna `exam_regime` do dataset; edital por edital na Etapa 2).

## 5. Arquivos entregues

- `data/metadata/source_catalog.csv` — catálogo oficial granular (URLs verificadas com data)
- `data/metadata/nabuco_sharepoint.csv` — 23 pastas por edição + drive completo
- `data/metadata/curso_cacd.csv` — índice + edições 2019–2026 (PDFs por tipo/disciplina)
- ⚠️ Os hashes de URL do Curso CACD (Wix) foram transcritos da página; na Etapa 3 (download) validar cada URL com HTTP HEAD e re-extrair do site ao vivo qualquer 404.

## 6. Próximos passos (Etapas 2–4)

1. **Etapa 2** — consolidar tabela por edição: nº de vagas, disciplinas, pesos, nº de questões (dos editais oficiais já catalogados).
2. **Etapa 3** — scraper (`scraper/`): baixar da API do Cebraspe (2017, 2018, 2024–2026), gov.br (editais) e das secundárias (2019–2023 + 2003–2016), com `source_type` e checksum SHA-256; validação dos PDFs do Curso CACD.
3. **Etapa 4** — extração de texto (PyMuPDF) com métrica de qualidade ≥90% das questões detectadas; OCR previsto para provas antigas escaneadas.
4. ~~Investigar via Wayback Machine as edições Cebraspe 2019–2023~~ — **verificado em 06/10/2026**, resultado na seção 7.

## 7. Wayback Machine — resultado da verificação (06/10/2026)

Consulta à API CDX (`web.archive.org/cdx`) por padrões de URL nos domínios `cebraspe.org.br`, `cespe.unb.br` e `security.cespe.unb.br`.

### O que foi recuperado (oficial, arquivado)

| Edição | Arquivado na Wayback | Destaques |
|---|---|---|
| **2013** | ✅ completo | Objetivas 1 e 2, gabaritos preliminar + definitivo, 7 discursivas por disciplina, **Guia de Estudos 2013**, editais, justificativas |
| **2014** | ✅ | Objetivas, gabaritos definitivos, 7 discursivas (incl. GPI combinada Geografia+PI), editais |
| **2015** | ✅ | Objetivas (4 variantes), gabaritos definitivos, discursiva 2ª fase + 6 provas da 3ª fase, editais |
| **2016** | ✅ | Objetivas, gabaritos **preliminares** + definitivos, discursivas das fases 2 e 3, editais |
| **2017** | ✅ | **Gabaritos preliminares** (perdidos no site atual), padrões por questão, editais |
| **2018** | ✅ | **Cadernos 417_IRBR_DISC_001–006 da 3ª fase** (ausentes do site atual), discursivas 2ª fase, editais |

→ Nas edições 2013–2016, onde o site oficial atual não tem **nada** de provas, agora temos fonte **oficial arquivada** (`official_cebraspe_archive`), bem melhor que depender só de cursinhos.

### O que NÃO foi encontrado

- **2019, 2020/21, 2022 e 2023: nenhuma captura útil.** No domínio novo não há nenhuma página/página-arquivo desses slugs; no antigo, só um 404 de abril/2019. As páginas dessas edições nunca foram capturadas (ou foram capturadas depois da remoção). **Ficam oficialmente NOT_FOUND em fonte oficial; corpus dependerá das secundárias.**
- **2005–2012: nada de DIPLOMACIA no domínio CESPE** (só os concursos de *Bolsa-Prêmio* IRBR_12/13_BOLSA, que são outro certame). Edições antigas continuam dependendo de fontes secundárias.
- Páginas individuais de consulta (`.asp`) do domínio `security.cespe.unb.br` quase não foram capturadas.

### Observações

- URLs arquivadas usam o formato `https://web.archive.org/web/<timestamp>/<url_original>`; todas as linhas do catálogo `data/metadata/wayback_archive.csv` foram confirmadas na CDX com status HTTP 200 na captura, mas o download precisa ser validado na Etapa 3.
- Registrado um total de ~60 documentos arquivados relevantes em `data/metadata/wayback_archive.csv` (seleção das provas/gabaritos/padrões; arquivos administrativos como relações de isenção foram ignorados).
- Migalha: a CDX de `cespe.unb.br/concursos/irbr*` atinge ~456 URLs colapsadas — vale varredura completa do scraper para resgatar editais adicionais (2013–2018) quando baixarmos os arquivos.

## 8. Fontes secundárias — varredura complementar (06/10/2026)

Objetivo: cobrir as lacunas (2019–2023 e 2003–2012) antes da Etapa 3. Três agentes verificaram bancos de questões, agregadores e acervos comunitários. **Resultado: 100% das edições ficaram com pelo menos uma fonte.**

### Novas fontes catalogadas

| Fonte | URL | Conteúdo | Cobre |
|---|---|---|---|
| **Archive.org** — item "Provas Diplomata CESPE 2003 a 2016" | `archive.org/download/DiplomataCESPE2014/` | 1 ZIP por edição (2003–2012 confirmados; 4–11 arquivos cada) | 2003–2012 (+2013–2016) |
| **PCI Concursos** | `pciconcursos.com.br/provas/diplomata/` | PDFs por edição, sem login (download com captcha) | 2003–2016, 2018, 2019, 2023–2026 |
| **Qconcursos** | `qconcursos.com/questoes-de-concursos/provas?by_institute[]=58` | Todas as edições 2003–2026 como questões online com gabarito; PDFs diretos em `arquivos.qconcursos.com` | 2003–2026 completo |
| **Gabarite** | `gabarite.com.br/provas-de-concursos/...` | Prova + gabarito por turno | 2019, 2020/21, 2022 |
| **Clipping CACD** | blob storage | Prova objetiva 2019 tarde (PDF direto) | 2019 |
| **Curso CACD (completo)** | `cursocacd.com/conteudo` | 279 PDFs extraídos da página: objetivas 1/2, gabaritos, 8 discursivas por disciplina, padrões e guias | 2003–2026 completo |

### Achados estruturais importantes

1. **Banca mudou**: IADES foi a banca do CACD **2019, 2020/21, 2022 e 2023** — não o Cebraspe. Por isso essas edições nunca estiveram no portal do Cebraspe: a remoção não foi um apagamento, foi troca de banca. Isso afeta a análise de `exam_regime` (as provas de 2019–2023 são da IADES, com formato certo/errado em blocos).
2. **2010 e 2011**: a 1ª fase do CACD foi a prova da **Bolsa-prêmio de Vocação para a Diplomacia** (Qconcursos cataloga assim). Impacto no regime de prova.
3. **CACD 2007 existiu** (2 etapas: PAPA e ECHO segundo o Qconcursos) — a ausência no site do MRE é apenas uma lacuna de publicação.

### Validação

- Curso CACD: 279 links extraídos automaticamente da página viva → `data/metadata/curso_cacd_full.csv` (substitui o `curso_cacd.csv` parcial anterior); amostra de 15 URLs validadas com HTTP HEAD: **15/15 OK (application/pdf)**.
- Qconcursos/PCI/Gabarite/Archive.org: URLs confirmadas por fetch (detalhes em `data/metadata/secondary_sources.csv`).

### Matriz final de cobertura de provas (todas as edições)

| Edição | Oficial viva | Oficial arquivada (Wayback) | Secundária (PDF) | Status final |
|---|---|---|---|---|
| 2003–2012 | ❌ | ❌ | ✅ Archive.org + PCI + Qconcursos + Curso CACD + Nabuco | COBERTA |
| 2013–2016 | ❌ | ✅ completa | ✅ redundante | COBERTA (oficial) |
| 2017–2018 | ✅ Cebraspe | ✅ complementos | ✅ redundante | COBERTA (oficial) |
| 2019–2023 | ❌ (banca IADES) | ❌ | ✅ Curso CACD + Gabarite + Qconcursos + PCI | COBERTA (secundária) |
| 2024–2026 | ✅ Cebraspe | n/a | ✅ redundante | COBERTA (oficial) |

**Conclusão da Etapa 1: nenhuma das 24 edições (2003–2026) ficou sem fonte de provas.** As únicas ressalvas: 2003–2012 e 2019–2023 são de origem secundária (nunca oficial), e para 2019–2023 é essencial anotar a banca IADES na coluna do dataset.
