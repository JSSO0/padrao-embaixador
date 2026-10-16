"""Extrai os gabaritos oficiais (C/E por item) dos PDFs de gabarito e aplica
as respostas aos registros manuais de 1a fase no parquet.

Formatos suportados (identificados por inspeção dos PDFs):
- A) grade estreita (2015-2018 wayback/cursocacd; 2024 cebraspe): linha de
     cabecalhos "Questao N" e, abaixo, 4 letras por questao (C/E/X).
- B) grade larga cursocacd (2019-2023): "QUESTǟO N" (mojibake) + linha de
     posicoes 1-4 + linha de letras; '#'/X = anulada. Secoes "Prova Tipo X"
     separam cadernos: usa o primeiro bloco (caderno das provas manuais).
- C) pares Item/Gabarito (2024-2026 cebraspe): linha "Item" com numeros
     (itens continuos) e linha "Gabarito" com as letras; o numero impresso
     e o proprio question_number (formato individual pos-2025).

Pareamento por proximidade de x (coluna), robusto a offsets de renderizacao.

Aplicacao (--apply): sobrescreve answer dos manuais de 1a fase com o
gabarito definitivo (autoridade maxima); X/# -> answer null + nota.

Uso:
    python scripts/extract_gabaritos.py --apply    # extrai tudo e aplica
    python scripts/extract_gabaritos.py --year 2015 --debug
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path

import pandas as pd
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PARQUET = ROOT / "data" / "processed" / "questions.parquet"
CACHE = ROOT / "data" / "processed" / "gabaritos.json"

RE_HEADER = re.compile(r"Quest\S{0,2}O\s*(\d{1,3})", re.I)
RE_ANS = re.compile(r"^[A-Ea-eXx#$☼]$")
RE_TIPO = re.compile(r"(?:prova\s+tipo|caderno)\s*\S{0,3}\s*([A-Da-d])\b", re.I)


def rows_of(page):
    """Agrupa spans em linhas visuais por y (tolerancia 3pt), ordenadas por x."""
    spans = []
    for b in page.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                t = unicodedata.normalize("NFC", s["text"].strip())
                if t:
                    spans.append((s["bbox"][1], s["bbox"][0], t))
    spans.sort()
    rows = []
    for y, x, t in spans:
        if rows and abs(rows[-1][0] - y) <= 3.0:
            rows[-1][1].append((x, t))
        else:
            rows.append([y, [(x, t)]])
    return [sorted(cells) for _, cells in rows]


def nearest_pairs(num_cells, let_cells, tol=14.0):
    """Pareia cada (x, numero) com a letra de x mais proximo."""
    out = []
    for x, t in num_cells:
        best, bx = None, 1e9
        for lx, lt in let_cells:
            d = abs(lx - x)
            if d < bx:
                best, bx = lt, d
        if best is not None and bx <= tol:
            out.append((int(t), best))
    return out


def parse_pdf(pdf: Path) -> dict[tuple[int, int], tuple[str, str]]:
    out: dict[tuple[int, int], tuple[str, str]] = {}
    caderno = "A"
    with pymupdf.open(pdf) as doc:
        full = " ".join(pg.get_text("text") for pg in doc)
        # gabaritos do TPS (pre-selecao 2005-2008) usam grade TRANSPOSTA
        # (linhas = itens, colunas = questoes) e nao correspondem a prova
        # objetiva do dataset: ignora o arquivo inteiro
        if re.search(r"\bTPS\b|PR[ÉE]-SELE[ÇC][ÃA]O", full):
            return {}
        for page in doc:
            rows = rows_of(page)
            i, n = 0, len(rows)
            while i < n:
                cells = rows[i]
                texts = [t for _, t in cells]
                joined = " ".join(texts)
                mt = RE_TIPO.search(joined)
                if mt and len(texts) <= 3:
                    caderno = mt.group(1).upper()
                    i += 1
                    continue

                # formato C: "Item" + numeros, seguido de "Gabarito" + letras
                if any(t.lower() == "item" for t in texts) and i + 1 < n:
                    num_cells = [
                        (x, t)
                        for x, t in cells
                        if re.fullmatch(r"\d{1,3}", t) and 1 <= int(t) <= 300
                    ]
                    let_cells = [(x, t) for x, t in rows[i + 1] if RE_ANS.match(t)]
                    if len(num_cells) >= 4 and len(let_cells) >= 4:
                        for item, ll in nearest_pairs(num_cells, let_cells):
                            out.setdefault((item, 1), (ll, caderno))
                        i += 2
                        continue

                # formato D (era antiga 2004-2010): linha de ~30 numeros de item
                # seguida de linha com as letras (células podem mesclar varios
                # tokens; pareia pela ordem dos tokens; ☼ = anulada)
                num_tokens: list[str] = []
                for _, t in cells:
                    num_tokens.extend(t.split())
                if (
                    len(num_tokens) >= 10
                    and all(re.fullmatch(r"\d{1,3}", tk) for tk in num_tokens)
                    and i + 1 < n
                ):
                    let_tokens: list[str] = []
                    for _, t in rows[i + 1]:
                        let_tokens.extend(t.split())
                    lets: list[str] = []
                    for tk in let_tokens:
                        u = tk.upper()
                        if u in ("X", "#", "☼"):
                            lets.append("X")
                        elif RE_ANS.match(u):
                            lets.append(u)
                    if len(lets) >= 10 and abs(len(lets) - len(num_tokens)) <= 3:
                        for nn, ll in zip(num_tokens, lets):
                            if 1 <= int(nn) <= 300:
                                out.setdefault((int(nn), 1), (ll, caderno))
                        i += 2
                        continue

                # formato E (2011-2013): "Questao N" (ou numero) + letras na
                # mesma linha, 1-4 itens por questao (A-D = multipla escolha)
                if len(cells) >= 2:
                    first = texts[0].strip()
                    me = RE_HEADER.fullmatch(first) or re.fullmatch(r"(\d{1,3})", first)
                    if me:
                        qn = int(me.group(1))
                        lets = [t for _, t in cells[1:] if RE_ANS.match(t)]
                        # questoes reais tem <= 5 itens; linhas com mais letras
                        # sao grade transposta do TPS (linha = item, coluna =
                        # questao) e seriam armazenadas invertidas
                        if lets and 1 <= qn <= 300 and len(lets) <= 6:
                            for pos, ll in enumerate(lets, 1):
                                out.setdefault((qn, pos), (ll, caderno))
                            i += 1
                            continue

                heads = []
                for _, t in cells:
                    m = RE_HEADER.search(t)
                    if m:
                        heads.append(int(m.group(1)))
                if heads:
                    # formato B: posicoes 1-4 entre cabecalho e letras
                    if i + 2 < n:
                        pos_cells = [
                            (x, t) for x, t in rows[i + 1] if re.fullmatch(r"[1-4]", t)
                        ]
                        let_cells = [(x, t) for x, t in rows[i + 2] if RE_ANS.match(t)]
                        if len(pos_cells) >= 4 and len(let_cells) >= 4:
                            pairs = nearest_pairs(pos_cells, let_cells)
                            for j, (pos, ll) in enumerate(pairs):
                                qn = (
                                    heads[j // 4]
                                    if len(pairs) == 4 * len(heads)
                                    else heads[min(j // 4, len(heads) - 1)]
                                )
                                out.setdefault((qn, pos), (ll, caderno))
                            i += 3
                            continue
                    # formato A: letras direto abaixo (4 por questao)
                    if i + 1 < n:
                        lets = [t for _, t in rows[i + 1] if RE_ANS.match(t)]
                        if len(lets) >= 4 * len(heads):
                            for k, qn in enumerate(heads):
                                for p, ll in enumerate(lets[k * 4 : (k + 1) * 4], 1):
                                    out.setdefault((qn, p), (ll, caderno))
                            i += 2
                            continue
                i += 1
    return out


def year_folder(year: int) -> Path | None:
    for cand in (RAW / f"CACD_{year}", RAW / f"CACD_{year}_{year + 1}"):
        if cand.exists():
            return cand
    return None


def collect_year(year: int) -> dict[tuple[int, int], tuple[str, str]]:
    folder = year_folder(year)
    if not folder:
        return {}
    pdfs = sorted(
        p
        for p in folder.rglob("gabarito*.pdf")
        if "justificativa" not in p.name.lower()
    )

    def rank(p: Path) -> int:
        s = p.name.lower()
        if "definitivo" in s:
            return 0
        if "preliminar" in s:
            return 2
        return 1

    merged: dict[tuple[int, int], tuple[str, str]] = {}
    for pdf in sorted(pdfs, key=rank):
        g = parse_pdf(pdf)
        print(f"     {pdf.parent.name}/{pdf.name}: {len(g)} respostas")
        for k, v in g.items():
            merged.setdefault(k, v)
    return merged


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--year", type=int, action="append")
    ap.add_argument("--debug", action="store_true")
    ap.add_argument("--no-apply", action="store_true")
    args = ap.parse_args()
    years = args.year or list(range(2015, 2027))

    all_g: dict[str, dict[str, str]] = {}
    for y in years:
        print(f"== {y}")
        g = collect_year(y)
        if not g:
            print(f"[!!] {y}: nenhum gabarito extraido")
            continue
        xs = sum(1 for v, _ in g.values() if v.upper() in ("X", "#"))
        qs = sorted({qn for qn, _ in g})
        print(
            f"[ok] {y}: {len(g)} respostas | questoes {qs[0]}-{qs[-1]} | anuladas: {xs}"
        )
        all_g[str(y)] = {f"{qn}:{itn}": v for (qn, itn), (v, _) in g.items()}

    CACHE.parent.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(all_g, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"[ok] cache: {CACHE} ({sum(len(v) for v in all_g.values())} respostas)")

    if args.debug or args.no_apply:
        return

    df = pd.read_parquet(PARQUET)
    # preenche manual E rules de 1a fase (as rules complementares de
    # 2011/2013/2014 tambem recebem o gabarito oficial)
    m = df.stage.eq("primeira_fase") & df.extraction_method.isin(["manual", "rules"])
    filled = anul = override = 0
    for idx, row in df[m].iterrows():
        y = str(int(row["year"]))
        qn = row["question_number"]
        if pd.isna(qn):
            continue
        qn_i = int(float(qn))
        itn_i = 1 if pd.isna(row["item_number"]) else int(float(row["item_number"]))
        letter = (all_g.get(y) or {}).get(f"{qn_i}:{itn_i}")
        if not letter:
            continue
        letter = letter.upper()
        if letter in ("X", "#", "☼"):
            letter = None  # anulada
        cur = row["answer"]
        has = not pd.isna(cur) and bool(str(cur).strip())
        if letter is None:
            if has:
                override += 1
                df.at[idx, "answer"] = None
                df.at[idx, "notes"] = "item anulado no gabarito definitivo"
            continue
        if has:
            if str(cur).strip().upper() != letter:
                override += 1
            df.at[idx, "answer"] = letter
        else:
            df.at[idx, "answer"] = letter
            filled += 1
    df.to_parquet(PARQUET, index=False)
    print(f"[ok] parquet: {filled} preenchidas, {override} sobrescritas/corrigidas")

    mm = df[df.extraction_method.eq("manual") & df.stage.eq("primeira_fase")]
    for y, grp in mm.groupby("year"):
        tot = len(grp)
        with_ans = grp.answer.notna() & grp.answer.astype(str).str.strip().ne("")
        print(f"  {y}: {int(with_ans.sum())}/{tot} com resposta")


if __name__ == "__main__":
    main()
