#!/usr/bin/env python3
"""RO-013 — Wave 1 LIVE verification (browserless).

Ops verification only. Does not modify educational packages or Runtime.
Walks a fresh Internal Alpha student from Baseline through Alpha→Beta→Gamma
using mission_date backdating between days so the calendar gate does not block
same-ops-session multi-day continuity verification.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import time
import urllib.parse
from pathlib import Path

ROOT = Path("/tmp/ro014")
ACCT = ROOT / "accounts"
HTML = ROOT / "html"
EVID = ROOT / "evidence"
CERT = ROOT / "certified"
EVID_REPO = Path(
    "/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/RO014"
)
EXPECTED_COMMIT = "4ff8c95d2b853114f0b99ba2d7d23ea847c62819"
SERVICE = "srv-d97ji5t7vvec73cbs5l0"

spec = importlib.util.spec_from_file_location(
    "pb001a", "/tmp/pb001a/run_verification.py"
)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.EXPECTED_COMMIT = EXPECTED_COMMIT
mod.BASE = "https://kwalitec.onrender.com"
mod.ROOT = ROOT
mod.ACCT = ACCT
mod.HTML = HTML
mod.EVID = EVID


def render_key() -> str:
    import re as _re

    text = Path("/Users/kwalitec/.render/cli.yaml").read_text()
    return _re.search(r"key:\s*(\S+)", text).group(1)


def render_job(start_command: str, *, timeout_s: int = 180) -> dict:
    import urllib.request

    key = render_key()
    req = urllib.request.Request(
        f"https://api.render.com/v1/services/{SERVICE}/jobs",
        data=json.dumps({"startCommand": start_command}).encode(),
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        created = json.loads(resp.read().decode())
    job_id = created["id"]
    deadline = time.time() + timeout_s
    while time.time() < deadline:
        req2 = urllib.request.Request(
            f"https://api.render.com/v1/services/{SERVICE}/jobs/{job_id}",
            headers={"Authorization": f"Bearer {key}"},
        )
        with urllib.request.urlopen(req2, timeout=30) as resp:
            st = json.loads(resp.read().decode())
        status = st.get("status")
        if status in {"succeeded", "failed", "canceled"}:
            return st
        time.sleep(4)
    return {"id": job_id, "status": "timeout"}


def load_snippets(path: Path) -> dict:
    d = json.loads(path.read_text())
    rg = d.get("reading_guidance") or {}
    miss = d.get("mission") or {}
    return {
        "package_id": d.get("package_id", ""),
        "topic_code": d.get("topic_code", ""),
        "campaign_day": d.get("campaign_day", ""),
        "display_title": miss.get("display_title", ""),
        "lead_line": rg.get("lead_line", ""),
        "exit_line": rg.get("exit_line", ""),
        "return_cue": rg.get("return_cue", ""),
        "open_point": rg.get("open_point", ""),
        "stop_condition": rg.get("stop_condition", ""),
        "tomorrow": d.get("tomorrow_preview") or {},
    }


SNIPPETS = {
    "CP-D1": load_snippets(CERT / "2.1.3-prob-quantiles-cs1016.json"),
    "CP-D2": load_snippets(CERT / "2.2.1-marginal-conditional-cs1016.json"),
    "CP-D3": load_snippets(CERT / "2.5.1-clt-cs1016.json"),
    "CP-D4": load_snippets(CERT / "2.6.1-random-samples-cs1016.json"),
    "CP-D5": load_snippets(CERT / "3.1.1-estimators-cs1016.json"),
    "CP-D6": load_snippets(CERT / "3.2.1-ci-sample-cs1016.json"),
    "CP-D7": load_snippets(CERT / "3.3.1-hypothesis-testing-cs1016.json"),
    "CP-D8": load_snippets(CERT / "4.1.1-linear-regression-cs1016.json"),
    "CP-D9": load_snippets(CERT / "5.1.1-bayes-theorem-cs1016.json"),
    "CP-R1": load_snippets(CERT / "revision-spine-memory-cs1016.json"),
}

EXPECTED_CHAIN = [
    "CP-D1","CP-D2","CP-D3","CP-D4","CP-D5","CP-D6","CP-D7","CP-D8","CP-D9","CP-R1",
]


def wait_login(slug: str, email: str, password: str, attempts: int = 18):
    for i in range(attempts):
        c = mod.Client(slug)
        c.html_dir = HTML / slug
        c.html_dir.mkdir(parents=True, exist_ok=True)
        try:
            if mod.login(c, email, password):
                return c
        except Exception as e:  # noqa: BLE001
            c.log("login_error", False, error=str(e)[:200])
        time.sleep(6)
        print(f"  retry login attempt {i + 1}", flush=True)
    return None



def backdate_missions(email: str) -> dict:
    """Shift completed mission_dates back one day via Render one-off job (curl)."""
    import subprocess
    import time as _time
    import base64

    key = render_key()
    script = (
        "from datetime import timedelta\n"
        "from app import create_app\n"
        "from app.extensions import db\n"
        "from app.models import User\n"
        "from app.models.educational_runtime_engine import RuntimeMissionInstance as M\n"
        f"email = {email!r}.lower()\n"
        "app = create_app()\n"
        "with app.app_context():\n"
        "    u = User.query.filter_by(email=email).first()\n"
        "    assert u is not None, 'user missing'\n"
        "    n = 0\n"
        "    for m in M.query.filter_by(user_id=u.id).all():\n"
        "        if m.mission_date is not None:\n"
        "            m.mission_date = m.mission_date - timedelta(days=1)\n"
        "            n += 1\n"
        "    db.session.commit()\n"
        "    print('BACKDATED', n, 'user', u.id)\n"
    )
    b64 = base64.b64encode(script.encode()).decode()
    start_command = f"python -c \"import base64; exec(base64.b64decode('{b64}').decode())\""
    payload_path = ACCT / f"backdate_{abs(hash(email)) % 10_000_000}.json"
    ACCT.mkdir(parents=True, exist_ok=True)
    payload_path.write_text(json.dumps({"startCommand": start_command}))
    raw = subprocess.check_output(
        [
            "curl", "-sS", "--max-time", "90",
            "-X", "POST",
            "-H", f"Authorization: Bearer {key}",
            "-H", "Content-Type: application/json",
            "-d", f"@{payload_path}",
            f"https://api.render.com/v1/services/{SERVICE}/jobs",
        ],
        text=True,
    )
    created = json.loads(raw)
    job_id = created["id"]
    for _ in range(60):
        st_raw = subprocess.check_output(
            [
                "curl", "-sS", "--max-time", "60",
                "-H", f"Authorization: Bearer {key}",
                f"https://api.render.com/v1/services/{SERVICE}/jobs/{job_id}",
            ],
            text=True,
        )
        st = json.loads(st_raw)
        if st.get("status") in {"succeeded", "failed", "canceled"}:
            return st
        _time.sleep(4)
    return {"id": job_id, "status": "timeout"}



def extract_mission_signals(html: str) -> dict:
    text = mod.Client("x").textish(html) if False else re.sub(
        r"\s+", " ", re.sub(r"<[^>]+>", " ", html)
    )
    title = None
    m = re.search(
        r'class="[^"]*(?:mission|ds-home)[^"]*title[^"]*"[^>]*>(.*?)</',
        html,
        re.S | re.I,
    )
    if m:
        title = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    if not title:
        m = re.search(
            r"(Evaluate probabilities|Poisson process|inverse transform|"
            r"statistical software|Retrieve PCA|Retrieve distributions|"
            r"Purpose and function|summary statistics|association|"
            r"Place continuous|discrete families|"
            r"Retrieve purpose|Guided Reading)",
            html,
            re.I,
        )
        if m:
            title = m.group(0)
    day_complete = bool(
        re.search(
            r"Return tomorrow|already completed today|Today'?s Session is finished",
            html,
            re.I,
        )
    )
    return {
        "title_guess": title,
        "day_complete": day_complete,
        "has_start": 'action="/student/session/start"' in html
        or bool(re.search(r"Start today|Begin today|session/start", html, re.I)),
        "text_sample": text[:400],
    }


def match_expected_day(html: str, expected_day: str) -> dict:
    snip = SNIPPETS[expected_day]
    hits = {
        "lead_line": snip["lead_line"][:48] in html,
        "display_title": bool(snip["display_title"])
        and snip["display_title"][:24].lower() in html.lower(),
        "package_id_absent_ok": True,
    }
    # Prefer lead_line presence in Reading; for home, display title helps.
    return {"expected_day": expected_day, "package_id": snip["package_id"], "hits": hits}


def complete_session(c: mod.Client, day_idx: int, expected_day: str) -> dict:
    """Complete one study day; capture Reading/CMP/activities/reflection/tomorrow."""
    out = {
        "day_index": day_idx,
        "expected_day": expected_day,
        "expected_package_id": SNIPPETS[expected_day]["package_id"],
        "finished": False,
        "reading": None,
        "checklist": {},
        "tomorrow_preview": {},
        "verdict": "FAIL",
    }
    _, final, html = c.get("/student/")
    c.save(f"day{day_idx}_home", html)
    home_sig = extract_mission_signals(html)
    out["home"] = home_sig
    if home_sig["day_complete"] or not home_sig["has_start"]:
        out["error"] = "no_startable_mission"
        return out

    # Start session
    mid = re.search(r'name="mission_id"[^>]*value="([^"]+)"', html)
    data = {"csrf_token": c.csrf(html)}
    if mid:
        data["mission_id"] = mid.group(1)
    form = re.search(
        r'<form[^>]*action="/student/session/start"[^>]*>(.*?)</form>',
        html,
        re.S | re.I,
    )
    if form:
        for n, v in re.findall(
            r'<input[^>]*name="([^"]+)"[^>]*value="([^"]*)"', form.group(1), re.I
        ):
            data.setdefault(n, v)
    _, final, html = c.post("/student/session/start", data)
    c.save(f"day{day_idx}_start", html)
    sid_m = re.search(r"/session/((?:lsr-|sess-)[a-z0-9]+)", final) or re.search(
        r"/session/((?:lsr-|sess-)[a-z0-9]+)", html
    )
    if not sid_m:
        out["error"] = f"no_session final={final}"
        return out
    sid = sid_m.group(1)
    out["session_id"] = sid

    if "/overview" in final or "Session Overview" in html:
        if "csrf_token" in html:
            _, final, html = c.post(
                f"/session/{sid}/begin",
                {"csrf_token": c.csrf(html), "session_id": sid},
            )
            c.save(f"day{day_idx}_begin", html)

    # Activity loop
    reading_html = ""
    for i in range(12):
        _, final, html = c.get(f"/session/{sid}/activity")
        path = urllib.parse.urlparse(final).path
        c.save(f"day{day_idx}_act_{i}", html)
        stage = None
        sm = re.search(r'data-session-stage="([^"]+)"', html)
        if sm:
            stage = sm.group(1)
        is_reading = bool(
            (stage and stage.lower() in ("read", "reading"))
            or re.search(r"Guided Reading:|Reading · Activity", html, re.I)
        )
        if is_reading and not reading_html:
            reading_html = html
            c.save(f"day{day_idx}_reading", html)
            dest = EVID / f"day{day_idx}_{expected_day}_reading.html"
            dest.write_text(html, encoding="utf-8")
            (EVID_REPO / "html" / f"day{day_idx}_{expected_day}_reading.html").write_text(
                html, encoding="utf-8"
            )

        if path.endswith("/reflection") or path.endswith("/summary"):
            break

        if f"/session/{sid}/activity/advance" in html:
            _, final, html = c.post(
                f"/session/{sid}/activity/advance",
                {"csrf_token": c.csrf(html), "session_id": sid},
            )
            if urllib.parse.urlparse(final).path.endswith("/reflection"):
                break
            continue

        if f"/session/{sid}/activity/answer" in html:
            aid = re.search(r'name="activity_id"[^>]*value="([^"]+)"', html)
            aid = aid.group(1) if aid else "act-1"
            fields = set(re.findall(r'name="([^"]+)"', html))
            data = {
                "csrf_token": c.csrf(html),
                "session_id": sid,
                "activity_id": aid,
                "response": (
                    f"RO-014 day {expected_day}: applied CMP guidance and answered as directed."
                ),
            }
            if "confidence" in fields:
                data["confidence"] = "3"
            if "confidence_level" in fields:
                data["confidence_level"] = "medium"
            _, final, html = c.post(f"/session/{sid}/activity/answer", data)
            _, final, html = c.get(f"/session/{sid}/activity")
            continue

        # Unexpected — stop loop
        break

    # Audit reading
    snip = SNIPPETS[expected_day]
    certified = {
        "lead_line": snip["lead_line"],
        "exit_line": snip["exit_line"],
        "return_cue": snip["return_cue"],
        "open_point": snip.get("open_point", ""),
    }
    audit = (
        mod.audit_reading_html(reading_html, certified_snippets=certified)
        if reading_html
        else {"verdict": "FAIL", "is_fallback_shell": True, "q_checks": {}, "error": "no_reading"}
    )
    q = audit.get("q_checks") or {}
    checklist = {
        "CMP_reference_present": bool(audit.get("mentions_cmp") or q.get("Q1_cmp_open")),
        "Educational_purpose_clear": bool(q.get("Q2_purpose")),
        "Reading_focus_clear": bool(q.get("Q3_attention")),
        "Ignore_guidance_present": bool(q.get("Q4_ignore")),
        "Stop_condition_explicit": bool(q.get("Q5_stop")),
        "Immediate_next_activity_named": bool(q.get("Q6_next")),
        "Not_fallback_shell": not bool(audit.get("is_fallback_shell")),
        "Matches_certified_snippets": all(
            (audit.get("certified_snippet_hits") or {}).values()
        )
        if audit.get("certified_snippet_hits")
        else False,
    }
    # Enrich audit for progressive detect()
    if reading_html and isinstance(audit, dict):
        sample = re.sub(r"<[^>]+>", " ", reading_html)
        sample = re.sub(r"\s+", " ", sample).strip()
        audit.setdefault("body_sample", sample[:4000])
        audit.setdefault("title", c.title(reading_html) if hasattr(c, "title") else "")
    out["reading"] = {
        "audit": audit,
        "checklist": checklist,
        "html": str(EVID / f"day{day_idx}_{expected_day}_reading.html")
        if reading_html
        else None,
    }
    out["checklist"] = checklist

    # Reflection
    _, final, html = c.get(f"/session/{sid}/reflection")
    c.save(f"day{day_idx}_reflection", html)
    reflection_ok = "Error" not in c.title(html) and "500" not in html[:2000]
    out["reflection_ok"] = reflection_ok
    if reflection_ok and "csrf_token" in html and "Not Found" not in c.title(html):
        _, final, html = c.post(
            f"/session/{sid}/reflection/continue",
            {
                "csrf_token": c.csrf(html),
                "session_id": sid,
                "reflection_note": (
                    f"RO-014 {expected_day}: completed activities; noted stickiest CMP cue."
                ),
                "submit": "Continue",
            },
        )

    # Summary + finish
    _, final, html = c.get(f"/session/{sid}/summary")
    c.save(f"day{day_idx}_summary", html)
    tomorrow_hits = {
        "next_topic_code": snip["tomorrow"].get("next_topic_code", "") in html,
        "continuity_fragment": bool(
            snip["tomorrow"].get("continuity_line")
            and snip["tomorrow"]["continuity_line"][:40] in html
        ),
        "student_facing_fragment": bool(
            snip["tomorrow"].get("student_facing")
            and snip["tomorrow"]["student_facing"][:40] in html
        ),
    }
    # Also accept tomorrow on home after finish
    out["tomorrow_preview"] = tomorrow_hits

    if "completion_status" in html:
        _, final, html = c.post(
            f"/session/{sid}/finish",
            {
                "csrf_token": c.csrf(html),
                "session_id": sid,
                "completion_status": "yes",
                "notes": f"RO-014 {expected_day}: finished planned study.",
                "submit": "Finish Session",
            },
        )
        flashes = c.flashes(html) if hasattr(c, "flashes") else []
        out["finished"] = ("Please choose Yes" not in html) and not any(
            "Please choose Yes" in f for f in flashes
        )
        # Heuristic: redirected to student home / session finished copy
        if not out["finished"]:
            out["finished"] = bool(
                __import__("re").search(
                    r"Session finished|Return tomorrow|already completed today|Today.?s Session is finished",
                    html,
                    __import__("re").I,
                )
            )
        c.save(f"day{day_idx}_finish", html)
        # Re-check tomorrow on post-finish home
        _, _, home = c.get("/student/")
        c.save(f"day{day_idx}_post_home", home)
        for k, frag_key in (
            ("next_topic_code", "next_topic_code"),
            ("continuity_fragment", "continuity_line"),
            ("student_facing_fragment", "student_facing"),
        ):
            frag = snip["tomorrow"].get(
                "next_topic_code"
                if frag_key == "next_topic_code"
                else frag_key,
                "",
            )
            if frag and frag[:40] in home:
                tomorrow_hits[k] = True
        out["tomorrow_preview"] = tomorrow_hits
    out["tomorrow_chrome_matches_approved"] = bool(
        tomorrow_hits.get("continuity_fragment")
        or tomorrow_hits.get("student_facing_fragment")
        or tomorrow_hits.get("next_topic_code")
    )

    # Package-path PASS: finished + reflection + CMP + no fallback (RO-002…RO-013 policy)
    cmp_ok = bool(checklist.get("CMP_reference_present") or audit.get("mentions_cmp"))
    ok = (
        out["finished"]
        and reflection_ok
        and cmp_ok
        and not bool(audit.get("is_fallback_shell"))
    )
    out["verdict"] = "PASS" if ok else "FAIL"
    out["package_path_ok"] = ok
    out["chrome_residual"] = not bool(out.get("tomorrow_chrome_matches_approved"))

    print(
        f"== {expected_day} {out['verdict']} finished={out['finished']} "
        f"fallback={audit.get('is_fallback_shell')} reading={audit.get('verdict')}",
        flush=True,
    )
    (EVID / f"day{day_idx}_{expected_day}_audit.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    (EVID_REPO / "audits" / f"day{day_idx}_{expected_day}.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    return out


def main() -> int:
    EVID.mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "html").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "audits").mkdir(parents=True, exist_ok=True)
    email = (ACCT / "student.email").read_text().strip()
    password = (ACCT / "shared_pass.txt").read_text().strip()

    probe = mod.Client("probe")
    probe.html_dir = HTML / "probe"
    probe.html_dir.mkdir(parents=True, exist_ok=True)
    health = mod.fingerprint(probe)
    results = {
        "programme": "RO-013",
        "host": mod.BASE,
        "expected_commit": EXPECTED_COMMIT,
        "live_health": health,
        "email": email,
        "days": [],
        "verdict": "FAIL",
    }
    if health.get("commit") != EXPECTED_COMMIT:
        results["reason"] = "fingerprint mismatch"
        (EVID / "results.json").write_text(json.dumps(results, indent=2))
        print(json.dumps(results, indent=2))
        return 1

    c = wait_login("wave1", email, password)
    if not c:
        results["reason"] = "login failed"
        (EVID / "results.json").write_text(json.dumps(results, indent=2))
        return 1

    # Enrol + Baseline start
    final, html = mod.enrol(c, position_mode="start")
    final, html = mod.complete_onboarding(c, final, html)
    c.save("enrolled_home", html)

    for idx, day in enumerate(EXPECTED_CHAIN, start=1):
        print(f"\n### Study day {idx}: expect {day}", flush=True)
        # Ensure startable mission (backdate if day_complete leftover)
        _, _, home = c.get("/student/")
        sig = extract_mission_signals(home)
        if sig["day_complete"] or not sig["has_start"]:
            print("  backdating missions for next day unlock…", flush=True)
            st = backdate_missions(email)
            results.setdefault("backdates", []).append(
                {"before_day": day, "job": st.get("id"), "status": st.get("status")}
            )
            if st.get("status") != "succeeded":
                results["reason"] = f"backdate failed before {day}"
                break
            time.sleep(2)
            # re-login to clear any stale page
            c = wait_login("wave1", email, password, attempts=8)
            if not c:
                results["reason"] = f"relogin failed before {day}"
                break

        day_result = complete_session(c, idx, day)
        results["days"].append(day_result)
        if day_result.get("verdict") != "PASS" and day.startswith("CG-"):
            results["reason"] = f"gamma day failed: {day}"
            break
        if not day_result.get("finished"):
            results["reason"] = f"day not finished: {day}"
            break

        # After finish, backdate so next chain day can generate today
        if idx < len(EXPECTED_CHAIN):
            st = backdate_missions(email)
            results.setdefault("backdates", []).append(
                {"after_day": day, "job": st.get("id"), "status": st.get("status")}
            )
            if st.get("status") != "succeeded":
                results["reason"] = f"backdate failed after {day}"
                break
            time.sleep(2)
            c = wait_login("wave1", email, password, attempts=8)
            if not c:
                results["reason"] = f"relogin failed after {day}"
                break

    gamma_days = [d for d in results["days"] if d.get("expected_day", "").startswith("CG-")]
    pre_days = [d for d in results["days"] if not d.get("expected_day", "").startswith("CG-")]
    results["summary"] = {
        "pre_gamma_finished": all(d.get("finished") for d in pre_days) and len(pre_days) == 7,
        "gamma_pass": all(d.get("verdict") == "PASS" for d in gamma_days)
        and len(gamma_days) == 5,
        "chain_days_completed": len(results["days"]),
        "expected_chain_len": len(EXPECTED_CHAIN),
    }
    if (
        results["summary"]["pre_gamma_finished"]
        and results["summary"]["gamma_pass"]
        and health.get("commit") == EXPECTED_COMMIT
    ):
        results["verdict"] = "PASS"
        results.pop("reason", None)

    (EVID / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    (EVID_REPO / "results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps({"verdict": results["verdict"], "summary": results["summary"], "reason": results.get("reason")}, indent=2))
    return 0 if results["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
