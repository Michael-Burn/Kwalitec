"""Domain H.1 / H.2 — confidence prompt wiring, rating capture, calibration.

Display-only. Does not feed Twin, Decision, mastery, or recommendation paths.
"""

from __future__ import annotations

import ast
from pathlib import Path

from app.application.educational_authoring.dto import AuthoringContext
from app.application.educational_packages.composition_overlay import (
    compose_from_package,
)
from app.application.educational_packages.loader import find_package_by_id
from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.session_experience.dto.reflection_snapshot import (
    ReflectionSnapshot,
)
from app.domain.session_experience.session_workspace import SessionSurface
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.session.forms import ContinueReflectionForm
from app.presentation.session.sitting_report import build_sitting_report
from app.presentation.session.view_models import ReflectionViewModel, reflection_vm
from tests.presentation.session.helpers import wire_session_experience


def _sample_package():
    pack = find_package_by_id("1.2.1-eda-summaries-ep001")
    if pack is None:
        # Fall back to any approved package with a confidence_prompt.
        from app.application.educational_packages.loader import (
            EducationalPackageLoader,
        )

        for candidate in EducationalPackageLoader().all_approved():
            if (candidate.confidence_prompt or "").strip():
                return candidate
        raise AssertionError("No package with confidence_prompt found")
    return pack


class TestH1ConfidencePromptWiring:
    def test_compose_from_package_copies_confidence_prompt(self):
        pack = _sample_package()
        assert pack.confidence_prompt.strip()
        composition = compose_from_package(
            pack,
            AuthoringContext(
                topic_id=pack.topic_code,
                topic_title=pack.topic_title,
                topic_code=pack.topic_code,
                subject_code=pack.subject_id,
                educational_package_id=pack.package_id,
            ),
        )
        assert composition.confidence_prompt == pack.confidence_prompt.strip()
        opaque = composition.to_opaque()
        assert opaque["confidence_prompt"] == pack.confidence_prompt.strip()

    def test_reflection_snapshot_exposes_package_confidence_prompt(self):
        pack = _sample_package()
        snap = ReflectionSnapshot(
            session_id="sess-h1",
            reflection_prompt=pack.reflection_prompt or "Reflect",
            confidence_prompt=pack.confidence_prompt,
            topic_title=pack.topic_title,
        )
        vm = reflection_vm(snap)
        assert isinstance(vm, ReflectionViewModel)
        assert vm.confidence_prompt == pack.confidence_prompt
        lowered = vm.confidence_prompt.lower()
        assert "Rate" in vm.confidence_prompt or "confident" in lowered

    def test_reflection_template_renders_confidence_block(self):
        body = Path("app/templates/session/partials/session_body.html").read_text(
            encoding="utf-8"
        )
        assert "s.confidence_prompt" in body
        assert 'data-confidence-rating="true"' in body
        assert "form.confidence_rating" in body
        assert "ds-session-finish-review__option" in body


class TestH1ConfidenceRatingPersistence:
    def test_form_resolves_1_to_5_rating(self, session_app):
        with session_app.app_context():
            form = ContinueReflectionForm(
                data={
                    "session_id": "sess-1",
                    "confidence_rating": "4",
                    "csrf_token": "unused",
                },
                meta={"csrf": False},
            )
            assert form.resolved_confidence_rating() == 4
            empty = ContinueReflectionForm(
                data={"session_id": "sess-1", "csrf_token": "unused"},
                meta={"csrf": False},
            )
            assert empty.resolved_confidence_rating() is None

    def test_save_reflection_note_persists_confidence_rating(self):
        store = SessionDocumentStore()
        persistence = LearningSessionPersistenceAdapter(store=store)
        session_id = "sess-confidence-1"
        store.save(
            "lsr.handle",
            session_id,
            {"student_id": "stu-1", "session_id": session_id, "topic_title": "EDA"},
        )
        updated = persistence.save_reflection_note(
            session_id=session_id,
            note="Stickiest cue was the summary choice.",
            student_id="stu-1",
            confidence_rating=5,
        )
        assert updated is not None
        assert updated["confidence_rating"] == 5
        assert updated["reflection_note"].startswith("Stickiest")
        reloaded = persistence.load(session_id=session_id)
        assert reloaded is not None
        assert reloaded["confidence_rating"] == 5

    def test_reflection_continue_route_persists_rating(
        self, session_client, session_app
    ):
        svc = wire_session_experience(session_app)
        svc.open_session("1", session_id="sess-1")
        ws = svc.registry.get_workspace_for_session("sess-1")
        assert ws is not None
        svc.registry.put_workspace(ws.navigate_to(SessionSurface.REFLECTION))
        session_client.get("/session/sess-1/reflection")
        cont = session_client.post(
            "/session/sess-1/reflection/continue",
            data={
                "session_id": "sess-1",
                "reflection_note": "I still find deferred tax tricky.",
                "confidence_rating": "2",
                "submit": "Continue to Summary",
            },
            follow_redirects=False,
        )
        assert cont.status_code in {302, 303}
        runtime_port = svc.reflection._runtime
        assert runtime_port.reflection_note_calls == [
            ("1", "sess-1", "I still find deferred tax tricky.", 2)
        ]


