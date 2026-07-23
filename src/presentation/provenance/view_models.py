"""Presentation-only provenance view models (RR-001).

Expose up to three deterministic reasons explaining why a surface
recommendation or state exists. Never compute educational decisions.
"""

from __future__ import annotations

from dataclasses import dataclass

from presentation.design_system import Accordion, AccordionPanel
from presentation.provenance.enums import ProvenanceKind

MAX_PROVENANCE_REASONS = 3
DEFAULT_PROVENANCE_TITLE = "Why this guidance"


@dataclass(frozen=True, slots=True)
class ProvenanceReasonView:
    """One deterministic, plain-language provenance reason."""

    kind: str
    sentence: str

    def __post_init__(self) -> None:
        kind = (self.kind or "").strip() or ProvenanceKind.RECOMMENDATION.value
        sentence = " ".join((self.sentence or "").split()).strip()
        object.__setattr__(self, "kind", kind)
        object.__setattr__(self, "sentence", sentence)


@dataclass(frozen=True, slots=True)
class ProvenanceViewModel:
    """Collapsible provenance block — maximum three one-sentence reasons."""

    title: str = DEFAULT_PROVENANCE_TITLE
    reasons: tuple[ProvenanceReasonView, ...] = ()
    open: bool = False
    surface: str = ""

    def __post_init__(self) -> None:
        title = (self.title or "").strip() or DEFAULT_PROVENANCE_TITLE
        object.__setattr__(self, "title", title)
        cleaned: list[ProvenanceReasonView] = []
        seen: set[str] = set()
        for reason in tuple(self.reasons or ())[:MAX_PROVENANCE_REASONS]:
            if not isinstance(reason, ProvenanceReasonView):
                continue
            sentence = reason.sentence
            if not sentence or sentence in seen:
                continue
            seen.add(sentence)
            cleaned.append(reason)
        object.__setattr__(self, "reasons", tuple(cleaned))
        object.__setattr__(self, "surface", (self.surface or "").strip())

    @property
    def available(self) -> bool:
        return bool(self.reasons)

    @property
    def has_content(self) -> bool:
        return self.available

    @property
    def reason_count(self) -> int:
        return len(self.reasons)

    @property
    def sentences(self) -> tuple[str, ...]:
        return tuple(reason.sentence for reason in self.reasons)

    def as_accordion(self) -> Accordion:
        """Design System accordion contract for expandable provenance."""
        body = "\n".join(self.sentences)
        return Accordion(
            panels=(
                AccordionPanel(
                    title=self.title,
                    body=body,
                    open=self.open,
                ),
            ),
            label=self.title,
            allow_multiple=False,
        )

    @classmethod
    def empty(
        cls,
        *,
        title: str = DEFAULT_PROVENANCE_TITLE,
        surface: str = "",
    ) -> ProvenanceViewModel:
        return cls(title=title, reasons=(), open=False, surface=surface)

    @classmethod
    def from_reasons(
        cls,
        reasons: tuple[ProvenanceReasonView, ...] | list[ProvenanceReasonView],
        *,
        title: str = DEFAULT_PROVENANCE_TITLE,
        surface: str = "",
        open: bool = False,
    ) -> ProvenanceViewModel:
        return cls(
            title=title,
            reasons=tuple(reasons or ())[:MAX_PROVENANCE_REASONS],
            open=open,
            surface=surface,
        )
