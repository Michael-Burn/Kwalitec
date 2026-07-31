"""Educational quality certifier for Runtime C generated artefacts (EQ-001)."""

from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING, Any

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    MissionTemplateSnapshot,
)
from app.application.educational_quality.dto import (
    JourneyExplanationSnapshot,
    MissionQualityEnvelope,
    StudyPlanPacingSnapshot,
)
from app.domain.educational_quality import (
    EducationalQualityReport,
    QualityCheckResult,
    QualityIssue,
    build_journey_explanation,
    build_mission_completion_definition,
    build_mission_educational_rationale,
    build_mission_explanation,
    build_prerequisite_validation,
    contains_forbidden_jargon,
    project_study_plan_pacing,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    student_syllabus_code,
)

if TYPE_CHECKING:
    from app.application.educational_runtime_engine.dto import (
        MissionInstanceSnapshot,
        ProgressSnapshot,
    )


class EducationalQualityCertifier:
    """Verify derived artefacts and runtime instances against EQ-001 rules."""

    SERVICE_ID = "educational_quality_certifier"
    SERVICE_VERSION = "1.0.0"

    def certify_artefacts(
        self,
        artefacts: EducationalArtefactSnapshot,
    ) -> EducationalQualityReport:
        checks: list[QualityCheckResult] = []
        issues: list[QualityIssue] = []

        templates = artefacts.mission_templates
        plan = artefacts.study_plan_template
        topic_by_id = {t["topic_id"]: t for t in artefacts.topics}
        objective_by_id = {o["objective_id"]: o for o in artefacts.objectives}

        # EQ-M01..M05 — mission templates
        for template in templates:
            tid = template.template_id
            topic_ok = bool(template.topic_id and template.topic_code)
            checks.append(
                QualityCheckResult(
                    rule_id="EQ-M01",
                    passed=topic_ok,
                    message=(
                        "mission template bound to curriculum topic"
                        if topic_ok
                        else "mission template missing topic binding"
                    ),
                    artefact_id=tid,
                )
            )
            if not topic_ok:
                issues.append(
                    QualityIssue(
                        "EQ-M01",
                        "error",
                        "missing topic binding",
                        tid,
                    )
                )

            lo_ok = len(template.objective_ids) >= 1
            checks.append(
                QualityCheckResult(
                    rule_id="EQ-M02",
                    passed=lo_ok,
                    message=(
                        "mission template has learning objective references"
                        if lo_ok
                        else "mission template missing learning objectives"
                    ),
                    artefact_id=tid,
                )
            )
            if not lo_ok:
                issues.append(
                    QualityIssue(
                        "EQ-M02",
                        "error",
                        "missing learning objectives",
                        tid,
                    )
                )

            duration = int(getattr(template, "estimated_duration_minutes", 0) or 0)
            if duration <= 0:
                topic = topic_by_id.get(template.topic_id) or {}
                duration = int(topic.get("estimated_minutes") or 0)
            duration_ok = duration > 0
            checks.append(
                QualityCheckResult(
                    rule_id="EQ-M03",
                    passed=duration_ok,
                    message=(
                        f"estimated duration {duration} minutes"
                        if duration_ok
                        else "missing or non-positive estimated duration"
                    ),
                    artefact_id=tid,
                )
            )
            if not duration_ok:
                issues.append(
                    QualityIssue(
                        "EQ-M03",
                        "error",
                        "invalid estimated duration",
                        tid,
                    )
                )

            completion = str(
                getattr(template, "completion_definition", "") or ""
            ).strip()
            completion_ok = bool(completion)
            checks.append(
                QualityCheckResult(
                    rule_id="EQ-M04",
                    passed=completion_ok,
                    message=(
                        "completion definition present"
                        if completion_ok
                        else "completion definition missing"
                    ),
                    artefact_id=tid,
                )
            )
            if not completion_ok:
                issues.append(
                    QualityIssue(
                        "EQ-M04",
                        "error",
                        "missing completion definition",
                        tid,
                    )
                )

            rationale = str(
                getattr(template, "educational_rationale", "") or ""
            ).strip()
            rationale_ok = bool(rationale) and not contains_forbidden_jargon(
                rationale
            )
            checks.append(
                QualityCheckResult(
                    rule_id="EQ-M05",
                    passed=rationale_ok,
                    message=(
                        "educational rationale present and clean"
                        if rationale_ok
                        else (
                            "educational rationale missing "
                            "or contains forbidden jargon"
                        )
                    ),
                    artefact_id=tid,
                )
            )
            if not rationale_ok:
                issues.append(
                    QualityIssue(
                        "EQ-M05",
                        "error",
                        "invalid educational rationale",
                        tid,
                    )
                )

        # EQ-P01..P03 — study plan template
        topic_templates = (
            plan.topic_templates if plan is not None else ()
        )
        published_topic_ids = tuple(t["topic_id"] for t in artefacts.topics)
        template_topic_ids = tuple(
            str(t["topic_id"]) for t in topic_templates
        )
        coverage_ok = set(template_topic_ids) == set(published_topic_ids) and bool(
            template_topic_ids
        )
        checks.append(
            QualityCheckResult(
                rule_id="EQ-P01",
                passed=coverage_ok,
                message=(
                    "study plan covers all published topics"
                    if coverage_ok
                    else "study plan topic coverage incomplete"
                ),
                artefact_id=artefacts.curriculum_identity,
            )
        )
        if not coverage_ok:
            issues.append(
                QualityIssue(
                    "EQ-P01",
                    "error",
                    "incomplete topic coverage",
                    artefacts.curriculum_identity,
                )
            )

        order_ok = self._prerequisite_order_ok(topic_templates)
        checks.append(
            QualityCheckResult(
                rule_id="EQ-P02",
                passed=order_ok,
                message=(
                    "study plan respects prerequisite integrity"
                    if order_ok
                    else "study plan violates prerequisite order"
                ),
                artefact_id=artefacts.curriculum_identity,
            )
        )
        if not order_ok:
            issues.append(
                QualityIssue(
                    "EQ-P02",
                    "error",
                    "prerequisite integrity failure",
                    artefacts.curriculum_identity,
                )
            )

        minutes_ok = all(
            int(t.get("recommended_minutes") or 0) > 0 for t in topic_templates
        ) and bool(topic_templates)
        checks.append(
            QualityCheckResult(
                rule_id="EQ-P03",
                passed=minutes_ok,
                message=(
                    "all recommended_minutes are positive"
                    if minutes_ok
                    else "non-positive recommended_minutes present"
                ),
                artefact_id=artefacts.curriculum_identity,
            )
        )
        if not minutes_ok:
            issues.append(
                QualityIssue(
                    "EQ-P03",
                    "error",
                    "invalid recommended minutes",
                    artefacts.curriculum_identity,
                )
            )

        # Objective mapping integrity for templates
        for template in templates:
            unknown = [
                oid
                for oid in template.objective_ids
                if oid not in objective_by_id
            ]
            mapping_ok = not unknown
            checks.append(
                QualityCheckResult(
                    rule_id="EQ-M02b",
                    passed=mapping_ok,
                    message=(
                        "objective ids resolve to published objectives"
                        if mapping_ok
                        else f"unknown objective ids: {unknown}"
                    ),
                    artefact_id=template.template_id,
                )
            )
            if not mapping_ok:
                issues.append(
                    QualityIssue(
                        "EQ-M02b",
                        "error",
                        f"unknown objectives {unknown}",
                        template.template_id,
                    )
                )

        passed = all(check.passed for check in checks)
        return EducationalQualityReport(
            curriculum_identity=artefacts.curriculum_identity,
            passed=passed,
            checks=tuple(checks),
            issues=tuple(issues),
        )

    def certify_mission(
        self,
        mission: MissionInstanceSnapshot,
        *,
        artefacts: EducationalArtefactSnapshot | None = None,
    ) -> EducationalQualityReport:
        checks: list[QualityCheckResult] = []
        issues: list[QualityIssue] = []
        envelope = mission.quality
        mid = mission.mission_instance_id

        envelope_ok = envelope is not None
        checks.append(
            QualityCheckResult(
                rule_id="EQ-M06",
                passed=envelope_ok,
                message=(
                    "mission instance carries quality envelope"
                    if envelope_ok
                    else "mission instance missing quality envelope"
                ),
                artefact_id=mid,
            )
        )
        if not envelope_ok:
            issues.append(
                QualityIssue(
                    "EQ-M06",
                    "error",
                    "missing quality envelope",
                    mid,
                )
            )
            return EducationalQualityReport(
                curriculum_identity=mission.curriculum_identity,
                passed=False,
                checks=tuple(checks),
                issues=tuple(issues),
            )

        prereq_ok = bool(envelope.prerequisite_validation.get("all_satisfied"))
        checks.append(
            QualityCheckResult(
                rule_id="EQ-M07",
                passed=prereq_ok,
                message=(
                    "prerequisites satisfied for mission topic"
                    if prereq_ok
                    else "mission generated with unsatisfied prerequisites"
                ),
                artefact_id=mid,
            )
        )
        if not prereq_ok:
            issues.append(
                QualityIssue(
                    "EQ-M07",
                    "error",
                    "unsatisfied prerequisites",
                    mid,
                )
            )

        explanation = envelope.explanation or {}
        schema_ok = bool(explanation.get("explanation_schema_complete"))
        for key in (
            "judgement",
            "why_this_mission",
            "supporting_evidence",
            "confidence_level",
            "suggested_next_action",
            "plan_drivers",
            "explanation_schema_version",
        ):
            value = explanation.get(key)
            if value is None or (
                isinstance(value, str | list | tuple) and len(value) == 0
            ):
                schema_ok = False
                break
        checks.append(
            QualityCheckResult(
                rule_id="EQ-X01",
                passed=schema_ok,
                message=(
                    "mission explanation schema complete"
                    if schema_ok
                    else "mission explanation schema incomplete"
                ),
                artefact_id=mid,
            )
        )
        if not schema_ok:
            issues.append(
                QualityIssue(
                    "EQ-X01",
                    "error",
                    "incomplete explanation schema",
                    mid,
                )
            )

        evidence = explanation.get("supporting_evidence") or []
        evidence_text = " ".join(str(item) for item in evidence)
        evidence_ok = bool(mission.topic_code) and (
            "objective" in evidence_text.lower()
            or bool(envelope.objective_ids)
        )
        checks.append(
            QualityCheckResult(
                rule_id="EQ-X02",
                passed=evidence_ok,
                message=(
                    "supporting evidence cites topic and objectives"
                    if evidence_ok
                    else "supporting evidence missing topic/objective citations"
                ),
                artefact_id=mid,
            )
        )
        if not evidence_ok:
            issues.append(
                QualityIssue(
                    "EQ-X02",
                    "error",
                    "weak supporting evidence",
                    mid,
                )
            )

        confidence = str(explanation.get("confidence_level") or "")
        confidence_ok = (
            "High" in confidence
            if prereq_ok
            else ("Low" in confidence or "Suggested" in confidence)
        )
        checks.append(
            QualityCheckResult(
                rule_id="EQ-X03",
                passed=confidence_ok,
                message=(
                    "confidence matches prerequisite satisfaction"
                    if confidence_ok
                    else "confidence does not match prerequisite state"
                ),
                artefact_id=mid,
            )
        )
        if not confidence_ok:
            issues.append(
                QualityIssue(
                    "EQ-X03",
                    "error",
                    "confidence mismatch",
                    mid,
                )
            )

        jargon_fields = [
            envelope.educational_rationale,
            explanation.get("why_this_mission") or "",
            explanation.get("judgement") or "",
        ]
        jargon_ok = not any(
            contains_forbidden_jargon(str(field)) for field in jargon_fields
        )
        checks.append(
            QualityCheckResult(
                rule_id="EQ-X05",
                passed=jargon_ok,
                message=(
                    "no forbidden jargon in student-facing rationale"
                    if jargon_ok
                    else "forbidden jargon detected"
                ),
                artefact_id=mid,
            )
        )
        if not jargon_ok:
            issues.append(
                QualityIssue(
                    "EQ-X05",
                    "error",
                    "forbidden jargon",
                    mid,
                )
            )

        if artefacts is not None:
            template = next(
                (
                    t
                    for t in artefacts.mission_templates
                    if t.template_id == mission.template_id
                ),
                None,
            )
            if template is not None:
                for rule_id, ok, msg in (
                    (
                        "EQ-M01",
                        bool(mission.topic_id and mission.topic_code),
                        "instance topic binding",
                    ),
                    (
                        "EQ-M02",
                        len(envelope.objective_ids) >= 1,
                        "instance learning objectives",
                    ),
                    (
                        "EQ-M03",
                        envelope.estimated_duration_minutes > 0,
                        "instance duration",
                    ),
                    (
                        "EQ-M04",
                        bool(envelope.completion_definition.strip()),
                        "instance completion definition",
                    ),
                    (
                        "EQ-M05",
                        bool(envelope.educational_rationale.strip()),
                        "instance educational rationale",
                    ),
                ):
                    checks.append(
                        QualityCheckResult(
                            rule_id=rule_id,
                            passed=ok,
                            message=msg if ok else f"failed {msg}",
                            artefact_id=mid,
                        )
                    )
                    if not ok:
                        issues.append(
                            QualityIssue(rule_id, "error", msg, mid)
                        )

        passed = all(check.passed for check in checks)
        return EducationalQualityReport(
            curriculum_identity=mission.curriculum_identity,
            passed=passed,
            checks=tuple(checks),
            issues=tuple(issues),
        )

    def certify_journey_explanation(
        self,
        explanation: JourneyExplanationSnapshot,
        *,
        curriculum_identity: str,
    ) -> EducationalQualityReport:
        checks: list[QualityCheckResult] = []
        issues: list[QualityIssue] = []

        present = bool(
            explanation.why_today
            and explanation.why_previous_complete
            and explanation.unlocks_next
        )
        checks.append(
            QualityCheckResult(
                rule_id="EQ-J01",
                passed=present,
                message=(
                    "journey explanation present"
                    if present
                    else "journey explanation incomplete"
                ),
            )
        )
        if not present:
            issues.append(
                QualityIssue("EQ-J01", "error", "missing journey explanation")
            )

        why_today_ok = bool(explanation.why_today.strip())
        checks.append(
            QualityCheckResult(
                rule_id="EQ-J02",
                passed=why_today_ok,
                message=(
                    "why_today present"
                    if why_today_ok
                    else "why_today missing"
                ),
            )
        )
        if not why_today_ok:
            issues.append(QualityIssue("EQ-J02", "error", "why_today missing"))

        previous_ok = bool(explanation.why_previous_complete.strip())
        checks.append(
            QualityCheckResult(
                rule_id="EQ-J03",
                passed=previous_ok,
                message=(
                    "why_previous_complete present"
                    if previous_ok
                    else "why_previous_complete missing"
                ),
            )
        )
        if not previous_ok:
            issues.append(
                QualityIssue(
                    "EQ-J03",
                    "error",
                    "why_previous_complete missing",
                )
            )

        unlocks_ok = bool(explanation.unlocks_next.strip())
        checks.append(
            QualityCheckResult(
                rule_id="EQ-J04",
                passed=unlocks_ok,
                message=(
                    "unlocks_next present" if unlocks_ok else "unlocks_next missing"
                ),
            )
        )
        if not unlocks_ok:
            issues.append(
                QualityIssue("EQ-J04", "error", "unlocks_next missing")
            )

        schema_ok = bool(explanation.explanation_schema_complete)
        checks.append(
            QualityCheckResult(
                rule_id="EQ-X04",
                passed=schema_ok and present,
                message=(
                    "journey answers the three mandatory questions"
                    if schema_ok and present
                    else "journey explanation schema incomplete"
                ),
            )
        )
        if not (schema_ok and present):
            issues.append(
                QualityIssue("EQ-X04", "error", "journey schema incomplete")
            )

        passed = all(check.passed for check in checks)
        return EducationalQualityReport(
            curriculum_identity=curriculum_identity,
            passed=passed,
            checks=tuple(checks),
            issues=tuple(issues),
        )

    def certify_pacing(
        self,
        pacing: StudyPlanPacingSnapshot,
        *,
        curriculum_identity: str,
        exam_date_required: bool,
    ) -> EducationalQualityReport:
        checks: list[QualityCheckResult] = []
        issues: list[QualityIssue] = []

        aware_ok = pacing.exam_date_aware if exam_date_required else True
        checks.append(
            QualityCheckResult(
                rule_id="EQ-P04",
                passed=aware_ok,
                message=(
                    "pacing is exam-date aware"
                    if aware_ok
                    else "pacing missing exam-date awareness"
                ),
            )
        )
        if not aware_ok:
            issues.append(
                QualityIssue("EQ-P04", "error", "exam-date awareness missing")
            )

        revision_ok = pacing.revision_minutes > 0
        checks.append(
            QualityCheckResult(
                rule_id="EQ-P05",
                passed=revision_ok,
                message=(
                    f"revision allocation {pacing.revision_minutes} minutes"
                    if revision_ok
                    else "revision allocation missing"
                ),
            )
        )
        if not revision_ok:
            issues.append(
                QualityIssue("EQ-P05", "error", "revision allocation missing")
            )

        honest_ok = True
        if pacing.feasible is False:
            honest_ok = (
                pacing.shortfall_minutes is not None
                and pacing.shortfall_minutes > 0
            )
        checks.append(
            QualityCheckResult(
                rule_id="EQ-P06",
                passed=honest_ok,
                message=(
                    "infeasible pacing reported honestly"
                    if honest_ok
                    else "infeasible pacing not reported honestly"
                ),
            )
        )
        if not honest_ok:
            issues.append(
                QualityIssue("EQ-P06", "error", "dishonest pacing compression")
            )

        passed = all(check.passed for check in checks)
        return EducationalQualityReport(
            curriculum_identity=curriculum_identity,
            passed=passed,
            checks=tuple(checks),
            issues=tuple(issues),
        )

    def build_mission_quality_envelope(
        self,
        *,
        template: MissionTemplateSnapshot,
        artefacts: EducationalArtefactSnapshot,
        completed_topic_ids: tuple[str, ...] | set[str],
        objective_ids: tuple[str, ...] | list[str] | None = None,
        estimated_duration_minutes: int | None = None,
    ) -> MissionQualityEnvelope:
        topic = next(
            (t for t in artefacts.topics if t["topic_id"] == template.topic_id),
            {},
        )
        selected_ids = tuple(
            str(oid).strip()
            for oid in (
                objective_ids
                if objective_ids is not None
                else template.objective_ids
            )
            if str(oid).strip()
        )
        if not selected_ids:
            selected_ids = tuple(template.objective_ids)
        selected_set = set(selected_ids)
        objectives = [
            o
            for o in artefacts.objectives
            if o["objective_id"] in selected_set
        ]
        # Preserve sitting order when a session-sized subset is supplied.
        by_id = {o["objective_id"]: o for o in objectives}
        objectives = [by_id[oid] for oid in selected_ids if oid in by_id]
        topic_title = str(topic.get("title") or template.topic_code)
        human_topic_code = student_syllabus_code(
            code=str(template.topic_code or topic.get("code") or ""),
            title=topic_title,
            number=str(topic.get("number") or ""),
        ) or str(template.topic_code or "")
        objective_codes = tuple(
            student_syllabus_code(
                code=str(o.get("code") or ""),
                title=str(o.get("text") or o.get("title") or ""),
                number=str(o.get("number") or ""),
            )
            or str(o.get("number") or o.get("text") or "")
            for o in objectives
        )
        objective_codes = tuple(c for c in objective_codes if c)
        prerequisite_ids = tuple(
            getattr(template, "prerequisite_ids", ())
            or tuple(topic.get("prerequisite_ids") or ())
        )
        if estimated_duration_minutes is not None and int(
            estimated_duration_minutes
        ) > 0:
            duration = int(estimated_duration_minutes)
        else:
            duration = int(
                getattr(template, "estimated_duration_minutes", 0)
                or topic.get("estimated_minutes")
                or 0
            )
        completion = str(
            getattr(template, "completion_definition", "")
            or build_mission_completion_definition(topic_code=human_topic_code)
        )
        # Always rebuild rationale with human codes (MISSION-002) — template may
        # still carry node-id codes from older package projections.
        rationale = build_mission_educational_rationale(
            topic_code=human_topic_code,
            topic_title=topic_title,
            objective_codes=objective_codes,
            prerequisite_ids=prerequisite_ids,
        )
        validation = build_prerequisite_validation(
            required_ids=prerequisite_ids,
            completed_topic_ids=completed_topic_ids,
        )
        explanation = build_mission_explanation(
            topic_id=template.topic_id,
            topic_code=human_topic_code,
            topic_title=topic_title,
            objective_ids=selected_ids,
            objective_codes=objective_codes,
            estimated_duration_minutes=duration,
            educational_rationale=rationale,
            prerequisites_satisfied=bool(validation["all_satisfied"]),
        )
        return MissionQualityEnvelope(
            topic_id=template.topic_id,
            topic_code=human_topic_code,
            objective_ids=selected_ids,
            estimated_duration_minutes=duration,
            completion_definition=completion,
            educational_rationale=rationale,
            prerequisite_validation=validation,
            explanation=explanation,
        )

    def build_journey_explanation_snapshot(
        self,
        *,
        artefacts: EducationalArtefactSnapshot,
        progress: ProgressSnapshot,
        previous_topic_id: str | None,
    ) -> JourneyExplanationSnapshot:
        topic_by_id = {t["topic_id"]: t for t in artefacts.topics}
        current = topic_by_id.get(progress.current_topic_id or "")
        previous = topic_by_id.get(previous_topic_id or "")
        next_topic_id = None
        if progress.current_topic_id and not progress.syllabus_complete:
            incomplete = list(progress.incomplete_topic_ids)
            if progress.current_topic_id in incomplete:
                idx = incomplete.index(progress.current_topic_id)
                if idx + 1 < len(incomplete):
                    next_topic_id = incomplete[idx + 1]
            elif incomplete:
                next_topic_id = incomplete[0]
        nxt = topic_by_id.get(next_topic_id or "")
        payload = build_journey_explanation(
            current_topic_id=progress.current_topic_id,
            current_topic_code=student_syllabus_code(
                code=str(current.get("code") or "") if current else "",
                title=str(current.get("title") or "") if current else "",
                number=str(current.get("number") or "") if current else "",
            ),
            current_topic_title=str(current.get("title")) if current else None,
            previous_topic_id=previous_topic_id,
            previous_topic_code=student_syllabus_code(
                code=str(previous.get("code") or "") if previous else "",
                title=str(previous.get("title") or "") if previous else "",
                number=str(previous.get("number") or "") if previous else "",
            ),
            next_topic_id=next_topic_id,
            next_topic_code=student_syllabus_code(
                code=str(nxt.get("code") or "") if nxt else "",
                title=str(nxt.get("title") or "") if nxt else "",
                number=str(nxt.get("number") or "") if nxt else "",
            ),
            next_topic_title=str(nxt.get("title")) if nxt else None,
            coverage_ratio=progress.coverage_ratio,
            journey_stage=progress.journey_stage,
            syllabus_complete=progress.syllabus_complete,
            completed_count=len(progress.completed_topic_ids),
            total_count=len(progress.topic_ids),
        )
        return JourneyExplanationSnapshot(
            why_today=str(payload["why_today"]),
            why_previous_complete=str(payload["why_previous_complete"]),
            unlocks_next=str(payload["unlocks_next"]),
            supporting_evidence=tuple(payload["supporting_evidence"]),
            explanation_schema_version=str(
                payload["explanation_schema_version"]
            ),
            explanation_level=str(payload["explanation_level"]),
            explanation_schema_complete=bool(
                payload["explanation_schema_complete"]
            ),
            current_topic_id=progress.current_topic_id,
            previous_topic_id=previous_topic_id,
            next_topic_id=next_topic_id,
        )

    def build_pacing_snapshot(
        self,
        *,
        artefacts: EducationalArtefactSnapshot,
        exam_date: date | None,
        as_of: date | None = None,
        weekday_minutes: int = 90,
        weekend_minutes: int = 120,
    ) -> StudyPlanPacingSnapshot:
        templates = (
            artefacts.study_plan_template.topic_templates
            if artefacts.study_plan_template
            else ()
        )
        projection = project_study_plan_pacing(
            topic_templates=templates,
            exam_date=exam_date,
            as_of=as_of or date.today(),
            weekday_minutes=weekday_minutes,
            weekend_minutes=weekend_minutes,
        )
        return StudyPlanPacingSnapshot(
            exam_date_aware=bool(projection["exam_date_aware"]),
            first_pass_minutes=int(projection["first_pass_minutes"]),
            revision_minutes=int(projection["revision_minutes"]),
            total_required_minutes=int(projection["total_required_minutes"]),
            feasible=projection["feasible"],
            shortfall_minutes=projection["shortfall_minutes"],
            projection=projection,
        )

    @staticmethod
    def _prerequisite_order_ok(topic_templates: tuple[dict[str, Any], ...]) -> bool:
        seen: set[str] = set()
        for template in topic_templates:
            topic_id = str(template.get("topic_id") or "")
            prereqs = tuple(template.get("prerequisite_ids") or ())
            for prereq in prereqs:
                if prereq not in seen:
                    return False
            if topic_id:
                seen.add(topic_id)
        return bool(topic_templates)
