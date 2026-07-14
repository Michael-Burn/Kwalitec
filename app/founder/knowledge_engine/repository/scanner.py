"""Filesystem scanner for the Knowledge Engine (FOS-001).

Internal to the subsystem — never export Paths outside this package.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from app.founder.knowledge_engine.classifiers import classify_relative_path
from app.founder.knowledge_engine.config import KnowledgeEngineConfig
from app.founder.knowledge_engine.dto.artefact import KnowledgeArtefactDTO
from app.founder.knowledge_engine.dto.validation import KnowledgeValidationIssue

_DOCUMENT_ID_RE = re.compile(
    r"^\*\*Document ID:\*\*\s*(?P<id>.+?)\s*$",
    re.MULTILINE,
)
_TITLE_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class ScanResult:
    """Internal scan payload (artefacts + issues)."""

    artefacts: tuple[KnowledgeArtefactDTO, ...]
    issues: tuple[KnowledgeValidationIssue, ...]
    missing_roots: tuple[str, ...]


class KnowledgeRepositoryScanner:
    """Discover indexable markdown artefacts under configured roots."""

    def __init__(
        self,
        *,
        repo_root: Path,
        config: KnowledgeEngineConfig,
    ) -> None:
        self._root = repo_root.resolve()
        self._config = config

    def scan(self) -> ScanResult:
        """Walk configured roots and return structured artefacts."""
        artefacts: list[KnowledgeArtefactDTO] = []
        issues: list[KnowledgeValidationIssue] = []
        missing_roots: list[str] = []
        seen_ids: dict[str, str] = {}

        for root_name in self._config.scan_roots:
            root_path = self._root / root_name
            if not root_path.is_dir():
                missing_roots.append(root_name)
                issues.append(
                    KnowledgeValidationIssue(
                        code="missing_root",
                        message=f"Configured scan root is missing: {root_name}",
                    )
                )
                continue

            for path in self._iter_markdown(root_path):
                try:
                    relative = path.relative_to(self._root)
                except ValueError:
                    issues.append(
                        KnowledgeValidationIssue(
                            code="path_escape",
                            message="Indexed file escaped repository root.",
                        )
                    )
                    continue

                try:
                    text = path.read_text(encoding="utf-8")
                except OSError as exc:
                    issues.append(
                        KnowledgeValidationIssue(
                            code="unreadable_file",
                            message=(
                                "Unable to read artefact: "
                                f"{exc.__class__.__name__}"
                            ),
                            artefact_id=path.stem,
                        )
                    )
                    continue

                artefact = self._to_artefact(relative, text)
                prior = seen_ids.get(artefact.artefact_id)
                if prior is not None:
                    issues.append(
                        KnowledgeValidationIssue(
                            code="duplicate_artefact_id",
                            message=(
                                f"Duplicate artefact id '{artefact.artefact_id}'."
                            ),
                            artefact_id=artefact.artefact_id,
                        )
                    )
                seen_ids[artefact.artefact_id] = artefact.collection
                artefacts.append(artefact)

        artefacts.sort(key=lambda a: (a.collection, a.artefact_id))
        return ScanResult(
            artefacts=tuple(artefacts),
            issues=tuple(issues),
            missing_roots=tuple(missing_roots),
        )

    def _iter_markdown(self, root: Path):
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            if any(part in self._config.skip_dir_names for part in path.parts):
                continue
            if path.suffix.lower() not in self._config.indexable_suffixes:
                continue
            if path.stem.lower() == "readme":
                continue
            yield path

    def _to_artefact(self, relative: Path, text: str) -> KnowledgeArtefactDTO:
        collection = classify_relative_path(relative)
        document_id = _extract_document_id(text)
        # Logical id only — never a filesystem path. Namespace by collection
        # when Document ID is absent so README stems do not falsely collide.
        artefact_id = document_id or f"{collection}:{relative.stem}"
        title = _extract_title(text) or relative.stem.replace("_", " ")
        return KnowledgeArtefactDTO(
            artefact_id=artefact_id,
            title=title,
            collection=collection,
            document_id=document_id,
        )


def _extract_document_id(text: str) -> str:
    match = _DOCUMENT_ID_RE.search(text)
    if match:
        return match.group("id").strip()
    return ""


def _extract_title(text: str) -> str:
    match = _TITLE_RE.search(text)
    if match:
        return match.group(1).strip()
    return ""
