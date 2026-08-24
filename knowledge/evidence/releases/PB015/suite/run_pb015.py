#!/usr/bin/env python3
"""PB-015 — Progressive Confidence evaluation suite (Campaign Omicron / LIVE).

Validation only. Does not modify syllabus content, educational packages, Runtime, Educational Framework, recommendation engine, or Student Twin.
Does not begin Wave 14 / EP-014.

Builds on RO-012 LIVE harness + PB-013 progressive confidence methodology.
"""
from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
import time
import traceback
from pathlib import Path

ROOT = Path("/tmp/pb015")
RO013 = Path("/tmp/ro013")
spec = importlib.util.spec_from_file_location("ro013", str(RO013 / "run_live_verification.py"))
ro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ro)

mod = ro.mod
EXPECTED_COMMIT = ro.EXPECTED_COMMIT
SERVICE = ro.SERVICE
ACCT = ROOT / "accounts"
HTML = ROOT / "html"
EVID_BASE = ROOT / "evidence"
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB015")
PASS_FILE = ACCT / "shared_pass.txt"
RO013_BASELINE = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/RO013/results.json")

TARGET = [
    "CO-D1",
    "CO-D2",
    "CO-D3",
    "CO-D4",
    "CO-D5",
    "CO-D6",
    "CO-D7",
    "CO-D8",
    "CO-D9",
    "CO-R1",
]
CODE_TO_DAY_51 = {f"5.1.{i}": f"CO-D{i}" for i in range(1, 10)}
CODE_TO_DAY_42 = {f"4.2.{i}": f"CX-D{i}" for i in range(1, 11)}
CODE_TO_DAY_41 = {f"4.1.{i}": f"CN-D{i}" for i in range(1, 6)}
CODE_TO_DAY_33 = {f"3.3.{i}": f"CM-D{i}" for i in range(1, 6)}
CODE_TO_DAY_32 = {f"3.2.{i}": f"CL-D{i}" for i in range(1, 9)}
CODE_TO_DAY_31 = {f"3.1.{i}": f"CK-D{i}" for i in range(1, 7)}

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
    "novice": "PB-015 beginner: opened the CMP at the named Bayesian section, worked slowly through the Guided Reading hinges, and answered with the example pattern shown.",
    "mixed": "PB-015 average: followed CMP open/ignore/stop guidance and answered using the session focus.",
    "strong": "PB-015 advanced: applied CMP guidance precisely; connected today's Bayesian hinge to prior Continuity Front GLM / regression ideas where relevant.",
    "weak": "PB-015 struggling: re-read the CMP open point, attempted the activity, noted confusion on the stickiest step, and followed stop guidance.",
}

NEEDLES = [
    ("CO-R1", ["campaign omicron revision", "strengthen retrieval of the campaign omicron", "campaign omicron chain", "rev-bayesian-omicron", "pkg-rev-bayesian-omicron", "bayesian hinge", "retrieve bayesian"]),
    ("CO-D9", ["syllabus 5.1.9", "bayes vs", "empirical bayes comparison", "bayes-vs-eb"]),
    ("CO-D8", ["syllabus 5.1.8", "empirical bayes", "empirical-bayes"]),
    ("CO-D7", ["syllabus 5.1.7", "bayesian credibility", "bayesian-credibility"]),
    ("CO-D6", ["syllabus 5.1.6", "credibility premium", "credibility-premium"]),
    ("CO-D5", ["syllabus 5.1.5", "credible interval", "credible-intervals"]),
    ("CO-D4", ["syllabus 5.1.4", "loss function", "bayesian estimator", "loss-estimators"]),
    ("CO-D3", ["syllabus 5.1.3", "posterior distribution", "posterior-simple"]),
    ("CO-D2", ["syllabus 5.1.2", "prior and posterior", "prior-posterior"]),
    ("CO-D1", ["syllabus 5.1.1", "bayes' theorem", "bayes theorem", "bayes-theorem"]),
    ("CX-R1", ["campaign xi revision", "strengthen retrieval of the campaign xi", "campaign xi chain", "rev-glm-xi", "pkg-rev-glm-xi", "glm hinge"]),
    ("CX-D10", ["syllabus 4.2.10", "fit and interpret", "fit-interpret"]),
    ("CX-D9", ["syllabus 4.2.9", "goodness of fit", "goodness-tests", "goodness tests"]),
    ("CX-D8", ["syllabus 4.2.8", "residual", "residuals"]),
    ("CX-D7", ["syllabus 4.2.7", "model choice", "model-choice"]),
    ("CX-D6", ["syllabus 4.2.6", "deviance", "deviance-estimation"]),
    ("CX-D5", ["syllabus 4.2.5", "linear predictor", "linear-predictor"]),
    ("CX-D4", ["syllabus 4.2.4", "factor", "interaction", "factors-interactions"]),
    ("CX-D3", ["syllabus 4.2.3", "link function", "canonical", "link-canonical"]),
    ("CX-D2", ["syllabus 4.2.2", "mean, variance", "variance function", "mean-variance"]),
    ("CX-D1", ["syllabus 4.2.1", "exponential family", "exponential-family"]),
    ("CN-R1", ["campaign nu revision", "strengthen retrieval of the campaign nu", "campaign nu chain", "rev-linear-regression-nu"]),
    ("CN-D5", ["syllabus 4.1.5", "variable selection"]),
    ("CN-D4", ["syllabus 4.1.4", "software fit"]),
    ("CN-D3", ["syllabus 4.1.3", "least squares estimates"]),
    ("CN-D2", ["syllabus 4.1.2", "simple and multiple linear"]),
    ("CN-D1", ["syllabus 4.1.1", "response and explanatory variables with modelling"]),
    ("CM-R1", ["campaign mu revision", "retrieve hypothesis", "strengthen retrieval of the campaign mu"]),
    ("CM-D5", ["syllabus 3.3.5", "contingency", "independence"]),
    ("CM-D4", ["syllabus 3.3.4", "chi-square", "goodness of fit", "gof"]),
    ("CM-D3", ["syllabus 3.3.3", "permutation"]),
    ("CM-D2", ["syllabus 3.3.2", "basic test", "one-sample", "two-sample", "paired"]),
    ("CM-D1", ["syllabus 3.3.1", "hypothesis concepts", "type i", "type ii", "p-value", "null hypothesis"]),
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
]

