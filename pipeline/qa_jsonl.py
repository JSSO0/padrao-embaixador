"""QA rapido do JSONL extraido: mostra questoes especificas."""

import json
import sys
from pathlib import Path

path = Path(sys.argv[1])
qns = [
    int(x) for x in (sys.argv[2].split(",") if len(sys.argv) > 2 else ["1", "2", "3"])
]
recs = [json.loads(l) for l in path.open(encoding="utf-8")]

for qn in qns:
    rs = [r for r in recs if r["question_number"] == qn]
    if not rs:
        print(f"== Q{qn}: SEM REGISTROS")
        continue
    r0 = rs[0]
    print("=" * 100)
    print(f"Q{qn} | disc: {r0['discipline']} | page: {r0['page']}")
    print("QT:", (r0["question_text"] or "")[:500].replace("\n", " / "))
    for x in rs:
        print(
            f"  item {x['item_number']}:",
            (x["item_text"] or "")[:180].replace("\n", " / "),
        )
