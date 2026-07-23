"""Domain isolation — orchestrator must not couple domain contexts together.

Bounded contexts remain independent. Only the application orchestrator may
compose them. Domain packages must not import application.education.orchestration.
"""

from __future__ import annotations

import ast
from pathlib import Path

DOMAIN_EDUCATION = (
    Path(__file__).resolve().parents[4] / "src" / "domain" / "education"
)

BOUNDED_CONTEXTS = (
    "student_state",
    "educational_evidence",
    "knowledge_graph",
    "mastery_estimation",
    "recommendation_engine",
)

FORBIDDEN_APPLICATION_PREFIXES = (
    "application.education.orchestration",
    "application.education",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def test_domain_contexts_do_not_import_orchestration() -> None:
    violations: list[str] = []
    for context in BOUNDED_CONTEXTS:
        root = DOMAIN_EDUCATION / context
        assert root.is_dir(), f"missing domain context {context}"
        for path in root.rglob("*.py"):
            for module in _imported_modules(path):
                if module.startswith(FORBIDDEN_APPLICATION_PREFIXES):
                    violations.append(f"{path}: imports {module}")
    assert violations == []


def test_peer_contexts_remain_uncoupled_except_engine_reads() -> None:
    """student_state / educational_evidence / knowledge_graph stay isolated.

    Mastery and recommendation engines may read the three input contexts —
    that is their purpose — but the three input contexts must not import
    each other or the engines.
    """
    isolated = ("student_state", "educational_evidence", "knowledge_graph")
    forbidden_for_isolated = {
        "domain.education.student_state",
        "domain.education.educational_evidence",
        "domain.education.knowledge_graph",
        "domain.education.mastery_estimation",
        "domain.education.recommendation_engine",
        "application.education.orchestration",
    }
    violations: list[str] = []
    for context in isolated:
        root = DOMAIN_EDUCATION / context
        own_prefix = f"domain.education.{context}"
        for path in root.rglob("*.py"):
            for module in _imported_modules(path):
                if module == own_prefix or module.startswith(own_prefix + "."):
                    continue
                if module.startswith("domain.education.foundation"):
                    continue
                for forbidden in forbidden_for_isolated:
                    if module == forbidden or module.startswith(forbidden + "."):
                        # own package already skipped
                        if forbidden == own_prefix:
                            continue
                        violations.append(
                            f"{context}/{path.name}: imports {module}"
                        )
    assert violations == []
