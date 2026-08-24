#!/usr/bin/env python3
"""PB-016 — aggregate persona results into cohort results.json."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

SUITE = Path("/tmp/pb016/suite/run_pb016.py")
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB016")

spec = importlib.util.spec_from_file_location("pb016", str(SUITE))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

results = []
for p in m.PERSONAS:
    path = EVID_REPO / "personas" / f"{p['slug']}.json"
    if not path.exists():
        print(f"missing {path}")
        continue
    results.append(json.loads(path.read_text()))

agg = m.aggregate(results)
print(json.dumps({
    "verdict": agg["verdict"],
    "mean": agg["mean_score_over_9"],
    "personas": agg["personas"],
    "regression": agg["regression_vs_ro014"]["regression_detected"],
}, indent=2))
