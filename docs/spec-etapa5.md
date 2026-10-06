# Spec da Etapa 5 — Segmentação de Questões e Dataset Granular

> Status: especificação aprovada para implementação · Depende de: corpus v0.1 (tag `v0.1-corpus`)
> Rastreia: spec-requisitos §6 (dataset principal), §7 (dataset temático vem depois), plano-mestre Etapa 5

---

## 1. Objetivo

Transformar os 453 TXTs + 463 PDFs do corpus em um **dataset granular validado**: 1 linha por questão (e por item, no formato IADES), com enunciado, alternativas, gabarito, disciplina e proveniência completa.

**Inputs:** `data/raw/` (PDFs) · `data/processed/text/` (TXTs) · `data/processed/text_metrics.csv` · `data/metadata/*` (catálogos)
**Outputs:**
- `data/processed/questions.parquet` — dataset principal (1 linha = 1 item/questão)
- `data/processed/extraction_report.csv` — auditoria por documento (questões extraídas vs. esperadas)
- `data/processed/answer_keys.parquet` — gabaritos normalizados por edição/fase/turno

## 2. Descobertas empíricas que condicionam o parser (verificadas nos TXTs reais)

| Família | Formato do marcador | Layout | Exemplo real |
|---|---|---|---|
| Cebraspe 2024–2026 | **número solto na linha** (item certo/errado) | 1 coluna, enunciado acima do número | `Em relação…, julgue os itens seguintes.` `\n1\n` `O texto trata…` |
| Cebraspe 2017–2018 (e Wayback) | `QUESTÃO N` + alternativas `A)`–`E)` (múltipla escolha na 1ª fase de 2018; itens a partir da 2ª) | 1 coluna | `QUESTÃO 12` |
| IADES 2019–2023 | `QUESTÃO N` com 4–5 **itens** certo/errado dentro de cada questão; grade de respostas no início do caderno | **2 colunas** — extração linear intercala colunas | `QUESTÃO 1` … itens numerados 1–156 |
| CESPE antigo 2003–2012 | `QUESTÃO N` com alternativas A–E; comandos por bloco de disciplina | 1 coluna | `QUESTÃO 1`, `Texto I - questões 2 e 4` |
| Curso CACD (todas as edições) | PDFs "consolidados" — caderno único por disciplina com cabeçalho próprio | variado | |
| Discursivas | `PROVA ESCRITA DE <DISCIPLINA>` + questões discursivas com valores | 1 coluna | |

**Implicação técnica importante:** cadernos em 2 colunas (IADES e parte do Cebraspe) exigem extração **cordonhecendo colunas** — re-extrair com `pymupdf` usando blocos (`page.get_text("blocks")`) ordenados por x0 antes de segmentar. O TXT linear existente serve para QA, não para parsing.

## 3. Bibliotecas

| Lib | Papel | Status |
|---|---|---|
| `pymupdf` | re-extração ciente de layout (`get_text("blocks")`), extração das páginas dos gabaritos | ✅ instalado |
| `pydantic` (v2) | modelos de domínio + validação de parsed | adicionar |
| `pandera` | schema do parquet de saída (validação obrigatória antes de escrever) | adicionar |
| `pandas` + `pyarrow` | dataset parquet | adicionar |
| `duckdb` | QA analítico (contagens por edição/disciplina) | adicionar |
| `litellm` + `instructor` | LLM só para casos ambíguos (determinar disciplina de bloco, corrigir recorte quebrado) — opcional e amostrado | adicionar quando precisar |
| `pytest` | testes dos parsers com **fixtures de texto real** (trechos dos TXTs) | adicionar |
| `tqdm` | progresso | adicionar |

## 4. Arquitetura de código (pacote `parser/`)

