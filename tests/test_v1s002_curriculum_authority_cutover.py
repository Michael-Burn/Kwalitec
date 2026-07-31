"""V1S-002 curriculum authority cutover and runtime ownership tests."""

from __future__ import annotations

import ast
from pathlib import Path

from app.application.educational_runtime_engine import RuntimeAuthority
from app.application.mission_adapter import (
    V1S002_DISPOSITION as ADAPTER_DISPOSITION,
)
from app.application.mission_adapter import (
    V1S002_STUDENT_SPINE as ADAPTER_SPINE,
)
from app.application.mission_engine import (
    V1S002_DISPOSITION as ME_DISPOSITION,
)
from app.application.mission_engine import (
    V1S002_STUDENT_SPINE as ME_SPINE,
)
from app.application.mission_engine_v2 import (
    V1S002_DISPOSITION as MEV2_DISPOSITION,
)
from app.application.mission_engine_v2 import (
    V1S002_STUDENT_SPINE as MEV2_SPINE,
)
from app.application.platform_integration.flags import (
    DOGFOOD_CURRICULUM_SUBJECTS,
    FounderStudentBridgeFlags,
    effective_runtime_c_allowlist,
    resolve_founder_student_bridge_flags,
)
from app.application.platform_integration.routing import RuntimeRoutingService
from app.services.runtime_ownership import (
    CURRICULUM_AUTHORITY_MATRIX,
    DOGFOOD_SUBJECTS,
    MISSION_RUNTIME_MATRIX,
    MISSION_SPINE,
    RUNTIME_OWNERSHIP_MATRIX,
    TECHNICAL_DEBT_REGISTER,
    curriculum_authority_for_dogfood_subject,
)
from app.services.v1_readiness_dashboard import build_v1_readiness_snapshot
from tests.application.platform_integration.helpers import (
    bridge_flags,
    publish_subject,
)


def test_dogfood_subjects_match_cutover_cohort():
    assert DOGFOOD_CURRICULUM_SUBJECTS == frozenset({"CS1", "CB2", "CM1"})
    assert set(DOGFOOD_SUBJECTS) == set(DOGFOOD_CURRICULUM_SUBJECTS)


def test_effective_allowlist_unions_dogfood_when_enrolment_on():
    flags = FounderStudentBridgeFlags(
        ENABLE_RUNTIME_C_ENROLMENT=True,
        RUNTIME_C_SUBJECT_ALLOWLIST=frozenset({"EXTRA"}),
    )
    assert effective_runtime_c_allowlist(flags) == frozenset(
        {"CS1", "CB2", "CM1", "EXTRA"}
    )
    assert flags.effective_allowlist == effective_runtime_c_allowlist(flags)


def test_effective_allowlist_empty_when_enrolment_off():
    flags = FounderStudentBridgeFlags(
        ENABLE_RUNTIME_C_ENROLMENT=False,
        RUNTIME_C_SUBJECT_ALLOWLIST=frozenset({"CS1"}),
    )
    assert effective_runtime_c_allowlist(flags) == frozenset({"CS1"})


def test_routing_dogfood_cutover_from_ifoa_catalogue(ctx):
    publish_subject("CS1", title="Actuarial Statistics")
    router = RuntimeRoutingService(flags=bridge_flags())
    decision = router.resolve(subject_code="CS1", category_code="IFoA")
    assert decision.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
    assert decision.reason == "dogfood_curriculum_cutover"
    assert "CS1" in decision.flags_snapshot["EFFECTIVE_RUNTIME_C_ALLOWLIST"]


def test_routing_non_dogfood_legacy_stays_runtime_a(ctx):
    publish_subject("CS1X")
    router = RuntimeRoutingService(flags=bridge_flags())
    decision = router.resolve(subject_code="CS1X", category_code="IFoA")
    assert decision.runtime_authority == RuntimeAuthority.JSON_BUNDLED
    assert decision.reason == "legacy_catalogue_defaults_to_runtime_a"


def test_routing_dogfood_without_package_stays_json(ctx):
    router = RuntimeRoutingService(flags=bridge_flags())
    decision = router.resolve(subject_code="CB2", category_code="IFoA")
    assert decision.runtime_authority == RuntimeAuthority.JSON_BUNDLED
    assert decision.reason == "no_active_published_package"


def test_curriculum_authority_helper():
    assert (
        curriculum_authority_for_dogfood_subject(
            "CS1",
            has_published_package=True,
            runtime_c_enrolment_enabled=True,
        )
        == "published_curriculum"
    )
    assert (
        curriculum_authority_for_dogfood_subject(
            "CS1",
            has_published_package=False,
            runtime_c_enrolment_enabled=True,
        )
        == "json_bundled"
    )


def test_mission_packages_marked_off_student_spine():
    assert MEV2_DISPOSITION == "ARCHIVE"
    assert ADAPTER_DISPOSITION == "ARCHIVE"
    assert ME_DISPOSITION == "DEPRECATED"
    assert MEV2_SPINE is False
    assert ADAPTER_SPINE is False
    assert ME_SPINE is False


def test_presentation_student_does_not_import_archived_mission_engines():
    """Static guard: student presentation must not import ARCHIVE packages."""
    root = Path(__file__).resolve().parents[1] / "app" / "presentation" / "student"
    forbidden = (
        "app.application.mission_engine_v2",
        "app.application.mission_adapter",
        "app.application.mission_engine.engine",
    )
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(alias.name.startswith(f) for f in forbidden):
                        offenders.append(f"{path}:{alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                if any(node.module.startswith(f) for f in forbidden):
                    offenders.append(f"{path}:{node.module}")
    assert offenders == []


def test_v1_readiness_snapshot_includes_ownership_sections():
    snapshot = build_v1_readiness_snapshot()
    assert snapshot.programme in {"V1S-002", "V1S-003"}
    assert len(snapshot.curriculum_authority) == len(CURRICULUM_AUTHORITY_MATRIX)
    assert len(snapshot.mission_runtime) == len(MISSION_RUNTIME_MATRIX)
    assert len(snapshot.runtime_ownership) == len(RUNTIME_OWNERSHIP_MATRIX)
    assert len(snapshot.technical_debt) == len(TECHNICAL_DEBT_REGISTER)
    assert snapshot.mission_spine == MISSION_SPINE
    assert any(
        e.status == "ARCHIVE" for e in snapshot.mission_runtime
    )


def test_umbrella_flag_still_resolves():
    flags = resolve_founder_student_bridge_flags(
        environ={"KWALITEC_FOUNDER_STUDENT_BRIDGE": "1"}
    )
    assert flags.ENABLE_RUNTIME_C_ENROLMENT is True
    assert "CS1" in flags.effective_allowlist