class TestH2ConfidenceCalibration:
    def test_high_rating_with_missed_checks(self):
        report = build_sitting_report(
            topic_title="Present value",
            opaque_summary={
                "confidence_rating": 5,
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                ],
                "substance": "package",
            },
        )
        assert report.confidence_calibration
        assert "felt ready" in report.confidence_calibration.lower()
        assert "different story" in report.confidence_calibration.lower()
        assert "—" not in report.confidence_calibration
        assert "exam ready" not in report.confidence_calibration.lower()

    def test_low_rating_with_mostly_correct_checks(self):
        report = build_sitting_report(
            topic_title="Discount factors",
            opaque_summary={
                "confidence_rating": 1,
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                ],
                "substance": "package",
            },
        )
        assert report.confidence_calibration
        assert "weren't sure" in report.confidence_calibration.lower()
        assert "checks went well" in report.confidence_calibration.lower()
        assert "—" not in report.confidence_calibration

    def test_skipped_when_no_scored_practice(self):
        report = build_sitting_report(
            topic_title="Equity method",
            opaque_summary={
                "confidence_rating": 5,
                "observations": [
                    {"type_id": RuntimeEvidenceType.READING_COMPLETED.value},
                    {"type_id": RuntimeEvidenceType.REFLECTION_SUBMITTED.value},
                ],
                "substance": "package",
            },
        )
        assert report.confidence_calibration == ""

    def test_aligned_high_and_all_correct_skips(self):
        report = build_sitting_report(
            topic_title="Cash flows",
            opaque_summary={
                "confidence_rating": 4,
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                ],
                "substance": "package",
            },
        )
        assert report.confidence_calibration == ""

    def test_complete_template_exposes_calibration_hook(self):
        body = Path("app/templates/session/partials/session_body.html").read_text(
            encoding="utf-8"
        )
        assert "s.confidence_calibration" in body
        assert 'data-confidence-calibration="true"' in body


class TestH1H2NoIntelligenceConsumers:
    """Confirm Twin / Decision / mastery / recommendation do not read the
    session-handle Domain H confidence_rating (1-5 reflection capture).

    Twin already owns an unrelated EvidenceEvent.confidence_rating (0-1 float)
    under evidence_type CONFIDENCE_RATING — that pre-existing field is not
    this Domain H session rating and must not be confused with it.
    """

    _ALLOWED_READERS = {
        Path("app/presentation/session/sitting_report.py"),
        Path("app/presentation/session/view_models.py"),
        Path("app/presentation/session/forms.py"),
        Path("app/presentation/session/routes.py"),
        Path("app/presentation/session/views.py"),
        Path("app/presentation/session/services/study_session_service.py"),
        Path("app/presentation/session/dto/study_session.py"),
        Path("app/application/session_experience/reflection_service.py"),
        Path("app/application/session_experience/facade.py"),
        Path("app/application/session_experience/ports/session_runtime_port.py"),
        Path("app/application/session_experience/completion_service.py"),
        Path("app/infrastructure/session/runtime_adapter.py"),
        Path("app/infrastructure/adapters/learning_session/runtime_engine.py"),
        Path("app/infrastructure/adapters/learning_session/persistence.py"),
        Path("app/infrastructure/session/defaults.py"),
    }

    def test_session_confidence_rating_stays_out_of_intelligence_cores(self):
        """No Twin/Decision/mastery/recommendation module reads handle rating."""
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
        ]
        # Session-handle Domain H writes use these exact persistence keys /
        # call sites. Twin's EvidenceEvent field is a different identifier.
        session_markers = (
            'updated["confidence_rating"]',
            'opaque.get("confidence_rating")',
            'record.get("confidence_rating")',
            "confidence_rating=confidence_rating",
            'metadata.append(("confidence_rating"',
            "_confidence_calibration",
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
            "Domain H session confidence_rating leaked into intelligence "
            f"cores: {hits}"
        )

    def test_reflection_emit_does_not_pass_rating_to_evidence(self):
        """Engine reflection emit payload must not include confidence_rating."""
        src = Path(
            "app/infrastructure/adapters/learning_session/runtime_engine.py"
        ).read_text(encoding="utf-8")
        start = src.index("def record_reflection_note_opaque")
        end = src.index("\n    def ", start + 1)
        body = src[start:end]
        assert 'payload={"note_length": len(text), "has_note": True}' in body
        # Evidence emit blocks must not ship the Domain H rating into Twin.
        emit_chunks = body.split("_emit_candidate")
        for chunk in emit_chunks[1:]:
            assert "confidence_rating" not in chunk.split(")")[0]

    def test_sitting_report_calibration_is_local_helper(self):
        """Calibration lives only in sitting_report presentation."""
        src = Path("app/presentation/session/sitting_report.py").read_text(
            encoding="utf-8"
        )
        assert "def _confidence_calibration" in src
        tree = ast.parse(src)
        names = {
            node.name
            for node in ast.walk(tree)
            if isinstance(node, ast.FunctionDef)
        }
        assert "_confidence_calibration" in names