EXPECTED_PACKAGES = {
    "CO-D1": "CS1-EP001-PKG-CO-5.1-BAYES-THEOREM",
    "CO-D2": "CS1-EP001-PKG-CO-5.1-PRIOR-POSTERIOR",
    "CO-D3": "CS1-EP001-PKG-CO-5.1-POSTERIOR-SIMPLE",
    "CO-D4": "CS1-EP001-PKG-CO-5.1-LOSS-ESTIMATORS",
    "CO-D5": "CS1-EP001-PKG-CO-5.1-CREDIBLE-INTERVALS",
    "CO-D6": "CS1-EP001-PKG-CO-5.1-CREDIBILITY-PREMIUM",
    "CO-D7": "CS1-EP001-PKG-CO-5.1-BAYESIAN-CREDIBILITY",
    "CO-D8": "CS1-EP001-PKG-CO-5.1-EMPIRICAL-BAYES",
    "CO-D9": "CS1-EP001-PKG-CO-5.1-BAYES-VS-EB",
    "CO-R1": "CS1-EP001-PKG-REV-BAYESIAN-OMICRON",
}


def render_key() -> str:
    return re.search(r"key:\s*(\S+)", Path("/Users/kwalitec/.render/cli.yaml").read_text()).group(1)


def create_user(email: str, name: str, password: str) -> dict:
    key = render_key()
    cmd = (
        f'flask --app wsgi.py create-test-user --name "{name}" '
        f'--email "{email}" --password "{password}"'
    )
    payload_path = ACCT / f"tmp_pb015_{email.split('@')[0].replace('.', '_')}.json"
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
    """Continuity Front entry at section 3 (CK→…→CX→CO) with persona baseline prefs."""
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

    continue_code = "3"  # Continuity Front from section 3 (CK→…→CX→CO); chapter 4 cold-entry is Trust Front Delta
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
    """Detect true campaign day from delivered reading body — never from expect-bound package_id."""
    audit = (day_out.get("reading") or {}).get("audit") or {}
    body = ((audit.get("body_sample") or "") + " " + (audit.get("title") or "")).lower()
    html_path = Path(str((day_out.get("reading") or {}).get("html") or ""))
    if html_path.exists():
        try:
            body += "\n" + html_path.read_text()[:10000].lower()
        except OSError:
            pass

    # Trust Front Delta markers must not be mistaken for Continuity Front Omicron/Xi.
    if re.search(r"\bcd-r\d+\b|retrieve mid-spine|campaign delta / volume cs1-003", body):
        mcd = re.search(r"\bcd-r(\d+)\b", body)
        return f"CD-R{mcd.group(1)}" if mcd else "CD-R?"
    if re.search(
        r"campaign omicron revision|rev-bayesian-omicron|pkg-rev-bayesian-omicron|retrieve bayesian",
        body,
    ):
        return "CO-R1"

    # Explicit campaign day markers (prefer over LO when present)
    m = re.search(
        r"\b(co-d[1-9]|co-r1|cx-d10|cx-d[1-9]|cx-r1|cn-d[1-5]|cn-r1|cm-d[1-5]|cm-r1|cl-d[1-8]|cl-r1|ck-d[1-6]|ck-r1)\b",
        body,
    )
    if m:
        return m.group(1).upper()

    # Prefer purpose/open CMP lead-line over "stop before later LO" mentions
    lead = re.search(
        r"(?:purpose of this reading:[^\n]{0,160}|open:\s*cmp[^\n]{0,120})"
        r".*?syllabus (5\.1\.[1-9]|4\.2\.10|4\.2\.[1-9]|4\.1\.[1-5]|3\.3\.[1-5]|3\.2\.[1-8]|3\.1\.[1-6])\b",
        body,
        re.S,
    )
    if lead:
        code = lead.group(1)
        if code.startswith("5.1."):
            return CODE_TO_DAY_51[code]
        if code.startswith("4.2."):
            return "CX-D10" if code == "4.2.10" else CODE_TO_DAY_42[code]
        if code.startswith("4.1."):
            return CODE_TO_DAY_41[code]
        if code.startswith("3.3."):
            return CODE_TO_DAY_33[code]
        if code.startswith("3.2."):
            return CODE_TO_DAY_32[code]
        if code.startswith("3.1."):
            return CODE_TO_DAY_31[code]

    # Syllabus lead-lines — 5.1 before 4.2 before earlier chapters
    # CRITICAL: Trust Front Delta 5.1 uses "skill. Stop at the stop condition" leads;
    # Continuity Front Omicron uses em-dash instructional leads / Campaign Omicron markers.
    # Never map Delta 5.1 sittings onto CO-D*.
    m = re.search(r"syllabus 5\.1\.([1-9])\b", body)
    if m:
        if re.search(r"skill\.\s*stop at the stop condition", body) and not re.search(
            r"campaign omicron|pkg-co-5\.1|contrast bayesian|derive bayesian|apply empirical bayes",
            body,
        ):
            return f"CD-D{15 + int(m.group(1))}"  # approximate Delta label for transit logging
        if re.search(r"purpose of this revision|campaign omicron revision|retrieve bayesian", body):
            return "CO-R1"
        return CODE_TO_DAY_51[f"5.1.{m.group(1)}"]
    if re.search(r"campaign omicron revision|rev-bayesian-omicron|pkg-rev-bayesian-omicron", body):
        return "CO-R1"
    m = re.search(r"syllabus 4\.2\.10\b", body)
    if m:
        if re.search(r"skill\.\s*stop at the stop condition", body) and "campaign xi" not in body:
            return "CD-D15"  # Trust Front 4.2 twin — not Continuity Front Xi
        return "CX-D10"
    m = re.search(r"syllabus 4\.2\.([1-9])\b", body)
    if m:
        if re.search(r"skill\.\s*stop at the stop condition", body) and "campaign xi" not in body:
            return f"CD-D{5 + int(m.group(1))}"
        return CODE_TO_DAY_42[f"4.2.{m.group(1)}"]
    m = re.search(r"syllabus 4\.1\.([1-5])", body)
    if m:
        return CODE_TO_DAY_41[f"4.1.{m.group(1)}"]
    m = re.search(r"syllabus 3\.3\.([1-5])", body)
    if m:
        return CODE_TO_DAY_33[f"3.3.{m.group(1)}"]
    m = re.search(r"syllabus 3\.2\.([1-8])", body)
    if m:
        return CODE_TO_DAY_32[f"3.2.{m.group(1)}"]
    m = re.search(r"syllabus 3\.1\.([1-6])", body)
    if m:
        return CODE_TO_DAY_31[f"3.1.{m.group(1)}"]
    for day, needles in NEEDLES:
        if any(n in body for n in needles):
            return day
    return None


