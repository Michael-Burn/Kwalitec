"""Evidence packaging application service (deterministic; no Twin / Reasoning)."""

from __future__ import annotations

from collections.abc import Callable, Mapping, Sequence
from datetime import datetime
from typing import Any

from application.assessment.evidence.dto import EvidencePackagingResultDTO
from application.assessment.evidence.mapper import EvidenceMapper
from application.assessment.ports.repositories import (
    AssessmentInstrumentRepository,
    AssessmentObservationRepository,
    AssessmentResultRepository,
    AssessmentSessionRepository,
    EvidenceBundleRepository,
)
from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.entities.assessment_result import AssessmentResult
from domain.assessment.factories import AssessmentResultFactory
from domain.assessment.packaging.ids import sequential_id_factory
from domain.assessment.packaging.packager import EvidencePackager
from domain.assessment.value_objects.ids import (
    InstrumentId,
    ResultId,
    SessionId,
)


class EvidencePackagingService:
    """Package session observations into an EvidenceBundle + AssessmentResult.

    Exposes packaged evidence for future AP-001 consumption. Does not invoke
    AP-001, StudentReasoningService, Twin writers, Mission, or Tutor.
    """

    def __init__(
        self,
        *,
        sessions: AssessmentSessionRepository | None = None,
        observations: AssessmentObservationRepository | None = None,
        results: AssessmentResultRepository | None = None,
        instruments: AssessmentInstrumentRepository | None = None,
        evidence_bundles: EvidenceBundleRepository | None = None,
        id_factory: Callable[[str], str] | None = None,
        packager: EvidencePackager | None = None,
    ) -> None:
        self._sessions = sessions
        self._observations = observations
        self._results = results
        self._instruments = instruments
        self._evidence_bundles = evidence_bundles
        self._id_factory = id_factory or sequential_id_factory()
        self._packager = packager or EvidencePackager(id_factory=self._id_factory)
        self._mapper = EvidenceMapper()

    def package_session(
        self,
        session_id: str,
        *,
        result_id: str | None = None,
        collected_at: datetime | None = None,
        extra: Mapping[str, Any] | None = None,
    ) -> EvidencePackagingResultDTO:
        """Load session observations and package evidence (persists when ports set)."""
        if self._sessions is None or self._observations is None:
            raise RuntimeError(
                "EvidencePackagingService.package_session requires "
                "sessions and observations ports"
            )
        sid = SessionId(session_id)
        session = self._sessions.get(sid)
        if session is None:
            raise LookupError(f"session not found: {session_id}")
        observations = self._observations.list_by_session(sid)
        instrument = None
        if self._instruments is not None:
            instrument = self._instruments.get(session.instrument_id)

        learning_objectives = ()
        if instrument is not None:
            learning_objectives = instrument.learning_objectives

        resolved_result_id = result_id or self._id_factory("result")
        packaging = self._packager.package(
            observations,
            session_id=sid,
            result_id=resolved_result_id,
            bundle_id=self._id_factory("evidence-bundle"),
            instrument_id=session.instrument_id,
            purpose=session.purpose.value,
            assessment_type=session.assessment_type.value,
            student_id=session.student_id,
            learning_objectives=learning_objectives,
            expected_question_count=len(session.questions),
            extra=extra,
            collected_at=collected_at,
        )
        result = AssessmentResultFactory.create(
            result_id=ResultId(resolved_result_id),
            session_id=sid,
            observation_ids=packaging.bundle.observation_ids(),
            correctness_counts=packaging.bundle.summary.correctness_count_map(),
            evidence_strength=packaging.bundle.strength,
            evidence_bundle=packaging.bundle,
        )
        if self._results is not None:
            self._results.save(result)
        if self._evidence_bundles is not None:
            self._evidence_bundles.save(packaging.bundle)
        return self._mapper.to_result_dto(packaging)

    def package_observations(
        self,
        observations: Sequence[AssessmentObservation],
        *,
        session_id: str,
        result_id: str | None = None,
        instrument_id: str | None = None,
        purpose: str | None = None,
        assessment_type: str | None = None,
        student_id: str | None = None,
        expected_question_count: int | None = None,
        learning_objectives: Sequence[Any] = (),
        concepts: Sequence[Any] = (),
        collected_at: datetime | None = None,
        extra: Mapping[str, Any] | None = None,
        persist_result: bool = False,
    ) -> tuple[AssessmentResult, EvidencePackagingResultDTO]:
        """Package an explicit observation sequence into result + DTO."""
        resolved_result_id = result_id or self._id_factory("result")
        packaging = self._packager.package(
            observations,
            session_id=session_id,
            result_id=resolved_result_id,
            bundle_id=self._id_factory("evidence-bundle"),
            instrument_id=(
                InstrumentId(instrument_id) if instrument_id is not None else None
            ),
            purpose=purpose,
            assessment_type=assessment_type,
            student_id=student_id,
            learning_objectives=learning_objectives,
            concepts=concepts,
            expected_question_count=expected_question_count,
            extra=extra,
            collected_at=collected_at,
        )
        result = AssessmentResultFactory.create(
            result_id=ResultId(resolved_result_id),
            session_id=SessionId(session_id),
            observation_ids=packaging.bundle.observation_ids(),
            correctness_counts=packaging.bundle.summary.correctness_count_map(),
            evidence_strength=packaging.bundle.strength,
            evidence_bundle=packaging.bundle,
        )
        if persist_result and self._results is not None:
            self._results.save(result)
        if persist_result and self._evidence_bundles is not None:
            self._evidence_bundles.save(packaging.bundle)
        return result, self._mapper.to_result_dto(packaging)

    def export_for_ap001(
        self, result: AssessmentResult
    ) -> EvidencePackagingResultDTO | None:
        """Expose packaged evidence from an AssessmentResult without invoking AP-001."""
        bundle = result.packaged_evidence()
        if bundle is None:
            return None
        from domain.assessment.evidence.models import EvidencePackagingResult

        packaging = EvidencePackagingResult(
            bundle=bundle,
            result_id=result.result_id,
            validated=True,
        )
        return self._mapper.to_result_dto(packaging)
