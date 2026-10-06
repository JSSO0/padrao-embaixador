"""
CACD Forecast AI - Etapa 3: downloader de PDFs.
Le os catalogos em data/metadata/, baixa apenas URLs de PDF/arquivo verificadas,
grava em data/raw/<contest_id>/<familia>/ com manifest e checksum SHA-256.

Uso:
    python scraper/download.py            # baixa tudo pendente (retomavel)
    python scraper/download.py --dry-run  # lista sem baixar
"""

import csv
import hashlib
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
MANIFEST = RAW / "download_manifest.csv"
HEADERS = {"User-Agent": "Mozilla/5.0 (research; cacd-forecast-data-collection)"}

# hint de origem -> (familia de pasta, delay segundos)
FAMILY = {
    "official_cebraspe": ("cebraspe", 0.4),
    "official_mre": ("mre", 0.6),
    "official_cebraspe_archive": ("wayback", 1.2),
    "secondary_repository": ("secondary", 0.6),
    "official_dou": ("dou", 1.0),
}

# statuses aceitaveis para download
OK_STATUS = {
    "VERIFIED_PDF",
    "VERIFIED_ITEM_METADATA",
    "VERIFIED_PDF_PATTERN_48_FILES",
    "EXTRACTED_FROM_LIVE_PAGE",
    "TO_DOWNLOAD_VALIDATE",
}


def family_for(url, source_type):
    """Define familia de pasta e delay a partir da URL (fonte mais confiavel primeiro)."""
    host = urlparse(url).netloc.lower()
    if "web.archive.org" in host:
        return "wayback", 1.2
    if "cdn.cebraspe.org.br" in host:
        return "cebraspe", 0.4
    if "gov.br" in host:
        return "mre", 0.6
    if "archive.org" in host:
        return "archive", 1.5
    if "cursocacd.com" in host:
        return "cursocacd", 0.5
    if "qconcursos.com" in host:
        return "qconcursos", 0.6
    if "clipping.blob.core.windows.net" in host:
        return "clipping", 0.6
    return "secondary", 0.6


