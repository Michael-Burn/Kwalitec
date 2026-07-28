"""Authority and architecture purity checks for AP-002D7 certification."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]

# Single Authority Rule — each stage root and what it must never import.
AUTHORITY_MATRIX: dict[str, tuple[Path, tuple[str, ...]]] = {
    "assessment_packaging": (
        REPO_ROOT / "src" / "domain" / "assessment" / "packaging",
        (
            "student_digital_twin",
            "TwinUpdater",
            "DecisionGenerator",
            "MissionPlanningService",
            "TutorExplanationService",
        ),
    ),
    "evidence_ingress": (
        REPO_ROOT / "app" / "application" / "assessment_pipeline" / "evidence_ingress",
        (
            "DecisionGenerator",
            "TwinUpdater",
            "MissionPlanningService",
            "TutorExplanationService",
            "TwinProjectionService",
        ),
    ),
    "interpretation": (
        REPO_ROOT / "app" / "application" / "reasoning" / "interpretation",
        (
            "TwinUpdater",
            "DecisionGenerator",
            "MissionPlanningService",
            "TutorExplanationService",
            "TwinProjectionService",
        ),
    ),
    "decisions": (
        REPO_ROOT / "app" / "application" / "reasoning" / "decisions",
        (
            "MissionPlanningService",
            "TutorExplanationService",
            "TwinProjectionService",
            "EvidencePackagingService",
        ),
    ),
    "projection": (
        REPO_ROOT / "app" / "application" / "learning_graph" / "projections",
        (
            "DecisionGenerator",
            "TwinUpdater",
            "MissionPlanningService",
            "TutorExplanationService",
            "StudentReasoningService",
        ),
    ),
    "planning": (
        REPO_ROOT / "app" / "application" / "mission_engine" / "planning",
        (
            "DecisionGenerator",
            "TwinUpdater",
            "TutorExplanationService",
            "EvidenceInterpreter",
            "StudentReasoningService",
        ),
    ),
    "explanation": (
        REPO_ROOT / "app" / "application" / "intelligent_tutor" / "explainability",
        (
            "DecisionGenerator",
            "TwinUpdater",
            "CandidateBuilder",
            "EvidenceInterpreter",
            "StudentReasoningService",
        ),
    ),
}

# Dependency direction: later stages may consume earlier artefacts, never reverse.
FORBIDDEN_CROSS_STAGE_IMPORTS: tuple[tuple[str, str, str], ...] = (
    (
        "app/application/reasoning/interpretation",
        "mission_engine.planning",
        "Interpretation must not plan missions",
    ),
    (
        "app/application/reasoning/interpretation",
        "intelligent_tutor.explainability",
        "Interpretation must not explain",
    ),
    (
        "app/application/reasoning/decisions",
        "mission_engine.planning",
        "Decision generation must not plan missions",
    ),
    (
        "app/application/reasoning/decisions",
        "intelligent_tutor.explainability",
        "Decision generation must not explain",
    ),
    (
        "app/application/learning_graph/projections",
        "mission_engine.planning",
        "Projection must not plan missions",
    ),
    (
        "app/application/learning_graph/projections",
        "intelligent_tutor.explainability",
        "Projection must not explain",
    ),
    (
        "app/application/mission_engine/planning",
        "intelligent_tutor.explainability",
        "Mission planning must not explain",
    ),
    (
        "app/application/mission_engine/planning",
        "reasoning.decisions.decision_generator",
        "Mission planning must not generate decisions",
    ),
    (
        "app/application/intelligent_tutor/explainability",
        "reasoning.decisions.decision_generator",
        "Tutor explanation must not generate decisions",
    ),
    (
        "app/application/intelligent_tutor/explainability",
        "mission_engine.planning.candidate_builder",
        "Tutor explanation must not build mission candidates",
    ),
)


@dataclass(frozen=True, slots=True)
class AuthorityFinding:
    stage: str
    path: str
    detail: str


def _iter_python_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(p for p in root.rglob("*.py") if p.is_file())


def _module_text_and_imports(path: Path) -> tuple[str, set[str]]:
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return text, names


def audit_authority_matrix() -> list[AuthorityFinding]:
    """Return authority violations (empty when certified)."""
    findings: list[AuthorityFinding] = []
    for stage, (root, forbidden) in AUTHORITY_MATRIX.items():
        for path in _iter_python_files(root):
            text, imports = _module_text_and_imports(path)
            for token in forbidden:
                if token in text or any(token in name for name in imports):
                    # Allow mentions inside comments/docstrings only when not imported
                    # and not used as an identifier import — still fail closed on text.
                    if token in text:
                        findings.append(
                            AuthorityFinding(
                                stage=stage,
                                path=str(path.relative_to(REPO_ROOT)),
                                detail=f"forbidden authority token {token!r}",
                            )
                        )
    return findings


def audit_dependency_direction() -> list[AuthorityFinding]:
    """Return dependency-direction violations (empty when certified)."""
    findings: list[AuthorityFinding] = []
    for relative_root, forbidden_substr, reason in FORBIDDEN_CROSS_STAGE_IMPORTS:
        root = REPO_ROOT / relative_root
        for path in _iter_python_files(root):
            _text, imports = _module_text_and_imports(path)
            if any(forbidden_substr in name for name in imports):
                findings.append(
                    AuthorityFinding(
                        stage=relative_root,
                        path=str(path.relative_to(REPO_ROOT)),
                        detail=reason,
                    )
                )
    return findings


def audit_student_reasoning_stop_boundaries() -> list[AuthorityFinding]:
    """Confirm StudentReasoningService does not auto-invoke D4/D5/D6."""
    path = (
        REPO_ROOT
        / "app"
        / "application"
        / "student_digital_twin"
        / "student_reasoning_service.py"
    )
    text, imports = _module_text_and_imports(path)
    findings: list[AuthorityFinding] = []
    forbidden = (
        "MissionPlanningService",
        "TutorExplanationService",
        "TwinProjectionService",
        "plan_from_decisions",
        "explain_from_decisions",
        "project_twin_decisions",
    )
    for token in forbidden:
        if token in text or any(token in name for name in imports):
            findings.append(
                AuthorityFinding(
                    stage="student_reasoning_service",
                    path=str(path.relative_to(REPO_ROOT)),
                    detail=f"STOP boundary breached: {token}",
                )
            )
    return findings
