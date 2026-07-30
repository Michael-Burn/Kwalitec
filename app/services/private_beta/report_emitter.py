"""Emit end-of-beta markdown report (PB-001)."""

# Markdown report templates intentionally use long table rows.
# ruff: noqa: E501, W291

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.services.private_beta.feedback_service import PrivateBetaFeedbackService
from app.services.private_beta.first_session_service import FirstSessionStudyService
from app.services.private_beta.metrics_service import (
    PrivateBetaMetricsService,
    PrivateBetaMetricsSnapshot,
)
from app.services.private_beta.observation_service import PrivateBetaObservationService
from app.version import APP_VERSION

DEFAULT_REPORT_PATH = Path(
    "knowledge/engineering/pb001_private_beta_validation/PB001_PRIVATE_BETA_REPORT.md"
)


class PrivateBetaReportEmitter:
    """Generate PB001_PRIVATE_BETA_REPORT.md from live evidence."""

    def __init__(
        self,
        *,
        metrics: PrivateBetaMetricsService | None = None,
        first_session: FirstSessionStudyService | None = None,
    ) -> None:
        self._metrics = metrics or PrivateBetaMetricsService()
        self._first_session = first_session or FirstSessionStudyService()

    def build_markdown(self, snapshot: PrivateBetaMetricsSnapshot | None = None) -> str:
        snap = snapshot or self._metrics.build()
        timings = self._first_session.for_cohort()
        feedback = PrivateBetaFeedbackService.recent(limit=20)
        observations = PrivateBetaObservationService.recent(limit=20)
        generated = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

        gate_lines = []
        for gate in snap.quality_gates:
            mark = "PASS" if gate.passed else "FAIL"
            gate_lines.append(
                f"| {gate.label} | {gate.actual}{gate.unit if gate.unit == '%' else ''} "
                f"| {gate.threshold}{gate.unit if gate.unit == '%' else ''} | {mark} |"
            )

        feedback_lines = []
        for item in feedback[:10]:
            feedback_lines.append(
                f"| #{item.id} | {item.category} | {item.severity} | "
                f"{(item.current_screen or '—')[:40]} | "
                f"{(item.message or '')[:80].replace('|', '/')} |"
            )
        if not feedback_lines:
            feedback_lines.append("| — | — | — | — | No feedback yet |")

        timing_lines = []
        for t in timings[:20]:
            timing_lines.append(
                f"| {t.email} | {t.minutes_to_first_mission} | "
                f"{t.minutes_to_first_session} | {t.minutes_to_first_tutor} | "
                f"{t.minutes_to_first_completion} | {t.drop_off_location or '—'} |"
            )
        if not timing_lines:
            timing_lines.append(
                "| — | — | — | — | — | No enrolled cohort timings yet |"
            )

        obs_stuck = sum(1 for o in observations if o.became_stuck)
        most = (
            "\n".join(
                f"- `{s.path}` — {s.visits} visits" for s in snap.most_visited_screens
            )
            or "- None yet"
        )
        least = (
            "\n".join(
                f"- `{s.path}` — {s.visits} visits" for s in snap.least_visited_screens
            )
            or "- None yet"
        )

        questions = self._answer_primary_questions(snap, timings, observations)

        return f"""# PB-001 — Private Beta Validation Report

**Programme:** PB-001 · Private Beta Validation · Version 1  
**Generated:** {generated}  
**Product version:** {APP_VERSION}  
**Scope:** Evidence only — no new educational architecture, AI systems, or curriculum reasoning  

---

## Summary

Private Beta Validation measures whether students can use Kwalitec to prepare
for professional examinations with minimal guidance. This report aggregates
cohort enrolment, study activity, Tutor / Knowledge Map usage, feedback,
first-session timing, founder observations, and quality gates.

**Cohort size:** {snap.total_beta_users}  
**Daily active users:** {snap.daily_active_users}  
**Weekly active users:** {snap.weekly_active_users}  

---

## FINAL DECISION

# {snap.go_recommendation}

**Evidence basis:** Quality gates passed = {snap.gates_passed}; enrolled users = {snap.total_beta_users}; critical bugs = {snap.critical_bugs}.

---

## Overall adoption

| Metric | Value |
|--------|-------|
| Total beta users | {snap.total_beta_users} |
| Daily active users | {snap.daily_active_users} |
| Weekly active users | {snap.weekly_active_users} |
| Study plans (% of cohort) | {snap.study_plan_completion_pct}% |
| First mission started (% of cohort) | {snap.first_mission_start_pct}% |
| Session completed (% of cohort) | {snap.session_completion_pct}% |
| Current in-progress sessions | {snap.current_study_sessions} |
| Average missions per user | {snap.average_missions_per_user} |
| Average session duration (min) | {snap.average_session_duration_minutes} |
| Average streak (approx.) | {snap.average_streak} |

---

## Primary questions

{questions}

---

## Quality gates

| Gate | Actual | Threshold | Result |
|------|--------|-----------|--------|
{chr(10).join(gate_lines)}

Hard stops (manual ops confirmation required outside this report):

- Zero data loss
- Zero certification errors
- Zero curriculum corruption

---

## Retention metrics

| Metric | Value |
|--------|-------|
| Daily return rate | {snap.daily_return_rate_pct}% |
| Weekly return rate | {snap.weekly_return_rate_pct}% |

---

## Mission completion

| Metric | Value |
|--------|-------|
| Missions started | {snap.missions_started} |
| Missions completed | {snap.missions_completed} |
| Mission completion % | {snap.mission_completion_pct}% |
| Mission abandonment % | {snap.mission_abandonment_pct}% |

---

## Tutor usage

| Metric | Value |
|--------|-------|
| Tutor activity events | {snap.tutor_activity} |
| Tutor adoption (% of cohort) | {snap.tutor_adoption_pct}% |

---

## Knowledge Map usage

| Metric | Value |
|--------|-------|
| Knowledge Map events | {snap.knowledge_map_usage} |
| Knowledge Map adoption (% of cohort) | {snap.knowledge_map_adoption_pct}% |
| Progress (Journey) opens | {snap.progress_usage} |

---

## Student feedback

| Metric | Value |
|--------|-------|
| Total feedback | {snap.feedback_total} |
| Critical | {snap.critical_bugs} |
| Major | {snap.major_bugs} |
| Feature requests | {snap.feature_requests} |

### Latest feedback

| ID | Category | Severity | Screen | Message |
|----|----------|----------|--------|---------|
{chr(10).join(feedback_lines)}

---

## Bug summary

Critical reports must stay below 5 for closed-beta success. Current critical count: **{snap.critical_bugs}**.

Classification ladder: Critical · Major · Minor · Enhancement · Question (auto-assigned on submit).

---

## First-session study

| Student | → Mission (min) | → Session (min) | → Tutor (min) | → Completion (min) | Drop-off |
|---------|-----------------|-----------------|---------------|--------------------|----------|
{chr(10).join(timing_lines)}

---

## Observation checklist

Observations recorded: **{snap.observations_total}** · Stuck: **{obs_stuck}**

Checklist dimensions: onboarding · where to click · Today's Mission · Progress · Tutor · Knowledge Map · stuck location.

---

## Screen analytics

### Most visited

{most}

### Least visited

{least}

---

## Performance metrics

Average session duration and streak are derived from existing study attempts and activity days — not new educational models.

| Metric | Value |
|--------|-------|
| Avg session duration (min) | {snap.average_session_duration_minutes} |
| Avg streak (approx.) | {snap.average_streak} |

---

## Recommendations

1. Enrol 10–20 students into the private beta cohort via the Founder Beta Dashboard.
2. Observe first-session timings until drop-off locations stabilize.
3. Triage every critical / major report within one business day.
4. Re-run this report after each cohort week before any public-beta claim.
5. Do not declare public beta until all quality gates pass with N ≥ 10.

---

## Commercial readiness assessment

This programme does **not** replace Version 1 production-ready
gates (P-002.1) or Product Board Stage 1 Go/No-Go. It answers only
whether private-beta students can successfully use Kwalitec with
minimal guidance.

| Claim | Status |
|-------|--------|
| Students understand Kwalitec | See Primary questions |
| Students trust recommendations | Feedback + incorrect-recommendation volume |
| Students complete study sessions | {snap.session_completion_pct}% of cohort |
| Students return | Weekly return {snap.weekly_return_rate_pct}% |
| Founder actionable feedback | {snap.feedback_total} reports / {snap.observations_total} obs |
| Product stability confirmed | Critical bugs {snap.critical_bugs} (gate < 5) |

---

## Go / No-Go recommendation

**{snap.go_recommendation}**

Generated from live metrics at {snap.as_of.isoformat()} UTC
(naive server clock stored as UTC wall time).
"""

    def _answer_primary_questions(
        self,
        snap: PrivateBetaMetricsSnapshot,
        timings,
        observations,
    ) -> str:
        if snap.total_beta_users == 0:
            return (
                "1. **Understand without training?** "
                "Insufficient evidence — cohort empty.\n"
                "2. **Complete a full study session?** "
                "Insufficient evidence — cohort empty.\n"
                "3. **Trust recommendations?** "
                "Insufficient evidence — cohort empty.\n"
                "4. **Return voluntarily?** "
                "Insufficient evidence — cohort empty.\n"
                "5. **Improve study consistency?** "
                "Insufficient evidence — cohort empty."
            )

        stuck = sum(1 for o in observations if o.became_stuck)
        understood = sum(
            1
            for o in observations
            if o.understood_todays_mission is True and o.knew_where_to_click is True
        )
        incorrect = sum(
            1
            for f in PrivateBetaFeedbackService.recent(limit=200)
            if f.category == "incorrect_recommendation"
        )
        completed_first = sum(1 for t in timings if t.reached_completion)
        returned = snap.weekly_return_rate_pct >= 70

        q1 = (
            f"Partial — {understood} observation(s) show clear orientation; "
            f"{stuck} report stuck moments."
            if observations
            else (
                f"Inferred from adoption: "
                f"{snap.first_mission_start_pct}% started a mission."
            )
        )
        q2 = (
            f"Yes for {snap.session_completion_pct}% of cohort "
            f"({completed_first} first-completions in timing study)."
        )
        q3 = (
            f"Watch — {incorrect} incorrect-recommendation report(s); "
            f"Tutor adoption {snap.tutor_adoption_pct}%."
        )
        q4 = (
            f"{'Yes' if returned else 'Not yet'} — weekly return "
            f"{snap.weekly_return_rate_pct}% (gate 70%)."
        )
        q5 = (
            f"Directional — average streak ≈ {snap.average_streak}; "
            f"daily return {snap.daily_return_rate_pct}%."
        )
        return (
            f"1. **Understand without training?** {q1}\n"
            f"2. **Complete a full study session?** {q2}\n"
            f"3. **Trust recommendations?** {q3}\n"
            f"4. **Return voluntarily?** {q4}\n"
            f"5. **Improve study consistency?** {q5}"
        )

    def write(
        self,
        path: Path | str | None = None,
        *,
        snapshot: PrivateBetaMetricsSnapshot | None = None,
    ) -> Path:
        """Write the report markdown to disk and return the path."""
        target = Path(path) if path is not None else DEFAULT_REPORT_PATH
        if not target.is_absolute():
            # Resolve relative to repository root (four parents up from this file
            # would be fragile); prefer CWD which is the app root in CLI/tests.
            target = Path.cwd() / target
        target.parent.mkdir(parents=True, exist_ok=True)
        markdown = self.build_markdown(snapshot)
        target.write_text(markdown, encoding="utf-8")
        return target
