"""Map Baseline continue-from declarations onto Runtime C leaf topics.

Published Baseline pickers use syllabus **section** codes (``1``…``5``).
Runtime C progress is event-sourced from leaf **topic_id**s. This module
bridges the two without inventing curriculum structure.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.application.educational_engine_foundation.dto import (
    EducationalArtefactSnapshot,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    student_syllabus_code,
)

_HIERARCHICAL = re.compile(r"^\d+\.\d+(?:\.\d+)*$")
_SECTION_NUMBER = re.compile(r"^\d+$")
_TITLE_LEADING = re.compile(r"^(\d+(?:\.\d+)*)\s+(.+)$")


@dataclass(frozen=True)
class BaselinePositionSeed:
    """Leaf-topic seed derived from Baseline continue-from declarations."""

    completed_topic_ids: tuple[str, ...]
    current_topic_id: str | None
    continue_code: str | None
    source: str = "baseline_self_declared"


def resolve_baseline_position_seed(
    artefacts: EducationalArtefactSnapshot,
    *,
    curriculum_topic_code: str | None,
    completed_curriculum_topics: list[str] | tuple[str, ...] | None = None,
) -> BaselinePositionSeed:
    """Resolve section/leaf Baseline codes into Runtime C topic ids.

    Continue-from semantics match Study Plan Baseline: the selected code is
    the **resume** point (not yet completed). Prior sections/topics become
    completed.
    """
    continue_code = (curriculum_topic_code or "").strip() or None
    if not continue_code:
        return BaselinePositionSeed(
            completed_topic_ids=(),
            current_topic_id=None,
            continue_code=None,
        )

    ordered_ids = _ordered_leaf_topic_ids(artefacts)
    if not ordered_ids:
        return BaselinePositionSeed(
            completed_topic_ids=(),
            current_topic_id=None,
            continue_code=continue_code,
        )

    # Section-level continue (published CS1 picker): "4" → Regression / GLM chapter.
    if _SECTION_NUMBER.match(continue_code):
        return _seed_from_section(
            artefacts,
            continue_section=continue_code,
            completed_section_codes=tuple(
                str(c).strip()
                for c in (completed_curriculum_topics or ())
                if str(c).strip()
            ),
            ordered_ids=ordered_ids,
        )

    # Leaf syllabus code (1.1 / 4.2) or raw topic_id.
    leaf_id = _resolve_leaf_topic_id(artefacts, continue_code)
    if leaf_id is None or leaf_id not in ordered_ids:
        return BaselinePositionSeed(
            completed_topic_ids=(),
            current_topic_id=None,
            continue_code=continue_code,
        )
    idx = ordered_ids.index(leaf_id)
    return BaselinePositionSeed(
        completed_topic_ids=tuple(ordered_ids[:idx]),
        current_topic_id=leaf_id,
        continue_code=continue_code,
    )


def _seed_from_section(
    artefacts: EducationalArtefactSnapshot,
    *,
    continue_section: str,
    completed_section_codes: tuple[str, ...],
    ordered_ids: tuple[str, ...],
) -> BaselinePositionSeed:
    sections_by_number = {
        str(s.get("number") or "").strip(): s
        for s in artefacts.sections
        if str(s.get("number") or "").strip()
    }
    continue_section_row = sections_by_number.get(continue_section)
    if continue_section_row is None:
        return BaselinePositionSeed(
            completed_topic_ids=(),
            current_topic_id=None,
            continue_code=continue_section,
        )

    prior = completed_section_codes
    if not prior:
        # Derive priors from section order when caller omitted the list.
        ordered_numbers = sorted(
            sections_by_number.keys(),
            key=lambda n: int(n) if n.isdigit() else n,
        )
        if continue_section in ordered_numbers:
            prior = tuple(
                ordered_numbers[: ordered_numbers.index(continue_section)]
            )

    completed: list[str] = []
    seen: set[str] = set()
    for number in prior:
        row = sections_by_number.get(number)
        if row is None:
            continue
        for tid in row.get("topic_ids") or ():
            tid_s = str(tid).strip()
            if tid_s and tid_s in ordered_ids and tid_s not in seen:
                seen.add(tid_s)
                completed.append(tid_s)

    current = None
    for tid in continue_section_row.get("topic_ids") or ():
        tid_s = str(tid).strip()
        if tid_s and tid_s in ordered_ids and tid_s not in seen:
            current = tid_s
            break

    return BaselinePositionSeed(
        completed_topic_ids=tuple(completed),
        current_topic_id=current,
        continue_code=continue_section,
    )


def _ordered_leaf_topic_ids(
    artefacts: EducationalArtefactSnapshot,
) -> tuple[str, ...]:
    if artefacts.progress_model and artefacts.progress_model.topic_ids:
        return tuple(
            str(tid).strip()
            for tid in artefacts.progress_model.topic_ids
            if str(tid).strip()
        )
    # Fallback: section order then topic display_order.
    ordered: list[str] = []
    seen: set[str] = set()
    for section in sorted(
        artefacts.sections,
        key=lambda s: int(s.get("display_order") or 0),
    ):
        for tid in section.get("topic_ids") or ():
            tid_s = str(tid).strip()
            if tid_s and tid_s not in seen:
                seen.add(tid_s)
                ordered.append(tid_s)
    if ordered:
        return tuple(ordered)
    return tuple(
        str(t.get("topic_id") or "").strip()
        for t in sorted(
            artefacts.topics,
            key=lambda row: int(row.get("display_order") or 0),
        )
        if str(t.get("topic_id") or "").strip()
    )


def _resolve_leaf_topic_id(
    artefacts: EducationalArtefactSnapshot,
    code: str,
) -> str | None:
    raw = (code or "").strip()
    if not raw:
        return None
    for topic in artefacts.topics:
        tid = str(topic.get("topic_id") or "").strip()
        if tid == raw:
            return tid
        human = student_syllabus_code(
            code=str(topic.get("code") or "").strip(),
            title=str(topic.get("title") or "").strip(),
            number=str(topic.get("number") or "").strip(),
        )
        title = str(topic.get("title") or "").strip()
        match = _TITLE_LEADING.match(title)
        embedded = match.group(1) if match else ""
        if raw in {human, embedded} and (
            _HIERARCHICAL.match(raw) or raw == human
        ):
            return tid
        # Title contains the phrase (e.g. "Generalised linear models").
        if len(raw) >= 8 and raw.lower() in title.lower():
            return tid
    return None
