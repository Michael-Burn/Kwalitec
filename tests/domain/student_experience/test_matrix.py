"""Volume matrices for Student Experience domain."""

from __future__ import annotations

import itertools

import pytest

from app.domain.student_experience.experience_workspace import (
    CANONICAL_SURFACES,
    ExperienceSurface,
)
from app.domain.student_experience.student_home import readiness_band_label
from tests.domain.student_experience.helpers import make_workspace


@pytest.mark.parametrize(
    ("left", "right"),
    list(itertools.combinations(CANONICAL_SURFACES, 2)),
)
def test_surface_pairs_distinct(left, right):
    assert left is not right
    ws = make_workspace().navigate_to(left)
    assert ws.is_on(left)
    assert not ws.is_on(right)


@pytest.mark.parametrize("mask", range(32))
def test_surface_presence_mask(mask):
    selected = [
        s for i, s in enumerate(CANONICAL_SURFACES) if mask & (1 << i)
    ]
    ws = make_workspace()
    for s in selected:
        ws = ws.navigate_to(s)
        assert ws.active_surface is s


@pytest.mark.parametrize("score_i", range(0, 101, 5))
def test_readiness_band_cover(score_i):
    label = readiness_band_label(score_i / 100)
    assert label in {"Building", "Developing", "On Track", "Exam Ready"}


@pytest.mark.parametrize("surface", list(ExperienceSurface))
@pytest.mark.parametrize("exam", ["CPA", "CFA", "ACCA", "Bar"])
def test_workspace_exam_labels(surface, exam):
    ws = make_workspace(examination_label=exam).navigate_to(surface)
    assert ws.examination_label == exam
    assert ws.active_surface is surface
