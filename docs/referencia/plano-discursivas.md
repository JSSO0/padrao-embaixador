# Plano — Bloco Discursivas (2ª/3ª fase)

Estado de partida (23/10/2026): 467 linhas de 2ª/3ª fase no parquet
(193 2ª fase, 274 3ª fase) contra **~229 documentos de discursiva baixados**
(161 por disciplina + 66 prova_discursiva + 43 padrão de resposta + zips).

## Fase 0 — Inventário e viabilidade (meio dia)

Mapear arquivo a arquivo (por ano × disciplina × fase):
- Qual PDF contém quais questões (os marcadores, o nº de itens).
- Qualidade do texto: limpo (Cebraspe/wayback 2013+) vs quebrado (2005-2012, 2019-2023).
- Saída: `data/processed/inventario_discursivas.csv` com colunas
  ano, disciplina, arquivo, familias, fase declarada no documento, n_questões, texto_ok.

Amostras já verificadas na conversa:

| Fonte | Texto | Marcadores | Observação |
|---|---|---|---|
| 2015 wayback (3ª fase, 12 p.) | ✅ limpo, 54k chars | QUESTÃO 1-12 | 3ª fase = C/E (4 itens/questão) |
| 2019-2023 secundário (19 p.) | ⚠️ cabeçalho limpo, corpo parcial | QUESTÃO 1-4 | 48 de ~160 extraídas; resto perde glifos |
| 2003 zip (Segunda_Fase_*) | dentro do zip, não extraído ainda | ? | extrair e testar |
| 2008/2010 zip (Prova Escrita por disciplina) | ? | ? | extrair e testar |

## Fase 1 — era Cebraspe completa (2017, 2018, 2024-2026)

1. **2017**: baixar os padrões de resposta faltantes (só 2 dos ~8 existem);
   aplicar com o parser `extract_padrao_antigo` (já implementado).
2. **2018**: as 8 disciplinas da 3ª fase têm padrão baixado mas as questões
   estão na família `discursiva_<materia>` — extrair com OCR ou parser
   específico; a LP/LI são redação/exercícios (sem QUESTÃO N) — modelar como
   `question_type='essay'` com o texto do exercício em `item_text`.
3. **2024-2026**: ✅ pronto (60 questões, todas com padrão).

## Fase 2 — era intermediária limpa (2013-2016, wayback)

- 4 anos × 7-8 provas, texto limpo confirmado (2015 amostrado).
- O formato: C/E com 4 itens ("quatro itens a serem julgados") + questões
  discursivas — mesmo parser da 1ª fase (marcadores QUESTÃO N + bullets)
  com `stage='terceira_fase'`.
- Conflito com as rules existentes (2014: 52, 2015: 64, 2016: 50 linhas de
  3ª fase): o dedup do import resolve por question_id; conferir cobertura
  antes/depois.

## Fase 3 — era antiga nos zips (2003-2012)

1. Extrair os PDFs das provas escritas dos zips (2003: 2 disciplinas;
   2008: 8; 2010: 9; demais anos: 2-8).
2. Texto provavelmente limpo (mesma família do PDF da 1ª fase de 2003, que
   extraiu 70k chars) — validar marcadores e numeração por disciplina.
3. Question_number por disciplina (cada prova tem sua numeração); o nº
   global da edição sai de `parent_question_id`/registry.
4. Padrão de resposta: não existe para essa era — `answer=null` documentado
   (o gabarito comentado do cursocacd, quando houver, é fase futura).

## Fase 4 — OCR (só o que sobrar)

- Instalar tesseract (winget) + `pytesseract`.
- Aplicar APENAS aos arquivos que falharem na extração de texto, com
  comparação automática: se o texto nativo já tiver ≥ 90% dos marcadores
  esperados, não roda OCR.
- Fila atual: 2019-2023 parciais, 2005-2012 conforme o zip, ~19 letras de
  gabarito, 13 questões de transcrição.

## Fase 5 — modelo de dados das discursivas

- `question_type='essay'` para dissertativas; itens C/E dentro da prova
  escrita continuam `certo_errado` com `item_number` 1-4.
- `answer` = padrão de resposta (2017+) ou null documentado.
- Chave: (contest_id, phase, stage, discipline, question_number, item_number).
- `notes` registra a fonte e o método (nativo vs OCR).

## Entregas e validação por fase

- Cada fase termina com: import → clean_dup_rules → overview → amostra
  qa_jsonl de 2 questões/ano → commit.
- Métrica de sucesso do bloco: das ~400-500 questões discursivas potenciais,
  extrair ≥ 80% com proveniência completa.

## Riscos

- Encoding quebrado nas fontes 2005-2012 e 2019-2023 (mitigação: OCR).
- Numeração local por disciplina (chave dupla disciplina+questão — já suportada).
- Falta de padrão de resposta para 2003-2016 (answer=null documentado).
- Duplicação com as rules de 3ª fase existentes (mitigação: dedup do import
  + clean_dup_rules).