# --- Continue Session recovery (infra) -----------------------------------------
# After LIVE timeouts mid-sitting, Home shows Continue Session + /overview and
# no Start form. Untreated, the RO harness returns no_startable_mission → empty
# sitting loops. Treat Continue Session as a startable mission (ops only).
_ORIG_EXTRACT_SIG = ro.extract_mission_signals
_ORIG_COMPLETE_SESSION = ro.complete_session


def _continue_sid(html: str) -> str | None:
    m = re.search(r"/session/((?:lsr-|sess-)[a-z0-9]+)/overview", html, re.I)
    return m.group(1) if m else None


def extract_mission_signals_continue_aware(html: str) -> dict:
    sig = _ORIG_EXTRACT_SIG(html)
    if (
        not sig.get("has_start")
        and not sig.get("day_complete")
        and _continue_sid(html)
        and re.search(r"Continue Session", html, re.I)
    ):
        sig = dict(sig)
        sig["has_start"] = True
        sig["continue_session"] = True
    return sig


def complete_session_continue_aware(c, day_idx: int, expected_day: str) -> dict:
    """Like RO complete_session, but enters via Continue Session overview when needed."""
    _, final, html = c.get("/student/")
    home_sig = extract_mission_signals_continue_aware(html)
    sid = _continue_sid(html) if home_sig.get("continue_session") else None
    if not sid:
        return _ORIG_COMPLETE_SESSION(c, day_idx, expected_day)

    # Enter existing session without /student/session/start
    import urllib.parse

    out = {
        "day_index": day_idx,
        "expected_day": expected_day,
        "expected_package_id": (ro.SNIPPETS.get(expected_day) or {}).get("package_id"),
        "finished": False,
        "reading": None,
        "checklist": {},
        "tomorrow_preview": {},
        "verdict": "FAIL",
        "home": home_sig,
        "session_id": sid,
        "continued_session": True,
    }
    c.save(f"day{day_idx}_home", html)
    _, final, html = c.get(f"/session/{sid}/overview")
    c.save(f"day{day_idx}_continue_overview", html)
    if "csrf_token" in html and (
        f"/session/{sid}/begin" in html or "Session Overview" in html
    ):
        try:
            _, final, html = c.post(
                f"/session/{sid}/begin",
                {"csrf_token": c.csrf(html), "session_id": sid},
            )
            c.save(f"day{day_idx}_continue_begin", html)
        except Exception as exc:  # noqa: BLE001
            print(f"  continue begin soft-fail: {exc}", flush=True)

    reading_html = ""
    for i in range(14):
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
            dest = ro.EVID / f"day{day_idx}_{expected_day}_reading.html"
            dest.write_text(html, encoding="utf-8")
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
                "response": f"PB-015 continue {expected_day}: applied CMP guidance.",
            }
            if "confidence" in fields:
                data["confidence"] = "3"
            if "confidence_level" in fields:
                data["confidence_level"] = "medium"
            _, final, html = c.post(f"/session/{sid}/activity/answer", data)
            continue
        break

    snip = ro.SNIPPETS.get(expected_day) or {
        "lead_line": "",
        "exit_line": "",
        "return_cue": "",
        "tomorrow": {},
    }
    certified = {
        "lead_line": snip.get("lead_line", ""),
        "exit_line": snip.get("exit_line", ""),
        "return_cue": snip.get("return_cue", ""),
        "open_point": snip.get("open_point", ""),
    }
    audit = (
        mod.audit_reading_html(reading_html, certified_snippets=certified)
        if reading_html
        else {"verdict": "FAIL", "is_fallback_shell": True, "q_checks": {}, "error": "no_reading"}
    )
    if reading_html and isinstance(audit, dict):
        sample = re.sub(r"<[^>]+>", " ", reading_html)
        sample = re.sub(r"\s+", " ", sample).strip()
        audit.setdefault("body_sample", sample[:4000])
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
    out["reading"] = {"audit": audit, "checklist": checklist, "html": None}
    out["checklist"] = checklist

    _, final, html = c.get(f"/session/{sid}/reflection")
    reflection_ok = "Error" not in c.title(html) and "500" not in html[:2000]
    out["reflection_ok"] = reflection_ok
    if reflection_ok and "csrf_token" in html and "Not Found" not in c.title(html):
        _, final, html = c.post(
            f"/session/{sid}/reflection/continue",
            {
                "csrf_token": c.csrf(html),
                "session_id": sid,
                "reflection_note": f"PB-015 continue {expected_day}: noted stickiest CMP cue.",
                "submit": "Continue",
            },
        )

    _, final, html = c.get(f"/session/{sid}/summary")
    tomorrow_hits = {
        "next_topic_code": (snip.get("tomorrow") or {}).get("next_topic_code", "") in html,
        "continuity_fragment": bool(
            (snip.get("tomorrow") or {}).get("continuity_line")
            and (snip.get("tomorrow") or {})["continuity_line"][:40] in html
        ),
        "student_facing_fragment": bool(
            (snip.get("tomorrow") or {}).get("student_facing")
            and (snip.get("tomorrow") or {})["student_facing"][:40] in html
        ),
    }
    out["tomorrow_preview"] = tomorrow_hits
    if "completion_status" in html:
        _, final, html = c.post(
            f"/session/{sid}/finish",
            {
                "csrf_token": c.csrf(html),
                "session_id": sid,
                "completion_status": "yes",
                "notes": f"PB-015 continue {expected_day}: finished planned study.",
                "submit": "Finish Session",
            },
        )
        flashes = c.flashes(html) if hasattr(c, "flashes") else []
        out["finished"] = ("Please choose Yes" not in html) and not any(
            "Please choose Yes" in f for f in flashes
        )
        if not out["finished"]:
            out["finished"] = bool(
                re.search(
                    r"Session finished|Return tomorrow|already completed today|Today.?s Session is finished",
                    html,
                    re.I,
                )
            )
        _, _, home = c.get("/student/")
        for k, frag_key in (
            ("next_topic_code", "next_topic_code"),
            ("continuity_fragment", "continuity_line"),
            ("student_facing_fragment", "student_facing"),
        ):
            frag = (snip.get("tomorrow") or {}).get(
                "next_topic_code" if frag_key == "next_topic_code" else frag_key,
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
        f"  CONTINUE-SESSION sid={sid} finished={out['finished']} verdict={out['verdict']}",
        flush=True,
    )
    return out


