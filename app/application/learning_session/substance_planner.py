"""Build package-derived educational substance for a Study Session (LXP-004A).

Resolves published curriculum artefacts into a continuous Read → Worked Example
→ Practice activity sequence with Learning Objectives. Never invents mastery
scores, Twin updates, or evidence grades.
"""

from __future__ import annotations

from typing import Any

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
    MissionTemplateSnapshot,
)
from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.application.learning_session.educational_flow import (
    EducationalActivitySpec,
    EducationalSessionSubstance,
    EducationalStage,
    LearningObjectiveRef,
    next_transition_label,
)
from app.application.learning_session.scoreable_practice import (
    PracticeResponseType,
    ScoreablePracticeItem,
)
from app.application.learning_session.scoreable_seed import items_for_topic
from app.domain.educational_runtime_engine.student_facing_identity import (
    format_learning_objective_label,
    student_syllabus_code,
)


class EducationalSubstancePlanner:
    """Derive session educational substance from published package artefacts."""

    def __init__(
        self,
        *,
        foundation: EducationalEngineFoundationService | None = None,
    ) -> None:
        self._foundation = foundation or EducationalEngineFoundationService()

    def plan_for_topic(
        self,
        *,
        curriculum_identity: str,
        topic_id: str,
        topic_title: str = "",
        task_descriptions: tuple[str, ...] | list[str] | None = None,
        educational_rationale: str = "",
        objective_ids: tuple[str, ...] | list[str] | None = None,
    ) -> EducationalSessionSubstance | None:
        """Resolve package substance for a mission topic.

        Returns None when the published package cannot be resolved — callers
        should fall back honestly rather than inventing \"Core methods\".
        """
        snapshot = self._resolve_snapshot(curriculum_identity)
        if snapshot is None:
            return self._plan_from_mission_facts(
                curriculum_identity=curriculum_identity,
                topic_id=topic_id,
                topic_title=topic_title,
                task_descriptions=tuple(task_descriptions or ()),
                educational_rationale=educational_rationale,
                objective_ids=tuple(objective_ids or ()),
            )

        topic = self._topic(snapshot, topic_id)
        if topic is None and not topic_title:
            return None

        title = (
            str((topic or {}).get("title") or topic_title or "").strip()
            or "Today's topic"
        )
        code = student_syllabus_code(
            code=str((topic or {}).get("code") or ""),
            title=title,
            number=str((topic or {}).get("number") or ""),
        ) or str((topic or {}).get("number") or (topic or {}).get("code") or "")

        objectives = self._objectives_for_topic(
            snapshot,
            topic_id=topic_id,
            preferred_ids=tuple(objective_ids or ()),
            topic=topic,
        )
        template = self._mission_template(snapshot, topic_id)
        tasks = tuple(task_descriptions or ())
        if not tasks and template is not None:
            tasks = tuple(template.task_descriptions)
        rationale = (educational_rationale or "").strip()
        if not rationale and template is not None:
            rationale = (template.educational_rationale or "").strip()

        activities = self._build_activities(
            topic_title=title,
            topic_code=code,
            objectives=objectives,
            task_descriptions=tasks,
            educational_rationale=rationale,
        )
        return EducationalSessionSubstance(
            topic_id=topic_id or str((topic or {}).get("topic_id") or ""),
            topic_title=title,
            topic_code=code,
            curriculum_identity=snapshot.curriculum_identity,
            learning_objectives=objectives,
            activities=activities,
            educational_rationale=rationale,
            task_descriptions=tasks,
            source="package",
        )

    def _plan_from_mission_facts(
        self,
        *,
        curriculum_identity: str,
        topic_id: str,
        topic_title: str,
        task_descriptions: tuple[str, ...],
        educational_rationale: str,
        objective_ids: tuple[str, ...],
    ) -> EducationalSessionSubstance | None:
        """Honest fallback when package store is unavailable but mission facts exist."""
        title = (topic_title or "").strip()
        if not title and not task_descriptions:
            return None
        title = title or "Today's topic"
        texts = list(task_descriptions) if task_descriptions else [title]
        ids = list(objective_ids) if objective_ids else []
        while len(ids) < len(texts):
            ids.append(f"obj-{len(ids) + 1}")
        objectives = tuple(
            LearningObjectiveRef(
                objective_id=oid or f"obj-{index + 1}",
                code="",
                text=(task or title).strip() or title,
                topic_id=topic_id,
            )
            for index, (oid, task) in enumerate(zip(ids, texts, strict=False))
        )
        if not objectives:
            objectives = (
                LearningObjectiveRef(
                    objective_id=f"obj-{topic_id or 'topic'}",
                    code="",
                    text=f"Understand the core ideas of {title}",
                    topic_id=topic_id,
                ),
            )
        activities = self._build_activities(
            topic_title=title,
            topic_code="",
            objectives=objectives,
            task_descriptions=task_descriptions,
            educational_rationale=educational_rationale,
        )
        return EducationalSessionSubstance(
            topic_id=topic_id,
            topic_title=title,
            topic_code="",
            curriculum_identity=curriculum_identity,
            learning_objectives=objectives,
            activities=activities,
            educational_rationale=educational_rationale,
            task_descriptions=task_descriptions,
            source="mission_facts",
        )

    def _resolve_snapshot(
        self, curriculum_identity: str
    ) -> EducationalArtefactSnapshot | None:
        identity = (curriculum_identity or "").strip()
        if not identity:
            return None
        subject = identity
        version = ""
        if ":" in identity:
            subject, version = identity.split(":", 1)
            subject, version = subject.strip(), version.strip()
        if subject and version:
            snap = self._foundation.derive_version(subject, version)
            if snap is not None:
                return snap
        if subject:
            return self._foundation.derive_active(subject)
        return None

    @staticmethod
    def _topic(
        snapshot: EducationalArtefactSnapshot, topic_id: str
    ) -> dict[str, Any] | None:
        tid = (topic_id or "").strip()
        for topic in snapshot.topics:
            if str(topic.get("topic_id") or "").strip() == tid:
                return dict(topic)
        return None

    @staticmethod
    def _mission_template(
        snapshot: EducationalArtefactSnapshot, topic_id: str
    ) -> MissionTemplateSnapshot | None:
        tid = (topic_id or "").strip()
        for template in snapshot.mission_templates:
            if template.topic_id == tid:
                return template
        return None

    @staticmethod
    def _objectives_for_topic(
        snapshot: EducationalArtefactSnapshot,
        *,
        topic_id: str,
        preferred_ids: tuple[str, ...],
        topic: dict[str, Any] | None,
    ) -> tuple[LearningObjectiveRef, ...]:
        by_id = {
            str(obj.get("objective_id") or ""): obj for obj in snapshot.objectives
        }
        ordered_ids: list[str] = []
        if preferred_ids:
            ordered_ids.extend(oid for oid in preferred_ids if oid in by_id)
        if not ordered_ids and topic is not None:
            ordered_ids.extend(
                str(oid)
                for oid in (topic.get("learning_objective_ids") or ())
                if str(oid) in by_id
            )
        if not ordered_ids:
            ordered_ids.extend(
                str(obj.get("objective_id") or "")
                for obj in snapshot.objectives
                if str(obj.get("topic_id") or "") == topic_id
            )
        refs: list[LearningObjectiveRef] = []
        seen: set[str] = set()
        for oid in ordered_ids:
            if not oid or oid in seen:
                continue
            seen.add(oid)
            raw = by_id.get(oid) or {}
            text = str(raw.get("text") or "").strip()
            if not text:
                continue
            code = student_syllabus_code(
                code=str(raw.get("code") or ""),
                title=text,
                number=str(raw.get("number") or ""),
            ) or str(raw.get("number") or raw.get("code") or "")
            refs.append(
                LearningObjectiveRef(
                    objective_id=oid,
                    code=code,
                    text=text,
                    topic_id=str(raw.get("topic_id") or topic_id),
                )
            )
        return tuple(refs)

    def _build_activities(
        self,
        *,
        topic_title: str,
        topic_code: str,
        objectives: tuple[LearningObjectiveRef, ...],
        task_descriptions: tuple[str, ...],
        educational_rationale: str,
    ) -> tuple[EducationalActivitySpec, ...]:
        lead = objectives[0] if objectives else None
        lead_text = lead.text if lead else f"the core ideas of {topic_title}"
        syllabus = tuple(
            ref
            for ref in (
                topic_code,
                *(obj.code for obj in objectives if obj.code),
            )
            if ref
        )
        objective_ids = tuple(obj.objective_id for obj in objectives)

        reading_lines = [
            f"Topic: {topic_title}" + (f" ({topic_code})" if topic_code else ""),
        ]
        if objectives:
            reading_lines.append("Learning objectives for this session:")
            for obj in objectives:
                label = format_learning_objective_label(
                    code=obj.code, text=obj.text
                )
                reading_lines.append(f"• {label}")
        elif task_descriptions:
            reading_lines.append("Today's study focus:")
            for task in task_descriptions:
                reading_lines.append(f"• {task}")
        if educational_rationale:
            reading_lines.append("")
            reading_lines.append(educational_rationale)

        activities: list[EducationalActivitySpec] = [
            EducationalActivitySpec(
                activity_id="act-read-1",
                stage=EducationalStage.READ,
                title=f"Read: {topic_title}",
                prompt=(
                    f"Read the material for {topic_title}. "
                    "Note one idea you want to remember."
                ),
                body="\n".join(reading_lines),
                supporting_material=(
                    f"Focus on how the learning objectives connect to {topic_title}."
                ),
                hints=("Underline the objective that feels least clear.",),
                answer_prompt="What stood out from the reading?",
                objective_ids=objective_ids,
                syllabus_refs=syllabus,
                metadata=(
                    ("activity_type", EducationalStage.READ.value),
                    ("stage", EducationalStage.READ.value),
                    ("stage_label", "Reading"),
                ),
            )
        ]

        # Worked example when we have an LO or rationale to walk through.
        if lead is not None or educational_rationale or len(task_descriptions) > 1:
            example_body_parts = [
                f"Worked example for {topic_title}",
                "",
                f"Objective in focus: {lead_text}",
            ]
            if educational_rationale:
                example_body_parts.extend(["", educational_rationale])
            if len(task_descriptions) > 1:
                example_body_parts.extend(
                    ["", "Mission walkthrough:", *(f"• {t}" for t in task_descriptions)]
                )
            example_body_parts.extend(
                [
                    "",
                    "Method steps:",
                    "1. Restate the objective in your own words.",
                    "2. Identify the syllabus idea the objective depends on.",
                    f"3. Apply that idea to one concrete case in {topic_title}.",
                    "4. Check your reasoning against the objective wording.",
                ]
            )
            activities.append(
                EducationalActivitySpec(
                    activity_id="act-example-1",
                    stage=EducationalStage.WORKED_EXAMPLE,
                    title=f"Worked example: {topic_title}",
                    prompt=(
                        f"Follow the worked example for {topic_title}. "
                        "Note the method step you will reuse in practice."
                    ),
                    body="\n".join(example_body_parts),
                    supporting_material=(
                        "Stay with the method — do not jump ahead to practice yet."
                    ),
                    hints=("Name the step that felt most transferable.",),
                    answer_prompt="Which method step will you reuse?",
                    objective_ids=objective_ids[:1] if objective_ids else (),
                    syllabus_refs=syllabus,
                    metadata=(
                        ("activity_type", EducationalStage.WORKED_EXAMPLE.value),
                        ("stage", EducationalStage.WORKED_EXAMPLE.value),
                        ("stage_label", "Worked example"),
                    ),
                )
            )

        scoreable_items = items_for_topic(topic_title=topic_title, limit=3)
        for index, item in enumerate(scoreable_items, start=1):
            is_final = index == len(scoreable_items)
            stage_next = (
                next_transition_label(EducationalStage.PRACTICE)
                if is_final
                else "Continue"
            )
            oid = (
                item.objective_ids[0]
                if item.objective_ids
                else (objective_ids[0] if objective_ids else f"practice-{index}")
            )
            bound = _bind_scoreable(
                item,
                objective_ids=(oid,) if oid else objective_ids[:1],
                syllabus_refs=syllabus,
            )
            answer_prompt = _answer_prompt_for(bound)
            activities.append(
                EducationalActivitySpec(
                    activity_id=f"act-practice-{index}",
                    stage=EducationalStage.PRACTICE,
                    title=f"Practice {index}: {topic_title}",
                    prompt=bound.prompt,
                    body=bound.body
                    or (
                        f"Practice activity for {topic_title}. "
                        "Use what you read and the worked example."
                    ),
                    supporting_material=bound.supporting_material
                    or (
                        f"Return to the reading if {topic_title} still feels unclear."
                    ),
                    hints=bound.hints
                    or (f"Start from the definition of {topic_title}.",),
                    answer_prompt=answer_prompt,
                    objective_ids=bound.objective_ids or objective_ids[:1],
                    syllabus_refs=bound.syllabus_refs or syllabus,
                    scoreable=bound,
                    metadata=(
                        ("activity_type", EducationalStage.PRACTICE.value),
                        ("stage", EducationalStage.PRACTICE.value),
                        ("stage_label", "Practice"),
                        ("next_action_label", stage_next),
                        ("scoreable", "1"),
                        ("response_type", bound.response_type.value),
                        ("item_id", bound.item_id),
                    ),
                )
            )

        # Fix next-action labels across the continuous sequence.
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
                    metadata=spec.metadata
                    + (("next_action_label", next_label),),
                )
            )
        return tuple(labelled)


def _bind_scoreable(
    item: ScoreablePracticeItem,
    *,
    objective_ids: tuple[str, ...],
    syllabus_refs: tuple[str, ...],
) -> ScoreablePracticeItem:
    """Attach sitting objective / syllabus refs without mutating the seed."""
    return ScoreablePracticeItem(
        item_id=item.item_id,
        prompt=item.prompt,
        response_type=item.response_type,
        answer_key=item.answer_key,
        explanation=item.explanation,
        model_answer=item.model_answer,
        mark_scheme=item.mark_scheme,
        common_mistake=item.common_mistake,
        next_action=item.next_action,
        objective_ids=item.objective_ids or objective_ids,
        syllabus_refs=item.syllabus_refs or syllabus_refs,
        topic_id=item.topic_id,
        topic_keywords=item.topic_keywords,
        choices=item.choices,
        emit_structured=item.emit_structured,
        body=item.body,
        supporting_material=item.supporting_material,
        hints=item.hints,
    )


def _answer_prompt_for(item: ScoreablePracticeItem) -> str:
    if item.response_type is PracticeResponseType.MCQ:
        return "Your choice (letter or full option)"
    if item.response_type is PracticeResponseType.NUMERIC:
        return "Your numeric answer"
    return "Your answer"
