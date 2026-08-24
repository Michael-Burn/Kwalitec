#!/usr/bin/env python3
"""PB-014 — aggregate persona results into cohort results.json."""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path("/tmp/pb014")
SUITE = ROOT / "suite" / "run_pb014.py"
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB014")

spec = importlib.util.spec_from_file_location("pb014", str(SUITE))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

results = []
for p in m.PERSONAS:
    path = EVID_REPO / "personas" / f"{p['slug']}.json"
    if not path.exists():
        path = ROOT / "evidence" / p["slug"] / "persona.json"
    if not path.exists():
        print("MISSING", p["slug"])
        sys.exit(2)
    results.append(json.loads(path.read_text()))
    print("HAVE", p["slug"], results[-1].get("verdict"), flush=True)

probe = m.mod.Client("pb014_agg_probe")
probe.html_dir = m.HTML / "agg_probe"
probe.html_dir.mkdir(parents=True, exist_ok=True)
health = m.mod.fingerprint(probe)
if health.get("commit") != m.EXPECTED_COMMIT:
    print("FINGERPRINT FAIL", health)
    sys.exit(1)

out = m.build_results(results, health)
(m.EVID_BASE / "results.json").write_text(json.dumps(out, indent=2, default=str))
(EVID_REPO / "results.json").write_text(json.dumps(out, indent=2, default=str))
(EVID_REPO / "suite" / "run_pb014.py").write_text(SUITE.read_text())
(EVID_REPO / "suite" / "aggregate_pb014.py").write_text(Path(__file__).read_text())
print("OVERALL", out["verdict"], "mean", out["cohort"]["mean_score_over_9"], flush=True)
raise SystemExit(0 if out["verdict"] == "PASS" else 1)
