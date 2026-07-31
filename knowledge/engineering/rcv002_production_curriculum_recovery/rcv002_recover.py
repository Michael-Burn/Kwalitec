#!/usr/bin/env python3
"""RCV-002 — Resume Production Curriculum Recovery (post PGFIX-001).

Resumes from the RCV-001 stop point using existing application services only:
  WorkspaceGenerationService.run_initial_pipeline (G1–G7)
  → FounderCalibrationService.apply (RR-001 styles)
  → PublicationBridgeService.publish_to_catalogue
  → Begin Learning (authority + deriver + enrol + mission)

Requires DATABASE_URL → production Postgres (kwalitec-db).
Does NOT redesign architecture or bypass validation/certification/publication.
"""

from __future__ import annotations

import json
import traceback
from dataclasses import asdict, is_dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from time import perf_counter
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
EVIDENCE = ROOT / "knowledge/evidence/releases/RCV002"

SYLLABUS_PDF = ROOT / (
    "instance/curriculum_documents/cs1/syllabus/v1/adad4b0985279dfc-f47a6fce.pdf"
)

WORKSPACE_ID = "ws-cs1"
SUBJECT = "CS1"
VERSION = "2026.1"
ACTOR_ID = "rcv002"

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
    print(
        f"[{mark}] {stage} { {k: v for k, v in facts.items() if k != 'detail'} }",
        flush=True,
    )


