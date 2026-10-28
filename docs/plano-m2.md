# Plano do Marco 2 — Temas

> Atividades necessárias para concluir o **M2** com sucesso.
> Fontes: [`MAPA-DO-PROJETO.md`](MAPA-DO-PROJETO.md) e [`ROADMAP.md`](ROADMAP.md). Elaborado em 28/10/2026.

---

## Spec (o que é "pronto")

**Objetivo:** cada item da 1ª fase tem **um** tema, vindo de uma taxonomia escrita e versionada, sem vazamento (a definição dos temas não "conhece" os anos futuros).

**Estado atual:** 60 temas; **82 itens sem tema (1,6%)** — todos de 2004/2005/2007; maior tema = `reading_comprehension` (7,7%); **18 temas com < 0,5%** (M2.4); 4 itens em `geral` (H. do Brasil); o `refine_taxonomy_tfidf.py` reclassifica usando o corpus **inteiro** (vazamento leve — M2.3).

**Critério de sucesso (definição de pronto):**
- 0 itens da 1ª fase sem tema
- Taxonomia versionada em `data/metadata/taxonomia.yaml`, lida pelos scripts (nada hardcoded)
- Método de classificação **sem vazamento** documentado e **provado por teste** (fold X não usa itens > X)
- Granularidade balanceada: nenhum tema > 8% dos itens nem < 0,5%; distribuição publicada em `docs/relatorios/`
- ≥ 90% de concordância na validação manual de 50 classificações

**Fora de escopo:** features de modelo (M4), protocolo de backtest (M3), temas de discursivas.

---

## Decisões de método (a documentar no M2.3)

| Decisão | Escolha proposta | Justificativa |
|---|---|---|
| Como atribuir tema a cada item | **Regras fixas do YAML (a priori)** — palavras-chave + descrição; fallback = tema mais amplo da disciplina, nunca "geral" | Auditável, reproduzível, não olha o futuro; o TF-IDF global fica abandonado |
| O que fazer com o TF-IDF atual | Desativar do fluxo (passo 13) — ou relegá-lo ao M4 como feature por fold | É a fonte do vazamento identificado no §4 do Mapa |
| Renumeração/merge de temas | Renumerar a taxonomia no YAML (v1) | Mudança de temas muda o baseline do M3 — congelar antes do M3 |

---

## Plano de execução

| Fase | O que resolve | Tarefas |
|---|---|---|
| A — Taxonomia versionada | Fonte única, legível por máquina | M2.1 |
| B — Cobertura e não-vazamento | 0 itens sem tema + teste anti-vazamento | M2.2, M2.3 |
| C — Granularidade | 18 temas raros fundidos; nenhum > 8% | M2.4 |
| D — Validação | ≥ 90% de concordância humana | M2.5 |

---

## Tasks

### Fase A — Taxonomia versionada (1 sessão)

- [x] **A1 (M2.1)** 🏷️ Escrever `data/metadata/taxonomia.yaml`: disciplina → tema → palavras-chave → descrição; cada tema com o tema "de fallback" da disciplina ✅ 28/10/2026
  - *Aceite:* **PASS** — YAML v1 com 9 disciplinas, 62 temas (keywords + descrição por tema) e fallback por disciplina; gerado de `ferramentas/extracoes_pontuais/gera_taxonomia_yaml.py` a partir das regras refinadas
- [x] **A2** 🔧 Adaptar `pipeline/build_taxonomy.py` + `refine_taxonomy.py` para lerem do YAML (remover listas literais dos scripts); documentar em `pipeline/README.md` a nova ordem (passos 11–13) ✅ 28/10/2026
  - *Aceite:* **PASS** — `build_taxonomy.py` reescrito (leitura do YAML, uma passada, dry-run); `refine_taxonomy.py` e `refine_taxonomy_tfidf.py` **removidos do fluxo** (TF-IDF global desativado); README atualizado

### Fase B — Cobertura e não-vazamento (1 sessão)

- [x] **B1 (M2.2)** 🏷️ Classificar as 82 itens sem tema (2004: 30, 2005: 20, 2007: 32) — 72 deles também sem `discipline_canon`; regras do YAML + conferência manual do texto ✅ 28/10/2026
  - *Aceite:* **PASS** — 0 itens sem tema; 0 com `topic = "geral"`. Disciplinas preenchidas (`pipeline/preenche_disciplinas_m2.py`): 2003 q11–14 → Economia; 2005 q9–11/15–16 → História (Mundial); 2007 q31–38 → História do Brasil; 2004 q141–150 (Cultura Geral) entraram no YAML
