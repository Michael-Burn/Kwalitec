"""Student display name persistence and validation."""

from __future__ import annotations

from app.extensions import db
from app.models.user import User


def test_edited_display_name_is_saved_and_shown_on_profile_and_home(
    student_client, user
):
    """An edited account display name is persisted and shown everywhere it appears."""
    response = student_client.post(
        "/settings/preferences",
        data={
            "display_name": "Ada Lovelace",
            "next": "/student/profile",
        },
        follow_redirects=True,
    )
    assert response.status_code == 200
    assert b"Display name updated." in response.data

    db.session.refresh(user)
    assert user.display_name == "Ada Lovelace"

    profile_html = student_client.get("/student/profile").get_data(as_text=True)
    assert 'id="display_name"' in profile_html
    assert 'value="Ada Lovelace"' in profile_html

    home_html = student_client.get("/student/").get_data(as_text=True)
    assert "Welcome back, Ada Lovelace." in home_html


def test_display_name_rejects_empty_and_excessively_long_values(
    student_client, user
):
    """Empty, whitespace-only, too-short, and too-long names are rejected."""
    user.display_name = "Kept Name"
    db.session.commit()

    too_long = "A" * (User.DISPLAY_NAME_MAX_LENGTH + 1)
    cases = ("", "   ", "A", too_long)
    for invalid in cases:
        response = student_client.post(
            "/settings/preferences",
            data={
                "display_name": invalid,
                "next": "/student/profile",
            },
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Enter a display name between" in response.data
        db.session.refresh(user)
        assert user.display_name == "Kept Name"

    profile_html = student_client.get("/student/profile").get_data(as_text=True)
    assert 'value="Kept Name"' in profile_html
    home_html = student_client.get("/student/").get_data(as_text=True)
    assert "Welcome back, Kept Name." in home_html
    assert too_long not in home_html
