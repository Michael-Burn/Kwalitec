"""Unit tests for OperationalStateValidator (FOS-005)."""

from __future__ import annotations

from dataclasses import replace

from app.founder.operational_state.models import SourceVersions
from app.founder.operational_state.tests.helpers import (
    make_alpha_dto,
    make_builder,
    make_capability_dto,
    make_knowledge_dto,
)
from app.founder.operational_state.validators import OperationalStateValidator


def _valid_state():
    return make_builder().build(
        make_knowledge_dto(),
        make_capability_dto(),
        make_alpha_dto(),
        validate=False,
    )


class TestOperationalStateValidator:
    def test_valid_state_ok(self) -> None:
        report = OperationalStateValidator().validate(_valid_state())
        assert report.ok is True
        assert report.issues == ()

    def test_missing_snapshot_version(self) -> None:
        state = replace(_valid_state(), snapshot_version="")
        report = OperationalStateValidator().validate(state)
        assert report.ok is False
        assert any(i.code == "missing_snapshot_version" for i in report.issues)

    def test_snapshot_version_mismatch(self) -> None:
        state = replace(_valid_state(), snapshot_version="9.9")
        report = OperationalStateValidator().validate(state)
        assert any(i.code == "snapshot_version_mismatch" for i in report.issues)

    def test_empty_source_version(self) -> None:
        state = replace(
            _valid_state(),
            source_versions=SourceVersions(
                knowledge="",
                capability_archive="capability-1.0",
                internal_alpha="alpha-1.0",
            ),
        )
        report = OperationalStateValidator().validate(state)
        assert any(i.code == "empty_source_version" for i in report.issues)

    def test_duplicate_subsystem_source_versions(self) -> None:
        state = replace(
            _valid_state(),
            source_versions=SourceVersions(
                knowledge="same-1.0",
                capability_archive="same-1.0",
                internal_alpha="alpha-1.0",
            ),
        )
        report = OperationalStateValidator().validate(state)
        assert any(i.code == "duplicate_subsystem_data" for i in report.issues)

    def test_unwired_sources_may_share_token(self) -> None:
        state = replace(
            _valid_state(),
            source_versions=SourceVersions(
                knowledge="unwired",
                capability_archive="unwired",
                internal_alpha="unwired",
            ),
        )
        report = OperationalStateValidator().validate(state)
        assert report.ok is True

    def test_negative_count(self) -> None:
        state = replace(
            _valid_state(),
            capability=replace(_valid_state().capability, total_count=-3),
        )
        report = OperationalStateValidator().validate(state)
        assert any(i.code == "negative_count" for i in report.issues)

    def test_cross_section_engineering_inconsistency(self) -> None:
        state = replace(
            _valid_state(),
            engineering=replace(
                _valid_state().engineering, standards_count=99
            ),
        )
        report = OperationalStateValidator().validate(state)
        assert any(
            i.code == "inconsistent_engineering_standards" for i in report.issues
        )

    def test_missing_current_release(self) -> None:
        state = replace(
            _valid_state(),
            release=replace(_valid_state().release, current_release=""),
        )
        report = OperationalStateValidator().validate(state)
        assert any(i.code == "missing_current_release" for i in report.issues)
