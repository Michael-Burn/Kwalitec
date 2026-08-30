"""Policy V1: evidence-backed revision-block selection (ADR-027 Phase 3).

On review days (continuous exam-proximity cadence), scores every revision-mode
package for the subject by average Twin Estimated Knowledge over covered
return_targets with evidence_count >= 3. Lowest score wins → ADAPTIVE.

When it is not a review day, or no package meets the evidence bar, defers to
Policy V0 and records SAFE_FALLBACK (or BLOCKED) exactly as V0 does.

Does not import Runtime A PlanningService. Reads EK only via LearnerTwinQueryPort.
Does not write Study Progress.
"""

from __future__ import annotations

import json
import uuid
from dataclasses import replace
from datetime import date
from typing import TYPE_CHECKING, Any

from app.application.adaptive_decision.policy_v0 import (
    PolicyV0AdaptiveDecisionEngine,
)
from app.application.adaptive_decision.review_cadence import is_review_day
from app.application.adaptive_decision.types import (
    INTENT_DAILY_SITTING,
    POLICY_V1_ID,
    POLICY_V1_MIN_EVIDENCE,
    REASON_POLICY_V1_BLOCK_WEAKNESS,
    REASON_POLICY_V1_INSUFFICIENT_EVIDENCE,
    REASON_POLICY_V1_NOT_REVIEW_DAY,
    DailySittingRequest,
    DecisionOutcome,
    SittingDecision,
)
from app.application.educational_packages.loader import (
    find_package_by_id,
    packages_for_subject,
)
from app.domain.educational_runtime_engine.events import EducationalEventType
from app.models.educational_runtime_engine import RuntimeEducationalEvent

if TYPE_CHECKING:
    from app.application.educational_packages.models import (
        CertifiedEducationalPackage,
    )
    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
    )
    from app.application.student_twin.query import (
        LearnerKnowledgeSnapshot,
        LearnerTwinQueryPort,
        TopicKnowledgeFact,
    )


def _new_decision_id() -> str:
    return f"dec_{uuid.uuid4().hex[:16]}"


def block_weakness_score(
    *,
    return_targets: tuple[str, ...] | list[str],
    facts_by_topic: dict[str, TopicKnowledgeFact],
    covered: set[str] | frozenset[str],
    min_evidence: int = POLICY_V1_MIN_EVIDENCE,
) -> float | None:
    """Mean EK over covered targets with enough Twin evidence.

    Returns None when no target meets the bar (package is unscorable).
    """
    eligible: list[float] = []
    for tid in return_targets:
        key = (tid or "").strip()
        if not key or key not in covered:
            continue
        fact = facts_by_topic.get(key)
        if fact is None:
            continue
        if not fact.has_estimated_knowledge:
            continue
        if fact.evidence_count < min_evidence:
            continue
        if fact.estimated_knowledge is None:
            continue
        eligible.append(float(fact.estimated_knowledge))
    if not eligible:
        return None
    return sum(eligible) / len(eligible)


def select_weakest_revision_package(
    *,
    packages: tuple[CertifiedEducationalPackage, ...]
    | list[CertifiedEducationalPackage],
    snapshot: LearnerKnowledgeSnapshot,
    twin: LearnerTwinQueryPort,
    user_id: int,
    subject_code: str,
    min_evidence: int = POLICY_V1_MIN_EVIDENCE,
) -> tuple[CertifiedEducationalPackage, float, tuple[str, ...]] | None:
    """Pick the revision package with the lowest block weakness score.

    Coverage is checked via ``twin.topic_covered`` (Study Progress fact through
    the Twin port). EK and evidence_count come from the snapshot, filtered
    locally by each package's return_targets.
    """
    facts_by_topic = {f.topic_id: f for f in snapshot.topics}
    best: tuple[CertifiedEducationalPackage, float, tuple[str, ...]] | None = None
    for pack in packages:
        targets = tuple(pack.return_targets or ())
        if not targets:
            continue
        covered = {
            t
            for t in targets
            if twin.topic_covered(
                user_id=user_id, subject_code=subject_code, topic_id=t
            )
        }
        score = block_weakness_score(
            return_targets=targets,
            facts_by_topic=facts_by_topic,
            covered=covered,
            min_evidence=min_evidence,
        )
        if score is None:
            continue
        eligible_ids = tuple(
            t
            for t in targets
            if t in covered
            and (fact := facts_by_topic.get(t)) is not None
            and fact.has_estimated_knowledge
            and fact.evidence_count >= min_evidence
            and fact.estimated_knowledge is not None
        )
        if best is None or score < best[1] or (
            score == best[1] and pack.package_id < best[0].package_id
        ):
            best = (pack, score, eligible_ids)
    return best


