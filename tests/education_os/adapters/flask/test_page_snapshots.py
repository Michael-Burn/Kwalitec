"""Page-level regression snapshots for eos HTML surfaces (V4-004)."""

from __future__ import annotations

from pathlib import Path

import pytest

SNAPSHOT_DIR = Path(__file__).parent / "snapshots" / "pages"


def _normalize(html: str) -> str:
    """Drop volatile whitespace while preserving structure for snapshots."""
    lines = [line.rstrip() for line in html.replace("\r\n", "\n").split("\n")]
    return "\n".join(line for line in lines if line.strip()).strip() + "\n"


def _assert_snapshot(name: str, html: str) -> None:
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    path = SNAPSHOT_DIR / name
    normalized = _normalize(html)
    if not path.exists():
        path.write_text(normalized, encoding="utf-8")
    expected = path.read_text(encoding="utf-8")
    assert normalized == expected


@pytest.mark.parametrize(
    ("path", "snapshot"),
    (
        ("/eos/login/", "login.html"),
        ("/eos/dashboard/?student_id=student-ada", "dashboard.html"),
        ("/eos/mission/?student_id=student-ada", "mission.html"),
        (
            "/eos/session/?student_id=student-ada&session_id=snap-1",
            "session.html",
        ),
        (
            "/eos/reflection/?student_id=student-ada&session_id=snap-1",
            "reflection.html",
        ),
    ),
)
def test_page_regression_snapshots(client, path: str, snapshot: str) -> None:
    response = client.get(path)
    assert response.status_code == 200
    _assert_snapshot(snapshot, response.get_data(as_text=True))
