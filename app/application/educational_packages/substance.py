"""Build session substance from a certified educational package (EA-006)."""

from __future__ import annotations

from app.application.educational_packages.models import (
    CertifiedEducationalPackage,
    KnowledgeCheck,
)
from app.application.learning_session.educational_flow import (
    EducationalActivitySpec,
    EducationalSessionSubstance,
    EducationalStage,
    LearningObjectiveRef,
    next_transition_label,
)
from app.application.learning_session.scoreable_practice import (
    AnswerKey,
    MarkScheme,
    PracticeResponseType,
    ScoreablePracticeItem,
)


def substance_from_package(
    pack: CertifiedEducationalPackage,
    *,
    curriculum_identity: str,
    topic_id: str = "",
    objective_ids: tuple[str, ...] | list[str] | None = None,
) -> EducationalSessionSubstance:
    """Map a certified package onto the live Read → Example → Practice shell."""
    objectives = _objectives(pack, topic_id=topic_id, objective_ids=objective_ids)
    activities = _activities(pack, objectives=objectives)
    return EducationalSessionSubstance(
        topic_id=topic_id or pack.topic_code,
        topic_title=pack.topic_title,
        topic_code=pack.topic_code,
        curriculum_identity=curriculum_identity,
        learning_objectives=objectives,
        activities=activities,
        educational_rationale=pack.educational_rationale,
        task_descriptions=pack.task_descriptions,
        source="educational_package",
    )


def _objectives(
    pack: CertifiedEducationalPackage,
    *,
    topic_id: str,
    objective_ids: tuple[str, ...] | list[str] | None,
) -> tuple[LearningObjectiveRef, ...]:
    preferred = tuple(
        str(oid).strip() for oid in (objective_ids or ()) if str(oid).strip()
    )
    # Prefer Mission learning objective as the lead LO;
    # keep package criteria as supporting.
    lead_id = preferred[0] if preferred else f"{pack.package_id}:lo"
    refs = [
        LearningObjectiveRef(
            objective_id=lead_id,
            code=f"{pack.topic_code}.structure" if pack.topic_code else "",
            text=pack.learning_objective,
            topic_id=topic_id or pack.topic_code,
        )
    ]
    for index, criterion in enumerate(pack.success_criteria[:2], start=1):
        oid = (
            preferred[index]
            if index < len(preferred)
            else f"{pack.package_id}:sc-{index}"
        )
        refs.append(
            LearningObjectiveRef(
                objective_id=oid,
                code="",
                text=criterion,
                topic_id=topic_id or pack.topic_code,
            )
        )
    return tuple(refs)


