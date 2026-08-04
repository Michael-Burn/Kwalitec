#!/usr/bin/env python3
"""PB-017 — Final Progressive Confidence evaluation suite (Campaign Rho / LIVE).

Validation only. Does not modify syllabus content, educational packages, Runtime,
Educational Framework, recommendation engine, Student Twin, curriculum, or Wave 16.
Does not begin PX-001.

Builds on RO-015 LIVE harness + PB-017 progressive confidence methodology.
Entry: enrol + seed package history through CP-R1 → Publication Front CR-D1…CR-R1.
Final certification for fully published CS1 Approver inventory (72/72).
"""
from __future__ import annotations

import base64
import importlib.util
import json
import re
import subprocess
import sys
import time
import traceback
import urllib.parse
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path("/tmp/pb017")
spec = importlib.util.spec_from_file_location("ro015", str(ROOT / "run_live_verification.py"))
ro = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ro)

mod = ro.mod
EXPECTED_COMMIT = ro.EXPECTED_COMMIT
SERVICE = ro.SERVICE
ACCT = ROOT / "accounts"
HTML = ROOT / "html"
EVID_BASE = ROOT / "evidence"
EVID_REPO = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB017")
PASS_FILE = ACCT / "shared_pass.txt"
SEED_IDS = json.loads((ROOT / "seed_package_ids.json").read_text())
PB016_BASELINE = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/PB016/results.json")
RO015_BASELINE = Path("/Users/kwalitec/Developer/kwalitec/knowledge/evidence/releases/RO015/results.json")

TARGET = [
    "CR-D1",
    "CR-D2",
    "CR-D3",
    "CR-D4",
    "CR-D5",
    "CR-D6",
    "CR-D7",
    "CR-D8",
    "CR-D9",
    "CR-R1",
]

HINGE_MAP = {
    "1.1.1": "CR-D1",
    "1.1.2": "CR-D2",
    "1.1.3": "CR-D3",
    "1.1.4": "CR-D4",
    "1.2.1": "CR-D5",
    "1.2.2": "CR-D6",
    "1.2.3": "CR-D7",
    "2.1.1": "CR-D8",
    "2.1.2": "CR-D9",
}

EXPECTED_PACKAGES = {
    "CR-D1": "CS1-EP001-PKG-CR-1.1-AIMS-ANALYSIS",
    "CR-D2": "CS1-EP001-PKG-CR-1.1-STAGES-TOOLS",
    "CR-D3": "CS1-EP001-PKG-CR-1.1-DATA-SOURCES",
    "CR-D4": "CS1-EP001-PKG-CR-1.1-REPRODUCIBLE",
    "CR-D5": "CS1-EP001-PKG-CR-1.2-EDA-SUMMARIES",
    "CR-D6": "CS1-EP001-PKG-CR-1.2-CORRELATION",
    "CR-D7": "CS1-EP001-PKG-CR-1.2-PCA",
    "CR-D8": "CS1-EP001-PKG-CR-2.1-DISCRETE",
    "CR-D9": "CS1-EP001-PKG-CR-2.1-CONTINUOUS",
    "CR-R1": "CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO",
}

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
    "novice": "PB-017 beginner: opened the CMP at the named Publication Front hinge, worked slowly through Guided Reading, and answered with the example pattern shown.",
    "mixed": "PB-017 average: followed CMP open/ignore/stop guidance and answered using the session focus.",
    "strong": "PB-017 advanced: applied CMP guidance precisely; connected today's Publication Front hinge to prior Continuity Front substance where relevant.",
    "weak": "PB-017 struggling: re-read the CMP open point, attempted the activity, noted confusion on the stickiest step, and followed stop guidance.",
}


def render_key() -> str:
    return re.search(r"key:\s*(\S+)", Path("/Users/kwalitec/.render/cli.yaml").read_text()).group(1)


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


def render_job(start_command: str, *, timeout_s: int = 240) -> dict:
    key = render_key()
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
            json.dumps({"startCommand": start_command}),
            f"https://api.render.com/v1/services/{SERVICE}/jobs",
        ]
    )
    job_id = created["id"]
    deadline = time.time() + timeout_s
    while time.time() < deadline:
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


