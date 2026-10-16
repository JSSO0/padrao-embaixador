"""Converte as transcrições .md (JSONL malformado) para .jsonl padronizado.

- Repara JSON: escapes inválidos (ex. "\\["), aspas não escapadas
- Normaliza campos: contest_id/year/phase/stage, question_type, source_file
- Renomeia para o padrao: cacd_<ano>_primeira_fase_prova_objetiva_<n>.jsonl
- Remove o .md original somente apos gravar e revalidar o .jsonl

Uso:
    python scripts/convert_md_transcripts.py            # converte tudo
    python scripts/convert_md_transcripts.py --dry-run  # so relatorio
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from parser.import_manual import iter_objects, repair_unescaped_quotes  # noqa: E402
from parser.parsers.base import normalize_disc  # noqa: E402

# escapes validos em JSON; qualquer outro backslash deve ser duplicado
RE_BAD_ESCAPE = re.compile(r'\\(?!["\\/bfnrtu])')

QTYPE_MAP = {
    "multipla_escolha": "multiple_choice",
    "multipla escolha": "multiple_choice",
    "multiple_choice": "multiple_choice",
    "certo_errado": "certo_errado",
    "certo/errado": "certo_errado",
    "discursiva": "essay",
    "essay": "essay",
}

RE_PARTE = re.compile(r"[_\s-]+(\d+)\s*\.(md|jsonl|txt)$", re.I)


RE_PARTE = re.compile(r"[_\s-]+(\d+)$")


def repair_text(text: str) -> str:
    """Escapa backslashes invalidos (ex. '\\[') sem tocar escapes validos."""
    return RE_BAD_ESCAPE.sub(r"\\\\", text)


# chaves conhecidas do schema (para decidir se aspas+virgula fecha o valor)
KNOWN_KEYS = {
    "contest_id",
    "year",
    "phase",
    "stage",
    "discipline",
    "question_number",
    "item_number",
    "question_type",
    "question_text",
    "item_text",
    "alternatives",
    "answer",
    "page",
    "caderno",
    "source_file",
    "source_url",
    "confidence",
    "notes",
    "parent_question_id",
    # chaves internas do array alternatives
    "letter",
    "text",
}
RE_NEXT_KEY = re.compile(r',\s*"(\w+)"\s*:')  # , "chave":


def fix_quotes(line: str) -> str:
    """Repara uma linha JSONL: aspas internas nao escapadas e escapes
    invalidos, ciente de contexto (dentro/fora de string).

    - fora de string: '\\[' / '\\]' perdem o backslash (colchetes de array)
    - dentro de string: '\\' + char invalido vira backslash dobrado; escapes
      validos sao preservados
    - dentro de string, '"' fecha o valor somente se seguido por ',' +
      chave conhecida, por ':' ou por '}'; aspas internas recebem '\\'
    """
    out: list[str] = []
    i, n = 0, len(line)
    in_str = False
    while i < n:
        c = line[i]
        if not in_str:
            if c == "\\" and i + 1 < n and line[i + 1] in "[]":
                out.append(line[i + 1])  # \[ fora de string = colchete
                i += 2
                continue
            out.append(c)
            if c == '"':
                in_str = True
            i += 1
            continue
        # dentro de string
        if c == "\\" and i + 1 < n:
            nxt = line[i + 1]
            if nxt in '"\\/bfnrtu':
                out.append(line[i : i + 2])  # escape valido: copia o par
            else:  # escape invalido (ex. '\\['): dobra o backslash
                out.append("\\\\")
                out.append(nxt)
            i += 2
            continue
        if c == '"':
            nxt = line[i + 1] if i + 1 < n else ""
            if nxt == ",":
                m = RE_NEXT_KEY.match(line, i + 1)
                if m and m.group(1) in KNOWN_KEYS:
                    in_str = False
                    out.append(c)
                    i += 1
                    continue
            if nxt in ":}":
                in_str = False
                out.append(c)
                i += 1
                continue
            out.append('\\"')  # aspa interna
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def parse_objects(text: str):
    """Tenta camadas de reparo; retorna (objs, camada, truncado)."""
    layers = [
        ("original", text),
        ("fix_quotes", "\n".join(fix_quotes(ln) for ln in text.split("\n"))),
        ("backslash", repair_text(text)),
        (
            "backslash+fix_quotes",
            "\n".join(fix_quotes(ln) for ln in repair_text(text).split("\n")),
        ),
    ]
    for name, t in layers:
        try:
            return list(iter_objects(t)), name, False
        except json.JSONDecodeError:
            continue
    # ultima chance: decodifica o maximo possivel (arquivo truncado no fim)
    best: list = []
    best_stop = 0
    for _name, t in layers:
        dec = json.JSONDecoder()
        i, n = 0, len(t)
        objs: list = []
        while i < n:
            while i < n and t[i] in " \r\n\t":
                i += 1
            if i >= n:
                break
            try:
                obj, j = dec.raw_decode(t, i)
                objs.append(obj)
                i = j
            except json.JSONDecodeError:
                break
        if len(objs) > len(best):
            best, best_stop = objs, i
    return best, "fix_quotes+truncado", best_stop < n * 0.95


def infer_source_file(
    objs: list[dict], year: int, parte: int, contest_dir: Path
) -> str | None:
    """Acha o PDF da prova objetiva correspondente em data/raw/CACD_<ano>/cursocacd."""
    base = ROOT / "data" / "raw" / f"CACD_{year}" / "cursocacd"
    if not base.is_dir():
        return None
    # 1) tenta pelos campos existentes
    for o in objs:
        sf = str(o.get("source_file") or "").strip()
        if sf:
            hits = list(base.glob(f"**/{Path(sf).name}"))
            if hits:
                return hits[0].relative_to(ROOT).as_posix()
    # 2) por parte (prova_objetiva_1 / 2)
    cand = sorted(base.glob(f"prova_objetiva_{parte}__*.pdf"))
    if cand:
        return cand[0].relative_to(ROOT).as_posix()
    # 3) por faixa de questoes: primeira prova cobre qn 1..35 tipicamente
    qns = [o.get("question_number") for o in objs if o.get("question_number")]
    if qns:
        mx = max(int(q) for q in qns)
        parte2 = 2 if mx > 35 else 1
        cand = sorted(base.glob(f"prova_objetiva_{parte2}__*.pdf"))
        if cand:
            return cand[0].relative_to(ROOT).as_posix()
    return None


def normalize(obj: dict, year: int, source_file: str | None, parte_hint: str) -> dict:
    out = dict(obj)
    out["contest_id"] = f"CACD_{year}"
    out["year"] = year
    phase = out.get("phase")
    try:
        phase = int(phase)
    except Exception:
        phase = 1
    out["phase"] = phase
    stage = out.get("stage")
    if not stage:
        stage = "primeira_fase" if phase == 1 else "segunda_fase"
    out["stage"] = str(stage)
    qt = QTYPE_MAP.get(str(out.get("question_type") or "").strip().lower())
    if qt:
        out["question_type"] = qt
    if out.get("discipline"):
        out["discipline"] = normalize_disc(out["discipline"])
    if source_file:
        out["source_file"] = source_file
    out.setdefault("page", None)
    out.setdefault("caderno", None)
    out.setdefault("source_url", None)
    out.setdefault(
        "confidence", None if out.get("confidence") is None else out["confidence"]
    )
    out.setdefault("notes", None)
    if parte_hint and "parte" not in out:
        pass
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted((ROOT / "data/raw").rglob("*.md"))
    print(f"arquivos .md: {len(files)}")
    for p in files:
        rel = p.relative_to(ROOT)
        year = int(p.parent.parent.name.replace("CACD_", "").split("_")[0])
        m = RE_PARTE.search(p.stem)
        parte = int(m.group(1)) if m else 1
        text = p.read_text(encoding="utf-8", errors="replace").lstrip("\ufeff \r\n\t")
        objs, layer, truncado = parse_objects(text)
        if not objs:
            print(f"[ERRO] {rel}: JSON irrecuperavel mesmo com reparos")
            continue
        src = infer_source_file(objs, year, parte, p.parent)
        objs_norm = [normalize(o, year, src, parte) for o in objs]
        new_name = f"cacd_{year}_primeira_fase_prova_objetiva_{parte}.jsonl"
        new_path = p.parent / new_name
        aviso = (
            " [TRUNCADO no arquivo original: ultimo objeto descartado]"
            if truncado
            else ""
        )
        print(
            f"[ok] {rel.name} -> {new_name}: {len(objs)} objetos (reparo: {layer}, fonte: {Path(src).name if src else 'N/D'}){aviso}"
        )
        if args.dry_run:
            continue
        with new_path.open("w", encoding="utf-8") as f:
            for o in objs_norm:
                f.write(json.dumps(o, ensure_ascii=False) + "\n")
        # revalida antes de remover o original
        check, _, _ = parse_objects(new_path.read_text(encoding="utf-8"))
        if len(check) == len(objs):
            p.unlink()
        else:
            print(f"[ERRO] revalidacao falhou para {new_name}; .md mantido")


if __name__ == "__main__":
    main()
