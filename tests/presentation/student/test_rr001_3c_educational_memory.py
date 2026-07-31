"""RR-001.3C — Educational memory & history coherence.

Verifies Decision Journal / Timeline / History distinct roles (EGC-R06),
empty-state tip/QC honesty (EGC-R12), and first-introduction consistency
(NCR-021) without changing recommendation, Mission Intelligence, or
curriculum behaviour.
"""

from __future__ import annotations

from app.application.decision_journal.dto import DecisionJournalTimelineSnapshot
from app.application.educational_timeline.dto import EducationalTimelineSnapshot
from app.presentation.product_language import (
    APPROVED_TERMS,
    EDUCATIONAL_MEMORY_MODEL_SENTENCE,
    HISTORY_EPISTEMOLOGY_BRIDGE,
    REJECTED_SYNONYMS,
)
from app.services.alpha_onboarding_service import (
    SENSEI_HANDOFF_SENTENCE,
    AlphaOnboardingService,
)


def test_educational_memory_model_sentence_distinguishes_surfaces():
    assert "Decision Journal" in EDUCATIONAL_MEMORY_MODEL_SENTENCE
    assert "Educational Timeline" in EDUCATIONAL_MEMORY_MODEL_SENTENCE
    assert "History" in EDUCATIONAL_MEMORY_MODEL_SENTENCE
    assert "not a second memory store" in EDUCATIONAL_MEMORY_MODEL_SENTENCE
    assert "meaning lives in the Journal and Timeline" in (
        EDUCATIONAL_MEMORY_MODEL_SENTENCE
    )
    assert "After a Reflection" in EDUCATIONAL_MEMORY_MODEL_SENTENCE


def test_history_bridge_sentence_is_context_not_mentor():
    assert "not Study Sensei’s mentor narrative" in HISTORY_EPISTEMOLOGY_BRIDGE
    assert "Decision Journal" in HISTORY_EPISTEMOLOGY_BRIDGE
    assert "Educational Timeline" in HISTORY_EPISTEMOLOGY_BRIDGE


def test_product_language_approves_memory_terms():
    for term in (
        "Decision Journal",
        "Educational Timeline",
        "History",
        "Study Sensei",
    ):
        assert term in APPROVED_TERMS
    rejected = " ".join(REJECTED_SYNONYMS)
    assert "mission tip" in rejected


def test_journal_empty_retires_tip_and_qc_ads():
    snap = DecisionJournalTimelineSnapshot()
    empty = snap.empty_description.lower()
    assert "mission tip" not in empty
    assert "quick check" not in empty
    assert "tip" not in empty
    assert "durable educational memory" in empty
    assert "educational timeline" in empty
    assert "history" in empty
    assert "durable educational memory" in snap.intro_line.lower()


def test_timeline_empty_distinguishes_journal_and_history():
    snap = EducationalTimelineSnapshot()
    empty = snap.empty_description.lower()
    assert "mission tip" not in empty
    assert "tip" not in empty
    assert "decision journal" in empty
    assert "not a second memory store" in empty
    assert "history" in empty
    assert "chronological" in snap.intro_line.lower()


def test_onboarding_introduces_educational_memory():
    """Educational memory model is taught in Help; onboarding stays practical."""
    steps = AlphaOnboardingService.steps()
    assert "memory" not in {step["id"] for step in steps}
    from app.presentation.product_language import EDUCATIONAL_MEMORY_MODEL_SENTENCE

    assert "Decision Journal" in EDUCATIONAL_MEMORY_MODEL_SENTENCE
    assert SENSEI_HANDOFF_SENTENCE


def test_help_teaches_educational_memory_model(client, ctx):
    from tests.test_alpha_001_infrastructure import _login, _make_alpha_user

    _make_alpha_user(onboarding_done=True)
    _login(client)
    body = client.get("/alpha/help").get_data(as_text=True)
    assert "One educational memory system" in body
    assert "What is the Decision Journal?" in body
    assert "What is the Educational Timeline?" in body
    assert "How are Decision Journal and Timeline different?" in body
    assert "Why does History exist?" in body
    assert "What happens after I complete a Reflection?" in body
    assert "Where does Study Sensei remember my learning?" in body
    assert "not a second memory store" in body
    assert "Practice archives and progress context" in body or (
        "practice archives and progress stats" in body.lower()
    )
    assert "Mission tip" not in body
    assert "Daily Reflection" not in body


def test_timeline_narrative_retires_mission_tip_phrase():
    """EGC-R06 / DEP-01 — mission milestone patterns use guidance noun."""
    from pathlib import Path

    source = Path("app/domain/educational_timeline/narrative.py").read_text(
        encoding="utf-8"
    )
    assert "Mission tip marked as" not in source
    assert "Mission guidance marked as" in source
    assert "fewer recorded tips" not in source
    assert "fewer recorded guidance moments" in source


def test_journal_route_empty_state_educational(student_client):
    resp = student_client.get("/student/decision-journal")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    assert "Decision Journal" in body
    assert "durable educational memory" in body.lower()
    assert "Mission tip" not in body
    assert "Quick Check" not in body
    assert "Back to Home" in body
