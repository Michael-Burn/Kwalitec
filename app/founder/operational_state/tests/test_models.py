"""Unit tests for FounderOperationalState snapshot model (FOS-005)."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from app.founder.operational_state.models import (
    SNAPSHOT_VERSION,
    FounderOperationalState,
)
from app.founder.operational_state.tests.helpers import (
    FIXED_NOW,
    make_alpha_dto,
    make_builder,
    make_capability_dto,
    make_knowledge_dto,
)


class TestFounderOperationalStateModel:
    def test_snapshot_is_frozen(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(),
            make_capability_dto(),
            make_alpha_dto(),
        )
        assert isinstance(state, FounderOperationalState)
        with pytest.raises(FrozenInstanceError):
            state.snapshot_version = "2.0"  # type: ignore[misc]

    def test_snapshot_carries_metadata(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(),
            make_capability_dto(),
            make_alpha_dto(),
            generated_at=FIXED_NOW,
        )
        assert state.generated_at == FIXED_NOW
        assert state.snapshot_version == SNAPSHOT_VERSION
        assert state.source_versions.knowledge == "knowledge-1.0"
        assert state.source_versions.capability_archive == "capability-1.0"
        assert state.source_versions.internal_alpha == "alpha-1.0"

    def test_sections_are_summaries_only(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(),
            make_capability_dto(),
            make_alpha_dto(),
        )
        assert state.engineering.standards_count == 5
        assert state.knowledge.indexed_artefacts == 10
        assert state.capability.total_count == 2
        assert state.internal_alpha.feedback_count == 7
        assert state.release.current_release == "1.0.0"
        assert "raw" not in state.__dataclass_fields__

    def test_source_versions_mapping_is_immutable(self) -> None:
        state = make_builder().build(
            make_knowledge_dto(),
            make_capability_dto(),
            make_alpha_dto(),
        )
        mapping = state.source_versions.as_mapping()
        with pytest.raises(TypeError):
            mapping["knowledge"] = "mutated"  # type: ignore[index]
