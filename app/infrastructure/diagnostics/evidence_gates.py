"""Product Strategy evidence gates report for Version 2 cutover (ADR-007 #5)."""

from __future__ import annotations

from dataclasses import dataclass

from app.infrastructure.diagnostics.dual_run import DualRunStatus, build_dual_run_status


@dataclass(frozen=True)
class EvidenceGateItem:
    """One evidence gate with current technical readiness hint."""

    code: str
    title: str
    description: str
    technical_ready: bool
    evidence_required: str


@dataclass(frozen=True)
class EvidenceGatesReport:
    """Ops-facing evidence gate checklist — does not invent educational proof."""

    items: tuple[EvidenceGateItem, ...]
    dual_run_label: str
    all_technical_ready: bool
    cutover_blocked: bool
    notes: tuple[str, ...]


def build_evidence_gates_report(
    *,
    dual_run: DualRunStatus | None = None,
) -> EvidenceGatesReport:
    """Build the Product Strategy / ADR-007 evidence gate checklist."""
    status = dual_run or build_dual_run_status()
    student_on = status.student_experience_enabled
    items = (
        EvidenceGateItem(
            code="persistence_dual_run",
            title="V2 persistence stable in dual-run",
            description=(
                "Experience/session aggregates survive restart on Postgres."
            ),
            technical_ready=status.durable_store and student_on,
            evidence_required=(
                "Production dual-run soak without data loss "
                "or dual-truth defects."
            ),
        ),
        EvidenceGateItem(
            code="explainable_path",
            title="Explainable Twin → Adaptive → Mission path",
            description=(
                "Student Home and Session show authority-backed next actions."
            ),
            technical_ready=status.engines_injected and student_on,
            evidence_required=(
                "Internal Alpha sessions with traceable "
                "recommendation explanations."
            ),
        ),
        EvidenceGateItem(
            code="no_dual_authority",
            title="No unresolved dual-authority defects",
            description=(
                "Adaptive Decision remains sole next-action authority "
                "on V2 paths."
            ),
            technical_ready=status.engines_injected,
            evidence_required=(
                "Defect log empty for competing Twin/recommendation "
                "authorities."
            ),
        ),
        EvidenceGateItem(
            code="studio_operable",
            title="Founder Studio operable",
            description=(
                "Curriculum review / validation / publication works "
                "via Studio UI."
            ),
            technical_ready=True,
            evidence_required=(
                "Founder can publish a curriculum without code changes."
            ),
        ),
        EvidenceGateItem(
            code="product_evidence",
            title="Product Strategy evidence gates",
            description=(
                "Measurable gains in consistency, revision quality, "
                "or efficiency."
            ),
            technical_ready=False,
            evidence_required=(
                "Internal Alpha metrics + Vision Journal themes "
                "before sole runtime."
            ),
        ),
        EvidenceGateItem(
            code="retirement_runbook",
            title="V2-020 retirement runbook ready",
            description="Explicit cutover steps documented and rehearsed.",
            technical_ready=True,
            evidence_required=(
                "Runbook dry-run completed; SOLE_RUNTIME only after "
                "all gates pass."
            ),
        ),
    )
    technical = all(
        i.technical_ready for i in items if i.code != "product_evidence"
    )
    return EvidenceGatesReport(
        items=items,
        dual_run_label=status.label,
        all_technical_ready=technical,
        cutover_blocked=not status.sole_runtime,
        notes=(
            "Technical readiness is not educational proof.",
            "Do not set KWALITEC_V2_SOLE_RUNTIME until product evidence "
            "is recorded.",
            f"Current dual-run posture: {status.label}.",
        ),
    )