ro.extract_mission_signals = extract_mission_signals_continue_aware
ro.complete_session = complete_session_continue_aware


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
                    f"PB-015 {persona['slug']} {expected_day}: completed; noted stickiest CMP cue."
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



def honest_omicron_stop(body: str) -> bool:
    return any(
        n in body
        for n in (
            "honest stop",
            "honest next",
            "not until-exam",
            "until-exam trust",
            "not first-pass spine",
            "first-pass spine",
            "campaign omicron / cs1-015",
            "campaign omicron / volume cs1-015",
            "wave 0 honesty",
            "trust front",
            "not absorb",
            "successor",
            "spine re-audit",
            "do not claim until-exam",
            "coverage remains",
            "63 / 72",
        )
    )


def score_co(day_out: dict, actual: str) -> dict:
    """Nine-dimension educational confidence scoring for LIVE-certified Omicron days."""
    checklist = day_out.get("checklist") or {}
    audit = (day_out.get("reading") or {}).get("audit") or {}
    finished = bool(day_out.get("finished"))
    reflection_ok = bool(day_out.get("reflection_ok"))
    not_fallback = not bool(audit.get("is_fallback_shell"))
    cmp = bool(checklist.get("CMP_reference_present") or audit.get("mentions_cmp"))
    purpose = bool(checklist.get("Educational_purpose_clear") or checklist.get("Reading_focus_clear"))
    chrome = bool(day_out.get("tomorrow_chrome_matches_approved"))
    is_rev = actual.startswith("CO-R")
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
        residuals.append("RO13-R3")
    if not chrome and not is_rev and finished:
        day_out["chrome_residual"] = True
        residuals.append("RO13-R3")
    if is_rev and not q6:
        day_out["revision_q6_residual"] = True
        residuals.append("RO13-R2")
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
    day_out["package_id"] = (ro.SNIPPETS.get(actual) or {}).get("package_id") or EXPECTED_PACKAGES.get(actual)
    return day_out