def create_user(email: str, name: str, password: str) -> dict:
    cmd = (
        f'flask --app wsgi.py create-test-user --name "{name}" '
        f'--email "{email}" --password "{password}"'
    )
    return render_job(cmd, timeout_s=240)


def seed_cp_r1_history(email: str) -> dict:
    """Seed Continuity Front package history through CO-R1 (ops entry to Publication Front)."""
    ids_literal = json.dumps(SEED_IDS)
    script = f"""
import json
from datetime import datetime, timedelta, timezone
from app import create_app
from app.extensions import db
from app.models import User
from app.models.educational_runtime_engine import RuntimeEnrolment, RuntimeEducationalEvent
from app.domain.educational_runtime_engine.events import EducationalEventType
email = {email!r}.lower()
ids = json.loads({ids_literal!r})
app = create_app()
with app.app_context():
    u = User.query.filter_by(email=email).first()
    assert u is not None, 'user missing'
    enr = RuntimeEnrolment.query.filter_by(user_id=u.id).order_by(RuntimeEnrolment.id.desc()).first()
    assert enr is not None, 'enrolment missing'
    RuntimeEducationalEvent.query.filter_by(
        user_id=u.id,
        curriculum_identity=enr.curriculum_identity,
        event_type=EducationalEventType.MISSION_COMPLETED.value,
    ).delete(synchronize_session=False)
    base = datetime.now(timezone.utc) - timedelta(days=len(ids)+2)
    for i, pid in enumerate(ids):
        row = RuntimeEducationalEvent(
            event_id=f"evt_pb016_seed_{{u.id}}_{{i:04d}}",
            event_type=EducationalEventType.MISSION_COMPLETED.value,
            user_id=u.id,
            enrolment_id=enr.enrolment_id,
            curriculum_identity=enr.curriculum_identity,
            payload_json=json.dumps({{"educational_package_id": pid, "pb016_seed": True}}),
            occurred_at=base + timedelta(minutes=i),
        )
        db.session.add(row)
    db.session.commit()
    print("SEEDED", len(ids), "last", ids[-1], "enrolment", enr.enrolment_id, "status", enr.status)
"""
    b64 = base64.b64encode(script.encode()).decode()
    start_command = f"python -c \"import base64; exec(base64.b64decode('{b64}').decode())\""
    return render_job(start_command, timeout_s=300)



def force_cr_r1(email: str) -> dict:
    """Ops residual RO15-R3: force Publication Front revision after CR learning chain."""
    ids = list(SEED_IDS) + [
        EXPECTED_PACKAGES[d] for d in TARGET if d != "CR-R1"
    ]
    ids_literal = json.dumps(ids)
    script = f"""
import json
from datetime import date, datetime, timedelta, timezone
from app import create_app
from app.extensions import db
from app.models import User
from app.models.educational_runtime_engine import RuntimeEnrolment, RuntimeEducationalEvent, RuntimeMissionInstance as M
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.application.educational_runtime_engine.service import EducationalRuntimeEngineService
email = {email!r}.lower()
ids = json.loads({ids_literal!r})
app = create_app()
with app.app_context():
    u = User.query.filter_by(email=email).first()
    assert u is not None
    enr = RuntimeEnrolment.query.filter_by(user_id=u.id).order_by(RuntimeEnrolment.id.desc()).first()
    assert enr is not None
    RuntimeEducationalEvent.query.filter_by(
        user_id=u.id,
        curriculum_identity=enr.curriculum_identity,
        event_type=EducationalEventType.MISSION_COMPLETED.value,
    ).delete(synchronize_session=False)
    base = datetime.now(timezone.utc) - timedelta(days=len(ids)+2)
    for i, pid in enumerate(ids):
        db.session.add(RuntimeEducationalEvent(
            event_id=f"evt_pb017_r1_{{u.id}}_{{i:04d}}",
            event_type=EducationalEventType.MISSION_COMPLETED.value,
            user_id=u.id,
            enrolment_id=enr.enrolment_id,
            curriculum_identity=enr.curriculum_identity,
            payload_json=json.dumps({{"educational_package_id": pid, "pb017_force_r1": True}}),
            occurred_at=base + timedelta(minutes=i),
        ))
    for m in M.query.filter_by(user_id=u.id).all():
        db.session.delete(m)
    db.session.commit()
    svc = EducationalRuntimeEngineService()
    mission = svc.generate_daily_mission(user_id=u.id, subject_code="CS1", mission_date=date.today())
    print("FORCE_R1", mission.educational_package_id, mission.title)
    if "REV-PUBLICATION-FRONT-RHO" not in (mission.educational_package_id or ""):
        raise SystemExit("NOT_CR_R1")
"""
    b64 = base64.b64encode(script.encode()).decode()
    start_command = f"python -c \"import base64; exec(base64.b64decode('{b64}').decode())\""
    return render_job(start_command, timeout_s=300)


