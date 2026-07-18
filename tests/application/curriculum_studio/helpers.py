"""Shared helpers for Curriculum Studio application tests."""

from __future__ import annotations

from typing import Any

from app.application.curriculum_studio.curriculum_studio_service import (
    CurriculumStudioService,
)
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)


class FakeManagementPort:
    """Stateful test double for CurriculumManagementPort."""

    def __init__(
        self,
        *,
        available: bool = True,
        subjects: dict[str, dict[str, Any]] | None = None,
    ) -> None:
        self._available = available
        self._subjects: dict[str, dict[str, Any]] = {
            k.upper(): dict(v) for k, v in (subjects or {}).items()
        }
        self._versions: dict[str, dict[str, Any]] = {}
        self._assets: dict[str, list[dict[str, Any]]] = {}
        self._validations: dict[str, dict[str, Any]] = {}
        self._previews: dict[str, dict[str, Any]] = {}
        self._seq = 0
        self.publish_calls: list[str] = []
        self.approve_calls: list[str] = []
        self.archive_calls: list[str] = []
        self.validate_calls: list[str] = []

    @property
    def component_id(self) -> str:
        return "curriculum_management"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def create_subject(
        self,
        subject_code: str,
        *,
        title: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        code = subject_code.strip().upper()
        summary = {
            "subject_code": code,
            "title": title,
            "subject_id": f"sub-{code.lower()}",
            "active_version_id": None,
            "version_count": 0,
            "publication_state": None,
            "metadata": dict(metadata or {}),
        }
        self._subjects[code] = summary
        return dict(summary)

    def get_subject_summary(self, subject_code: str) -> dict[str, Any] | None:
        item = self._subjects.get(subject_code.strip().upper())
        return None if item is None else dict(item)

    def list_subjects(self) -> tuple[dict[str, Any], ...]:
        return tuple(dict(s) for s in self._subjects.values())

    def create_version(
        self,
        subject_code: str,
        version_label: str,
        *,
        version_id: str | None = None,
        parent_version_id: str | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        code = subject_code.strip().upper()
        self._seq += 1
        vid = version_id or f"ver-{code.lower()}-{self._seq}"
        if vid in self._versions:
            raise ValueError(f"duplicate version {vid}")
        summary = {
            "version_id": vid,
            "subject_code": code,
            "version_label": version_label,
            "status": "draft",
            "publication_state": "draft",
            "parent_version_id": parent_version_id,
            "notes": notes,
            "created_at": "created",
            "rollback_snapshot_id": None,
            "rollback_eligible": False,
        }
        self._versions[vid] = summary
        self._assets[vid] = []
        sub = self._subjects.get(code)
        if sub is not None:
            sub["version_count"] = int(sub.get("version_count") or 0) + 1
        return dict(summary)

    def get_version_summary(self, version_id: str) -> dict[str, Any] | None:
        item = self._versions.get(version_id)
        return None if item is None else dict(item)

    def list_versions(self, subject_code: str) -> tuple[dict[str, Any], ...]:
        code = subject_code.strip().upper()
        return tuple(
            dict(v)
            for v in self._versions.values()
            if v.get("subject_code") == code
        )

    def archive_version(
        self, version_id: str, *, occurred_at: str = ""
    ) -> dict[str, Any]:
        return self.archive(version_id, occurred_at=occurred_at)

    def rollback_version(
        self, version_id: str, *, occurred_at: str = ""
    ) -> dict[str, Any]:
        ver = self._require_version(version_id)
        if not ver.get("rollback_eligible") and not ver.get(
            "rollback_snapshot_id"
        ):
            raise ValueError("not rollback eligible")
        ver["status"] = "published"
        ver["publication_state"] = "published"
        ver["published_at"] = occurred_at or "rolled_back"
        return dict(ver)

    def add_asset_ref(
        self,
        version_id: str,
        *,
        kind: str,
        reference: str,
        asset_id: str | None = None,
    ) -> dict[str, Any]:
        self._require_version(version_id)
        self._seq += 1
        asset = {
            "asset_id": asset_id or f"asset-{self._seq}",
            "kind": kind,
            "reference": reference,
        }
        self._assets.setdefault(version_id, []).append(asset)
        ver = self._versions[version_id]
        if ver.get("publication_state") == "draft":
            ver["publication_state"] = "uploaded"
            ver["status"] = "uploaded"
        return dict(asset)

    def list_assets(self, version_id: str) -> tuple[dict[str, Any], ...]:
        return tuple(dict(a) for a in self._assets.get(version_id, []))

    def assign_blueprint(
        self,
        version_id: str,
        *,
        section_id: str,
        blueprint_profile_id: str,
    ) -> dict[str, Any]:
        ver = self._require_version(version_id)
        ver["blueprint_assigned"] = True
        ver["publication_state"] = "blueprint_assigned"
        return {
            "version_id": version_id,
            "section_id": section_id,
            "blueprint_profile_id": blueprint_profile_id,
        }

    def validate_version(self, version_id: str) -> dict[str, Any]:
        self._require_version(version_id)
        self.validate_calls.append(version_id)
        report = {
            "version_id": version_id,
            "passed": True,
            "readiness": "passed",
            "errors": (),
            "warnings": (),
        }
        self._validations[version_id] = report
        self._versions[version_id]["publication_state"] = "validated"
        self._versions[version_id]["status"] = "validated"
        return dict(report)

    def latest_validation(self, version_id: str) -> dict[str, Any] | None:
        item = self._validations.get(version_id)
        return None if item is None else dict(item)

    def preview_version(self, version_id: str) -> dict[str, Any]:
        ver = self._require_version(version_id)
        payload = {
            "version_id": version_id,
            "subject_code": ver["subject_code"],
            "hierarchy": [
                {
                    "node_id": "sec-1",
                    "title": "Section 1",
                    "kind": "section",
                    "order_index": 0,
                },
                {
                    "node_id": "topic-1",
                    "title": "Topic 1",
                    "kind": "topic",
                    "parent_id": "sec-1",
                    "order_index": 1,
                },
            ],
            "objectives": ("obj-1",),
            "prerequisites": (),
            "estimated_workload_hours": 10.0,
        }
        self._previews[version_id] = payload
        ver["publication_state"] = "preview_ready"
        return dict(payload)

    def approve(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        del actor_id, occurred_at, reason
        ver = self._require_version(version_id)
        self.approve_calls.append(version_id)
        ver["publication_state"] = "approved"
        ver["status"] = "approved"
        return dict(ver)

    def reject(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        del actor_id, occurred_at, reason
        ver = self._require_version(version_id)
        ver["publication_state"] = "preview_ready"
        ver["status"] = "preview_ready"
        return dict(ver)

    def publication_state(self, version_id: str) -> str | None:
        ver = self._versions.get(version_id)
        if ver is None:
            return None
        return str(ver.get("publication_state") or ver.get("status") or "draft")

    def publish(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        del actor_id
        ver = self._require_version(version_id)
        self.publish_calls.append(version_id)
        ver["publication_state"] = "published"
        ver["status"] = "published"
        ver["published_at"] = occurred_at or "published"
        ver["rollback_snapshot_id"] = ver.get("rollback_snapshot_id") or (
            f"rb-{version_id}"
        )
        ver["rollback_eligible"] = True
        code = ver["subject_code"]
        if code in self._subjects:
            self._subjects[code]["active_version_id"] = version_id
            self._subjects[code]["publication_state"] = "published"
        return {
            "version_id": version_id,
            "publication_state": "published",
            "status": "published",
        }

    def archive(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        del actor_id
        ver = self._require_version(version_id)
        self.archive_calls.append(version_id)
        ver["publication_state"] = "archived"
        ver["status"] = "archived"
        ver["archived_at"] = occurred_at or "archived"
        return dict(ver)

    def _require_version(self, version_id: str) -> dict[str, Any]:
        ver = self._versions.get(version_id)
        if ver is None:
            raise KeyError(version_id)
        return ver


class FakeIngestionPort:
    """Stateful test double for CurriculumIngestionPort."""

    def __init__(self, *, available: bool = True) -> None:
        self._available = available
        self._jobs: dict[str, dict[str, Any]] = {}
        self._seq = 0
        self.start_calls: list[str] = []

    @property
    def component_id(self) -> str:
        return "curriculum_ingestion"

    @property
    def component_version(self) -> str:
        return "test-1"

    def is_available(self) -> bool:
        return self._available

    def start_ingestion(
        self,
        *,
        subject_code: str,
        sources: tuple[dict[str, Any], ...] | list[dict[str, Any]],
        job_id: str | None = None,
    ) -> dict[str, Any]:
        self._seq += 1
        jid = job_id or f"job-{self._seq}"
        self.start_calls.append(jid)
        summary = {
            "job_id": jid,
            "subject_code": subject_code.upper(),
            "state": "completed",
            "sources": list(sources),
        }
        self._jobs[jid] = summary
        return dict(summary)

    def get_ingestion_summary(self, job_id: str) -> dict[str, Any] | None:
        item = self._jobs.get(job_id)
        return None if item is None else dict(item)

    def normalised_structure(self, job_id: str) -> dict[str, Any] | None:
        job = self._jobs.get(job_id)
        if job is None and not job_id:
            return None
        subject = (job or {}).get("subject_code", "CS1")
        # Distinct topics per job for diff tests
        topic_title = "A" if job_id.endswith("1") or "1" in job_id else "B"
        return {
            "curriculum_id": job_id or "unknown",
            "subject_code": subject,
            "topics": [
                {
                    "topic_id": "topic-1",
                    "title": topic_title,
                    "section_id": "sec-1",
                    "objectives": ("obj-1",),
                    "prerequisites": (),
                }
            ],
        }

    def get_validation_report(self, job_id: str) -> dict[str, Any] | None:
        if job_id not in self._jobs and not job_id.startswith("job-"):
            return None
        return {
            "job_id": job_id,
            "passed": True,
            "readiness": "passed",
            "errors": (),
            "warnings": (),
        }


class FakePlatformPort:
    """Test double for EducationPlatformPort."""

    def __init__(self, *, available: bool = True) -> None:
        self._available = available
        self.surface_calls: list[tuple[str, str | None]] = []

    @property
    def component_id(self) -> str:
        return "education_platform"

    @property
    def component_version(self) -> str:
        return "test-1"

    def health(self) -> dict[str, Any]:
        return {"status": "ok" if self._available else "down"}

    def is_available(self) -> bool:
        return self._available

    def student_surface(
        self,
        *,
        subject_code: str,
        version_id: str | None = None,
    ) -> dict[str, Any] | None:
        self.surface_calls.append((subject_code, version_id))
        return {
            "subject_code": subject_code,
            "version_id": version_id,
            "topic_ids": ("topic-1",),
        }


def make_studio(**port_kwargs) -> CurriculumStudioService:
    return CurriculumStudioService.create(**port_kwargs)


def make_studio_with_ports(
    *,
    management: FakeManagementPort | None = None,
    ingestion: FakeIngestionPort | None = None,
    platform: FakePlatformPort | None = None,
) -> tuple[
    CurriculumStudioService,
    FakeManagementPort,
    FakeIngestionPort,
    FakePlatformPort,
]:
    management = management or FakeManagementPort()
    ingestion = ingestion or FakeIngestionPort()
    platform = platform or FakePlatformPort()
    studio = make_studio(
        curriculum_management=management,
        curriculum_ingestion=ingestion,
        education_platform=platform,
    )
    return studio, management, ingestion, platform


def make_ready_facts() -> WorkspacePublicationFacts:
    return WorkspacePublicationFacts.create(
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
        preview_approved=True,
        version_assigned=True,
        rollback_snapshot_created=True,
    )


def seed_workspace(
    studio: CurriculumStudioService | None = None,
    *,
    workspace_id: str = "ws-1",
    subject_code: str = "CS1",
    ready: bool = False,
    with_ports: bool = False,
) -> CurriculumStudioService:
    if studio is None:
        if with_ports:
            studio, _, _, _ = make_studio_with_ports()
        else:
            studio = make_studio()
    facts = make_ready_facts() if ready else None
    studio.create_workspace(
        workspace_id,
        subject_code,
        subject_title="Core Statistics",
        section_ids=("sec-1",),
        topic_ids=("topic-1",),
        objective_ids=("obj-1",),
        facts=facts,
    )
    return studio


def seed_publishable(
    studio: CurriculumStudioService | None = None,
    *,
    workspace_id: str = "ws-1",
) -> CurriculumStudioService:
    """Workspace with ready facts, assigned version, and rollback snapshot."""
    if studio is None:
        studio, _, _, _ = make_studio_with_ports()
    elif studio._ports.get("curriculum_management") is None:  # noqa: SLF001
        # Re-wire is hard; require caller to pass port-backed studio
        studio, _, _, _ = make_studio_with_ports()
        return seed_publishable(studio, workspace_id=workspace_id)
    studio = seed_workspace(studio, workspace_id=workspace_id, ready=True)
    studio.versions.assign_version(workspace_id, "2026.1", version_id="ver-1")
    studio.versions.create_rollback_snapshot("ver-1")
    studio.publication.update_facts(
        workspace_id,
        cmp_uploaded=True,
        official_syllabus_uploaded=True,
        validation_passed=True,
        blueprint_assigned=True,
        preview_approved=True,
        version_assigned=True,
        rollback_snapshot_created=True,
    )
    return studio
