# Sessões e decisões — extração fiel da conversa

## Sessão 1 — 16/10/2026: 2025/2026 e gabaritos

### Problema inicial
O extrator de colunas (`extract_objetivas_2015_2018.py`) não entendia o formato
novo Cebraspe 2025/2026: **não existe mais "Questão N"** — itens numerados
continuamente (1-240), vinculados ao comando imediatamente anterior. A primeira
metade de cada caderno (itens 1-40 e 121-129) era engolida.

### Solução: extrator pelo TEXTO LINEAR
`scripts/extract_cebraspe_linear.py` — abandona a segmentação por colunas e
parseia o texto linear do PDF oficial (ordem nativa = ordem de leitura):
- Item = `<num> <comando>` (inline) ou `<num>` em linha própria (standalone,
  itens 1-9 do caderno), com o comando nas linhas seguintes até: linha em
  branco, próximo item, cabeçalho de página ("CEBRASPE ...") ou título de seção
- Textos-base/citações/instruções acumulam em buffer e vinculam ao **1º item
  do bloco** (contexto + comando no 1º item; só enunciado nos seguintes)
- Disciplina vem do título de seção em linha própria (via
  `parser/parsers/base.py::DISCIPLINE_NORMALIZE`)
- **Resultado: 240/240 itens em 2025 e 240/240 em 2026, zero lacunas**

### Gabaritos — 6 formatos decifrados (`scripts/extract_gabaritos.py`)
1. Grade estreita "Questão N + 4 letras" (2014-2018 wayback/cursocacd; 2024 cebraspe) — C/E/X
2. Grade larga cursocacd com mojibake "QUESTǟO" (2019-2023) + linha de posições 1-4; `#`/X = anulada
3. Pares Item/Gabarito (2024-2026 cebraspe) — pareamento por proximidade de x
4. Grade de 30 itens × 30 letras (2004; ☼ = anulada)
5. Tabela "Questão | item 1..4" (2009-2013; A-D = múltipla escolha)
6. Grade TRANSPOSTA da era TPS (2003-2008): colunas = questões, linhas = itens;
   pareamento por **intervalo de coluna x** (robusto a células mescladas)

### Bugs encontrados e corrigidos
| Bug | Causa | Fix |
|---|---|---|
| Linhas de gabarito descartadas inteiras | `RE_ANS` aceitava `x` minúsculo mas não `X` MAIÚSCULO (anuladas) — 2024 perdia q1-5, 2015/2016/2017/2018 perdiam blocos | classe `[CEeXx#$]` |
| 2024 com "Questão28" sem espaço | regex exigia `\s+` | `Quest\S{0,2}O\s*(\d{1,3})` |
| TPS aplicado errado | arquivos de 2005-2008 = TPS (pré-seleção) com grade transposta | skip por `TPS\|PRÉ-SELEÇÃO` + rejeição de linhas com >6 letras |
| CACD_2003 recebendo gabarito de 2004 | as linhas do CACD_2003 têm `year=2004` no parquet (TPS de out/2003 = pré-seleção do concurso 2004) | apply por `contest_id` com exceção: CACD_2003 → gabarito de 2003 |
| Multiplos-escolha sem chave | grid '+' não tinha chave (qn, itn) no dataset (itn=null) | cache `(qn, 0)` + apply nas linhas `itn=null` + `alternatives` |
| **2025/2026 sem gabarito após re-import** | fallback `itn=null → 1` foi removido; formato C usa chave (item, 1) | aplicar `itn=1` para year>=2024 question_type=certo_errado |
| **Cache regravado sem 2003-2014** | `main()` usava default `range(2015, 2027)` quando `--year` omitido | loop explícito 2003-2026 no `main()` |

### Fatos importantes descobertos
- **TPS (Teste de Pré-Seleção) ERA a prova objetiva de 2003-2008** — o próprio
  gabarito diz "QUESTÕES OBJETIVAS DO TPS (1.ª FASE)"
- **CACD_2003 = TPS de 25/10/2003 = pré-seleção do concurso 2004** — daí o
  `year=2004` nas linhas do CACD_2003 (correto semânticamente)
- As respostas resgatadas das rules (2019-2023) estavam **rotacionadas em 1
  posição** dentro da questão — o gabarito oficial corrigiu 564 respostas