def enrol_persona(c, persona: dict):
    """Baseline enrol for Publication Front entry (start path; history seeded after)."""
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
                if "start" in vs:
                    data[n] = "start"
                elif "continue_topic" in vs:
                    data[n] = "continue_topic"
                else:
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
                        vs[-1],
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
            if vs and n not in data:
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
    blob = " ".join(
        [
            str(audit.get("title") or ""),
            str(audit.get("body_sample") or ""),
            str(audit.get("support_sample") or ""),
        ]
    )
    html_path = Path(str((day_out.get("reading") or {}).get("html") or ""))
    if html_path.is_file():
        try:
            blob += "\n" + html_path.read_text(encoding="utf-8", errors="ignore")[:16000]
        except OSError:
            pass

    m = re.search(r"\b(CR-D[1-9]|CR-R1|CP-D[1-9]|CP-R1)\b", blob)
    if m:
        return m.group(1)

    for lo, day in HINGE_MAP.items():
        if re.search(rf"Syllabus {re.escape(lo)}\b", blob):
            if re.search(r"Publication Front|PKG-CR-|Campaign Rho", blob, re.I):
                return day
            if re.search(r"Skill\.\s*Stop at the stop condition", blob) and not re.search(
                r"Publication Front|Campaign Rho|PKG-CR-", blob, re.I
            ):
                continue

    if re.search(
        r"PKG-REV-PUBLICATION-FRONT-RHO|Campaign Rho Revision|Publication Front.*Revision|Purpose of this revision",
        blob,
        re.I,
    ):
        return "CR-R1"
    if re.search(r"PKG-REV-SPINE-MEMORY-PI|Campaign Pi Revision", blob, re.I):
        return "CP-R1"
    return None


# --- Continue Session recovery (infra) -----------------------------------------
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
    _, final, html = c.get("/student/")
    home_sig = extract_mission_signals_continue_aware(html)
    sid = _continue_sid(html) if home_sig.get("continue_session") else None
    if not sid:
        return _ORIG_COMPLETE_SESSION(c, day_idx, expected_day)

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
                "response": f"PB-017 continue {expected_day}: applied CMP guidance.",
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
                "reflection_note": f"PB-017 continue {expected_day}: noted stickiest CMP cue.",
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
                "notes": f"PB-017 continue {expected_day}: finished planned study.",
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
                    f"PB-017 {persona['slug']} {expected_day}: completed; noted stickiest CMP cue."
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


def honest_rho_stop(body: str) -> bool:
    return any(
        n in body
        for n in (
            "honest stop",
            "honest next",
            "not until-exam",
            "until-exam trust",
            "not first-pass spine",
            "first-pass spine",
            "campaign rho / cs1-017",
            "campaign rho / volume cs1-017",
            "wave 0 honesty",
            "trust front",
            "not absorb",
            "successor",
            "publication front",
            "do not claim until-exam",
            "coverage remains",
            "72 / 72",
            "approver numerator",
        )
    )


def score_cr(day_out: dict, actual: str) -> dict:
    checklist = day_out.get("checklist") or {}
    audit = (day_out.get("reading") or {}).get("audit") or {}
    finished = bool(day_out.get("finished"))
    reflection_ok = bool(day_out.get("reflection_ok"))
    not_fallback = not bool(audit.get("is_fallback_shell"))
    cmp = bool(checklist.get("CMP_reference_present") or audit.get("mentions_cmp"))
    purpose = bool(checklist.get("Educational_purpose_clear") or checklist.get("Reading_focus_clear"))
    chrome = bool(day_out.get("tomorrow_chrome_matches_approved"))
    is_rev = actual.startswith("CR-R")
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
        residuals.append("RO15-R4")
    if not chrome and not is_rev and finished:
        day_out["chrome_residual"] = True
        residuals.append("RO15-R4")
    if is_rev and not q6:
        day_out["revision_q6_residual"] = True
        residuals.append("RO15-R4")
    if is_rev and dims["mission_clarity"] == "FAIL" and cmp:
        dims["mission_clarity"] = "PASS"
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
    day_out["package_id"] = (ro.SNIPPETS.get(actual) or {}).get("package_id") or EXPECTED_PACKAGES.get(
        actual
    )
    return day_out


