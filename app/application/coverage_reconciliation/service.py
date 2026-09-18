"""Canonical coverage reconciliation (dual-source eligibility).

Reads Stage A ``TopicProgress.completed`` and Runtime C verified
``TOPIC_COMPLETED`` events, resolves both through the existing
``canonical_curriculum_topic`` / ``curriculum_topic_identity_map`` layer, and
classifies each canonical topic into one of four eligibility categories.

Student-facing coverage displays may consume ``display_coverage`` /
``coverage_for_learner``. Does not write Study Progress. Does not touch Twin,
Progression Readiness, Policy V1, assessment, arbitration, or Exam Readiness.
"""

from __future__ import annotations

import json
import logging
from collections import defaultdict
from typing import Any

from app.application.coverage_reconciliation.acceptance import (
    LegacyCompletionCandidate,
    accept_legacy_completion,
)
from app.application.coverage_reconciliation.constants import (
    ACCEPTABLE_MAPPING_STATUSES,
    CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
    CATEGORY_CONFIRMED_COVERED,
    CATEGORY_HISTORICALLY_COMPLETED,
    CATEGORY_NOT_COVERED,
    COVERED_FOR_DISPLAY,
    EVIDENCE_LEGACY_COMPLETION,
    EVIDENCE_VERIFIED_COMPLETION,
)
from app.application.coverage_reconciliation.types import (
    CanonicalCoverageVerdict,
    CoverageDisplay,
    EvidenceProvenance,
    LearnerCoverageReconciliation,
    UnmappedHistoricalActivity,
)
from app.application.curriculum_identity.constants import (
    ACTIVE_CS1_CURRICULUM_VERSION,
    ACTIVE_CS1_STAGE_A_SOURCE_VERSION,
    MAPPING_OBSOLETE_NO_EQUIVALENT,
    SOURCE_PUBLISHED_CONTENT,
    SOURCE_STAGE_A_DATABASE,
    SOURCE_STUDY_EVENT,
    STATUS_ACTIVE,
    UNKNOWN_CURRICULUM_IDENTITY,
)
from app.application.curriculum_identity.service import CurriculumIdentityService
from app.domain.educational_runtime_engine.events import (
    EducationalEventRecord,
    EducationalEventType,
)
from app.domain.educational_runtime_engine.progress import (
    is_legacy_baseline_topic_completed,
)
from app.models.curriculum_identity import (
    CanonicalCurriculumTopic,
    CurriculumTopicIdentityMap,
)
from app.models.educational_runtime_engine import RuntimeEducationalEvent
from app.models.topic_progress import TopicProgress
from app.models.user import User

logger = logging.getLogger(__name__)


def _parse_payload(payload_json: str | None) -> dict[str, Any]:
    try:
        data = json.loads(payload_json or "{}")
    except (TypeError, ValueError):
        return {}
    return data if isinstance(data, dict) else {}


def _event_record(row: RuntimeEducationalEvent) -> EducationalEventRecord | None:
    try:
        event_type = EducationalEventType(row.event_type)
    except ValueError:
        return None
    return EducationalEventRecord(
        event_id=row.event_id,
        event_type=event_type,
        user_id=row.user_id,
        curriculum_identity=row.curriculum_identity or "",
        enrolment_id=row.enrolment_id,
        plan_instance_id=row.plan_instance_id,
        topic_id=row.topic_id,
        mission_instance_id=row.mission_instance_id,
        payload=_parse_payload(row.payload_json),
        occurred_at=row.occurred_at,
    )


def _classify_eligibility(
    *,
    legacy_accepted: bool,
    verified_accepted: bool,
    ambiguous_activity: bool,
) -> tuple[str, str]:
    """Return (eligibility, reasoning) for one canonical topic."""
    if verified_accepted and legacy_accepted:
        return (
            CATEGORY_CONFIRMED_COVERED,
            "Verified Runtime C TOPIC_COMPLETED and accepted Stage A "
            "LEGACY_COMPLETION both establish coverage for this canonical topic.",
        )
    if verified_accepted:
        return (
            CATEGORY_CONFIRMED_COVERED,
            "Verified Runtime C TOPIC_COMPLETED establishes coverage. "
            "Absence of accepted legacy evidence does not weaken verified coverage.",
        )
    if legacy_accepted:
        return (
            CATEGORY_HISTORICALLY_COMPLETED,
            "Accepted Stage A LEGACY_COMPLETION establishes historical coverage. "
            "Absence of verified Runtime C evidence must not be read as proof "
            "that legitimate historical exposure did not occur.",
        )
    if ambiguous_activity:
        return (
            CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
            "Historical activity exists but failed the coverage acceptance "
            "contract (unmapped/orphan identity, prior-knowledge declaration "
            "only, or otherwise non-defensible mapping).",
        )
    return (
        CATEGORY_NOT_COVERED,
        "No Stage A completion and no verified Runtime C TOPIC_COMPLETED "
        "for this canonical topic.",
    )