def _activities(
    pack: CertifiedEducationalPackage,
    *,
    objectives: tuple[LearningObjectiveRef, ...],
) -> tuple[EducationalActivitySpec, ...]:
    objective_ids = tuple(o.objective_id for o in objectives)
    syllabus = tuple(
        ref
        for ref in (pack.topic_code, *(o.code for o in objectives if o.code))
        if ref
    )
    reading = pack.reading
    reading_body = _reading_body(pack)
    activities: list[EducationalActivitySpec] = [
        EducationalActivitySpec(
            activity_id="act-read-1",
            stage=EducationalStage.READ,
            title=f"Guided Reading: {pack.display_title or pack.topic_title}",
            prompt=reading.lead_line
            or (
                f"Open your CMP for Syllabus {pack.topic_code} "
                "and follow the Reading Guidance."
            ),
            body=reading_body,
            # exit_line is a legacy authoring dump that restates structured
            # fields and often includes internal CMP-authority commentary.
            # Structured body already carries open/stop/return; do not also
            # render exit_line as supporting_material (that caused duplication).
            supporting_material="",
            hints=tuple(reading.misconception_watch[:2])
            or ("Sketch Family / η / Link before deep reading.",),
            answer_prompt="What did you extract from the CMP setup?",
            objective_ids=objective_ids,
            syllabus_refs=syllabus,
            metadata=(
                ("activity_type", EducationalStage.READ.value),
                ("stage", EducationalStage.READ.value),
                ("stage_label", "Reading"),
                ("package_id", pack.package_id),
                ("episode", "guided_reading"),
            ),
        )
    ]

    example_body = _worked_example_body(pack)
    activities.append(
        EducationalActivitySpec(
            activity_id="act-example-1",
            stage=EducationalStage.WORKED_EXAMPLE,
            title="Structure walkthrough: Family → η → link",
            prompt=(
                "Before Knowledge Checks: confirm your chain sketch "
                "and pause-point notes. "
                + (reading.reentry_line or "")
            ).strip(),
            body=example_body,
            supporting_material=(
                "Keep the CMP closed for retrieval. "
                "Do not re-brief the Mission — move to Knowledge Checks when ready."
            ),
            hints=tuple(
                f"{pp.get('id', 'PP')}: {pp.get('cue', '')}".strip()
                for pp in reading.pause_points
                if pp.get("cue")
            )
            or (reading.attempt_before_reveal,),
            answer_prompt="Which pause-point note will you reuse in the checks?",
            objective_ids=objective_ids[:1] if objective_ids else (),
            syllabus_refs=syllabus,
            metadata=(
                ("activity_type", EducationalStage.WORKED_EXAMPLE.value),
                ("stage", EducationalStage.WORKED_EXAMPLE.value),
                ("stage_label", "Worked example"),
                ("package_id", pack.package_id),
            ),
        )
    )

    for index, check in enumerate(pack.knowledge_checks, start=1):
        scoreable = _scoreable_from_check(check, pack=pack)
        is_final = index == len(pack.knowledge_checks)
        stage_next = (
            next_transition_label(EducationalStage.PRACTICE)
            if is_final
            else "Continue"
        )
        activities.append(
            EducationalActivitySpec(
                activity_id=f"act-practice-{index}",
                stage=EducationalStage.PRACTICE,
                title=check.title or f"Knowledge Check {index}",
                prompt=check.prompt,
                body=check.body
                or "Closed-book retrieval aligned to today's Mission success criteria.",
                supporting_material=check.explanation,
                hints=check.hints,
                answer_prompt="Your answer",
                objective_ids=objective_ids[:1] if objective_ids else (),
                syllabus_refs=syllabus,
                scoreable=scoreable,
                metadata=(
                    ("activity_type", EducationalStage.PRACTICE.value),
                    ("stage", EducationalStage.PRACTICE.value),
                    ("stage_label", "Practice"),
                    ("next_action_label", stage_next),
                    ("scoreable", "1"),
                    ("response_type", scoreable.response_type.value),
                    ("item_id", scoreable.item_id),
                    ("package_id", pack.package_id),
                    ("episode", check.kind or "knowledge_check"),
                ),
            )
        )

    return _label_sequence(tuple(activities))


def _reading_body(pack: CertifiedEducationalPackage) -> str:
    """Assemble Guided Reading body from structured reading_guidance fields.

    Does **not** append ``exit_line``: that field restates the same open/stop
    /focus/misconception content and often includes internal authoring voice
    ("Kwalitec is the guide… substitute textbook"). lead_line is the activity
    prompt/title — omit it here to avoid repeating the purpose sentence.
    """
    reading = pack.reading
    is_revision = (pack.mode or "").strip().lower() == "revision"
    if is_revision:
        # PX-B-004: retrieval-framed checklist — presentation only; package
        # educational body / LO wording unchanged.
        lines = [
            f"Topic: {pack.topic_title} ({pack.topic_code})",
            f"Mission: {pack.display_title}",
            "",
            "Revision focus — retrieve, do not re-learn:",
            f"• Open: {reading.open_point}",
            f"• Stop: {reading.stop_condition}",
            "",
            "Retrieval questions (answer closed-book first):",
            *(f"• {q}" for q in reading.focus_questions),
            "",
            "Misconception watch:",
            *(f"• {m}" for m in reading.misconception_watch),
            "",
            "While you retrieve:",
            f"• {reading.annotation_task}",
            f"• {reading.attempt_before_reveal}",
            "",
            "Out of scope today:",
            *(f"• {x}" for x in reading.out_of_scope_today),
            "",
            "When you finish:",
            f"• {reading.return_cue}",
            "",
            "Next after Revision:",
            "• Close this retrieval sitting, then continue from Home when "
            "tomorrow's Mission is ready.",
        ]
        return "\n".join(line for line in lines if line is not None)

    lines = [
        f"Topic: {pack.topic_title} ({pack.topic_code})",
        f"Mission: {pack.display_title}",
        "",
        "Open the CMP:",
        f"• Open your CMP at {reading.open_point}",
        f"• Stop when: {reading.stop_condition}",
        "",
        "Focus questions:",
        *(f"• {q}" for q in reading.focus_questions),
        "",
        "Misconception watch:",
        *(f"• {m}" for m in reading.misconception_watch),
        "",
        "While you read:",
        f"• {reading.annotation_task}",
        f"• {reading.attempt_before_reveal}",
        "",
        "Out of scope today:",
        *(f"• {x}" for x in reading.out_of_scope_today),
        "",
        "When you finish:",
        f"• {reading.return_cue}",
    ]
    return "\n".join(line for line in lines if line is not None)


