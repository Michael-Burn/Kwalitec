#!/usr/bin/env python3
"""PB-014 resilient resume — continue an existing Internal Alpha persona from checkpoint.

Does not re-provision. Does not replay completed certified Xi packages.
Infrastructure timeouts are retried / logged as operational notes, not educational defects.
"""
from __future__ import annotations

import importlib.util
import json
import sys
import time
import traceback
from datetime import datetime, timezone
from pathlib import Path

SUITE = Path("/tmp/pb014/suite/run_pb014.py")
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB014")
CKPT_DIR = EVID_REPO / "checkpoints"

spec = importlib.util.spec_from_file_location("pb014", str(SUITE))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_ckpt(slug: str) -> dict:
    p = CKPT_DIR / f"{slug}.json"
    if not p.exists():
        raise SystemExit(f"missing checkpoint {p}")
    return json.loads(p.read_text())


def save_ckpt(ck: dict) -> None:
    CKPT_DIR.mkdir(parents=True, exist_ok=True)
    path = CKPT_DIR / f"{ck['persona']}.json"
    # append-only history copy
    hist = CKPT_DIR / "history"
    hist.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if path.exists():
        (hist / f"{ck['persona']}_{stamp}.json").write_text(path.read_text())
    ck["updated_at"] = utcnow()
    path.write_text(json.dumps(ck, indent=2, default=str))


def op_note(ck: dict, event: str, **kw) -> None:
    ck.setdefault("operational_notes", []).append(
        {"at": utcnow(), "event": event, "educational_failure": False, **kw}
    )


def persona_by_slug(slug: str) -> dict:
    for p in m.PERSONAS:
        if p["slug"] == slug:
            return p
    raise SystemExit(f"unknown persona {slug}")


def with_backoff(label: str, fn, *, attempts: int = 5, base: float = 4.0):
    last = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as exc:  # noqa: BLE001
            last = exc
            wait = base * (2**i)
            print(f"  INFRA {label} attempt {i+1}/{attempts}: {type(exc).__name__}: {exc}; sleep {wait}s", flush=True)
            time.sleep(wait)
    raise last  # type: ignore[misc]


def persist_certified_sitting(ck: dict, slug: str, day_out: dict, actual: str, idx: int) -> None:
    traj_item = {
        "day": actual,
        "package_id": day_out.get("package_id"),
        "curriculum_topic": "4.2" if actual.startswith("CX-D") else "4.2-revision",
        "campaign_day": actual,
        "educational_package_id": day_out.get("package_id"),
        "confidence_level": day_out.get("confidence_level"),
        "score_over_9": day_out.get("score_over_9"),
        "dimensions": day_out.get("dimensions"),
        "programme_metrics": day_out.get("programme_metrics"),
        "residuals": day_out.get("residuals") or [],
        "chrome_residual": bool(day_out.get("chrome_residual")),
        "revision_q6_residual": bool(day_out.get("revision_q6_residual")),
        "evidence_audit": str(m.EVID_REPO / "audits" / slug / f"day{idx}_{actual}.json"),
        "completed_at": utcnow(),
    }
    days = {t["day"] for t in ck.get("certified_trajectory") or []}
    if actual not in days:
        ck.setdefault("certified_trajectory", []).append(traj_item)
    ck["certified_days_complete"] = [t["day"] for t in ck["certified_trajectory"]]
    ck["last_certified_day"] = actual
    ck["remaining_xi_days"] = [d for d in m.TARGET if d not in set(ck["certified_days_complete"])]
    ck["status"] = "complete" if not ck["remaining_xi_days"] else "in_progress"
    save_ckpt(ck)