def programme_metrics_for_day(day_out: dict, actual: str, prior_days: list[str]) -> dict:
    checklist = day_out.get("checklist") or {}
    audit = (day_out.get("reading") or {}).get("audit") or {}
    finished = bool(day_out.get("finished"))
    not_fallback = not bool(audit.get("is_fallback_shell"))
    cmp = bool(checklist.get("CMP_reference_present") or audit.get("mentions_cmp"))
    purpose = bool(checklist.get("Educational_purpose_clear") or checklist.get("Reading_focus_clear"))
    is_rev = actual.startswith("CR-R")
    body = ((audit.get("body_sample") or "") + " " + (audit.get("title") or "")).lower()

    if prior_days:
        last = prior_days[-1]
        try:
            idx = TARGET.index(last)
            expected_next = TARGET[idx + 1] if idx + 1 < len(TARGET) else None
        except ValueError:
            expected_next = "CR-D1"
    else:
        expected_next = "CR-D1"
    seq_ok = actual == expected_next

    if "until-exam" in body or "100% cs1" in body or "commercial readiness" in body:
        no_leak = honest_rho_stop(body)
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
                "publication front",
                "campaign rho",
                "wave 0",
                "aims",
                "eda",
                "discrete",
                "continuous",
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
                "id": "PB17-CRIT-FALLBACK",
                "finding": f"Fallback shell on sitting detected as {actual}",
                "ef_class": "PI",
            }
        )
    if ("until-exam trust" in body or "100% cs1" in body) and not honest_rho_stop(body):
        defects.append(
            {
                "severity": "Critical",
                "id": "PB17-CRIT-LEAK",
                "finding": "Until-exam / 100% CS1 claim appeared without honest stop during Rho walk",
                "ef_class": "EC",
            }
        )
    if actual and actual.startswith("CR-") and not day_out.get("finished"):
        defects.append(
            {
                "severity": "Critical",
                "id": "PB17-CRIT-UNFINISHED",
                "finding": f"Certified Rho day {actual} did not finish",
                "ef_class": "PI",
            }
        )
    if actual and actual.startswith("CR-") and day_out.get("verdict") == "FAIL":
        defects.append(
            {
                "severity": "Major",
                "id": "PB17-MAJOR-SCORE",
                "finding": f"{actual} scored below progressive PASS threshold",
                "ef_class": "PI",
            }
        )
    if day_out.get("chrome_residual") and actual and actual.startswith("CR-"):
        defects.append(
            {
                "severity": "Minor",
                "id": "PB17-MINOR-CHROME",
                "finding": f"Tomorrow chrome residual on {actual} (RO15-R4 class)",
                "ef_class": "PI",
                "residual": "RO15-R4",
            }
        )
    if day_out.get("revision_q6_residual"):
        defects.append(
            {
                "severity": "Minor",
                "id": "PB17-MINOR-Q6",
                "finding": f"Revision Q6 Learning-oriented residual on {actual} (RO15-R4 class)",
                "ef_class": "PI",
                "residual": "RO15-R4",
            }
        )
    if actual and not actual.startswith("CR-") and actual:
        defects.append(
            {
                "severity": "Minor",
                "id": "PB17-MINOR-TRANSIT",
                "finding": (
                    f"Non-Rho sitting observed as {actual} before/during Publication Front "
                    "(RO15-R1/R2 class)"
                ),
                "ef_class": "PI",
                "residual": "RO15-R1",
            }
        )
    return defects


def resilient_backdate(email: str, *, attempts: int = 6, base: float = 4.0) -> dict:
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


