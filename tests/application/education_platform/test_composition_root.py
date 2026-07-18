"""CompositionRoot assembly and DI tests."""

from __future__ import annotations

import pytest

from app.application.education_platform.composition_root import CompositionRoot
from app.application.education_platform.exceptions import CompositionError
from app.application.education_platform.platform import EducationPlatform
from app.application.education_platform.policies.orchestration_policy import (
    DEPENDENCY_CHAIN,
)
from tests.application.education_platform.helpers import (
    FakeActivity,
    FakeBlueprint,
    FakeCurriculum,
    FakeJourney,
    FakeMission,
    FakeSession,
    make_full_ports,
    make_request,
)


def test_build_registry_empty():
    reg = CompositionRoot.build_registry()
    assert len(reg) == 0
    assert reg.missing_names() == DEPENDENCY_CHAIN


def test_build_registry_partial():
    reg = CompositionRoot.build_registry(curriculum=FakeCurriculum())
    assert reg.registered_names() == ("curriculum",)


def test_build_registry_full():
    ports = make_full_ports()
    reg = CompositionRoot.build_registry(**ports)
    assert reg.registered_names() == DEPENDENCY_CHAIN
    assert reg.missing_names() == ()


def test_build_registry_require_complete_raises():
    with pytest.raises(CompositionError, match="Incomplete"):
        CompositionRoot.build_registry(
            curriculum=FakeCurriculum(),
            require_complete=True,
        )


def test_build_registry_require_complete_ok():
    ports = make_full_ports()
    reg = CompositionRoot.build_registry(require_complete=True, **ports)
    assert len(reg) == 6


def test_assemble_returns_platform():
    platform = CompositionRoot.assemble(curriculum=FakeCurriculum())
    assert isinstance(platform, EducationPlatform)


def test_assemble_full_workflows():
    ports = make_full_ports()
    platform = CompositionRoot.assemble(**ports)
    resp = platform.generate_daily_missions(make_request())
    assert resp.success is True
    assert resp.missions


def test_assemble_does_not_construct_engines():
    from pathlib import Path

    text = Path(
        "app/application/education_platform/composition_root.py"
    ).read_text(encoding="utf-8")
    for name in (
        "InstructionalBlueprintEngine(",
        "LearningJourneyEngine(",
        "LearningSessionRuntime(",
        "LearningActivityEngine(",
        "MissionEngineV2(",
        "MissionAdapter(",
        "CurriculumGraph(",
    ):
        assert name not in text


def test_assemble_order_independent_injection():
    """Ports can be injected in any keyword order."""
    platform = CompositionRoot.assemble(
        mission=FakeMission(),
        curriculum=FakeCurriculum(),
        activity=FakeActivity(),
        blueprint=FakeBlueprint(),
        session=FakeSession(),
        journey=FakeJourney(),
    )
    assert platform.registry.registered_names() == DEPENDENCY_CHAIN


@pytest.mark.parametrize("omit", list(DEPENDENCY_CHAIN))
def test_assemble_without_each_port(omit):
    ports = make_full_ports()
    ports[omit] = None
    reg = CompositionRoot.build_registry(**ports)
    assert omit not in reg.registered_names()
    assert omit in reg.missing_names()


def test_education_platform_create_delegates():
    platform = EducationPlatform.create(curriculum=FakeCurriculum())
    assert "curriculum" in platform.registry


def test_from_registry():
    reg = CompositionRoot.build_registry(**make_full_ports())
    platform = EducationPlatform.from_registry(reg)
    assert platform.health_status()["platform_status"] == "healthy"
