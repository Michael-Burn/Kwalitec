"""Replay fixtures covering Educational Intelligence certification scenarios."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum

from application.assessment.evidence.dto import EvidenceBundleDTO, EvidenceItemDTO
from tests.application.reasoning.conftest import make_bundle, make_item

CERT_FIXED_AT = datetime(2026, 7, 28, 12, 0, 0, tzinfo=UTC).replace(tzinfo=None)


class ReplayScenario(StrEnum):
    """Named deterministic replay scenarios for AP-002D7."""

    COLD_START = "cold_start_learner"
    RETURNING = "returning_learner"
    STRONG_EVIDENCE = "strong_evidence"
    WEAK_EVIDENCE = "weak_evidence"
    CONFLICTING_EVIDENCE = "conflicting_evidence"
    DUPLICATE_SUBMISSION = "duplicate_submission"
    VERSION_MISMATCH = "version_mismatch"
    PARTIAL_EVIDENCE = "partial_evidence"


@dataclass(frozen=True, slots=True)
class ReplayFixture:
    """Immutable evidence fixture for one certification scenario."""

    scenario: ReplayScenario
    twin_id: str
    student_id: str
    correlation_id: str
    reasoning_request_id: str
    bundle: EvidenceBundleDTO
    packaging_version: str = "AP-002C.1"
    notes: str = ""


def _items_strong() -> tuple[EvidenceItemDTO, ...]:
    return tuple(
        make_item(
            item_id=f"item-s{i}",
            observation_id=f"obs-s{i}",
            question_id=f"q-s{i}",
            correctness="correct",
            confidence=5,
            hints_used=0,
            retries=0,
        )
        for i in range(1, 5)
    )


def _items_weak() -> tuple[EvidenceItemDTO, ...]:
    return (
        make_item(
            item_id="item-w1",
            observation_id="obs-w1",
            question_id="q-w1",
            correctness="correct",
            confidence=None,
            hints_used=2,
            retries=2,
        ),
    )


def _items_conflicting() -> tuple[EvidenceItemDTO, ...]:
    return (
        make_item(
            item_id="item-c1",
            observation_id="obs-c1",
            question_id="q-c1",
            correctness="correct",
            confidence=4,
        ),
        make_item(
            item_id="item-c2",
            observation_id="obs-c2",
            question_id="q-c2",
            correctness="incorrect",
            confidence=4,
            hints_used=1,
            retries=1,
            misconception_tags=("confuses_prior",),
        ),
        make_item(
            item_id="item-c3",
            observation_id="obs-c3",
            question_id="q-c3",
            correctness="correct",
            confidence=3,
        ),
    )


def _items_partial() -> tuple[EvidenceItemDTO, ...]:
    return (
        make_item(
            item_id="item-p1",
            observation_id="obs-p1",
            question_id="q-p1",
            correctness="incorrect",
            confidence=2,
            hints_used=1,
            misconception_tags=("thin_signal",),
        ),
    )


def build_fixture(scenario: ReplayScenario) -> ReplayFixture:
    """Build a deterministic evidence fixture for the named scenario."""
    base_id = scenario.value.replace("_", "-")
    twin_id = f"twin-{base_id}"
    student_id = f"student-{base_id}"
    correlation_id = f"corr-{base_id}"
    reasoning_request_id = f"rrq-{base_id}"

    if scenario is ReplayScenario.COLD_START:
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            evidence_strength="moderate",
        )
        notes = "Cold-start Twin with empty mastery; first evidence cycle."
    elif scenario is ReplayScenario.RETURNING:
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            items=(
                make_item(
                    item_id="item-r1",
                    observation_id="obs-r1",
                    question_id="q-r1",
                    correctness="correct",
                    confidence=4,
                ),
            ),
            observation_ids=("obs-r1",),
            question_ids=("q-r1",),
            summary_count=1,
            evidence_strength="moderate",
        )
        notes = "Returning learner receives additional moderate evidence."
    elif scenario is ReplayScenario.STRONG_EVIDENCE:
        items = _items_strong()
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            items=items,
            observation_ids=tuple(i.observation_id for i in items),
            question_ids=tuple(i.question_id for i in items if i.question_id),
            summary_count=len(items),
            evidence_strength="strong",
        )
        notes = "Strong multi-item correct evidence."
    elif scenario is ReplayScenario.WEAK_EVIDENCE:
        items = _items_weak()
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            items=items,
            observation_ids=tuple(i.observation_id for i in items),
            question_ids=tuple(i.question_id for i in items if i.question_id),
            summary_count=len(items),
            evidence_strength="thin",
        )
        notes = "Thin/weak evidence must preserve uncertainty."
    elif scenario is ReplayScenario.CONFLICTING_EVIDENCE:
        items = _items_conflicting()
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            items=items,
            observation_ids=tuple(i.observation_id for i in items),
            question_ids=tuple(i.question_id for i in items if i.question_id),
            summary_count=len(items),
            evidence_strength="moderate",
        )
        notes = "Correct/incorrect mix; mastery must not overstate certainty."
    elif scenario is ReplayScenario.DUPLICATE_SUBMISSION:
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            evidence_strength="moderate",
        )
        notes = "Identical bundle replayed; stage outputs must match exactly."
    elif scenario is ReplayScenario.VERSION_MISMATCH:
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            packaging_version="AP-999.unsupported.v0",
            evidence_strength="moderate",
        )
        notes = "Unsupported packaging version must be rejected."
    elif scenario is ReplayScenario.PARTIAL_EVIDENCE:
        items = _items_partial()
        bundle = make_bundle(
            bundle_id=f"bundle-{base_id}",
            session_id=f"sess-{base_id}",
            items=items,
            observation_ids=tuple(i.observation_id for i in items),
            question_ids=tuple(i.question_id for i in items if i.question_id),
            summary_count=len(items),
            evidence_strength="thin",
        )
        notes = "Partial single-item evidence; honesty over fabrication."
    else:  # pragma: no cover - enum exhaustive
        raise ValueError(f"unknown scenario: {scenario!r}")

    return ReplayFixture(
        scenario=scenario,
        twin_id=twin_id,
        student_id=student_id,
        correlation_id=correlation_id,
        reasoning_request_id=reasoning_request_id,
        bundle=bundle,
        packaging_version=bundle.metadata.packaging_version,
        notes=notes,
    )


def all_replay_fixtures() -> tuple[ReplayFixture, ...]:
    """Return every certified replay fixture in stable order."""
    return tuple(build_fixture(scenario) for scenario in ReplayScenario)