```
parser/
├── __init__.py
├── models.py          # dominio (Pydantic)
├── schemas.py         # schemas pandera de saida
├── extract_text.py    # (existente) etapa 4
├── document_loader.py # le ciente de colunas -> ParsedDocument
├── parsers/
│   ├── __init__.py    # registro/factory dos parsers por familia
│   ├── base.py        # DocumentParser ABC
│   ├── cebraspe_modern.py   # 2024-2026 (itens numerados soltos)
│   ├── cebraspe_2017_2018.py # QUESTAO N + alternativas A-E
│   ├── iades.py             # 2019-2023 (questao com itens certo/errado)
│   └── cespe_legacy.py      # 2003-2012
├── answer_merger.py   # gabarito -> resposta por questao/item
├── dedup.py           # selecao de espelho por prioridade de fonte
├── qa.py              # validacoes contra o edital
└── build_dataset.py   # CLI: orquestra e escreve o parquet
```

### 4.1 Modelos de domínio (`models.py`)

```python
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

SourceType = Literal["official_mre", "official_cebraspe", "official_cebraspe_archive",
                     "secondary_repository", "unknown"]
QuestionType = Literal["multiple_choice", "certo_errado", "essay"]

class Alternative(BaseModel):
    letter: str                      # "A".."E"
    text: str

class Item(BaseModel):
    """Sub-unidade de questao certo/errado (IADES) ou item Cebraspe moderno."""
    item_number: int
    text: str
    answer: str | None = None        # "C" | "E" quando gabarito casado
    confidence: float = 1.0

class Question(BaseModel):
    question_id: str                 # SHA-1 deterministico
    contest_id: str
    year: int
    phase: int                       # 1 = objetiva, 2 = escrita, 3 = escrita antiga
    stage: str                       # "primeira_fase" | "segunda_fase" | "terceira_fase"
    discipline: str | None           # normalizada (registry de disciplinas)
    question_number: int | None
    question_type: QuestionType
    question_text: str
    alternatives: list[Alternative] = []
    answer: str | None = None        # letra, para multiple_choice
    items: list[Item] = []           # para certo/errado
    source_url: str | None
    source_type: SourceType
    source_file: str                 # caminho relativo do PDF
    page: int | None
    extraction_method: Literal["rules", "llm_assist", "manual"] = "rules"

class ParsedExam(BaseModel):
    contest_id: str
    source_file: str
    family: str                      # cebraspe | iades | cespe_legacy | cursocacd
    questions: list[Question]
    warnings: list[str] = []

class ExtractionReport(BaseModel):
    contest_id: str
    source_file: str
    questions_found: int
    questions_expected: int | None   # do contest_registry (Etapa 2)
    expected_unknown: bool
    coverage: float | None           # found/expected
    issues: list[str]
```

### 4.2 Contrato do parser (`parsers/base.py`)

```python
class DocumentParser(ABC):
    family: str

    @abstractmethod
    def matches(self, doc: DocumentContext) -> bool:
        """Decide se este parser atende o documento (família + palavras-chave)."""

    @abstractmethod
    def parse(self, doc: DocumentContext) -> ParsedExam:
        """Extrai questões de um documento já carregado."""
```

- `DocumentContext`: texto (com colunas resolvidas), metadados do arquivo (caminho → contest_id, família, URL do manifest), nº esperado de questões (opcional)
- **Factory** em `parsers/__init__.py`: escolhe o parser por (família de pasta, ano, detecção de padrão no texto) — ordem de tentativa: específico → genérico `QUESTÃO N` → fallback com warning
- Regra de ouro: **parser novo = arquivo novo + fixtures de teste**; nada de regex soltas espalhadas

### 4.3 Loader ciente de colunas (`document_loader.py`)

- Abre o PDF com PyMuPDF; para cada página, `get_text("blocks")` → agrupa blocos em colunas por clusters de `x0` (threshold configurável em `configs/segmentation.yaml`) → concatena coluna a coluna
- Gera `DocumentContext(text, blocks, n_pages)`; TXT linear da Etapa 4 vira material de comparação (QA), não input do parser
- **Discrimina cadernos de gabarito**: arquivos `gabarito*` entram no fluxo do `answer_merger`, não do parser de questões

### 4.4 Fusão de gabaritos (`answer_merger.py`)