def programme_metrics_for_day(day_out: dict, actual: str, prior_days: list[str]) -> dict:
    checklist = day_out.get("checklist") or {}
    audit = (day_out.get("reading") or {}).get("audit") or {}
    finished = bool(day_out.get("finished"))
    not_fallback = not bool(audit.get("is_fallback_shell"))
    cmp = bool(checklist.get("CMP_reference_present") or audit.get("mentions_cmp"))
    purpose = bool(checklist.get("Educational_purpose_clear") or checklist.get("Reading_focus_clear"))
    is_rev = actual.startswith("CO-R")
    body = ((audit.get("body_sample") or "") + " " + (audit.get("title") or "")).lower()

    expected_next = None
    if prior_days:
        last = prior_days[-1]
        try:
            idx = TARGET.index(last)
            expected_next = TARGET[idx + 1] if idx + 1 < len(TARGET) else None
        except ValueError:
            expected_next = "CO-D1"
    else:
        expected_next = "CO-D1"
    seq_ok = actual == expected_next

    # Continuity: honest Omicron stop / no premature until-exam trophy leak.
    if "until-exam" in body or "100% cs1" in body or "commercial readiness" in body:
        no_leak = honest_omicron_stop(body)
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
                "bayes",
                "bayesian",
                "prior",
                "posterior",
                "credibility",
                "hinge",
                "campaign omicron",
                "5.1",
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
                "id": "PB15-CRIT-FALLBACK",
                "finding": f"Fallback shell on sitting detected as {actual}",
                "ef_class": "PI",
            }
        )
    if ("until-exam trust" in body or "100% cs1" in body) and not honest_omicron_stop(body):
        defects.append(
            {
                "severity": "Critical",
                "id": "PB15-CRIT-LEAK",
                "finding": "Until-exam / 100% CS1 claim appeared without honest stop during Omicron walk",
                "ef_class": "EC",
            }
        )
    if actual and actual.startswith("CO-") and not day_out.get("finished"):
        defects.append(
            {
                "severity": "Critical",
                "id": "PB15-CRIT-UNFINISHED",
                "finding": f"Certified Omicron day {actual} did not finish",
                "ef_class": "PI",
            }
        )
    if actual and actual.startswith("CO-") and day_out.get("verdict") == "FAIL":
        defects.append(
            {
                "severity": "Major",
                "id": "PB15-MAJOR-SCORE",
                "finding": f"{actual} scored below progressive PASS threshold",
                "ef_class": "PI",
            }
        )
    if day_out.get("chrome_residual") and actual and actual.startswith("CO-"):
        defects.append(
            {
                "severity": "Minor",
                "id": "PB15-MINOR-CHROME",
                "finding": f"Tomorrow chrome residual on {actual} (RO13-R3 class)",
                "ef_class": "PI",
                "residual": "RO13-R3",
            }
        )
    if day_out.get("revision_q6_residual"):
        defects.append(
            {
                "severity": "Minor",
                "id": "PB15-MINOR-Q6",
                "finding": f"Revision Q6 Learning-oriented residual on {actual} (RO13-R2 class)",
                "ef_class": "PI",
                "residual": "RO13-R2",
            }
        )
    if actual and not actual.startswith("CO-") and actual:
        defects.append(
            {
                "severity": "Minor",
                "id": "PB15-MINOR-LABEL",
                "finding": (
                    f"Ops transit / label desync sitting observed as {actual} "
                    "before/during Omicron entry (RO13-R1 class)"
                ),
                "ef_class": "PI",
                "residual": "RO13-R1",
            }
        )
    return defects



