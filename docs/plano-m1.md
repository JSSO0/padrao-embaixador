# Plano do Marco 1 — Dados confiáveis

> Atividades necessárias para concluir o **M1** com sucesso.
> Fontes: [`MAPA-DO-PROJETO.md`](MAPA-DO-PROJETO.md) e [`ROADMAP.md`](ROADMAP.md). Elaborado em 27/10/2026.

---

## Spec (o que é "pronto")

**Objetivo:** só entram no modelo questões reais da 1ª fase, com texto, disciplina e gabarito corretos.

**Critério de sucesso:**

- Nova amostra de 50 questões (outra seed) com **≥ 97% de fidelidade** (hoje: 88%)
- **Nenhuma linha `rules`** na 1ª fase sem justificativa em `notes`
- 0 duplicatas, 0 itens sem resposta sem motivo registrado

**Fora de escopo:** temas/taxonomia (M2), backtest (M3), discursivas.

---

## Plano de execução

Sequência proposital: primeiro eliminar as fontes de lixo (bug, contaminação por
discursivas), depois transcrever o que falta, depois validar tudo com a nova amostra.

| Fase | O que resolve | Tarefas |
|---|---|---|
| A — Bugs e contaminação | Parar de estragar o dado | M1.1, M1.2, M1.5 |
| B — Transcrição manual | Eliminar o maior bloco de `rules` | M1.3 |
| C — Revisão dos demais `rules` | Cobrir o resto das linhas automáticas | M1.4, M1.7 |
| D — Gabaritos faltantes | Fechar os sem resposta | M1.6 |
| E — Integridade e validação | Provar que está pronto | M1.8, M1.9 |

---

## Tasks

### Fase A — Bugs e contaminação (1 sessão)

- [x] **A1 (M1.1)** 🔧 Corrigir default de anos do `pipeline/extract_gabaritos.py` — hoje roda sem `--year` e apaga respostas de 2003–2014 ✅ 27/10/2026
  - *Aceite:* rodar sem argumentos não altera 2003–2014 — **verificado: 0 alterações (amostra de 1.951 linhas)**
- [x] **A2 (M1.2)** 🗂️ Remover linhas de PDFs de discursiva da 1ª fase (`source_file` com `discursiva_*`) ✅ 27/10/2026
  - *Aceite:* 0 linhas de discursiva com `stage = primeira_fase` — **verificado: 80 linhas removidas (`pipeline/remove_discursivas_primeira_fase.py`), 0 restantes**
- [x] **A3 (M1.5)** 🗂️ Registrar anulados: `notes = "anulado"` onde o gabarito tem X/#/☼; QA exibe "anulado" em vez de `nan` ✅ 27/10/2026
  - *Aceite:* 100% dos itens sem resposta têm motivo em `notes` — **verificado: 114 anulados marcados (`pipeline/marcar_anulados.py`), 0 sem motivo; os 20 itens ainda sem gabarito ficam para o M1.6 (OCR)**

### Fase B — Transcrição 2014 Q32–73 (2 sessões)

- [x] **B1 (M1.3)** 🗂️ Transcrever à mão 2014, questões 32–73 (42 linhas `rules` sem itens e sem disciplina) ✅ 27/10/2026
  - *Aceite:* 2014 com 73 questões `manual`, 4 itens cada — **verificado: 168 itens transcritos (`cacd_2014_primeira_fase_prova_objetiva_2.jsonl`), 42 `rules` removidas, 0 linhas não-2014 alteradas (exceto 34 reclassificações de `topic` do passo 13 do pipeline)**

### Fase C — Revisão das `rules` restantes (1 sessão)

- [x] **C1 (M1.4)** 🗂️ Revisar linhas `rules` da 1ª fase: 2011 (37), 2024 (12), 2025 (17), 2026 (6), 2006, 2007, 2015, 2017, 2023 ✅ 27/10/2026
  - *Aceite:* cada linha vira `manual` ou tem justificativa em `notes` — **verificado: 0 linhas `rules` na 1ª fase. As 37 de 2011 q29–65 foram transcritas (`cacd_2011_primeira_fase_prova_objetiva_2.jsonl`, 97 registros: 80 C/E + 17 MC); as demais já haviam sido removidas/revisadas nas fases A/B**
- [x] **C2 (M1.7)** 🗂️ Corrigir/documentar defeitos pontuais ✅ 27/10/2026
  - *2004 (duplicado `itn=qn`)*: verificado — CACD_2004 tem 150 linhas achatadas, 0 duplicatas (resolvido em reparo anterior)
  - *2013 (qn 174–227)*: verificado — 0 linhas com numeração ruidosa (resolvido em reparo anterior)
  - *2024 (textos-base trocados)*: verificado item a item contra o PDF (q1–9 Textos I–VI; q34–40 Texts I–V) — vinculação correta, defeito não observável
  - *2025 (item 235)*: **corrigido** (`pipeline/corrige_q235_2025.py`) — enunciado compartilhado de q235–236 reconstruído do PDF; q236 tinha o enunciado da q237 colado
  - *2018 Q40 (sufixo "Text V")*: **corrigido** (`pipeline/corrige_sufixo_text.py`) — e 7 casos irmãos em 2016 (4) e 2017 (2): cabeçalho "Text N" colado no fim do `item_text`

### Fase D — Gabaritos faltantes (1 sessão, paralela a B/C)

- [x] **D1 (M1.6)** 🗂️ OCR dos gabaritos 2005–2013 (`ferramentas/extracoes_pontuais/ocr_gabaritos*.py`) ✅ 27/10/2026
  - *Aceite:* itens sem resposta e sem motivo = 0 — **verificado: 26 itens resolvidos. 2008 (3) e 2006-q4: anulados oficiais (celula "+" na tabela do gabarito); 2005: 2 fragmentos removidos + 6 linhas de discursiva removidas + cauda renumerada (39→40 … 47→48, com dupe da q43 removida); 2010 q9 e 2011 q41 recuperadas do text layer (spans duplicados/desalinhados no parser)**

### Fase E — Integridade e validação final (1 sessão, só depois de A–D)

- [ ] **E1 (M1.8)** 🔧 Teste de duplicidade: `contest + stage + discipline + qn + itn` único
  - *Aceite:* `duplicated().sum() == 0`
- [ ] **E2 (M1.9)** 📏 Nova amostra de 50 questões (outra seed) e revisão manual
  - *Aceite:* **≥ 97% OK** → fecha o M1

---

## Dependências e ordem

- **A1** vem primeiro (evita re-trabalho no gabarito).
- **E1/E2** só depois de A–D concluídas.
- **D1** é independente e pode rodar em paralelo com B e C.

**Total: ~5–6 sessões** (estimativa do roadmap: 4–6).

## Riscos

- Transcrição manual de 2014 (B1) é trabalhosa — pode ser feita em paralelo ao M2.1 e M3.2 se atrasar.
- OCR 2005–2013 (D1) depende de Tesseract + `por.traineddata` instalados.
