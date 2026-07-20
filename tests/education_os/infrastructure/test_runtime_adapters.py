"""INF-006 runtime adapter tests (clock, UUIDs, event publisher)."""

from __future__ import annotations

import ast
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

from application.events.base import ApplicationEvent
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.uuid_generator import UUIDGenerator
from infrastructure.runtime import (
    SynchronousApplicationEventPublisher,
    SystemClock,
    SystemUUIDGenerator,
)


def test_clock_correctness() -> None:
    clock: Clock = SystemClock()
    now = clock.now()

    assert isinstance(now, datetime)
    assert now.tzinfo is UTC


def test_uuid_uniqueness() -> None:
    generator: UUIDGenerator = SystemUUIDGenerator()
    ids = [generator.new_id() for _ in range(200)]

    assert len(set(ids)) == len(ids)
    for raw in ids:
        parsed = UUID(raw)
        assert parsed.version == 4


def test_publisher_interface_compliance() -> None:
    published: list[tuple[str, ApplicationEvent]] = []
    event = ApplicationEvent(
        occurred_at=datetime(2026, 7, 20, 12, 0, tzinfo=UTC),
    )

    def first_handler(e: ApplicationEvent) -> None:
        published.append(("first", e))

    def second_handler(e: ApplicationEvent) -> None:
        published.append(("second", e))

    publisher: ApplicationEventPublisher = SynchronousApplicationEventPublisher(
        handlers=(first_handler, second_handler)
    )
    publisher.publish(event)

    assert published == [("first", event), ("second", event)]


PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3] / "src" / "infrastructure" / "runtime"
)

FORBIDDEN_MODULES = frozenset(
    {
        "flask",
        "sqlalchemy",
        "alembic",
        "jinja2",
        "wtforms",
        "requests",
        "httpx",
        "celery",
        "redis",
        "boto3",
        "pydantic",
        "marshmallow",
    }
)

FORBIDDEN_PREFIXES = (
    "flask.",
    "sqlalchemy.",
    "app.",
    "app.models",
    "app.services",
    "app.domain",
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "diagnose",
        "calculate_mastery",
        "prioritise",
        "prioritize",
        "choose_strategy",
        "select_strategy",
        "interpret_evidence",
        "create_hypothesis",
    }
)


def _iter_python_files() -> list[Path]:
    return sorted(PACKAGE_ROOT.rglob("*.py"))


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


def _defined_methods(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            names.add(node.name)
    return names


def test_architecture_purity() -> None:
    expected_layout = {
        PACKAGE_ROOT / "__init__.py",
        PACKAGE_ROOT / "clock.py",
        PACKAGE_ROOT / "uuid_generator.py",
        PACKAGE_ROOT / "event_publisher.py",
    }
    assert PACKAGE_ROOT.is_dir()
    for path in expected_layout:
        assert path.is_file(), f"missing {path.relative_to(PACKAGE_ROOT)}"

    for path in _iter_python_files():
        imported = _imported_modules(path)
        for name in imported:
            assert name not in FORBIDDEN_MODULES, f"{path.name} imports {name}"
            assert not any(
                name == prefix.rstrip(".") or name.startswith(prefix)
                for prefix in FORBIDDEN_PREFIXES
            ), f"{path.name} imports forbidden module {name}"

        source = path.read_text(encoding="utf-8").lower()
        for fragment in (
            "pickle",
            "sqlite",
            "psycopg",
            "pymongo",
            "dto",
            "repository",
            "serializer",
        ):
            assert fragment not in source, f"{path.name} contains {fragment}"

        methods = _defined_methods(path)
        for forbidden in FORBIDDEN_METHOD_NAMES:
            assert forbidden not in methods, f"{path.name} defines {forbidden}"

        content = path.read_text(encoding="utf-8")
        if content.strip():
            assert "from __future__ import annotations" in content

