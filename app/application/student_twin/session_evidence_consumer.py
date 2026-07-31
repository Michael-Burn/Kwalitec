"""Student Digital Twin — consumer of Accepted Educational+ evidence (SDT-004).

The Twin observes. It does not evaluate evidence.
EducationalEvidenceAuthority remains the sole Evidence Authority.

Consumption rules (EV-001A / EIP-002 / SR-001A P5):
- Consume only when Authority sets ``may_update_twin=True``
- Ignore Rejected, Behavioural-only, Informational packages
- Map only Educational+ observations into Twin EvidenceEvents
- Update Estimated Knowledge / Estimated Mastery deterministically
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.learning_session.dto.candidate_observation import (
    TYPE_CEILING_GRADE,
    CandidateObservation,
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
    EvidenceLifecycleState,
    SessionEvidencePackage,
)
from app.application.student_twin.daily_loop_codec import (
    decode_daily_loop_twin,
    encode_daily_loop_twin,
)
from app.application.student_twin.dto.twin_consumption_result import (
    TwinConsumptionResult,
)
from app.application.student_twin.exceptions import DuplicateEvidence, EvidenceRejected
from app.application.student_twin.twin_engine import StudentTwinEngine
from app.domain.student_twin.digital_twin import DigitalTwin
from app.domain.student_twin.evidence_event import EvidenceEvent
from app.domain.student_twin.evidence_type import EvidenceType
from app.domain.student_twin.learner import Learner

# Grades that may lawfully inform Twin-owned estimates (Educational+).
_TWIN_GRADES = frozenset({"educational", "mastery", "constitutional"})

# Runtime catalogue types authorised for Twin writers under EIP-002 / EV-001A.
_TWIN_AUTHORISED_TYPES: dict[RuntimeEvidenceType, EvidenceType] = {
    RuntimeEvidenceType.PRACTICE_CORRECT: EvidenceType.PRACTICE_RESULT,
    RuntimeEvidenceType.PRACTICE_INCORRECT: EvidenceType.PRACTICE_RESULT,
    RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS: EvidenceType.ASSESSMENT_OUTCOME,
    RuntimeEvidenceType.QUIZ_RESULTS: EvidenceType.ASSESSMENT_OUTCOME,
    RuntimeEvidenceType.MISSION_ASSESSMENT_RESULTS: EvidenceType.ASSESSMENT_OUTCOME,
    RuntimeEvidenceType.MOCK_EXAMINATION_RESULTS: EvidenceType.ASSESSMENT_OUTCOME,
    RuntimeEvidenceType.OFFICIAL_EXAMINATION_RESULTS: EvidenceType.ASSESSMENT_OUTCOME,
}


class SessionTwinEvidenceConsumer:
    """Apply Authority-Accepted Educational+ packages to the Student Twin.

    Never revalidates grades. Never completes missions. Never advances Progress.
    """

    CONSUMER_ID = "session_twin_evidence_consumer"
    CONSUMER_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        engine: StudentTwinEngine | None = None,
        store: Any | None = None,
        clock: Callable[[], datetime] | None = None,
        id_factory: Callable[[], str] | None = None,
        flag_resolver: Callable[[], Any] | None = None,
    ) -> None:
        self._engine = engine or StudentTwinEngine()
        self._store = store
        self._clock = clock or (lambda: datetime.now(tz=UTC))
        self._id_factory = id_factory or (lambda: uuid4().hex[:12])
        self._flag_resolver = flag_resolver or resolve_v2_feature_flags

    def consume(
        self,
        package: SessionEvidencePackage | dict[str, Any] | None,
    ) -> TwinConsumptionResult:
        """Consume one sitting package when Authority authorises Twin update."""
        if not bool(getattr(self._flag_resolver(), "SR_TWIN_DAILY_LOOP", False)):
            return TwinConsumptionResult.ignored("twin_daily_loop_flag_off")

        resolved = self._resolve_package(package)
        if resolved is None:
            return TwinConsumptionResult.ignored("package_missing")

        validation = resolved.validation
        if validation is None:
            return TwinConsumptionResult.ignored(
                "package_not_validated",
                package_id=resolved.package_id,
                learner_id=resolved.student_id,
            )

        if validation.disposition == EvidenceDisposition.REJECTED:
            return TwinConsumptionResult.ignored(
                "rejected_package",
                package_id=resolved.package_id,
                learner_id=resolved.student_id,
            )

        if not validation.may_update_twin:
            reason = self._ignore_reason(validation.highest_grade, validation.reason)
            return TwinConsumptionResult.ignored(
                reason,
                package_id=resolved.package_id,
                learner_id=resolved.student_id,
            )

        events = self.extract_authorised_events(resolved)
        if not events:
            return TwinConsumptionResult.ignored(
                "no_educational_plus_observations",
                package_id=resolved.package_id,
                learner_id=resolved.student_id,
            )

        twin, status = self._load_or_birth(
            learner_id=resolved.student_id,
            curriculum_identity=resolved.curriculum_identity,
            topic_id=resolved.topic_id,
        )
        ingested = 0
        for event in events:
            try:
                twin = self._engine.ingest_evidence(twin, event)
                ingested += 1
            except DuplicateEvidence:
                continue
            except EvidenceRejected:
                continue

        if ingested == 0:
            return TwinConsumptionResult.ignored(
                "no_new_events_ingested",
                package_id=resolved.package_id,
                learner_id=resolved.student_id,
            )

        status = "active"
        self._persist(twin, status=status)
        knowledge = {
            record.topic_id: round(record.knowledge_score, 6)
            for record in twin.knowledge.topic_records
        }
        mastery = {
            record.topic_id: round(record.mastery_score, 6)
            for record in twin.mastery.topic_records
        }
        return TwinConsumptionResult(
            twin_updated=True,
            reason="accepted_educational_plus_consumed",
            twin_id=twin.twin_id,
            learner_id=twin.learner_id,
            package_id=resolved.package_id,
            events_ingested=ingested,
            twin_status=status,
            estimated_knowledge=knowledge,
            estimated_mastery=mastery,
            overall_knowledge=round(twin.knowledge.overall_score, 6),
            overall_mastery=round(twin.mastery.overall_score, 6),
        )

    def extract_authorised_events(
        self,
        package: SessionEvidencePackage,
    ) -> list[EvidenceEvent]:
        """Map Educational+ candidates to Twin EvidenceEvents.

        Behavioural / Informational observations in the same package are ignored.
        """
        events: list[EvidenceEvent] = []
        topic_fallback = (package.topic_id or "").strip() or None
        for obs in package.observations:
            event = self._observation_to_event(obs, topic_fallback=topic_fallback)
            if event is not None:
                events.append(event)
        return events

    def mark_package_consumed(
        self, package: SessionEvidencePackage
    ) -> SessionEvidencePackage:
        """Advance Accepted package lifecycle to Consumed after Twin write."""
        if package.lifecycle_state in {
            EvidenceLifecycleState.ACCEPTED,
            EvidenceLifecycleState.PERSISTED,
        }:
            return package.with_lifecycle(EvidenceLifecycleState.CONSUMED)
        return package

    def _observation_to_event(
        self,
        obs: CandidateObservation,
        *,
        topic_fallback: str | None,
    ) -> EvidenceEvent | None:
        grade = TYPE_CEILING_GRADE.get(obs.type_id, "informational")
        if grade not in _TWIN_GRADES:
            return None
        twin_type = _TWIN_AUTHORISED_TYPES.get(obs.type_id)
        if twin_type is None:
            return None

        topic_id = (obs.topic_id or "").strip() or topic_fallback
        outcome, score = self._outcome_and_score(obs)
        payload = obs.payload or {}
        metadata = [
            ("runtime_type", obs.type_id.value),
            ("session_id", obs.session_id),
            ("package_provenance", "learning_session_runtime"),
        ]
        if obs.activity_id:
            metadata.append(("activity_id", obs.activity_id))
        if obs.mission_instance_id:
            metadata.append(("mission_instance_id", obs.mission_instance_id))
        source_ref = str(
            payload.get("source_ref")
            or f"ev:{obs.session_id}:{obs.observation_id}"
        )
        return EvidenceEvent.create(
            event_id=f"twin-{obs.observation_id}",
            evidence_type=twin_type,
            occurred_at=obs.recorded_at,
            topic_id=topic_id,
            outcome=outcome,
            score=score,
            source_ref=source_ref,
            metadata=metadata,
        )

    @staticmethod
    def _outcome_and_score(
        obs: CandidateObservation,
    ) -> tuple[str | None, float | None]:
        payload = obs.payload or {}
        if obs.type_id == RuntimeEvidenceType.PRACTICE_CORRECT:
            return "correct", 1.0
        if obs.type_id == RuntimeEvidenceType.PRACTICE_INCORRECT:
            return "incorrect", 0.0
        raw_score = payload.get("score")
        if isinstance(raw_score, int | float) and not isinstance(raw_score, bool):
            score = max(0.0, min(1.0, float(raw_score)))
        elif payload.get("accuracy") is not None:
            try:
                accuracy = float(payload["accuracy"])
            except (TypeError, ValueError):
                accuracy = None
            else:
                score = (
                    accuracy / 100.0
                    if accuracy > 1.0
                    else max(0.0, min(1.0, accuracy))
                )
        else:
            scored = payload.get("scored_correct")
            if scored is True:
                score = 1.0
            elif scored is False:
                score = 0.0
            else:
                score = None
        outcome = payload.get("outcome")
        if isinstance(outcome, str) and outcome.strip():
            return outcome.strip().lower(), score
        if score is None:
            return None, None
        if score >= 0.6:
            return "correct", score
        if score <= 0.4:
            return "incorrect", score
        return "partial", score

    def _load_or_birth(
        self,
        *,
        learner_id: str,
        curriculum_identity: str,
        topic_id: str,
    ) -> tuple[DigitalTwin, str]:
        subject = _subject_from_curriculum(curriculum_identity)
        if self._store is not None:
            raw = self._store.load_twin(learner_id=learner_id, subject_code=subject)
            decoded = decode_daily_loop_twin(raw, engine=self._engine)
            if decoded is not None:
                return decoded
        twin_id = f"twin-dl-{learner_id}"
        if subject:
            twin_id = f"twin-dl-{learner_id}-{subject}"
        twin = self._engine.create_twin(
            Learner.create(learner_id),
            twin_id=twin_id,
            subject_code=subject,
        )
        # Birth Twin is Initialised; first lawful evidence activates it.
        _ = topic_id  # retained for future topic-scoped birth provenance
        self._persist(twin, status="initialised")
        return twin, "initialised"

    def _persist(self, twin: DigitalTwin, *, status: str) -> None:
        if self._store is None:
            return
        document = encode_daily_loop_twin(twin, status=status)
        self._store.save_twin(
            learner_id=twin.learner_id,
            subject_code=twin.identity.subject_code,
            document=document,
        )

    @staticmethod
    def _resolve_package(
        package: SessionEvidencePackage | dict[str, Any] | None,
    ) -> SessionEvidencePackage | None:
        if package is None:
            return None
        if isinstance(package, SessionEvidencePackage):
            return package
        if isinstance(package, dict):
            return SessionEvidencePackage.from_opaque(package)
        return None

    @staticmethod
    def _ignore_reason(highest_grade: str, authority_reason: str) -> str:
        grade = (highest_grade or "").strip().lower()
        if grade in {"informational"}:
            return "informational_package_ignored"
        if grade in {"behavioural"}:
            return "behavioural_package_ignored"
        if authority_reason:
            return f"twin_not_authorised:{authority_reason}"
        return "twin_not_authorised"


def _subject_from_curriculum(curriculum_identity: str) -> str | None:
    raw = (curriculum_identity or "").strip()
    if not raw:
        return None
    # Common forms: "CS1:edition" / "CS1"
    head = raw.split(":", 1)[0].strip()
    return head or None