def load_jobs():
    jobs = {}

    def add(contest, url, doc):
        if not url or not url.strip():
            return
        url = url.strip()
        if not url.lower().startswith(("http://", "https://")):
            return
        if url in jobs:
            return
        fam, delay = family_for(url)
        jobs[url] = {
            "contest_id": contest or "ALL",
            "family": fam,
            "doc_type": doc or "arquivo",
            "delay": delay,
        }

    def family_for(url):
        host = urlparse(url).netloc.lower()
        if "web.archive.org" in host:
            return "wayback", 1.2
        if "cdn.cebraspe.org.br" in host:
            return "cebraspe", 0.4
        if "gov.br" in host:
            return "mre", 0.6
        if "archive.org" in host:
            return "archive", 1.5
        if "cursocacd.com" in host:
            return "cursocacd", 0.5
        if "qconcursos" in host:
            return "qconcursos", 0.6
        if "clipping.blob.core.windows.net" in host:
            return "clipping", 0.6
        return "secondary", 0.6

    # 1) catalogo oficial (URLs diretas verificadas)
    p = ROOT / "data" / "metadata" / "source_catalog.csv"
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("status") in OK_STATUS and r.get("url"):
                add(r["contest_id"], r["url"], r.get("doc_type"))

    # 2) wayback
    p = ROOT / "data/metadata/wayback_archive.csv"
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("wayback_url"):
                add(r["contest_id"], r["wayback_url"], r.get("doc_type"))

    # 3) curso CACD completo
    p = ROOT / "data/metadata/curso_cacd_full.csv"
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            add(r.get("contest_id"), r.get("url"), r.get("doc_type"))

    # 4) outras secundarias (PDFs diretos e items archive.org)
    p = ROOT / "data/metadata/secondary_sources.csv"
    with p.open(encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r.get("status") in {"VERIFIED_PDF", "VERIFIED_ITEM_METADATA"} and r.get(
                "url"
            ):
                add(r.get("contest_id"), r.get("url"), r.get("doc_type"))

    return jobs


def fetch(sess, url):
    last_err = "desconhecido"
    for attempt in range(3):
        try:
            resp = sess.get(url, timeout=60, headers=HEADERS)
            if resp.status_code == 200:
                return resp
            last_err = f"HTTP {resp.status_code}"
        except requests.RequestException as e:
            last_err = str(e)[:120]
        time.sleep(1.5 * (attempt + 1))
    return last_err


def safe_name(s, maxlen=48):
    s = "".join(c if (c.isalnum() or c in "._-") else "_" for c in s)
    return s[:maxlen]


def main():
    dry = "--dry-run" in sys.argv
    jobs = load_jobs()
    print(f"Jobs: {len(jobs)}")
    if dry:
        for url, j in list(jobs.items())[:15]:
            print(" ", j["contest_id"], j["family"], j["doc_type"], "|", url[:80])
        return

    RAW.mkdir(parents=True, exist_ok=True)
    manifest_fields = [
        "contest_id",
        "family",
        "doc_type",
        "url",
        "file_path",
        "sha256",
        "bytes",
        "http_status",
        "ok",
        "error",
        "downloaded_at",
    ]

    done = set()
    if MANIFEST.exists():
        with MANIFEST.open(encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("ok") == "1":
                    done.add(r["url"])

    new_manifest = not MANIFEST.exists()
    sess = requests.Session()
    with MANIFEST.open("a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=manifest_fields)
        if new_manifest:
            w.writeheader()

        n_ok = n_fail = 0
        for url, j in sorted(
            jobs.items(),
            key=lambda kv: (kv[1]["family"], kv[1]["contest_id"], kv[1]["doc_type"]),
        ):
            if url in done:
                continue

            row = {k: "" for k in manifest_fields}
            row.update(
                {
                    "contest_id": j["contest_id"],
                    "family": j["family"],
                    "doc_type": j["doc_type"],
                    "url": url,
                    "downloaded_at": datetime.now(timezone.utc).isoformat(),
                }
            )

            ext = ".zip" if url.lower().endswith(".zip") else ".pdf"
            target_dir = RAW / j["contest_id"] / j["family"]
            target_dir.mkdir(parents=True, exist_ok=True)
            short_hash = hashlib.sha256(url.encode()).hexdigest()[:8]
            target = target_dir / f"{safe_name(j['doc_type'])}__{short_hash}{ext}"
            row["file_path"] = str(target.relative_to(ROOT))

            if target.exists() and target.stat().st_size > 0:
                # ja existe de execucao anterior (recupera checksum)
                data = target.read_bytes()
                row.update(
                    {
                        "ok": "1",
                        "http_status": "cache",
                        "bytes": len(data),
                        "sha256": hashlib.sha256(data).hexdigest(),
                    }
                )
                w.writerow(row)
                n_ok += 1
                continue

            result = fetch(sess, url)
            if isinstance(result, str):
                row.update({"ok": "0", "error": result})
                w.writerow(row)
                f.flush()
                n_fail += 1
                print(f"[FAIL] {j['contest_id']} {url[:80]} -> {result}")
            else:
                data = result.content
                is_pdf = data[:5] == b"%PDF-"
                is_zip = data[:2] == b"PK"
                if not (is_pdf or is_zip):
                    row.update(
                        {"ok": "0", "error": f"magic bytes invalidos: {data[:12]!r}"}
                    )
                    w.writerow(row)
                    f.flush()
                    n_fail += 1
                    print(f"[MAGIC] {j['contest_id']} {url[:80]}")
                else:
                    target.write_bytes(data)
                    row.update(
                        {
                            "ok": "1",
                            "http_status": result.status_code,
                            "bytes": len(data),
                            "sha256": hashlib.sha256(data).hexdigest(),
                        }
                    )
                    w.writerow(row)
                    f.flush()
                    n_ok += 1
                    if n_ok % 25 == 0:
                        print(f"  ... ok={n_ok} falhas={n_fail}")

            time.sleep(j["delay"])

    print(f"CONCLUIDO: ok={n_ok} falhas={n_fail}")


if __name__ == "__main__":
    main()
