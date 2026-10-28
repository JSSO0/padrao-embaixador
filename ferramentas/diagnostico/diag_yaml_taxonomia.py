# -*- coding: utf-8 -*-
"""Valida a estrutura do taxonomia.yaml (M2.1)."""

import sys
from pathlib import Path

import yaml

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
d = yaml.safe_load(
    (Path(__file__).resolve().parents[2] / "data/metadata/taxonomia.yaml").read_text(
        encoding="utf-8"
    )
)["taxonomia"]
print("version:", d["version"], "| metodo:", d["metodo"])
for disc, temas in d["disciplinas"].items():
    print(f"  {disc}: {len(temas)} temas | fallback={d['fallback'][disc]}")
