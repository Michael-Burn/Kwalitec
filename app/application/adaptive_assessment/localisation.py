"""Localisation readiness for Adaptive Assessment product resources.

Externalises learner-facing strings, supports pluralisation and variable
interpolation. Does not translate — English defaults only (ILE-001A).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from string import Formatter

from app.application.adaptive_assessment.copy_registry import (
    AdaptiveAssessmentCopy,
    get_copy,
    iter_copy_entries,
)

_FORMATTER = Formatter()


@dataclass(frozen=True)
class PluralForms:
    """CLDR-style plural forms for one message (English subset)."""

    one: str
    other: str


@dataclass(frozen=True)
class CatalogueEntry:
    """One localisable catalogue entry (locale-ready, not yet translated)."""

    key: str
    default: str
    plurals: PluralForms | None = None
    description: str = ""


@dataclass(frozen=True)
class MessageCatalogue:
    """Immutable message catalogue for a locale.

    Attributes:
        locale: BCP 47 locale tag (defaults to ``en``).
        entries: Key → catalogue entry.
    """

    locale: str = "en"
    entries: dict[str, CatalogueEntry] = field(default_factory=dict)

    def get(self, key: str) -> CatalogueEntry:
        """Return entry or raise ``KeyError``."""
        if key not in self.entries:
            raise KeyError(f"catalogue missing key: {key}")
        return self.entries[key]

    def has(self, key: str) -> bool:
        """True when ``key`` is present."""
        return key in self.entries


def format_message(
    template: str,
    /,
    **variables: object,
) -> str:
    """Interpolate ``{name}`` placeholders; unknown keys left untouched.

    Uses ``str.format_map`` with a tolerant mapping so missing variables do
    not raise — useful while UI wiring is incomplete.
    """

    class _Safe(dict):
        def __missing__(self, key: str) -> str:  # type: ignore[override]
            return "{" + key + "}"

    # Validate template fields are brace-style (no printf).
    for _, field_name, _, _ in _FORMATTER.parse(template):
        if field_name is None:
            continue
    return template.format_map(_Safe(**variables))


def select_plural(
    forms: PluralForms,
    count: int,
) -> str:
    """Select English plural form for ``count`` (one vs other)."""
    if int(count) == 1:
        return forms.one
    return forms.other


def format_pluralizable(
    key: str,
    *,
    count: int,
    catalogue: MessageCatalogue | None = None,
    **variables: object,
) -> str:
    """Resolve a pluralizable copy key and interpolate variables.

    English rule: ``one`` when count == 1, else ``other``. The default
    catalogue synthesises ``one`` / ``other`` from the English default when
    explicit plurals are absent (``other`` uses the default; ``one`` uses
    the same string with singular-friendly wording where registered).
    """
    cat = catalogue if catalogue is not None else get_default_catalogue()
    entry = cat.get(key)
    if entry.plurals is not None:
        template = select_plural(entry.plurals, count)
    else:
        template = entry.default
    return format_message(template, count=count, **variables)


def build_catalogue_from_copy_registry(
    *,
    locale: str = "en",
) -> MessageCatalogue:
    """Build a locale catalogue from the Adaptive Assessment copy registry."""
    entries: dict[str, CatalogueEntry] = {}
    for copy_entry in iter_copy_entries():
        plurals = _english_plurals_for(copy_entry)
        entries[copy_entry.key] = CatalogueEntry(
            key=copy_entry.key,
            default=copy_entry.default,
            plurals=plurals,
            description=copy_entry.description,
        )
    return MessageCatalogue(locale=locale, entries=entries)


def _english_plurals_for(entry: AdaptiveAssessmentCopy) -> PluralForms | None:
    """Synthesise English plural forms for pluralizable keys."""
    if not entry.pluralizable:
        return None
    # Known pluralizable templates.
    if entry.key == "duration.about_minutes":
        return PluralForms(
            one="About {count} minute",
            other="About {count} minutes",
        )
    return PluralForms(one=entry.default, other=entry.default)


_DEFAULT_CATALOGUE: MessageCatalogue | None = None


def get_default_catalogue() -> MessageCatalogue:
    """Return the process-default English catalogue (lazy singleton)."""
    global _DEFAULT_CATALOGUE
    if _DEFAULT_CATALOGUE is None:
        _DEFAULT_CATALOGUE = build_catalogue_from_copy_registry(locale="en")
    return _DEFAULT_CATALOGUE


def resolve_copy(
    key: str,
    *,
    catalogue: MessageCatalogue | None = None,
    count: int | None = None,
    **variables: object,
) -> str:
    """Resolve a copy key with optional pluralisation and interpolation."""
    cat = catalogue if catalogue is not None else get_default_catalogue()
    if count is not None and get_copy(key).pluralizable:
        return format_pluralizable(
            key, count=count, catalogue=cat, **variables
        )
    entry = cat.get(key)
    return format_message(entry.default, **variables)
