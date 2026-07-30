"""UX-001 — Lightweight Founder Curriculum Health projection.

Read-only presentation over existing EI services. No new architecture.
"""

from __future__ import annotations

import json
from dataclasses import dataclass


@dataclass(frozen=True)
class CurriculumHealthMetric:
    label: str
    value: str
    detail: str = ""


@dataclass(frozen=True)
class CurriculumHealthRow:
    workspace_id: str
    subject_label: str
    publication_status: str
    certification_status: str
    review_pack_label: str
    review_pack_href: str
    calibration_label: str
    observatory_summary: str
    workspace_href: str


@dataclass(frozen=True)
class FounderCurriculumHealthPage:
    page_title: str
    page_support: str
    rows: tuple[CurriculumHealthRow, ...]
    metrics: tuple[CurriculumHealthMetric, ...]
    empty_reason: str


def _metric_triplet(metrics: tuple) -> str:
    if not metrics:
        return "No observatory metrics"
    top = metrics[:3]
    return " · ".join(
        f"{m.name}: {m.value:g}{(' ' + m.unit) if m.unit else ''}" for m in top
    )


class FounderCurriculumHealthService:
    """Aggregate publication + certification + observatory for Founder UI."""

    def build(self) -> FounderCurriculumHealthPage:
        from flask import url_for

        rows: list[CurriculumHealthRow] = []
        metrics: list[CurriculumHealthMetric] = []

        try:
            from app.application.curriculum_intelligence.curriculum_observatory import (
                CurriculumObservatory,
            )
            from app.application.curriculum_intelligence.founder_preview import (
                CertifiedSnapshotPreviewService,
            )
            from app.application.curriculum_studio_foundation.authority import (
                PublishedCurriculumAuthority,
            )
            from app.infrastructure.adapters.curriculum_intelligence import (
                SqlAlchemyGenerationStore,
                StoreCertifiedSnapshotLoader,
            )
            from app.models.curriculum_studio_foundation import (
                StudioWorkspaceProjection,
            )

            workspaces = (
                StudioWorkspaceProjection.query.order_by(
                    StudioWorkspaceProjection.updated_at.desc()
                )
                .limit(12)
                .all()
            )
            store = SqlAlchemyGenerationStore()
            observatory = CurriculumObservatory(store)
            preview = CertifiedSnapshotPreviewService(
                loader=StoreCertifiedSnapshotLoader(store)
            )
            authority = PublishedCurriculumAuthority()

            certified_count = 0
            published_count = 0
            for ws in workspaces:
                wid = str(ws.workspace_id)
                subject = (
                    f"{(ws.subject_code or '').strip()} · "
                    f"{(ws.subject_title or '').strip()}"
                ).strip(" ·")
                pub_status = (ws.current_stage or ws.status or "draft").strip()
                code = (ws.subject_code or "").strip()
                try:
                    if code and authority.get_active(code) is not None:
                        pub_status = "Published"
                        published_count += 1
                except Exception:  # noqa: BLE001
                    pass

                cert_status = (ws.certification_status or "Not certified").strip()
                try:
                    certified = preview.get_certified_for_workspace(wid)
                    if certified is not None:
                        outcome = getattr(certified, "certification_status", None)
                        if outcome is not None:
                            cert_status = str(
                                getattr(outcome, "value", outcome)
                            )
                        elif cert_status.lower() in {"", "not certified", "none"}:
                            cert_status = "Certified"
                        certified_count += 1
                except Exception:  # noqa: BLE001
                    if not cert_status:
                        cert_status = "Unavailable"

                review_label = "Not available"
                review_href = url_for("curriculum_studio.workspace", workspace_id=wid)
                if (ws.review_pack_ref or "").strip():
                    review_label = "Review pack available"
                else:
                    try:
                        meta = json.loads(ws.metadata_json or "{}")
                    except (TypeError, ValueError):
                        meta = {}
                    if isinstance(meta, dict) and (
                        meta.get("review_pack_ref") or meta.get("review_pack")
                    ):
                        review_label = "Review pack available"

                calib_label = "No calibration yet"
                if (ws.calibration_profile_id or "").strip():
                    calib_label = "Calibration profile bound"
                obs_summary = "No observatory metrics"
                try:
                    report = observatory.report_for_workspace(wid)
                    parts = []
                    if report.certification_trends:
                        parts.append(_metric_triplet(report.certification_trends))
                    if report.calibration_frequency:
                        calib_label = _metric_triplet(report.calibration_frequency)
                    if report.coverage_metrics:
                        parts.append(_metric_triplet(report.coverage_metrics))
                    if parts:
                        obs_summary = " · ".join(parts[:2])
                except Exception:  # noqa: BLE001
                    pass

                rows.append(
                    CurriculumHealthRow(
                        workspace_id=wid,
                        subject_label=subject or wid,
                        publication_status=pub_status,
                        certification_status=str(cert_status),
                        review_pack_label=review_label,
                        review_pack_href=review_href,
                        calibration_label=calib_label,
                        observatory_summary=obs_summary,
                        workspace_href=review_href,
                    )
                )

            metrics.extend(
                [
                    CurriculumHealthMetric(
                        label="Workspaces reviewed",
                        value=str(len(rows)),
                    ),
                    CurriculumHealthMetric(
                        label="Certified",
                        value=str(certified_count),
                    ),
                    CurriculumHealthMetric(
                        label="Published",
                        value=str(published_count),
                    ),
                ]
            )
        except Exception:  # noqa: BLE001 — Founder UI must soft-fail
            return FounderCurriculumHealthPage(
                page_title="Curriculum Health",
                page_support="Publication, certification, and observatory at a glance.",
                rows=(),
                metrics=(),
                empty_reason=(
                    "Curriculum health is temporarily unavailable. "
                    "Open Curriculum Studio to continue publication work."
                ),
            )

        return FounderCurriculumHealthPage(
            page_title="Curriculum Health",
            page_support=(
                "Certification, publication, review packs, calibration, "
                "and observatory — without engineering noise."
            ),
            rows=tuple(rows),
            metrics=tuple(metrics),
            empty_reason=(
                "No curriculum workspaces yet. Create a subject in Curriculum Studio."
                if not rows
                else ""
            ),
        )
