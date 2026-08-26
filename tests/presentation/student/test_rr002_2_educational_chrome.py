"""RR-002.2 — Educational chrome & presentation convergence.

Closes RP-002 Contained findings RP002-NCR-005–007 without changing
recommendation algorithms, Mission Intelligence, schema, or feature flags.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]


def test_ncr005_latent_recommendation_card_macro_removed():
    """NCR-005 / RP002-NCR-005 — orphan recommendation_card macro deleted."""
    path = ROOT / "app/templates/student/components/recommendation_card.html"
    assert not path.exists()


def test_ncr006_session_feedback_reattributes_authority():
    """NCR-006 / RP002-NCR-006 — System facts + Study Sensei conclusions."""
    src = (ROOT / "app/templates/mission/session_recorded.html").read_text(
        encoding="utf-8"
    )
    assert "What the system observed" in src
    assert "What can Study Sensei honestly conclude?" in src
    assert "What did Kwalitec observe?" not in src
    assert "What can Kwalitec honestly conclude?" not in src
    assert "What happened today?" in src
    assert "What happens next?" in src


def test_ncr007_dashboard_guidance_chrome_not_recommendation_hero():
    """NCR-007 / RP002-NCR-007 — dashboard aligns with Mission-led Guidance."""
    src = (ROOT / "app/templates/dashboard/index.html").read_text(
        encoding="utf-8"
    )
    assert 'class="card-section-header mb-3">Guidance</h2>' in src
    assert ">Today's Recommendation<" not in src
    assert 'data-narrator="study-sensei">Study Sensei</p>' in src
    assert "Why this guidance?" in src
    assert "No guidance yet" in src
    assert "Study Sensei can prepare your first Mission" in src
    assert "Guidance needing attention" in src
    assert "Recommendations needing attention" not in src
    assert "Study Sensei can guide what to study each day" in src
    assert "Kwalitec can recommend what to study each day" not in src
