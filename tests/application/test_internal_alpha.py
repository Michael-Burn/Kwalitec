"""Tests for Educational Intelligence Internal Alpha glue (Capability 3.5.2)."""

from __future__ import annotations

from app.application.config import (
    FEATURE_FLAGS,
    EducationalIntelligenceFeatureFlags,
    build_twin_provider,
    is_internal_alpha_enabled,
    resolve_feature_flags,
)
from app.application.twin import (
    InternalAlphaTwinSource,
    TwinProvider,
    TwinRetrievalContext,
)
from app.domain.twin import DigitalTwin


class TestInternalAlphaFlags:
    def test_disabled_by_default(self) -> None:
        assert is_internal_alpha_enabled(environ={}) is False
        assert resolve_feature_flags(environ={}) is FEATURE_FLAGS

    def test_enabled_resolves_recommendation_slice_only(self) -> None:
        flags = resolve_feature_flags(
            environ={"KWALITEC_EI_INTERNAL_ALPHA": "1"}
        )
        assert flags.ENABLE_EDUCATIONAL_ORCHESTRATOR is True
        assert flags.ENABLE_EI_RECOMMENDATIONS is True
        assert flags.ENABLE_EI_MISSIONS is False
        assert flags.ENABLE_EI_EXPLAINABILITY is False
        assert flags.ENABLE_EI_PROGRESS is False

    def test_truthy_variants(self) -> None:
        for value in ("true", "YES", "on", "1"):
            assert is_internal_alpha_enabled(
                environ={"KWALITEC_EI_INTERNAL_ALPHA": value}
            )

    def test_falsey_variants(self) -> None:
        for value in ("", "0", "false", "no", "off"):
            assert not is_internal_alpha_enabled(
                environ={"KWALITEC_EI_INTERNAL_ALPHA": value}
            )


class TestInternalAlphaTwinSource:
    def test_returns_structural_cold_start_twin(self) -> None:
        source = InternalAlphaTwinSource()
        twin = source.load(
            "42",
            context=TwinRetrievalContext(curriculum_id="7", surface_intent="dashboard"),
        )
        assert isinstance(twin, DigitalTwin)
        assert twin.identity.student_id == "42"
        assert twin.identity.curriculum_id == "7"
        # Empty structural domains — honest cold-start, not Mid theatre.
        assert twin.knowledge == twin.knowledge.__class__.create()
        assert twin.memory == twin.memory.__class__.create()
        assert twin.performance == twin.performance.__class__.create()

    def test_build_twin_provider_wires_source_when_alpha_on(self) -> None:
        flags = EducationalIntelligenceFeatureFlags(
            ENABLE_EDUCATIONAL_ORCHESTRATOR=True,
            ENABLE_EI_RECOMMENDATIONS=True,
        )
        provider = build_twin_provider(
            flags=flags,
            environ={"KWALITEC_EI_INTERNAL_ALPHA": "1"},
        )
        assert isinstance(provider, TwinProvider)
        twin = provider.retrieve(
            "99",
            context=TwinRetrievalContext(curriculum_id="1"),
        )
        assert isinstance(twin, DigitalTwin)
        assert twin.identity.student_id == "99"

    def test_build_twin_provider_has_no_source_when_alpha_off(self) -> None:
        provider = build_twin_provider(
            flags=FEATURE_FLAGS,
            environ={},
        )
        from app.application.twin import TwinAbsent

        result = provider.retrieve("99")
        assert isinstance(result, TwinAbsent)