- `AnswerKeyParser`: extrai `número → letra` (ou `C/E`) do PDF de gabarito (Cebraspe: tabela por caderno/turno; IADES: gabarito separado; antigos: gabarito no mesmo PDF)
- `AnswerMerger.merge(questions, answer_keys)` — casamento por (contest_id, fase, turno, nº da questão/item); conflitos entre preliminar e definitivo → **definitivo vence** e o conflito é logado (regra §5 da spec: guardar ambos no manifest, nunca sobrescrever silenciosamente)

### 4.5 Deduplicação de espelhos (`dedup.py`)

- Mesmo documento em 2+ fontes (ex.: 2013–2017 oficial + cursocacd) → escolher por prioridade: `official_cebraspe` > `official_cebraspe_archive` > `official_mre` > `secondary_repository`
- Dedupe por similaridade de hash de texto normalizado (não por nome de arquivo)
- Espelhos descartados ficam registrados no `extraction_report` como `duplicate_of`

### 4.6 QA (`qa.py`) — gates obrigatórios

1. `count_check`: questões extraídas vs. nº do edital (Etapa 2); sem edital, vs. maior número contínuo de questão; alvo ≥95%
2. `answer_coverage`: % de questões com gabarito casado; alvo ≥95%
3. `discipline_coverage`: cada questão com disciplina (ou warning explícito)
4. `text_quality`: enunciado mínimo (≥40 chars), sem chars de controle, sem cabeçalho/rodapé vazando no texto
5. Amostragem manual: export de 5% aleatório para revisão humana (`data/processed/qa_sample/`)

## 5. Decisões de design já tomadas

1. **Granularidade: 1 linha por ITEM** no formato certo/errado (Cebraspe moderno e IADES), com coluna `parent_question_id` para questões compostas. Múltipla escolha antiga (2003–2018 1ª fase) = 1 linha por questão com alternativas. Motivo: previsão por tema usa item como unidade mais fina; questões compostas são recuperáveis via `parent_question_id`.
2. **Disciplinas**: registry normalizado em `data/metadata/discipline_registry.csv` (mapeia variações de nomes por edital; nos cadernos modernos, o bloco de disciplina vem como cabeçalho de seção).
3. **`question_id` determinístico** = SHA-1 de `contest_id|stage|discipline|question_number|item_number` — reprocessar não muda IDs.
4. **Config separada do código**: `configs/segmentation.yaml` (thresholds de coluna, regex por família, prioridade de fontes).
5. **Pydantic em memória → pandera na borda** (validação do parquet) → DuckDB para QA. Sem banco nesta etapa.

## 6. Critérios de aceitação da Etapa 5

- [ ] `questions.parquet` com schema pandera validado e `question_id` únicos
- [ ] ≥95% de cobertura de extração vs. nº oficial de questões por edição (exceções documentadas: 2005/2019 needs_ocr)
- [ ] ≥95% de cobertura de gabarito
- [ ] Deduplicação aplicada e registrada (espelho secundário descartado com `duplicate_of`)
- [ ] Amostra de 5% revisada manualmente com fidelidade ≥97%
- [ ] `extraction_report.csv` completo (todo documento do corpus tem linha: extraído, duplicado, needs_ocr ou NOT_FOUND)
- [ ] Testes pytest dos parsers com fixtures de texto real de cada família

## 7. Sequência de implementação (sugestão de PRs)

1. `feat(parser): domain models + document loader com colunas` (models.py, document_loader.py, configs)
2. `feat(parser): parser cebraspe moderno` (2024–2026 — formato mais estável, corpus oficial)
3. `feat(parser): parser iades` (2019–2023, 2 colunas)
4. `feat(parser): parser cespe legacy` (2003–2018, `QUESTÃO N` + alternativas)
5. `feat(parser): answer merger + dedup + qa` + `build_dataset.py`
6. `test(parser): fixtures de texto real + casos borda`
7. `feat: dataset final questions.parquet + extraction_report` (tag `v0.2-dataset`)
