#!/usr/bin/env python3
from __future__ import annotations
import importlib.util, json, sys
from pathlib import Path

spec = importlib.util.spec_from_file_location("pb010", "/tmp/pb010/suite/run_pb010.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

m.PERSONAS = [p for p in m.PERSONAS if p["slug"] != "beginner"]
print("Resuming:", [p["slug"] for p in m.PERSONAS], flush=True)

probe = m.mod.Client("pb010_probe_resume")
probe.html_dir = m.HTML / "probe_resume"
probe.html_dir.mkdir(parents=True, exist_ok=True)
health = m.mod.fingerprint(probe)
if health.get("commit") != m.EXPECTED_COMMIT:
    print("FINGERPRINT FAIL", health.get("commit")); sys.exit(1)

results = [json.loads((m.EVID_REPO / "personas" / "beginner.json").read_text())]
for p in m.PERSONAS:
    results.append(m.run_persona(p))

pass_n = sum(1 for r in results if r.get("verdict") == "PASS")
scores = [t["score_over_9"] for r in results for t in (r.get("summary") or {}).get("trajectory") or []]
mean_score = (sum(scores) / len(scores)) if scores else 0.0
regression = m.regression_vs_kappa(results)
prog = m.aggregate_programme_metrics(results)
if not regression.get("cross_persona_sequence_consistent"):
    prog["recommendation_consistency"]["result"] = "FAIL"
    prog["recommendation_consistency"]["note"] = "cross-persona sequence mismatch"

all_defects = []
for r in results:
    all_defects.extend((r.get("summary") or {}).get("defects") or [])
seen=set(); deduped=[]
for d in all_defects:
    key=(d.get("id"), d.get("finding"), d.get("severity"))
    if key in seen: continue
    seen.add(key); deduped.append(d)
critical=[d for d in deduped if d.get("severity")=="Critical"]
major=[d for d in deduped if d.get("severity")=="Major"]
prog_all_pass=all(v.get("result")=="PASS" for v in prog.values())
overall = (
    "PASS" if pass_n==len(results) and mean_score>=8.0 and not regression.get("regression_detected")
    and not critical and not major and prog_all_pass else "FAIL"
)
out={
    "programme":"PB-010 Progressive Educational Confidence (Kappa)",
    "host": m.mod.BASE,
    "expected_commit": m.EXPECTED_COMMIT,
    "live_health": health,
    "fingerprint_ok": True,
    "live_certified_inventory": m.TARGET,
    "personas": results,
    "cohort": {
        "personas_pass": pass_n,
        "personas_total": len(results),
        "certified_day_observations": len(scores),
        "mean_score_over_9": mean_score,
        "programme_metrics": prog,
        "defects": deduped,
        "defect_counts": {
            "Critical": len(critical),
            "Major": len(major),
            "Minor": len([d for d in deduped if d.get("severity")=="Minor"]),
            "Cosmetic": len([d for d in deduped if d.get("severity")=="Cosmetic"]),
        },
    },
    "regression_vs_campaign_kappa": regression,
    "verdict": overall,
    "notes": [
        "Honest Kappa stop copy ('do not begin syllabus 3.2') is not a Critical leak",
        "beginner salvaged after classifier fix; remaining personas run with fixed classifier",
    ],
}
(m.EVID_BASE/"results.json").write_text(json.dumps(out, indent=2, default=str))
(m.EVID_REPO/"results.json").write_text(json.dumps(out, indent=2, default=str))
(m.EVID_REPO/"suite"/"run_pb010.py").write_text(Path("/tmp/pb010/suite/run_pb010.py").read_text())
print("OVERALL", overall, "mean", mean_score, flush=True)
sys.exit(0 if overall=="PASS" else 1)
