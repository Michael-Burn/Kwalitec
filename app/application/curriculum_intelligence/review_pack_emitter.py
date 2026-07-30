"""Educational Review Pack emitter (EI-001D)."""

from __future__ import annotations

import json
from uuid import uuid4

from app.application.curriculum_intelligence.decision_quality import (
    summarise_decision_ledger,
)
from app.domain.curriculum_intelligence.certification import (
    CertificationReport,
    CertifiedCurriculumSnapshot,
)
from app.domain.curriculum_intelligence.decision_ledger import DecisionLedgerEntry
from app.domain.curriculum_intelligence.generation import (
    CurriculumGenerationSnapshot,
    RegressionReport,
    purpose_for_index,
)
from app.domain.curriculum_intelligence.review_pack import (
    EducationalReviewPack,
    GenerationComparisonRow,
)

_OBJECTIVE_KINDS = frozenset({"learning_objective", "objective"})
_TOPIC_KINDS = frozenset({"topic", "subtopic", "concept"})
_CHAPTER_KINDS = frozenset({"chapter", "module"})


class ReviewPackEmitter:
    """Build generation-aware Educational Review Pack artefacts."""

    def emit(
        self,
        *,
        chain_id: str,
        workspace_id: str,
        snapshots: tuple[CurriculumGenerationSnapshot, ...],
        decision_ledger: tuple[DecisionLedgerEntry, ...],
        regression_reports: tuple[RegressionReport, ...],
        certification_report: CertificationReport | None,
        created_at_iso: str,
        pack_id: str | None = None,
    ) -> EducationalReviewPack:
        """Generate the full Review Pack for an engine run."""
        comparison = tuple(
            GenerationComparisonRow(
                generation_index=s.generation_index,
                generation_id=s.generation_id,
                purpose=s.generation.purpose or purpose_for_index(s.generation_index),
                metrics=s.metrics,
                active_nodes=s.metrics.active_node_count or len(s.active_nodes()),
                rejected_nodes=s.metrics.rejected_node_count
                or len(s.rejected_nodes),
                generation_hash=s.generation_hash,
            )
            for s in sorted(snapshots, key=lambda x: x.generation_index)
        )
        summary = summarise_decision_ledger(chain_id, decision_ledger)
        head = snapshots[-1] if snapshots else None
        coverage_matrix = self._coverage_matrix(head, decision_ledger)
        hierarchy_report = self._hierarchy_report(head)
        evidence_report = self._evidence_report(head, decision_ledger)
        artefacts = self._markdown_artefacts(
            comparison=comparison,
            summary=summary,
            coverage_matrix=coverage_matrix,
            hierarchy_report=hierarchy_report,
            evidence_report=evidence_report,
            regression_reports=regression_reports,
            certification_report=certification_report,
            decision_ledger=decision_ledger,
        )
        return EducationalReviewPack(
            pack_id=pack_id or f"pack-{uuid4().hex[:12]}",
            chain_id=chain_id,
            workspace_id=workspace_id,
            created_at_iso=created_at_iso,
            generation_comparison=comparison,
            decision_summary=summary,
            coverage_matrix=coverage_matrix,
            hierarchy_report=hierarchy_report,
            evidence_report=evidence_report,
            decision_ledger_summary=summary,
            regression_report=regression_reports,
            certification_report=certification_report,
            artefacts_markdown=artefacts,
        )

    def emit_for_certified(
        self,
        certified: CertifiedCurriculumSnapshot,
        *,
        workspace_id: str,
        snapshots: tuple[CurriculumGenerationSnapshot, ...],
        regression_reports: tuple[RegressionReport, ...],
        created_at_iso: str,
    ) -> EducationalReviewPack:
        """Convenience for a CertifiedCurriculumSnapshot head."""
        return self.emit(
            chain_id=certified.chain_id,
            workspace_id=workspace_id,
            snapshots=snapshots,
            decision_ledger=certified.decision_ledger,
            regression_reports=regression_reports,
            certification_report=certified.report,
            created_at_iso=created_at_iso,
        )

    def write_to_directory(
        self, pack: EducationalReviewPack, directory: str
    ) -> tuple[str, ...]:
        """Write markdown artefacts to ``directory``; return written paths."""
        from pathlib import Path

        root = Path(directory)
        root.mkdir(parents=True, exist_ok=True)
        written: list[str] = []
        readme = (
            f"# Educational Review Pack\n\n"
            f"Chain: `{pack.chain_id}`  \n"
            f"Workspace: `{pack.workspace_id}`  \n"
            f"Created: {pack.created_at_iso}\n\n"
            "## Artefacts\n\n"
            + "\n".join(f"- `{name}`" for name in pack.artefact_names)
            + "\n"
        )
        readme_path = root / "README.md"
        readme_path.write_text(readme, encoding="utf-8")
        written.append(str(readme_path))
        for name, body in sorted(pack.artefacts_markdown.items()):
            path = root / name
            path.write_text(body, encoding="utf-8")
            written.append(str(path))
        return tuple(written)

    def _coverage_matrix(
        self,
        head: CurriculumGenerationSnapshot | None,
        ledger: tuple[DecisionLedgerEntry, ...],
    ) -> dict[str, object]:
        covered = sum(1 for e in ledger if e.decision_type.value == "covered")
        missing = sum(1 for e in ledger if e.decision_type.value == "missing")
        unexpected = sum(1 for e in ledger if e.decision_type.value == "unexpected")
        report_nodes = []
        if head is not None:
            report_nodes = [
                n for n in head.nodes if n.kind == "coverage_report" and n.active
            ]
        attrs: dict[str, str] = {}
        if report_nodes:
            attrs = dict(report_nodes[0].attributes)
        covered_val = attrs.get("covered") or attrs.get("coverage_covered") or covered
        missing_val = attrs.get("missing") or attrs.get("coverage_missing") or missing
        unexpected_val = (
            attrs.get("unexpected") or attrs.get("coverage_unexpected") or unexpected
        )
        hierarchy_consistent = attrs.get("hierarchy_consistent") or attrs.get(
            "coverage_hierarchy_consistent", "unknown"
        )
        return {
            "covered": int(covered_val),
            "missing": int(missing_val),
            "unexpected": int(unexpected_val),
            "completeness": (
                head.metrics.coverage if head is not None else 0.0
            ),
            "hierarchy_consistent": hierarchy_consistent,
            "source": "coverage_report_node" if report_nodes else "decision_ledger",
        }

    def _hierarchy_report(
        self, head: CurriculumGenerationSnapshot | None
    ) -> dict[str, object]:
        if head is None:
            return {
                "chapters": 0,
                "topics": 0,
                "objectives": 0,
                "parent_justification_failures": (),
                "role_chain_ok": False,
            }
        active = head.active_nodes()
        by_id = {n.node_id: n for n in active}
        failures: list[str] = []
        for node in active:
            if node.parent_node_id and node.parent_node_id not in by_id:
                failures.append(f"{node.node_id}: missing parent {node.parent_node_id}")
        return {
            "chapters": sum(1 for n in active if n.kind in _CHAPTER_KINDS),
            "topics": sum(1 for n in active if n.kind in _TOPIC_KINDS),
            "objectives": sum(1 for n in active if n.kind in _OBJECTIVE_KINDS),
            "hierarchy_score": head.metrics.hierarchy,
            "parent_justification_failures": tuple(failures),
            "role_chain_ok": len(failures) == 0 and head.metrics.hierarchy >= 0.5,
        }

    def _evidence_report(
        self,
        head: CurriculumGenerationSnapshot | None,
        ledger: tuple[DecisionLedgerEntry, ...],
    ) -> dict[str, object]:
        grade_counts: dict[str, int] = {}
        for entry in ledger:
            key = entry.evidence_grade.value
            grade_counts[key] = grade_counts.get(key, 0) + 1
        low_conf = []
        if head is not None:
            low_conf = [
                n.node_id
                for n in head.active_nodes()
                if n.confidence.score < 0.6
            ]
        return {
            "evidence_quality": (
                head.metrics.evidence_quality if head is not None else 0.0
            ),
            "grade_counts": grade_counts,
            "ledger_entries": len(ledger),
            "low_confidence_nodes": tuple(low_conf[:50]),
            "low_confidence_share": (
                head.metrics.low_confidence_share if head is not None else 0.0
            ),
        }

    def _markdown_artefacts(
        self,
        *,
        comparison: tuple[GenerationComparisonRow, ...],
        summary,
        coverage_matrix: dict[str, object],
        hierarchy_report: dict[str, object],
        evidence_report: dict[str, object],
        regression_reports: tuple[RegressionReport, ...],
        certification_report: CertificationReport | None,
        decision_ledger: tuple[DecisionLedgerEntry, ...],
    ) -> dict[str, str]:
        lines = [
            "# Generation comparison\n",
            "| Gen | Purpose | Cov | Hier | Noise | Gran | Evid | Conf |",
            "|---:|---|---:|---:|---:|---:|---:|---:|",
        ]
        for row in comparison:
            m = row.metrics
            lines.append(
                f"| {row.generation_index} | {row.purpose} | "
                f"{m.coverage:.4f} | {m.hierarchy:.4f} | {m.noise:.4f} | "
                f"{m.granularity:.4f} | {m.evidence_quality:.4f} | "
                f"{m.confidence:.4f} |"
            )
        gen_cmp = "\n".join(lines) + "\n"

        decision_summary_md = (
            "# Decision summary\n\n"
            f"- Entries: {summary.entry_count}\n"
            f"- Accepted: {summary.accepted_count}\n"
            f"- Warnings: {summary.warning_count}\n"
            f"- Rejected: {summary.rejected_count}\n"
            f"- Mean confidence: {summary.mean_confidence:.4f}\n"
            f"- Mean reasoning confidence: {summary.mean_reasoning_confidence:.4f}\n"
            f"- Mean evidence weight: {summary.mean_evidence_weight:.4f}\n\n"
            "## By type\n\n"
            + "\n".join(f"- `{k}`: {v}" for k, v in summary.by_type)
            + "\n\n## By generation\n\n"
            + "\n".join(f"- Gen {g}: {c}" for g, c in summary.by_generation)
            + "\n"
        )

        coverage_md = (
            "# Coverage matrix\n\n```json\n"
            + json.dumps(coverage_matrix, indent=2, sort_keys=True)
            + "\n```\n"
        )
        hierarchy_md = (
            "# Hierarchy report\n\n```json\n"
            + json.dumps(hierarchy_report, indent=2, sort_keys=True)
            + "\n```\n"
        )
        evidence_md = (
            "# Evidence report\n\n```json\n"
            + json.dumps(evidence_report, indent=2, sort_keys=True)
            + "\n```\n"
        )

        ledger_lines = [
            "# Decision Ledger summary\n",
            f"Total entries: {len(decision_ledger)}\n",
            "| Decision ID | Gen | Type | Policy | Grade | Confidence | Outcome |",
            "|---|---:|---|---|---|---:|---|",
        ]
        for entry in decision_ledger[:200]:
            ledger_lines.append(
                f"| `{entry.decision_id}` | {entry.generation_index} | "
                f"{entry.decision_type.value} | `{entry.policy_id}` | "
                f"{entry.evidence_grade.value} | {entry.confidence:.2f} | "
                f"{entry.decision_outcome.value} |"
            )
        ledger_md = "\n".join(ledger_lines) + "\n"

        reg_lines = ["# Regression report\n"]
        if not regression_reports:
            reg_lines.append("No regression reports recorded.\n")
        for report in regression_reports:
            status = "ACCEPTED" if report.accepted else "REJECTED"
            reg_lines.append(
                f"## `{report.report_id}` — {status}\n\n"
                f"- Candidate: `{report.candidate_generation_id}`\n"
                f"- Reason: {report.reason}\n"
                f"- Gate failures: {', '.join(report.gate_failures) or 'none'}\n"
            )
        regression_md = "\n".join(reg_lines)

        if certification_report is None:
            cert_md = "# Certification report\n\nNot certified in this pack.\n"
        else:
            d = certification_report.decision
            cert_md = (
                "# Certification report\n\n"
                f"- Status: **{d.outcome.value}**\n"
                f"- Quality Score: {d.quality_score}\n"
                f"- Coverage: {d.coverage}\n"
                f"- Hierarchy Score: {d.hierarchy_score}\n"
                f"- Granularity Score: {d.granularity_score}\n"
                f"- Evidence Quality: {d.evidence_quality}\n"
                f"- Confidence: {d.confidence}\n"
                f"- Reasoning Confidence: {d.reasoning_confidence}\n"
                f"- Decision Quality: {d.decision_quality}\n\n"
                "## Hard gate failures\n\n"
                + (
                    "\n".join(f"- {f}" for f in d.hard_gate_failures)
                    or "- none"
                )
                + "\n\n## Warnings\n\n"
                + ("\n".join(f"- {w}" for w in d.warnings) or "- none")
                + "\n\n## Decision quality vector\n\n```json\n"
                + json.dumps(
                    certification_report.decision_quality.as_vector(),
                    indent=2,
                    sort_keys=True,
                )
                + "\n```\n"
            )

        return {
            "01_generation_comparison.md": gen_cmp,
            "02_decision_summary.md": decision_summary_md,
            "03_coverage_matrix.md": coverage_md,
            "04_hierarchy_report.md": hierarchy_md,
            "05_evidence_report.md": evidence_md,
            "06_decision_ledger_summary.md": ledger_md,
            "07_regression_report.md": regression_md,
            "08_certification_report.md": cert_md,
        }
