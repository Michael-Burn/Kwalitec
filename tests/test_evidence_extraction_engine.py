"""Unit tests for the Evidence Extraction Engine domain package."""

from __future__ import annotations

import ast
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from app.domain.evidence import (
    BaseExtractor,
    EvidenceCandidate,
    EvidenceCategory,
    EvidenceConfidenceLevel,
    EvidenceExtractor,
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
) -> LearningEvent:
    return LearningEvent.create(
        event_type,
        EventSource.QUIZ_ENGINE,
        EventMetadata(
            timestamp=datetime(2026, 7, 10, 14, 0, tzinfo=UTC),
            topic_id=topic_id,
            curriculum_id="CS1-2026",
            session_id="sess-42",
            duration_seconds=90,
            attributes={"correct": True},
        ),
        event_id="evt-200",
    )


class _StubKnowledgeExtractor(BaseExtractor):
    """Test double that emits a Knowledge candidate for question events."""

    def supports(self, event: LearningEvent) -> bool:
        return event.event_type in {
            LearningEventType.QUESTION_ATTEMPTED,
            LearningEventType.QUESTION_CORRECT,
            LearningEventType.QUESTION_INCORRECT,
        }

    def extract(self, event: LearningEvent) -> list[EvidenceCandidate]:
        return [
            EvidenceCandidate.create(
                identifier=f"knowledge-{event.event_id}",
                category=EvidenceCategory.KNOWLEDGE,
                originating_event=event,
                timestamp=event.metadata.timestamp,
                topic_id=event.metadata.topic_id,
                payload={"outcome": event.metadata.attributes.get("correct")},
                provenance=event.source.value,
                confidence_level=EvidenceConfidenceLevel.MEDIUM,
            )
        ]


class _StubTimeExtractor(BaseExtractor):
    """Test double that emits a Time candidate when duration is present."""

    def supports(self, event: LearningEvent) -> bool:
        return event.metadata.duration_seconds is not None

    def extract(self, event: LearningEvent) -> list[EvidenceCandidate]:
        return [
            EvidenceCandidate.create(
                identifier=f"time-{event.event_id}",
                category=EvidenceCategory.TIME,
                originating_event=event,
                timestamp=event.metadata.timestamp,
                topic_id=event.metadata.topic_id,
                payload={"duration_seconds": event.metadata.duration_seconds},
                provenance=event.source.value,
                confidence_level=EvidenceConfidenceLevel.LOW,
            )
        ]


class _StubMultiCandidateExtractor(BaseExtractor):
    """Test double that returns multiple candidates from one event."""

    def supports(self, event: LearningEvent) -> bool:
        return event.event_type is LearningEventType.QUIZ_COMPLETED

    def extract(self, event: LearningEvent) -> list[EvidenceCandidate]:
        ts = event.metadata.timestamp
        return [
            EvidenceCandidate.create(
                identifier="perf-1",
                category=EvidenceCategory.PERFORMANCE,
                originating_event=event,
                timestamp=ts,
                topic_id=event.metadata.topic_id,
                provenance=event.source.value,
                confidence_level=EvidenceConfidenceLevel.HIGH,
            ),
            EvidenceCandidate.create(
                identifier="engage-1",
                category=EvidenceCategory.ENGAGEMENT,
                originating_event=event,
                timestamp=ts,
                provenance=event.source.value,
                confidence_level=EvidenceConfidenceLevel.LOW,
            ),
        ]


class TestEvidenceCategory:
    """Evidence category enumeration behaviour."""

    def test_recognised_categories_present(self) -> None:
        expected = {
            EvidenceCategory.KNOWLEDGE,
            EvidenceCategory.PERFORMANCE,
            EvidenceCategory.BEHAVIOUR,
            EvidenceCategory.TIME,
            EvidenceCategory.REVISION,
            EvidenceCategory.CONFIDENCE,
            EvidenceCategory.PLANNING,
            EvidenceCategory.ENGAGEMENT,
            EvidenceCategory.RETENTION,
            EvidenceCategory.MOTIVATION,
        }
        assert set(EvidenceCategory) == expected

    def test_values_are_stable_snake_case(self) -> None:
        for member in EvidenceCategory:
            assert member.value == member.name.lower()
            assert " " not in member.value

    def test_str_enum_compares_to_value(self) -> None:
        assert EvidenceCategory.REVISION == "revision"
        assert EvidenceCategory("confidence") is EvidenceCategory.CONFIDENCE


