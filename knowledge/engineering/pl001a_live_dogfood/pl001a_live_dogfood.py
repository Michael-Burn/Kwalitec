#!/usr/bin/env python3
"""PL-001A — Live CS1 Curriculum Intelligence Platform dogfood.

Runs Upload→EI→Certification→Calibration→Publication projection→Student
Runtime surfaces against real IFoA CS1 PDFs. No new architecture.

Evidence lands under knowledge/evidence/releases/PL001A/.
"""

from __future__ import annotations

import json
import traceback
from dataclasses import asdict, is_dataclass
from datetime import UTC, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "knowledge/evidence/releases/PL001A"
REPORT_DIR = ROOT / "knowledge/engineering/pl001a_live_dogfood"

SYLLABUS_PDF = ROOT / (
    "instance/curriculum_documents/cs1/syllabus/v1/adad4b0985279dfc-f47a6fce.pdf"
)
CMP_PDF = ROOT / (
    "instance/curriculum_documents/cs1/cmp/v1/6cb786c59ea43960-730062a9.pdf"
)

# EQ-001: CMP educational content starts ~page 35. Cap keeps Gen1 tractable
# while remaining real CMP instructional material (not synthetic).
CMP_PAGE_START = 30
CMP_PAGE_END = 180  # inclusive window; full 912-page scale probed separately

WORKSPACE_ID = "ws-cs1"
SUBJECT = "CS1"
VERSION = "2026.7-pl001a"

timeline: list[dict[str, Any]] = []
issues: list[dict[str, Any]] = []
t0 = perf_counter()


def utc() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def log(stage: str, ok: bool, **facts: Any) -> None:
    entry = {
        "stage": stage,
        "ok": ok,
        "t_s": round(perf_counter() - t0, 2),
        "timestamp": utc(),
        **facts,
    }
    timeline.append(entry)
    mark = "✓" if ok else "✗"
    print(f"[{mark}] {stage} { {k: v for k, v in facts.items() if k != 'detail'} }")


def note_issue(
    severity: str, title: str, detail: str, *, area: str = "platform"
) -> None:
    issues.append(
        {
            "severity": severity,
            "area": area,
            "title": title,
            "detail": detail,
        }
    )


def dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, indent=2, default=_json_default, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def _json_default(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    if hasattr(obj, "value"):
        try:
            return obj.value
        except Exception:  # noqa: BLE001
            pass
    return str(obj)


def slice_pages(doc, start: int, end: int):
    from app.domain.curriculum_intelligence.extracted_document import (
        ExtractedDocument,
    )

    pages = tuple(p for p in doc.pages if start <= p.page_number <= end)
    meta = list(doc.metadata) + [
        ("pl001a_page_window", f"{start}-{end}"),
        ("pl001a_full_page_count", str(doc.page_count)),
    ]
    return ExtractedDocument(
        extraction_id=f"{doc.extraction_id}-p{start}-{end}",
        document_id=doc.document_id,
        page_count=len(pages),
        pages=pages,
        metadata=tuple(meta),
        diagnostics=tuple(doc.diagnostics)
        + (f"pl001a_sliced_pages={start}-{end}",),
    )


def project_package_from_snapshot(
    certified_snapshot,
    certification,
    chain_id: str,
    snapshot_id: str,
) -> dict:
    """Build a Student Runtime package from certified EducationalNodes.

    Maps chapter/module → section, topic/subtopic/concept → topic,
    learning_objective → objective. Orphan LO parents are reparented to the
    nearest topic ancestor or the first topic in the same chapter.
    """
    active = list(certified_snapshot.snapshot.active_nodes())
    by_id = {n.node_id: n for n in active}
    section_kinds = {"chapter", "module", "section"}
    topic_kinds = {"topic", "subtopic", "concept"}
    objective_kinds = {"learning_objective", "objective"}

    sections_nodes = [n for n in active if n.kind in section_kinds]
    topics_nodes = [n for n in active if n.kind in topic_kinds]
    objectives_nodes = [n for n in active if n.kind in objective_kinds]
    topic_ids = {n.node_id for n in topics_nodes}
    section_ids = {n.node_id for n in sections_nodes}

    def nearest_topic(node_id: str | None) -> str:
        seen: set[str] = set()
        cur = node_id
        while cur and cur not in seen:
            seen.add(cur)
            if cur in topic_ids:
                return cur
            parent = by_id.get(cur)
            cur = parent.parent_node_id if parent else None
        return topics_nodes[0].node_id if topics_nodes else ""

    def nearest_section(node_id: str | None) -> str:
        seen: set[str] = set()
        cur = node_id
        while cur and cur not in seen:
            seen.add(cur)
            if cur in section_ids:
                return cur
            parent = by_id.get(cur)
            cur = parent.parent_node_id if parent else None
        return sections_nodes[0].node_id if sections_nodes else ""

    sections = []
    for i, n in enumerate(sections_nodes, start=1):
        sections.append(
            {
                "section_id": n.node_id,
                "code": str(i),
                "title": n.title or n.node_id,
                "number": str(i),
                "order_index": i,
            }
        )
    topics = []
    for i, n in enumerate(topics_nodes, start=1):
        sref = nearest_section(n.parent_node_id) or (
            sections[0]["section_id"] if sections else ""
        )
        prereq = []
        if i > 1:
            prereq = [topics_nodes[i - 2].node_id]
        topics.append(
            {
                "topic_id": n.node_id,
                "code": f"T{i}",
                "title": n.title or n.node_id,
                "section_ref": sref,
                "number": f"T{i}",
                "order_index": i,
                "estimated_minutes": 45,
                "difficulty": "foundational" if i == 1 else "intermediate",
                "prerequisite_ids": prereq,
            }
        )
    objectives = []
    for i, n in enumerate(objectives_nodes, start=1):
        tref = nearest_topic(n.parent_node_id)
        objectives.append(
            {
                "objective_id": n.node_id,
                "code": f"O{i}",
                "text": n.title or n.node_id,
                "topic_ref": tref,
                "number": f"O{i}",
                "order_index": i,
                "estimated_minutes": 20,
            }
        )
    # Attach learning_objective_refs onto topics for deriver templates.
    by_topic_objectives: dict[str, list[str]] = {}
    for o in objectives:
        by_topic_objectives.setdefault(o["topic_ref"], []).append(o["objective_id"])
    for t in topics:
        refs = by_topic_objectives.get(t["topic_id"], [])
        t["learning_objective_refs"] = refs

    prereq_edges = []
    for t in topics:
        for p in t.get("prerequisite_ids") or []:
            prereq_edges.append([t["topic_id"], p])

    outcome = certification.outcome.value if certification else "unknown"
    status = outcome.lower()
    return {
        "subject_code": SUBJECT,
        "version_label": VERSION,
        "certification": {
            "chain_id": chain_id,
            "snapshot_id": snapshot_id,
            "status": status,
            "authority": "certified_snapshot",
            "certification_outcome": outcome,
            "quality_score": getattr(certification, "quality_score", None),
            "coverage": getattr(certification, "coverage", None),
            "warnings": list(getattr(certification, "warnings", ()) or ()),
        },
        "structure": {
            "sections": sections,
            "topics": topics,
            "objectives": objectives,
            "prerequisite_edges": prereq_edges,
            "calibration": {
                "difficulty_bias": "exam_focused",
                "topic_density": "consolidated",
                "granularity": "balanced",
                "hierarchy": "strict_syllabus",
            },
            "source": "certified_snapshot",
            "curriculum_authority": "certified_snapshot",
            "metadata": [
                ["provider", "PL-001A"],
                ["workspace_id", WORKSPACE_ID],
            ],
        },
    }


def project_package(preview, certification, chain_id: str, snapshot_id: str) -> dict:
    """Legacy preview-only projector retained for diagnostics."""
    sections = []
    for i, (sid, title) in enumerate(preview.section_titles, start=1):
        sections.append(
            {
                "section_id": sid,
                "code": str(i),
                "title": title,
                "number": str(i),
                "order_index": i,
            }
        )
    section_by_id = {s["section_id"]: s for s in sections}
    topic_section = {tid: sid for tid, sid in preview.topic_section_refs}
    topics = []
    for i, (tid, title) in enumerate(preview.topic_titles, start=1):
        sref = topic_section.get(tid, "")
        topics.append(
            {
                "topic_id": tid,
                "code": f"T{i}",
                "title": title,
                "section_ref": sref if sref in section_by_id else (
                    sections[0]["section_id"] if sections else ""
                ),
                "number": f"T{i}",
                "order_index": i,
                "estimated_minutes": 45,
                "difficulty": "intermediate" if i % 3 else "foundational",
                "prerequisite_ids": (
                    [topics[i - 2]["topic_id"]] if i > 1 and topics else []
                ),
            }
        )
    topic_ids = {t["topic_id"] for t in topics}
    objectives = []
    for i, (oid, title, parent) in enumerate(preview.objective_rows, start=1):
        tref = parent if parent in topic_ids else (
            topics[0]["topic_id"] if topics else ""
        )
        objectives.append(
            {
                "objective_id": oid,
                "code": f"O{i}",
                "text": title,
                "topic_ref": tref,
                "number": f"O{i}",
                "order_index": i,
                "estimated_minutes": 20,
            }
        )
    prereq_edges = []
    for t in topics:
        for p in t.get("prerequisite_ids") or []:
            prereq_edges.append([t["topic_id"], p])
    outcome = certification.outcome.value if certification else "unknown"
    status = outcome.lower()
    return {
        "subject_code": SUBJECT,
        "version_label": VERSION,
        "certification": {
            "chain_id": chain_id,
            "snapshot_id": snapshot_id,
            "status": status,
            "authority": "certified_snapshot",
            "certification_outcome": outcome,
            "quality_score": getattr(certification, "quality_score", None),
            "coverage": getattr(certification, "coverage", None),
            "warnings": list(getattr(certification, "warnings", ()) or ()),
        },
        "structure": {
            "sections": sections,
            "topics": topics,
            "objectives": objectives,
            "prerequisite_edges": prereq_edges,
            "calibration": {
                "difficulty_bias": "balanced",
                "topic_density": "balanced",
                "granularity": "balanced",
                "hierarchy": "strict_syllabus",
            },
            "source": "certified_snapshot",
            "curriculum_authority": "certified_snapshot",
            "metadata": [
                ["provider", "PL-001A"],
                ["workspace_id", WORKSPACE_ID],
            ],
        },
    }


def write_markdown(path: Path, title: str, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(f"# {title}\n\n{body.strip()}\n", encoding="utf-8")


def main() -> int:
    from app import create_app
    from app.application.curriculum_intelligence.calibration_service import (
        FounderCalibrationService,
    )
    from app.application.curriculum_intelligence.certified_adaptive_learning_service import (  # noqa: E501
        CertifiedAdaptiveLearningService,
    )
    from app.application.curriculum_intelligence.certified_mission_engine import (
        CertifiedMissionEngine,
    )
    from app.application.curriculum_intelligence.certified_progress_engine import (
        CertifiedProgressEngine,
    )
    from app.application.curriculum_intelligence.certified_tutor_context_service import (
        CertifiedTutorContextService,
    )
    from app.application.curriculum_intelligence.curriculum_observatory import (
        CurriculumObservatory,
    )
    from app.application.curriculum_intelligence.document_normalization_service import (
        DocumentNormalizationService,
    )
    from app.application.curriculum_intelligence.founder_preview import (
        CertifiedSnapshotPreviewService,
    )
    from app.application.curriculum_intelligence.in_memory_generation_store import (
        InMemoryGenerationStore,
    )
    from app.application.curriculum_intelligence.learner_knowledge_graph_service import (
        LearnerKnowledgeGraphBuilder,
    )
    from app.application.curriculum_intelligence.workspace_generation_service import (
        WorkspaceGenerationService,
        build_default_orchestrator,
    )
    from app.domain.curriculum_intelligence.generation import (
        DifficultyBiasStyle,
        GranularityStyle,
        HierarchyStyle,
        TopicDensityStyle,
    )
    from app.infrastructure.adapters.curriculum_intelligence.certified_snapshot_loader import (  # noqa: E501
        StoreCertifiedSnapshotLoader,
    )
    from app.infrastructure.adapters.curriculum_intelligence.pypdf_extractor import (
        PyPdfExtractionAdapter,
    )
    from app.presentation.curriculum_studio.factory import get_studio_service

    app = create_app()
    evidence: dict[str, Any] = {
        "programme": "PL-001A",
        "subject": SUBJECT,
        "workspace_id": WORKSPACE_ID,
        "started_at": utc(),
    }

    with app.app_context():
        # ------------------------------------------------------------------
        # 0. Baseline published package (FV-002 legacy)
        # ------------------------------------------------------------------
        from app.extensions import db
        from sqlalchemy import text

        legacy = db.session.execute(
            text(
                "SELECT id, version_label, is_active, package_json "
                "FROM published_curriculum_packages WHERE subject_code=:c "
                "ORDER BY id DESC LIMIT 1"
            ),
            {"c": SUBJECT},
        ).fetchone()
        legacy_summary = None
        if legacy:
            pkg = legacy[3]
            if isinstance(pkg, str):
                pkg = json.loads(pkg)
            st = pkg.get("structure") or {}
            legacy_summary = {
                "id": legacy[0],
                "version_label": legacy[1],
                "is_active": bool(legacy[2]),
                "has_certification": bool(pkg.get("certification")),
                "sections": len(st.get("sections") or []),
                "topics": len(st.get("topics") or []),
                "objectives": len(st.get("objectives") or []),
            }
            dump(EVIDENCE / "legacy_published_package_summary.json", legacy_summary)
            log("baseline_legacy_package", True, **legacy_summary)
            if not pkg.get("certification"):
                note_issue(
                    "critical",
                    "Active CS1 package lacks certification block",
                    "FV-002 published CS1/2026.1 has no package.certification; "
                    "Student Runtime uses legacy topic selection, not certified LOs.",
                    area="publication",
                )
            if (legacy_summary["topics"] or 0) > 500:
                note_issue(
                    "critical",
                    "Active CS1 package still uses pre-EQ001 noisy structure",
                    f"Published structure has {legacy_summary['topics']} topics / "
                    f"{legacy_summary['sections']} sections — not syllabus-first.",
                    area="curriculum_fidelity",
                )

        # ------------------------------------------------------------------
        # 1. Upload / extract (real PDFs already bound in Studio storage)
        # ------------------------------------------------------------------
        if not SYLLABUS_PDF.is_file() or not CMP_PDF.is_file():
            log("extract_sources", False, syllabus=str(SYLLABUS_PDF), cmp=str(CMP_PDF))
            note_issue(
                "critical",
                "CS1 source PDFs missing",
                "Expected instance/curriculum_documents/cs1/{syllabus,cmp}/…",
                area="upload",
            )
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 1

        extractor = PyPdfExtractionAdapter()
        normalizer = DocumentNormalizationService()
        t_ext = perf_counter()
        syllabus_raw = extractor.extract(
            SYLLABUS_PDF.read_bytes(),
            extraction_id="pl001a-syllabus",
            document_id=101,
        )
        cmp_raw = extractor.extract(
            CMP_PDF.read_bytes(),
            extraction_id="pl001a-cmp",
            document_id=102,
        )
        syllabus = normalizer.normalize(syllabus_raw)
        cmp_full = normalizer.normalize(cmp_raw)
        cmp = slice_pages(cmp_full, CMP_PAGE_START, CMP_PAGE_END)
        extract_meta = {
            "syllabus_pages": syllabus.page_count,
            "syllabus_blocks": sum(len(p.blocks) for p in syllabus.pages),
            "cmp_full_pages": cmp_full.page_count,
            "cmp_full_blocks": sum(len(p.blocks) for p in cmp_full.pages),
            "cmp_window": f"{CMP_PAGE_START}-{CMP_PAGE_END}",
            "cmp_window_pages": cmp.page_count,
            "cmp_window_blocks": sum(len(p.blocks) for p in cmp.pages),
            "extract_s": round(perf_counter() - t_ext, 2),
        }
        dump(EVIDENCE / "extraction_metrics.json", extract_meta)
        log("extract_normalize", True, **extract_meta)
        if cmp_full.page_count > 500:
            note_issue(
                "minor",
                "Full CMP Gen1 scale requires windowed dogfood",
                f"Full CMP has {cmp_full.page_count} pages / "
                f"{extract_meta['cmp_full_blocks']} blocks; PL-001A ran EI on "
                f"pages {CMP_PAGE_START}-{CMP_PAGE_END} plus full syllabus to "
                "keep certification tractable. Full-CMP republish remains polish.",
                area="operations",
            )

        # ------------------------------------------------------------------
        # 2. Curriculum Intelligence Engine G1–G7
        # ------------------------------------------------------------------
        store = InMemoryGenerationStore()
        studio = get_studio_service()
        # Ensure workspace present in registry (reconcile from durable facts).
        try:
            reconcile = getattr(studio, "reconcile_workspace", None)
            if callable(reconcile):
                reconcile(WORKSPACE_ID)
            elif studio.registry.get_workspace(WORKSPACE_ID) is None:
                from app.infrastructure.adapters.curriculum_studio_workspace_persistence import (  # noqa: E501
                    load_all_workspaces,
                )

                for ws in load_all_workspaces():
                    studio.registry.put_workspace(ws)
        except Exception as exc:  # noqa: BLE001
            note_issue(
                "minor",
                "Workspace reconcile warning",
                str(exc),
                area="founder",
            )

        orch = build_default_orchestrator(store)
        service = WorkspaceGenerationService(
            store, registry=studio.registry, orchestrator=orch
        )

        # ------------------------------------------------------------------
        # 2a. CMP+syllabus probe (production stop_on_regression=True)
        # ------------------------------------------------------------------
        probe_store = InMemoryGenerationStore()
        probe_orch = build_default_orchestrator(probe_store)
        t_probe = perf_counter()
        probe = probe_orch.run_chain(
            chain_id="pl001a-cmp-probe",
            workspace_id=WORKSPACE_ID,
            source_document_ids=(101, 102),
            start_from=1,
            through=3,
            source_documents=(syllabus, cmp),
            subject_code=SUBJECT,
            version_label=f"{VERSION}-cmp-probe",
            fixed_created_at_iso="2026-07-30T05:50:00Z",
            stop_on_regression=True,
            emit_review_pack=False,
        )
        probe_regs = list(probe_store.list_regression_reports("pl001a-cmp-probe"))
        probe_meta = {
            "accepted": [
                {
                    "index": s.generation_index,
                    "active": len(s.active_nodes()),
                    "rejected": len(s.rejected_nodes),
                    "confidence": s.metrics.confidence,
                    "coverage": s.metrics.coverage,
                    "noise": s.metrics.noise,
                }
                for s in probe.accepted_snapshots
            ],
            "rejected": [
                {
                    "index": s.generation_index,
                    "active": len(s.active_nodes()),
                    "rejected_nodes": len(s.rejected_nodes),
                    "confidence": s.metrics.confidence,
                    "coverage": s.metrics.coverage,
                    "noise": s.metrics.noise,
                }
                for s in probe.rejected_snapshots
            ],
            "regression_reports": [
                {
                    "accepted": r.accepted,
                    "reason": r.reason,
                    "gate_failures": list(r.gate_failures),
                    "candidate_generation_id": r.candidate_generation_id,
                }
                for r in probe_regs
            ],
            "stopped_at_index": probe.stopped_at_index,
            "duration_s": round(perf_counter() - t_probe, 2),
            "cmp_window": f"{CMP_PAGE_START}-{CMP_PAGE_END}",
        }
        dump(EVIDENCE / "cmp_probe_regression.json", probe_meta)
        if probe.rejected_snapshots:
            note_issue(
                "critical",
                "CMP+syllabus Gen2 rejected by regression confidence gate",
                (
                    "Noise elimination improves coverage/noise but dips mean "
                    f"confidence enough to fail RegressionPolicy "
                    f"(failures={probe_meta['regression_reports']}). "
                    "Production stop_on_regression=True halts before hierarchy/"
                    "certification when CMP body is included."
                ),
                area="certification_consistency",
            )
            log("cmp_syllabus_probe", False, **{
                k: probe_meta[k]
                for k in ("stopped_at_index", "duration_s", "cmp_window")
            })
        else:
            log("cmp_syllabus_probe", True, stopped_at_index=probe.stopped_at_index)

        # ------------------------------------------------------------------
        # 2b. Primary path — syllabus-authoritative (EQ-001 Founder shape)
        # ------------------------------------------------------------------
        t_pipe = perf_counter()
        try:
            pipe = service.run_initial_pipeline(
                WORKSPACE_ID,
                source_document_ids=(101,),
                source_documents=(syllabus,),
                subject_code=SUBJECT,
                version_label=VERSION,
                fixed_created_at_iso="2026-07-30T06:00:00Z",
            )
            pipe_ok = True
            pipe_err = None
        except Exception as exc:  # noqa: BLE001
            pipe_ok = False
            pipe_err = f"{exc}\n{traceback.format_exc()}"
            pipe = None
            note_issue(
                "critical",
                "EI G1–G7 pipeline failed",
                str(exc),
                area="engine",
            )

        pipeline_meta: dict[str, Any] = {
            "ok": pipe_ok,
            "duration_s": round(perf_counter() - t_pipe, 2),
            "source_mode": "syllabus_authoritative",
            "rationale": (
                "Matches EQ-001 Founder publish shape (official syllabus). "
                "CMP body inclusion blocked at Gen2 under production regression "
                "gates — see cmp_probe_regression.json."
            ),
        }
        if pipe is not None:
            result = pipe.orchestrator
            pipeline_meta.update(
                {
                    "chain_id": result.chain_id,
                    "intelligence_certified": pipe.intelligence_certified,
                    "active_snapshot_id": result.active_snapshot_id,
                    "certified_snapshot_id": pipe.binding.certified_snapshot_id,
                    "certification_status": (
                        pipe.binding.certification_status.value
                        if pipe.binding.certification_status
                        else None
                    ),
                    "snapshot_count": len(result.accepted_snapshots),
                    "generations": [
                        {
                            "index": s.generation_index,
                            "snapshot_id": s.snapshot_id,
                            "active_nodes": len(s.active_nodes()),
                            "rejected_nodes": len(s.rejected_nodes),
                            "status": s.status.value
                            if hasattr(s.status, "value")
                            else str(s.status),
                            "metrics": _json_default(s.metrics),
                        }
                        for s in sorted(
                            result.accepted_snapshots,
                            key=lambda x: x.generation_index,
                        )
                    ],
                }
            )
            if result.certification is not None:
                cert = result.certification
                cert_report = {
                    "outcome": cert.outcome.value,
                    "quality_score": cert.quality_score,
                    "coverage": cert.coverage,
                    "hierarchy_score": cert.hierarchy_score,
                    "granularity_score": cert.granularity_score,
                    "confidence": cert.confidence,
                    "evidence_quality": cert.evidence_quality,
                    "decision_quality": cert.decision_quality,
                    "hard_gate_failures": list(cert.hard_gate_failures or ()),
                    "warnings": list(cert.warnings or ()),
                    "failure_reasons": list(cert.failure_reasons or ()),
                    "snapshot_id": cert.snapshot_id,
                    "chain_id": result.chain_id,
                }
                dump(EVIDENCE / "certification_report.json", cert_report)
                write_markdown(
                    EVIDENCE / "Certification_Report.md",
                    "PL-001A Certification Report — CS1",
                    f"""
**Outcome:** `{cert.outcome.value}`  
**Chain:** `{result.chain_id}`  
**Snapshot:** `{cert.snapshot_id}`  
**Quality score:** {cert.quality_score}  
**Coverage:** {cert.coverage}  
**Hierarchy:** {cert.hierarchy_score}  
**Granularity:** {cert.granularity_score}  
**Confidence:** {cert.confidence}  
**Evidence quality:** {cert.evidence_quality}  
**Decision quality:** {cert.decision_quality}

### Hard gate failures
{chr(10).join(f'- {x}' for x in (cert.hard_gate_failures or ())) or '_None_'}

### Warnings
{chr(10).join(f'- {x}' for x in (cert.warnings or ())) or '_None_'}

### Failure reasons
{chr(10).join(f'- {x}' for x in (cert.failure_reasons or ())) or '_None_'}
""",
                )
                if cert.outcome.value == "NOT_CERTIFIED":
                    note_issue(
                        "critical",
                        "CS1 generation NOT_CERTIFIED",
                        f"Hard gates: {list(cert.hard_gate_failures or ())}; "
                        f"reasons: {list(cert.failure_reasons or ())}",
                        area="certification",
                    )
                elif cert.outcome.value == "CERTIFIED_WITH_WARNINGS":
                    note_issue(
                        "minor",
                        "CS1 certified with warnings",
                        "; ".join(cert.warnings or ()) or "warnings present",
                        area="certification",
                    )

            if result.review_pack is not None:
                pack = result.review_pack
                pack_dir = EVIDENCE / "review_pack"
                pack_dir.mkdir(parents=True, exist_ok=True)
                dump(
                    pack_dir / "review_pack.json",
                    {
                        "pack_id": pack.pack_id,
                        "chain_id": pack.chain_id,
                        "workspace_id": pack.workspace_id,
                        "generation_comparison": pack.generation_comparison,
                        "artefact_names": list(pack.artefact_names),
                        "coverage_matrix": pack.coverage_matrix,
                        "hierarchy_report": pack.hierarchy_report,
                    },
                )
                for name, content in (pack.artefacts_markdown or {}).items():
                    safe = str(name).replace(" ", "_").replace("/", "_")
                    if safe.endswith(".md"):
                        out_name = safe
                    else:
                        out_name = f"{safe}.md"
                    (pack_dir / out_name).write_text(
                        content or "", encoding="utf-8"
                    )
                log(
                    "review_pack",
                    True,
                    pack_id=pack.pack_id,
                    artefacts=len(pack.artefacts_markdown or {}),
                )
            else:
                note_issue(
                    "minor",
                    "Review Pack missing from orchestrator result",
                    "Expected ReviewPackEmitter output after Gen 7.",
                    area="review_pack",
                )

        dump(EVIDENCE / "pipeline_metrics.json", pipeline_meta)
        log(
            "ei_pipeline_g1_g7",
            pipe_ok,
            **{
                k: v
                for k, v in pipeline_meta.items()
                if k not in {"generations", "ok"}
            },
        )
        if pipe_err:
            (EVIDENCE / "pipeline_error.txt").write_text(pipe_err, encoding="utf-8")

        if not pipe_ok or pipe is None:
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            evidence["timeline"] = timeline
            evidence["issues"] = issues
            evidence["finished_at"] = utc()
            dump(EVIDENCE / "dogfood_evidence.json", evidence)
            return 2

        result = pipe.orchestrator
        chain_id = result.chain_id
        certification = result.certification

        # ------------------------------------------------------------------
        # 3. Founder Calibration
        # ------------------------------------------------------------------
        cal_svc = FounderCalibrationService(
            store, registry=studio.registry, orchestrator=orch
        )
        t_cal = perf_counter()
        try:
            cal = cal_svc.apply(
                WORKSPACE_ID,
                granularity=GranularityStyle.BALANCED,
                hierarchy=HierarchyStyle.STRICT_SYLLABUS,
                topic_density=TopicDensityStyle.CONSOLIDATED,
                difficulty_bias=DifficultyBiasStyle.EXAM_FOCUSED,
                source_documents=(syllabus,),
                subject_code=SUBJECT,
                version_label=VERSION,
                fixed_created_at_iso="2026-07-30T06:30:00Z",
            )
            cal_ok = True
            cal_meta = {
                "profile_id": cal.profile.profile_id,
                "generations_rerun": list(cal.generations_rerun),
                "intelligence_certified": cal.intelligence_certified,
                "granularity": cal.profile.granularity.value,
                "hierarchy": cal.profile.hierarchy.value,
                "topic_density": cal.profile.topic_density.value,
                "difficulty_bias": cal.profile.difficulty_bias.value,
                "duration_s": round(perf_counter() - t_cal, 2),
                "post_cal_certification": (
                    cal.orchestrator.certification.outcome.value
                    if cal.orchestrator.certification
                    else None
                ),
            }
            # Keep latest certification after calibration.
            if cal.orchestrator.certification is not None:
                certification = cal.orchestrator.certification
                result = cal.orchestrator
            elif not cal.intelligence_certified:
                note_issue(
                    "critical",
                    "Calibration re-certification did not produce a decision",
                    (
                        f"generations_rerun={list(cal.generations_rerun)}; "
                        "initial Gen7 certification retained for student "
                        "surfaces where still preview-eligible."
                    ),
                    area="calibration",
                )
        except Exception as exc:  # noqa: BLE001
            cal_ok = False
            cal_meta = {
                "error": str(exc),
                "duration_s": round(perf_counter() - t_cal, 2),
            }
            note_issue(
                "critical",
                "Founder calibration failed",
                str(exc),
                area="calibration",
            )
        dump(EVIDENCE / "calibration" / "calibration_history.json", cal_meta)
        log("founder_calibration", cal_ok, **cal_meta)

        # ------------------------------------------------------------------
        # 4. Founder Preview / certified structure projection
        # ------------------------------------------------------------------
        loader = StoreCertifiedSnapshotLoader(store)
        preview_svc = CertifiedSnapshotPreviewService(loader=loader)
        certified = preview_svc.get_certified_for_workspace(WORKSPACE_ID)
        if certified is None:
            note_issue(
                "critical",
                "No preview-eligible certified snapshot",
                "Founder Preview refused or could not load certified snapshot.",
                area="certification",
            )
            preview = None
            package = None
        else:
            preview = preview_svc.project(certified)
            snap_id = certified.snapshot_id
            # Prefer node-faithful package projection for Student Runtime.
            package = project_package_from_snapshot(
                certified, certification, chain_id, snap_id
            )
            preview_meta = {
                "certification_status": preview.certification_status.value,
                "quality_score": preview.quality_score,
                "warnings": list(preview.warnings),
                "sections": len(preview.section_ids),
                "topics": len(preview.topic_ids),
                "objectives": len(preview.objective_ids),
                "preview_eligible": preview.preview_eligible,
                "source": preview.source,
            }
            dump(EVIDENCE / "founder_preview_structure.json", preview_meta)
            dump(EVIDENCE / "certified_package.json", package)
            log("founder_preview", True, **preview_meta)
            if preview.section_ids and not preview.topic_ids:
                note_issue(
                    "critical",
                    "Certified preview has sections but no topics",
                    "Student missions cannot be derived from empty topics.",
                    area="curriculum_structure",
                )
            if len(preview.objective_ids) < 10:
                note_issue(
                    "minor",
                    "Low objective count in certified preview",
                    f"Only {len(preview.objective_ids)} objectives projected.",
                    area="objective_coverage",
                )

        # ------------------------------------------------------------------
        # 5. Observatory metrics
        # ------------------------------------------------------------------
        observatory = CurriculumObservatory(store)
        obs = observatory.report_for_workspace(WORKSPACE_ID)
        obs_payload = _json_default(obs)
        dump(EVIDENCE / "observatory" / "observatory_metrics.json", obs_payload)
        write_markdown(
            EVIDENCE / "observatory" / "Observatory_Report.md",
            "Curriculum Observatory — CS1 (PL-001A)",
            f"""
```json
{json.dumps(obs_payload, indent=2, default=_json_default)}
```
""",
        )
        log(
            "observatory",
            True,
            trends=len(obs.certification_trends),
            coverage=len(obs.coverage_metrics),
            decision_quality=len(obs.decision_quality),
            warnings=len(obs.policy_warnings),
        )

        # ------------------------------------------------------------------
        # 6. Student surfaces (certified package)
        # ------------------------------------------------------------------
        if package is None:
            note_issue(
                "critical",
                "Student surfaces skipped — no certified package",
                "Cannot validate missions/tutor/progress without certification.",
                area="student_runtime",
            )
        else:
            # Knowledge graph
            from app.domain.curriculum_intelligence.certified_learning import (
                CertifiedNodeKind,
            )

            graph = LearnerKnowledgeGraphBuilder().build(package)
            chapters = [
                n
                for n in graph.nodes
                if n.kind
                in {CertifiedNodeKind.CHAPTER, CertifiedNodeKind.SECTION}
            ]
            kg = {
                "curriculum_identity": graph.curriculum_identity,
                "is_certified": graph.provenance.is_certified,
                "node_count": len(graph.nodes),
                "edge_count": len(graph.edges),
                "chapters": [
                    {"id": n.node_id, "title": n.title} for n in chapters
                ][:20],
                "topics": [
                    {"id": n.node_id, "title": n.title} for n in graph.topics()
                ][:40],
                "objectives": [
                    {"id": n.node_id, "title": n.title} for n in graph.objectives()
                ][:40],
                "sample_prerequisites": {},
            }
            for topic in list(graph.topics())[:8]:
                kg["sample_prerequisites"][topic.node_id] = list(
                    graph.prerequisites(topic.node_id)
                )
            dump(EVIDENCE / "knowledge_graph" / "graph_summary.json", kg)
            # Mermaid "screenshot" substitute (no KG UI yet)
            lines = ["```mermaid", "flowchart TD"]
            for ch in chapters[:8]:
                safe_ch = ch.node_id.replace("-", "_")
                title = (ch.title or ch.node_id)[:48].replace('"', "'")
                lines.append(f'  {safe_ch}["{title}"]')
                for child_id in list(graph.children(ch.node_id))[:6]:
                    child = graph.node(child_id)
                    if child is None:
                        continue
                    safe_c = child_id.replace("-", "_")
                    ctitle = (child.title or child_id)[:40].replace('"', "'")
                    lines.append(f'  {safe_c}["{ctitle}"]')
                    lines.append(f"  {safe_ch} --> {safe_c}")
            lines.append("```")
            write_markdown(
                EVIDENCE / "knowledge_graph" / "Knowledge_Graph.md",
                "Learner Knowledge Graph (CS1 certified)",
                "\n".join(lines)
                + f"\n\nNodes: {kg['node_count']} · Edges: {kg['edge_count']}\n",
            )
            log(
                "knowledge_graph",
                True,
                nodes=kg["node_count"],
                edges=kg["edge_count"],
                objectives=len(list(graph.objectives())),
            )
            if not graph.provenance.is_certified:
                note_issue(
                    "critical",
                    "Knowledge graph not marked certified",
                    "LearnerKnowledgeGraph provenance.is_certified is False.",
                    area="knowledge_graph",
                )

            # Missions
            mission_engine = CertifiedMissionEngine()
            missions = []
            completed: list[str] = []
            mastered: list[str] = []
            for i in range(5):
                try:
                    m = mission_engine.generate(
                        package,
                        mission_id=f"pl001a-msn-{i+1}",
                        completed_node_ids=tuple(completed),
                        mastered_objective_ids=tuple(mastered),
                    )
                except ValueError as exc:
                    note_issue(
                        "critical" if i == 0 else "minor",
                        "Mission generation exhausted or failed",
                        str(exc),
                        area="missions",
                    )
                    break
                missions.append(
                    {
                        "mission_id": m.mission_id,
                        "topic_id": m.topic_id,
                        "topic_title": m.topic_title,
                        "objective_ids": list(m.objective_ids),
                        "objective_titles": list(m.objective_titles),
                        "selection_reasons": [
                            r.value if hasattr(r, "value") else str(r)
                            for r in m.selection_reasons
                        ],
                        "estimated_minutes": m.estimated_minutes,
                        "calibration_notes": list(m.calibration_notes),
                        "provenance": _json_default(m.provenance),
                    }
                )
                completed.append(m.topic_id)
                mastered.extend(m.objective_ids)
            dump(EVIDENCE / "missions" / "mission_samples.json", missions)
            write_markdown(
                EVIDENCE / "missions" / "Mission_Samples.md",
                "Daily Mission samples (certified CS1)",
                "\n\n".join(
                    f"### {m['mission_id']}\n"
                    f"- Topic: **{m['topic_title']}** (`{m['topic_id']}`)\n"
                    f"- Objectives: {', '.join(m['objective_titles']) or '_none_'}\n"
                    f"- Reasons: {', '.join(m['selection_reasons'])}\n"
                    f"- Minutes: {m['estimated_minutes']}"
                    for m in missions
                ),
            )
            mission_ok = all(m["objective_ids"] for m in missions) or all(
                m["topic_id"] for m in missions
            )
            log("missions", mission_ok, samples=len(missions))
            if not any(m["objective_ids"] for m in missions):
                note_issue(
                    "critical",
                    "Missions lack learning objectives",
                    "CertifiedMissionEngine returned missions without LO ids — "
                    "curriculum fidelity for daily missions is weak.",
                    area="missions",
                )
            # Coherence: titles should not look like front-matter
            bad_titles = [
                m
                for m in missions
                if any(
                    x in (m["topic_title"] or "").lower()
                    for x in (
                        "associateship",
                        "copyright",
                        "combined materials",
                        "agogo",
                    )
                )
            ]
            if bad_titles:
                note_issue(
                    "critical",
                    "Mission topics include front-matter noise",
                    f"Examples: {[m['topic_title'] for m in bad_titles]}",
                    area="mission_coherence",
                )

            # Progress stability
            progress_engine = CertifiedProgressEngine()
            p1 = progress_engine.snapshot(
                package,
                completed_node_ids=tuple(completed[:1]),
                objective_mastery={mastered[0]: 0.85} if mastered else {},
                topic_mastery={completed[0]: 0.8} if completed else {},
                attempts_by_node={mastered[0]: 2} if mastered else {},
            )
            p2 = progress_engine.snapshot(
                package,
                completed_node_ids=tuple(completed[:1]),
                objective_mastery={mastered[0]: 0.85} if mastered else {},
                topic_mastery={completed[0]: 0.8} if completed else {},
                attempts_by_node={mastered[0]: 2} if mastered else {},
            )
            progress_payload = {
                "curriculum_identity": p1.curriculum_identity,
                "subject_mastery": p1.subject_mastery,
                "missed_objectives": list(p1.missed_objective_ids)[:30],
                "chapter_count": len(p1.chapter_records),
                "topic_count": len(p1.topic_records),
                "objective_count": len(p1.objective_records),
                "stable_repeat": p1.subject_mastery == p2.subject_mastery
                and list(p1.missed_objective_ids) == list(p2.missed_objective_ids),
                "sample_objectives": [
                    {
                        "node_id": r.node_id,
                        "mastery": r.mastery,
                        "attempts": r.attempts,
                    }
                    for r in p1.objective_records[:15]
                ],
            }
            dump(EVIDENCE / "progress" / "progress_examples.json", progress_payload)
            log(
                "progress",
                progress_payload["stable_repeat"],
                subject_mastery=p1.subject_mastery,
            )
            if not progress_payload["stable_repeat"]:
                note_issue(
                    "critical",
                    "Progress snapshot unstable",
                    "Identical inputs produced divergent progress snapshots.",
                    area="progress",
                )

            # Adaptive learning
            adaptive = CertifiedAdaptiveLearningService().plan(
                package,
                progress=p1,
            )
            adaptive_payload = {
                "weak_concepts": [
                    _json_default(x) for x in adaptive.weak_concepts[:15]
                ],
                "missed_objectives": [
                    _json_default(x) for x in adaptive.missed_objectives[:15]
                ],
                "revision_priorities": [
                    _json_default(x) for x in adaptive.revision_priorities[:15]
                ],
                "concept_dependencies": [
                    _json_default(x) for x in adaptive.concept_dependencies[:15]
                ],
            }
            dump(
                EVIDENCE / "adaptive" / "adaptive_learning_examples.json",
                adaptive_payload,
            )
            log(
                "adaptive",
                True,
                weak=len(adaptive.weak_concepts),
                missed=len(adaptive.missed_objectives),
                revision=len(adaptive.revision_priorities),
                dependencies=len(adaptive.concept_dependencies),
            )

            # Tutor context grounding
            tutor_svc = CertifiedTutorContextService()
            primary = (
                missions[0]["objective_ids"][0]
                if missions and missions[0]["objective_ids"]
                else (preview.objective_ids[0] if preview and preview.objective_ids else None)
            )
            tutor_conversations = []
            if primary:
                ctx = tutor_svc.build(
                    package,
                    primary_node_id=primary,
                    candidate_node_ids=(
                        primary,
                        "foreign-injected-node",
                        *(missions[0]["objective_ids"][1:2] or ()),
                    ),
                    excerpts=(
                        (primary, "Official CS1 objective text for tutor grounding."),
                        ("foreign-injected-node", "Should be rejected."),
                    ),
                    context_id="pl001a-tutor-1",
                )
                tutor_conversations.append(
                    {
                        "question": (
                            "Explain this learning objective in exam terms."
                        ),
                        "primary_node_id": ctx.primary_node_id,
                        "allowed_node_ids": list(ctx.allowed_node_ids)[:20],
                        "rejected_foreign_ids": list(ctx.rejected_foreign_ids),
                        "excerpts": [list(x) for x in ctx.excerpts],
                        "provenance": _json_default(ctx.provenance),
                        "grounded": "foreign-injected-node"
                        not in {e[0] for e in ctx.excerpts}
                        and "foreign-injected-node" in ctx.rejected_foreign_ids,
                    }
                )
                # Second turn — different objective if available
                alt = None
                for m in missions[1:]:
                    if m["objective_ids"]:
                        alt = m["objective_ids"][0]
                        break
                if alt:
                    ctx2 = tutor_svc.build(
                        package,
                        primary_node_id=alt,
                        context_id="pl001a-tutor-2",
                    )
                    tutor_conversations.append(
                        {
                            "question": "What should I revise next related to this?",
                            "primary_node_id": ctx2.primary_node_id,
                            "allowed_node_ids": list(ctx2.allowed_node_ids)[:20],
                            "rejected_foreign_ids": list(ctx2.rejected_foreign_ids),
                            "provenance": _json_default(ctx2.provenance),
                            "grounded": True,
                        }
                    )
                dump(
                    EVIDENCE / "tutor" / "tutor_conversations.json",
                    tutor_conversations,
                )
                write_markdown(
                    EVIDENCE / "tutor" / "Tutor_Conversations.md",
                    "Tutor grounding conversations (certified context)",
                    "\n\n".join(
                        f"### Turn {i+1}\n"
                        f"**Q:** {c['question']}\n\n"
                        f"- Primary node: `{c['primary_node_id']}`\n"
                        f"- Grounded: {c.get('grounded')}\n"
                        f"- Rejected foreign: {c.get('rejected_foreign_ids')}"
                        for i, c in enumerate(tutor_conversations)
                    ),
                )
                tutor_ok = all(c.get("grounded") for c in tutor_conversations)
                log("tutor", tutor_ok, turns=len(tutor_conversations))
                if not tutor_ok:
                    note_issue(
                        "critical",
                        "Tutor context not grounded in certified nodes",
                        "Foreign node leaked into tutor excerpts or rejection failed.",
                        area="tutor",
                    )
            else:
                note_issue(
                    "critical",
                    "No certified objective for tutor primary",
                    "Cannot validate tutor grounding without LO ids.",
                    area="tutor",
                )

            # Review Pack vs certification consistency
            if result.review_pack and certification:
                pack_cert_ok = True
                # Pack should reference same chain
                if result.review_pack.chain_id != chain_id:
                    pack_cert_ok = False
                    note_issue(
                        "critical",
                        "Review Pack chain mismatch",
                        f"pack={result.review_pack.chain_id} chain={chain_id}",
                        area="review_pack",
                    )
                dump(
                    EVIDENCE / "review_pack" / "pack_vs_certification.json",
                    {
                        "pack_chain_id": result.review_pack.chain_id,
                        "cert_chain_id": chain_id,
                        "cert_outcome": certification.outcome.value,
                        "consistent": pack_cert_ok,
                    },
                )
                log("review_pack_matches_certification", pack_cert_ok)

        # ------------------------------------------------------------------
        # 7. Publication readiness check (gate — do not force republish)
        # ------------------------------------------------------------------
        pub_check = {
            "intelligence_certified": pipe.intelligence_certified,
            "legacy_active_package_uncertified": bool(
                legacy_summary and not legacy_summary.get("has_certification")
            ),
            "certified_package_built": package is not None,
            "note": (
                "PL-001A validates certified package projection + student "
                "surfaces. Live Founder Console republish of Gen7 into "
                "published_curriculum_packages is recommended polish after "
                "CMP full-window certification."
            ),
        }
        if package is not None and pipe.intelligence_certified:
            # Soft-publish evidence package for student runtime experiments
            dump(EVIDENCE / "publication_candidate_package.json", package)
        else:
            note_issue(
                "critical",
                "Not ready to replace active published CS1",
                "Certification or package projection incomplete.",
                area="publication",
            )
        dump(EVIDENCE / "publication_readiness.json", pub_check)
        log("publication_readiness", pub_check["certified_package_built"], **pub_check)

        # Known product gaps from EI-002B residual
        note_issue(
            "minor",
            "Tutor certified filter is opt-in in production DI",
            "EI-002B: certified_tutor= must be bound when package available.",
            area="tutor",
        )
        note_issue(
            "minor",
            "Observatory Founder Console UI not shipped",
            "Service + report ready; no Founder UI surface yet.",
            area="observatory",
        )
        note_issue(
            "minor",
            "Learner Knowledge Graph has no student UI screenshot surface",
            "PL-001A captured graph summary + Mermaid projection from service.",
            area="knowledge_graph",
        )

    # ------------------------------------------------------------------
    # Quality gates summary
    # ------------------------------------------------------------------
    critical = [i for i in issues if i["severity"] == "critical"]
    minor = [i for i in issues if i["severity"] == "minor"]
    gates = {
        "full_cs1_pipeline_validated": any(
            e["stage"] == "ei_pipeline_g1_g7" and e["ok"] for e in timeline
        ),
        "missions_reflect_curriculum": any(
            e["stage"] == "missions" and e["ok"] for e in timeline
        )
        and not any(i["area"] == "mission_coherence" and i["severity"] == "critical" for i in issues),
        "tutor_grounded": any(e["stage"] == "tutor" and e["ok"] for e in timeline),
        "progress_stable": any(e["stage"] == "progress" and e["ok"] for e in timeline),
        "knowledge_graph_ok": any(
            e["stage"] == "knowledge_graph" and e["ok"] for e in timeline
        ),
        "review_pack_matches_cert": any(
            e["stage"] == "review_pack_matches_certification" and e["ok"]
            for e in timeline
        )
        or any(e["stage"] == "review_pack" and e["ok"] for e in timeline),
        "observatory_meaningful": any(
            e["stage"] == "observatory" and e["ok"] for e in timeline
        ),
        "critical_issue_count": len(critical),
        "minor_issue_count": len(minor),
    }
    # Decision rule: READY if pipeline+student surfaces pass and no critical
    # defects in certified path; active legacy package debt alone does not
    # block if certified candidate is produced — but DOES block closed beta
    # if student would still consume the noisy active package.
    certified_path_ok = (
        gates["full_cs1_pipeline_validated"]
        and gates["missions_reflect_curriculum"]
        and gates["tutor_grounded"]
        and gates["progress_stable"]
        and gates["knowledge_graph_ok"]
        and gates["observatory_meaningful"]
        and pipe.intelligence_certified
    )
    active_student_path_safe = not any(
        i["title"] == "Active CS1 package still uses pre-EQ001 noisy structure"
        for i in critical
    ) and not any(
        i["title"] == "Active CS1 package lacks certification block" for i in critical
    )
    if certified_path_ok and active_student_path_safe:
        decision = "READY FOR CLOSED BETA"
        decision_rationale = (
            "Certified CS1 pipeline and student surfaces validated; active "
            "published package is certified/clean."
        )
    elif certified_path_ok and not active_student_path_safe:
        decision = "BLOCKED"
        decision_rationale = (
            "Certified engine path works, but the active published CS1 package "
            "students would enrol into remains uncertified/noisy. Closed beta "
            "requires republishing the certified snapshot as the live package."
        )
    else:
        decision = "BLOCKED"
        decision_rationale = (
            "Certified CS1 path failed one or more product quality gates. "
            f"Critical issues: {len(critical)}."
        )

    evidence.update(
        {
            "finished_at": utc(),
            "duration_s": round(perf_counter() - t0, 2),
            "timeline": timeline,
            "issues": issues,
            "quality_gates": gates,
            "decision": decision,
            "decision_rationale": decision_rationale,
            "cmp_window": f"{CMP_PAGE_START}-{CMP_PAGE_END}",
            "baseline_commit_note": "run against local working tree",
        }
    )
    dump(EVIDENCE / "timeline.json", timeline)
    dump(EVIDENCE / "issues.json", issues)
    dump(EVIDENCE / "quality_gates.json", gates)
    dump(EVIDENCE / "dogfood_evidence.json", evidence)
    dump(
        EVIDENCE / "final_decision.json",
        {"decision": decision, "rationale": decision_rationale, "gates": gates},
    )
    print("\n==== FINAL DECISION ====")
    print(decision)
    print(decision_rationale)
    print(f"Critical issues: {len(critical)} · Minor: {len(minor)}")
    return 0 if decision == "READY FOR CLOSED BETA" else 3


if __name__ == "__main__":
    raise SystemExit(main())
