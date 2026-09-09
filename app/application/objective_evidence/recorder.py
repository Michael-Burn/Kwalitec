"""Record Assessment Evidence from tagged scoreable practice (OEA Phase 2).

Writes only when the scored item carries a real authored curriculum
``objective_id`` on ``ScoreablePracticeItem.objective_ids``. Never infers
from package ``topic_focus_lo`` or synthetic activity objective ids.

Does not notify Twin, Spacing Scheduler, Policy V1, Decision Engine, or
any Progress / EK path.
"""

from __future__ import annotations

from typing import Any

from app.application.learning_session.scoreable_practice import (
    PracticeScoreResult,
    ScoreablePracticeItem,
)
from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import (
    ObjectiveAssessmentEvidenceStore,
    get_objective_assessment_evidence_store,
    new_evidence_id,
    utc_now,
)

SOURCE_PACKAGE_ACTIVITY_ENGINE = "package_activity_engine"


def _authored_curriculum_objective_id(
    scoreable: ScoreablePracticeItem | None,
) -> str:
    """Return the single authored curriculum objective_id, or empty.

    Requires a non-empty ``objective_ids`` entry that looks like a published
    curriculum LO id (contains ``-LO``). Synthetic package activity ids such
    as ``{package_id}:lo`` are ignored.
    """
    if scoreable is None:
        return ""
    for raw in scoreable.objective_ids or ():
        token = str(raw or "").strip()
        if not token:
            continue
        # Published CS1 (and similar) LOs use ids like CS1-B-T01-LO04.
        if "-LO" in token.upper():
            return token
    return ""


class ObjectiveAssessmentEvidenceRecorder:
    """Append Assessment Evidence only for authored, tagged practice items."""

    def __init__(
        self,
        *,
        store: ObjectiveAssessmentEvidenceStore | None = None,
    ) -> None:
        self._store = store or get_objective_assessment_evidence_store()

    def record_if_tagged(
        self,
        *,
        student_id: str,
        session_id: str,
        package_id: str,
        scoreable: ScoreablePracticeItem | None,
        score: PracticeScoreResult,
        response_type: str = "",
        selected_misconception_tag: str = "",
        source: str = SOURCE_PACKAGE_ACTIVITY_ENGINE,
        occurred_at: Any = None,
    ) -> AssessmentEvidenceRecord | None:
        """Write one evidence row when the item carries a real objective_id.

        Returns the stored record, or None when the item is untagged.
        Never falls back to package-level LO inference.
        """
        objective_id = _authored_curriculum_objective_id(scoreable)
        if not objective_id:
            return None

        item_id = str(
            (score.item_id if score is not None else "")
            or (scoreable.item_id if scoreable is not None else "")
            or ""
        ).strip()
        if not item_id:
            return None

        when = occurred_at if occurred_at is not None else utc_now()
        if getattr(when, "tzinfo", None) is None:
            from datetime import UTC

            when = when.replace(tzinfo=UTC)

        rtype = (response_type or "").strip()
        if not rtype and scoreable is not None:
            raw_type = getattr(
                scoreable.response_type, "value", scoreable.response_type
            )
            rtype = str(raw_type or "")
        if not rtype and score is not None:
            rtype = str(score.response_type or "").strip()

        tag = (selected_misconception_tag or "").strip()
        if not tag and score is not None:
            tag = str(score.selected_misconception_tag or "").strip()

        record = AssessmentEvidenceRecord(
            evidence_id=new_evidence_id(),
            student_id=str(student_id or "").strip(),
            objective_id=objective_id,
            item_id=item_id,
            package_id=str(package_id or "").strip(),
            session_id=str(session_id or "").strip(),
            response_type=rtype,
            scored_correct=score.scored_correct if score is not None else None,
            occurred_at=when,
            source=(source or "").strip() or SOURCE_PACKAGE_ACTIVITY_ENGINE,
            selected_misconception_tag=tag,
        )
        return self._store.append(record)
