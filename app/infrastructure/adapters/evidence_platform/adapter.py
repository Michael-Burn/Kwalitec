"""Evidence Platform Adapter — MS-006 E0/E1/E2/E3/E4/E5 surface.

Implements LearningEvidenceContract / EvidenceAdapter. E1 wires
EvidenceFactory (collector → assembler → validator) for deterministic
evidence collection. E2 wires ExperimentFramework for deterministic
experiment assignment. E3 wires PolicyEvaluationFactory for deterministic
policy evaluation. E4 wires AnalyticsEngine and EvidenceProjector for
deterministic analytics aggregation and governance projection. E5 Shadow
Validation is wired separately via EvidenceShadowValidator. No
persistence, policy promotion, or educational writes.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any

from app.infrastructure.adapters.evidence_platform.advisory_assembler import (
    EvidenceAdvisoryAssembler,
    build_evidence_advisory_assembler,
)
from app.infrastructure.adapters.evidence_platform.aggregator import (
    AnalyticsValidationError,
)
from app.infrastructure.adapters.evidence_platform.analytics_engine import (
    AnalyticsEngine,
    build_analytics_engine,
)
from app.infrastructure.adapters.evidence_platform.assembler import EvidenceAssembler
from app.infrastructure.adapters.evidence_platform.collector import EvidenceCollector
from app.infrastructure.adapters.evidence_platform.contracts import (
    ANALYTICS_AUDIENCE_GOVERNANCE,
    AUTHORITY_EVIDENCE_PLATFORM,
    AVAILABILITY_UNAVAILABLE,
    EVIDENCE_VERSION_E1,
    AnalyticsSummary,
    EvidenceAdvisory,
    EvidenceContext,
    EvidenceFactualSummary,
    EvidenceProjection,
    EvidenceQuality,
    EvidenceRecord,
    EvidenceResult,
    ExperimentDefinition,
    ExperimentObservation,
    ObservedEvent,
    PolicyDefinition,
    PolicyEvaluation,
)
from app.infrastructure.adapters.evidence_platform.evaluation_factory import (
    PolicyEvaluationFactory,
    build_policy_evaluation_factory,
)
from app.infrastructure.adapters.evidence_platform.evaluation_validator import (
    EvaluationValidationError,
)
from app.infrastructure.adapters.evidence_platform.experiment_validator import (
    ExperimentValidationError,
)
from app.infrastructure.adapters.evidence_platform.factory import (
    EvidenceFactory,
    build_evidence_factory,
)
from app.infrastructure.adapters.evidence_platform.factual_query import (
    REPORTING_PERIOD_THIS_WEEK,
    build_factual_summary,
)
from app.infrastructure.adapters.evidence_platform.framework import (
    ExperimentFramework,
    build_experiment_framework,
)
from app.infrastructure.adapters.evidence_platform.projector import (
    EvidenceGovernanceProjectionPort,
    EvidenceProjector,
    build_evidence_projection_port,
    build_evidence_projector,
)
from app.infrastructure.adapters.evidence_platform.validation import (
    EvidenceValidationError,
    EvidenceValidator,
)


class EvidencePlatformAdapter:
    """Evidence Platform Adapter — E1–E4 behind flag.

    When constructed behind ``ENABLE_EVIDENCE_PLATFORM``, collects observed
    events into immutable EvidenceRecords, assigns them to registered
    experiments, evaluates policies against ExperimentObservations, and
    aggregates governance-facing analytics projections. Does not persist,
    promote policies, or mutate upstream educational state.

    P2-MS008 adds a process-local observational read buffer so
    ``query_factual_summary`` can return previously collected facts through
    the public EvidenceReadPort without repositories or educational writes.

    P2-MS009 adds ``query_advisory`` (EvidenceAdvisoryPort) so Runtime A may
    read factual advisory inputs without repositories or educational writes.
    """

    ADAPTER_ID = "evidence_platform"
    ADAPTER_VERSION = "1.0.0-e5"
    EVIDENCE_VERSION = EVIDENCE_VERSION_E1
    PORT_ID = "evidence_advisory_port"
    # Bounded observational buffer — not durable persistence.
    OBSERVATION_BUFFER_LIMIT = 10_000

    def __init__(
        self,
        *,
        factory: EvidenceFactory | None = None,
        collector: EvidenceCollector | None = None,
        assembler: EvidenceAssembler | None = None,
        validator: EvidenceValidator | None = None,
        experiment_framework: ExperimentFramework | None = None,
        policy_evaluation_factory: PolicyEvaluationFactory | None = None,
        analytics_engine: AnalyticsEngine | None = None,
        evidence_projector: EvidenceProjector | None = None,
        evidence_projection_port: EvidenceGovernanceProjectionPort | None = None,
        advisory_assembler: EvidenceAdvisoryAssembler | None = None,
        observation_buffer_limit: int | None = None,
    ) -> None:
        self._validator = validator or EvidenceValidator()
        self._collector = collector or EvidenceCollector(validator=self._validator)
        self._assembler = assembler or EvidenceAssembler(validator=self._validator)
        self._factory = factory or EvidenceFactory(
            collector=self._collector,
            assembler=self._assembler,
            validator=self._validator,
        )
        self._experiment_framework = experiment_framework
        self._policy_evaluation_factory = policy_evaluation_factory
        self._analytics_engine = analytics_engine
        self._evidence_projector = evidence_projector
        self._evidence_projection_port = evidence_projection_port
        self._advisory_assembler = (
            advisory_assembler or EvidenceAdvisoryAssembler(enabled=True)
        )
        self._available = True
        limit = (
            self.OBSERVATION_BUFFER_LIMIT
            if observation_buffer_limit is None
            else max(0, int(observation_buffer_limit))
        )
        self._observation_buffer_limit = limit
        self._observation_buffer: list[EvidenceRecord] = []

    @property
    def adapter_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def adapter_version(self) -> str:
        return self.ADAPTER_VERSION

    @property
    def port_id(self) -> str:
        """EvidenceAdvisoryPort identity (P2-MS009)."""
        return self.PORT_ID

    @property
    def factory(self) -> EvidenceFactory:
        return self._factory

    @property
    def collector(self) -> EvidenceCollector:
        return self._collector

    @property
    def assembler(self) -> EvidenceAssembler:
        return self._assembler

    @property
    def validator(self) -> EvidenceValidator:
        return self._validator

    @property
    def experiment_framework(self) -> ExperimentFramework | None:
        return self._experiment_framework

    @property
    def policy_evaluation_factory(self) -> PolicyEvaluationFactory | None:
        return self._policy_evaluation_factory

    @property
    def analytics_engine(self) -> AnalyticsEngine | None:
        return self._analytics_engine

    @property
    def evidence_projector(self) -> EvidenceProjector | None:
        return self._evidence_projector

    @property
    def evidence_projection_port(self) -> EvidenceGovernanceProjectionPort | None:
        return self._evidence_projection_port

    @property
    def advisory_assembler(self) -> EvidenceAdvisoryAssembler:
        return self._advisory_assembler

    def is_available(self) -> bool:
        return self._available

    def observe(self, context: EvidenceContext) -> EvidenceRecord:
        """Project an EvidenceContext into an immutable EvidenceRecord (E1 intake)."""
        if not isinstance(context, EvidenceContext):
            raise TypeError("context must be an EvidenceContext")
        return self._factory.create_from_context(context)

    def collect_event(self, event: ObservedEvent) -> EvidenceRecord:
        """Collect an ObservedEvent into an immutable EvidenceRecord."""
        if not isinstance(event, ObservedEvent):
            raise TypeError("event must be an ObservedEvent")
        record = self._factory.create_from_observed_event(event)
        self._retain_observation(record)
        return record

    def query_factual_summary(
        self,
        student_id: str,
        *,
        reporting_period: str = REPORTING_PERIOD_THIS_WEEK,
        as_of: str | None = None,
        evidence_records: Sequence[EvidenceRecord] | None = None,
    ) -> EvidenceResult:
        """Public Evidence read — factual observation summary for Experience.

        Uses caller-supplied ``evidence_records`` when provided; otherwise
        reads the process-local observational buffer populated by
        ``collect_event``. Never scores, predicts, or writes educational state.
        """
        sid = (student_id or "").strip()
        if not sid:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="student_id must be a non-empty string",
            )
        if as_of is not None and not isinstance(as_of, str):
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="as_of must be an ISO string or None",
            )
        if evidence_records is not None:
            for record in evidence_records:
                if not isinstance(record, EvidenceRecord):
                    return EvidenceResult(
                        ok=False,
                        error_code="INVALID_STATE",
                        message=(
                            "evidence_records must contain EvidenceRecord values"
                        ),
                    )
            source = tuple(evidence_records)
        else:
            source = tuple(self._observation_buffer)
        try:
            summary = build_factual_summary(
                sid,
                source,
                reporting_period=reporting_period,
                as_of=as_of,
            )
            return EvidenceResult(ok=True, value=summary)
        except (TypeError, ValueError) as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )

    def query_advisory(
        self,
        student_id: str,
        *,
        reporting_period: str = REPORTING_PERIOD_THIS_WEEK,
        as_of: str | None = None,
        evidence_records: Sequence[EvidenceRecord] | None = None,
    ) -> EvidenceResult:
        """Public Evidence advisory read for Runtime A (EvidenceAdvisoryPort).

        Builds a factual summary then projects it into EvidenceAdvisory.
        Never scores, predicts, recommends, or writes educational state.
        """
        summary_result = self.query_factual_summary(
            student_id,
            reporting_period=reporting_period,
            as_of=as_of,
            evidence_records=evidence_records,
        )
        if not summary_result.ok:
            return summary_result
        summary = summary_result.value
        if not isinstance(summary, EvidenceFactualSummary):
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="factual summary unavailable for advisory assembly",
            )
        try:
            advisory = self._advisory_assembler.assemble(
                summary, generated_at=as_of
            )
            if not isinstance(advisory, EvidenceAdvisory):
                return EvidenceResult(
                    ok=False,
                    error_code="INVALID_STATE",
                    message="advisory assembly did not return EvidenceAdvisory",
                )
            return EvidenceResult(ok=True, value=advisory)
        except (TypeError, ValueError) as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )

    def retained_observations(self) -> tuple[EvidenceRecord, ...]:
        """Return a copy of the process-local observational buffer."""
        return tuple(self._observation_buffer)

    def clear_observation_buffer(self) -> None:
        """Clear the process-local observational buffer (tests / ops)."""
        self._observation_buffer.clear()

    def _retain_observation(self, record: EvidenceRecord) -> None:
        if self._observation_buffer_limit <= 0:
            return
        self._observation_buffer.append(record)
        overflow = len(self._observation_buffer) - self._observation_buffer_limit
        if overflow > 0:
            del self._observation_buffer[:overflow]

    def assign_to_experiment(
        self,
        record: EvidenceRecord,
        definition: ExperimentDefinition | None = None,
        *,
        experiment_id: str | None = None,
    ) -> EvidenceResult:
        """Assign validated evidence to an experiment (E2).

        Returns EvidenceResult with ``value`` set to ExperimentObservation on
        success. Never mutates the EvidenceRecord. Requires a wired
        ExperimentFramework (flag ON).
        """
        if self._experiment_framework is None:
            return EvidenceResult(
                ok=False,
                error_code="UNAVAILABLE",
                message="ExperimentFramework is not wired (feature flag OFF)",
            )
        if not isinstance(record, EvidenceRecord):
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="record must be an EvidenceRecord",
            )
        try:
            observation = self._experiment_framework.assign(
                record,
                definition,
                experiment_id=experiment_id,
            )
            return EvidenceResult(ok=True, value=observation)
        except ExperimentValidationError as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )
        except (TypeError, ValueError) as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )

    def evaluate_policy(
        self,
        observations: Sequence[ExperimentObservation],
        definition: PolicyDefinition | None = None,
        *,
        policy_id: str | None = None,
        created_at: str | None = None,
    ) -> EvidenceResult:
        """Evaluate ExperimentObservations against a registered policy (E3).

        Returns EvidenceResult with ``value`` set to PolicyEvaluation on
        success. Never mutates observations or evidence. Never promotes
        policies. Requires a wired PolicyEvaluationFactory (flag ON).
        """
        if self._policy_evaluation_factory is None:
            return EvidenceResult(
                ok=False,
                error_code="UNAVAILABLE",
                message="PolicyEvaluationFactory is not wired (feature flag OFF)",
            )
        try:
            evaluation = self._policy_evaluation_factory.evaluate(
                observations,
                definition,
                policy_id=policy_id,
                created_at=created_at,
            )
            return EvidenceResult(ok=True, value=evaluation)
        except EvaluationValidationError as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )
        except (TypeError, ValueError) as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )

    def aggregate_analytics(
        self,
        *,
        evaluations: Sequence[PolicyEvaluation] = (),
        observations: Sequence[ExperimentObservation] = (),
        evidence_records: Sequence[EvidenceRecord] = (),
        audience: str = ANALYTICS_AUDIENCE_GOVERNANCE,
        as_of: str | None = None,
        period: Mapping[str, Any] | None = None,
    ) -> EvidenceResult:
        """Aggregate observational inputs into AnalyticsSummary (E4).

        Never mutates inputs. Never promotes policies. Requires a wired
        AnalyticsEngine (flag ON).
        """
        if self._analytics_engine is None:
            return EvidenceResult(
                ok=False,
                error_code="UNAVAILABLE",
                message="AnalyticsEngine is not wired (feature flag OFF)",
            )
        try:
            summary = self._analytics_engine.aggregate(
                evaluations=evaluations,
                observations=observations,
                evidence_records=evidence_records,
                audience=audience,
                as_of=as_of,
                period=period,
            )
            return EvidenceResult(ok=True, value=summary)
        except AnalyticsValidationError as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )
        except (TypeError, ValueError) as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )

    def project_evidence(
        self,
        summary: AnalyticsSummary,
        *,
        audience: str = ANALYTICS_AUDIENCE_GOVERNANCE,
        as_of: str | None = None,
    ) -> EvidenceResult:
        """Project AnalyticsSummary into EvidenceProjection (E4).

        Never mutates the summary. Never serves student coaching. Requires a
        wired EvidenceProjector / EvidenceProjectionPort (flag ON).
        """
        if self._evidence_projection_port is not None:
            try:
                projection = self._evidence_projection_port.project_summary(
                    summary, audience=audience, as_of=as_of
                )
                return EvidenceResult(ok=True, value=projection)
            except (TypeError, ValueError) as exc:
                return EvidenceResult(
                    ok=False,
                    error_code="INVALID_STATE",
                    message=str(exc),
                )
        if self._evidence_projector is None:
            return EvidenceResult(
                ok=False,
                error_code="UNAVAILABLE",
                message="EvidenceProjector is not wired (feature flag OFF)",
            )
        try:
            projection = self._evidence_projector.project(
                summary, audience=audience, as_of=as_of
            )
            return EvidenceResult(ok=True, value=projection)
        except (TypeError, ValueError) as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )

    def assemble_record(
        self,
        student_id: str,
        *,
        context: EvidenceContext | None = None,
        event: ObservedEvent | None = None,
        as_of: str | None = None,
        mode: str = "collection",
    ) -> EvidenceResult:
        """Produce an EvidenceRecord behind the Learning Evidence contract.

        ``mode`` is accepted for interface stability (shadow / evaluation later).
        E1–E4 never write Runtime A, Twin, Adaptive, Strategy, or Experience state.
        Analytics remain governance-facing only (no Experience authority).
        """
        sid = (student_id or "").strip()
        if not sid:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="student_id must be a non-empty string",
            )
        if as_of is not None and not isinstance(as_of, str):
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="as_of must be an ISO string or None",
            )
        if context is not None and not isinstance(context, EvidenceContext):
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="context must be an EvidenceContext or None",
            )
        if event is not None and not isinstance(event, ObservedEvent):
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="event must be an ObservedEvent or None",
            )
        if context is not None and event is not None:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message="provide context or event, not both",
            )
        _ = mode
        try:
            if event is not None:
                if event.student_id != sid:
                    return EvidenceResult(
                        ok=False,
                        error_code="INVALID_STATE",
                        message="event.student_id must match student_id",
                    )
                return EvidenceResult(
                    ok=True, value=self._factory.create_from_observed_event(event)
                )
            resolved = context
            if resolved is None:
                resolved = EvidenceContext(student_id=sid, as_of=as_of)
            elif resolved.student_id != sid:
                return EvidenceResult(
                    ok=False,
                    error_code="INVALID_STATE",
                    message="context.student_id must match student_id",
                )
            return EvidenceResult(
                ok=True, value=self._factory.create_from_context(resolved)
            )
        except EvidenceValidationError as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )
        except (TypeError, ValueError) as exc:
            return EvidenceResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )


def empty_evidence_record(
    *,
    context: EvidenceContext | None = None,
    as_of: str | None = None,
) -> EvidenceRecord:
    """Build a structurally complete empty EvidenceRecord (fallback stub)."""
    resolved = context or EvidenceContext(student_id="anonymous")
    resolved_as_of = as_of if as_of is not None else resolved.as_of
    return EvidenceRecord(
        evidence_id=(
            f"evidence-{resolved.student_id}" if resolved.student_id else ""
        ),
        evidence_version=EVIDENCE_VERSION_E1,
        student_id=resolved.student_id,
        source_refs=resolved.source_refs,
        evidence_class=resolved.evidence_class,
        event_type=resolved.evidence_class.lower() if resolved.evidence_class else "",
        claim_boundary=resolved.claim_boundary,
        quality=EvidenceQuality(
            result="",
            codes=("empty_authentic",),
            summary="Empty authentic evidence record — no observation collected.",
            runtime_a_ref_present=False,
        ),
        payload_summary={},
        provenance={},
        limitations=("empty_authentic", *resolved.limitations),
        engine_version=EVIDENCE_VERSION_E1,
        observed_at=None,
        ingested_at=None,
        as_of=resolved_as_of,
        authority=AUTHORITY_EVIDENCE_PLATFORM,
        availability=AVAILABILITY_UNAVAILABLE,
        unavailable_reason="empty_authentic",
    )


def build_evidence_platform_adapter(
    *,
    enabled: bool,
    factory: EvidenceFactory | None = None,
    experiment_framework: ExperimentFramework | None = None,
    policy_evaluation_factory: PolicyEvaluationFactory | None = None,
    analytics_engine: AnalyticsEngine | None = None,
    evidence_projector: EvidenceProjector | None = None,
    evidence_projection_port: EvidenceGovernanceProjectionPort | None = None,
    advisory_assembler: EvidenceAdvisoryAssembler | None = None,
    advisory_enabled: bool = True,
) -> EvidencePlatformAdapter | None:
    """DI helper — construct EvidencePlatformAdapter only when the flag is on."""
    if not enabled:
        return None
    if factory is not None:
        wired_factory = factory
    else:
        wired_factory = build_evidence_factory(enabled=True)
        if wired_factory is None:
            return None
    wired_framework = experiment_framework
    if wired_framework is None:
        wired_framework = build_experiment_framework(enabled=True)
    wired_evaluation = policy_evaluation_factory
    if wired_evaluation is None:
        wired_evaluation = build_policy_evaluation_factory(enabled=True)
    wired_analytics = analytics_engine
    if wired_analytics is None:
        wired_analytics = build_analytics_engine(enabled=True)
    wired_projector = evidence_projector
    if wired_projector is None:
        wired_projector = build_evidence_projector(enabled=True)
    wired_port = evidence_projection_port
    if wired_port is None:
        wired_port = build_evidence_projection_port(
            enabled=True, projector=wired_projector
        )
    wired_advisory = advisory_assembler
    if wired_advisory is None and advisory_enabled:
        wired_advisory = build_evidence_advisory_assembler(enabled=True)
    if wired_advisory is None:
        wired_advisory = EvidenceAdvisoryAssembler(enabled=True)
    return EvidencePlatformAdapter(
        factory=wired_factory,
        experiment_framework=wired_framework,
        policy_evaluation_factory=wired_evaluation,
        analytics_engine=wired_analytics,
        evidence_projector=wired_projector,
        evidence_projection_port=wired_port,
        advisory_assembler=wired_advisory,
    )


# Re-export for type checkers / callers that expect observation on results.
__all__ = [
    "EvidencePlatformAdapter",
    "EvidenceProjection",
    "EvidenceFactualSummary",
    "EvidenceAdvisory",
    "ExperimentObservation",
    "PolicyEvaluation",
    "AnalyticsSummary",
    "build_evidence_platform_adapter",
    "empty_evidence_record",
]