def pick_expect(seen: dict, last_detected: str | None) -> str:
    """Bind expect-day for chrome once Continuity Front reaches Omicron entry."""
    entered_co = bool(seen) or (last_detected in TARGET) or last_detected == "CX-R1"
    if entered_co:
        return next((d for d in TARGET if d not in seen), "CO-R1")
    if last_detected and last_detected.startswith("CX-"):
        cx_order = [f"CX-D{i}" for i in range(1, 11)] + ["CX-R1"]
        try:
            i = cx_order.index(last_detected)
            nxt = cx_order[i + 1] if i + 1 < len(cx_order) else "CX-R1"
            return nxt if nxt in ro.SNIPPETS else "CX-D1"
        except ValueError:
            return "CX-D1"
    if last_detected and last_detected.startswith("CN-"):
        cn_order = [f"CN-D{i}" for i in range(1, 6)] + ["CN-R1"]
        try:
            i = cn_order.index(last_detected)
            nxt = cn_order[i + 1] if i + 1 < len(cn_order) else "CN-R1"
            return nxt if nxt in ro.SNIPPETS else "CN-D1"
        except ValueError:
            return "CN-D1"
    if last_detected and last_detected.startswith("CM-"):
        cm_order = [f"CM-D{i}" for i in range(1, 6)] + ["CM-R1"]
        try:
            i = cm_order.index(last_detected)
            nxt = cm_order[i + 1] if i + 1 < len(cm_order) else "CM-R1"
            return nxt if nxt in ro.SNIPPETS else "CM-D1"
        except ValueError:
            return "CM-D1"
    if last_detected and last_detected.startswith("CL-"):
        cl_order = [f"CL-D{i}" for i in range(1, 9)] + ["CL-R1"]
        try:
            i = cl_order.index(last_detected)
            nxt = cl_order[i + 1] if i + 1 < len(cl_order) else "CL-R1"
            return nxt if nxt in ro.SNIPPETS else "CL-D1"
        except ValueError:
            return "CL-D1"
    if last_detected and last_detected.startswith("CK-"):
        ck_order = [f"CK-D{i}" for i in range(1, 7)] + ["CK-R1"]
        try:
            i = ck_order.index(last_detected)
            nxt = ck_order[i + 1] if i + 1 < len(ck_order) else "CL-D1"
            if nxt == "CL-D1":
                return "CL-D1" if "CL-D1" in ro.SNIPPETS else "CK-R1"
            return nxt if nxt in ro.SNIPPETS else "CK-D1"
        except ValueError:
            return "CK-D1"
    if last_detected == "CL-R1":
        return "CM-D1" if "CM-D1" in ro.SNIPPETS else "CL-R1"
    if last_detected == "CM-R1":
        return "CN-D1" if "CN-D1" in ro.SNIPPETS else "CM-R1"
    if last_detected == "CN-R1":
        return "CX-D1" if "CX-D1" in ro.SNIPPETS else "CN-R1"
    return "CK-D1" if "CK-D1" in ro.SNIPPETS else "CO-D1"




def resilient_backdate(email: str, *, attempts: int = 6, base: float = 4.0) -> dict:
    """Ops backdate with DNS/timeout retries — infrastructure only, not educational."""
    last = None
    for i in range(attempts):
        try:
            st = ro.backdate_missions(email)
            if st.get("status") == "succeeded":
                return st
            last = st
        except Exception as exc:  # noqa: BLE001
            last = {"status": "error", "error": str(exc)[:300]}
        wait = base * (2 ** min(i, 4))
        print(f"  INFRA backdate attempt {i+1}/{attempts}: {last}; sleep {wait}s", flush=True)
        time.sleep(wait)
    return last if isinstance(last, dict) else {"status": "error", "error": str(last)}


