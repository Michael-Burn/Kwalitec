"""Unit tests for OperationalStateBuilder (FOS-005)."""

from __future__ import annotations

import pytest

from app.founder.operational_state.dto.validation import (
    OperationalStateValidationError,
)
from app.founder.operational_state.tests.helpers import (
    FIXED_NOW,
    make_alpha_dto,
    make_builder,
    make_capability_dto,
    make_knowledge_dto,
)


class TestOperationalStateBuilder:
    def test_assembles_sections_from_dtos(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(),
            make_capability_dto(),
            make_alpha_dto(),
        )
        assert state.generated_at == FIXED_NOW
        assert state.engineering.tests_pass is True
        assert state.knowledge.architecture_documents == 4
        assert state.capability.completed_count == 1
        assert state.internal_alpha.duplicate_count == 2
        assert state.release.completed_capabilities == 1
        assert state.release.current_release == "1.0.0"

    def test_default_release_when_capability_blank(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(),
            make_capability_dto(current_release=""),
            make_alpha_dto(),
        )
        assert state.release.current_release == "1.0.0"

    def test_copies_source_versions(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(source_version="k-2"),
            make_capability_dto(source_version="c-2"),
            make_alpha_dto(source_version="a-2"),
        )
        assert state.source_versions.knowledge == "k-2"
        assert state.source_versions.capability_archive == "c-2"
        assert state.source_versions.internal_alpha == "a-2"

    def test_raises_on_validation_failure(self) -> None:
        with pytest.raises(OperationalStateValidationError) as exc_info:
            make_builder().build(
                make_knowledge_dto(engineering_standards=-1),
                make_capability_dto(),
                make_alpha_dto(),
            )
        codes = {issue.code for issue in exc_info.value.report.issues}
        assert "negative_count" in codes

    def test_validate_false_skips_raise(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(engineering_standards=-1),
            make_capability_dto(),
            make_alpha_dto(),
            validate=False,
        )
        assert state.knowledge.engineering_standards == -1
