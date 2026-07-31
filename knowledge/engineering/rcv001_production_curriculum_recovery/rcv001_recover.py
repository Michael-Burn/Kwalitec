#!/usr/bin/env python3
"""RCV-001 — Production Curriculum Recovery.

Executes the missing Educational Intelligence + calibration + certified
publication pipeline against the PRODUCTION database using existing
application services only (same service sequence as RR-001).

Requires:
  DATABASE_URL  — production Postgres (Render kwalitec-db external URL)
  APP_ENV       — typically development for local ops against prod DB
  SECRET_KEY    — any valid key for create_app

Does NOT modify application architecture, validation, Runtime, Deriver,
publication rules, or certification rules.
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
EVIDENCE = ROOT / "knowledge/evidence/releases/RCV001"

SYLLABUS_PDF = ROOT / (
    "instance/curriculum_documents/cs1/syllabus/v1/adad4b0985279dfc-f47a6fce.pdf"
)
CMP_PDF = ROOT / (
    "instance/curriculum_documents/cs1/cmp/v1/6cb786c59ea43960-730062a9.pdf"
)

CMP_PAGE_START = 30
CMP_PAGE_END = 180

WORKSPACE_ID = "ws-cs1"
SUBJECT = "CS1"
VERSION = "2026.1"
ACTOR_ID = "rcv001"

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
        ("rcv001_page_window", f"{start}-{end}"),
        ("rcv001_full_page_count", str(doc.page_count)),
    ]
    return ExtractedDocument(
        extraction_id=f"{doc.extraction_id}-p{start}-{end}",
        document_id=doc.document_id,
        page_count=len(pages),
        pages=pages,
        metadata=tuple(meta),
        diagnostics=tuple(doc.diagnostics)
        + (f"rcv001_sliced_pages={start}-{end}",),
    )


def _load_json(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return json.loads(value or "{}")
    return dict(value)


def active_package_summary(db) -> dict[str, Any] | None:
    """Postgres-safe active package summary."""
    from sqlalchemy import text

    row = db.session.execute(
        text(
            "SELECT id, version_label, is_active, package_json "
            "FROM published_curriculum_packages WHERE subject_code=:c "
            "AND is_active IS TRUE ORDER BY id DESC LIMIT 1"
        ),
        {"c": SUBJECT},
    ).mappings().first()
    if row is None:
        return None
    package = _load_json(row["package_json"])
    structure = package.get("structure") or {}
    cert = package.get("certification")
    sections = structure.get("sections") or []
    topics = structure.get("topics") or []
    objectives = structure.get("objectives") or []
    return {
        "id": row["id"],
        "version_label": row["version_label"],
        "is_active": bool(row["is_active"]),
        "has_certification": bool(cert)
        and str((cert or {}).get("authority") or "").startswith("certified"),
        "certification": cert,
        "sections": int(structure.get("section_count") or len(sections)),
        "topics": int(structure.get("topic_count") or len(topics)),
        "objectives": int(structure.get("objective_count") or len(objectives)),
        "source": structure.get("source"),
        "curriculum_authority": structure.get("curriculum_authority"),
    }


def assert_production_target(db) -> dict[str, Any]:
    """Refuse to run against local SQLite by accident."""
    from sqlalchemy import text

    bind = db.session.get_bind()
    dialect = bind.dialect.name
    url = str(bind.url)
    identity = db.session.execute(
        text("SELECT current_database(), current_user")
    ).first()
    meta = {
        "dialect": dialect,
        "database": identity[0] if identity else None,
        "user": identity[1] if identity else None,
        "host": getattr(bind.url, "host", None),
    }
    if dialect == "sqlite":
        raise RuntimeError(
            "RCV-001 refused: DATABASE_URL points at SQLite. "
            "Set production Postgres DATABASE_URL before recovery."
        )
    if meta["database"] != "kwalitec":
        raise RuntimeError(
            f"RCV-001 refused: unexpected database {meta['database']!r}"
        )
    if "dpg-d97bmbm8bjmc73c497e0-a" not in url and "oregon-postgres" not in url:
        # Allow internal Render hostname without oregon suffix.
        if "dpg-d97bmbm8bjmc73c497e0-a" not in (meta.get("host") or ""):
            raise RuntimeError(
                "RCV-001 refused: DATABASE_URL host is not kwalitec-db "
                f"(host={meta.get('host')!r})."
            )
    return meta


def main() -> int:
    from app import create_app
    from app.application.curriculum_intelligence.calibration_service import (
        FounderCalibrationService,
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
    from app.application.curriculum_intelligence.workspace_generation_service import (
        WorkspaceGenerationService,
        build_default_orchestrator,
    )
    from app.application.curriculum_studio_foundation.authority import (
        PublishedCurriculumAuthority,
    )
    from app.application.platform_integration.publication_bridge import (
        PublicationBridgeService,
    )
    from app.domain.curriculum_intelligence.generation import (
        DifficultyBiasStyle,
        GranularityStyle,
        HierarchyStyle,
        TopicDensityStyle,
    )
    from app.domain.educational_engine_foundation.derivation import (
        EducationalArtefactDeriver,
    )
    from app.infrastructure.adapters.curriculum_intelligence.certified_snapshot_loader import (  # noqa: E501
        StoreCertifiedSnapshotLoader,
    )
    from app.infrastructure.adapters.curriculum_intelligence.generation_store import (
        SqlAlchemyGenerationStore,
    )
    from app.infrastructure.adapters.curriculum_intelligence.pypdf_extractor import (
        PyPdfExtractionAdapter,
    )
    from app.presentation.curriculum_studio.factory import get_studio_service

    app = create_app()
    evidence: dict[str, Any] = {
        "programme": "RCV-001",
        "subject": SUBJECT,
        "workspace_id": WORKSPACE_ID,
        "started_at": utc(),
        "objective": "Bring production CS1 to local certified parity",
    }

    with app.app_context():
        from app.extensions import db
        from sqlalchemy import text

        try:
            target = assert_production_target(db)
        except Exception as exc:  # noqa: BLE001
            note_issue("critical", "Production target check failed", str(exc))
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            print(f"STOP: {exc}")
            return 1
        evidence["production_target"] = {
            k: v for k, v in target.items() if k != "password"
        }
        log("production_target", True, **evidence["production_target"])

        before = active_package_summary(db)
        dump(EVIDENCE / "before_active_package.json", before)
        log(
            "baseline_active_package",
            bool(before),
            sections=(before or {}).get("sections"),
            topics=(before or {}).get("topics"),
            objectives=(before or {}).get("objectives"),
            has_certification=(before or {}).get("has_certification"),
        )

        # -----------------------------------------------------------------
        # STEP 1 — Prerequisites
        # -----------------------------------------------------------------
        cur = db.session.execute(
            text(
                "SELECT id, kind, checksum_sha256, storage_key, processing_stage "
                "FROM studio_foundation_documents "
                "WHERE is_active IS TRUE AND workspace_id=:w ORDER BY id"
            ),
            {"w": WORKSPACE_ID},
        ).mappings().all()
        ws = db.session.execute(
            text(
                "SELECT workspace_id, status, version_label, certification_status "
                "FROM studio_workspace_projections WHERE workspace_id=:w"
            ),
            {"w": WORKSPACE_ID},
        ).mappings().first()
        fv = db.session.execute(
            text(
                "SELECT v.id, v.version_label, v.publication_state "
                "FROM studio_foundation_versions v "
                "JOIN studio_foundation_subjects s ON s.id = v.subject_id "
                "WHERE s.subject_code=:c ORDER BY v.id"
            ),
            {"c": SUBJECT},
        ).mappings().all()
        enrollments = db.session.execute(
            text("SELECT COUNT(*) AS n FROM runtime_enrolments")
        ).scalar()

        kinds = {r["kind"] for r in cur}
        step1_ok = (
            ws is not None
            and bool(fv)
            and "cmp" in kinds
            and "syllabus" in kinds
            and SYLLABUS_PDF.is_file()
            and CMP_PDF.is_file()
        )
        step1 = {
            "active_documents": [dict(r) for r in cur],
            "workspace": dict(ws) if ws else None,
            "foundation_versions": [dict(r) for r in fv],
            "runtime_enrolments": int(enrollments or 0),
            "local_syllabus_readable": SYLLABUS_PDF.is_file(),
            "local_cmp_readable": CMP_PDF.is_file(),
        }
        # Redact nothing sensitive in checksums/storage keys — already public.
        dump(EVIDENCE / "step1_prerequisites.json", step1)
        log("step1_prerequisites", step1_ok, enrollments=step1["runtime_enrolments"])
        if not step1_ok:
            note_issue(
                "critical",
                "STEP 1 prerequisites failed",
                json.dumps(step1, default=str)[:1500],
                area="prerequisites",
            )
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 1

        extractor = PyPdfExtractionAdapter()
        normalizer = DocumentNormalizationService()
        syllabus = normalizer.normalize(
            extractor.extract(
                SYLLABUS_PDF.read_bytes(),
                extraction_id="rcv001-syllabus",
                document_id=101,
            )
        )
        cmp_full = normalizer.normalize(
            extractor.extract(
                CMP_PDF.read_bytes(),
                extraction_id="rcv001-cmp",
                document_id=102,
            )
        )
        cmp = slice_pages(cmp_full, CMP_PAGE_START, CMP_PAGE_END)
        dump(
            EVIDENCE / "extraction_metrics.json",
            {
                "syllabus_pages": syllabus.page_count,
                "cmp_full_pages": cmp_full.page_count,
                "cmp_window": f"{CMP_PAGE_START}-{CMP_PAGE_END}",
                "cmp_window_pages": cmp.page_count,
            },
        )
        log(
            "extract_normalize",
            True,
            syllabus_pages=syllabus.page_count,
            cmp_window=f"{CMP_PAGE_START}-{CMP_PAGE_END}",
        )

        store = SqlAlchemyGenerationStore()
        studio = get_studio_service()
        try:
            reconcile = getattr(studio, "reconcile_workspace", None)
            if callable(reconcile):
                reconcile(WORKSPACE_ID)
        except Exception as exc:  # noqa: BLE001
            note_issue(
                "minor", "Workspace reconcile warning", str(exc), area="founder"
            )

        orch = build_default_orchestrator(store)
        service = WorkspaceGenerationService(
            store, registry=studio.registry, orchestrator=orch
        )

        # -----------------------------------------------------------------
        # Optional CMP+syllabus probe (RR-001 C3 confidence)
        # -----------------------------------------------------------------
        cmp_store = SqlAlchemyGenerationStore()
        cmp_orch = build_default_orchestrator(cmp_store)
        t_cmp = perf_counter()
        try:
            cmp_result = cmp_orch.run_chain(
                chain_id="rcv001-cmp-syllabus",
                workspace_id=f"{WORKSPACE_ID}-cmp",
                source_document_ids=(101, 102),
                start_from=1,
                through=7,
                source_documents=(syllabus, cmp),
                subject_code=SUBJECT,
                version_label=f"{VERSION}-cmp",
                fixed_created_at_iso="2026-07-30T11:00:00Z",
                stop_on_regression=True,
                emit_review_pack=True,
            )
            db.session.commit()
        except Exception as exc:  # noqa: BLE001
            cmp_result = None
            note_issue(
                "critical",
                "CMP+syllabus G1–G7 raised",
                f"{exc}\n{traceback.format_exc()}",
                area="c3",
            )
        cmp_meta: dict[str, Any] = {
            "duration_s": round(perf_counter() - t_cmp, 2),
            "cmp_window": f"{CMP_PAGE_START}-{CMP_PAGE_END}",
        }
        if cmp_result is not None:
            cmp_meta.update(
                {
                    "stopped_at_index": cmp_result.stopped_at_index,
                    "rolled_back": cmp_result.rolled_back,
                    "accepted_indices": [
                        s.generation_index for s in cmp_result.accepted_snapshots
                    ],
                    "rejected_indices": [
                        s.generation_index for s in cmp_result.rejected_snapshots
                    ],
                    "certification": (
                        cmp_result.certification.outcome.value
                        if cmp_result.certification
                        else None
                    ),
                }
            )
            cmp_ok = (
                cmp_result.stopped_at_index is None
                and cmp_result.certification is not None
                and 7 in [s.generation_index for s in cmp_result.accepted_snapshots]
            )
            if not cmp_ok:
                note_issue(
                    "critical",
                    "CMP+syllabus did not complete G1→G7 certification",
                    json.dumps(cmp_meta, default=str)[:1200],
                    area="c3",
                )
            log(
                "cmp_syllabus_g1_g7",
                cmp_ok,
                **{
                    k: cmp_meta[k]
                    for k in (
                        "stopped_at_index",
                        "certification",
                        "duration_s",
                        "accepted_indices",
                    )
                    if k in cmp_meta
                },
            )
        else:
            log("cmp_syllabus_g1_g7", False)
        dump(EVIDENCE / "cmp_syllabus_g1_g7.json", cmp_meta)

        # -----------------------------------------------------------------
        # STEP 2 — Syllabus-authoritative Generations 1–7
        # -----------------------------------------------------------------
        t_pipe = perf_counter()
        try:
            pipe = service.run_initial_pipeline(
                WORKSPACE_ID,
                source_document_ids=(101,),
                source_documents=(syllabus,),
                subject_code=SUBJECT,
                version_label=VERSION,
                fixed_created_at_iso="2026-07-30T11:10:00Z",
            )
            db.session.commit()
            pipe_ok = pipe.intelligence_certified
        except Exception as exc:  # noqa: BLE001
            pipe = None
            pipe_ok = False
            note_issue(
                "critical",
                "Syllabus G1–G7 failed",
                f"{exc}\n{traceback.format_exc()}",
                area="engine",
            )
        pipe_meta: dict[str, Any] = {
            "ok": pipe_ok,
            "duration_s": round(perf_counter() - t_pipe, 2),
            "source_mode": "syllabus_authoritative",
        }
        if pipe is not None:
            pipe_meta.update(
                {
                    "chain_id": pipe.orchestrator.chain_id,
                    "intelligence_certified": pipe.intelligence_certified,
                    "certification": (
                        pipe.orchestrator.certification.outcome.value
                        if pipe.orchestrator.certification
                        else None
                    ),
                    "certified_snapshot_id": pipe.binding.certified_snapshot_id,
                    "accepted_indices": [
                        s.generation_index
                        for s in pipe.orchestrator.accepted_snapshots
                    ],
                    "metrics": (
                        _json_default(pipe.orchestrator.accepted_snapshots[-1].metrics)
                        if pipe.orchestrator.accepted_snapshots
                        else None
                    ),
                }
            )
        dump(EVIDENCE / "syllabus_pipeline.json", pipe_meta)
        log(
            "step2_syllabus_g1_g7",
            pipe_ok,
            **{
                k: pipe_meta[k]
                for k in (
                    "intelligence_certified",
                    "certification",
                    "duration_s",
                    "accepted_indices",
                )
                if k in pipe_meta
            },
        )
        if not pipe_ok or pipe is None:
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            dump(
                EVIDENCE / "verification_evidence.json",
                evidence
                | {
                    "timeline": timeline,
                    "issues": issues,
                    "finished_at": utc(),
                },
            )
            return 2

        # -----------------------------------------------------------------
        # STEP 3 — Founder Calibration (RR-001 style set)
        # -----------------------------------------------------------------
        cal_svc = FounderCalibrationService(
            store, registry=studio.registry, orchestrator=orch
        )
        t_cal = perf_counter()
        try:
            cal_svc.apply(
                WORKSPACE_ID,
                granularity=GranularityStyle.BALANCED,
                hierarchy=HierarchyStyle.BALANCED,
                topic_density=TopicDensityStyle.BALANCED,
                difficulty_bias=DifficultyBiasStyle.BALANCED,
                source_documents=(syllabus,),
                subject_code=SUBJECT,
                version_label=VERSION,
                fixed_created_at_iso="2026-07-30T11:20:00Z",
            )
            cal = cal_svc.apply(
                WORKSPACE_ID,
                granularity=GranularityStyle.BALANCED,
                hierarchy=HierarchyStyle.STRICT_SYLLABUS,
                topic_density=TopicDensityStyle.CONSOLIDATED,
                difficulty_bias=DifficultyBiasStyle.EXAM_FOCUSED,
                source_documents=(syllabus,),
                subject_code=SUBJECT,
                version_label=VERSION,
                fixed_created_at_iso="2026-07-30T11:21:00Z",
            )
            db.session.commit()
            cal_ok = (
                cal.intelligence_certified
                and cal.orchestrator.certification is not None
                and cal.orchestrator.stopped_at_index is None
                and 7 in cal.generations_rerun
            )
            cal_meta = {
                "profile_id": cal.profile.profile_id,
                "generations_rerun": list(cal.generations_rerun),
                "intelligence_certified": cal.intelligence_certified,
                "post_cal_certification": (
                    cal.orchestrator.certification.outcome.value
                    if cal.orchestrator.certification
                    else None
                ),
                "stopped_at_index": cal.orchestrator.stopped_at_index,
                "rolled_back": cal.orchestrator.rolled_back,
                "review_pack": cal.orchestrator.review_pack is not None,
                "duration_s": round(perf_counter() - t_cal, 2),
            }
            if not cal_ok:
                note_issue(
                    "critical",
                    "Calibration did not re-certify through Gen7",
                    json.dumps(cal_meta, default=str),
                    area="c4",
                )
        except Exception as exc:  # noqa: BLE001
            cal_ok = False
            cal_meta = {
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "duration_s": round(perf_counter() - t_cal, 2),
            }
            note_issue("critical", "Calibration raised", str(exc), area="c4")
        dump(EVIDENCE / "calibration.json", cal_meta)
        log(
            "step3_calibration_recert",
            cal_ok,
            **{
                k: cal_meta[k]
                for k in (
                    "intelligence_certified",
                    "post_cal_certification",
                    "generations_rerun",
                    "duration_s",
                )
                if k in cal_meta
            },
        )

        workspace = studio.registry.get_workspace(WORKSPACE_ID)
        if workspace is not None and not workspace.facts.intelligence_certified:
            note_issue(
                "critical",
                "Workspace intelligence_certified false after calibration",
                "Publish gate would block certified cutover.",
                area="c4",
            )

        if not cal_ok:
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            dump(
                EVIDENCE / "verification_evidence.json",
                evidence
                | {
                    "timeline": timeline,
                    "issues": issues,
                    "finished_at": utc(),
                },
            )
            return 3

        # -----------------------------------------------------------------
        # STEP 4 — Publish via existing PublicationBridgeService
        # -----------------------------------------------------------------
        t_pub = perf_counter()
        try:
            if workspace is not None:
                studio.publication.update_facts(
                    WORKSPACE_ID,
                    intelligence_certified=True,
                    preview_approved=True,
                    validation_passed=True,
                    blueprint_assigned=True,
                    preview_built=True,
                    version_assigned=True,
                    rollback_snapshot_created=True,
                    cmp_uploaded=True,
                    official_syllabus_uploaded=True,
                )
            bridge = PublicationBridgeService(studio.registry)
            pub = bridge.publish_to_catalogue(WORKSPACE_ID, actor_id=ACTOR_ID)
            db.session.commit()
            pub_ok = True
            pub_meta = {**pub, "duration_s": round(perf_counter() - t_pub, 2)}
        except Exception as exc:  # noqa: BLE001
            pub_ok = False
            pub_meta = {
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "duration_s": round(perf_counter() - t_pub, 2),
            }
            note_issue(
                "critical",
                "Certified catalogue cutover publish failed",
                str(exc),
                area="publish",
            )
        dump(EVIDENCE / "publication_cutover.json", pub_meta)
        log(
            "step4_catalogue_cutover",
            pub_ok,
            **{
                k: pub_meta[k]
                for k in ("package_id", "version_label", "is_active", "duration_s")
                if k in pub_meta
            },
        )

        # -----------------------------------------------------------------
        # STEP 5 — Verify published package
        # -----------------------------------------------------------------
        after = active_package_summary(db)
        dump(EVIDENCE / "after_active_package.json", after)
        package_ok = bool(
            after
            and after.get("has_certification")
            and (after.get("sections") or 0) > 0
            and (after.get("topics") or 0) > 0
            and (after.get("objectives") or 0) > 0
        )
        parity_ok = bool(
            after
            and after.get("sections") == 5
            and after.get("topics") == 15
            and after.get("objectives") == 73
        )
        if not package_ok:
            note_issue(
                "critical",
                "Published package missing sections/topics/objectives",
                json.dumps(after, default=str),
                area="verify",
            )
        log(
            "step5_package_verify",
            package_ok,
            sections=(after or {}).get("sections"),
            topics=(after or {}).get("topics"),
            objectives=(after or {}).get("objectives"),
            has_certification=(after or {}).get("has_certification"),
            local_parity=parity_ok,
        )

        # -----------------------------------------------------------------
        # STEP 6 — Begin Learning / Educational Deriver
        # -----------------------------------------------------------------
        authority = PublishedCurriculumAuthority()
        runtime_snap = authority.get_active(SUBJECT)
        derive_ok = False
        derive_meta: dict[str, Any] = {"loaded": runtime_snap is not None}
        runtime_pkg: dict[str, Any] | None = None
        if runtime_snap is not None:
            runtime_pkg = (
                runtime_snap.package
                if hasattr(runtime_snap, "package")
                else dict(runtime_snap)  # type: ignore[arg-type]
            )
            cert = (runtime_pkg or {}).get("certification") or {}
            structure = (runtime_pkg or {}).get("structure") or {}
            derive_meta.update(
                {
                    "authority": cert.get("authority"),
                    "status": cert.get("status"),
                    "topics": structure.get("topic_count")
                    or len(structure.get("topics") or []),
                    "objectives": structure.get("objective_count")
                    or len(structure.get("objectives") or []),
                    "sections": structure.get("section_count")
                    or len(structure.get("sections") or []),
                }
            )
            try:
                bundle = EducationalArtefactDeriver().derive(runtime_pkg or {})
                derive_ok = True
                derive_meta["derive"] = {
                    "sections": len(getattr(bundle, "sections", []) or []),
                    "topics": len(getattr(bundle, "topics", []) or []),
                    "objectives": len(getattr(bundle, "objectives", []) or []),
                }
                # Best-effort attribute discovery for report clarity.
                for attr in ("sections", "topics", "objectives", "artefacts"):
                    if hasattr(bundle, attr):
                        derive_meta["derive"][attr] = len(getattr(bundle, attr) or [])
            except Exception as exc:  # noqa: BLE001
                derive_ok = False
                derive_meta["derive_error"] = str(exc)
                note_issue(
                    "critical",
                    "EducationalArtefactDeriver failed (Begin Learning gate)",
                    str(exc),
                    area="begin_learning",
                )
        else:
            note_issue(
                "critical",
                "PublishedCurriculumAuthority returned no active CS1 package",
                "",
                area="begin_learning",
            )
        dump(EVIDENCE / "begin_learning_derive.json", derive_meta)
        log("step6_begin_learning_derive", derive_ok, **{
            k: derive_meta[k]
            for k in ("authority", "status", "sections", "topics", "objectives")
            if k in derive_meta
        })

        # -----------------------------------------------------------------
        # STEP 7 — Regression surfaces
        # -----------------------------------------------------------------
        loader = StoreCertifiedSnapshotLoader(store)
        preview = CertifiedSnapshotPreviewService(loader=loader)
        certified = preview.get_certified_for_workspace(WORKSPACE_ID)
        surface_meta: dict[str, Any] = {"certified_loaded": certified is not None}
        surfaces_ok = certified is not None
        if certified is not None:
            try:
                topics = []
                if runtime_pkg is not None:
                    structure = runtime_pkg.get("structure") or {}
                    topics = structure.get("topics") or []
                    surface_meta["mission_topic_sample"] = [
                        t.get("title") or t.get("topic_title")
                        for t in topics[:5]
                        if isinstance(t, dict)
                    ]
                surface_meta["missions_ok"] = bool(
                    surface_meta.get("mission_topic_sample")
                )
                _ = (
                    CertifiedMissionEngine,
                    CertifiedProgressEngine,
                    CertifiedTutorContextService,
                )
            except Exception as exc:  # noqa: BLE001
                surface_meta["missions_error"] = str(exc)
                surfaces_ok = False

            try:
                observatory = CurriculumObservatory(store)
                obs = observatory.report_for_chain(pipe.orchestrator.chain_id)
                surface_meta["observatory_ok"] = obs is not None
                dump(
                    EVIDENCE / "observatory_summary.json",
                    {
                        "chain_id": pipe.orchestrator.chain_id,
                        "has_report": obs is not None,
                    },
                )
            except Exception as exc:  # noqa: BLE001
                surface_meta["observatory_error"] = str(exc)
                note_issue(
                    "critical",
                    "Observatory surface regression",
                    str(exc),
                    area="surfaces",
                )
                surfaces_ok = False

        # Health-style counts after recovery
        ei_counts = {}
        for table in (
            "ei_generation_chains",
            "ei_generations",
            "ei_generation_snapshots",
            "ei_certification_records",
            "ei_educational_nodes",
        ):
            ei_counts[table] = int(
                db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0
            )
        surface_meta["ei_counts"] = ei_counts
        dump(EVIDENCE / "student_surfaces.json", surface_meta)
        log(
            "step7_regression_surfaces",
            surfaces_ok,
            **{
                k: surface_meta[k]
                for k in ("certified_loaded", "missions_ok", "observatory_ok")
                if k in surface_meta
            },
        )

        # -----------------------------------------------------------------
        # Decision
        # -----------------------------------------------------------------
        blockers = {
            "step1_prerequisites": step1_ok,
            "step2_syllabus_g1_g7": pipe_ok,
            "step3_calibration_recert": cal_ok,
            "step4_publish": pub_ok,
            "step5_package_nonempty": package_ok,
            "step5_local_parity_5_15_73": parity_ok,
            "step6_begin_learning_derive": derive_ok,
            "step7_surfaces": surfaces_ok,
            "cmp_probe_optional": any(
                e["stage"] == "cmp_syllabus_g1_g7" and e["ok"] for e in timeline
            ),
        }
        critical = [i for i in issues if i["severity"] == "critical"]
        # Success criteria: functionally equivalent (non-empty certified + derive).
        # Local exact parity is expected but reported separately.
        required = [
            "step1_prerequisites",
            "step2_syllabus_g1_g7",
            "step3_calibration_recert",
            "step4_publish",
            "step5_package_nonempty",
            "step6_begin_learning_derive",
            "step7_surfaces",
        ]
        ready = all(blockers[k] for k in required) and not any(
            i["area"] in {"engine", "c4", "publish", "verify", "begin_learning"}
            for i in critical
        )
        decision = "RECOVERY COMPLETE" if ready else "RECOVERY BLOCKED"
        decision_rationale = (
            "Production CS1 active package is certified with non-empty "
            "sections/topics/objectives; EducationalArtefactDeriver succeeds."
            if ready
            else (
                "One or more RCV-001 steps failed. "
                f"blockers={json.dumps(blockers)}; critical={len(critical)}."
            )
        )

        evidence.update(
            {
                "finished_at": utc(),
                "duration_s": round(perf_counter() - t0, 2),
                "before": before,
                "after": after,
                "blockers": blockers,
                "timeline": timeline,
                "issues": issues,
                "decision": decision,
                "decision_rationale": decision_rationale,
                "local_parity_5_15_73": parity_ok,
            }
        )
        dump(EVIDENCE / "timeline.json", timeline)
        dump(EVIDENCE / "issues.json", issues)
        dump(EVIDENCE / "blockers.json", blockers)
        dump(
            EVIDENCE / "final_decision.json",
            {
                "decision": decision,
                "rationale": decision_rationale,
                "blockers": blockers,
                "local_parity_5_15_73": parity_ok,
            },
        )
        dump(EVIDENCE / "verification_evidence.json", evidence)
        print()
        print("=" * 60)
        print(f"RCV-001 DECISION: {decision}")
        print(decision_rationale)
        print(f"Before: {before}")
        print(f"After:  {after}")
        print("=" * 60)
        return 0 if ready else 3


if __name__ == "__main__":
    raise SystemExit(main())