def _worked_example_body(pack: CertifiedEducationalPackage) -> str:
    reading = pack.reading
    lines = [
        "Re-entry after CMP reading",
        "",
        reading.reentry_line,
        "",
        "Confirm your structure sketch:",
        f"• Concept focus: {pack.concept_focus}",
        f"• Learning objective: {pack.learning_objective}",
        "",
        "Pause-point harvest:",
    ]
    for pp in reading.pause_points:
        lines.append(f"• {pp.get('id', 'PP')}: {pp.get('cue', '')}")
    lines.extend(
        [
            "",
            "Success criteria you will stress-test next:",
            *(f"• {c}" for c in pack.success_criteria),
        ]
    )
    return "\n".join(lines)


def _scoreable_from_check(
    check: KnowledgeCheck,
    *,
    pack: CertifiedEducationalPackage,
) -> ScoreablePracticeItem:
    response = PracticeResponseType.SHORT_STRUCTURED
    if (check.response_type or "").lower() in {"mcq", "multiple_choice"}:
        response = PracticeResponseType.MCQ
    elif (check.response_type or "").lower() in {"numeric", "number"}:
        response = PracticeResponseType.NUMERIC
    return ScoreablePracticeItem(
        item_id=check.item_id or check.episode_id,
        prompt=check.prompt,
        response_type=response,
        answer_key=AnswerKey(accepted=check.accepted_keywords or ("explain", "link")),
        mark_scheme=MarkScheme(
            points=check.success_criteria
            or ("Address the Mission success criteria for this check.",),
            max_marks=max(1, len(check.success_criteria) or 1),
        ),
        explanation=check.explanation,
        model_answer=check.model_answer,
        common_mistake=check.common_mistake,
        next_action="Continue to the next Knowledge Check or Reflection.",
        topic_id=pack.topic_code,
        topic_keywords=pack.topic_title_keywords,
        body=check.body,
        supporting_material=check.explanation,
        hints=check.hints,
        emit_structured=True,
    )


def _label_sequence(
    activities: tuple[EducationalActivitySpec, ...],
) -> tuple[EducationalActivitySpec, ...]:
    labelled: list[EducationalActivitySpec] = []
    for index, spec in enumerate(activities):
        is_last = index >= len(activities) - 1
        if is_last:
            next_label = next_transition_label(EducationalStage.PRACTICE)
        elif activities[index + 1].stage is EducationalStage.WORKED_EXAMPLE:
            next_label = next_transition_label(EducationalStage.READ)
        elif activities[index + 1].stage is EducationalStage.PRACTICE:
            if spec.stage is EducationalStage.WORKED_EXAMPLE:
                next_label = next_transition_label(EducationalStage.WORKED_EXAMPLE)
            else:
                next_label = "Continue"
        else:
            next_label = "Continue"
        # Preserve existing next_action_label for practice items when already set.
        existing = dict(spec.metadata)
        if "next_action_label" in existing and spec.stage is EducationalStage.PRACTICE:
            next_label = existing["next_action_label"]
        labelled.append(
            EducationalActivitySpec(
                activity_id=spec.activity_id,
                stage=spec.stage,
                title=spec.title,
                prompt=spec.prompt,
                body=spec.body,
                supporting_material=spec.supporting_material,
                hints=spec.hints,
                answer_prompt=spec.answer_prompt,
                requires_response=spec.requires_response,
                objective_ids=spec.objective_ids,
                syllabus_refs=spec.syllabus_refs,
                scoreable=spec.scoreable,
                metadata=tuple(
                    (k, v) for k, v in existing.items() if k != "next_action_label"
                )
                + (("next_action_label", next_label),),
            )
        )
    return tuple(labelled)