class CoverageReconciliationService:
    """Derive dual-source coverage eligibility per canonical topic."""

    @staticmethod
    def display_coverage(
        result: LearnerCoverageReconciliation,
    ) -> CoverageDisplay:
        """Project reconciled eligibility into student-facing coverage numbers."""
        confirmed = 0
        historical = 0
        for verdict in result.canonical_verdicts:
            if verdict.eligibility not in COVERED_FOR_DISPLAY:
                continue
            if verdict.eligibility == CATEGORY_CONFIRMED_COVERED:
                confirmed += 1
            else:
                historical += 1
        covered = confirmed + historical
        total = len(result.canonical_verdicts)
        ratio = (covered / total) if total else 0.0
        ratio = max(0.0, min(1.0, float(ratio)))
        percent = int(round(ratio * 100)) if total else 0
        label = f"{covered} of {total} topics completed" if total else ""
        return CoverageDisplay(
            covered_count=covered,
            topic_count=total,
            coverage_ratio=ratio,
            coverage_percent=percent,
            coverage_label=label,
            confirmed_covered_count=confirmed,
            historically_completed_count=historical,
        )

    @staticmethod
    def coverage_for_learner(
        user_id: int,
        *,
        curriculum_version: str = ACTIVE_CS1_CURRICULUM_VERSION,
        stage_a_source_version: str = ACTIVE_CS1_STAGE_A_SOURCE_VERSION,
    ) -> CoverageDisplay:
        """Reconcile then project coverage numbers for one learner."""
        result = CoverageReconciliationService.reconcile_learner(
            user_id,
            curriculum_version=curriculum_version,
            stage_a_source_version=stage_a_source_version,
        )
        return CoverageReconciliationService.display_coverage(result)

    @staticmethod
    def reconcile_learner(
        user_id: int,
        *,
        curriculum_version: str = ACTIVE_CS1_CURRICULUM_VERSION,
        stage_a_source_version: str = ACTIVE_CS1_STAGE_A_SOURCE_VERSION,
    ) -> LearnerCoverageReconciliation:
        """Reconcile coverage evidence for one learner (read-only)."""
        CurriculumIdentityService.ensure_active_cs1_populated(require_stage_a=False)

        user = User.query.filter_by(id=user_id).first()
        email = user.email if user is not None else None

        canonical_rows = (
            CanonicalCurriculumTopic.query.filter_by(
                curriculum_version=curriculum_version,
                status=STATUS_ACTIVE,
            )
            .order_by(CanonicalCurriculumTopic.title)
            .all()
        )

        stage_a_maps = CurriculumTopicIdentityMap.query.filter_by(
            source_system=SOURCE_STAGE_A_DATABASE,
            source_version=stage_a_source_version,
        ).all()
        stage_a_by_source_id = {row.source_id: row for row in stage_a_maps}
        stage_a_by_canonical: dict[str, list[CurriculumTopicIdentityMap]] = defaultdict(
            list
        )
        for row in stage_a_maps:
            if row.canonical_id:
                stage_a_by_canonical[row.canonical_id].append(row)

        progress_rows = TopicProgress.query.filter_by(user_id=user_id).all()
        progress_by_topic_id = {int(row.topic_id): row for row in progress_rows}

        event_rows = RuntimeEducationalEvent.query.filter_by(user_id=user_id).all()

        verified_by_canonical: dict[str, list[RuntimeEducationalEvent]] = defaultdict(
            list
        )
        claims_by_canonical: dict[str, list[RuntimeEducationalEvent]] = defaultdict(
            list
        )
        unmapped_events: list[UnmappedHistoricalActivity] = []

        for row in event_rows:
            record = _event_record(row)
            if record is None:
                continue
            if record.event_type not in (
                EducationalEventType.TOPIC_COMPLETED,
                EducationalEventType.PRIOR_KNOWLEDGE_CLAIM,
            ):
                continue

            token = (row.topic_id or "").strip()
            if not token or token == UNKNOWN_CURRICULUM_IDENTITY:
                unmapped_events.append(
                    UnmappedHistoricalActivity(
                        kind=row.event_type,
                        source_system=SOURCE_STUDY_EVENT,
                        source_id=token or UNKNOWN_CURRICULUM_IDENTITY,
                        source_version=row.curriculum_identity,
                        mapping_status=None,
                        eligibility=CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
                        reasoning=(
                            "Runtime event topic_id missing or firewall-"
                            "unknown; cannot bind to a canonical topic."
                        ),
                        details={
                            "event_id": row.event_id,
                            "curriculum_identity": row.curriculum_identity,
                        },
                    )
                )
                continue

            resolved = CoverageReconciliationService._resolve_event_topic(
                token=token,
                curriculum_identity=row.curriculum_identity or "",
            )
            if resolved is None:
                unmapped_events.append(
                    UnmappedHistoricalActivity(
                        kind=row.event_type,
                        source_system=SOURCE_STUDY_EVENT,
                        source_id=token,
                        source_version=row.curriculum_identity,
                        mapping_status=None,
                        eligibility=CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
                        reasoning=(
                            "Runtime event topic_id did not resolve through "
                            "the canonical identity map."
                        ),
                        details={"event_id": row.event_id},
                    )
                )
                continue

            if record.event_type == EducationalEventType.PRIOR_KNOWLEDGE_CLAIM:
                claims_by_canonical[resolved.canonical_id].append(row)
            elif is_legacy_baseline_topic_completed(record):
                claims_by_canonical[resolved.canonical_id].append(row)
            else:
                verified_by_canonical[resolved.canonical_id].append(row)

        unmapped_progress: list[UnmappedHistoricalActivity] = []
        for topic_id, progress in progress_by_topic_id.items():
            if not progress.completed:
                continue
            map_row = stage_a_by_source_id.get(str(topic_id))
            if map_row is None:
                unmapped_progress.append(
                    UnmappedHistoricalActivity(
                        kind="stage_a_completed",
                        source_system=SOURCE_STAGE_A_DATABASE,
                        source_id=str(topic_id),
                        source_version=stage_a_source_version,
                        mapping_status=None,
                        eligibility=CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
                        reasoning=(
                            "Stage A TopicProgress.completed has no identity-map "
                            "row; never silently promoted to coverage."
                        ),
                        details={
                            "topic_progress_id": progress.id,
                            "current_stage": progress.current_stage,
                        },
                    )
                )
                continue
            if (
                map_row.mapping_status == MAPPING_OBSOLETE_NO_EQUIVALENT
                or map_row.canonical_id is None
            ):
                unmapped_progress.append(
                    UnmappedHistoricalActivity(
                        kind="stage_a_completed_orphan",
                        source_system=SOURCE_STAGE_A_DATABASE,
                        source_id=str(topic_id),
                        source_version=stage_a_source_version,
                        mapping_status=map_row.mapping_status,
                        eligibility=CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY,
                        reasoning=(
                            "Stage A TopicProgress.completed maps as orphan / "
                            "obsolete_no_equivalent; preserved as ambiguous "
                            "historical activity, not coverage."
                        ),
                        details={
                            "topic_progress_id": progress.id,
                            "mapping_notes": map_row.mapping_notes,
                        },
                    )
                )

        verdicts: list[CanonicalCoverageVerdict] = []
        for canonical in canonical_rows:
            cid = canonical.canonical_id
            maps_for = stage_a_by_canonical.get(cid, [])
            mapping_status = maps_for[0].mapping_status if maps_for else None

            legacy_present = False
            legacy_accepted = False
            legacy_reason = "no_stage_a_completed_row"
            legacy_details: dict[str, Any] = {}
            claim_present = bool(claims_by_canonical.get(cid))

            for map_row in maps_for:
                if map_row.mapping_status not in ACCEPTABLE_MAPPING_STATUSES:
                    continue
                try:
                    topic_pk = int(map_row.source_id)
                except (TypeError, ValueError):
                    continue
                progress = progress_by_topic_id.get(topic_pk)
                if progress is None or not progress.completed:
                    continue
                legacy_present = True
                acceptance = accept_legacy_completion(
                    LegacyCompletionCandidate(
                        user_id=progress.user_id,
                        learner_user_id=user_id,
                        completed=bool(progress.completed),
                        last_reviewed=progress.last_reviewed,
                        revision_count=int(progress.revision_count or 0),
                        mapping_status=map_row.mapping_status,
                        canonical_id=cid,
                        prior_knowledge_claim_present=claim_present,
                    )
                )
                legacy_reason = acceptance.reason
                legacy_details = {
                    "stage_a_topic_id": topic_pk,
                    "topic_progress_id": progress.id,
                    "last_reviewed": (
                        progress.last_reviewed.isoformat()
                        if progress.last_reviewed
                        else None
                    ),
                    "revision_count": int(progress.revision_count or 0),
                    "current_stage": progress.current_stage,
                    "prior_knowledge_claim_present": claim_present,
                }
                if acceptance.accepted:
                    legacy_accepted = True
                    break

            verified_rows = verified_by_canonical.get(cid, [])
            verified_present = bool(verified_rows)
            verified_accepted = verified_present
            verified_reason = (
                "verified_topic_completed_event"
                if verified_accepted
                else "no_verified_topic_completed"
            )

            ambiguous = False
            if legacy_present and not legacy_accepted:
                ambiguous = True
            if claim_present and not legacy_accepted and not verified_accepted:
                ambiguous = True

            evidence: list[str] = []
            provenance: list[EvidenceProvenance] = []
            if legacy_present:
                provenance.append(
                    EvidenceProvenance(
                        source=EVIDENCE_LEGACY_COMPLETION,
                        accepted=legacy_accepted,
                        reason=legacy_reason,
                        details=legacy_details,
                    )
                )
                if legacy_accepted:
                    evidence.append(EVIDENCE_LEGACY_COMPLETION)
            if verified_present:
                provenance.append(
                    EvidenceProvenance(
                        source=EVIDENCE_VERIFIED_COMPLETION,
                        accepted=verified_accepted,
                        reason=verified_reason,
                        details={
                            "event_ids": [row.event_id for row in verified_rows],
                            "topic_ids": [row.topic_id for row in verified_rows],
                        },
                    )
                )
                if verified_accepted:
                    evidence.append(EVIDENCE_VERIFIED_COMPLETION)
            if claim_present and not legacy_present and not verified_present:
                provenance.append(
                    EvidenceProvenance(
                        source="PRIOR_KNOWLEDGE_CLAIM",
                        accepted=False,
                        reason="prior_knowledge_claim_is_not_coverage",
                        details={
                            "event_ids": [
                                row.event_id for row in claims_by_canonical[cid]
                            ],
                        },
                    )
                )

            eligibility, reasoning = _classify_eligibility(
                legacy_accepted=legacy_accepted,
                verified_accepted=verified_accepted,
                ambiguous_activity=ambiguous,
            )

            verdicts.append(
                CanonicalCoverageVerdict(
                    canonical_id=cid,
                    curriculum_version=canonical.curriculum_version,
                    title=canonical.title,
                    legacy_completion_present=legacy_present,
                    legacy_completion_accepted=legacy_accepted,
                    verified_completion_present=verified_present,
                    verified_completion_accepted=verified_accepted,
                    mapping_status=mapping_status,
                    evidence_sources=tuple(evidence),
                    eligibility=eligibility,
                    reasoning=reasoning,
                    provenance=tuple(provenance),
                )
            )

        unmapped = tuple(unmapped_progress + unmapped_events)
        summary = {
            CATEGORY_CONFIRMED_COVERED: 0,
            CATEGORY_HISTORICALLY_COMPLETED: 0,
            CATEGORY_AMBIGUOUS_HISTORICAL_ACTIVITY: 0,
            CATEGORY_NOT_COVERED: 0,
            "unmapped_historical_activity": len(unmapped),
        }
        for verdict in verdicts:
            summary[verdict.eligibility] = summary.get(verdict.eligibility, 0) + 1

        return LearnerCoverageReconciliation(
            user_id=user_id,
            user_email=email,
            curriculum_version=curriculum_version,
            canonical_verdicts=tuple(verdicts),
            unmapped_activity=unmapped,
            summary=summary,
        )

    @staticmethod
    def _resolve_event_topic(*, token: str, curriculum_identity: str):
        version = (curriculum_identity or "").strip() or ACTIVE_CS1_CURRICULUM_VERSION
        for source_system in (SOURCE_STUDY_EVENT, SOURCE_PUBLISHED_CONTENT):
            resolved = CurriculumIdentityService.resolve(
                source_system=source_system,
                source_id=token,
                source_version=version,
            )
            if resolved is not None:
                return resolved
        # Fall back to active CS1 version when event curriculum_identity differs
        # but published ids match the active map (shadow diagnostic only).
        if version != ACTIVE_CS1_CURRICULUM_VERSION:
            for source_system in (SOURCE_STUDY_EVENT, SOURCE_PUBLISHED_CONTENT):
                resolved = CurriculumIdentityService.resolve(
                    source_system=source_system,
                    source_id=token,
                    source_version=ACTIVE_CS1_CURRICULUM_VERSION,
                )
                if resolved is not None:
                    return resolved
        return None

    @staticmethod
    def reconcile_accounts(
        emails: list[str] | tuple[str, ...] | None = None,
        *,
        curriculum_version: str = ACTIVE_CS1_CURRICULUM_VERSION,
    ) -> list[LearnerCoverageReconciliation]:
        """Reconcile named accounts (or all users with any progress/events)."""
        users: list[User]
        if emails:
            wanted = {e.strip().lower() for e in emails if e and e.strip()}
            users = [
                u
                for u in User.query.order_by(User.id).all()
                if (u.email or "").strip().lower() in wanted
            ]
        else:
            progress_user_ids = {
                row.user_id
                for row in TopicProgress.query.with_entities(
                    TopicProgress.user_id
                ).distinct()
            }
            event_user_ids = {
                row.user_id
                for row in RuntimeEducationalEvent.query.with_entities(
                    RuntimeEducationalEvent.user_id
                ).distinct()
            }
            relevant = progress_user_ids | event_user_ids
            # Always include founder-shaped empty accounts when named elsewhere;
            # for the default path include all users that have history, plus any
            # user with Founder/admin-like emails handled by the CLI.
            users = [
                u
                for u in User.query.order_by(User.id).all()
                if u.id in relevant
            ]

        return [
            CoverageReconciliationService.reconcile_learner(
                user.id,
                curriculum_version=curriculum_version,
            )
            for user in users
        ]

    @staticmethod
    def format_report(
        results: (
            list[LearnerCoverageReconciliation]
            | tuple[LearnerCoverageReconciliation, ...]
        ),
    ) -> str:
        """Render a human-readable shadow report (no live behaviour change)."""
        lines: list[str] = []
        lines.append("Coverage reconciliation shadow report")
        lines.append("=" * 72)
        lines.append(
            "Interpretive eligibility report. Live Study / Stats / Journey / "
            "Settings coverage displays consume the same dual-source rules via "
            "display_coverage / coverage_for_learner."
        )
        lines.append("")

        for result in results:
            lines.append("-" * 72)
            lines.append(
                f"Account: {result.user_email or '(no email)'} "
                f"(user_id={result.user_id})"
            )
            lines.append(f"Curriculum version: {result.curriculum_version}")
            lines.append(f"Summary: {result.summary}")
            lines.append("")
            lines.append(
                f"{'Title':<58} {'Legacy':<8} {'Verified':<8} "
                f"{'Map':<12} {'Eligibility'}"
            )
            lines.append("-" * 120)
            for v in result.canonical_verdicts:
                title = (v.title[:55] + "...") if len(v.title) > 58 else v.title
                legacy = (
                    "Y/acc"
                    if v.legacy_completion_accepted
                    else ("Y/rej" if v.legacy_completion_present else "N")
                )
                verified = "Y" if v.verified_completion_accepted else "N"
                mapping = v.mapping_status or "-"
                lines.append(
                    f"{title:<58} {legacy:<8} {verified:<8} "
                    f"{mapping:<12} {v.eligibility}"
                )
                lines.append(f"  reasoning: {v.reasoning}")
                if v.evidence_sources:
                    lines.append(
                        f"  evidence_sources: {', '.join(v.evidence_sources)}"
                    )
                for prov in v.provenance:
                    lines.append(
                        f"  provenance[{prov.source}]: accepted={prov.accepted} "
                        f"reason={prov.reason} details={prov.details}"
                    )
            if result.unmapped_activity:
                lines.append("")
                lines.append("Unmapped / orphan historical activity:")
                for item in result.unmapped_activity:
                    lines.append(
                        f"  - kind={item.kind} source={item.source_system}:"
                        f"{item.source_id} map={item.mapping_status} "
                        f"-> {item.eligibility}"
                    )
                    lines.append(f"    reasoning: {item.reasoning}")
                    if item.details:
                        lines.append(f"    details: {item.details}")
            lines.append("")
        return "\n".join(lines)
