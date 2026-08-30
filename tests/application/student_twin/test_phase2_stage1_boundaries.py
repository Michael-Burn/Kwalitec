"""Phase 2 Stage 1 content-boundary and no-EK-write guards."""

from __future__ import annotations

import ast
from pathlib import Path

# Application Stage 1 modules (framework-independent).
APP_STAGE1_MODULES = (
    "query.py",
    "canonical_topic_id.py",
    "drift_detector.py",
)

# Infrastructure adapter that may import models / persistence, but not content.
INFRA_STAGE1_MODULES = (
    Path("app") / "infrastructure" / "adapters" / "student_twin" / "query_adapter.py",
)

FORBIDDEN_IMPORT_FRAGMENTS = (
    "educational_packages",
    "educational_campaigns",
    "curriculum.data",
    "curriculum/data",
    "app.curriculum.data",
)

FORBIDDEN_WRITE_TOKENS = (
    "replace_inferences",
    "SdtMasteryRecord(",
    "save_twin",
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _app_stage1_dir() -> Path:
    return _repo_root() / "app" / "application" / "student_twin"


def _all_stage1_paths() -> list[Path]:
    paths = [_app_stage1_dir() / name for name in APP_STAGE1_MODULES]
    paths.extend(_repo_root() / rel for rel in INFRA_STAGE1_MODULES)
    return paths


def test_stage1_modules_do_not_import_content_authoring_paths():
    offenders: list[str] = []
    for path in _all_stage1_paths():
        assert path.is_file(), f"missing Stage 1 module {path}"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            modules: list[str] = []
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                modules = [node.module or ""]
            for mod in modules:
                lowered = mod.replace("\\", "/")
                for frag in FORBIDDEN_IMPORT_FRAGMENTS:
                    if frag in lowered:
                        offenders.append(f"{path.name}:{mod}")
    assert offenders == [], offenders


def test_stage1_app_modules_do_not_write_ek_stores():
    offenders: list[str] = []
    for name in APP_STAGE1_MODULES:
        path = _app_stage1_dir() / name
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN_WRITE_TOKENS:
            if token in text:
                if name == "drift_detector.py" and token in (
                    "replace_inferences",
                    "SdtMasteryRecord(",
                ):
                    continue
                offenders.append(f"{path.name}:{token}")
        if ".average_accuracy =" in text:
            offenders.append(f"{path.name}:average_accuracy assignment")
        if ".mastery_score =" in text and name in (
            "query.py",
            "canonical_topic_id.py",
        ):
            offenders.append(f"{path.name}:mastery_score assignment")
    assert offenders == [], offenders


def test_stage1_query_adapter_does_not_call_save_twin():
    path = _repo_root() / INFRA_STAGE1_MODULES[0]
    text = path.read_text(encoding="utf-8")
    assert "save_twin" not in text
    assert ".mastery_score =" not in text
    assert ".average_accuracy =" not in text