class TestEvidenceConfidenceLevel:
    """Qualitative confidence enumeration."""

    def test_recognised_levels_present(self) -> None:
        expected = {
            EvidenceConfidenceLevel.HIGH,
            EvidenceConfidenceLevel.MEDIUM,
            EvidenceConfidenceLevel.LOW,
            EvidenceConfidenceLevel.UNKNOWN,
        }
        assert set(EvidenceConfidenceLevel) == expected


class TestEvidenceCandidate:
    """Evidence Candidate creation and shape."""

    def test_create_evidence_candidate(self) -> None:
        event = _sample_event()
        candidate = EvidenceCandidate.create(
            identifier="cand-1",
            category=EvidenceCategory.KNOWLEDGE,
            originating_event=event,
            timestamp=event.metadata.timestamp,
            topic_id="CS1-A-T01",
            payload={"correct": True},
            provenance=EventSource.QUIZ_ENGINE.value,
            confidence_level=EvidenceConfidenceLevel.MEDIUM,
            metadata={"extractor": "stub"},
        )
        assert candidate.identifier == "cand-1"
        assert candidate.category is EvidenceCategory.KNOWLEDGE
        assert candidate.originating_event is event
        assert candidate.topic_id == "CS1-A-T01"
        assert candidate.payload["correct"] is True
        assert candidate.provenance == "quiz_engine"
        assert candidate.confidence_level is EvidenceConfidenceLevel.MEDIUM
        assert candidate.metadata["extractor"] == "stub"

    def test_direct_construction_defaults(self) -> None:
        event = _sample_event(LearningEventType.CONFIDENCE_UPDATED, topic_id=None)
        candidate = EvidenceCandidate(
            identifier="cand-2",
            category=EvidenceCategory.CONFIDENCE,
            originating_event=event,
            timestamp=event.metadata.timestamp,
        )
        assert candidate.topic_id is None
        assert candidate.payload == {}
        assert candidate.provenance is None
        assert candidate.confidence_level is EvidenceConfidenceLevel.UNKNOWN
        assert candidate.metadata == {}

    def test_evidence_candidate_is_frozen(self) -> None:
        event = _sample_event()
        candidate = EvidenceCandidate.create(
            identifier="cand-3",
            category=EvidenceCategory.BEHAVIOUR,
            originating_event=event,
            timestamp=event.metadata.timestamp,
        )
        with pytest.raises(AttributeError):
            candidate.category = EvidenceCategory.MOTIVATION  # type: ignore[misc]


class TestEvidenceExtractor:
    """Coordinator registration and invocation."""

    def test_register_extractor(self) -> None:
        engine = EvidenceExtractor()
        stub = _StubKnowledgeExtractor()
        engine.register(stub)
        assert engine.extractors == (stub,)

    def test_constructor_accepts_initial_extractors(self) -> None:
        knowledge = _StubKnowledgeExtractor()
        time = _StubTimeExtractor()
        engine = EvidenceExtractor([knowledge, time])
        assert engine.extractors == (knowledge, time)

    def test_extract_invokes_supporting_extractor(self) -> None:
        engine = EvidenceExtractor()
        engine.register(_StubKnowledgeExtractor())
        event = _sample_event(LearningEventType.QUESTION_CORRECT)
        candidates = engine.extract(event)
        assert len(candidates) == 1
        assert candidates[0].category is EvidenceCategory.KNOWLEDGE
        assert candidates[0].originating_event is event

    def test_extract_skips_non_supporting_extractors(self) -> None:
        engine = EvidenceExtractor([_StubKnowledgeExtractor()])
        event = _sample_event(LearningEventType.MISSION_MISSED)
        assert engine.extract(event) == []

    def test_multiple_extractors_combine_candidates(self) -> None:
        engine = EvidenceExtractor()
        engine.register(_StubKnowledgeExtractor())
        engine.register(_StubTimeExtractor())
        event = _sample_event(LearningEventType.QUESTION_ATTEMPTED)
        candidates = engine.extract(event)
        categories = {c.category for c in candidates}
        assert categories == {EvidenceCategory.KNOWLEDGE, EvidenceCategory.TIME}
        assert len(candidates) == 2

    def test_single_extractor_returns_multiple_candidates(self) -> None:
        engine = EvidenceExtractor([_StubMultiCandidateExtractor()])
        event = _sample_event(LearningEventType.QUIZ_COMPLETED)
        candidates = engine.extract(event)
        assert len(candidates) == 2
        assert candidates[0].category is EvidenceCategory.PERFORMANCE
        assert candidates[1].category is EvidenceCategory.ENGAGEMENT

    def test_empty_registry_returns_no_candidates(self) -> None:
        engine = EvidenceExtractor()
        assert engine.extract(_sample_event()) == []


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
