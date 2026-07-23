"""ARP-004 product language tests — Founder / Curriculum Studio presentation."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.domain.curriculum_studio.workflow_stage import WorkflowStage
from app.founder.dashboard.nav import COMMAND_CENTRE_NAV
from app.presentation.curriculum_studio.forms import (
    AdvanceWorkflowForm,
    ApproveWorkspaceForm,
    AssignVersionForm,
    CreateSubjectForm,
    CreateWorkspaceForm,
    PreviewWorkspaceForm,
    PublishWorkspaceForm,
    ValidateWorkspaceForm,
)
from app.presentation.curriculum_studio.view_models import (
    FLASH_SUCCESS,
    FLASH_WARNING,
    NEXT_ACTION_BY_STAGE,
    STAGE_LABELS,
)
from app.presentation.product_language import (
    FOUNDER_PRIMARY_NAV_LABELS,
    FOUNDER_STUDIO_CTAS,
    REJECTED_SYNONYMS,
)
from tests.presentation.workflows.helpers import login_founder, wire_studio

GUIDE = Path("knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md")
STUDIO_TEMPLATES = Path("app/templates/curriculum_studio")
FOUNDER_TEMPLATES = Path(
    "app/founder/dashboard/templates/founder_dashboard"
)


@pytest.fixture
def founder_client(app, client, ctx):
    wire_studio(app, with_workspace=True)
    login_founder(client, app)
    return client


@pytest.fixture
def app_ctx(app):
    with app.app_context():
        with app.test_request_context():
            yield


# --- Guide & nav -----------------------------------------------------------


def test_guide_documents_publish_curriculum_cta():
    text = GUIDE.read_text(encoding="utf-8")
    assert "Publish Curriculum" in text
    assert "Review Evidence" in text


@pytest.mark.parametrize("label", FOUNDER_PRIMARY_NAV_LABELS)
def test_founder_nav_includes_approved_label(label):
    labels = [item.label for item in COMMAND_CENTRE_NAV]
    assert label in labels


def test_founder_nav_labels_match_guide_order_core():
    labels = [item.label for item in COMMAND_CENTRE_NAV]
    assert labels.index("Learning") < labels.index("Assessments")
    assert labels.index("Assessments") < labels.index("Content")


# --- Studio CTAs -----------------------------------------------------------


@pytest.mark.parametrize(
    ("form_cls", "label"),
    (
        (CreateSubjectForm, "Create Subject"),
        (CreateWorkspaceForm, "Open Workspace"),
        (AdvanceWorkflowForm, "Advance to Next Stage"),
        (ValidateWorkspaceForm, "Validate Curriculum"),
        (PreviewWorkspaceForm, "Build Preview"),
        (ApproveWorkspaceForm, "Approve Curriculum"),
        (PublishWorkspaceForm, "Publish Curriculum"),
        (AssignVersionForm, "Assign Version"),
    ),
)
def test_studio_form_cta_title_case(app_ctx, form_cls, label):
    assert form_cls().submit.label.text == label
    assert label in FOUNDER_STUDIO_CTAS


def test_studio_workspace_renders_publish_curriculum(founder_client):
    html = founder_client.get("/console/studio/workspaces/ws-cs1").get_data(
        as_text=True
    )
    assert "Publish Curriculum" in html
    assert "execute publish" not in html.lower()
    assert "go live" not in html.lower()


def test_studio_dashboard_headings_title_case(founder_client):
    html = founder_client.get("/console/studio/").get_data(as_text=True)
    assert "Create Subject" in html
    assert "Open Workspace" in html


def test_publication_stage_label_is_publish():
    assert STAGE_LABELS[WorkflowStage.PUBLICATION.value] == "Publish"


@pytest.mark.parametrize("stage", list(WorkflowStage))
def test_stage_labels_avoid_go_live_and_release(stage):
    label = STAGE_LABELS[stage.value].lower()
    assert "go live" not in label
    assert label != "release"
    assert label != "publication"


# --- Studio flashes --------------------------------------------------------


@pytest.mark.parametrize("key", list(FLASH_SUCCESS))
def test_studio_success_uses_we_voice(key):
    msg = FLASH_SUCCESS[key]
    assert msg.startswith("We've")
    assert msg.endswith(".")


@pytest.mark.parametrize("key", list(FLASH_WARNING))
def test_studio_warnings_use_we_couldnt_or_recovery(key):
    msg = FLASH_WARNING[key]
    lowered = msg.lower()
    assert msg.endswith(".")
    assert "we couldn't" in lowered or "could not be found" in lowered
    assert "try again" in lowered


def test_publish_success_matches_guide_example():
    assert FLASH_SUCCESS["published"] == (
        "We've published your curriculum successfully."
    )


def test_publish_warning_guides_approval_path():
    msg = FLASH_WARNING["publish"].lower()
    assert "couldn't publish" in msg
    assert "approval" in msg or "version" in msg
    assert "try again" in msg


def test_approval_next_step_avoids_student_experience_jargon():
    text = NEXT_ACTION_BY_STAGE[WorkflowStage.APPROVAL.value]
    assert "Student Experience" not in text
    assert "student" in text.lower()


# --- Founder advisory pages ------------------------------------------------


def test_intelligence_review_evidence_cta(founder_client):
    html = founder_client.get("/console/intelligence").get_data(as_text=True)
    assert "Review Evidence" in html
    assert "Open Evidence Gates checklist" not in html
    assert "Open Curriculum Studio" not in html


def test_evidence_gates_links_avoid_open_verb(founder_client):
    html = founder_client.get("/console/evidence-gates").get_data(as_text=True)
    assert "Evidence Gates" in html
    assert "Open Curriculum Studio" not in html
    assert "Curriculum Studio" in html
    assert "Founder Intelligence" in html


def test_intelligence_avoids_execute_launch(founder_client):
    html = founder_client.get("/console/intelligence").get_data(as_text=True).lower()
    assert "execute" not in html
    assert "launch" not in html


def test_studio_templates_avoid_go_live():
    for path in STUDIO_TEMPLATES.rglob("*.html"):
        text = path.read_text(encoding="utf-8").lower()
        assert "go live" not in text, path


def test_evidence_and_intelligence_templates_avoid_rejected_learner_terms():
    for name in ("founder_intelligence.html", "evidence_gates.html"):
        text = (FOUNDER_TEMPLATES / name).read_text(encoding="utf-8").lower()
        for term in ("digital twin", "student twin", "mission engine"):
            assert term not in text, f"{name} contains {term}"


def test_studio_presentation_avoids_learning_session_synonym():
    root = Path("app/presentation/curriculum_studio")
    for path in root.rglob("*.py"):
        # Docstrings may mention architecture; flash/CTA strings must not.
        if path.name in {"view_models.py", "forms.py", "routes.py"}:
            source = path.read_text(encoding="utf-8").lower()
            assert "go live" not in source
            assert "execute publish" not in source


@pytest.mark.parametrize(
    "path",
    ("/console/studio/", "/console/intelligence", "/console/evidence-gates"),
)
def test_founder_pages_avoid_rejected_product_synonyms(founder_client, path):
    html = founder_client.get(path).get_data(as_text=True).lower()
    for term in ("study session", "go live", "progress path", "twin insights"):
        assert term not in html, f"{path} contains {term}"


def test_rejected_synonyms_constant_covers_guide():
    for term in ("study session", "learning session", "go live", "twin insights"):
        assert term in REJECTED_SYNONYMS