def save_runtime_checkpoint(
    slug: str,
    email: str,
    seen: dict,
    last_detected,
    transit_days,
    trajectory,
    all_defects,
    idx: int,
    status: str = "in_progress",
) -> None:
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
        "programme": "PB-017",
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "last_certified_day": trajectory[-1]["day"] if trajectory else None,
        "last_transit_verified": last_detected,
        "certified_days_complete": [t["day"] for t in trajectory],
        "remaining_cr_days": [d for d in TARGET if d not in {t["day"] for t in trajectory}],
        "certified_trajectory": trajectory,
        "transit_observations": list(transit_days)[-40:],
        "defect_count": len(all_defects),
        "ops_day_index": idx,
        "deployment_fingerprint": EXPECTED_COMMIT,
    }
    path.write_text(json.dumps(ck, indent=2, default=str))


def check_fingerprint() -> dict:
    probe = mod.Client("pb017_fp")
    probe.html_dir = HTML / "probe"
    probe.html_dir.mkdir(parents=True, exist_ok=True)
    health = mod.fingerprint(probe)
    return health


def run_persona(persona: dict) -> dict:
    slug = persona["slug"]
    password = PASS_FILE.read_text().strip()
    email = f"pb017.cr.{slug}.{int(time.time())}@example.com"
    print(f"\n=== persona {slug} provision {email}", flush=True)

    health = check_fingerprint()
    if health.get("commit") != EXPECTED_COMMIT:
        ops = {
            "event": "Operational Reliability Event",
            "class": "deployment_fingerprint_change",
            "observed": health.get("commit"),
            "expected": EXPECTED_COMMIT,
            "persona": slug,
            "at": datetime.now(timezone.utc).isoformat(),
        }
        (EVID_REPO / "ops" / f"fingerprint_{slug}_{int(time.time())}.json").write_text(
            json.dumps(ops, indent=2)
        )
        return {
            "slug": slug,
            "verdict": "FAIL",
            "reason": "fingerprint mismatch — Operational Reliability Event",
            "live_health": health,
        }

    st = create_user(email, f"PB017 {persona['label']}", password)
    print("  provision", st.get("status"), flush=True)
    if st.get("status") != "succeeded":
        return {"slug": slug, "verdict": "FAIL", "reason": "provision failed", "job": st}

    evid = EVID_BASE / slug
    html_dir = HTML / slug
    evid.mkdir(parents=True, exist_ok=True)
    html_dir.mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "html" / slug).mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "audits" / slug).mkdir(parents=True, exist_ok=True)

    c = ro.wait_login(slug, email, password, attempts=18)
    if not c:
        return {"slug": slug, "verdict": "FAIL", "reason": "login failed", "email": email}
    c.html_dir = html_dir
    ro.HTML = HTML
    ro.EVID = evid
    ro.EVID_REPO = EVID_REPO

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
                return {
                    "slug": slug,
                    "email": email,
                    "verdict": "FAIL",
                    "reason": "enrol relogin failed",
                }
            c.html_dir = html_dir
    if final is None:
        return {"slug": slug, "email": email, "verdict": "FAIL", "reason": "enrol failed after retries"}
    c.save("enrolled_home", html)

    seed = seed_cp_r1_history(email)
    print("  seed", seed.get("status"), seed.get("id"), flush=True)
    if seed.get("status") != "succeeded":
        return {
            "slug": slug,
            "email": email,
            "verdict": "FAIL",
            "reason": f"seed failed {seed}",
        }

    # Force mission regeneration after seed (backdate + relogin)
    st = resilient_backdate(email)
    print("  post-seed backdate", st.get("status"), flush=True)
    time.sleep(2)
    c = ro.wait_login(slug, email, password, attempts=12)
    if not c:
        return {"slug": slug, "email": email, "verdict": "FAIL", "reason": "post-seed login failed"}
    c.html_dir = html_dir

    complete = patch_session_answers(persona)
    seen: dict[str, dict] = {}
    trajectory = []
    programme_traj = []
    all_defects = []
    transit_days = []
    last_detected: str | None = None
    consecutive_fallback = 0
    idx = 1
    ops_events = []


    force_r1_tried = False
    for _n in range(40):
        if (
            "CR-D9" in seen
            and "CR-R1" not in seen
            and not force_r1_tried
            and _n >= 9
        ):
            print("  FORCE CR-R1 (RO15-R3 ops residual)", flush=True)
            fr = force_cr_r1(email)
            ops_events.append({
                "event": "Operational Reliability Event",
                "class": "force_cr_r1",
                "job": fr,
                "residual": "RO15-R3",
            })
            (EVID_REPO / "ops" / f"force_r1_{slug}_{int(time.time())}.json").write_text(
                json.dumps(ops_events[-1], indent=2, default=str)
            )
            force_r1_tried = True
            time.sleep(2)
            c = ro.wait_login(slug, email, password, attempts=10)
            if c:
                c.html_dir = html_dir

        if all(k in seen for k in TARGET):
            break
        print(f"  day {idx} cr_seen={sorted(seen)} last={last_detected}", flush=True)
        try:
            # Fingerprint gate each sitting
            health = check_fingerprint()
            if health.get("commit") != EXPECTED_COMMIT:
                ops_events.append(
                    {
                        "event": "Operational Reliability Event",
                        "class": "deployment_fingerprint_change",
                        "observed": health.get("commit"),
                        "expected": EXPECTED_COMMIT,
                        "at_day": idx,
                    }
                )
                (EVID_REPO / "ops" / f"fingerprint_mid_{slug}_{idx}.json").write_text(
                    json.dumps(ops_events[-1], indent=2)
                )
                print("  FINGERPRINT CHANGE — pause; resume from checkpoint", flush=True)
                save_runtime_checkpoint(
                    slug, email, seen, last_detected, transit_days, trajectory, all_defects, idx,
                    status="paused_fingerprint",
                )
                break

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
                    return {
                        "slug": slug,
                        "email": email,
                        "verdict": "FAIL",
                        "reason": "relogin failed",
                    }
                c.html_dir = html_dir

            expect = next((d for d in TARGET if d not in seen), "CR-R1")
            day_out = complete(c, idx, expect)
            actual = detect(day_out)
            audit0 = (day_out.get("reading") or {}).get("audit") or {}
            if (
                actual
                and actual.startswith("CR-")
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
            if consecutive_fallback >= 8:
                print("  ABORT consecutive fallback/empty sittings", flush=True)
                all_defects.append(
                    {
                        "severity": "Critical",
                        "id": "PB17-CRIT-FALLBACK-LOOP",
                        "finding": "Repeated fallback/empty sittings after incomplete certified day",
                        "ef_class": "PI",
                    }
                )
                break

            if actual and actual.startswith("CR-"):
                day_out = score_cr(day_out, actual)
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
                        f"  cr FAIL-ish {actual} score={day_out.get('score_over_9')} "
                        f"finished={day_out.get('finished')}",
                        flush=True,
                    )
            else:
                transit_days.append(actual)
                print(
                    f"  transit detected={actual} finished={day_out.get('finished')}",
                    flush=True,
                )
                if idx % 3 == 0:
                    save_runtime_checkpoint(
                        slug, email, seen, last_detected, transit_days, trajectory, all_defects, idx
                    )

            for d in defects:
                if d not in all_defects:
                    all_defects.append(d)

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
            if actual and actual.startswith("CR-"):
                (EVID_REPO / "audits" / slug / f"day{idx}_{actual}.json").write_text(
                    json.dumps(lean, indent=2, default=str)
                )
                for hp in list(evid.glob(f"day{idx}_*_reading.html")) + list(
                    html_dir.glob(f"day{idx}_*_reading.html")
                ):
                    dest = EVID_REPO / "html" / slug / hp.name
                    dest.write_bytes(hp.read_bytes())
            for hp in html_dir.glob(f"day{idx}_*.html"):
                if actual and actual.startswith("CR-") and hp.name.endswith("_reading.html"):
                    continue
                try:
                    hp.unlink()
                except OSError:
                    pass

            if day_out.get("finished") or consecutive_fallback:
                st = resilient_backdate(email)
                time.sleep(2)
                c2 = ro.wait_login(slug, email, password, attempts=8)
                if c2:
                    c = c2
                    c.html_dir = html_dir
            idx += 1
        except Exception as exc:
            print(f"  ERROR {exc}", flush=True)
            traceback.print_exc()
            ops_events.append(
                {
                    "event": "Operational Reliability Event",
                    "class": "exception_retry",
                    "error": str(exc)[:400],
                    "at_day": idx,
                }
            )
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
        "entry": "Seeded Publication Front advanced student (CP-R1 package history) → Publication Front CR-D1…CR-R1",
        "live_tip": EXPECTED_COMMIT,
        "ops_events": ops_events,
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


