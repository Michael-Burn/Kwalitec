"""Unit tests for the Evidence Transformation Stage domain package."""

from __future__ import annotations

import ast
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from app.domain.evidence import (
    BaseTransformer,
    EvidenceCandidate,
    EvidenceCategory,
    EvidenceConfidenceLevel,
    EvidenceTransformer,
    EvidenceType,
    LearningEvidence,
    TransformationError,
)
from app.domain.learning_events import (
    EventMetadata,
    EventSource,
    LearningEvent,
    LearningEventType,
)

EVIDENCE_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "evidence"
FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "sqlalchemy",
        "wtforms",
    }
)


def _sample_event(
    event_type: LearningEventType = LearningEventType.QUESTION_ATTEMPTED,
    *,
    topic_id: str | None = "CS1-A-T01",
    curriculum_id: str | None = "CS1-2026",
) -> LearningEvent:
    return LearningEvent.create(
        event_type,
        EventSource.QUIZ_ENGINE,
        EventMetadata(
            timestamp=datetime(2026, 7, 10, 14, 0, tzinfo=UTC),
            topic_id=topic_id,
            curriculum_id=curriculum_id,
            session_id="sess-42",
            duration_seconds=90,
            attributes={"correct": True},
        ),
        event_id="evt-400",
    )


def _valid_candidate(**overrides: Any) -> EvidenceCandidate:
    event = overrides.pop("originating_event", None) or _sample_event()
    defaults: dict[str, Any] = {
        "identifier": "cand-xform-1",
        "category": EvidenceCategory.KNOWLEDGE,
        "originating_event": event,
        "timestamp": event.metadata.timestamp,
        "topic_id": event.metadata.topic_id,
        "payload": {"correct": True},
        "provenance": EventSource.QUIZ_ENGINE.value,
        "confidence_level": EvidenceConfidenceLevel.MEDIUM,
        "metadata": {"extractor": "stub"},
    }
    defaults.update(overrides)
    return EvidenceCandidate.create(**defaults)


class _StubKnowledgeTransformer(BaseTransformer):
    """Test double that normalizes Knowledge candidates."""

    def supports(self, candidate: EvidenceCandidate) -> bool:
        return candidate.category is EvidenceCategory.KNOWLEDGE

    def transform(self, candidate: EvidenceCandidate) -> LearningEvidence:
        event = candidate.originating_event
        return LearningEvidence.create(
            evidence_id=candidate.identifier,
            evidence_type=EvidenceType.QUESTION_ATTEMPT,
            originating_event_id=event.event_id,
            timestamp=candidate.timestamp,
            topic_id=candidate.topic_id,
            curriculum_id=event.metadata.curriculum_id,
            payload=dict(candidate.payload),
            provenance=candidate.provenance,
            confidence_level=candidate.confidence_level,
            metadata={
                **dict(candidate.metadata),
                "transformer": "stub_knowledge",
            },
        )


class _StubTimeTransformer(BaseTransformer):
    """Test double that normalizes Time candidates."""

    def supports(self, candidate: EvidenceCandidate) -> bool:
        return candidate.category is EvidenceCategory.TIME

    def transform(self, candidate: EvidenceCandidate) -> LearningEvidence:
        event = candidate.originating_event
        return LearningEvidence.create(
            evidence_id=candidate.identifier,
            evidence_type=EvidenceType.TIME_ON_TASK,
            originating_event_id=event.event_id,
            timestamp=candidate.timestamp,
            topic_id=candidate.topic_id,
            curriculum_id=event.metadata.curriculum_id,
            payload=dict(candidate.payload),
            provenance=candidate.provenance,
            confidence_level=candidate.confidence_level,
            metadata={"transformer": "stub_time"},
        )


class _CatchAllTransformer(BaseTransformer):
    """Broad fallback used to verify registration-order precedence."""

    def supports(self, candidate: EvidenceCandidate) -> bool:
        return True

    def transform(self, candidate: EvidenceCandidate) -> LearningEvidence:
        return LearningEvidence.create(
            evidence_id=candidate.identifier,
            evidence_type=EvidenceType.STUDY_SESSION,
            originating_event_id=candidate.originating_event.event_id,
            timestamp=candidate.timestamp,
            payload=dict(candidate.payload),
            provenance=candidate.provenance,
            confidence_level=candidate.confidence_level,
            metadata={"transformer": "catch_all"},
        )


class TestEvidenceType:
    """Evidence type catalogue behaviour."""

    def test_recognised_core_types_present(self) -> None:
        expected = {
            EvidenceType.STUDY_SESSION,
            EvidenceType.QUESTION_ATTEMPT,
            EvidenceType.QUESTION_CORRECT,
            EvidenceType.QUESTION_INCORRECT,
            EvidenceType.QUIZ_COMPLETED,
            EvidenceType.MOCK_EXAM,
            EvidenceType.MISSION_COMPLETED,
            EvidenceType.MISSION_MISSED,
            EvidenceType.REVISION_SESSION,
            EvidenceType.CONFIDENCE_RATING,
            EvidenceType.TIME_ON_TASK,
            EvidenceType.SKIPPED_SESSION,
            EvidenceType.DIAGNOSTIC_ASSESSMENT,
        }
        assert expected.issubset(set(EvidenceType))

    def test_values_are_stable_snake_case(self) -> None:
        for member in EvidenceType:
            assert member.value == member.name.lower()
            assert " " not in member.value