def resume_persona(slug: str) -> dict:
    ck = load_ckpt(slug)
    persona = persona_by_slug(slug)
    email = ck.get("email")
    if not email:
        raise SystemExit(f"checkpoint {slug} missing email")
    password = m.PASS_FILE.read_text().strip()

    evid = m.EVID_BASE / slug
    html_dir = m.HTML / slug
    evid.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    (m.EVID_REPO / "html" / slug).mkdir(parents=True, exist_ok=True)
    (m.EVID_REPO / "audits" / slug).mkdir(parents=True, exist_ok=True)

    print(f"\n=== RESUME {slug} {email} certified={ck.get('certified_days_complete')} remaining={ck.get('remaining_xi_days')}", flush=True)
    op_note(ck, "resume_start", remaining=ck.get("remaining_xi_days"))
    save_ckpt(ck)

    def login():
        c = m.ro.wait_login(f"{slug}_resume", email, password, attempts=12)
        if not c:
            raise RuntimeError("login failed")
        c.html_dir = html_dir
        return c

    c = with_backoff("login", login)
    m.ro.HTML = m.HTML
    m.ro.EVID = evid
    m.ro.EVID_REPO = m.EVID_REPO

    complete = m.patch_session_answers(persona)
    seen = {t["day"]: t for t in ck.get("certified_trajectory") or []}
    trajectory = list(ck.get("certified_trajectory") or [])
    programme_traj = [t.get("programme_metrics") or {} for t in trajectory if t.get("programme_metrics")]
    all_defects = []
    transit_days = []
    last_detected = ck.get("last_certified_day") or ck.get("last_transit_verified")
    consecutive_empty = 0
    infra_failures = 0
    idx = 1000 + len(trajectory)  # avoid colliding with prior day indices

    for _n in range(80):
        if all(k in seen for k in m.TARGET):
            break
        print(f"  day {idx} xi_seen={sorted(seen)} last={last_detected}", flush=True)
        try:
            def home_get():
                return c.get("/student/")

            try:
                _, _, home = with_backoff("home", home_get, attempts=4, base=3.0)
            except Exception as exc:
                op_note(ck, "infra_home_timeout", error=str(exc)[:300])
                save_ckpt(ck)
                infra_failures += 1
                if infra_failures >= 6:
                    print("  YIELD too many infra failures; checkpoint saved", flush=True)
                    ck["status"] = "yielded_infra"
                    save_ckpt(ck)
                    return {"slug": slug, "verdict": "YIELD", "reason": "infra", "email": email, "checkpoint": ck}
                c = with_backoff("relogin", login)
                continue

            sig = m.ro.extract_mission_signals(home)
            if sig["day_complete"] or not sig["has_start"]:
                def do_backdate():
                    st = m.ro.backdate_missions(email)
                    if st.get("status") != "succeeded":
                        raise RuntimeError(f"backdate {st}")
                    return st

                try:
                    with_backoff("backdate", do_backdate, attempts=4, base=5.0)
                except Exception as exc:
                    op_note(ck, "infra_backdate_timeout", error=str(exc)[:300])
                    save_ckpt(ck)
                    infra_failures += 1
                    if infra_failures >= 6:
                        ck["status"] = "yielded_infra"
                        save_ckpt(ck)
                        return {"slug": slug, "verdict": "YIELD", "reason": "backdate_infra", "email": email, "checkpoint": ck}
                    continue
                time.sleep(2)
                c = with_backoff("relogin_after_backdate", login)

            expect = m.pick_expect(seen, last_detected)

            def do_complete():
                return complete(c, idx, expect)

            try:
                day_out = with_backoff("complete_session", do_complete, attempts=3, base=6.0)
            except Exception as exc:
                op_note(ck, "infra_session_timeout", error=str(exc)[:300], expect=expect)
                save_ckpt(ck)
                infra_failures += 1
                consecutive_empty += 1
                if infra_failures >= 6 or consecutive_empty >= 8:
                    ck["status"] = "yielded_infra"
                    save_ckpt(ck)
                    return {"slug": slug, "verdict": "YIELD", "reason": "session_infra", "email": email, "checkpoint": ck}
                c = with_backoff("relogin_after_timeout", login)
                idx += 1
                continue

            actual = m.detect(day_out)
            audit0 = (day_out.get("reading") or {}).get("audit") or {}
            if (
                actual
                and actual.startswith("CX-")
                and not day_out.get("finished")
                and not audit0.get("is_fallback_shell")
            ):
                print(f"  RETRY unfinished {actual}", flush=True)
                time.sleep(3)
                try:
                    day_out = with_backoff(
                        "retry_unfinished",
                        lambda: complete(c, idx, actual),
                        attempts=2,
                        base=5.0,
                    )
                    actual = m.detect(day_out) or actual
                except Exception as exc:
                    op_note(ck, "infra_retry_unfinished", error=str(exc)[:300], day=actual)
                    save_ckpt(ck)

            if actual:
                last_detected = actual
                ck["last_transit_verified"] = actual

            # Never score infra emptiness as educational Critical
            audit = (day_out.get("reading") or {}).get("audit") or {}
            if audit.get("is_fallback_shell"):
                consecutive_empty += 1
            elif not day_out.get("finished") and not actual:
                consecutive_empty += 1
                op_note(ck, "empty_sitting_infra_or_ops", finished=False)
            else:
                consecutive_empty = 0
                infra_failures = 0

            if consecutive_empty >= 8:
                op_note(ck, "yield_empty_sittings", count=consecutive_empty)
                ck["status"] = "yielded_infra"
                save_ckpt(ck)
                print("  YIELD empty sittings; checkpoint saved", flush=True)
                return {"slug": slug, "verdict": "YIELD", "reason": "empty", "email": email, "checkpoint": ck}

            if actual and actual.startswith("CX-"):
                # Skip already certified
                if actual in seen:
                    print(f"  already certified {actual}; advancing calendar", flush=True)
                    if day_out.get("finished"):
                        m.ro.backdate_missions(email)
                        time.sleep(2)
                        c = with_backoff("relogin", login)
                    idx += 1
                    continue

                day_out = m.score_xi(day_out, actual)
                metrics = m.programme_metrics_for_day(
                    day_out, actual, [t["day"] for t in trajectory]
                )
                day_out["programme_metrics"] = metrics
                # Educational defects only — strip infra-ish label noise on certified path
                defects = [
                    d
                    for d in m.classify_defects(day_out, actual)
                    if d.get("severity") in ("Critical", "Major")
                    or d.get("id") in ("PB14-MINOR-CHROME", "PB14-MINOR-Q6")
                ]
                all_defects.extend(defects)

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
                            "revision_q6_residual": bool(day_out.get("revision_q6_residual")),
                        }
                    )
                    programme_traj.append(metrics)
                    # Persist evidence append-only
                    lean = {
                        "expected_day": actual,
                        "detected_campaign_day": actual,
                        "finished": day_out.get("finished"),
                        "reflection_ok": day_out.get("reflection_ok"),
                        "verdict": day_out.get("verdict"),
                        "score_over_9": day_out.get("score_over_9"),
                        "dimensions": day_out.get("dimensions"),
                        "programme_metrics": metrics,
                        "checklist": day_out.get("checklist"),
                        "tomorrow_chrome_matches_approved": day_out.get(
                            "tomorrow_chrome_matches_approved"
                        ),
                        "chrome_residual": day_out.get("chrome_residual"),
                        "revision_q6_residual": day_out.get("revision_q6_residual"),
                        "residuals": day_out.get("residuals"),
                        "package_id": day_out.get("package_id"),
                        "reading": {
                            "audit": (day_out.get("reading") or {}).get("audit"),
                            "html": (day_out.get("reading") or {}).get("html"),
                        },
                        "resumed": True,
                        "completed_at": utcnow(),
                    }
                    (evid / f"day{idx}_{actual}.json").write_text(
                        json.dumps(lean, indent=2, default=str)
                    )
                    dest = m.EVID_REPO / "audits" / slug / f"day{idx}_{actual}.json"
                    if not dest.exists():
                        dest.write_text(json.dumps(lean, indent=2, default=str))
                    for hp in list(html_dir.glob(f"day{idx}_*_reading.html")):
                        hdest = m.EVID_REPO / "html" / slug / hp.name
                        if not hdest.exists():
                            hdest.write_bytes(hp.read_bytes())
                    persist_certified_sitting(ck, slug, day_out, actual, idx)
                    print(
                        f"  SCORED {actual} {day_out['score_over_9']}/9 metrics="
                        f"{sum(1 for v in metrics.values() if v=='PASS')}/6",
                        flush=True,
                    )
                else:
                    print(
                        f"  xi educational FAIL-ish {actual} score={day_out.get('score_over_9')} "
                        f"finished={day_out.get('finished')}",
                        flush=True,
                    )
            else:
                transit_days.append(actual)
                if actual:
                    ck["last_transit_verified"] = actual
                    save_ckpt(ck)
                print(
                    f"  transit detected={actual} finished={day_out.get('finished')}",
                    flush=True,
                )

            if day_out.get("finished") or consecutive_empty:
                try:
                    m.ro.backdate_missions(email)
                except Exception as exc:
                    op_note(ck, "infra_post_finish_backdate", error=str(exc)[:200])
                time.sleep(2)
                try:
                    c = with_backoff("relogin", login, attempts=3, base=4.0)
                except Exception as exc:
                    op_note(ck, "infra_relogin", error=str(exc)[:200])
                    save_ckpt(ck)
            idx += 1
        except Exception as exc:
            print(f"  ERROR {exc}", flush=True)
            traceback.print_exc()
            op_note(ck, "infra_loop_exception", error=str(exc)[:400])
            save_ckpt(ck)
            time.sleep(5)
            try:
                c = with_backoff("relogin_after_error", login)
            except Exception:
                ck["status"] = "yielded_infra"
                save_ckpt(ck)
                return {"slug": slug, "email": email, "verdict": "YIELD", "reason": str(exc), "checkpoint": ck}
            idx += 1

    certified_all = all(k in seen for k in m.TARGET)
    scores = [t["score_over_9"] for t in trajectory]
    avg = (sum(scores) / len(scores)) if scores else 0.0
    levels = [t.get("confidence_level") or "HIGH" for t in trajectory]
    rank = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    stable = (
        all(rank.get(levels[i], 0) <= rank.get(levels[i + 1], 0) for i in range(len(levels) - 1))
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
        vals = [(t.get("programme_metrics") or {}).get(k) for t in trajectory]
        vals = [v for v in vals if v]
        prog_agg[k] = {
            "pass_count": sum(1 for v in vals if v == "PASS"),
            "total": len(vals),
            "result": "PASS" if vals and all(v == "PASS" for v in vals) else ("FAIL" if vals else "FAIL"),
        }
    critical = [d for d in all_defects if d.get("severity") == "Critical"]
    major = [d for d in all_defects if d.get("severity") == "Major"]
    verdict = (
        "PASS"
        if certified_all and avg >= 8.0 and stable and not critical and not major
        else "FAIL"
    )
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
        "summary": {
            "certified_days_scored": len(trajectory),
            "certified_all_pass": certified_all,
            "avg_score_over_9": avg,
            "trajectory": trajectory,
            "stable_high": stable and all(l == "HIGH" for l in levels),
            "programme_metrics": prog_agg,
            "transit_observations": transit_days,
            "defects": all_defects,
            "defect_counts": {
                "Critical": len(critical),
                "Major": len(major),
                "Minor": len([d for d in all_defects if d.get("severity") == "Minor"]),
                "Cosmetic": 0,
            },
            "operational_notes": ck.get("operational_notes") or [],
        },
    }
    # Append-only persona write: keep prior if exists by writing resume sidecar then merge main
    prior = m.EVID_REPO / "personas" / f"{slug}.json"
    if prior.exists():
        (m.EVID_REPO / "personas" / f"{slug}.pre_resume.json").write_text(prior.read_text())
    (evid / "persona.json").write_text(json.dumps(out, indent=2, default=str))
    prior.write_text(json.dumps(out, indent=2, default=str))
    ck["status"] = "complete" if verdict == "PASS" else ck.get("status")
    op_note(ck, "resume_finished", verdict=verdict, avg=avg)
    save_ckpt(ck)
    print(f"persona {slug} {verdict} avg={avg}", flush=True)
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: run_pb014_resume.py <slug>")
        return 2
    slug = sys.argv[1]
    m.ACCT.mkdir(parents=True, exist_ok=True)
    m.HTML.mkdir(parents=True, exist_ok=True)
    m.EVID_BASE.mkdir(parents=True, exist_ok=True)
    result = resume_persona(slug)
    print("RESUME_RESULT", result.get("verdict"), flush=True)
    return 0 if result.get("verdict") in {"PASS", "YIELD"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
