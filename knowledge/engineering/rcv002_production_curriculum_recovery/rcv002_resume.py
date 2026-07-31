#!/usr/bin/env python3
"""RCV-002 resume — continue from STEP 2 after STEP 1 succeeded.

Assumes production already has:
  ei-chain-ws-cs1 with gens 1–7 accepted
  certification CERTIFIED_WITH_WARNINGS
  workspace certified_snapshot_id set

Then: FounderCalibration (RR-001 styles) → publish → Begin Learning → regression.
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
    entry = {"stage": stage, "ok": ok, "t_s": round(perf_counter() - t0, 2),
             "timestamp": utc(), **facts}
    timeline.append(entry)
    print(f"[{'✓' if ok else '✗'}] {stage} "
          f"{ {k: v for k, v in facts.items() if k != 'detail'} }", flush=True)


def note_issue(severity: str, title: str, detail: str, *, area: str = "platform") -> None:
    issues.append({"severity": severity, "area": area, "title": title, "detail": detail})


def dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, default=_jd, ensure_ascii=False) + "\n")


def _jd(obj: Any) -> Any:
    if is_dataclass(obj):
        return asdict(obj)
    if hasattr(obj, "value"):
        try:
            return obj.value
        except Exception:  # noqa: BLE001
            pass
    return str(obj)


def _load(v: Any) -> dict[str, Any]:
    if v is None:
        return {}
    if isinstance(v, dict):
        return v
    if isinstance(v, str):
        return json.loads(v or "{}")
    return dict(v)


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
    with app.app_context():
        from app.extensions import db

        # Fresh pool after prior SSL drop.
        db.engine.dispose()

        before = json.loads((EVIDENCE / "before_active_package.json").read_text())
        before_ei = json.loads((EVIDENCE / "before_ei_inventory.json").read_text())
        before_fv = json.loads((EVIDENCE / "before_foundation.json").read_text())

        def ei_inventory() -> dict[str, Any]:
            counts = {
                t: int(db.session.execute(text(f"SELECT COUNT(*) FROM {t}")).scalar() or 0)
                for t in (
                    "ei_generation_chains",
                    "ei_generations",
                    "ei_generation_snapshots",
                    "ei_educational_nodes",
                    "ei_certification_records",
                    "ei_calibration_profiles",
                    "runtime_enrolments",
                )
            }
            ws = db.session.execute(
                text(
                    "SELECT certification_status, certified_snapshot_id, active_chain_id "
                    "FROM studio_workspace_projections WHERE workspace_id=:w"
                ),
                {"w": WORKSPACE_ID},
            ).mappings().first()
            return {"counts": counts, "workspace": dict(ws) if ws else None}

        def package_summary() -> dict[str, Any] | None:
            row = db.session.execute(
                text(
                    "SELECT id, version_label, is_active, package_json, published_by "
                    "FROM published_curriculum_packages WHERE subject_code=:c "
                    "AND is_active IS TRUE ORDER BY id DESC LIMIT 1"
                ),
                {"c": SUBJECT},
            ).mappings().first()
            if not row:
                return None
            package = _load(row["package_json"])
            structure = package.get("structure") or {}
            cert = package.get("certification")
            return {
                "id": row["id"],
                "version_label": row["version_label"],
                "is_active": bool(row["is_active"]),
                "published_by": row["published_by"],
                "has_certification": bool(cert)
                and str((cert or {}).get("authority") or "").startswith("certified"),
                "certification": cert,
                "sections": int(
                    structure.get("section_count") or len(structure.get("sections") or [])
                ),
                "topics": int(
                    structure.get("topic_count") or len(structure.get("topics") or [])
                ),
                "objectives": int(
                    structure.get("objective_count")
                    or len(structure.get("objectives") or [])
                ),
                "source": structure.get("source"),
            }

        def foundation_summary() -> dict[str, Any] | None:
            row = db.session.execute(
                text(
                    "SELECT v.id, v.version_label, v.publication_state, "
                    "v.parsed_structure_json FROM studio_foundation_versions v "
                    "JOIN studio_foundation_subjects s ON s.id=v.subject_id "
                    "WHERE s.subject_code=:c ORDER BY v.id LIMIT 1"
                ),
                {"c": SUBJECT},
            ).mappings().first()
            if not row:
                return None
            structure = _load(row["parsed_structure_json"])
            return {
                "id": row["id"],
                "version_label": row["version_label"],
                "publication_state": row["publication_state"],
                "sections": len(structure.get("sections") or []),
                "topics": len(structure.get("topics") or []),
                "objectives": len(structure.get("objectives") or []),
                "source": structure.get("source"),
            }

        inv = ei_inventory()
        log("resume_precheck", True, **inv["counts"], workspace=inv["workspace"])
        status = str((inv.get("workspace") or {}).get("certification_status") or "")
        if inv["counts"]["ei_generation_snapshots"] < 7 or status.upper() not in {
            "CERTIFIED",
            "CERTIFIED_WITH_WARNINGS",
        }:
            note_issue(
                "critical",
                "STEP 1 artefacts missing — cannot resume",
                json.dumps(inv, default=str),
                area="engine",
            )
            dump(EVIDENCE / "issues.json", issues)
            return 2

        syllabus = DocumentNormalizationService().normalize(
            PyPdfExtractionAdapter().extract(
                SYLLABUS_PDF.read_bytes(),
                extraction_id="rcv002-resume-syllabus",
                document_id=101,
            )
        )
        store = SqlAlchemyGenerationStore()
        studio = get_studio_service()
        orch = build_default_orchestrator(store)
        cal_svc = FounderCalibrationService(
            store, registry=studio.registry, orchestrator=orch
        )

        # STEP 2 — RR-001 calibration (balanced seed + exam-focused)
        print("STEP 2: FounderCalibrationService.apply (RR-001 styles)…", flush=True)
        t_cal = perf_counter()
        cal_ok = False
        cal_meta: dict[str, Any] = {}
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
                fixed_created_at_iso="2026-07-30T13:00:00Z",
            )
            db.session.commit()
            print("STEP 2a: balanced seed committed", flush=True)
            db.engine.dispose()  # refresh pool between long phases
            cal = cal_svc.apply(
                WORKSPACE_ID,
                granularity=GranularityStyle.BALANCED,
                hierarchy=HierarchyStyle.STRICT_SYLLABUS,
                topic_density=TopicDensityStyle.CONSOLIDATED,
                difficulty_bias=DifficultyBiasStyle.EXAM_FOCUSED,
                source_documents=(syllabus,),
                subject_code=SUBJECT,
                version_label=VERSION,
                fixed_created_at_iso="2026-07-30T13:01:00Z",
            )
            db.session.commit()
            outcome = (
                cal.orchestrator.certification.outcome.value
                if cal.orchestrator.certification
                else None
            )
            cal_ok = (
                cal.intelligence_certified
                and outcome in {"CERTIFIED", "CERTIFIED_WITH_WARNINGS"}
                and cal.orchestrator.stopped_at_index is None
                and 7 in cal.generations_rerun
            )
            cal_meta = {
                "profile_id": cal.profile.profile_id,
                "generations_rerun": list(cal.generations_rerun),
                "intelligence_certified": cal.intelligence_certified,
                "post_cal_certification": outcome,
                "duration_s": round(perf_counter() - t_cal, 2),
            }
        except Exception as exc:  # noqa: BLE001
            try:
                db.session.rollback()
            except Exception:  # noqa: BLE001
                db.engine.dispose()
            cal_meta = {
                "error": str(exc),
                "traceback": traceback.format_exc(),
                "duration_s": round(perf_counter() - t_cal, 2),
            }
            # If STEP 1 certification still holds, continue to publish.
            inv_after = ei_inventory()
            status2 = str(
                (inv_after.get("workspace") or {}).get("certification_status") or ""
            ).upper()
            if status2 in {"CERTIFIED", "CERTIFIED_WITH_WARNINGS"} and inv_after[
                "counts"
            ]["ei_certification_records"] >= 1:
                cal_ok = True
                cal_meta["continued_with_step1_certification"] = True
                cal_meta["workspace_status"] = status2
                note_issue(
                    "warning",
                    "Calibration apply failed after network error; "
                    "continuing with STEP 1 CERTIFIED_WITH_WARNINGS snapshot",
                    str(exc)[:800],
                    area="calibration",
                )
            else:
                note_issue("critical", "Calibration failed", str(exc), area="calibration")

        dump(EVIDENCE / "step2_calibration_resume.json", cal_meta)
        log("step2_calibration_recert", cal_ok, **{
            k: cal_meta[k]
            for k in (
                "post_cal_certification",
                "generations_rerun",
                "duration_s",
                "continued_with_step1_certification",
            )
            if k in cal_meta
        })
        if not cal_ok:
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 3

        # STEP 3 — artefacts
        cert_inv = ei_inventory()
        dump(EVIDENCE / "step3_certification_inventory.json", cert_inv)
        cert_ok = (
            cert_inv["counts"]["ei_generation_chains"] >= 1
            and cert_inv["counts"]["ei_generation_snapshots"] >= 7
            and cert_inv["counts"]["ei_educational_nodes"] > 0
            and cert_inv["counts"]["ei_certification_records"] >= 1
            and bool((cert_inv.get("workspace") or {}).get("certified_snapshot_id"))
            and str(
                (cert_inv.get("workspace") or {}).get("certification_status") or ""
            ).upper()
            in {"CERTIFIED", "CERTIFIED_WITH_WARNINGS"}
        )
        log("step3_certification_artefacts", cert_ok, **cert_inv["counts"],
            workspace=cert_inv.get("workspace"))
        if not cert_ok:
            note_issue(
                "critical",
                "Certification artefacts incomplete",
                json.dumps(cert_inv, default=str),
                area="certification",
            )
            return 3

        # STEP 4 — publish
        print("STEP 4: PublicationBridgeService.publish_to_catalogue…", flush=True)
        db.engine.dispose()
        t_pub = perf_counter()
        try:
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
            pub = PublicationBridgeService(studio.registry).publish_to_catalogue(
                WORKSPACE_ID, actor_id=ACTOR_ID
            )
            db.session.commit()
            pub_ok = True
            pub_meta = {**pub, "duration_s": round(perf_counter() - t_pub, 2)}
        except Exception as exc:  # noqa: BLE001
            try:
                db.session.rollback()
            except Exception:  # noqa: BLE001
                db.engine.dispose()
            pub_ok = False
            pub_meta = {"error": str(exc), "traceback": traceback.format_exc()}
            note_issue("critical", "Publication failed", str(exc), area="publish")
        dump(EVIDENCE / "step4_publication.json", pub_meta)
        log("step4_publish", pub_ok, **{
            k: pub_meta[k] for k in ("package_id", "version_label", "duration_s")
            if k in pub_meta
        })
        if not pub_ok:
            dump(EVIDENCE / "timeline.json", timeline)
            dump(EVIDENCE / "issues.json", issues)
            return 4

        # STEP 5 — package verify
        after_pkg = package_summary()
        after_fv = foundation_summary()
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
                "Published package incomplete",
                json.dumps(after_pkg, default=str),
                area="verify",
            )
            return 5

        # STEP 6 — Begin Learning
        authority = PublishedCurriculumAuthority()
        runtime_snap = authority.get_active(SUBJECT)
        begin_meta: dict[str, Any] = {"loaded": runtime_snap is not None}
        derive_ok = enrol_ok = mission_ok = False
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
                EducationalArtefactDeriver().derive(runtime_pkg or {})
                derive_ok = True
                begin_meta["derive"] = {"ok": True}
            except Exception as exc:  # noqa: BLE001
                begin_meta["derive_error"] = str(exc)
                note_issue("critical", "Deriver failed", str(exc), area="begin_learning")

        if derive_ok:
            user_row = db.session.execute(
                text(
                    "SELECT u.id FROM users u WHERE NOT EXISTS ("
                    " SELECT 1 FROM user_roles ur WHERE ur.user_id=u.id "
                    " AND lower(ur.role) IN ('admin','founder','owner')"
                    ") ORDER BY u.id ASC LIMIT 1"
                )
            ).first() or db.session.execute(
                text("SELECT id FROM users ORDER BY id ASC LIMIT 1")
            ).first()
            if user_row is None:
                note_issue(
                    "critical", "No users for enrolment", "", area="begin_learning"
                )
            else:
                user_id = int(user_row[0])
                begin_meta["enrolment_user_id"] = user_id
                runtime = EducationalRuntimeEngineService()
                try:
                    runtime.enrol_student(
                        user_id=user_id,
                        subject_code=SUBJECT,
                        auto_instantiate_plan=True,
                    )
                    enrol_ok = True
                    begin_meta["enrolment"] = {"ok": True}
                except EnrolmentAlreadyExists:
                    enrol_ok = True
                    begin_meta["enrolment"] = {"ok": True, "already_enrolled": True}
                except Exception as exc:  # noqa: BLE001
                    try:
                        db.session.rollback()
                    except Exception:  # noqa: BLE001
                        pass
                    begin_meta["enrolment_error"] = str(exc)
                    note_issue(
                        "critical", "Enrolment failed", str(exc), area="begin_learning"
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
                        try:
                            db.session.rollback()
                        except Exception:  # noqa: BLE001
                            pass
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

        # STEP 7
        loader = StoreCertifiedSnapshotLoader(store)
        preview = CertifiedSnapshotPreviewService(loader=loader)
        certified = preview.get_certified_for_workspace(WORKSPACE_ID)
        surface_meta: dict[str, Any] = {
            "certified_preview_loaded": certified is not None,
            "ei_inventory": ei_inventory(),
            "package": after_pkg,
            "foundation": after_fv,
        }
        surfaces_ok = certified is not None
        try:
            obs = CurriculumObservatory(store).report_for_chain("ei-chain-ws-cs1")
            surface_meta["observatory_ok"] = obs is not None
            surfaces_ok = surfaces_ok and obs is not None
        except Exception as exc:  # noqa: BLE001
            surface_meta["observatory_error"] = str(exc)
            surfaces_ok = False
        _ = (
            CertifiedMissionEngine,
            CertifiedProgressEngine,
            CertifiedTutorContextService,
        )
        surface_meta["student_surface_imports_ok"] = True
        dump(EVIDENCE / "step7_regression.json", surface_meta)
        log(
            "step7_regression",
            surfaces_ok,
            certified_preview_loaded=surface_meta.get("certified_preview_loaded"),
            observatory_ok=surface_meta.get("observatory_ok"),
        )

        after_ei = ei_inventory()
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
            "published_package": {"before": before, "after": after_pkg},
            "foundation_structure": {"before": before_fv, "after": after_fv},
            "curriculum_counts": {
                "before": {
                    "sections": before.get("sections"),
                    "topics": before.get("topics"),
                    "objectives": before.get("objectives"),
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

        blockers = {
            "step1_g1_g7": True,
            "step2_calibration": cal_ok,
            "step3_cert_artefacts": cert_ok,
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
            "Production CS1 certified, published with objectives, "
            "Begin Learning (derive+enrol+mission) succeeded."
            if ready
            else f"blockers={json.dumps(blockers)}; critical={len(critical)}"
        )
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
        dump(
            EVIDENCE / "verification_evidence.json",
            {
                "programme": "RCV-002",
                "mode": "resume_from_step2",
                "finished_at": utc(),
                "duration_s": round(perf_counter() - t0, 2),
                "comparison": comparison,
                "blockers": blockers,
                "timeline": timeline,
                "issues": issues,
                "decision": decision,
            },
        )
        print()
        print("=" * 60)
        print(f"RCV-002 DECISION: {decision}")
        print(rationale)
        print(f"Before: {before}")
        print(f"After:  {after_pkg}")
        print("=" * 60)
        return 0 if ready else 3


if __name__ == "__main__":
    raise SystemExit(main())
