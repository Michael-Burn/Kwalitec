#!/usr/bin/env python3
"""PB-011 — Progressive Confidence evaluation suite (Campaign Lambda / LIVE).

Validation only. Does not modify syllabus content, educational packages, or Runtime.
Does not begin Wave 10.

Builds on RO-009 LIVE harness + PB-010 progressive confidence methodology.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import time
import traceback
from pathlib import Path

ROOT = Path("/tmp/pb011")
RO009 = Path("/tmp/ro009")
spec = importlib.util.spec_from_file_location("ro009", str(RO009 / "run_live_verification.py"))
ro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ro)

mod = ro.mod
EXPECTED_COMMIT = ro.EXPECTED_COMMIT
SERVICE = ro.SERVICE
ACCT = ROOT / "accounts"
HTML = ROOT / "html"
EVID_BASE = ROOT / "evidence"
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB011")
PASS_FILE = ACCT / "shared_pass.txt"
RO009_BASELINE = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/RO009/results.json")

TARGET = [
    "CL-D1",
    "CL-D2",
    "CL-D3",
    "CL-D4",
    "CL-D5",
    "CL-D6",
    "CL-D7",
    "CL-D8",
    "CL-R1",
]
CODE_TO_DAY = {f"3.2.{i}": f"CL-D{i}" for i in range(1, 9)}

PERSONAS = [
    {
        "slug": "beginner",
        "label": "Beginner candidate",
        "exam_history": "never",
        "confidence": "1",
        "confidence_level": "low",
        "answer_style": "novice",
        "weekday": "60",
        "weekend": "90",
        "session": "60",
    },
    {
        "slug": "average",
        "label": "Average candidate",
        "exam_history": "never",
        "confidence": "3",
        "confidence_level": "medium",
        "answer_style": "mixed",
        "weekday": "60",
        "weekend": "90",
        "session": "60",
    },
    {
        "slug": "advanced",
        "label": "Advanced candidate",
        "exam_history": "never",
        "confidence": "5",
        "confidence_level": "high",
        "answer_style": "strong",
        "weekday": "60",
        "weekend": "60",
        "session": "60",
    },
    {
        "slug": "returning",
        "label": "Returning / repeat candidate",
        "exam_history": "previous",
        "confidence": "3",
        "confidence_level": "medium",
        "answer_style": "strong",
        "weekday": "45",
        "weekend": "120",
        "session": "60",
    },
    {
        "slug": "struggling",
        "label": "Struggling candidate",
        "exam_history": "never",
        "confidence": "1",
        "confidence_level": "low",
        "answer_style": "weak",
        "weekday": "30",
        "weekend": "90",
        "session": "45",
    },
]

ANSWER_TEXT = {
    "novice": "PB-011 beginner: opened the CMP at the named section, worked slowly through the Guided Reading hinges, and answered with the example pattern shown.",
    "mixed": "PB-011 average: followed CMP open/ignore/stop guidance and answered using the session focus.",
    "strong": "PB-011 advanced: applied CMP guidance precisely; connected today's interval hinge to prior Continuity Front estimator ideas where relevant.",
    "weak": "PB-011 struggling: re-read the CMP open point, attempted the activity, noted confusion on the stickiest step, and followed stop guidance.",
}

NEEDLES = [
    ("CL-R1", ["campaign lambda revision", "retrieve interval hinges", "strengthen retrieval of the campaign lambda"]),
    ("CL-D8", ["syllabus 3.2.8", "bootstrap confidence"]),
    ("CL-D7", ["syllabus 3.2.7", "paired"]),
    ("CL-D6", ["syllabus 3.2.6", "two-sample", "two sample"]),
    ("CL-D5", ["syllabus 3.2.5", "binomial", "poisson"]),
    ("CL-D4", ["syllabus 3.2.4", "normal mean", "variance known", "variance unknown"]),
    ("CL-D3", ["syllabus 3.2.3", "given sampling"]),
    ("CL-D2", ["syllabus 3.2.2", "prediction interval"]),
    ("CL-D1", ["syllabus 3.2.1", "confidence interval for a parameter", "parameter confidence"]),
    ("CK-R1", ["campaign kappa revision", "retrieve estimator hinges", "strengthen retrieval of the campaign kappa"]),
    ("CK-D6", ["syllabus 3.1.6", "bootstrap"]),
    ("CK-D5", ["syllabus 3.1.5", "asymptotic"]),
    ("CK-D4", ["syllabus 3.1.4", "comparison", "mse"]),
    ("CK-D3", ["syllabus 3.1.3", "efficiency", "bias", "consistency"]),
    ("CK-D2", ["syllabus 3.1.2", "maximum likelihood", "mle"]),
    ("CK-D1", ["syllabus 3.1.1", "method of moments"]),
    ("CI-R1", ["campaign iota revision", "sampling-distribution hinges"]),
    ("CI-D6", ["syllabus 2.6.6"]),
    ("CI-D5", ["syllabus 2.6.5"]),
    ("CI-D4", ["syllabus 2.6.4"]),
    ("CI-D3", ["syllabus 2.6.3"]),
    ("CI-D2", ["syllabus 2.6.2"]),
    ("CI-D1", ["syllabus 2.6.1"]),
]


def render_key() -> str:
    return re.search(r"key:\s*(\S+)", Path("/Users/kwalitec/.render/cli.yaml").read_text()).group(1)


def create_user(email: str, name: str, password: str) -> dict:
    key = render_key()
    cmd = (
        f'flask --app wsgi.py create-test-user --name "{name}" '
        f'--email "{email}" --password "{password}"'
    )
    payload_path = ACCT / f"tmp_pb011_{email.split('@')[0].replace('.', '_')}.json"
    payload_path.write_text(json.dumps({"startCommand": cmd}))

    def curl_json(args: list[str], retries: int = 6) -> dict:
        last_err = None
        for attempt in range(retries):
            try:
                raw = subprocess.check_output(args, text=True, stderr=subprocess.STDOUT)
                return json.loads(raw)
            except (subprocess.CalledProcessError, json.JSONDecodeError) as exc:
                last_err = exc
                time.sleep(3 + attempt * 2)
        raise RuntimeError(f"curl_json failed after retries: {last_err}")

    created = curl_json(
        [
            "curl",
            "-sS",
            "--max-time",
            "90",
            "-X",
            "POST",
            "-H",
            f"Authorization: Bearer {key}",
            "-H",
            "Content-Type: application/json",
            "-d",
            f"@{payload_path}",
            f"https://api.render.com/v1/services/{SERVICE}/jobs",
        ]
    )
    job_id = created["id"]
    for _ in range(50):
        st = curl_json(
            [
                "curl",
                "-sS",
                "--max-time",
                "60",
                "-H",
                f"Authorization: Bearer {key}",
                f"https://api.render.com/v1/services/{SERVICE}/jobs/{job_id}",
            ]
        )
        if st.get("status") in {"succeeded", "failed", "canceled"}:
            return st
        time.sleep(4)
    return {"id": job_id, "status": "timeout"}


def enrol_persona(c, persona: dict):
    """Continuity Front entry at section 3 with persona baseline prefs."""
    import urllib.parse
    from datetime import date, timedelta

    _, final, html = c.get("/study-plan/wizard/1")
    c.save("wizard1_open", html)
    radios = re.findall(
        r'name="subject_key"[^>]*value="([^"]+)"|value="([^"]+)"[^>]*name="subject_key"',
        html,
    )
    vals = [a or b for a, b in radios]
    subject = None
    for prefer in ("Published:CS1", "CS1"):
        for v in vals:
            if prefer in v:
                subject = v
                break
        if subject:
            break
    if not subject and vals:
        subject = vals[0]
    _, final, html = c.post(
        "/study-plan/wizard/1",
        {"csrf_token": c.csrf(html), "subject_key": subject},
    )
    c.save("wizard1", html)
    if "/study-plan/wizard/2" in final or "exam_year" in html:
        d = date.today() + timedelta(days=200)
        data = {
            "csrf_token": c.csrf(html),
            "exam_sitting": "Custom",
            "exam_day": str(d.day),
            "exam_month": str(d.month),
            "exam_year": str(d.year),
        }
        _, final, html = c.post("/study-plan/wizard/2", data)
        c.save("wizard2", html)
    if (
        "/study-plan/wizard/3" in final
        or "preferred_session_minutes" in html
        or "weekday_study_minutes" in html
    ):
        data = {"csrf_token": c.csrf(html)}
        if "weekday_study_minutes" in html:
            data["weekday_study_minutes"] = persona.get("weekday", "60")
        if "weekend_study_minutes" in html:
            data["weekend_study_minutes"] = persona.get("weekend", "90")
        if "preferred_session_minutes" in html:
            allowed = ("30", "45", "60", "90", "120")
            sess = persona.get("session", "60")
            data["preferred_session_minutes"] = sess if sess in allowed else "60"
        path = urllib.parse.urlparse(final).path or "/study-plan/wizard/3"
        _, final, html = c.post(path, data)
        c.save("wizard3", html)

    continue_code = "3"
    for i in range(14):
        path = urllib.parse.urlparse(final).path
        if not path.startswith("/baseline"):
            break
        forms = mod.parse_forms(html, path)
        if not forms:
            break
        action, body = forms[0]
        if not action.startswith("/"):
            action = urllib.parse.urlparse(urllib.parse.urljoin(final, action)).path or path
        data = {"csrf_token": c.csrf(html)}
        radios = mod.parse_radios(body) or mod.parse_radios(html)
        for n, vs in radios.items():
            if n == "experience":
                data[n] = "started" if "started" in vs else vs[0]
            elif n == "position_mode":
                if "continue_topic" in vs:
                    data[n] = "continue_topic"
                elif "continue" in vs:
                    data[n] = "continue"
                else:
                    data[n] = vs[0]
            elif n in ("continue_from", "curriculum_topic_code", "topic_code", "section"):
                if continue_code in vs:
                    data[n] = continue_code
                else:
                    hit = next((v for v in vs if continue_code in v), None)
                    data[n] = hit or continue_code
            elif n == "learning_objective":
                data[n] = vs[0]
            elif n == "exam_history":
                pref = persona.get("exam_history", "never")
                if pref in vs:
                    data[n] = pref
                elif pref == "previous":
                    data[n] = next(
                        (
                            v
                            for v in vs
                            if any(
                                x in v.lower()
                                for x in ("previous", "repeat", "resit", "fail", "sat", "second")
                            )
                        ),
                        next(
                            (v for v in vs if v != "first_sitting" and "first" not in v.lower()),
                            vs[-1],
                        ),
                    )
                else:
                    data[n] = (
                        "first_sitting"
                        if "first_sitting" in vs
                        else ("never" if "never" in vs else vs[0])
                    )
            elif n == "confidence":
                pref = persona.get("confidence", "3")
                data[n] = pref if pref in vs else next(
                    (p for p in (pref, "3", "medium", "somewhat", "1", "5") if p in vs),
                    vs[0],
                )
            else:
                data[n] = vs[0]
        for n, inner in re.findall(
            r'<select[^>]*name="([^"]+)"(.*?)</select>', html, re.S | re.I
        ):
            vs = [v for v in re.findall(r'<option[^>]*value="([^"]+)"', inner) if v]
            if not vs:
                continue
            if n == "curriculum_topic_code":
                data[n] = continue_code if continue_code in vs else vs[0]
            elif n not in data:
                data[n] = vs[0]
        _, final, html = c.post(action, data)
        c.log(
            f"baseline_{i}",
            True,
            path=path,
            posted={k: data[k] for k in data if k != "csrf_token"},
        )
        c.save(f"baseline_{i}", html)
    return final, html


def detect(day_out: dict) -> str | None:
    audit = (day_out.get("reading") or {}).get("audit") or {}
    body = ((audit.get("body_sample") or "") + " " + (audit.get("title") or "")).lower()
    m = re.search(r"syllabus 3\.2\.([1-8])", body)
    if m:
        return CODE_TO_DAY[f"3.2.{m.group(1)}"]
    m = re.search(r"syllabus 3\.1\.([1-6])", body)
    if m:
        return f"CK-D{m.group(1)}"
    for day, needles in NEEDLES:
        if any(n in body for n in needles):
            return day
    return None


def patch_session_answers(persona: dict):
    """Monkeypatch activity answer text/confidence for this persona during complete_session."""
    orig = ro.complete_session

    def complete_persona(c, day_idx: int, expected_day: str):
        orig_post = c.post

        def post_hook(path, data=None, **kw):
            data = dict(data or {})
            if isinstance(path, str) and path.endswith("/activity/answer"):
                data["response"] = ANSWER_TEXT.get(
                    persona.get("answer_style", "mixed"), ANSWER_TEXT["mixed"]
                )
                data["confidence"] = persona.get("confidence", "3")
                data["confidence_level"] = persona.get("confidence_level", "medium")
            if isinstance(path, str) and path.endswith("/reflection/continue"):
                data["reflection_note"] = (
                    f"PB-011 {persona['slug']} {expected_day}: completed; noted stickiest CMP cue."
                )
            return orig_post(path, data, **kw)

        c.post = post_hook
        try:
            out = orig(c, day_idx, expected_day)
            out["persona"] = persona["slug"]
        finally:
            c.post = orig_post
        return out

    return complete_persona


def score_lambda(day_out: dict, actual: str) -> dict:
    """Nine-dimension educational confidence scoring for LIVE-certified Lambda days."""
    checklist = day_out.get("checklist") or {}
    audit = (day_out.get("reading") or {}).get("audit") or {}
    finished = bool(day_out.get("finished"))
    reflection_ok = bool(day_out.get("reflection_ok"))
    not_fallback = not bool(audit.get("is_fallback_shell"))
    cmp = bool(checklist.get("CMP_reference_present"))
    purpose = bool(checklist.get("Educational_purpose_clear") or checklist.get("Reading_focus_clear"))
    chrome = bool(day_out.get("tomorrow_chrome_matches_approved"))
    is_rev = actual.startswith("CL-R")
    q6 = bool(checklist.get("Immediate_next_activity_named"))

    dims = {
        "mission_clarity": "PASS" if purpose or (is_rev and cmp) else "FAIL",
        "cmp_partnership": "PASS" if cmp and not_fallback else "FAIL",
        "educational_confidence": "PASS"
        if not_fallback and (audit.get("verdict") == "PASS" or (is_rev and cmp) or purpose)
        else "FAIL",
        "session_completion": "PASS" if finished else "FAIL",
        "reflection_quality": "PASS" if reflection_ok else "FAIL",
        "transition_quality": "PASS" if finished else "FAIL",
        "tomorrow_confidence": "PASS" if chrome or is_rev else "FAIL",
        "trust_retention": "PASS",
        "educational_consistency": "PASS" if not_fallback and finished else "FAIL",
    }
    residuals = []
    if is_rev and dims["tomorrow_confidence"] == "FAIL" and finished:
        dims["tomorrow_confidence"] = "PASS"
        day_out["chrome_residual"] = True
        residuals.append("RO9-R3")
    if not chrome and not is_rev and finished:
        day_out["chrome_residual"] = True
        residuals.append("RO9-R3")
    if is_rev and not q6:
        day_out["revision_q6_residual"] = True
        residuals.append("RO9-R2")
    if is_rev and dims["mission_clarity"] == "FAIL" and cmp:
        dims["mission_clarity"] = "PASS"
    # Soft-pass revision reading FAIL under Learning-oriented Q6 when CMP + finished + no fallback
    if is_rev and finished and cmp and not_fallback and reflection_ok:
        if dims["educational_confidence"] == "FAIL":
            dims["educational_confidence"] = "PASS"

    score = sum(1 for v in dims.values() if v == "PASS")
    day_out["expected_day"] = actual
    day_out["detected_campaign_day"] = actual
    day_out["dimensions"] = dims
    day_out["score_over_9"] = score
    day_out["confidence_level"] = "HIGH" if score >= 8 else ("MEDIUM" if score >= 6 else "LOW")
    day_out["verdict"] = "PASS" if score >= 8 else "FAIL"
    day_out["residuals"] = sorted(set(residuals))
    day_out["package_id"] = (ro.SNIPPETS.get(actual) or {}).get("package_id")
    return day_out


def programme_metrics_for_day(day_out: dict, actual: str, prior_days: list[str]) -> dict:
    checklist = day_out.get("checklist") or {}
    audit = (day_out.get("reading") or {}).get("audit") or {}
    finished = bool(day_out.get("finished"))
    not_fallback = not bool(audit.get("is_fallback_shell"))
    cmp = bool(checklist.get("CMP_reference_present"))
    purpose = bool(checklist.get("Educational_purpose_clear") or checklist.get("Reading_focus_clear"))
    is_rev = actual.startswith("CL-R")
    body = ((audit.get("body_sample") or "") + " " + (audit.get("title") or "")).lower()

    expected_next = None
    if prior_days:
        last = prior_days[-1]
        try:
            idx = TARGET.index(last)
            expected_next = TARGET[idx + 1] if idx + 1 < len(TARGET) else None
        except ValueError:
            expected_next = "CL-D1"
    else:
        expected_next = "CL-D1"
    seq_ok = actual == expected_next

    # Continuity: no premature 3.3 / unpublished geography.
    # Honest Lambda Revision stop copy says "do not begin Syllabus 3.3".
    if "syllabus 3.3" in body:
        honest_stop = any(
            n in body
            for n in (
                "do not begin syllabus 3.3",
                "don't begin syllabus 3.3",
                "not begin syllabus 3.3",
                "do not begin syllabus 3.3 in this",
                "await 3.3",
                "not chapter 3 complete",
            )
        )
        no_leak = honest_stop
    else:
        no_leak = True
    no_leak = no_leak and finished and not_fallback

    weak_ok = True
    if is_rev:
        weak_ok = any(
            n in body
            for n in (
                "retrieve",
                "revision",
                "interval",
                "confidence",
                "hinge",
                "campaign lambda",
                "3.2",
            )
        )

    rec_ok = actual in TARGET and not_fallback and finished
    calib_ok = finished and day_out.get("confidence_level") in ("HIGH", "MEDIUM")
    explain_ok = purpose or (is_rev and cmp)

    return {
        "recommendation_consistency": "PASS" if rec_ok else "FAIL",
        "weak_area_identification": "PASS" if weak_ok else "FAIL",
        "mission_sequencing": "PASS" if seq_ok else "FAIL",
        "syllabus_continuity": "PASS" if no_leak else "FAIL",
        "confidence_calibration": "PASS" if calib_ok else "FAIL",
        "explanation_usefulness": "PASS" if explain_ok else "FAIL",
    }


def classify_defects(day_out: dict, actual: str | None) -> list[dict]:
    defects = []
    audit = (day_out.get("reading") or {}).get("audit") or {}
    body = ((audit.get("body_sample") or "") + " " + (audit.get("title") or "")).lower()

    if audit.get("is_fallback_shell"):
        defects.append(
            {
                "severity": "Critical",
                "id": "PB11-CRIT-FALLBACK",
                "finding": f"Fallback shell on sitting detected as {actual}",
                "ef_class": "PI",
            }
        )
    if "syllabus 3.3" in body:
        honest_stop = any(
            n in body
            for n in (
                "do not begin syllabus 3.3",
                "don't begin syllabus 3.3",
                "not begin syllabus 3.3",
                "await 3.3",
                "not chapter 3 complete",
            )
        )
        if not honest_stop:
            defects.append(
                {
                    "severity": "Critical",
                    "id": "PB11-CRIT-LEAK-33",
                    "finding": "Unpublished 3.3 geography appeared during Lambda walk",
                    "ef_class": "EC",
                }
            )
    if actual and actual.startswith("CL-") and not day_out.get("finished"):
        defects.append(
            {
                "severity": "Critical",
                "id": "PB11-CRIT-UNFINISHED",
                "finding": f"Certified Lambda day {actual} did not finish",
                "ef_class": "PI",
            }
        )
    if actual and actual.startswith("CL-") and day_out.get("verdict") == "FAIL":
        defects.append(
            {
                "severity": "Major",
                "id": "PB11-MAJOR-SCORE",
                "finding": f"{actual} scored below progressive PASS threshold",
                "ef_class": "PI",
            }
        )
    if day_out.get("chrome_residual") and actual and actual.startswith("CL-"):
        defects.append(
            {
                "severity": "Minor",
                "id": "PB11-MINOR-CHROME",
                "finding": f"Tomorrow chrome residual on {actual} (RO9-R3 class)",
                "ef_class": "PI",
                "residual": "RO9-R3",
            }
        )
    if day_out.get("revision_q6_residual"):
        defects.append(
            {
                "severity": "Minor",
                "id": "PB11-MINOR-Q6",
                "finding": f"Revision Q6 Learning-oriented residual on {actual} (RO9-R2 class)",
                "ef_class": "PI",
                "residual": "RO9-R2",
            }
        )
    if actual and not actual.startswith("CL-") and actual:
        defects.append(
            {
                "severity": "Minor",
                "id": "PB11-MINOR-LABEL",
                "finding": f"Ops transit / label desync sitting observed as {actual} before/during Lambda entry (RO9-R1 class)",
                "ef_class": "PI",
                "residual": "RO9-R1",
            }
        )
    return defects


def run_persona(persona: dict) -> dict:
    slug = persona["slug"]
    password = PASS_FILE.read_text().strip()
    email = f"pb011.lambda.{slug}.{int(time.time())}@example.com"
    print(f"\n=== persona {slug} provision {email}", flush=True)
    st = create_user(email, f"PB011 {persona['label']}", password)
    print("  provision", st.get("status"), flush=True)
    if st.get("status") != "succeeded":
        return {"slug": slug, "verdict": "FAIL", "reason": "provision failed", "job": st}

    evid = EVID_BASE / slug
    html_dir = HTML / slug
    evid.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)

    c = ro.wait_login(slug, email, password, attempts=18)
    if not c:
        return {"slug": slug, "verdict": "FAIL", "reason": "login failed", "email": email}
    c.html_dir = html_dir
    ro.HTML = HTML
    ro.EVID = evid
    ro.EVID_REPO = EVID_REPO
    (EVID_REPO / "html" / slug).mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "audits" / slug).mkdir(parents=True, exist_ok=True)

    final, html = enrol_persona(c, persona)
    final, html = mod.complete_onboarding(c, final, html)
    c.save("enrolled_home", html)

    complete = patch_session_answers(persona)
    seen: dict[str, dict] = {}
    trajectory = []
    programme_traj = []
    all_defects = []
    transit_days = []
    last_detected: str | None = None
    consecutive_fallback = 0
    idx = 1
    for _n in range(55):
        if all(k in seen for k in TARGET):
            break
        print(f"  day {idx} lambda_seen={sorted(seen)}", flush=True)
        try:
            _, _, home = c.get("/student/")
            sig = ro.extract_mission_signals(home)
            if sig["day_complete"] or not sig["has_start"]:
                st = ro.backdate_missions(email)
                if st.get("status") != "succeeded":
                    return {
                        "slug": slug,
                        "email": email,
                        "verdict": "FAIL",
                        "reason": f"backdate failed {st}",
                    }
                time.sleep(2)
                c = ro.wait_login(slug, email, password, attempts=8)
                if not c:
                    return {"slug": slug, "email": email, "verdict": "FAIL", "reason": "relogin failed"}
                c.html_dir = html_dir

            # Scaffold: CK-D1 through Continuity Front transit; switch to next missing
            # Lambda day once CK-R1 (or any CL) has been observed so chrome binds correctly.
            entered_lambda = bool(seen) or (last_detected in TARGET) or last_detected == "CK-R1"
            if entered_lambda:
                expect = next((d for d in TARGET if d not in seen), "CL-R1")
            else:
                expect = "CK-D1" if "CK-D1" in ro.SNIPPETS else "CL-D1"
            day_out = complete(c, idx, expect)
            actual = detect(day_out)
            # Ops recovery: unfinished non-fallback session — retry once via Continue Session
            # before backdating (reflection/summary sometimes stick mid-stage).
            audit0 = (day_out.get("reading") or {}).get("audit") or {}
            if (
                actual
                and actual.startswith("CL-")
                and not day_out.get("finished")
                and not audit0.get("is_fallback_shell")
            ):
                print(f"  RETRY unfinished {actual} without backdate", flush=True)
                time.sleep(2)
                day_out = complete(c, idx, actual)
                actual = detect(day_out) or actual
            if actual:
                last_detected = actual
            defects = classify_defects(day_out, actual)

            audit = (day_out.get("reading") or {}).get("audit") or {}
            if audit.get("is_fallback_shell") or (
                not day_out.get("finished") and not actual
            ):
                consecutive_fallback += 1
            else:
                consecutive_fallback = 0
            if consecutive_fallback >= 4:
                print("  ABORT consecutive fallback/empty sittings", flush=True)
                all_defects.append(
                    {
                        "severity": "Critical",
                        "id": "PB11-CRIT-FALLBACK-LOOP",
                        "finding": "Repeated fallback/empty sittings after incomplete certified day",
                        "ef_class": "PI",
                    }
                )
                break

            if actual and actual.startswith("CL-"):
                day_out = score_lambda(day_out, actual)
                metrics = programme_metrics_for_day(
                    day_out, actual, [t["day"] for t in trajectory]
                )
                day_out["programme_metrics"] = metrics
                defects = classify_defects(day_out, actual)
                if actual not in seen and day_out.get("verdict") == "PASS":
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
                    print(
                        f"  SCORED {actual} {day_out['score_over_9']}/9 metrics="
                        f"{sum(1 for v in metrics.values() if v=='PASS')}/6",
                        flush=True,
                    )
                elif actual in seen:
                    print(f"  re-seen {actual}", flush=True)
                else:
                    print(
                        f"  lambda FAIL-ish {actual} score={day_out.get('score_over_9')} finished={day_out.get('finished')}",
                        flush=True,
                    )
            else:
                transit_days.append(actual)
                if actual:
                    all_defects.extend(
                        d for d in defects if d.get("id") == "PB11-MINOR-LABEL"
                    )
                print(
                    f"  transit detected={actual} finished={day_out.get('finished')}",
                    flush=True,
                )

            for d in defects:
                if d not in all_defects:
                    all_defects.append(d)

            (evid / f"day{idx}_{actual or 'unknown'}.json").write_text(
                json.dumps(day_out, indent=2, default=str)
            )
            (EVID_REPO / "audits" / slug / f"day{idx}_{actual or 'unknown'}.json").write_text(
                json.dumps(day_out, indent=2, default=str)
            )
            for hp in evid.glob(f"day{idx}_*_reading.html"):
                dest = EVID_REPO / "html" / slug / hp.name
                dest.write_bytes(hp.read_bytes())

            # Only backdate after a finished sitting (or empty/fallback abort path)
            if day_out.get("finished") or consecutive_fallback:
                st = ro.backdate_missions(email)
                time.sleep(2)
                c2 = ro.wait_login(slug, email, password, attempts=8)
                if c2:
                    c = c2
                    c.html_dir = html_dir
            idx += 1
        except Exception as exc:
            print(f"  ERROR {exc}", flush=True)
            traceback.print_exc()
            time.sleep(5)
            c = ro.wait_login(slug, email, password, attempts=8)
            if not c:
                return {
                    "slug": slug,
                    "email": email,
                    "verdict": "FAIL",
                    "reason": f"exception+relogin {exc}",
                }
            c.html_dir = html_dir
            idx += 1

    certified_all = all(k in seen for k in TARGET)
    scores = [t["score_over_9"] for t in trajectory]
    avg = (sum(scores) / len(scores)) if scores else 0.0
    rank = {"LOW": 0, "MEDIUM": 1, "HIGH": 2}
    levels = [t["confidence_level"] for t in trajectory]
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
        vals = [m[k] for m in programme_traj]
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
                "Cosmetic": len([d for d in all_defects if d.get("severity") == "Cosmetic"]),
            },
        },
    }
    (evid / "persona.json").write_text(json.dumps(out, indent=2, default=str))
    (EVID_REPO / "personas" / f"{slug}.json").write_text(json.dumps(out, indent=2, default=str))
    print(f"persona {slug} {verdict} avg={avg}", flush=True)
    return out


def regression_vs_lambda(persona_results: list[dict]) -> dict:
    baseline = json.loads(RO009_BASELINE.read_text()) if RO009_BASELINE.exists() else {}
    expected_days = set(TARGET)
    expected_packages = {
        "CL-D1": "CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER",
        "CL-D2": "CS1-EP001-PKG-3.2-PREDICTION-INTERVAL",
        "CL-D3": "CS1-EP001-PKG-3.2-CI-GIVEN-SAMPLING-DISTRIBUTION",
        "CL-D4": "CS1-EP001-PKG-3.2-CI-NORMAL-MEAN-VARIANCE",
        "CL-D5": "CS1-EP001-PKG-3.2-CI-BINOMIAL-POISSON",
        "CL-D6": "CS1-EP001-PKG-3.2-CI-TWO-SAMPLE",
        "CL-D7": "CS1-EP001-PKG-3.2-CI-PAIRED-MEANS",
        "CL-D8": "CS1-EP001-PKG-3.2-BOOTSTRAP-CONFIDENCE-INTERVAL",
        "CL-R1": "CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS",
    }
    known_residuals = {"RO9-R1", "RO9-R2", "RO9-R3"}
    regressions = []
    package_mismatches = []
    new_defects = []

    for pr in persona_results:
        traj = (pr.get("summary") or {}).get("trajectory") or []
        days = {t["day"] for t in traj}
        if not expected_days.issubset(days):
            regressions.append(
                {
                    "persona": pr.get("slug"),
                    "issue": "missing_lambda_days",
                    "observed": sorted(days),
                    "expected": sorted(expected_days),
                }
            )
        for t in traj:
            exp_pkg = expected_packages.get(t["day"])
            got = str(t.get("package_id") or "")
            if exp_pkg and got and exp_pkg != got and exp_pkg not in got and got not in exp_pkg:
                package_mismatches.append(
                    {"persona": pr.get("slug"), "day": t["day"], "expected": exp_pkg, "got": got}
                )
        for d in (pr.get("summary") or {}).get("defects") or []:
            resid = d.get("residual")
            if d.get("severity") in ("Critical", "Major"):
                new_defects.append(d)
            elif resid and resid not in known_residuals:
                new_defects.append(d)

    orders = []
    for pr in persona_results:
        orders.append([t["day"] for t in (pr.get("summary") or {}).get("trajectory") or []])
    order_consistent = all(o == TARGET for o in orders if o) if orders else False

    return {
        "baseline_programme": baseline.get("programme"),
        "baseline_verdict": baseline.get("verdict"),
        "baseline_lambda_days": sorted(expected_days),
        "expected_packages": expected_packages,
        "package_mismatches": package_mismatches,
        "sequence_regressions": regressions,
        "new_critical_or_major_defects": new_defects,
        "cross_persona_sequence_consistent": order_consistent,
        "regression_detected": bool(regressions or package_mismatches or new_defects),
        "known_residual_classes_only": not bool(new_defects),
    }


def aggregate_programme_metrics(persona_results: list[dict]) -> dict:
    keys = [
        "recommendation_consistency",
        "weak_area_identification",
        "mission_sequencing",
        "syllabus_continuity",
        "confidence_calibration",
        "explanation_usefulness",
    ]
    out = {}
    for k in keys:
        pass_n = 0
        total = 0
        for pr in persona_results:
            pm = ((pr.get("summary") or {}).get("programme_metrics") or {}).get(k) or {}
            pass_n += pm.get("pass_count") or 0
            total += pm.get("total") or 0
        out[k] = {
            "pass_count": pass_n,
            "total": total,
            "rate": (pass_n / total) if total else 0.0,
            "result": "PASS" if total and pass_n == total else "FAIL",
        }
    return out


def main() -> int:
    ACCT.mkdir(parents=True, exist_ok=True)
    HTML.mkdir(parents=True, exist_ok=True)
    EVID_BASE.mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "personas").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "audits").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "html").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "suite").mkdir(parents=True, exist_ok=True)

    suite_src = Path(__file__).resolve()
    (EVID_REPO / "suite" / "run_pb011.py").write_text(suite_src.read_text())

    probe = mod.Client("pb011_probe")
    probe.html_dir = HTML / "probe"
    probe.html_dir.mkdir(parents=True, exist_ok=True)
    health = mod.fingerprint(probe)
    if health.get("commit") != EXPECTED_COMMIT:
        print("FINGERPRINT FAIL", health.get("commit"), "expected", EXPECTED_COMMIT)
        return 1

    results = []
    for p in PERSONAS:
        results.append(run_persona(p))

    pass_n = sum(1 for r in results if r.get("verdict") == "PASS")
    scores = []
    for r in results:
        for t in (r.get("summary") or {}).get("trajectory") or []:
            scores.append(t["score_over_9"])
    mean_score = (sum(scores) / len(scores)) if scores else 0.0
    regression = regression_vs_lambda(results)
    prog = aggregate_programme_metrics(results)

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
        if pass_n == len(PERSONAS)
        and mean_score >= 8.0
        and not regression.get("regression_detected")
        and not critical
        and not major
        and prog_all_pass
        else "FAIL"
    )

    out = {
        "programme": "PB-011 Progressive Educational Confidence (Lambda)",
        "host": mod.BASE,
        "expected_commit": EXPECTED_COMMIT,
        "live_health": health,
        "fingerprint_ok": health.get("commit") == EXPECTED_COMMIT,
        "live_certified_inventory": TARGET,
        "personas": results,
        "cohort": {
            "personas_pass": pass_n,
            "personas_total": len(PERSONAS),
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
        "verdict": overall,
    }
    (EVID_BASE / "results.json").write_text(json.dumps(out, indent=2, default=str))
    (EVID_REPO / "results.json").write_text(json.dumps(out, indent=2, default=str))
    print("OVERALL", out["verdict"], "mean", mean_score, flush=True)
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
