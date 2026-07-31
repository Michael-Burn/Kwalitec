"""Scoreable practice items for commercial Session practice (KWP-004).

Content-layer schema and deterministic scoring against authorised answer keys.
Does not redefine Evidence grades, Twin math, or Session FSM. Activity engines
score here; Evidence Package Builder maps outcomes to EV-RT-07 / EV-RT-08 /
EV-RT-40.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class PracticeResponseType(StrEnum):
    """Authorised response shapes for scoreable Session practice."""

    MCQ = "mcq"
    NUMERIC = "numeric"
    SHORT_STRUCTURED = "short_structured"
    FREE_TEXT = "free_text"


@dataclass(frozen=True)
class AnswerKey:
    """Authorised correct answers / acceptable variants."""

    accepted: tuple[str, ...]
    case_sensitive: bool = False
    numeric_tolerance: float | None = None
    correct_choice_id: str = ""

    def to_opaque(self) -> dict[str, Any]:
        return {
            "accepted": list(self.accepted),
            "case_sensitive": self.case_sensitive,
            "numeric_tolerance": self.numeric_tolerance,
            "correct_choice_id": self.correct_choice_id,
        }

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> AnswerKey | None:
        if not isinstance(raw, dict):
            return None
        accepted = tuple(
            str(v).strip() for v in (raw.get("accepted") or ()) if str(v).strip()
        )
        if not accepted and not str(raw.get("correct_choice_id") or "").strip():
            return None
        tol = raw.get("numeric_tolerance")
        return cls(
            accepted=accepted,
            case_sensitive=bool(raw.get("case_sensitive")),
            numeric_tolerance=float(tol) if tol is not None else None,
            correct_choice_id=str(raw.get("correct_choice_id") or "").strip(),
        )


@dataclass(frozen=True)
class MarkScheme:
    """Deterministic mark points for learner-facing feedback."""

    points: tuple[str, ...] = ()
    max_marks: int = 1

    def to_opaque(self) -> dict[str, Any]:
        return {"points": list(self.points), "max_marks": int(self.max_marks)}

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> MarkScheme:
        if not isinstance(raw, dict):
            return cls()
        points = tuple(
            str(p).strip() for p in (raw.get("points") or ()) if str(p).strip()
        )
        try:
            max_marks = max(1, int(raw.get("max_marks") or 1))
        except (TypeError, ValueError):
            max_marks = 1
        return cls(points=points, max_marks=max_marks)


@dataclass(frozen=True)
class ScoreablePracticeItem:
    """One assessable practice item bound to syllabus / learning objectives."""

    item_id: str
    prompt: str
    response_type: PracticeResponseType
    answer_key: AnswerKey
    explanation: str
    model_answer: str
    mark_scheme: MarkScheme = field(default_factory=MarkScheme)
    common_mistake: str = ""
    next_action: str = ""
    objective_ids: tuple[str, ...] = ()
    syllabus_refs: tuple[str, ...] = ()
    topic_id: str = ""
    topic_keywords: tuple[str, ...] = ()
    choices: tuple[tuple[str, str], ...] = ()
    emit_structured: bool = False
    body: str = ""
    supporting_material: str = ""
    hints: tuple[str, ...] = ()

    @property
    def is_structured(self) -> bool:
        return self.response_type in {
            PracticeResponseType.MCQ,
            PracticeResponseType.NUMERIC,
        } or self.emit_structured

    def to_opaque(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "prompt": self.prompt,
            "response_type": self.response_type.value,
            "answer_key": self.answer_key.to_opaque(),
            "mark_scheme": self.mark_scheme.to_opaque(),
            "explanation": self.explanation,
            "model_answer": self.model_answer,
            "common_mistake": self.common_mistake,
            "next_action": self.next_action,
            "objective_ids": list(self.objective_ids),
            "syllabus_refs": list(self.syllabus_refs),
            "topic_id": self.topic_id,
            "topic_keywords": list(self.topic_keywords),
            "choices": [{"id": cid, "label": label} for cid, label in self.choices],
            "emit_structured": self.emit_structured,
            "body": self.body,
            "supporting_material": self.supporting_material,
            "hints": list(self.hints),
        }

    def learner_opaque(self) -> dict[str, Any]:
        """Learner-safe payload — never exposes the answer key."""
        return {
            "item_id": self.item_id,
            "prompt": self.prompt,
            "response_type": self.response_type.value,
            "choices": [{"id": cid, "label": label} for cid, label in self.choices],
            "objective_ids": list(self.objective_ids),
            "syllabus_refs": list(self.syllabus_refs),
            "mark_scheme_points": list(self.mark_scheme.points),
            "max_marks": self.mark_scheme.max_marks,
        }

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> ScoreablePracticeItem | None:
        if not isinstance(raw, dict) or not raw.get("item_id"):
            return None
        key = AnswerKey.from_opaque(raw.get("answer_key"))
        if key is None:
            return None
        try:
            raw_type = str(
                raw.get("response_type")
                or PracticeResponseType.SHORT_STRUCTURED.value
            )
            response_type = PracticeResponseType(raw_type)
        except ValueError:
            response_type = PracticeResponseType.SHORT_STRUCTURED
        choices_raw = raw.get("choices") or ()
        choices: list[tuple[str, str]] = []
        for choice in choices_raw:
            if isinstance(choice, dict):
                cid = str(choice.get("id") or "").strip()
                label = str(choice.get("label") or "").strip()
                if cid and label:
                    choices.append((cid, label))
            elif isinstance(choice, list | tuple) and len(choice) >= 2:
                choices.append((str(choice[0]).strip(), str(choice[1]).strip()))
        return cls(
            item_id=str(raw["item_id"]).strip(),
            prompt=str(raw.get("prompt") or "").strip(),
            response_type=response_type,
            answer_key=key,
            explanation=str(raw.get("explanation") or "").strip(),
            model_answer=str(raw.get("model_answer") or "").strip(),
            mark_scheme=MarkScheme.from_opaque(raw.get("mark_scheme")),
            common_mistake=str(raw.get("common_mistake") or "").strip(),
            next_action=str(raw.get("next_action") or "").strip(),
            objective_ids=tuple(
                str(o).strip()
                for o in (raw.get("objective_ids") or ())
                if str(o).strip()
            ),
            syllabus_refs=tuple(
                str(r).strip()
                for r in (raw.get("syllabus_refs") or ())
                if str(r).strip()
            ),
            topic_id=str(raw.get("topic_id") or "").strip(),
            topic_keywords=tuple(
                str(k).strip().lower()
                for k in (raw.get("topic_keywords") or ())
                if str(k).strip()
            ),
            choices=tuple(choices),
            emit_structured=bool(raw.get("emit_structured")),
            body=str(raw.get("body") or "").strip(),
            supporting_material=str(raw.get("supporting_material") or "").strip(),
            hints=tuple(
                str(h).strip() for h in (raw.get("hints") or ()) if str(h).strip()
            ),
        )


@dataclass(frozen=True)
class PracticeScoreResult:
    """Deterministic scoring outcome for one practice response."""

    scored: bool
    correct: bool | None
    marks_awarded: float = 0.0
    marks_available: float = 1.0
    matched_key: str = ""
    feedback_outcome: str = "Not yet scored"
    explanation: str = ""
    model_answer: str = ""
    common_mistake: str = ""
    next_action: str = ""
    emit_structured: bool = False
    item_id: str = ""
    response_type: str = ""

    @property
    def scored_correct(self) -> bool | None:
        return self.correct if self.scored else None

    def to_opaque(self) -> dict[str, Any]:
        return {
            "scored": self.scored,
            "correct": self.correct,
            "scored_correct": self.scored_correct,
            "marks_awarded": self.marks_awarded,
            "marks_available": self.marks_available,
            "matched_key": self.matched_key,
            "feedback_outcome": self.feedback_outcome,
            "explanation": self.explanation,
            "model_answer": self.model_answer,
            "common_mistake": self.common_mistake,
            "next_action": self.next_action,
            "emit_structured": self.emit_structured,
            "item_id": self.item_id,
            "response_type": self.response_type,
            "accuracy": (
                (self.marks_awarded / self.marks_available)
                if self.scored and self.marks_available
                else None
            ),
        }


def score_practice_response(
    item: ScoreablePracticeItem | None,
    response: str,
) -> PracticeScoreResult:
    """Score ``response`` against an authorised item.

    Unscoreable when the item or answer key is missing — never invents correctness.
    """
    text = (response or "").strip()
    if item is None or not text:
        return PracticeScoreResult(
            scored=False,
            correct=None,
            feedback_outcome="Not yet scored",
            explanation=(
                "This attempt was recorded. Scoring needs an authorised answer key."
                if item is None
                else "Enter a response to receive feedback."
            ),
            model_answer=(item.model_answer if item is not None else ""),
            common_mistake=(item.common_mistake if item is not None else ""),
            next_action=(
                item.next_action
                if item is not None
                else "Continue when you are ready."
            ),
            item_id=(item.item_id if item is not None else ""),
            response_type=(
                item.response_type.value if item is not None else ""
            ),
        )

    correct, matched = _matches_key(item, text)
    marks = float(item.mark_scheme.max_marks)
    awarded = marks if correct else 0.0
    outcome = "Correct" if correct else "Incorrect"
    next_action = item.next_action
    if not next_action:
        next_action = (
            "Continue to the next practice step."
            if correct
            else "Review the model answer, then try the next question."
        )
    return PracticeScoreResult(
        scored=True,
        correct=correct,
        marks_awarded=awarded,
        marks_available=marks,
        matched_key=matched,
        feedback_outcome=outcome,
        explanation=item.explanation,
        model_answer=item.model_answer,
        common_mistake="" if correct else item.common_mistake,
        next_action=next_action,
        emit_structured=item.is_structured,
        item_id=item.item_id,
        response_type=item.response_type.value,
    )


def _matches_key(item: ScoreablePracticeItem, response: str) -> tuple[bool, str]:
    key = item.answer_key
    if item.response_type is PracticeResponseType.MCQ:
        return _match_mcq(item, response)
    if item.response_type is PracticeResponseType.NUMERIC:
        return _match_numeric(key, response)
    return _match_text(key, response)


def _match_mcq(
    item: ScoreablePracticeItem, response: str
) -> tuple[bool, str]:
    raw = response.strip()
    normalised = _normalise(raw, case_sensitive=False)
    correct_id = (item.answer_key.correct_choice_id or "").strip()
    if correct_id and (
        normalised == _normalise(correct_id, case_sensitive=False)
        or raw == correct_id
    ):
        return True, correct_id
    for cid, label in item.choices:
        if cid == correct_id or _normalise(label, case_sensitive=False) in {
            _normalise(a, case_sensitive=False) for a in item.answer_key.accepted
        }:
            if normalised in {
                _normalise(cid, case_sensitive=False),
                _normalise(label, case_sensitive=False),
            }:
                return True, cid or label
    for accepted in item.answer_key.accepted:
        if normalised == _normalise(
            accepted, case_sensitive=item.answer_key.case_sensitive
        ):
            return True, accepted
    return False, ""


def _match_numeric(key: AnswerKey, response: str) -> tuple[bool, str]:
    candidate = _parse_number(response)
    if candidate is None:
        return False, ""
    tol = key.numeric_tolerance
    if tol is None:
        tol = 1e-6
    for accepted in key.accepted:
        expected = _parse_number(accepted)
        if expected is None:
            continue
        if abs(candidate - expected) <= tol:
            return True, accepted
    return False, ""


def _match_text(key: AnswerKey, response: str) -> tuple[bool, str]:
    normalised = _normalise(response, case_sensitive=key.case_sensitive)
    for accepted in key.accepted:
        target = _normalise(accepted, case_sensitive=key.case_sensitive)
        if not target:
            continue
        if normalised == target or target in normalised:
            return True, accepted
    return False, ""


def _normalise(value: str, *, case_sensitive: bool) -> str:
    text = (value or "").strip()
    if not case_sensitive:
        text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^\w\s.%-]", "", text)
    return text.strip()


def _parse_number(value: str) -> float | None:
    cleaned = (value or "").strip().replace(",", "")
    cleaned = re.sub(r"[^0-9eE.+-]", "", cleaned)
    if not cleaned:
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None