- [x] **B2 (M2.3)** 🏷️ Classificação **sem olhar o futuro**: remover o passo 13 (`refine_taxonomy_tfidf.py`) do fluxo e substituir por regras fixas do YAML; escrever teste que prova que a atribuição do fold X não usa itens > X ✅ 28/10/2026
  - *Aceite:* **PASS** — método documentado no README do pipeline; `tests/test_taxonomia_nao_vazamento.py` (7 testes): YAML íntegro, sem tema "geral", classificação invariante ao corpus (idêntica com df completo ou só o item), fallback sem keyword, keyword matching

### Fase C — Granularidade (1 sessão)

- [x] **C1 (M2.4)** 🏷️ Balancear: fundir os temas com < 0,5% e revisar se algum > 8% ✅ 28/10/2026
  - *Aceite:* **PASS — 40 temas, maior 7,36% (`guerras_mundiais`), menor 0,56% (`economia_internacional` → fundido no `comércio_internacional`); distribuição publicada em `docs/relatorios/distribuicao-temas.md`. Fusões aplicadas por `pipeline/funde_temas_raros.py` (20 fusões, cada uma com justificativa no changelog do YAML)**
- [x] **C2** 🔧 Renumerar/limpar temas legados e congelar a versão da taxonomia (v1) com tag/changelog no YAML ✅ 28/10/2026
  - *Aceite:* **PASS** — `taxonomia.yaml` version 2 com changelog completo (v1: criação; v2: 20 fusões do M2.4); 0 temas fora da faixa; 0 `geral`

### Fase D — Validação (1 sessão)

- [~] **D1 (M2.5)** 📏 Validar 50 classificações à mão (amostra nova, seed fixa, checklist igual ao do M1.9) 🔄 28/10/2026
  - *1ª validação (seed 2028): 34/50 = 68% — abaixo do aceite.* Os 18 erros foram analisados (`ferramentas/diagnostico/diag_m25_keywords.py`) e geraram a **taxonomia v3/v4**: correção da disciplina de 2018 q43 (Text VI = Língua Inglesa), remoção de keywords genéricas (`sentence`, `paragraph`, `pronome`, `preposição`, `mercado`, `equilíbrio`, `ambiental` da geografia física) e novas chaves discriminantes (semântica, comércio_internacional, desenvolvimento, macroeconomia, urbanização, meio_ambiente, internacional_público, revoluções_liberais, vocabulary). `pipeline/ajusta_taxonomia_v3.py`
  - *Re-verificação dos 18 casos: 16 agora classificam conforme o revisor; 2 divergências residuais por nuance de stem (2018 Q43 e 2024 Q39/2, grammar_semantics × vocabulary/RC).* Distribuição continua na faixa (max 7,83%).
  - **Falta: 2ª validação manual** — amostra nova (seed 2029) em `data/processed/qa_sample/validacao_temas_m2.md`
  - 🔄 28/10/2026 — **1ª rodada FALHOU: 33/50 = 66%** (72% contando os discutíveis) em `data/processed/qa_sample/validacao_temas_m2.md`. Fallback acerta 2/10; keyword acerta 31/40. Próximo: corrigir fallback, fronteira de palavra nas keywords, peso do item × texto-base, lacunas da taxonomia; corrigir disciplina da CACD_2018 Q43 (é inglês); validar com seed nova

---

## Dependências e ordem

- **A1** vem primeiro (tudo sai do YAML).
- **B1** depende de A1; **B2** é independente de B1 e pode rodar em paralelo.
- **C1** só depois de B1 (a distribuição precisa de 100% de cobertura).
- **D1** por último (valida o resultado final congelado).

**Total: ~2–3 sessões** (estimativa do roadmap: 2–3).

## Riscos

- Subjetividade da taxonomia: os resultados do M4 dependem da definição dos temas — mitigado pelo YAML versionado + validação manual (D1)
- Fundir temas raros demais pode engolir distinções que o modelo usaria — revisar cada fusão contra a distribuição final
- Remover o TF-IDF global pode deixar itens mal classificados que hoje recebem "melhor tema por similaridade" — mitigado por regras de fallback explícitas por disciplina