class PolicyV1AdaptiveDecisionEngine:
    """AdaptiveDecisionEngine: review-day block weakness, else Policy V0."""

    def __init__(
        self,
        *,
        runtime: EducationalRuntimeEngineService | None = None,
        twin: LearnerTwinQueryPort,
        v0: PolicyV0AdaptiveDecisionEngine | None = None,
    ) -> None:
        if runtime is None:
            from app.application.educational_runtime_engine.service import (
                EducationalRuntimeEngineService,
            )

            runtime = EducationalRuntimeEngineService()
        self._runtime = runtime
        self._twin = twin
        self._v0 = v0 or PolicyV0AdaptiveDecisionEngine(runtime=runtime)

    def decide_daily_sitting(
        self, request: DailySittingRequest
    ) -> SittingDecision:
        """Review-day adaptive block pick, otherwise exact Policy V0 behaviour."""
        days_remaining = _days_remaining(
            exam_date=request.exam_date, mission_date=request.mission_date
        )
        topics_since = self._topics_since_last_review(request)
        review = is_review_day(
            days_remaining=days_remaining,
            topics_since_last_review=topics_since,
        )
        if not review:
            decision = self._v0.decide_daily_sitting(request)
            return _retag_v0_fallback(
                decision,
                reason=REASON_POLICY_V1_NOT_REVIEW_DAY,
                selection_trace_extra={
                    "policy_v1_review_day": False,
                    "days_remaining": days_remaining,
                    "topics_since_last_review": topics_since,
                },
            )

        selected = self._try_select_revision_block(request)
        if selected is None:
            decision = self._v0.decide_daily_sitting(request)
            return _retag_v0_fallback(
                decision,
                reason=REASON_POLICY_V1_INSUFFICIENT_EVIDENCE,
                selection_trace_extra={
                    "policy_v1_review_day": True,
                    "days_remaining": days_remaining,
                    "topics_since_last_review": topics_since,
                    "adaptive_attempted": True,
                    "adaptive_selected": False,
                },
            )

        pack, score, eligible = selected
        carrier = self._v0.decide_daily_sitting(request)
        if carrier.outcome == DecisionOutcome.BLOCKED:
            # No materialisable sitting scaffold; honest fallback to V0 block.
            return _retag_v0_fallback(
                carrier,
                reason=REASON_POLICY_V1_INSUFFICIENT_EVIDENCE,
                selection_trace_extra={
                    "policy_v1_review_day": True,
                    "days_remaining": days_remaining,
                    "topics_since_last_review": topics_since,
                    "adaptive_attempted": True,
                    "adaptive_selected": False,
                    "blocked_carrier": True,
                    "would_have_selected_package_id": pack.package_id,
                    "would_have_weakness_score": score,
                },
            )

        decision_id = _new_decision_id()
        trace = dict(carrier.selection_trace or {})
        trace.update(
            {
                "adaptive_attempted": True,
                "adaptive_selected": True,
                "policy_v1_review_day": True,
                "days_remaining": days_remaining,
                "topics_since_last_review": topics_since,
                "weakness_score": score,
                "eligible_return_targets": list(eligible),
                "selected_package_id": pack.package_id,
                "return_targets": list(pack.return_targets or ()),
            }
        )
        return SittingDecision(
            outcome=DecisionOutcome.ADAPTIVE,
            intent=INTENT_DAILY_SITTING,
            policy_id=POLICY_V1_ID,
            decision_id=decision_id,
            topic_id=carrier.topic_id,
            topic_code=carrier.topic_code,
            educational_package_id=pack.package_id,
            educational_package_mode=(pack.mode or "revision").strip().lower(),
            certified_mission_id=carrier.certified_mission_id,
            objective_ids=tuple(carrier.objective_ids),
            reason_codes=(REASON_POLICY_V1_BLOCK_WEAKNESS,),
            block_reason=None,
            selection_trace=trace,
            template_id=carrier.template_id,
            educational_campaign_day=pack.campaign_day or None,
            selection_reasons=tuple(carrier.selection_reasons),
            curriculum_provenance=carrier.curriculum_provenance,
            calibration_notes=tuple(carrier.calibration_notes),
            enrolment_id=carrier.enrolment_id,
            plan_instance_id=carrier.plan_instance_id,
            curriculum_identity=carrier.curriculum_identity
            or request.curriculum_identity,
            withhold_message=None,
        )

    def _try_select_revision_block(
        self, request: DailySittingRequest
    ) -> tuple[CertifiedEducationalPackage, float, tuple[str, ...]] | None:
        packs = packages_for_subject(request.subject_code, mode="revision")
        if not packs:
            return None
        snapshot = self._twin.knowledge_snapshot(
            user_id=request.user_id, subject_code=request.subject_code
        )
        return select_weakest_revision_package(
            packages=packs,
            snapshot=snapshot,
            twin=self._twin,
            user_id=request.user_id,
            subject_code=request.subject_code,
        )

    def _topics_since_last_review(self, request: DailySittingRequest) -> int:
        """Count Runtime C topic completions since last revision-mode sitting.

        Uses Runtime C educational events only (not Study Progress ORM writes).
        """
        identity = (request.curriculum_identity or "").strip()
        if not identity:
            try:
                enrolment = self._runtime._require_enrolment(
                    request.user_id, request.subject_code
                )
                identity = enrolment.curriculum_identity or ""
            except Exception:
                return 0
        if not identity:
            return 0

        mission_rows = (
            RuntimeEducationalEvent.query.filter_by(
                user_id=request.user_id,
                curriculum_identity=identity,
                event_type=EducationalEventType.MISSION_COMPLETED.value,
            )
            .order_by(RuntimeEducationalEvent.id.asc())
            .all()
        )
        last_revision_event_id: int | None = None
        for row in mission_rows:
            payload = _payload(row)
            pid = str(payload.get("educational_package_id") or "").strip()
            if not pid:
                continue
            pack = find_package_by_id(pid)
            if pack is not None and (pack.mode or "").strip().lower() == "revision":
                last_revision_event_id = int(row.id)

        topic_rows = (
            RuntimeEducationalEvent.query.filter_by(
                user_id=request.user_id,
                curriculum_identity=identity,
                event_type=EducationalEventType.TOPIC_COMPLETED.value,
            )
            .order_by(RuntimeEducationalEvent.id.asc())
            .all()
        )
        seen: set[str] = set()
        count = 0
        for row in topic_rows:
            if (
                last_revision_event_id is not None
                and int(row.id) <= last_revision_event_id
            ):
                continue
            tid = (row.topic_id or "").strip()
            if not tid or tid in seen:
                continue
            seen.add(tid)
            count += 1
        return count


def _days_remaining(*, exam_date: date | None, mission_date: date) -> int | None:
    if exam_date is None:
        return None
    return (exam_date - mission_date).days


def _payload(row: RuntimeEducationalEvent) -> dict[str, Any]:
    try:
        raw = json.loads(row.payload_json or "{}")
    except json.JSONDecodeError:
        return {}
    return raw if isinstance(raw, dict) else {}


def _retag_v0_fallback(
    decision: SittingDecision,
    *,
    reason: str,
    selection_trace_extra: dict[str, Any],
) -> SittingDecision:
    """Keep V0 outcome/fields; stamp policy_v1 id and fallback reason honesty."""
    trace = dict(decision.selection_trace or {})
    trace.update(selection_trace_extra)
    reasons = tuple(decision.reason_codes) + (reason,)
    return replace(
        decision,
        policy_id=POLICY_V1_ID,
        reason_codes=reasons,
        selection_trace=trace,
    )
