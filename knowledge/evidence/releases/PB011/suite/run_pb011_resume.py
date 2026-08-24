#!/usr/bin/env python3
"""PB-011 resume — remaining personas after beginner/average PASS.

Re-runs advanced (fresh provision; prior attempt stalled mid CL-D3 reflection),
returning, and struggling. Merges with existing persona results.
"""
from __future__ import annotations

import importlib.util
import json
import runpy
import sys
from pathlib import Path

ROOT = Path("/tmp/pb011")
SUITE = ROOT / "suite" / "run_pb011.py"
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB011")

# Refresh suite copy
src = EVID_REPO / "suite" / "run_pb011.py"
SUITE.write_text(src.read_text())

spec = importlib.util.spec_from_file_location("pb011", str(SUITE))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# Keep PASS personas
keep = []
for slug in ("beginner", "average"):
    p = EVID_REPO / "personas" / f"{slug}.json"
    if not p.exists():
        p = ROOT / "evidence" / slug / "persona.json"
    if not p.exists():
        print("MISSING keep persona", slug)
        sys.exit(2)
    keep.append(json.loads(p.read_text()))
    print("KEEP", slug, keep[-1].get("verdict"), flush=True)

resume_slugs = ("advanced", "returning", "struggling")
personas = [p for p in m.PERSONAS if p["slug"] in resume_slugs]

# Clear stale advanced working dir for fresh run
adv = ROOT / "evidence" / "advanced"
if adv.exists():
    # leave stuck archive; wipe live working tree for fresh files
    for f in adv.iterdir():
        if f.is_file():
            f.unlink()

probe = m.mod.Client("pb011_resume_probe")
probe.html_dir = m.HTML / "resume_probe"
probe.html_dir.mkdir(parents=True, exist_ok=True)
health = m.mod.fingerprint(probe)
if health.get("commit") != m.EXPECTED_COMMIT:
    print("FINGERPRINT FAIL", health)
    sys.exit(1)

results = list(keep)
for p in personas:
    results.append(m.run_persona(p))

# Aggregate as main()
pass_n = sum(1 for r in results if r.get("verdict") == "PASS")
scores = []
for r in results:
    for t in (r.get("summary") or {}).get("trajectory") or []:
        scores.append(t["score_over_9"])
mean_score = (sum(scores) / len(scores)) if scores else 0.0
regression = m.regression_vs_lambda(results)
prog = m.aggregate_programme_metrics(results)
if not regression.get("cross_persona_sequence_consistent"):
    prog["recommendation_consistency"]["result"] = "FAIL"
    prog["recommendation_consistency"]["note"] = "cross-persona sequence mismatch"

all_defects = []
for r in results:
    all_defects.extend((r.get("summary") or {}).get("defects") or [])
seen_d = set()
deduped = []
for d in all_defects:
    key = (d.get("id"), d.get("finding"), d.get("severity"))
    if key in seen_d:
        continue
    seen_d.add(key)
    deduped.append(d)

critical = [d for d in deduped if d.get("severity") == "Critical"]
major = [d for d in deduped if d.get("severity") == "Major"]
prog_all_pass = all(v.get("result") == "PASS" for v in prog.values())

overall = (
    "PASS"
    if pass_n == len(m.PERSONAS)
    and mean_score >= 8.0
    and not regression.get("regression_detected")
    and not critical
    and not major
    and prog_all_pass
    else "FAIL"
)

out = {
    "programme": "PB-011 Progressive Educational Confidence (Lambda)",
    "host": m.mod.BASE,
    "expected_commit": m.EXPECTED_COMMIT,
    "live_health": health,
    "fingerprint_ok": health.get("commit") == m.EXPECTED_COMMIT,
    "live_certified_inventory": m.TARGET,
    "personas": results,
    "cohort": {
        "personas_pass": pass_n,
        "personas_total": len(m.PERSONAS),
        "certified_day_observations": len(scores),
        "mean_score_over_9": mean_score,
        "programme_metrics": prog,
        "defects": deduped,
        "defect_counts": {
            "Critical": len(critical),
            "Major": len(major),
            "Minor": len([d for d in deduped if d.get("severity") == "Minor"]),
            "Cosmetic": len([d for d in deduped if d.get("severity") == "Cosmetic"]),
        },
    },
    "regression_vs_campaign_lambda": regression,
    "resume_note": "advanced re-provisioned after mid-CL-D3 unfinished reflection stall on first attempt; beginner/average retained",
    "verdict": overall,
}
(m.EVID_BASE / "results.json").write_text(json.dumps(out, indent=2, default=str))
(EVID_REPO / "results.json").write_text(json.dumps(out, indent=2, default=str))
(EVID_REPO / "suite" / "run_pb011_resume.py").write_text(Path(__file__).read_text())
print("OVERALL", out["verdict"], "mean", mean_score, "pass", pass_n, flush=True)
sys.exit(0 if overall == "PASS" else 1)
