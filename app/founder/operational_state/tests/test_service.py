"""Unit tests for FounderOperationalStateService (FOS-005)."""

from __future__ import annotations

import pytest

from app.founder.operational_state.dto.validation import (
    OperationalStateValidationError,
)
from app.founder.operational_state.tests.helpers import (
    FIXED_NOW,
    make_alpha_dto,
    make_capability_dto,
    make_knowledge_dto,
    make_service,
)


class TestFounderOperationalStateService:
    def test_get_state_aggregates_providers(self) -> None:
        service = make_service(
            knowledge=make_knowledge_dto(),
            capability=make_capability_dto(),
            alpha=make_alpha_dto(),
        )
        state = service.get_state()
        assert state.generated_at == FIXED_NOW
        assert state.knowledge.engineering_standards == 5
        assert state.capability.total_count == 2
        assert state.internal_alpha.current_week == "2026-W28"
        assert state.release.current_release == "1.0.0"
        assert state.source_versions.knowledge == "knowledge-1.0"

    def test_get_state_accepts_fixed_generated_at(self) -> None:
        service = make_service(
            knowledge=make_knowledge_dto(),
            capability=make_capability_dto(),
            alpha=make_alpha_dto(),
        )
        state = service.get_state(generated_at=FIXED_NOW)
        assert state.generated_at == FIXED_NOW

    def test_empty_providers_produce_valid_defaults(self) -> None:
        state = make_service().get_state()
        assert state.capability.total_count == 0
        assert state.internal_alpha.feedback_count == 0
        assert state.release.current_release == "1.0.0"
        assert state.source_versions.knowledge == "unwired"

    def test_invalid_provider_data_raises(self) -> None:
        service = make_service(
            knowledge=make_knowledge_dto(engineering_standards=-1),
            capability=make_capability_dto(),
            alpha=make_alpha_dto(),
        )
        with pytest.raises(OperationalStateValidationError):
            service.get_state()