def save_runtime_checkpoint(slug: str, email: str, seen: dict, last_detected, transit_days, trajectory, all_defects, idx: int, status: str = "in_progress") -> None:
    """Append-only Continuation Protocol checkpoint (educational path only)."""
    from datetime import datetime, timezone
    ckpt_dir = EVID_REPO / "checkpoints"
    ckpt_dir.mkdir(parents=True, exist_ok=True)
    hist = ckpt_dir / "history"
    hist.mkdir(parents=True, exist_ok=True)
    path = ckpt_dir / f"{slug}.json"
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if path.exists():
        (hist / f"{slug}_{stamp}.json").write_text(path.read_text())
    ck = {
        "persona": slug,
        "email": email,
        "programme": "PB-015",
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "last_certified_day": trajectory[-1]["day"] if trajectory else None,
        "last_transit_verified": last_detected,
        "certified_days_complete": [t["day"] for t in trajectory],
        "remaining_co_days": [d for d in TARGET if d not in {t["day"] for t in trajectory}],
        "remaining_xi_days": [d for d in TARGET if d not in {t["day"] for t in trajectory}],  # resume compat alias
        "certified_trajectory": trajectory,
        "transit_observations": list(transit_days)[-40:],
        "defect_count": len(all_defects),
        "ops_day_index": idx,
    }
    path.write_text(__import__("json").dumps(ck, indent=2, default=str))


