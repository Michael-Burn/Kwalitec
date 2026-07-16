"""RR-001B Internal Alpha Provisioning / onboarding tests.

Founder observation (FC-001): the absence of registration produced
uncertainty — a participant reaching the sign-in page had no guidance on how
to obtain access or begin.

Fix (student-facing only): the login page shows a clear invite-only onboarding
note when Internal Alpha is enabled, explaining that access is provided by a
coordinator. Public self-registration is intentionally NOT reopened.

Accounts are provisioned operationally via the ``create-admin`` and
``create-test-user`` CLI commands (covered by test_internal_alpha_enablement).
"""

from __future__ import annotations

import pytest


class TestLoginOnboardingNote:
    def test_note_shown_when_internal_alpha_enabled(self, client, monkeypatch):
        monkeypatch.setenv("KWALITEC_EI_INTERNAL_ALPHA", "1")
        response = client.get("/auth/login")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "New to the Internal Alpha?" in body
        assert "invite-only" in body
        assert "coordinator" in body

    def test_note_hidden_when_internal_alpha_disabled(self, client, monkeypatch):
        monkeypatch.delenv("KWALITEC_EI_INTERNAL_ALPHA", raising=False)
        response = client.get("/auth/login")
        assert response.status_code == 200
        body = response.get_data(as_text=True)
        assert "New to the Internal Alpha?" not in body


class TestPublicRegistrationRemainsClosed:
    @pytest.mark.parametrize("path", ["/auth/register", "/register", "/auth/signup"])
    def test_no_public_registration_route(self, client, path):
        response = client.get(path)
        assert response.status_code == 404

    def test_login_page_has_no_public_signup_cta(self, client, monkeypatch):
        monkeypatch.setenv("KWALITEC_EI_INTERNAL_ALPHA", "1")
        response = client.get("/auth/login")
        body = response.get_data(as_text=True).lower()
        # Invite-only messaging is present; a public "create account" CTA is not.
        assert "sign up" not in body
        assert "create account" not in body
        assert "create an account" not in body