class TestLearningEvidence:
    """Learning Evidence creation and shape."""

    def test_create_learning_evidence(self) -> None:
        evidence = LearningEvidence.create(
            evidence_id="ev-1",
            evidence_type=EvidenceType.QUESTION_ATTEMPT,
            originating_event_id="evt-400",
            timestamp=datetime(2026, 7, 10, 14, 0, tzinfo=UTC),
            topic_id="CS1-A-T01",
            curriculum_id="CS1-2026",
            payload={"correct": True},
            provenance="quiz_engine",
            confidence_level=EvidenceConfidenceLevel.HIGH,
            metadata={"stage": "transformation"},
        )
        assert evidence.evidence_id == "ev-1"
        assert evidence.evidence_type is EvidenceType.QUESTION_ATTEMPT
        assert evidence.originating_event_id == "evt-400"
        assert evidence.topic_id == "CS1-A-T01"
        assert evidence.curriculum_id == "CS1-2026"
        assert evidence.payload == {"correct": True}
        assert evidence.provenance == "quiz_engine"
        assert evidence.confidence_level is EvidenceConfidenceLevel.HIGH
        assert evidence.metadata == {"stage": "transformation"}

    def test_create_defaults_optional_fields(self) -> None:
        evidence = LearningEvidence.create(
            evidence_id="ev-2",
            evidence_type=EvidenceType.STUDY_SESSION,
            originating_event_id=None,
            timestamp=datetime(2026, 7, 10, 14, 0, tzinfo=UTC),
        )
        assert evidence.topic_id is None
        assert evidence.curriculum_id is None
        assert evidence.payload == {}
        assert evidence.provenance is None
        assert evidence.confidence_level is EvidenceConfidenceLevel.UNKNOWN
        assert evidence.metadata == {}

    def test_create_copies_mutable_mappings(self) -> None:
        payload = {"score_hint": "not_a_score"}
        metadata = {"k": "v"}
        evidence = LearningEvidence.create(
            evidence_id="ev-3",
            evidence_type=EvidenceType.TIME_ON_TASK,
            originating_event_id="evt-1",
            timestamp=datetime(2026, 7, 10, 14, 0, tzinfo=UTC),
            payload=payload,
            metadata=metadata,
        )
        payload["mutated"] = True
        metadata["mutated"] = True
        assert evidence.payload == {"score_hint": "not_a_score"}
        assert evidence.metadata == {"k": "v"}

    def test_learning_evidence_is_frozen(self) -> None:
        evidence = LearningEvidence.create(
            evidence_id="ev-4",
            evidence_type=EvidenceType.REVISION_SESSION,
            originating_event_id="evt-1",
            timestamp=datetime(2026, 7, 10, 14, 0, tzinfo=UTC),
        )
        with pytest.raises(AttributeError):
            evidence.evidence_id = "mutated"  # type: ignore[misc]
        with pytest.raises(AttributeError):
            evidence.evidence_type = EvidenceType.MOCK_EXAM  # type: ignore[misc]

    def test_no_scoring_or_weight_fields(self) -> None:
        field_names = set(LearningEvidence.__dataclass_fields__)
        forbidden = {
            "score",
            "weight",
            "mastery",
            "readiness",
            "weighted_score",
            "numerical_confidence",
        }
        assert field_names.isdisjoint(forbidden)


