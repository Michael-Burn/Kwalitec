"""Acceptance contract for LEGACY_COMPLETION evidence.

Stage A ``TopicProgress.completed`` is confirmed from live write paths to mean
Study Progress completion only (not Estimated Knowledge / mastery). Writers:

1. Study Plan Wizard / Educational History ``sync_declared_completed_topics``
   and plan-init ``completed_curriculum_topics``: self-declared prior units
   written as Study Progress (no ``last_reviewed``, ``revision_count`` stays 0).
2. Legacy Learning Mode mission helper ``_apply_mission_topic_progress``:
   authorised first-time mission completion (calls ``mark_reviewed()``).
3. Educational Continuity remap: copies whatever ``completed`` already was.

Runtime C separately records prior knowledge as ``PRIOR_KNOWLEDGE_CLAIM``
(and reclassifies legacy baseline ``TOPIC_COMPLETED`` payloads). Those claims
are never LEGACY_COMPLETION and never VERIFIED_COMPLETION.

Acceptance for LEGACY_COMPLETION therefore requires:
- ``completed is True`` on a row owned by the learner;
- resolution through ``curriculum_topic_identity_map`` (stage_a_database) to an
  active canonical topic (exact or defensible_but_changed; never orphan /
  obsolete_no_equivalent / unmapped);
- not claim-only: when a correlating prior-knowledge claim exists for the same
  canonical topic and the Stage A row shows no study activity
  (``last_reviewed is None`` and ``revision_count == 0``), reject.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from app.application.coverage_reconciliation.constants import (
    ACCEPTABLE_MAPPING_STATUSES,
)


@dataclass(frozen=True)
class LegacyCompletionCandidate:
    """Inputs evaluated by the LEGACY_COMPLETION acceptance contract."""

    user_id: int
    learner_user_id: int
    completed: bool
    last_reviewed: datetime | None
    revision_count: int
    mapping_status: str | None
    canonical_id: str | None
    prior_knowledge_claim_present: bool


@dataclass(frozen=True)
class LegacyAcceptanceResult:
    """Outcome of the LEGACY_COMPLETION acceptance contract."""

    accepted: bool
    reason: str


def has_stage_a_study_activity(
    *,
    last_reviewed: datetime | None,
    revision_count: int,
) -> bool:
    """True when Stage A shows study activity beyond a bare completed flag."""
    if last_reviewed is not None:
        return True
    return int(revision_count or 0) > 0


def accept_legacy_completion(
    candidate: LegacyCompletionCandidate,
) -> LegacyAcceptanceResult:
    """Apply the LEGACY_COMPLETION acceptance contract to one Stage A row."""
    if candidate.user_id != candidate.learner_user_id:
        return LegacyAcceptanceResult(
            accepted=False,
            reason="not_attributable_to_learner",
        )
    if not candidate.completed:
        return LegacyAcceptanceResult(
            accepted=False,
            reason="stage_a_completed_false",
        )
    if not candidate.canonical_id:
        return LegacyAcceptanceResult(
            accepted=False,
            reason="no_canonical_identity",
        )
    if candidate.mapping_status not in ACCEPTABLE_MAPPING_STATUSES:
        return LegacyAcceptanceResult(
            accepted=False,
            reason=f"mapping_not_acceptable:{candidate.mapping_status or 'missing'}",
        )

    study_activity = has_stage_a_study_activity(
        last_reviewed=candidate.last_reviewed,
        revision_count=candidate.revision_count,
    )
    if candidate.prior_knowledge_claim_present and not study_activity:
        return LegacyAcceptanceResult(
            accepted=False,
            reason="prior_knowledge_declaration_only",
        )

    if study_activity:
        return LegacyAcceptanceResult(
            accepted=True,
            reason="stage_a_completed_with_study_activity",
        )
    return LegacyAcceptanceResult(
        accepted=True,
        reason="stage_a_completed_historical_study_progress",
    )
