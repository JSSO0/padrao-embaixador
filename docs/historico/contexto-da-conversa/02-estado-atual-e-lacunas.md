# Estado atual dos dados (23/10/2026)

## Parquet (`data/processed/questions.parquet`)

- **5.487 registros** = 454 rules + 5.033 manual
- Por stage: primeira_fase 5.020 · segunda_fase 193 · terceira_fase 274
- Colunas: question_id, parent_question_id, contest_id, year, phase, stage,
  discipline, question_number, item_number, question_type, question_text,
  item_text, alternatives, answer, source_type, source_file,
  extraction_method, warnings, notes (sem coluna `page`)

### 1ª fase — cobertura por contest (linhas SEM gabarito, 23/10/2026)

| Contest | Sem gabarito | Nota |
|---|---|---|
| CACD_2003 | 2 | itens itn=null (sem alternatives) |
| CACD_2004 | 1 | qn=109 (letra não extraída da grade) |
| CACD_2005 | 9 | MC sem letra no grid + nan sem alternatives |
| CACD_2006 | 23 | rules itn=null (22) + 1 manual |
| CACD_2007 | 15 | rules itn=null (15) |
| CACD_2008 | 3 | perdas de extração |
| CACD_2009-2013 | 36+33+11+48+63 | rules itn=null + perdas (regressão parcial pós-import) |
| CACD_2014 | 2 | anuladas |
| CACD_2015-2018 | 7+7+11+9 | anuladas |
| CACD_2019-2023 | 7+4+1+2 | anuladas |
| CACD_2024 | 19 | anuladas (15) + não extraídas |
| CACD_2025/2026 | 240/240? não — **16/14 sem** | anuladas |

**Total: 4.677/5.020 (93,2%) com gabarito.** O pico histórico foi 4.827
(96,1%) em 19/10 antes do re-import das discursivas; a diferença (~150
linhas) são as rules 2009-2013 com itn=null que o guard atual do apply
não cobre (decisão: não aplicar sem chave confiável).

### 2ª fase (193 itens)

- 2017: 24 (20 novos + 4 legado) — 1 com padrão de resposta
- 2024/2025/2026: 20 cada, **todas com padrão de resposta oficial**
- 2006 (77), 2007-2016 (4-7 cada): legado das rules, sem resposta

### 3ª fase (274 linhas)

- Legado rules: 2006-2018 (2009: 7, 2010: 6, 2011-2012: 4, 2014: 52,
  2015: 64, 2016: 50, 2017: 5, 2018: 4)
- Novo (2019-2023): 12+12+16+8 = 48 questões extraídas por disciplina
- 3ª fase não tem padrão de resposta aplicado

## Gabaritos por formato (data/processed/gabaritos.json)

| Ano | Respostas em cache | Anuladas |
|---|---|---|
| 2003 | 150 | 0 |
| 2004 | 150 | 1 |
| 2005-2008 | 136/144/145/189 | 0 |
| 2009-2013 | 221/237/178/156/128 | 4/2/3/9/7 |
| 2014 | 292 | 10 |
| 2015-2018 | 292 cada | 7/7/11/9 |
| 2019 | 292 | 7 |
| 2020 (2020_2021) | 292 | 4 |
| 2022/2023 | 292 | 1/1 |
| 2024 | 260 | 17 |
| 2025/2026 | 242/242 | 16/14 |

## Lacunas de transcrição (questões inteiras ausentes)

| Contest | Questões |
|---|---|
| CACD_2003 | 11, 12, 13, 14 |
| CACD_2005 | 9, 10, 11, 15, 16, 17, 43 |
| CACD_2010 | 38, 39 |

PDFs localizados e extraídos em `data/raw/*/archive/`; rascunhos em
`questoes_faltantes.md` (incompletos — PyMuPDF perde glifos).

## Defeitos de qualidade conhecidos

1. **2024**: algumas questões com question_text de LI vinculadas a passagem
   de outra disciplina (vínculo de textos-base)
2. **2025 item 235**: grupo "completar frase" da CF88 — enunciado no item
   234; item 236 absorveu 1ª linha da instrução seguinte
3. **2013**: 10 linhas de rules com qn 174-227 (itens contados como questões)
4. **2004**: manual com esquema duplicado (agrupado qn+itn e achatado itn=qn);
   148/150 com gabarito via mapeamento especial
5. Regras 2015+: linhas vindas de PDFs de discursiva com stage
   primeira_fase e qn=nan (fragmentos de gabarito comentado — mantidas pois
   carregam respostas reais)
