"""Build session substance from a certified educational package (EA-006)."""

from __future__ import annotations

from app.application.educational_packages.models import (
    CertifiedEducationalPackage,
    KnowledgeCheck,
    WorkedExample,
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
    real = pack.worked_example
    has_real = real is not None and bool(real.steps)
    if has_real:
        assert real is not None  # narrow for type checkers
        example_title = real.title or "Worked example"
        example_prompt = (
            (real.attempt_before_reveal or "")
            + " Then continue to Knowledge Checks."
        ).strip()
        example_hints = tuple(
            f"{step.id}: {step.attempt_cue}"
            for step in real.steps
            if step.attempt_cue
        ) or (real.attempt_before_reveal,)
        example_answer_prompt = (
            "Which calculated quantity will you reuse in the checks?"
        )
    else:
        example_title = "Structure walkthrough: Family → η → link"
        example_prompt = (
            "Before Knowledge Checks: confirm your chain sketch "
            "and pause-point notes. "
            + (reading.reentry_line or "")
        ).strip()
        example_hints = tuple(
            f"{pp.get('id', 'PP')}: {pp.get('cue', '')}".strip()
            for pp in reading.pause_points
            if pp.get("cue")
        ) or (reading.attempt_before_reveal,)
        example_answer_prompt = (
            "Which pause-point note will you reuse in the checks?"
        )
    activities.append(
        EducationalActivitySpec(
            activity_id="act-example-1",
            stage=EducationalStage.WORKED_EXAMPLE,
            title=example_title,
            prompt=example_prompt,
            body=example_body,
            # Supporting line is folded into the structured body ("Before you
            # continue") so the template does not render it a second time.
            supporting_material="",
            hints=example_hints,
            answer_prompt=example_answer_prompt,
            objective_ids=objective_ids[:1] if objective_ids else (),
            syllabus_refs=syllabus,
            metadata=(
                ("activity_type", EducationalStage.WORKED_EXAMPLE.value),
                ("stage", EducationalStage.WORKED_EXAMPLE.value),
                ("stage_label", "Worked example"),
                ("package_id", pack.package_id),
                ("worked_example_kind", "numeric" if has_real else "scaffold"),
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
        if scoreable.response_type is PracticeResponseType.MCQ:
            answer_prompt = "Select your answer"
        elif scoreable.response_type is PracticeResponseType.NUMERIC:
            answer_prompt = "Your numeric answer"
        else:
            answer_prompt = "Your answer"
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
                answer_prompt=answer_prompt,
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
    """Assemble Worked Example body from structured package fields.

    When ``pack.worked_example`` has steps, emit a genuine numeric walkthrough.
    Otherwise emit the structure-walkthrough scaffold from mission / reading
    fields. Does **not** prepend the activity prompt/lead sentence — that
    belongs in the stage chrome, not as a duplicated H1/body dump.
    """
    real = pack.worked_example
    if real is not None and real.steps:
        return _real_worked_example_body(real)

    reading = pack.reading
    lines = [
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
            "",
            "Before you continue:",
            "• Keep the CMP closed for retrieval.",
            "• Move to Knowledge Checks when your sketch and pause notes are ready.",
        ]
    )
    return "\n".join(line for line in lines if line is not None)


def _real_worked_example_body(example: WorkedExample) -> str:
    """Assemble genuine numeric worked-example body for structured presentation."""
    lines: list[str] = []
    if example.problem_statement:
        lines.append(example.problem_statement)
        lines.append("")

    if example.given:
        lines.append("Given values:")
        for g in example.given:
            note = f" — {g.note}" if g.note else ""
            lines.append(f"• {g.symbol} = {g.value}{note}")
        lines.append("")

    lines.append("Attempt before reveal:")
    if example.attempt_before_reveal:
        lines.append(f"• {example.attempt_before_reveal}")
    for step in example.steps:
        if step.attempt_cue:
            lines.append(f"• {step.id}: {step.attempt_cue}")
    lines.append("")

    for index, step in enumerate(example.steps, start=1):
        # Keep header under parse_session_content_body's 60-char limit.
        lines.append(f"Worked solution — Step {index}:")
        if step.label:
            lines.append(step.label)
        if step.explanation:
            lines.append(step.explanation)
        if step.calculation:
            lines.append(step.calculation)
        if step.result:
            lines.append(f"Result: {step.result}")
        lines.append("")

    if example.final_answer:
        lines.append("Final answer:")
        lines.append(f"• {example.final_answer}")
        lines.append("")

    if example.common_pitfall:
        lines.append("Common pitfall:")
        lines.append(f"• {example.common_pitfall}")

    return "\n".join(line for line in lines if line is not None)


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
    if response is PracticeResponseType.MCQ:
        accepted = check.accepted_keywords
        answer_key = AnswerKey(
            accepted=accepted,
            correct_choice_id=check.correct_choice_id,
        )
        choices = tuple(
            (c.id, c.label, c.misconception_tag)
            if c.misconception_tag
            else (c.id, c.label)
            for c in check.choices
        )
    elif response is PracticeResponseType.NUMERIC:
        # Never fall back to ("explain", "link") — those can never match a
        # numeric response and would silently mark every answer wrong.
        accepted = check.accepted_keywords
        if not accepted:
            raise ValueError(
                f"numeric knowledge check {check.item_id or check.episode_id!r} "
                "requires non-empty accepted_keywords "
                "(authoring error: numeric items cannot use the "
                "short_structured explain/link fallback)"
            )
        answer_key = AnswerKey(
            accepted=accepted,
            numeric_tolerance=check.numeric_tolerance,
        )
        choices = ()
    else:
        answer_key = AnswerKey(
            accepted=check.accepted_keywords or ("explain", "link"),
        )
        choices = ()
    return ScoreablePracticeItem(
        item_id=check.item_id or check.episode_id,
        prompt=check.prompt,
        response_type=response,
        answer_key=answer_key,
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
        choices=choices,
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
