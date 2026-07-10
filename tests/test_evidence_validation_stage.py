"""Unit tests for the Evidence Validation Stage domain package."""

from __future__ import annotations

import ast
import sys
from dataclasses import fields
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import pytest

from app.domain.evidence import (
    BaseValidator,
    EvidenceCandidate,
    EvidenceCategory,
    EvidenceConfidenceLevel,
    EvidenceValidator,
    ValidationMessage,
    ValidationResult,
    ValidationSeverity,
)
from app.domain.evidence.validators.structural import (
    CategoryPresentValidator,
    IdentifierPresentValidator,
    MetadataPresentValidator,
    OriginatingEventPresentValidator,
    PayloadPresentValidator,
    SourcePresentValidator,
    TimestampPresentValidator,
    default_structural_validators,
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
        event_id="evt-300",
    )


def _valid_candidate(**overrides: Any) -> EvidenceCandidate:
    event = overrides.pop("originating_event", None) or _sample_event()
    defaults: dict[str, Any] = {
        "identifier": "cand-valid-1",
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


def _candidate_with(**overrides: Any) -> EvidenceCandidate:
    """Build a candidate allowing structurally invalid field values.

    Uses ``object.__new__`` so tests can supply ``None`` / wrong types that
    normal construction would reject at the type layer.
    """
    event = _sample_event()
    values: dict[str, Any] = {
        "identifier": "cand-broken",
        "category": EvidenceCategory.PERFORMANCE,
        "originating_event": event,
        "timestamp": event.metadata.timestamp,
        "topic_id": None,
        "payload": {},
        "provenance": "quiz_engine",
        "confidence_level": EvidenceConfidenceLevel.UNKNOWN,
        "metadata": {},
    }
    values.update(overrides)
    candidate = object.__new__(EvidenceCandidate)
    for field_def in fields(EvidenceCandidate):
        object.__setattr__(candidate, field_def.name, values[field_def.name])
    return candidate


class _StubWarningValidator(BaseValidator):
    """Test double that always emits a WARNING."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        return [
            ValidationMessage(
                code="stub_warning",
                message=f"Advisory note for {candidate.identifier}",
                severity=ValidationSeverity.WARNING,
                field="identifier",
            )
        ]


class _StubErrorValidator(BaseValidator):
    """Test double that always emits an ERROR."""

    def validate(self, candidate: EvidenceCandidate) -> list[ValidationMessage]:
        return [
            ValidationMessage(
                code="stub_error",
                message="Forced rejection",
                severity=ValidationSeverity.ERROR,
                field=None,
            )
        ]


class TestValidationSeverity:
    """Severity enumeration behaviour."""

    def test_recognised_severities_present(self) -> None:
        expected = {
            ValidationSeverity.ERROR,
            ValidationSeverity.WARNING,
            ValidationSeverity.INFO,
        }
        assert set(ValidationSeverity) == expected

    def test_values_are_stable_snake_case(self) -> None:
        for member in ValidationSeverity:
            assert member.value == member.name.lower()


class TestValidationMessage:
    """Validation message shape."""

    def test_create_message(self) -> None:
        message = ValidationMessage(
            code="missing_identifier",
            message="Identifier required",
            severity=ValidationSeverity.ERROR,
            field="identifier",
        )
        assert message.code == "missing_identifier"
        assert message.field == "identifier"
        assert message.severity is ValidationSeverity.ERROR

    def test_message_is_frozen(self) -> None:
        message = ValidationMessage(
            code="x",
            message="y",
            severity=ValidationSeverity.INFO,
        )
        with pytest.raises(AttributeError):
            message.code = "z"  # type: ignore[misc]


class TestValidationResult:
    """Aggregated validation outcome."""

    def test_from_messages_accepted_when_no_errors(self) -> None:
        result = ValidationResult.from_messages(
            [
                ValidationMessage(
                    code="note",
                    message="ok",
                    severity=ValidationSeverity.INFO,
                ),
                ValidationMessage(
                    code="soft",
                    message="careful",
                    severity=ValidationSeverity.WARNING,
                ),
            ]
        )
        assert result.accepted is True
        assert len(result.warnings) == 1
        assert len(result.errors) == 0
        assert len(result.infos) == 1

    def test_from_messages_rejected_when_error_present(self) -> None:
        result = ValidationResult.from_messages(
            [
                ValidationMessage(
                    code="bad",
                    message="fail",
                    severity=ValidationSeverity.ERROR,
                ),
                ValidationMessage(
                    code="soft",
                    message="careful",
                    severity=ValidationSeverity.WARNING,
                ),
            ]
        )
        assert result.accepted is False
        assert len(result.errors) == 1
        assert len(result.warnings) == 1

    def test_severity_summary_counts_all_levels(self) -> None:
        result = ValidationResult.from_messages(
            [
                ValidationMessage("a", "a", ValidationSeverity.ERROR),
                ValidationMessage("b", "b", ValidationSeverity.ERROR),
                ValidationMessage("c", "c", ValidationSeverity.WARNING),
            ]
        )
        summary = result.severity_summary
        assert summary[ValidationSeverity.ERROR] == 2
        assert summary[ValidationSeverity.WARNING] == 1
        assert summary[ValidationSeverity.INFO] == 0

    def test_empty_messages_accepted(self) -> None:
        result = ValidationResult.from_messages([])
        assert result.accepted is True
        assert result.messages == ()
        assert result.severity_summary[ValidationSeverity.ERROR] == 0

    def test_result_is_frozen(self) -> None:
        result = ValidationResult.from_messages([])
        with pytest.raises(AttributeError):
            result.accepted = False  # type: ignore[misc]


class TestStructuralValidators:
    """Individual structural presence/type rules."""

    def test_identifier_rejects_empty_and_blank(self) -> None:
        validator = IdentifierPresentValidator()
        assert validator.validate(_candidate_with(identifier=""))[0].code == (
            "missing_identifier"
        )
        assert validator.validate(_candidate_with(identifier="   "))[0].code == (
            "missing_identifier"
        )
        assert validator.validate(_candidate_with(identifier=None))[0].code == (
            "missing_identifier"
        )
        assert validator.validate(_valid_candidate()) == []

    def test_category_rejects_non_enum(self) -> None:
        validator = CategoryPresentValidator()
        messages = validator.validate(_candidate_with(category="knowledge"))
        assert messages[0].code == "missing_category"
        assert validator.validate(_valid_candidate()) == []

    def test_timestamp_rejects_non_datetime(self) -> None:
        validator = TimestampPresentValidator()
        messages = validator.validate(_candidate_with(timestamp="2026-07-10"))
        assert messages[0].code == "missing_timestamp"
        assert validator.validate(_valid_candidate()) == []

    def test_originating_event_rejects_missing(self) -> None:
        validator = OriginatingEventPresentValidator()
        messages = validator.validate(_candidate_with(originating_event=None))
        assert messages[0].code == "missing_originating_event"
        assert validator.validate(_valid_candidate()) == []

    def test_source_rejects_missing_provenance(self) -> None:
        validator = SourcePresentValidator()
        assert validator.validate(_candidate_with(provenance=None))[0].code == (
            "missing_source"
        )
        assert validator.validate(_candidate_with(provenance=""))[0].code == (
            "missing_source"
        )
        assert validator.validate(_valid_candidate()) == []

    def test_metadata_rejects_non_dict(self) -> None:
        validator = MetadataPresentValidator()
        messages = validator.validate(_candidate_with(metadata=None))
        assert messages[0].code == "missing_metadata"
        assert validator.validate(_valid_candidate(metadata={})) == []

    def test_payload_rejects_non_dict_allows_empty(self) -> None:
        validator = PayloadPresentValidator()
        assert validator.validate(_candidate_with(payload=None))[0].code == (
            "missing_payload"
        )
        assert validator.validate(_candidate_with(payload="raw"))[0].code == (
            "missing_payload"
        )
        assert validator.validate(_valid_candidate(payload={})) == []


class TestEvidenceValidator:
    """Coordinator registration and invocation."""

    def test_with_structural_rules_registers_defaults(self) -> None:
        engine = EvidenceValidator.with_structural_rules()
        assert len(engine.validators) == len(default_structural_validators())

    def test_register_validator(self) -> None:
        engine = EvidenceValidator()
        stub = _StubWarningValidator()
        engine.register(stub)
        assert engine.validators == (stub,)

    def test_constructor_accepts_initial_validators(self) -> None:
        warning = _StubWarningValidator()
        error = _StubErrorValidator()
        engine = EvidenceValidator([warning, error])
        assert engine.validators == (warning, error)

    def test_valid_candidate_is_accepted(self) -> None:
        engine = EvidenceValidator.with_structural_rules()
        result = engine.validate(_valid_candidate())
        assert result.accepted is True
        assert result.errors == ()
        assert result.messages == ()

    def test_invalid_candidate_is_rejected(self) -> None:
        engine = EvidenceValidator.with_structural_rules()
        result = engine.validate(_candidate_with(identifier="", provenance=None))
        assert result.accepted is False
        codes = {message.code for message in result.errors}
        assert "missing_identifier" in codes
        assert "missing_source" in codes

    def test_warnings_do_not_reject(self) -> None:
        engine = EvidenceValidator.with_structural_rules()
        engine.register(_StubWarningValidator())
        result = engine.validate(_valid_candidate())
        assert result.accepted is True
        assert len(result.warnings) == 1
        assert result.warnings[0].code == "stub_warning"

    def test_multiple_validators_combine_messages(self) -> None:
        engine = EvidenceValidator(
            [_StubWarningValidator(), _StubErrorValidator()]
        )
        result = engine.validate(_valid_candidate())
        assert result.accepted is False
        assert len(result.messages) == 2
        assert result.severity_summary[ValidationSeverity.WARNING] == 1
        assert result.severity_summary[ValidationSeverity.ERROR] == 1

    def test_empty_registry_accepts(self) -> None:
        engine = EvidenceValidator()
        result = engine.validate(_valid_candidate())
        assert result.accepted is True
        assert result.messages == ()

    def test_validate_does_not_mutate_candidate(self) -> None:
        candidate = _valid_candidate(
            payload={"correct": True},
            metadata={"extractor": "stub"},
        )
        original_payload = dict(candidate.payload)
        original_metadata = dict(candidate.metadata)
        engine = EvidenceValidator.with_structural_rules()
        engine.register(_StubWarningValidator())
        engine.validate(candidate)
        assert candidate.payload == original_payload
        assert candidate.metadata == original_metadata
        with pytest.raises(AttributeError):
            candidate.identifier = "mutated"  # type: ignore[misc]

    def test_validate_returns_single_result_per_candidate(self) -> None:
        engine = EvidenceValidator.with_structural_rules()
        result = engine.validate(_valid_candidate())
        assert isinstance(result, ValidationResult)


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
