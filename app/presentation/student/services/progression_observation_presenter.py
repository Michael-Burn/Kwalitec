"""Translate Progression Readiness into Study observation panels.

Presentation-only. Read-only over OEA. Never writes evidence. Never feeds
Decision Engine, arbitration, curriculum progression, or recommendations.
"""

from __future__ import annotations

from collections.abc import Sequence

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import (
    ObjectiveAssessmentEvidenceStore,
    get_objective_assessment_evidence_store,
)
from app.application.progression_readiness import (
    PROGRESSION_READINESS_CONTRACTS,
    ContractKind,
    EvidenceModality,
    InsufficientReason,
    ProgressionReadiness,
    ProgressionReadinessContract,
    evaluate,
    get_contract,
)
from app.presentation.student.dto.study_curriculum import StudyObservationPanelView

BRAND_HEADING = "What Kwalitec has observed"

# Topics authorized for observation panels (locked activation scope).
OBSERVATION_TOPIC_OBJECTIVES: dict[str, tuple[str, ...]] = {
    "CS1-A-T01": (
        "CS1-A-T01-LO01",
        "CS1-A-T01-LO02",
        "CS1-A-T01-LO03",
        "CS1-A-T01-LO04",
    ),
    "CS1-B-T03": (
        "CS1-B-T03-LO01",
        "CS1-B-T03-LO02",
    ),
}

_OBJECTIVE_LABELS: dict[str, str] = {
    "CS1-A-T01-LO01": "1.1.1",
    "CS1-A-T01-LO02": "1.1.2",
    "CS1-A-T01-LO03": "1.1.3",
    "CS1-A-T01-LO04": "1.1.4",
    "CS1-B-T03-LO01": "2.3.1",
    "CS1-B-T03-LO02": "2.3.2",
}


def _latest_scored_per_item(
    evidence: Sequence[AssessmentEvidenceRecord],
    item_ids: frozenset[str],
) -> dict[str, AssessmentEvidenceRecord]:
    latest: dict[str, AssessmentEvidenceRecord] = {}
    for record in sorted(
        (
            r
            for r in evidence
            if r.item_id in item_ids and r.scored_correct is not None
        ),
        key=lambda r: (r.occurred_at, r.evidence_id),
    ):
        latest[record.item_id] = record
    return latest


