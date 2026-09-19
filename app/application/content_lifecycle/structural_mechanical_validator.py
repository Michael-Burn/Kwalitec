"""Structural and Mechanical/Deterministic checks for content drafts.

This module validates package-shaped payloads for structural integrity and
deterministic mechanical rules only (MCQ choice shape, correct_choice_id
membership, objective_id presence/resolution, AnswerSpecification
constructibility).

It does **not** assess mathematical correctness of answers, educational
quality, or pedagogical appropriateness. Those gates are human/educational
review, not this validator.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from app.application.numeric_assessment.catalogue import (
    answer_specification_from_dict,
)
from app.application.objective_evidence.canonical_objective_id import (
    CanonicalObjectiveId,
)

SEVERITY_ERROR = "error"

RULE_MCQ_CHOICE_COUNT = "mcq.choice_count"
RULE_MCQ_CORRECT_CHOICE_ID = "mcq.correct_choice_id"
RULE_OBJECTIVE_REQUIRED = "objective.required"
RULE_OBJECTIVE_RESOLVE = "objective.resolve"
RULE_NUMERIC_ANSWER_SPECIFICATION = "numeric.answer_specification"

REQUIRED_MCQ_CHOICE_COUNT = 4


@dataclass(frozen=True)
class StructuralMechanicalFinding:
    """One structured finding from a structural/mechanical check."""

    rule_id: str
    severity: str
    field: str
    message: str


def validate_structural_and_mechanical(
    payload: dict[str, Any],
    *,
    subject_id: str,
    require_objective_id: bool = True,
    objective_resolver: CanonicalObjectiveId | None = None,
) -> tuple[StructuralMechanicalFinding, ...]:
    """Run Structural and Mechanical/Deterministic checks on a package payload.

    Args:
        payload: Educational package JSON shape (same fields as live packages).
        subject_id: Subject code used for objective_id resolution (e.g. CS1).
        require_objective_id: When True, each knowledge check must carry a
            non-empty ``objective_id``. Live inventory tests that only assert
            MCQ shape may pass False.
        objective_resolver: Optional ``CanonicalObjectiveId`` instance
            (injectable for tests).

    Returns:
        Tuple of findings. Empty means all structural/mechanical rules passed.
        An empty result does **not** mean the content is mathematically or
        educationally correct.
    """
    findings: list[StructuralMechanicalFinding] = []
    resolver = objective_resolver or CanonicalObjectiveId()
    sid = (subject_id or "").strip()

    checks = payload.get("knowledge_checks")
    if checks is None:
        checks = []
    if not isinstance(checks, list):
        findings.append(
            StructuralMechanicalFinding(
                rule_id=RULE_MCQ_CHOICE_COUNT,
                severity=SEVERITY_ERROR,
                field="knowledge_checks",
                message=(
                    "knowledge_checks must be a list of check objects; "
                    f"got {type(checks).__name__}."
                ),
            )
        )
        return tuple(findings)

    for index, check in enumerate(checks):
        if not isinstance(check, dict):
            findings.append(
                StructuralMechanicalFinding(
                    rule_id=RULE_MCQ_CHOICE_COUNT,
                    severity=SEVERITY_ERROR,
                    field=f"knowledge_checks[{index}]",
                    message=(
                        "Each knowledge check must be an object; "
                        f"got {type(check).__name__}."
                    ),
                )
            )
            continue
        findings.extend(
            _validate_knowledge_check(
                check,
                index=index,
                subject_id=sid,
                require_objective_id=require_objective_id,
                resolver=resolver,
            )
        )
    return tuple(findings)


def validate_mcq_check_structure(
    *,
    choices: list[Any] | tuple[Any, ...],
    correct_choice_id: str,
    field_prefix: str,
) -> tuple[StructuralMechanicalFinding, ...]:
    """Shared MCQ structural rules used by inventory tests and the full validator.

    Encodes the same requiredness previously asserted only in
    ``test_mcq_phase0_infrastructure``: exactly four choices, and
    ``correct_choice_id`` must match one of those choice ids.
    """
    findings: list[StructuralMechanicalFinding] = []
    choice_ids = _choice_ids(choices)
    count = len(choice_ids)
    if count != REQUIRED_MCQ_CHOICE_COUNT:
        findings.append(
            StructuralMechanicalFinding(
                rule_id=RULE_MCQ_CHOICE_COUNT,
                severity=SEVERITY_ERROR,
                field=f"{field_prefix}.choices",
                message=(
                    f"MCQ knowledge check must have exactly "
                    f"{REQUIRED_MCQ_CHOICE_COUNT} choices; found {count}."
                ),
            )
        )
    cid = (correct_choice_id or "").strip()
    if not cid or cid not in set(choice_ids):
        findings.append(
            StructuralMechanicalFinding(
                rule_id=RULE_MCQ_CORRECT_CHOICE_ID,
                severity=SEVERITY_ERROR,
                field=f"{field_prefix}.correct_choice_id",
                message=(
                    f"correct_choice_id {cid!r} does not match any choice id "
                    f"among {list(choice_ids)}."
                    if cid
                    else "correct_choice_id is missing or empty."
                ),
            )
        )
    return tuple(findings)


def _validate_knowledge_check(
    check: dict[str, Any],
    *,
    index: int,
    subject_id: str,
    require_objective_id: bool,
    resolver: CanonicalObjectiveId,
) -> list[StructuralMechanicalFinding]:
    findings: list[StructuralMechanicalFinding] = []
    prefix = f"knowledge_checks[{index}]"
    response_type = str(check.get("response_type") or "").strip().lower()

    if response_type == "mcq":
        findings.extend(
            validate_mcq_check_structure(
                choices=check.get("choices") or (),
                correct_choice_id=str(check.get("correct_choice_id") or ""),
                field_prefix=prefix,
            )
        )

    objective_id = str(check.get("objective_id") or "").strip()
    if require_objective_id:
        if not objective_id:
            findings.append(
                StructuralMechanicalFinding(
                    rule_id=RULE_OBJECTIVE_REQUIRED,
                    severity=SEVERITY_ERROR,
                    field=f"{prefix}.objective_id",
                    message="objective_id is required and must be non-empty.",
                )
            )
        else:
            resolved = resolver.resolve_from_objective_id(
                objective_id, subject_code=subject_id
            )
            if resolved is None:
                # Also accept syllabus LO codes via resolve().
                resolved = resolver.resolve(
                    objective_id, subject_code=subject_id
                )
            if resolved is None:
                findings.append(
                    StructuralMechanicalFinding(
                        rule_id=RULE_OBJECTIVE_RESOLVE,
                        severity=SEVERITY_ERROR,
                        field=f"{prefix}.objective_id",
                        message=(
                            f"objective_id {objective_id!r} does not resolve "
                            f"to a published learning objective for "
                            f"subject {subject_id!r}."
                        ),
                    )
                )
    elif objective_id:
        resolved = resolver.resolve_from_objective_id(
            objective_id, subject_code=subject_id
        )
        if resolved is None:
            resolved = resolver.resolve(objective_id, subject_code=subject_id)
        if resolved is None:
            findings.append(
                StructuralMechanicalFinding(
                    rule_id=RULE_OBJECTIVE_RESOLVE,
                    severity=SEVERITY_ERROR,
                    field=f"{prefix}.objective_id",
                    message=(
                        f"objective_id {objective_id!r} does not resolve "
                        f"to a published learning objective for "
                        f"subject {subject_id!r}."
                    ),
                )
            )

    if response_type == "numeric":
        findings.extend(_validate_numeric_specification(check, prefix=prefix))

    return findings


def _validate_numeric_specification(
    check: dict[str, Any],
    *,
    prefix: str,
) -> list[StructuralMechanicalFinding]:
    raw_spec = check.get("answer_specification")
    if raw_spec is None:
        findings: list[StructuralMechanicalFinding] = [
            StructuralMechanicalFinding(
                rule_id=RULE_NUMERIC_ANSWER_SPECIFICATION,
                severity=SEVERITY_ERROR,
                field=f"{prefix}.answer_specification",
                message=(
                    "Numeric knowledge check requires an "
                    "answer_specification object."
                ),
            )
        ]
        return findings
    if not isinstance(raw_spec, dict):
        return [
            StructuralMechanicalFinding(
                rule_id=RULE_NUMERIC_ANSWER_SPECIFICATION,
                severity=SEVERITY_ERROR,
                field=f"{prefix}.answer_specification",
                message=(
                    "answer_specification must be an object; "
                    f"got {type(raw_spec).__name__}."
                ),
            )
        ]
    try:
        answer_specification_from_dict(raw_spec)
    except (ValueError, KeyError, TypeError) as exc:
        return [
            StructuralMechanicalFinding(
                rule_id=RULE_NUMERIC_ANSWER_SPECIFICATION,
                severity=SEVERITY_ERROR,
                field=f"{prefix}.answer_specification",
                message=(
                    "answer_specification failed AnswerSpecification "
                    f"validation: {exc}."
                ),
            )
        ]
    return []


def _choice_ids(choices: list[Any] | tuple[Any, ...]) -> list[str]:
    ids: list[str] = []
    for choice in choices:
        if isinstance(choice, dict):
            cid = str(choice.get("id") or "").strip()
            if cid:
                ids.append(cid)
        elif hasattr(choice, "id"):
            cid = str(getattr(choice, "id") or "").strip()
            if cid:
                ids.append(cid)
        elif isinstance(choice, list | tuple) and choice:
            cid = str(choice[0] or "").strip()
            if cid:
                ids.append(cid)
    return ids
