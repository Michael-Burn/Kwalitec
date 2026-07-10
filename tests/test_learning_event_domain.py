"""Unit tests for the Learning Events domain package."""

from __future__ import annotations

import ast
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest

from app.domain.learning_events import (
    EventMetadata,
    EventSource,
    LearningEvent,
    LearningEventType,
)

DOMAIN_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain"
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


def _iter_domain_python_files() -> list[Path]:
    return sorted(DOMAIN_ROOT.rglob("*.py"))


class TestLearningEventType:
    """Event type enumeration behaviour."""

    def test_recognised_types_present(self) -> None:
        expected = {
            LearningEventType.STUDY_SESSION_STARTED,
            LearningEventType.STUDY_SESSION_COMPLETED,
            LearningEventType.TOPIC_STARTED,
            LearningEventType.TOPIC_COMPLETED,
            LearningEventType.QUESTION_ATTEMPTED,
            LearningEventType.QUESTION_CORRECT,
            LearningEventType.QUESTION_INCORRECT,
            LearningEventType.QUIZ_COMPLETED,
            LearningEventType.MOCK_COMPLETED,
            LearningEventType.REVISION_COMPLETED,
            LearningEventType.MISSION_COMPLETED,
            LearningEventType.MISSION_MISSED,
            LearningEventType.CONFIDENCE_UPDATED,
            LearningEventType.STUDY_SESSION_SKIPPED,
        }
        assert set(LearningEventType) == expected

    def test_values_are_stable_snake_case(self) -> None:
        for member in LearningEventType:
            assert member.value == member.name.lower()
            assert " " not in member.value

    def test_str_enum_compares_to_value(self) -> None:
        assert LearningEventType.QUIZ_COMPLETED == "quiz_completed"
        assert LearningEventType("mission_missed") is LearningEventType.MISSION_MISSED


class TestEventSource:
    """Event source enumeration behaviour."""

    def test_recognised_sources_present(self) -> None:
        expected = {
            EventSource.MANUAL,
            EventSource.STUDY_PLANNER,
            EventSource.MISSION_ENGINE,
            EventSource.QUIZ_ENGINE,
            EventSource.MOCK_EXAM,
            EventSource.AI_TUTOR,
            EventSource.REVISION_ENGINE,
            EventSource.FUTURE_INTEGRATIONS,
        }
        assert set(EventSource) == expected


class TestEventMetadata:
    """Metadata structure and helpers."""

    def test_minimal_metadata(self) -> None:
        ts = datetime(2026, 7, 10, 12, 0, tzinfo=UTC)
        meta = EventMetadata(timestamp=ts)
        assert meta.timestamp == ts
        assert meta.topic_id is None
        assert meta.tags == ()
        assert meta.attributes == {}

    def test_full_metadata_fields(self) -> None:
        ts = datetime(2026, 7, 10, 12, 0, tzinfo=UTC)
        meta = EventMetadata(
            timestamp=ts,
            topic_id="CS1-A-T01",
            curriculum_id="CS1-2026",
            session_id="sess-1",
            duration_seconds=2700,
            difficulty="intermediate",
            confidence=0.7,
            source=EventSource.QUIZ_ENGINE.value,
            tags=("assessment",),
            attributes={"score": 0.8},
        )
        assert meta.topic_id == "CS1-A-T01"
        assert meta.duration_seconds == 2700
        assert meta.has_tag("assessment")
        assert not meta.has_tag("self_report")
        assert meta.attributes["score"] == 0.8

    def test_with_tags_is_immutable_copy(self) -> None:
        ts = datetime(2026, 7, 10, 12, 0, tzinfo=UTC)
        original = EventMetadata(timestamp=ts, tags=("behaviour",))
        updated = original.with_tags("self_report", "behaviour")
        assert original.tags == ("behaviour",)
        assert updated.tags == ("behaviour", "self_report")
        assert updated is not original


class TestLearningEvent:
    """Learning Event creation and shape."""

    def test_create_learning_event(self) -> None:
        ts = datetime(2026, 7, 10, 18, 30, tzinfo=UTC)
        event = LearningEvent.create(
            LearningEventType.TOPIC_STARTED,
            EventSource.MISSION_ENGINE,
            EventMetadata(timestamp=ts, topic_id="CS1-B-T02", curriculum_id="CS1-2026"),
            event_id="evt-100",
        )
        assert event.event_type is LearningEventType.TOPIC_STARTED
        assert event.source is EventSource.MISSION_ENGINE
        assert event.metadata.topic_id == "CS1-B-T02"
        assert event.event_id == "evt-100"

    def test_direct_construction(self) -> None:
        ts = datetime(2026, 7, 10, 9, 0, tzinfo=UTC)
        event = LearningEvent(
            event_type=LearningEventType.CONFIDENCE_UPDATED,
            source=EventSource.MANUAL,
            metadata=EventMetadata(
                timestamp=ts,
                confidence=0.4,
                tags=("self_report",),
            ),
        )
        assert event.event_type is LearningEventType.CONFIDENCE_UPDATED
        assert event.metadata.has_tag("self_report")
        assert event.event_id is None

    def test_learning_event_is_frozen(self) -> None:
        ts = datetime(2026, 7, 10, 9, 0, tzinfo=UTC)
        event = LearningEvent.create(
            LearningEventType.STUDY_SESSION_SKIPPED,
            EventSource.STUDY_PLANNER,
            EventMetadata(timestamp=ts),
        )
        with pytest.raises(AttributeError):
            event.event_type = LearningEventType.MISSION_COMPLETED  # type: ignore[misc]


class TestDomainIndependence:
    """Domain package must remain framework-independent."""

    def test_source_files_have_no_framework_imports(self) -> None:
        violations: list[str] = []
        for path in _iter_domain_python_files():
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
        # Domain modules must not pull Flask as a dependency of their own imports.
        domain_modules = [
            name
            for name in sys.modules
            if name == "app.domain" or name.startswith("app.domain.")
        ]
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