def has_meaningful_evidence(
    contract: ProgressionReadinessContract,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> bool:
    """True iff the student has attempted at least one contracted tagged item."""
    item_ids = contract.item_ids
    return any(r.item_id in item_ids for r in evidence)


def _evidence_lines(
    contract: ProgressionReadinessContract,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> tuple[str, ...]:
    latest = _latest_scored_per_item(evidence, contract.item_ids)
    lines: list[str] = []
    for spec in contract.evidence_items:
        record = latest.get(spec.item_id)
        if record is None:
            continue
        lines.append("Correct" if record.scored_correct else "Incorrect")
    return tuple(lines)


def _incorrect_component_phrase(
    contract: ProgressionReadinessContract,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> str:
    """Plain-language component for Scenario 4 (never MCQ/numeric jargon)."""
    latest = _latest_scored_per_item(evidence, contract.item_ids)
    if contract.kind is ContractKind.MIXED_MODALITY:
        for spec in contract.evidence_items:
            record = latest.get(spec.item_id)
            if record is None or record.scored_correct is not False:
                continue
            if spec.modality is EvidenceModality.NUMERIC:
                return "calculation"
            return "conceptual"
    return "conceptual"


def _correct_count(
    contract: ProgressionReadinessContract,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> int:
    latest = _latest_scored_per_item(evidence, contract.item_ids)
    return sum(1 for r in latest.values() if r.scored_correct is True)


def translate_result(
    *,
    contract: ProgressionReadinessContract,
    readiness: ProgressionReadiness,
    reason: InsufficientReason | None,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> StudyObservationPanelView:
    """Map an evaluator result to locked student-facing copy."""
    oid = contract.objective_id
    label = _OBJECTIVE_LABELS.get(oid, oid)
    lines = _evidence_lines(contract, evidence)
    n_correct = _correct_count(contract, evidence)
    m_items = contract.item_count

    if readiness is ProgressionReadiness.READY:
        return StudyObservationPanelView(
            objective_id=oid,
            objective_label=label,
            brand_heading=BRAND_HEADING,
            scenario_heading="Sufficient evidence to move forward",
            evidence_lines=lines,
            body_paragraphs=(
                (
                    f"You've answered {n_correct} of the {m_items} independent "
                    "questions assessing this objective correctly."
                ),
            ),
            meaning_paragraphs=(
                (
                    "Your current evidence meets Kwalitec's progression "
                    "requirement for this objective. This is an assessment of "
                    "the evidence available so far, not a permanent measure of "
                    "mastery."
                ),
            ),
            next_step="",
            keep_in_mind=(
                "This result can change as you encounter new assessment evidence."
            ),
        )

    if readiness is ProgressionReadiness.NOT_READY:
        component = _incorrect_component_phrase(contract, evidence)
        return StudyObservationPanelView(
            objective_id=oid,
            objective_label=label,
            brand_heading=BRAND_HEADING,
            scenario_heading="More work recommended",
            evidence_lines=lines,
            body_paragraphs=(
                (
                    "The available evidence indicates that a required part of "
                    "this objective has not yet been demonstrated."
                ),
                (
                    "Your recent assessment included an incorrect response on "
                    f"the {component} component required by this objective."
                ),
            ),
            meaning_paragraphs=(),
            next_step=(
                "Review the explanation, then look for another opportunity to "
                "demonstrate the concept independently."
            ),
            keep_in_mind="",
        )

    # INSUFFICIENT_EVIDENCE family
    if reason is InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED:
        return StudyObservationPanelView(
            objective_id=oid,
            objective_label=label,
            brand_heading=BRAND_HEADING,
            scenario_heading="More evidence needed",
            evidence_lines=lines,
            body_paragraphs=(
                (
                    "Your performance on this objective provides positive "
                    "evidence, but Kwalitec has not yet established the "
                    "prerequisite concept this objective depends on."
                ),
                (
                    "Because that prerequisite has not been assessed, Kwalitec "
                    "is not treating this result as confirmation of full "
                    "progression readiness."
                ),
            ),
            meaning_paragraphs=(),
            next_step="",
            keep_in_mind="",
        )

    # INSUFFICIENT_SAMPLE and other insufficient-family reasons
    return StudyObservationPanelView(
        objective_id=oid,
        objective_label=label,
        brand_heading=BRAND_HEADING,
        scenario_heading="More evidence needed",
        evidence_lines=lines,
        body_paragraphs=(
            (
                "Kwalitec has seen some evidence for this objective, but not "
                "enough to make a reliable progression judgment yet."
            ),
        ),
        meaning_paragraphs=(),
        next_step=(
            "Continue studying and complete another independent assessment "
            "when one is presented."
        ),
        keep_in_mind="",
    )


def panels_for_topic(
    *,
    topic_id: str,
    student_id: str,
    evidence: Sequence[AssessmentEvidenceRecord],
) -> tuple[StudyObservationPanelView, ...]:
    """Build observation panels for an authorized topic (noise-gated)."""
    objective_ids = OBSERVATION_TOPIC_OBJECTIVES.get((topic_id or "").strip(), ())
    if not objective_ids:
        return ()
    panels: list[StudyObservationPanelView] = []
    for oid in objective_ids:
        contract = get_contract(oid)
        if contract is None:
            continue
        if not has_meaningful_evidence(contract, evidence):
            continue
        result = evaluate(oid, student_id, contract, evidence)
        panels.append(
            translate_result(
                contract=contract,
                readiness=result.readiness,
                reason=result.reason,
                evidence=evidence,
            )
        )
    return tuple(panels)


def panels_by_topic_for_student(
    *,
    student_id: str,
    store: ObjectiveAssessmentEvidenceStore | None = None,
    topic_ids: Sequence[str] | None = None,
) -> dict[str, tuple[StudyObservationPanelView, ...]]:
    """One OEA read, then panels for authorized topics present in topic_ids."""
    sid = str(student_id or "").strip()
    evidence_store = store or get_objective_assessment_evidence_store()
    evidence = evidence_store.list_for_student(sid)
    wanted = {
        (t or "").strip()
        for t in (topic_ids if topic_ids is not None else OBSERVATION_TOPIC_OBJECTIVES)
    }
    out: dict[str, tuple[StudyObservationPanelView, ...]] = {}
    for topic_id in OBSERVATION_TOPIC_OBJECTIVES:
        if topic_id not in wanted:
            continue
        panels = panels_for_topic(
            topic_id=topic_id, student_id=sid, evidence=evidence
        )
        if panels:
            out[topic_id] = panels
    return out


def contracted_objective_ids() -> frozenset[str]:
    """Objective ids that have authored contracts (for tests / founder)."""
    return frozenset(PROGRESSION_READINESS_CONTRACTS)
