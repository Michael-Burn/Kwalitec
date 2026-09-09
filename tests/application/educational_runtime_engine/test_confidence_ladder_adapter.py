"""Domain H confidence → Spacing ladder nudge (roadmap item 5).

Proves the locked three-way mapping, sole-bridge discipline, Domain H
non-consumer constraints, and end-to-end durability of the nudged state.
"""

from __future__ import annotations

import ast
from datetime import date, timedelta
from pathlib import Path

import pytest

from app.application.educational_runtime_engine import EducationalRuntimeEngineService
from app.application.educational_runtime_engine.confidence_ladder_adapter import (
    confidence_rating_to_ladder_step_delta,
    ladder_step_delta_for_completed_sitting,
    load_sitting_confidence_rating,
)
from app.application.spacing_scheduler import (
    discard_canonical_spacing_scheduler_for_tests,
    get_spacing_scheduler,
)
from app.infrastructure.adapters.learning_session.persistence import (
    NS_HANDLE,
    NS_MISSION,
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.composition import (
    build_production_session_experience,
)
from tests.application.educational_runtime_engine import (
    test_due_review_daily_composer as _due_review,
)
from tests.application.educational_runtime_engine.helpers import (
    make_user,
    publish_subject,
)

PACKAGE_DUE = _due_review.PACKAGE_DUE
PACKAGE_SEQ = _due_review.PACKAGE_SEQ
_Pack = _due_review._Pack
_patch_packages = _due_review._patch_packages

ADAPTER_PATH = Path(
    "app/application/educational_runtime_engine/confidence_ladder_adapter.py"
)
ERE_SERVICE_PATH = Path(
    "app/application/educational_runtime_engine/service.py"
)
SCHEDULER_ROOTS = [
    Path("app/domain/spacing_scheduler"),
    Path("app/application/spacing_scheduler"),
]


@pytest.mark.parametrize(
    ("rating", "expected_delta"),
    [
        (None, 0),
        (1, -1),
        (2, -1),
        (3, 0),
        (4, 1),
        (5, 1),
        (0, 0),
        (6, 0),
        ("x", 0),
    ],
)
def test_locked_confidence_to_ladder_delta_table(
    rating: object, expected_delta: int
) -> None:
    assert confidence_rating_to_ladder_step_delta(rating) == expected_delta  # type: ignore[arg-type]


def test_adapter_is_sole_confidence_to_scheduling_bridge() -> None:
    """Only the named adapter may connect confidence_rating to a ladder delta."""
    bridge_markers = (
        "confidence_rating_to_ladder_step_delta",
        "ladder_step_delta_for_completed_sitting",
    )
    hits: list[str] = []
    for root in (
        Path("app/application"),
        Path("app/domain"),
        Path("app/services"),
        Path("app/presentation"),
        Path("app/infrastructure"),
    ):
        if not root.exists():
            continue
        for path in root.rglob("*.py"):
            if path == ADAPTER_PATH:
                continue
            text = path.read_text(encoding="utf-8")
            # ERE completion path may call the adapter; it must not inline the map.
            if path == ERE_SERVICE_PATH:
                assert "ladder_step_delta_for_completed_sitting" in text
                assert "confidence_rating_to_ladder_step_delta" not in text
                assert "load_sitting_confidence_rating" not in text
                assert 'doc.get("confidence_rating")' not in text
                continue
            if any(marker in text for marker in bridge_markers):
                hits.append(str(path))
            elif "ladder_step_delta" in text and "confidence_rating" in text:
                hits.append(str(path))
    assert hits == [], f"unexpected confidence→scheduling bridges: {hits}"

    adapter_src = ADAPTER_PATH.read_text(encoding="utf-8")
    assert "confidence_rating_to_ladder_step_delta" in adapter_src
    assert "ladder_step_delta" in adapter_src

    # Scheduler packages must never mention Domain H confidence_rating.
    for root in SCHEDULER_ROOTS:
        for path in root.rglob("*.py"):
            text = path.read_text(encoding="utf-8")
            assert "confidence_rating" not in text, path
            if path.name == "types.py":
                assert '"confidence"' in text
                assert "FORBIDDEN_SIGNAL_NAMES" in text


def test_domain_h_intelligence_cores_still_never_consume_confidence() -> None:
    """Twin / Decision / mastery / recommendations still do not read Domain H."""
    banned_roots = [
        Path("app/application/student_twin"),
        Path("app/domain/student_twin"),
        Path("app/application/decision_journal"),
        Path("app/services/decision_journal_service.py"),
        Path("app/services/recommendation_service.py"),
        Path("app/application/learning_strategy"),
        Path("app/application/progress_engine"),
        Path("app/domain/adaptive_decision"),
        Path("app/application/adaptive_decision"),
        Path("app/services/mission_service.py"),
        Path("app/services/readiness_service.py"),
        Path("app/domain/spacing_scheduler"),
        Path("app/application/spacing_scheduler"),
    ]
    session_markers = (
        'updated["confidence_rating"]',
        'opaque.get("confidence_rating")',
        'record.get("confidence_rating")',
        "confidence_rating=confidence_rating",
        'metadata.append(("confidence_rating"',
        "_confidence_calibration",
        "confidence_rating_to_ladder_step_delta",
        "load_sitting_confidence_rating",
    )
    hits: list[str] = []
    for root in banned_roots:
        paths = (
            [root]
            if root.is_file()
            else list(root.rglob("*.py"))
            if root.exists()
            else []
        )
        for path in paths:
            if not path.is_file():
                continue
            text = path.read_text(encoding="utf-8")
            for marker in session_markers:
                if marker in text:
                    hits.append(f"{path}: {marker}")
    assert hits == [], (
        "Domain H session confidence_rating leaked into banned cores: "
        f"{hits}"
    )


def _seed_sitting_confidence(
    *,
    user_id: int,
    mission_instance_id: str,
    confidence_rating: int | None,
) -> str:
    composition, _service = build_production_session_experience(
        seed_demo_learners=False
    )
    adapter = LearningSessionPersistenceAdapter(store=composition.store)
    sid = str(user_id)
    session_id = f"sess-confidence-{sid}-{mission_instance_id}"
    doc = {
        "student_id": sid,
        "session_id": session_id,
        "mission_instance_id": mission_instance_id,
        "status": "completed",
        "topic_title": "Confidence nudge sitting",
    }
    if confidence_rating is not None:
        doc["confidence_rating"] = confidence_rating
    adapter.store.save(NS_HANDLE, session_id, doc)
    adapter.store.save(
        NS_MISSION,
        f"{sid}::{mission_instance_id}",
        {"session_id": session_id},
    )
    return session_id


@pytest.mark.parametrize(
    ("rating", "expected_interval"),
    [
        (None, 1),
        (1, 1),  # shorten from initial 1, clamped at min
        (2, 1),
        (3, 1),
        (4, 3),  # lengthen one ladder step
        (5, 3),
    ],
)
def test_complete_mission_applies_confidence_ladder_nudge_end_to_end(
    ctx,
    monkeypatch,
    rating: int | None,
    expected_interval: int,
) -> None:
    """Real MISSION_COMPLETED + Domain H rating → durable nudged spacing state."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    discard_canonical_spacing_scheduler_for_tests()

    user = make_user(f"conf-nudge-{rating}@example.com")
    subject = publish_subject(f"CNF{rating if rating is not None else 'X'}")
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=user.id, subject_code=subject)

    seq = _Pack(package_id=PACKAGE_SEQ, subject_id=subject, display_title="Seq")
    due = _Pack(package_id=PACKAGE_DUE, subject_id=subject, display_title="Due")
    _patch_packages(monkeypatch, subject=subject, sequential=seq, due=due)

    day = date(2026, 9, 1)
    mission = runtime.generate_daily_mission(
        user_id=user.id,
        subject_code=subject,
        mission_date=day,
    )
    _seed_sitting_confidence(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
        confidence_rating=rating,
    )
    assert (
        load_sitting_confidence_rating(
            user_id=user.id,
            mission_instance_id=mission.mission_instance_id,
        )
        == rating
    )
    assert (
        ladder_step_delta_for_completed_sitting(
            user_id=user.id,
            mission_instance_id=mission.mission_instance_id,
        )
        == confidence_rating_to_ladder_step_delta(rating)
    )

    runtime.complete_mission(
        user_id=user.id,
        mission_instance_id=mission.mission_instance_id,
    )

    scheduler = get_spacing_scheduler()
    state = scheduler.get_state(learner_id=str(user.id), package_id=PACKAGE_SEQ)
    assert state is not None
    assert state.current_interval_days == expected_interval
    assert state.next_due_on == day + timedelta(days=expected_interval)
    assert state.last_completed_on == day

    # Same durable-store round trip proven in item 4.
    discard_canonical_spacing_scheduler_for_tests()
    restored = get_spacing_scheduler().get_state(
        learner_id=str(user.id), package_id=PACKAGE_SEQ
    )
    assert restored is not None
    assert restored.current_interval_days == expected_interval
    assert restored.next_due_on == day + timedelta(days=expected_interval)


def test_adapter_module_has_no_scheduler_forbidden_imports() -> None:
    """Adapter may call the facade; it must not teach the scheduler confidence."""
    tree = ast.parse(ADAPTER_PATH.read_text(encoding="utf-8"))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                imported.add(alias.name)
    assert not any(
        name.startswith("app.domain.spacing_scheduler") for name in imported
    )
    src = ADAPTER_PATH.read_text(encoding="utf-8")
    assert "FORBIDDEN_SIGNAL_NAMES" not in src
    assert "reject_forbidden_kwargs" not in src
