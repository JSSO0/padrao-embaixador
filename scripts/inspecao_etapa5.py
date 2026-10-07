# -*- coding: utf-8 -*-
"""Gera relatorio de inspecao dos formatos problematicos da etapa 5.

Saida: docs/inspecao-formatos.md
O usuario abre este relatorio junto com o PDF original e responde o
template no fim do arquivo. As anotacoes alimentam os regex dos parsers.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from parser.document_loader import load_pdf  # noqa: E402

RAW = ROOT / "data" / "raw"
OUT = ROOT / "docs" / "inspecao-formatos.md"

ALVOS = [
    ("IADES 2022 (manhã)", "CACD_2022/cursocacd/prova_objetiva_1__52befe35.pdf"),
    ("IADES 2019", "CACD_2019/cursocacd/prova_objetiva_1__623b6355.pdf"),
    ("IADES 2023", "CACD_2023/cursocacd/prova_objetiva_1__b1aab22b.pdf"),
    ("CESPE 2004", "CACD_2004/cursocacd/prova_objetiva_1__582843a3.pdf"),
    ("CESPE 2010 (alternativas)", "CACD_2010/cursocacd/prova_objetiva_1__9ee3dea5.pdf"),
]


def find_file(rel_sub: str) -> Path | None:
    for p in RAW.glob(rel_sub):
        return p
    # fallback por prefixo
    parts = rel_sub.split("/")
    folder = RAW / parts[0] / parts[1]
    prefix = parts[2][:16]
    cands = sorted(folder.glob("*"))
    for c in cands:
        if c.stem.startswith(prefix.replace("__", "__")) or prefix[:12] in c.stem:
            return c
    return None


def dump_block(block: str, max_chars: int = 1600) -> str:
    txt = block.replace("\n", " ⏎ ")
    return txt[:max_chars]


def main() -> None:
    lines = ["# Inspeção de formatos — Etapa 5 (para resolução manual)", ""]
    lines.append("Cada seção abaixo mostra o começo de 2 questões do PDF problemático.")
    lines.append(
        "⏎ = quebra de linha real do texto extraído. Compare com o PDF aberto e responda o template no fim do arquivo."
    )
    lines.append("")

    for titulo, rel in ALVOS:
        pdf = find_file(rel)
        lines.append(
            f"## {titulo_format(titulo := titulo)}" if False else f"## {titulo}"
        )
        if pdf is None:
            # busca generica por prefixo
            base = RAW / rel.split("/")[0] / rel.split("/")[1]
            cands = sorted(base.glob(f"{rel.split('/')[2][:12]}*.pdf"))
            if not cands:
                lines.append(f"> PDF não encontrado: `{rel}`")
                lines.append("")
                continue
            pdf = cands[0]
        lines.append(f"Arquivo: `{pdf.name}`")
        doc = load_pdf(pdf, ROOT)
        t = doc.text
        marks = list(re.finditer(r"QUEST[ÃA]O\s+(\d+)", t))
        lines.append(
            f"Marcadores `QUESTÃO N` encontrados: **{len(marks)}** -> {[m.group(1) for m in marks[:12]]}"
        )
        lines.append(f"Layout estimado: {doc.n_pages} páginas, {len(t)} chars")
        lines.append("")
        if not marks:
            lines.append(
                "### SEM marcadores QUESTAO N - primeiros 1600 chars do documento"
            )
            lines.append("```text")
            lines.append(dump_block(t, 1600))
            lines.append("```")
            lines.append("")
            lines.append("---")
            lines.append("")
            continue
        # bloco 1 e 2
        for qi in range(min(2, len(marks) - 1)):
            a = marks[qi].start()
            b = marks[qi + 1].start() if qi + 1 < len(marks) else min(a + 2500, len(t))
            lines.append(
                f"### Bloco QUESTÃO {marks[qi].group(1)} (primeiros ~1600 chars)"
            )
            lines.append("```text")
            lines.append(dump_block(t[a:b], 1600))
            lines.append("```")
            lines.append("")
        # candidatos a numero-de-item no meio do bloco 1
        block = (
            t[marks[0].start() : marks[1].start()]
            if len(marks) > 1
            else t[marks[0].start() : marks[0].start() + 4000]
        )
        cands = [
            (m.group(1), m.group(2)[:70])
            for m in re.finditer(r"(?m)^\s*(\d{1,2})\s*[\)\.\-]?\s+(\S.{20,})", block)
        ]
        lines.append(f"Linhas iniciando com número no bloco 1: {len(cands)}")
        for n, txt in cands[:12]:
            lines.append(f"- `{n}` → {txt}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines.append("## Template de respostas (preencha e devolva)")
    lines.append("")
    lines.append("""### IADES (2019/2022/2023)
1. A "grade" de números no topo da questão (1, 4, 7, 10, 13...) é o quê no PDF? (tabela? cabeçalho? folha de respostas?)
2. Como CADA item certo/errado aparece no texto? (ex.: número em linha própria? letra a)? de_bullet?)
3. Copie aqui 1 item completo exatamente como aparece no PDF (do número até o fim da frase).
4. A prova tem 1 ou 2 colunas por página?

### CESPE 2004
5. Copie o trecho de 1 questão completa (do "QUESTÃO 1" até a alternativa A).
6. As alternativas usam letras A/B/C/D/E ou outra marcação?

### CESPE 2010
7. Como a alternativa aparece: letra sozinha em uma linha, letra + ")" colada, ou outra?
8. Copie 1 alternativa completa como aparece no PDF.
""")

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"relatorio gerado: {OUT}")


def titulo_format(t: str) -> str:
    return t


if __name__ == "__main__":
    main()