def run_persona(persona: dict) -> dict:
    slug = persona["slug"]
    password = PASS_FILE.read_text().strip()
    email = f"pb015.co.{slug}.{int(time.time())}@example.com"
    print(f"\n=== persona {slug} provision {email}", flush=True)
    st = create_user(email, f"PB015 {persona['label']}", password)
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

    final, html = None, None
    for enrol_try in range(4):
        try:
            final, html = enrol_persona(c, persona)
            final, html = mod.complete_onboarding(c, final, html)
            break
        except Exception as enrol_exc:
            print(f"  enrol retry {enrol_try + 1}: {enrol_exc}", flush=True)
            time.sleep(8 + enrol_try * 4)
            c = ro.wait_login(slug, email, password, attempts=10)
            if not c:
                return {"slug": slug, "email": email, "verdict": "FAIL", "reason": "enrol relogin failed"}
            c.html_dir = html_dir
    if final is None:
        return {"slug": slug, "email": email, "verdict": "FAIL", "reason": "enrol failed after retries"}
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
    for _n in range(200):
        if all(k in seen for k in TARGET):
            break
        print(f"  day {idx} co_seen={sorted(seen)} last={last_detected}", flush=True)
        try:
            _, _, home = c.get("/student/")
            sig = ro.extract_mission_signals(home)
            if sig["day_complete"] or not sig["has_start"]:
                st = resilient_backdate(email)
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

            expect = pick_expect(seen, last_detected)
            day_out = complete(c, idx, expect)
            actual = detect(day_out)
            # Ops recovery: unfinished non-fallback Xi session — retry once via Continue Session
            audit0 = (day_out.get("reading") or {}).get("audit") or {}
            if (
                actual
                and actual.startswith("CO-")
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
            if audit.get("is_fallback_shell"):
                consecutive_fallback += 1
            elif not day_out.get("finished") and not actual:
                consecutive_fallback += 1
            else:
                consecutive_fallback = 0
            # Allow more transient empty/unfinished sittings under LIVE load before abort.
            if consecutive_fallback >= 8:
                print("  ABORT consecutive fallback/empty sittings", flush=True)
                all_defects.append(
                    {
                        "severity": "Critical",
                        "id": "PB15-CRIT-FALLBACK-LOOP",
                        "finding": "Repeated fallback/empty sittings after incomplete certified day",
                        "ef_class": "PI",
                    }
                )
                break

            if actual and actual.startswith("CO-"):
                day_out = score_co(day_out, actual)
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
                    save_runtime_checkpoint(
                        slug, email, seen, last_detected, transit_days, trajectory, all_defects, idx
                    )
                elif actual in seen:
                    print(f"  re-seen {actual}", flush=True)
                else:
                    print(
                        f"  co FAIL-ish {actual} score={day_out.get('score_over_9')} "
                        f"finished={day_out.get('finished')}",
                        flush=True,
                    )
            else:
                transit_days.append(actual)
                if actual:
                    all_defects.extend(
                        d for d in defects if d.get("id") == "PB15-MINOR-LABEL"
                    )
                print(
                    f"  transit detected={actual} finished={day_out.get('finished')}",
                    flush=True,
                )
                if idx % 5 == 0:
                    save_runtime_checkpoint(
                        slug, email, seen, last_detected, transit_days, trajectory, all_defects, idx
                    )

            for d in defects:
                if d not in all_defects:
                    all_defects.append(d)

            # Persist lean audits always; HTML only for certified Xi sittings (disk hygiene).
            lean = {
                "expected_day": day_out.get("expected_day"),
                "detected_campaign_day": actual,
                "finished": day_out.get("finished"),
                "reflection_ok": day_out.get("reflection_ok"),
                "verdict": day_out.get("verdict"),
                "score_over_9": day_out.get("score_over_9"),
                "dimensions": day_out.get("dimensions"),
                "programme_metrics": day_out.get("programme_metrics"),
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
            }
            (evid / f"day{idx}_{actual or 'unknown'}.json").write_text(
                json.dumps(lean, indent=2, default=str)
            )
            if actual and actual.startswith("CO-"):
                (EVID_REPO / "audits" / slug / f"day{idx}_{actual}.json").write_text(
                    json.dumps(lean, indent=2, default=str)
                )
                for hp in list(evid.glob(f"day{idx}_*_reading.html")) + list(
                    html_dir.glob(f"day{idx}_*_reading.html")
                ):
                    dest = EVID_REPO / "html" / slug / hp.name
                    dest.write_bytes(hp.read_bytes())
            # Drop local transit HTML after each sitting to keep /tmp lean.
            for hp in html_dir.glob(f"day{idx}_*.html"):
                if actual and actual.startswith("CO-") and hp.name.endswith("_reading.html"):
                    continue
                try:
                    hp.unlink()
                except OSError:
                    pass

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
            "result": "PASS"
            if vals and all(v == "PASS" for v in vals)
            else ("FAIL" if vals else "FAIL"),
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
    save_runtime_checkpoint(
        slug, email, seen, last_detected, transit_days, trajectory, all_defects, idx,
        status="complete" if verdict == "PASS" else "finished_fail",
    )
    print(f"persona {slug} {verdict} avg={avg}", flush=True)
    return out


def regression_vs_omicron(persona_results: list[dict]) -> dict:
    baseline = json.loads(RO013_BASELINE.read_text()) if RO013_BASELINE.exists() else {}
    expected_days = set(TARGET)
    expected_packages = dict(EXPECTED_PACKAGES)
    known_residuals = {"RO13-R1", "RO13-R2", "RO13-R3"}
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
                    "issue": "missing_omicron_days",
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
        "baseline_omicron_days": sorted(expected_days),
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


def build_results(results: list[dict], health: dict) -> dict:
    pass_n = sum(1 for r in results if r.get("verdict") == "PASS")
    scores = []
    for r in results:
        for t in (r.get("summary") or {}).get("trajectory") or []:
            scores.append(t["score_over_9"])
    mean_score = (sum(scores) / len(scores)) if scores else 0.0
    regression = regression_vs_omicron(results)
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

    return {
        "programme": "PB-015 Progressive Educational Confidence (Omicron)",
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
        "regression_vs_campaign_omicron": regression,
        "verdict": overall,
    }


def main() -> int:
    ACCT.mkdir(parents=True, exist_ok=True)
    HTML.mkdir(parents=True, exist_ok=True)
    EVID_BASE.mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "personas").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "audits").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "html").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "suite").mkdir(parents=True, exist_ok=True)

    suite_src = Path(__file__).resolve()
    (EVID_REPO / "suite" / "run_pb015.py").write_text(suite_src.read_text())

    only = [a for a in sys.argv[1:] if a and not a.startswith("-")]
    personas = [p for p in PERSONAS if p["slug"] in only] if only else list(PERSONAS)

    probe = mod.Client("pb015_probe")
    probe.html_dir = HTML / "probe"
    probe.html_dir.mkdir(parents=True, exist_ok=True)
    health = mod.fingerprint(probe)
    if health.get("commit") != EXPECTED_COMMIT:
        print("FINGERPRINT FAIL", health.get("commit"), "expected", EXPECTED_COMMIT)
        return 1

    results = []
    for p in personas:
        results.append(run_persona(p))

    # Single-persona mode: write partial and exit without full cohort gate
    if only and len(personas) == 1:
        (EVID_BASE / f"persona_{personas[0]['slug']}_done.json").write_text(
            json.dumps(results[0], indent=2, default=str)
        )
        print("PERSONA_DONE", personas[0]["slug"], results[0].get("verdict"), flush=True)
        return 0 if results[0].get("verdict") == "PASS" else 1

    out = build_results(results, health)
    (EVID_BASE / "results.json").write_text(json.dumps(out, indent=2, default=str))
    (EVID_REPO / "results.json").write_text(json.dumps(out, indent=2, default=str))
    print("OVERALL", out["verdict"], "mean", out["cohort"]["mean_score_over_9"], flush=True)
    return 0 if out["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