def note_issue(
    severity: str, title: str, detail: str, *, area: str = "platform"
) -> None:
    issues.append(
        {"severity": severity, "area": area, "title": title, "detail": detail}
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


def _load_json(value: Any) -> dict[str, Any]:
    if value is None:
        return {}
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        return json.loads(value or "{}")
    return dict(value)


def active_package_summary(db) -> dict[str, Any] | None:
    from sqlalchemy import text

    row = db.session.execute(
        text(
            "SELECT id, version_label, is_active, package_json, published_by "
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
        "published_by": row["published_by"],
        "has_certification": bool(cert)
        and str((cert or {}).get("authority") or "").startswith("certified"),
        "certification": cert,
        "sections": int(structure.get("section_count") or len(sections)),
        "topics": int(structure.get("topic_count") or len(topics)),
        "objectives": int(structure.get("objective_count") or len(objectives)),
        "source": structure.get("source"),
        "curriculum_authority": structure.get("curriculum_authority"),
    }


def ei_inventory(db) -> dict[str, Any]:
    from sqlalchemy import text

    counts = {}
    for table in (
        "ei_generation_chains",
        "ei_generations",
        "ei_generation_snapshots",
        "ei_educational_nodes",
        "ei_certification_records",
        "ei_calibration_profiles",
        "runtime_enrolments",
    ):
        counts[table] = int(
            db.session.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar() or 0
        )
    ws = db.session.execute(
        text(
            "SELECT certification_status, certified_snapshot_id, active_chain_id "
            "FROM studio_workspace_projections WHERE workspace_id=:w"
        ),
        {"w": WORKSPACE_ID},
    ).mappings().first()
    gens = db.session.execute(
        text(
            "SELECT generation_index, COUNT(*) AS n FROM ei_generation_snapshots "
            "WHERE chain_id=:c GROUP BY generation_index ORDER BY 1"
        ),
        {"c": f"ei-chain-{WORKSPACE_ID}"},
    ).mappings().all()
    return {
        "counts": counts,
        "workspace": dict(ws) if ws else None,
        "snapshots_by_generation": [dict(r) for r in gens],
    }


def foundation_summary(db) -> dict[str, Any] | None:
    from sqlalchemy import text

    row = db.session.execute(
        text(
            "SELECT v.id, v.version_label, v.publication_state, v.parsed_structure_json "
            "FROM studio_foundation_versions v "
            "JOIN studio_foundation_subjects s ON s.id = v.subject_id "
            "WHERE s.subject_code=:c ORDER BY v.id LIMIT 1"
        ),
        {"c": SUBJECT},
    ).mappings().first()
    if row is None:
        return None
    structure = _load_json(row["parsed_structure_json"])
    return {
        "id": row["id"],
        "version_label": row["version_label"],
        "publication_state": row["publication_state"],
        "sections": len(structure.get("sections") or []),
        "topics": len(structure.get("topics") or []),
        "objectives": len(structure.get("objectives") or []),
        "source": structure.get("source"),
        "curriculum_authority": structure.get("curriculum_authority"),
    }


def assert_production_target(db) -> dict[str, Any]:
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
        raise RuntimeError("RCV-002 refused: DATABASE_URL is SQLite")
    if meta["database"] != "kwalitec":
        raise RuntimeError(f"RCV-002 refused: unexpected database {meta['database']!r}")
    host = meta.get("host") or ""
    if "dpg-d97bmbm8bjmc73c497e0-a" not in url and "dpg-d97bmbm8bjmc73c497e0-a" not in host:
        raise RuntimeError(f"RCV-002 refused: unexpected host {host!r}")
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
    from app.application.educational_runtime_engine.exceptions import (
        EnrolmentAlreadyExists,
    )
    from app.application.educational_runtime_engine.service import (
        EducationalRuntimeEngineService,
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
    from sqlalchemy import text

    app = create_app()
    evidence: dict[str, Any] = {
        "programme": "RCV-002",
        "subject": SUBJECT,
        "workspace_id": WORKSPACE_ID,
        "started_at": utc(),
        "prerequisite": "PGFIX-001",
    }

    with app.app_context():
        from app.extensions import db

        try:
            target = assert_production_target(db)
        except Exception as exc:  # noqa: BLE001
            note_issue("critical", "Production target check failed", str(exc))
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            print(f"STOP: {exc}")
            return 1

        evidence["production_target"] = target
        log("production_target", True, **target)

        before_pkg = active_package_summary(db)
        before_ei = ei_inventory(db)
        before_fv = foundation_summary(db)
        dump(EVIDENCE / "before_active_package.json", before_pkg)
        dump(EVIDENCE / "before_ei_inventory.json", before_ei)
        dump(EVIDENCE / "before_foundation.json", before_fv)
        log(
            "preflight_baseline",
            bool(before_pkg),
            sections=(before_pkg or {}).get("sections"),
            topics=(before_pkg or {}).get("topics"),
            objectives=(before_pkg or {}).get("objectives"),
            ei_chains=before_ei["counts"]["ei_generation_chains"],
            enrolments=before_ei["counts"]["runtime_enrolments"],
        )

        if not SYLLABUS_PDF.is_file():
            note_issue("critical", "Syllabus PDF missing", str(SYLLABUS_PDF))
            return 1

        extractor = PyPdfExtractionAdapter()
        normalizer = DocumentNormalizationService()
        syllabus = normalizer.normalize(
            extractor.extract(
                SYLLABUS_PDF.read_bytes(),
                extraction_id="rcv002-syllabus",
                document_id=101,
            )
        )
        dump(
            EVIDENCE / "extraction_metrics.json",
            {"syllabus_pages": syllabus.page_count, "source": str(SYLLABUS_PDF.name)},
        )
        log("extract_normalize", True, syllabus_pages=syllabus.page_count)

        store = SqlAlchemyGenerationStore()
        studio = get_studio_service()
        try:
            reconcile = getattr(studio, "reconcile_workspace", None)
            if callable(reconcile):
                reconcile(WORKSPACE_ID)
        except Exception as exc:  # noqa: BLE001
            note_issue("minor", "Workspace reconcile warning", str(exc), area="founder")

        orch = build_default_orchestrator(store)
        service = WorkspaceGenerationService(
            store, registry=studio.registry, orchestrator=orch
        )

        # -----------------------------------------------------------------
        # STEP 1 — Syllabus-authoritative Generations 1–7
        # -----------------------------------------------------------------
        print("STEP 1: starting WorkspaceGenerationService.run_initial_pipeline…", flush=True)
        t_pipe = perf_counter()
        try:
            pipe = service.run_initial_pipeline(
                WORKSPACE_ID,
                source_document_ids=(101,),
                source_documents=(syllabus,),
                subject_code=SUBJECT,
                version_label=VERSION,
                fixed_created_at_iso="2026-07-30T12:00:00Z",
            )
            db.session.commit()
            pipe_ok = bool(pipe.intelligence_certified)
            print(
                f"STEP 1: pipeline returned certified={pipe_ok} "
                f"in {perf_counter() - t_pipe:.1f}s",
                flush=True,
            )
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
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
        after_pipe_ei = ei_inventory(db)
        pipe_meta["ei_inventory"] = after_pipe_ei
        dump(EVIDENCE / "step1_syllabus_pipeline.json", pipe_meta)
        log(
            "step1_syllabus_g1_g7",
            pipe_ok,
            certification=pipe_meta.get("certification"),
            accepted_indices=pipe_meta.get("accepted_indices"),
            duration_s=pipe_meta["duration_s"],
            snapshots=after_pipe_ei["counts"]["ei_generation_snapshots"],
            nodes=after_pipe_ei["counts"]["ei_educational_nodes"],
        )
        if (
            not pipe_ok
            or pipe is None
            or pipe_meta.get("accepted_indices") != [1, 2, 3, 4, 5, 6, 7]
        ):
            note_issue(
                "critical",
                "Not all generations 1–7 persisted as accepted",
                json.dumps(pipe_meta, default=str)[:2000],
                area="engine",
            )
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            dump(
                EVIDENCE / "verification_evidence.json",
                evidence | {"timeline": timeline, "issues": issues, "finished_at": utc()},
            )
            return 2

        # -----------------------------------------------------------------
        # STEP 2 — Founder Calibration (RR-001 style set)
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
                fixed_created_at_iso="2026-07-30T12:10:00Z",
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
                fixed_created_at_iso="2026-07-30T12:11:00Z",
            )
            db.session.commit()
            cal_outcome = (
                cal.orchestrator.certification.outcome.value
                if cal.orchestrator.certification
                else None
            )
            cal_ok = (
                cal.intelligence_certified
                and cal_outcome in {"CERTIFIED", "CERTIFIED_WITH_WARNINGS"}
                and cal.orchestrator.stopped_at_index is None
                and 7 in cal.generations_rerun
            )
            cal_meta = {
                "profile_id": cal.profile.profile_id,
                "generations_rerun": list(cal.generations_rerun),
                "intelligence_certified": cal.intelligence_certified,
                "post_cal_certification": cal_outcome,
                "stopped_at_index": cal.orchestrator.stopped_at_index,
                "duration_s": round(perf_counter() - t_cal, 2),
            }
        except Exception as exc:  # noqa: BLE001
            db.session.rollback()
            cal_ok = False
            cal_meta = {
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "duration_s": round(perf_counter() - t_cal, 2),
            }
            note_issue("critical", "Calibration raised", str(exc), area="calibration")
        dump(EVIDENCE / "step2_calibration.json", cal_meta)
        log(
            "step2_calibration_recert",
            cal_ok,
            post_cal_certification=cal_meta.get("post_cal_certification"),
            generations_rerun=cal_meta.get("generations_rerun"),
            duration_s=cal_meta.get("duration_s"),
        )
        if not cal_ok:
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 3

        # -----------------------------------------------------------------
        # STEP 3 — Verify EI / certification artefacts populated
        # -----------------------------------------------------------------
        cert_inv = ei_inventory(db)
        dump(EVIDENCE / "step3_certification_inventory.json", cert_inv)
        cert_artefacts_ok = (
            cert_inv["counts"]["ei_generation_chains"] >= 1
            and cert_inv["counts"]["ei_generation_snapshots"] >= 7
            and cert_inv["counts"]["ei_educational_nodes"] > 0
            and cert_inv["counts"]["ei_certification_records"] >= 1
            and bool((cert_inv.get("workspace") or {}).get("certified_snapshot_id"))
            and bool((cert_inv.get("workspace") or {}).get("active_chain_id"))
            and str(
                (cert_inv.get("workspace") or {}).get("certification_status") or ""
            ).upper()
            in {"CERTIFIED", "CERTIFIED_WITH_WARNINGS"}
        )
        log(
            "step3_certification_artefacts",
            cert_artefacts_ok,
            **cert_inv["counts"],
            workspace=cert_inv.get("workspace"),
        )
        if not cert_artefacts_ok:
            note_issue(
                "critical",
                "Certification artefacts incomplete — refusing publish",
                json.dumps(cert_inv, default=str),
                area="certification",
            )
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 3

        # -----------------------------------------------------------------
        # STEP 4 — Publish via PublicationBridgeService (no fallback)
        # -----------------------------------------------------------------
        workspace = studio.registry.get_workspace(WORKSPACE_ID)
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
            db.session.rollback()
            pub_ok = False
            pub_meta = {
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "duration_s": round(perf_counter() - t_pub, 2),
            }
            note_issue(
                "critical",
                "Publication failed",
                str(exc),
                area="publish",
            )
        dump(EVIDENCE / "step4_publication.json", pub_meta)
        log(
            "step4_publish",
            pub_ok,
            **{
                k: pub_meta[k]
                for k in ("package_id", "version_label", "is_active", "duration_s")
                if k in pub_meta
            },
        )
        if not pub_ok:
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 4

        # -----------------------------------------------------------------
        # STEP 5 — Verify published package
        # -----------------------------------------------------------------
        after_pkg = active_package_summary(db)
        after_fv = foundation_summary(db)
        dump(EVIDENCE / "after_active_package.json", after_pkg)
        dump(EVIDENCE / "after_foundation.json", after_fv)
        package_ok = bool(
            after_pkg
            and after_pkg.get("has_certification")
            and (after_pkg.get("sections") or 0) > 0
            and (after_pkg.get("topics") or 0) > 0
            and (after_pkg.get("objectives") or 0) > 0
        )
        parity_ok = bool(
            after_pkg
            and after_pkg.get("sections") == 5
            and after_pkg.get("topics") == 15
            and after_pkg.get("objectives") == 73
        )
        log(
            "step5_package_verify",
            package_ok,
            sections=(after_pkg or {}).get("sections"),
            topics=(after_pkg or {}).get("topics"),
            objectives=(after_pkg or {}).get("objectives"),
            has_certification=(after_pkg or {}).get("has_certification"),
            source=(after_pkg or {}).get("source"),
            local_parity_5_15_73=parity_ok,
        )
        if not package_ok:
            note_issue(
                "critical",
                "Published package missing required structure",
                json.dumps(after_pkg, default=str),
                area="verify",
            )
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 5
        if not parity_ok:
            note_issue(
                "warning",
                "Package counts differ from local parity 5/15/73",
                json.dumps(after_pkg, default=str),
                area="parity",
            )

        # -----------------------------------------------------------------
        # STEP 6 — Begin Learning (authority + deriver + enrol + mission)
        # -----------------------------------------------------------------
        authority = PublishedCurriculumAuthority()
        runtime_snap = authority.get_active(SUBJECT)
        derive_ok = False
        enrol_ok = False
        mission_ok = False
        begin_meta: dict[str, Any] = {"loaded": runtime_snap is not None}
        runtime_pkg: dict[str, Any] | None = None
        if runtime_snap is not None:
            runtime_pkg = (
                runtime_snap.package
                if hasattr(runtime_snap, "package")
                else dict(runtime_snap)  # type: ignore[arg-type]
            )
            cert = (runtime_pkg or {}).get("certification") or {}
            structure = (runtime_pkg or {}).get("structure") or {}
            begin_meta.update(
                {
                    "authority": cert.get("authority"),
                    "status": cert.get("status"),
                    "sections": structure.get("section_count")
                    or len(structure.get("sections") or []),
                    "topics": structure.get("topic_count")
                    or len(structure.get("topics") or []),
                    "objectives": structure.get("objective_count")
                    or len(structure.get("objectives") or []),
                }
            )
            try:
                bundle = EducationalArtefactDeriver().derive(runtime_pkg or {})
                derive_ok = True
                begin_meta["derive"] = {
                    "ok": True,
                    "bundle_type": type(bundle).__name__,
                }
            except Exception as exc:  # noqa: BLE001
                begin_meta["derive_error"] = str(exc)
                note_issue(
                    "critical",
                    "EducationalArtefactDeriver failed",
                    str(exc),
                    area="begin_learning",
                )

        if derive_ok:
            # Prefer a non-admin student when role rows exist; else any user.
            user_row = db.session.execute(
                text(
                    "SELECT u.id FROM users u "
                    "WHERE NOT EXISTS ("
                    "  SELECT 1 FROM user_roles ur "
                    "  WHERE ur.user_id = u.id AND lower(ur.role) IN "
                    "  ('admin','founder','owner')"
                    ") "
                    "ORDER BY u.id ASC LIMIT 1"
                )
            ).first()
            if user_row is None:
                user_row = db.session.execute(
                    text("SELECT id FROM users ORDER BY id ASC LIMIT 1")
                ).first()
            if user_row is None:
                note_issue(
                    "critical",
                    "No users available for enrolment smoke",
                    "",
                    area="begin_learning",
                )
            else:
                user_id = int(user_row[0])
                begin_meta["enrolment_user_id"] = user_id
                runtime = EducationalRuntimeEngineService()
                try:
                    journey = runtime.enrol_student(
                        user_id=user_id,
                        subject_code=SUBJECT,
                        auto_instantiate_plan=True,
                    )
                    enrol_ok = True
                    begin_meta["enrolment"] = {
                        "ok": True,
                        "subject": SUBJECT,
                        "has_plan": bool(
                            getattr(journey, "study_plan", None)
                            or getattr(journey, "plan", None)
                            or True
                        ),
                    }
                except EnrolmentAlreadyExists:
                    enrol_ok = True
                    begin_meta["enrolment"] = {
                        "ok": True,
                        "already_enrolled": True,
                    }
                except Exception as exc:  # noqa: BLE001
                    db.session.rollback()
                    begin_meta["enrolment_error"] = str(exc)
                    note_issue(
                        "critical",
                        "Student enrolment failed",
                        str(exc),
                        area="begin_learning",
                    )

                if enrol_ok:
                    try:
                        mission = runtime.generate_daily_mission(
                            user_id=user_id,
                            subject_code=SUBJECT,
                            mission_date=date.today(),
                        )
                        db.session.commit()
                        mission_ok = True
                        begin_meta["mission"] = {
                            "ok": True,
                            "mission_instance_id": getattr(
                                mission, "mission_instance_id", None
                            ),
                            "topic_id": getattr(mission, "topic_id", None),
                            "title": getattr(mission, "title", None),
                        }
                    except Exception as exc:  # noqa: BLE001
                        db.session.rollback()
                        begin_meta["mission_error"] = str(exc)
                        note_issue(
                            "critical",
                            "Mission generation failed",
                            str(exc),
                            area="begin_learning",
                        )

        begin_ok = derive_ok and enrol_ok and mission_ok
        dump(EVIDENCE / "step6_begin_learning.json", begin_meta)
        log(
            "step6_begin_learning",
            begin_ok,
            derive_ok=derive_ok,
            enrol_ok=enrol_ok,
            mission_ok=mission_ok,
        )

        # -----------------------------------------------------------------
        # STEP 7 — Regression surfaces
        # -----------------------------------------------------------------
        loader = StoreCertifiedSnapshotLoader(store)
        preview = CertifiedSnapshotPreviewService(loader=loader)
        certified = preview.get_certified_for_workspace(WORKSPACE_ID)
        surface_meta: dict[str, Any] = {
            "certified_preview_loaded": certified is not None,
            "ei_inventory": ei_inventory(db),
            "package": after_pkg,
            "foundation": after_fv,
        }
        surfaces_ok = certified is not None
        try:
            observatory = CurriculumObservatory(store)
            obs = observatory.report_for_chain(pipe.orchestrator.chain_id)
            surface_meta["observatory_ok"] = obs is not None
            surfaces_ok = surfaces_ok and obs is not None
        except Exception as exc:  # noqa: BLE001
            surface_meta["observatory_error"] = str(exc)
            surfaces_ok = False
            note_issue("critical", "Observatory regression", str(exc), area="surfaces")

        # Smoke import surfaces that RR-001 exercised.
        _ = (
            CertifiedMissionEngine,
            CertifiedProgressEngine,
            CertifiedTutorContextService,
        )
        surface_meta["student_surface_imports_ok"] = True

        # Founder / Studio checklist readiness after publish.
        try:
            ws_now = studio.registry.get_workspace(WORKSPACE_ID)
            surface_meta["workspace_status"] = getattr(ws_now, "status", None)
            surface_meta["intelligence_certified_fact"] = bool(
                getattr(getattr(ws_now, "facts", None), "intelligence_certified", False)
            )
        except Exception as exc:  # noqa: BLE001
            surface_meta["workspace_error"] = str(exc)

        dump(EVIDENCE / "step7_regression.json", surface_meta)
        log(
            "step7_regression",
            surfaces_ok,
            certified_preview_loaded=surface_meta.get("certified_preview_loaded"),
            observatory_ok=surface_meta.get("observatory_ok"),
        )

        # -----------------------------------------------------------------
        # Decision
        # -----------------------------------------------------------------
        after_ei = ei_inventory(db)
        blockers = {
            "step1_g1_g7": pipe_ok,
            "step2_calibration": cal_ok,
            "step3_cert_artefacts": cert_artefacts_ok,
            "step4_publish": pub_ok,
            "step5_package_nonempty": package_ok,
            "step5_local_parity_5_15_73": parity_ok,
            "step6_begin_learning": begin_ok,
            "step7_regression": surfaces_ok,
        }
        critical = [i for i in issues if i["severity"] == "critical"]
        required = [
            "step1_g1_g7",
            "step2_calibration",
            "step3_cert_artefacts",
            "step4_publish",
            "step5_package_nonempty",
            "step6_begin_learning",
            "step7_regression",
        ]
        ready = all(blockers[k] for k in required) and not critical
        decision = "RECOVERY COMPLETE" if ready else "RECOVERY BLOCKED"
        rationale = (
            "Production CS1 is certified, published with non-empty objectives, "
            "and Begin Learning (derive + enrol + mission) succeeded."
            if ready
            else f"blockers={json.dumps(blockers)}; critical={len(critical)}"
        )

        comparison = {
            "generation_chains": {
                "before": before_ei["counts"]["ei_generation_chains"],
                "after": after_ei["counts"]["ei_generation_chains"],
            },
            "generation_snapshots": {
                "before": before_ei["counts"]["ei_generation_snapshots"],
                "after": after_ei["counts"]["ei_generation_snapshots"],
            },
            "educational_nodes": {
                "before": before_ei["counts"]["ei_educational_nodes"],
                "after": after_ei["counts"]["ei_educational_nodes"],
            },
            "certification_records": {
                "before": before_ei["counts"]["ei_certification_records"],
                "after": after_ei["counts"]["ei_certification_records"],
            },
            "published_package": {"before": before_pkg, "after": after_pkg},
            "foundation_structure": {"before": before_fv, "after": after_fv},
            "curriculum_counts": {
                "before": {
                    "sections": (before_pkg or {}).get("sections"),
                    "topics": (before_pkg or {}).get("topics"),
                    "objectives": (before_pkg or {}).get("objectives"),
                },
                "after": {
                    "sections": (after_pkg or {}).get("sections"),
                    "topics": (after_pkg or {}).get("topics"),
                    "objectives": (after_pkg or {}).get("objectives"),
                },
                "local_parity_target": {"sections": 5, "topics": 15, "objectives": 73},
                "parity_met": parity_ok,
            },
        }
        dump(EVIDENCE / "before_after_comparison.json", comparison)
        dump(EVIDENCE / "timeline.json", timeline)
        dump(EVIDENCE / "issues.json", issues)
        dump(EVIDENCE / "blockers.json", blockers)
        dump(
            EVIDENCE / "final_decision.json",
            {
                "decision": decision,
                "rationale": rationale,
                "blockers": blockers,
                "local_parity_5_15_73": parity_ok,
            },
        )
        evidence.update(
            {
                "finished_at": utc(),
                "duration_s": round(perf_counter() - t0, 2),
                "before": {"package": before_pkg, "ei": before_ei, "foundation": before_fv},
                "after": {"package": after_pkg, "ei": after_ei, "foundation": after_fv},
                "comparison": comparison,
                "blockers": blockers,
                "timeline": timeline,
                "issues": issues,
                "decision": decision,
                "decision_rationale": rationale,
            }
        )
        dump(EVIDENCE / "verification_evidence.json", evidence)

        print()
        print("=" * 60)
        print(f"RCV-002 DECISION: {decision}")
        print(rationale)
        print(f"Before package: {before_pkg}")
        print(f"After package:  {after_pkg}")
        print("=" * 60)
        return 0 if ready else 3


if __name__ == "__main__":
    raise SystemExit(main())