- O import das discursivas (19/10) **regravou o parquet e apagou as respostas
  da 1ª fase** — a cadeia de gabaritos precisa rodar APÓS todo import
- **PyMuPDF perde glifos** dos PDFs CESPE 2003-2010 (fontes com encoding
  quebrado): letras de gabarito, marcadores de item e enunciados inteiros

### 2ª e 3ª fase — discursivas (`scripts/extract_discursivas.py`)
- Era Cebraspe: `-- PROVA ESCRITA DE X --` (travessões opcionais) + blocos
  `QUESTÃO N` (qualquer capitalização) + padrão de resposta oficial no `answer`
- Padrões antigos (2017/2018): `PROVA DISCURSIVA|ESCRITA – SEGUNDA/TERCEIRA
  FASE` + `<DISCIPLINA> – QUESTÃO N` (subject quebrando linha) ou
  `<DISCIPLINA> – REDAÇÃO/RESUMO/SUMMARY` → qn 1
- Provas por disciplina (2019-2023): arquivos `discursiva_<materia>__*.pdf`,
  ~4 questões cada, extraídas como terceira fase; subject pelo nome do
  arquivo (cuidado com `__` duplo no regex)
- 2024-2026: **20 questões/ano, todas com padrão de resposta**
- 2017: 20 questões, só 1 com padrão (só 2 arquivos de padrão baixados)
- 2018: 0 questões (LP/LI são redação sem marcadores; resto em
  `discursiva_<materia>` com encoding quebrado)

### Transcrição das 13 questões faltantes
- Localizadas nos PDFs dos zips archive.org (extraídos para
  `data/raw/*/archive/`)
- Rascunhos automáticos salvos como `questoes_faltantes.md` em cada pasta
  archive (RENOMEADOS de .jsonl para .md para o import NÃO pegá-los)
- **Não importados**: 2003 saiu com 2 de 5 itens por questão; 2005 só o
  comando; 2010 q38-39 estão em outro PDF (PARTE_I não tem marcadores)
- Fechamento exige **OCR** ou revisão manual

## Sessão 2 — 22/10/2026: lacunas e levantamento
- Levantamento completo de lacunas: 13 questões de transcrição ausentes
  (2003: q11-14; 2005: q9-11/15-17/43; 2010: q38-39), 197 itens sem gabarito
  (anulados + MC + perdas de grade), defeitos de qualidade conhecidos
- Post do plano de conteúdo: dias 19 e 30 gerados em `conteudo/` + INDEX.md

## Sessão 3 — 22/10/2026: commit e push
- `3dd8214 feat(data): completa gabaritos e extrai discursivas 2a/3a fase`
  (25 arquivos) — push para `origin/main` concluído
- Primeiro commit falhou com "unable to write new index file" — lock
  transitório (OneDrive/antivírus); retry funcionou

## Sessão 4 — 22/10/2026: posts do plano de 31 dias
- Lido estado real do repo: `evaluation/` vazio (0 backtest), `tests/` vazio
  (0 testes), `data/metadata/` sem taxonomia (só catálogos de fontes)
- Gerados `conteudo/2026-11-09-backtesting-precision-k.md` (dia 19 — status
  "depende de mudança", post de método), `conteudo/2026-11-20-pesquisa-
  reprodutivel-manifesto.md` (dia 30 — manifesto real: 463 entradas com
  SHA-256, 460 PDFs) e `conteudo/INDEX.md`

## Sessão 5 — 23/10/2026: reparo de pipeline (regras de dados)
- Descoberta: o import das discursivas regravou o parquet e apagou as
  respostas da 1ª fase (só 136 restaram)
- Causa 1: rodar `extract_gabaritos.py` sem `--year` regrava o cache só com
  2015-2026 — corrigido (loop explícito 2003-2026 no main())
- Causa 2: o fallback itn=null → 1 (necessário para o formato C 2024-2026)
  tinha sido removido no guard de "feche as lacunas" — reintroduzido
  condicionalmente (year>=2024 + certo_errado)
- Estado pós-reparo: **1ª fase 5.020 itens, 4.677 (93,2%) com gabarito**
  (o pico anterior era 4.827/96,1% — a diferença de ~150 linhas são as
  rules 2009-2013 com itn=null que o guard atual não cobre)
