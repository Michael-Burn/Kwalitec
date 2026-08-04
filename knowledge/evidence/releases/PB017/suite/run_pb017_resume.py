#!/usr/bin/env python3
"""PB-016 resilient resume — continue an existing Internal Alpha persona from checkpoint.

Never replays already-certified Pi sittings. Ops-only Continue Session recovery.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

SUITE = Path("/tmp/pb017/suite/run_pb017.py")
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB017")
CKPT_DIR = EVID_REPO / "checkpoints"

spec = importlib.util.spec_from_file_location("pb017", str(SUITE))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def load_ckpt(slug: str) -> dict:
    path = CKPT_DIR / f"{slug}.json"
    if not path.exists():
        raise SystemExit(f"no checkpoint for {slug}")
    return json.loads(path.read_text())


def persona_by_slug(slug: str) -> dict:
    for p in m.PERSONAS:
        if p["slug"] == slug:
            return p
    raise SystemExit(f"unknown persona {slug}")


def resume_persona(slug: str) -> dict:
    ck = load_ckpt(slug)
    persona = persona_by_slug(slug)
    email = ck["email"]
    password = m.PASS_FILE.read_text().strip()
    certified = set(ck.get("certified_days_complete") or [])
    print(f"=== resume {slug} {email} certified={sorted(certified)}", flush=True)

    health = m.check_fingerprint()
    if health.get("commit") != m.EXPECTED_COMMIT:
        ops = {
            "event": "Operational Reliability Event",
            "class": "deployment_fingerprint_change",
            "observed": health.get("commit"),
            "expected": m.EXPECTED_COMMIT,
            "persona": slug,
            "at": datetime.now(timezone.utc).isoformat(),
        }
        (EVID_REPO / "ops" / f"fingerprint_resume_{slug}_{int(time.time())}.json").write_text(
            json.dumps(ops, indent=2)
        )
        return {
            "slug": slug,
            "verdict": "FAIL",
            "reason": "fingerprint mismatch on resume",
            "live_health": health,
        }

    evid = m.EVID_BASE / slug
    html_dir = m.HTML / slug
    evid.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "html" / slug).mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "audits" / slug).mkdir(parents=True, exist_ok=True)

    c = m.ro.wait_login(f"{slug}_resume", email, password, attempts=18)
    if not c:
        return {"slug": slug, "email": email, "verdict": "FAIL", "reason": "login failed"}
    c.html_dir = html_dir
    m.ro.HTML = m.HTML
    m.ro.EVID = evid
    m.ro.EVID_REPO = EVID_REPO

    complete = m.patch_session_answers(persona)
    seen = {d: {"day": d} for d in certified}
    trajectory = list(ck.get("certified_trajectory") or [])
    programme_traj = [t.get("programme_metrics") or {} for t in trajectory]
    all_defects = []
    transit_days = list(ck.get("transit_observations") or [])
    last_detected = ck.get("last_transit_verified")
    consecutive_fallback = 0
    idx = int(ck.get("ops_day_index") or 1)

    for _n in range(30):
        if all(k in seen for k in m.TARGET):
            break
        print(f"  day {idx} cp_seen={sorted(seen)} last={last_detected}", flush=True)
        try:
            health = m.check_fingerprint()
            if health.get("commit") != m.EXPECTED_COMMIT:
                m.save_runtime_checkpoint(
                    slug,
                    email,
                    seen,
                    last_detected,
                    transit_days,
                    trajectory,
                    all_defects,
                    idx,
                    status="paused_fingerprint",
                )
                break

            _, _, home = c.get("/student/")
            sig = m.ro.extract_mission_signals(home)
            if sig["day_complete"] or not sig["has_start"]:
                st = m.resilient_backdate(email)
                if st.get("status") != "succeeded":
                    return {
                        "slug": slug,
                        "email": email,
                        "verdict": "FAIL",
                        "reason": f"backdate failed {st}",
                    }
                time.sleep(2)
                c = m.ro.wait_login(f"{slug}_r{idx}", email, password, attempts=8)
                if not c:
                    return {
                        "slug": slug,
                        "email": email,
                        "verdict": "FAIL",
                        "reason": "relogin failed",
                    }
                c.html_dir = html_dir

            expect = next((d for d in m.TARGET if d not in seen), "CP-R1")
            day_out = complete(c, idx, expect)
            actual = m.detect(day_out)
            audit0 = (day_out.get("reading") or {}).get("audit") or {}
            if (
                actual
                and actual.startswith("CP-")
                and not day_out.get("finished")
                and not audit0.get("is_fallback_shell")
            ):
                print(f"  RETRY unfinished {actual}", flush=True)
                time.sleep(2)
                day_out = complete(c, idx, actual)
                actual = m.detect(day_out) or actual
            if actual:
                last_detected = actual

            audit = (day_out.get("reading") or {}).get("audit") or {}
            if audit.get("is_fallback_shell") or (
                not day_out.get("finished") and not actual
            ):
                consecutive_fallback += 1
            else:
                consecutive_fallback = 0
            if consecutive_fallback >= 8:
                break

            if actual and actual.startswith("CP-"):
                if actual in seen:
                    print(f"  skip already-certified {actual}", flush=True)
                else:
                    day_out = m.score_cp(day_out, actual)
                    metrics = m.programme_metrics_for_day(
                        day_out, actual, [t["day"] for t in trajectory]
                    )
                    day_out["programme_metrics"] = metrics
                    if day_out.get("verdict") == "PASS":
                        seen[actual] = day_out
                        trajectory.append(
                            {
                                "day": actual,
                                "package_id": day_out.get("package_id"),
                                "confidence_level": day_out["confidence_level"],
                                "score_over_9": day_out["score_over_9"],
                                "dimensions": day_out["dimensions"],
                                "programme_metrics": metrics,
                                "residuals": day_out.get("residuals") or [],
                                "chrome_residual": bool(day_out.get("chrome_residual")),
                                "revision_q6_residual": bool(
                                    day_out.get("revision_q6_residual")
                                ),
                            }
                        )
                        programme_traj.append(metrics)
                        print(
                            f"  SCORED {actual} {day_out['score_over_9']}/9",
                            flush=True,
                        )
                        m.save_runtime_checkpoint(
                            slug,
                            email,
                            seen,
                            last_detected,
                            transit_days,
                            trajectory,
                            all_defects,
                            idx,
                        )
                    lean = {
                        "expected_day": day_out.get("expected_day"),
                        "detected_campaign_day": actual,
                        "finished": day_out.get("finished"),
                        "verdict": day_out.get("verdict"),
                        "score_over_9": day_out.get("score_over_9"),
                        "dimensions": day_out.get("dimensions"),
                        "programme_metrics": metrics,
                        "checklist": day_out.get("checklist"),
                        "residuals": day_out.get("residuals"),
                        "package_id": day_out.get("package_id"),
                    }
                    (EVID_REPO / "audits" / slug / f"day{idx}_{actual}.json").write_text(
                        json.dumps(lean, indent=2, default=str)
                    )
            else:
                transit_days.append(actual)
                print(f"  transit detected={actual}", flush=True)

            if day_out.get("finished") or consecutive_fallback:
                m.resilient_backdate(email)
                time.sleep(2)
                c2 = m.ro.wait_login(f"{slug}_a{idx}", email, password, attempts=8)
                if c2:
                    c = c2
                    c.html_dir = html_dir
            idx += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  ERROR {exc}", flush=True)
            time.sleep(5)
            c = m.ro.wait_login(f"{slug}_e{idx}", email, password, attempts=8)
            if not c:
                return {
                    "slug": slug,
                    "email": email,
                    "verdict": "FAIL",
                    "reason": f"exception {exc}",
                }
            c.html_dir = html_dir
            idx += 1

    certified_all = all(k in seen for k in m.TARGET)
    scores = [t["score_over_9"] for t in trajectory]
    avg = (sum(scores) / len(scores)) if scores else 0.0
    levels = [t["confidence_level"] for t in trajectory]
    rank = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    stable = (
        all(rank[levels[i]] <= rank[levels[i + 1]] for i in range(len(levels) - 1))
        if len(levels) > 1
        else True
    )
    prog_keys = [
        "recommendation_consistency",
        "weak_area_identification",
        "mission_sequencing",
        "syllabus_continuity",
        "confidence_calibration",
        "explanation_usefulness",
    ]
    prog_agg = {}
    for k in prog_keys:
        vals = [mtr.get(k) for mtr in programme_traj if mtr]
        prog_agg[k] = {
            "pass_count": sum(1 for v in vals if v == "PASS"),
            "total": len(vals),
            "result": "PASS" if vals and all(v == "PASS" for v in vals) else "FAIL",
        }
    verdict = "PASS" if certified_all and avg >= 8.0 and stable else "FAIL"
    out = {
        "slug": slug,
        "label": persona["label"],
        "email": email,
        "persona_profile": {
            "exam_history": persona.get("exam_history"),
            "confidence": persona.get("confidence"),
            "answer_style": persona.get("answer_style"),
        },
        "verdict": verdict,
        "resumed": True,
        "entry": "Seeded Continuity Front advanced student (CO-R1 package history) → Memory Front CP-D1…CP-R1",
        "live_tip": m.EXPECTED_COMMIT,
        "summary": {
            "certified_days_scored": len(trajectory),
            "certified_all_pass": certified_all,
            "avg_score_over_9": avg,
            "trajectory": trajectory,
            "stable_high": stable and all(l == "HIGH" for l in levels),
            "programme_metrics": prog_agg,
            "transit_observations": transit_days,
            "defects": all_defects,
            "defect_counts": {"Critical": 0, "Major": 0, "Minor": 0, "Cosmetic": 0},
        },
    }
    prior = EVID_REPO / "personas" / f"{slug}.json"
    if prior.exists():
        (EVID_REPO / "personas" / f"{slug}.pre_resume.json").write_text(prior.read_text())
    (EVID_REPO / "personas" / f"{slug}.json").write_text(json.dumps(out, indent=2, default=str))
    m.save_runtime_checkpoint(
        slug,
        email,
        seen,
        last_detected,
        transit_days,
        trajectory,
        all_defects,
        idx,
        status="complete" if verdict == "PASS" else "finished_fail",
    )
    print(f"persona {slug} {verdict} avg={avg}", flush=True)
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("Usage: run_pb017_resume.py <slug>")
    slug = sys.argv[1]
    result = resume_persona(slug)
    print(json.dumps({"slug": result.get("slug"), "verdict": result.get("verdict")}, indent=2))
    raise SystemExit(0 if result.get("verdict") == "PASS" else 1)
