"""Structural/Mechanical validator findings for content drafts."""

from __future__ import annotations

from app.application.content_lifecycle.structural_mechanical_validator import (
    RULE_MCQ_CHOICE_COUNT,
    RULE_MCQ_CORRECT_CHOICE_ID,
    RULE_NUMERIC_ANSWER_SPECIFICATION,
    RULE_OBJECTIVE_REQUIRED,
    RULE_OBJECTIVE_RESOLVE,
    validate_structural_and_mechanical,
)


class _StubObjectiveResolver:
    """Deterministic LO resolver for unit tests (no foundation dependency)."""

    def __init__(self, known: set[str]) -> None:
        self._known = known

    def resolve_from_objective_id(
        self, objective_id: str, *, subject_code: str
    ) -> str | None:
        token = (objective_id or "").strip()
        return token if token in self._known else None

    def resolve(self, token: str, *, subject_code: str) -> str | None:
        raw = (token or "").strip()
        return raw if raw in self._known else None


_RESOLVER = _StubObjectiveResolver({"CS1-B-T01-LO03"})


def _four_choices():
    return [
        {"id": "a", "label": "A"},
        {"id": "b", "label": "B"},
        {"id": "c", "label": "C"},
        {"id": "d", "label": "D"},
    ]


def _mcq_check(**overrides):
    check = {
        "item_id": "draft-ar-01",
        "kind": "active_recall",
        "response_type": "mcq",
        "prompt": "Pick one",
        "choices": _four_choices(),
        "correct_choice_id": "a",
        "objective_id": "CS1-B-T01-LO03",
    }
    check.update(overrides)
    return check


def _valid_numeric_spec():
    return {
        "item_id": "draft-cp-01",
        "canonical_value": 0.3297,
        "quantity_type": "probability",
        "assessment_intent": "calculate_value",
        "comparison_policy": {
            "policy": "absolute_tolerance",
            "absolute_tolerance": 0.001,
        },
        "accepted_forms": ["decimal"],
    }


def _payload(*checks):
    return {
        "package_id": "DRAFT-VALIDATOR-PKG",
        "subject_id": "CS1",
        "knowledge_checks": list(checks),
    }


def _rule_ids(findings):
    return {f.rule_id for f in findings}


def test_validator_rejects_three_mcq_choices():
    payload = _payload(
        _mcq_check(choices=_four_choices()[:3], correct_choice_id="a")
    )
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        objective_resolver=_RESOLVER,
    )
    assert RULE_MCQ_CHOICE_COUNT in _rule_ids(findings)
    finding = next(f for f in findings if f.rule_id == RULE_MCQ_CHOICE_COUNT)
    assert finding.severity == "error"
    assert "choices" in finding.field
    assert "3" in finding.message


def test_validator_rejects_five_mcq_choices():
    choices = _four_choices() + [{"id": "e", "label": "E"}]
    payload = _payload(_mcq_check(choices=choices, correct_choice_id="a"))
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        objective_resolver=_RESOLVER,
    )
    assert RULE_MCQ_CHOICE_COUNT in _rule_ids(findings)
    assert "5" in next(
        f.message for f in findings if f.rule_id == RULE_MCQ_CHOICE_COUNT
    )


def test_validator_rejects_mismatched_correct_choice_id():
    payload = _payload(_mcq_check(correct_choice_id="z"))
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        objective_resolver=_RESOLVER,
    )
    assert RULE_MCQ_CORRECT_CHOICE_ID in _rule_ids(findings)
    finding = next(
        f for f in findings if f.rule_id == RULE_MCQ_CORRECT_CHOICE_ID
    )
    assert "z" in finding.message
    assert finding.field.endswith("correct_choice_id")


def test_validator_rejects_missing_objective_id():
    payload = _payload(_mcq_check(objective_id=""))
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        require_objective_id=True,
        objective_resolver=_RESOLVER,
    )
    assert RULE_OBJECTIVE_REQUIRED in _rule_ids(findings)


def test_validator_rejects_unresolved_objective_id():
    payload = _payload(_mcq_check(objective_id="CS1-NOT-A-REAL-LO"))
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        objective_resolver=_RESOLVER,
    )
    assert RULE_OBJECTIVE_RESOLVE in _rule_ids(findings)
    assert "CS1-NOT-A-REAL-LO" in next(
        f.message for f in findings if f.rule_id == RULE_OBJECTIVE_RESOLVE
    )


def test_validator_rejects_invalid_numeric_configuration():
    bad_spec = {
        "item_id": "draft-cp-01",
        "canonical_value": 1.0,
        "quantity_type": "scalar",
        "assessment_intent": "calculate_value",
        "comparison_policy": {
            "policy": "absolute_tolerance",
            # missing absolute_tolerance — AnswerSpecification rejects this
        },
    }
    payload = _payload(
        {
            "item_id": "draft-cp-01",
            "kind": "checkpoint",
            "response_type": "numeric",
            "prompt": "Compute",
            "objective_id": "CS1-B-T01-LO03",
            "answer_specification": bad_spec,
        }
    )
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        objective_resolver=_RESOLVER,
    )
    assert RULE_NUMERIC_ANSWER_SPECIFICATION in _rule_ids(findings)
    finding = next(
        f for f in findings if f.rule_id == RULE_NUMERIC_ANSWER_SPECIFICATION
    )
    assert finding.severity == "error"
    assert "answer_specification" in finding.field


def test_validator_passes_well_formed_mcq_draft():
    payload = _payload(_mcq_check())
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        objective_resolver=_RESOLVER,
    )
    assert findings == ()


def test_validator_passes_well_formed_numeric_draft():
    payload = _payload(
        {
            "item_id": "draft-cp-01",
            "kind": "checkpoint",
            "response_type": "numeric",
            "prompt": "Compute the quantile",
            "objective_id": "CS1-B-T01-LO03",
            "accepted_keywords": ["0.3297"],
            "answer_specification": _valid_numeric_spec(),
        }
    )
    findings = validate_structural_and_mechanical(
        payload,
        subject_id="CS1",
        objective_resolver=_RESOLVER,
    )
    assert findings == ()


def test_validator_naming_boundary_in_docstring():
    """Honest boundary: module must not claim educational/math correctness."""
    from app.application.content_lifecycle import (
        structural_mechanical_validator as mod,
    )

    doc = (mod.__doc__ or "").lower()
    assert "structural" in doc
    assert "mechanical" in doc or "deterministic" in doc
    assert "does **not** assess mathematical" in (mod.__doc__ or "").lower() or (
        "does not assess mathematical" in doc
    )
    assert "educational" in doc and "quality" in doc
    assert "validate_structural_and_mechanical" in dir(mod)
    assert not hasattr(mod, "validate_educational_correctness")
    assert not hasattr(mod, "validate_mathematical_correctness")
