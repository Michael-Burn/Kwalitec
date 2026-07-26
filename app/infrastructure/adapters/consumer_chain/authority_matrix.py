"""Twin × Authority flag matrix validation (EP-002.3).

Verifies expected Experience TwinPort routing and build_* availability
for each Soak Plan cell. Observational only — no HTTP cutover.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain import soak_telemetry as telemetry
from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    CELL_TWIN_OFF_AUTHORITY_ENV,
    CELL_TWIN_OFF_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_ON,
    TWINPORT_EXPERIENCE,
    TWINPORT_FOUNDATION_AUTHORITY,
    FlagMatrixCell,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry

CompositionFactory = Callable[..., tuple[Any, Any]]


def classify_twin_port(twin: Any) -> str:
    """Classify Experience TwinPort implementation for matrix / rollback."""
    if twin is None:
        return "none"
    name = type(twin).__name__
    adapter_id = getattr(twin, "ADAPTER_ID", None) or getattr(
        twin, "component_id", None
    )
    if adapter_id == "student_twin_foundation_authority":
        return TWINPORT_FOUNDATION_AUTHORITY
    if name == TWINPORT_FOUNDATION_AUTHORITY:
        return TWINPORT_FOUNDATION_AUTHORITY
    if name == TWINPORT_EXPERIENCE or "ExperienceTwin" in name:
        return TWINPORT_EXPERIENCE
    return name


def _build_apis_probeable(twin_resolved: bool) -> bool:
    """build_* are Twin-gated; available only when Twin resolves ON."""
    return bool(twin_resolved)


def evaluate_matrix_cell(
    *,
    cell_id: str,
    twin_env: bool,
    authority_env: bool,
    composition_factory: CompositionFactory | None = None,
    base_environ: dict[str, str] | None = None,
) -> FlagMatrixCell:
    """Evaluate one Twin × Authority matrix cell against composition routing."""
    from app.infrastructure.adapters.student_experience.composition import (
        build_production_experience,
    )

    factory = composition_factory or build_production_experience
    env = {
        **dict(base_environ or {}),
        "KWALITEC_DIGITAL_TWIN": "1" if twin_env else "0",
        "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1" if authority_env else "0",
    }
    flags = resolve_v2_feature_flags(environ=env)
    twin_resolved = bool(flags.ENABLE_DIGITAL_TWIN)
    authority_resolved = bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY)
    comp, _service = factory(flags=flags)
    port_kind = classify_twin_port(getattr(comp, "twin", None))
    authority_flag = bool(getattr(comp, "twin_authority_enabled", False))
    details: list[str] = []

    expected_authority = twin_env and authority_env
    expected_port = (
        TWINPORT_FOUNDATION_AUTHORITY
        if expected_authority
        else TWINPORT_EXPERIENCE
    )

    ok = True
    if twin_resolved != twin_env:
        ok = False
        details.append("FAIL:twin_resolved_mismatch")
    else:
        details.append("twin_resolved_ok")

    if authority_resolved != expected_authority:
        ok = False
        details.append("FAIL:authority_resolved_mismatch")
    else:
        details.append("authority_resolved_ok")

    if authority_flag != authority_resolved:
        ok = False
        details.append("FAIL:composition_authority_flag_mismatch")
    else:
        details.append("composition_authority_flag_ok")

    if port_kind != expected_port:
        # Authority ON with Foundation missing may fall back — still fail-open.
        if expected_authority and port_kind == TWINPORT_EXPERIENCE:
            details.append("authority_fail_open_to_experience_twin")
            twin_foundation = getattr(comp, "twin_foundation", None)
            if twin_foundation is None:
                details.append("foundation_absent_fail_open_accepted")
            else:
                ok = False
                details.append("FAIL:authority_on_but_experience_twin_port")
        else:
            ok = False
            details.append(f"FAIL:unexpected_twin_port:{port_kind}")
    else:
        details.append(f"twin_port_ok:{port_kind}")

    # Demo seed must not run under Authority (no Twin theatre).
    seed_demo = bool(getattr(comp, "_seed_demo", True))
    if authority_resolved and seed_demo:
        ok = False
        details.append("FAIL:demo_seed_enabled_under_authority")
    elif authority_resolved:
        details.append("demo_seed_disabled_under_authority")

    return FlagMatrixCell(
        cell_id=cell_id,
        twin_env=twin_env,
        authority_env=authority_env,
        twin_resolved=twin_resolved,
        authority_resolved=authority_resolved,
        twin_port_kind=port_kind,
        build_apis_available=_build_apis_probeable(twin_resolved),
        ok=ok,
        details=tuple(details),
    )


def run_authority_matrix(
    *,
    composition_factory: CompositionFactory | None = None,
    base_environ: dict[str, str] | None = None,
    structured: StructuredLogger | None = None,
    events: EventRegistry | None = None,
) -> tuple[FlagMatrixCell, ...]:
    """Run Soak Plan cells A–D and emit matrix telemetry."""
    sink = structured or StructuredLogger("kwalitec.consumer_chain.soak")
    registry = events if events is not None else EventRegistry()
    specs = (
        (CELL_TWIN_OFF_AUTHORITY_OFF, False, False),
        (CELL_TWIN_OFF_AUTHORITY_ENV, False, True),
        (CELL_TWIN_ON_AUTHORITY_OFF, True, False),
        (CELL_TWIN_ON_AUTHORITY_ON, True, True),
    )
    cells: list[FlagMatrixCell] = []
    for cell_id, twin_env, authority_env in specs:
        cell = evaluate_matrix_cell(
            cell_id=cell_id,
            twin_env=twin_env,
            authority_env=authority_env,
            composition_factory=composition_factory,
            base_environ=base_environ,
        )
        cells.append(cell)
        telemetry.emit_matrix_cell(
            structured=sink,
            events=registry,
            cell=cell.to_canonical_dict(),
        )
    return tuple(cells)


def verify_authority_fail_open(
    *,
    fallback: Any,
) -> tuple[bool, tuple[str, ...]]:
    """Confirm Authority port falls back when Foundation assemble fails."""
    from app.infrastructure.adapters.digital_twin.authority import (
        StudentTwinFoundationAuthorityPort,
    )

    details: list[str] = []

    class _FailingFoundation:
        def is_enabled(self) -> bool:
            return True

        def assemble(self, student_id: str):  # noqa: ANN001
            raise RuntimeError("forced_assemble_failure")

    port = StudentTwinFoundationAuthorityPort(
        foundation=_FailingFoundation(),  # type: ignore[arg-type]
        fallback=fallback,
        enabled=True,
    )
    summary = port.get_learner_summary("soak-fail-open")
    if summary is None:
        details.append("FAIL:fail_open_returned_none")
        return False, tuple(details)
    details.append("fail_open_summary_present")
    details.append("authority_fail_open_ok")
    return True, tuple(details)


__all__ = [
    "classify_twin_port",
    "evaluate_matrix_cell",
    "run_authority_matrix",
    "verify_authority_fail_open",
]