class TestEvidenceTransformer:
    """Coordinator registration and transformation pipeline."""

    def test_register_transformer(self) -> None:
        engine = EvidenceTransformer()
        stub = _StubKnowledgeTransformer()
        engine.register(stub)
        assert engine.transformers == (stub,)

    def test_constructor_accepts_initial_transformers(self) -> None:
        knowledge = _StubKnowledgeTransformer()
        time = _StubTimeTransformer()
        engine = EvidenceTransformer([knowledge, time])
        assert engine.transformers == (knowledge, time)

    def test_transform_returns_single_learning_evidence(self) -> None:
        engine = EvidenceTransformer([_StubKnowledgeTransformer()])
        result = engine.transform(_valid_candidate())
        assert isinstance(result, LearningEvidence)
        assert result.evidence_id == "cand-xform-1"
        assert result.evidence_type is EvidenceType.QUESTION_ATTEMPT
        assert result.originating_event_id == "evt-400"
        assert result.curriculum_id == "CS1-2026"
        assert result.topic_id == "CS1-A-T01"
        assert result.payload == {"correct": True}
        assert result.provenance == EventSource.QUIZ_ENGINE.value
        assert result.confidence_level is EvidenceConfidenceLevel.MEDIUM
        assert result.metadata["transformer"] == "stub_knowledge"

    def test_first_supporting_transformer_wins(self) -> None:
        engine = EvidenceTransformer(
            [_StubKnowledgeTransformer(), _CatchAllTransformer()]
        )
        result = engine.transform(_valid_candidate())
        assert result.metadata["transformer"] == "stub_knowledge"

    def test_later_transformer_used_when_earlier_does_not_support(self) -> None:
        engine = EvidenceTransformer(
            [_StubKnowledgeTransformer(), _StubTimeTransformer()]
        )
        candidate = _valid_candidate(
            identifier="cand-time",
            category=EvidenceCategory.TIME,
            payload={"duration_seconds": 90},
            confidence_level=EvidenceConfidenceLevel.LOW,
        )
        result = engine.transform(candidate)
        assert result.evidence_type is EvidenceType.TIME_ON_TASK
        assert result.metadata["transformer"] == "stub_time"

    def test_unsupported_candidate_raises(self) -> None:
        engine = EvidenceTransformer([_StubKnowledgeTransformer()])
        candidate = _valid_candidate(category=EvidenceCategory.BEHAVIOUR)
        with pytest.raises(TransformationError, match="No registered transformer"):
            engine.transform(candidate)

    def test_empty_registry_raises(self) -> None:
        engine = EvidenceTransformer()
        with pytest.raises(TransformationError):
            engine.transform(_valid_candidate())

    def test_transform_does_not_mutate_candidate(self) -> None:
        candidate = _valid_candidate(
            payload={"correct": True},
            metadata={"extractor": "stub"},
        )
        original_payload = dict(candidate.payload)
        original_metadata = dict(candidate.metadata)
        engine = EvidenceTransformer([_StubKnowledgeTransformer()])
        engine.transform(candidate)
        assert candidate.payload == original_payload
        assert candidate.metadata == original_metadata
        with pytest.raises(AttributeError):
            candidate.identifier = "mutated"  # type: ignore[misc]

    def test_pipeline_extraction_validation_transformation(self) -> None:
        """End-to-end domain pipeline with stubs (no persistence / Twin)."""
        from app.domain.evidence import EvidenceExtractor, EvidenceValidator
        from app.domain.evidence.extractors.base_extractor import BaseExtractor

        class _KnowledgeExtractor(BaseExtractor):
            def supports(self, event: LearningEvent) -> bool:
                return event.event_type is LearningEventType.QUESTION_ATTEMPTED

            def extract(self, event: LearningEvent) -> list[EvidenceCandidate]:
                return [
                    EvidenceCandidate.create(
                        identifier=f"knowledge-{event.event_id}",
                        category=EvidenceCategory.KNOWLEDGE,
                        originating_event=event,
                        timestamp=event.metadata.timestamp,
                        topic_id=event.metadata.topic_id,
                        payload={"outcome": True},
                        provenance=event.source.value,
                        confidence_level=EvidenceConfidenceLevel.MEDIUM,
                        metadata={},
                    )
                ]

        event = _sample_event()
        candidates = EvidenceExtractor([_KnowledgeExtractor()]).extract(event)
        assert len(candidates) == 1

        validation = EvidenceValidator.with_structural_rules().validate(candidates[0])
        assert validation.accepted is True

        evidence = EvidenceTransformer([_StubKnowledgeTransformer()]).transform(
            candidates[0]
        )
        assert evidence.evidence_id == "knowledge-evt-400"
        assert evidence.originating_event_id == "evt-400"
        assert evidence.evidence_type is EvidenceType.QUESTION_ATTEMPT


class TestFrameworkIndependence:
    """Evidence package must remain framework-independent."""

    def test_source_files_have_no_framework_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(EVIDENCE_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES:
                            loc = f"{path}:{node.lineno}"
                            violations.append(f"{loc} import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES:
                        loc = f"{path}:{node.lineno}"
                        violations.append(f"{loc} from {node.module}")
        assert violations == []

    def test_importing_package_does_not_require_flask(self) -> None:
        domain_modules = [
            name
            for name in sys.modules
            if name == "app.domain.evidence" or name.startswith("app.domain.evidence.")
        ]
        assert domain_modules
        for name in domain_modules:
            module = sys.modules[name]
            module_file = getattr(module, "__file__", "") or ""
            if "site-packages" in module_file or "flask" in module_file.lower():
                pytest.fail(
                    f"Unexpected framework module path for {name}: {module_file}"
                )
            assert not any(
                dep in getattr(module, "__dict__", {})
                for dep in ("Flask", "request", "db", "SQLAlchemy")
            )

    def test_transformer_modules_importable_without_services(self) -> None:
        import app.domain.evidence.evidence_transformer as transformer_mod
        import app.domain.evidence.learning_evidence as learning_mod
        import app.domain.evidence.transformers.base_transformer as base_mod

        for module in (transformer_mod, learning_mod, base_mod):
            module_dict = getattr(module, "__dict__", {})
            assert "services" not in module_dict
            module_attrs = dir(module)
            assert not any(
                key.startswith("app.services")
                for key in sys.modules
                if key in module_attrs
            )