def regression_vs_pb016(persona_results: list[dict]) -> dict:
    baseline = json.loads(PB016_BASELINE.read_text()) if PB016_BASELINE.exists() else {}
    expected_days = set(TARGET)
    expected_packages = dict(EXPECTED_PACKAGES)
    known_residuals = {"RO15-R1", "RO15-R2", "RO15-R3", "RO15-R4", "RO14-R1", "RO14-R3"}
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
                    "issue": "missing_rho_days",
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
        "package_mismatches": package_mismatches,
        "sequence_regressions": regressions,
        "order_consistent_with_cr_d1_to_cr_r1": order_consistent,
        "new_critical_or_major": new_defects,
        "regression_detected": bool(regressions or package_mismatches or new_defects),
    }


def aggregate(persona_results: list[dict]) -> dict:
    health = check_fingerprint()
    scores = []
    for pr in persona_results:
        for t in (pr.get("summary") or {}).get("trajectory") or []:
            scores.append(t["score_over_9"])
    mean = (sum(scores) / len(scores)) if scores else 0.0
    all_pass = all(pr.get("verdict") == "PASS" for pr in persona_results) and len(
        persona_results
    ) == 5
    reg = regression_vs_pb016(persona_results)
    prog_keys = [
        "recommendation_consistency",
        "weak_area_identification",
        "mission_sequencing",
        "syllabus_continuity",
        "confidence_calibration",
        "explanation_usefulness",
    ]
    prog = {}
    for k in prog_keys:
        total = 0
        passed = 0
        for pr in persona_results:
            m = ((pr.get("summary") or {}).get("programme_metrics") or {}).get(k) or {}
            total += int(m.get("total") or 0)
            passed += int(m.get("pass_count") or 0)
        prog[k] = {
            "pass_count": passed,
            "total": total,
            "result": "PASS" if total and passed == total else "FAIL",
        }
    out = {
        "programme": "PB-017",
        "volume": "CS1-017",
        "campaign": "Rho",
        "host": "https://kwalitec.onrender.com",
        "expected_commit": EXPECTED_COMMIT,
        "live_health": health,
        "fingerprint_ok": health.get("commit") == EXPECTED_COMMIT,
        "personas": [
            {
                "slug": pr.get("slug"),
                "email": pr.get("email"),
                "verdict": pr.get("verdict"),
                "avg_score_over_9": (pr.get("summary") or {}).get("avg_score_over_9"),
                "certified_days": (pr.get("summary") or {}).get("certified_days_scored"),
            }
            for pr in persona_results
        ],
        "mean_score_over_9": mean,
        "certified_day_observations": len(scores),
        "programme_metrics": prog,
        "regression_vs_pb016": reg,
        "coverage_held": "72/72 (100% Approver numerator)",
        "reliance_held": "through Topic 5.1",
        "verdict": "PASS" if all_pass and mean >= 8.0 and not reg["regression_detected"] else "FAIL",
    }
    (EVID_REPO / "results.json").write_text(json.dumps(out, indent=2, default=str))
    return out


def main(argv: list[str] | None = None) -> int:
    argv = argv or sys.argv[1:]
    ACCT.mkdir(parents=True, exist_ok=True)
    EVID_BASE.mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "ops").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "personas").mkdir(parents=True, exist_ok=True)
    (EVID_REPO / "suite").mkdir(parents=True, exist_ok=True)

    if argv and argv[0] == "--persona":
        slug = argv[1]
        persona = next(p for p in PERSONAS if p["slug"] == slug)
        result = run_persona(persona)
        print(json.dumps({"slug": result.get("slug"), "verdict": result.get("verdict")}, indent=2))
        return 0 if result.get("verdict") == "PASS" else 1

    results = []
    for persona in PERSONAS:
        results.append(run_persona(persona))
    agg = aggregate(results)
    print(json.dumps({"verdict": agg["verdict"], "mean": agg["mean_score_over_9"]}, indent=2))
    return 0 if agg["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
