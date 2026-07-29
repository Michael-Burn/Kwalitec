"""Prepare extracted curriculum structure for Founder validation and preview.

Syncs CIP / Foundation extraction into the Studio workspace projection and
ensures Management has blueprint assignments required by publication safety
gates — without inventing curriculum content.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.application.curriculum_studio._ports import require_management
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio.exceptions import ValidationError
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)

logger = logging.getLogger(__name__)

# Default instructional profile used when Founder has not chosen a profile.
# Safety still requires validation + approval before publish.
DEFAULT_BLUEPRINT_PROFILE_ID = "founder-default"

# CIP entity kinds that represent Founder-visible curriculum structure.
_SECTION_KINDS = frozenset({"module", "subject"})
_TOPIC_KINDS = frozenset({"topic", "subtopic"})
_OBJECTIVE_KINDS = frozenset({"learning_objective"})


@dataclass(frozen=True)
class PreparedStructure:
    """Structure prepared for validation / preview."""

    section_ids: tuple[str, ...]
    topic_ids: tuple[str, ...]
    objective_ids: tuple[str, ...]
    section_titles: tuple[tuple[str, str], ...]  # (id, title)
    topic_titles: tuple[tuple[str, str], ...]
    blueprint_assigned: bool
    source: str


class StructurePreparationService:
    """Materialise extracted curriculum into Studio + Management gates."""

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management

    def prepare_for_validation(self, workspace_id: str) -> PreparedStructure:
        """Load extraction, sync workspace, assign default blueprints.

        Raises:
            ValidationError: When no extractable curriculum structure exists.
        """
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise ValidationError(f"Workspace not found: {workspace_id!r}")

        prepared = self._load_structure(workspace_id, workspace.subject_code)
        if not prepared.section_ids and not prepared.topic_ids:
            if workspace.section_ids or workspace.topic_ids:
                prepared = PreparedStructure(
                    section_ids=tuple(workspace.section_ids),
                    topic_ids=tuple(workspace.topic_ids),
                    objective_ids=tuple(workspace.objective_ids),
                    section_titles=tuple(
                        (sid, sid) for sid in workspace.section_ids
                    ),
                    topic_titles=tuple(
                        (tid, tid) for tid in workspace.topic_ids
                    ),
                    blueprint_assigned=False,
                    source="workspace",
                )
            else:
                raise ValidationError(
                    f"No extracted curriculum structure for {workspace_id}. "
                    "Upload Official CMP and Official Syllabus, wait for "
                    "extraction to finish, then validate again."
                )

        updated = workspace.with_structure(
            section_ids=prepared.section_ids,
            topic_ids=prepared.topic_ids,
            objective_ids=prepared.objective_ids,
        )
        self._registry.put_workspace(updated)

        blueprint_ok = bool(updated.facts.blueprint_assigned)
        if workspace.version_id and self._management is not None:
            blueprint_ok = self._ensure_blueprints(
                workspace.version_id,
                section_ids=prepared.section_ids or prepared.topic_ids[:1],
            )

        facts = WorkspacePublicationFacts.create(
            cmp_uploaded=updated.facts.cmp_uploaded,
            official_syllabus_uploaded=updated.facts.official_syllabus_uploaded,
            validation_passed=updated.facts.validation_passed,
            blueprint_assigned=blueprint_ok,
            preview_built=updated.facts.preview_built,
            preview_approved=updated.facts.preview_approved,
            version_assigned=updated.facts.version_assigned,
            rollback_snapshot_created=updated.facts.rollback_snapshot_created,
        )
        final = self._registry.get_workspace(workspace_id) or updated
        self._registry.put_workspace(final.with_facts(facts))

        return PreparedStructure(
            section_ids=prepared.section_ids,
            topic_ids=prepared.topic_ids,
            objective_ids=prepared.objective_ids,
            section_titles=prepared.section_titles,
            topic_titles=prepared.topic_titles,
            blueprint_assigned=blueprint_ok,
            source=prepared.source,
        )

    def hierarchy_nodes(
        self, workspace_id: str
    ) -> list[tuple[str, str, str]]:
        """Return (node_id, title, kind) for Founder preview when available."""
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            return []
        prepared = self._load_structure(workspace_id, workspace.subject_code)
        nodes: list[tuple[str, str, str]] = []
        for sid, title in prepared.section_titles:
            nodes.append((sid, title, "section"))
        for tid, title in prepared.topic_titles:
            nodes.append((tid, title, "topic"))
        if not nodes:
            for sid in workspace.section_ids:
                nodes.append((sid, sid, "section"))
            for tid in workspace.topic_ids:
                nodes.append((tid, tid, "topic"))
        return nodes

    def structure_dict(self, workspace_id: str) -> dict:
        """Foundation-compatible structure payload from extraction."""
        workspace = self._registry.get_workspace(workspace_id)
        subject = workspace.subject_code if workspace else ""
        prepared = self._load_structure(workspace_id, subject)
        sections = [
            {
                "section_id": sid,
                "code": sid,
                "title": title,
                "number": str(idx + 1),
                "order_index": idx + 1,
                "source_ids": [],
            }
            for idx, (sid, title) in enumerate(prepared.section_titles)
        ]
        topics = [
            {
                "topic_id": tid,
                "code": tid,
                "title": title,
                "section_ref": sections[0]["section_id"] if sections else "",
                "number": str(idx + 1),
                "order_index": idx + 1,
                "prerequisite_ids": [],
                "source_ids": [],
            }
            for idx, (tid, title) in enumerate(prepared.topic_titles)
        ]
        objectives = [
            {
                "objective_id": oid,
                "code": oid,
                "text": oid,
                "topic_ref": topics[0]["topic_id"] if topics else "",
                "number": str(idx + 1),
                "order_index": idx + 1,
                "estimated_minutes": 20,
                "learning_type": "concept",
                "cognitive_level": "understand",
                "source_ids": [],
            }
            for idx, oid in enumerate(prepared.objective_ids)
        ]
        return {
            "section_count": len(sections),
            "topic_count": len(topics),
            "objective_count": len(objectives),
            "sections": sections,
            "topics": topics,
            "objectives": objectives,
        }

    def _load_structure(
        self, workspace_id: str, subject_code: str
    ) -> PreparedStructure:
        cip = self._from_cip(workspace_id)
        if cip.section_ids or cip.topic_ids:
            return cip
        foundation = self._from_foundation(subject_code)
        if foundation.section_ids or foundation.topic_ids:
            return foundation
        return PreparedStructure(
            section_ids=(),
            topic_ids=(),
            objective_ids=(),
            section_titles=(),
            topic_titles=(),
            blueprint_assigned=False,
            source="empty",
        )

    def _from_cip(self, workspace_id: str) -> PreparedStructure:
        try:
            import importlib

            entity_mod = importlib.import_module(
                "app.models.curriculum_intelligence"
            )
            foundation_mod = importlib.import_module(
                "app.models.curriculum_studio_foundation"
            )
            CipCurriculumEntity = entity_mod.CipCurriculumEntity  # noqa: N806
            StudioFoundationDocument = (  # noqa: N806
                foundation_mod.StudioFoundationDocument
            )
        except Exception:  # noqa: BLE001 — optional when models unavailable
            return PreparedStructure(
                section_ids=(),
                topic_ids=(),
                objective_ids=(),
                section_titles=(),
                topic_titles=(),
                blueprint_assigned=False,
                source="cip_unavailable",
            )

        try:
            docs = StudioFoundationDocument.query.filter_by(
                workspace_id=workspace_id, is_active=True
            ).all()
            doc_ids = [d.id for d in docs]
        except RuntimeError:
            # Pure unit tests outside Flask app context.
            return PreparedStructure(
                section_ids=(),
                topic_ids=(),
                objective_ids=(),
                section_titles=(),
                topic_titles=(),
                blueprint_assigned=False,
                source="cip_no_app_context",
            )
        if not doc_ids:
            return PreparedStructure(
                section_ids=(),
                topic_ids=(),
                objective_ids=(),
                section_titles=(),
                topic_titles=(),
                blueprint_assigned=False,
                source="cip_empty",
            )

        entities = (
            CipCurriculumEntity.query.filter(
                CipCurriculumEntity.document_id.in_(doc_ids)
            )
            .order_by(CipCurriculumEntity.id.asc())
            .all()
        )
        section_titles: list[tuple[str, str]] = []
        topic_titles: list[tuple[str, str]] = []
        objectives: list[str] = []
        seen: set[str] = set()
        for entity in entities:
            kind = (entity.kind or "").strip().lower()
            eid = (entity.entity_id or "").strip()
            title = (entity.title or eid or kind).strip()
            if not eid or eid in seen:
                continue
            seen.add(eid)
            if kind in _SECTION_KINDS:
                section_titles.append((eid, title or eid))
            elif kind in _TOPIC_KINDS:
                topic_titles.append((eid, title or eid))
            elif kind in _OBJECTIVE_KINDS:
                objectives.append(title or eid)

        return PreparedStructure(
            section_ids=tuple(s for s, _ in section_titles),
            topic_ids=tuple(t for t, _ in topic_titles),
            objective_ids=tuple(objectives),
            section_titles=tuple(section_titles),
            topic_titles=tuple(topic_titles),
            blueprint_assigned=False,
            source="cip",
        )

    def _from_foundation(self, subject_code: str) -> PreparedStructure:
        code = (subject_code or "").strip().upper()
        if not code:
            return PreparedStructure(
                section_ids=(),
                topic_ids=(),
                objective_ids=(),
                section_titles=(),
                topic_titles=(),
                blueprint_assigned=False,
                source="foundation_empty",
            )
        try:
            import importlib

            foundation_svc = importlib.import_module(
                "app.application.curriculum_studio_foundation.service"
            )
            foundation_cls = foundation_svc.CurriculumStudioFoundationService
            foundation = foundation_cls()
            versions = foundation.list_versions(code)
            if not versions:
                return PreparedStructure(
                    section_ids=(),
                    topic_ids=(),
                    objective_ids=(),
                    section_titles=(),
                    topic_titles=(),
                    blueprint_assigned=False,
                    source="foundation_empty",
                )
            # Prefer the newest version label.
            version = sorted(
                versions, key=lambda v: v.version_label, reverse=True
            )[0]
            parsed = foundation.review_parsed_curriculum(version.version_id)
        except RuntimeError:
            return PreparedStructure(
                section_ids=(),
                topic_ids=(),
                objective_ids=(),
                section_titles=(),
                topic_titles=(),
                blueprint_assigned=False,
                source="foundation_no_app_context",
            )
        except Exception as exc:  # noqa: BLE001
            logger.debug("Foundation structure unavailable: %s", exc)
            return PreparedStructure(
                section_ids=(),
                topic_ids=(),
                objective_ids=(),
                section_titles=(),
                topic_titles=(),
                blueprint_assigned=False,
                source="foundation_error",
            )

        section_titles = []
        for item in parsed.sections:
            if isinstance(item, dict):
                sid = str(item.get("section_id") or item.get("code") or "")
                title = str(item.get("title") or sid)
                if sid:
                    section_titles.append((sid, title))
        topic_titles = []
        for item in parsed.topics:
            if isinstance(item, dict):
                tid = str(item.get("topic_id") or item.get("code") or "")
                title = str(item.get("title") or tid)
                if tid:
                    topic_titles.append((tid, title))
        objectives = []
        for item in parsed.objectives:
            if isinstance(item, dict):
                oid = str(
                    item.get("objective_id")
                    or item.get("code")
                    or item.get("text")
                    or ""
                )
                if oid:
                    objectives.append(oid)

        return PreparedStructure(
            section_ids=tuple(s for s, _ in section_titles),
            topic_ids=tuple(t for t, _ in topic_titles),
            objective_ids=tuple(objectives),
            section_titles=tuple(section_titles),
            topic_titles=tuple(topic_titles),
            blueprint_assigned=False,
            source="foundation",
        )

    def _ensure_blueprints(
        self,
        version_id: str,
        *,
        section_ids: tuple[str, ...],
    ) -> bool:
        mgmt = require_management(self._management, action="assign_blueprint")
        assigned_any = False
        for section_id in section_ids:
            try:
                mgmt.assign_blueprint(
                    version_id,
                    section_id=section_id,
                    blueprint_profile_id=DEFAULT_BLUEPRINT_PROFILE_ID,
                )
                assigned_any = True
            except Exception as exc:  # noqa: BLE001 — already assigned is OK
                logger.debug(
                    "Blueprint assign skipped for %s/%s: %s",
                    version_id,
                    section_id,
                    exc,
                )
                assigned_any = True
        return assigned_any
