"""AccessibilityRenderer — AccessibilityContract → HTML attributes.

Applies WCAG-oriented ARIA and focus attributes from presentation contracts.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from adapters.flask.rendering.html_helpers import format_attributes
from presentation.design_system.colours import SemanticColour, colour
from presentation.design_system.components.base import AccessibilityContract
from presentation.design_system.contrast import meets_contrast


class AccessibilityRenderer:
    """Translate accessibility contracts into HTML attribute mappings."""

    def attributes(
        self,
        contract: AccessibilityContract,
        *,
        label: str = "",
        labelled_by: str = "",
        described_by: str = "",
        disabled: bool = False,
        expanded: bool | None = None,
        pressed: bool | None = None,
        valuemin: float | None = None,
        valuemax: float | None = None,
        valuenow: float | None = None,
        valuetext: str = "",
        extra: Mapping[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Build an attribute dict honouring the accessibility contract."""
        attrs: dict[str, Any] = {}
        if contract.role:
            attrs["role"] = contract.role
        if contract.label_required:
            if labelled_by:
                attrs["aria-labelledby"] = labelled_by
            elif label:
                attrs["aria-label"] = label
        elif label:
            attrs["aria-label"] = label
        if described_by:
            attrs["aria-describedby"] = described_by
        if contract.keyboard_focusable and not disabled:
            attrs.setdefault("tabindex", "0")
        if disabled:
            attrs["aria-disabled"] = "true"
            if contract.keyboard_focusable:
                attrs["tabindex"] = "-1"
        if expanded is not None:
            attrs["aria-expanded"] = "true" if expanded else "false"
        if pressed is not None:
            attrs["aria-pressed"] = "true" if pressed else "false"
        if contract.role == "progressbar":
            attrs["aria-valuemin"] = (
                "0" if valuemin is None else str(int(valuemin))
            )
            attrs["aria-valuemax"] = (
                "100" if valuemax is None else str(int(valuemax))
            )
            if valuenow is not None:
                attrs["aria-valuenow"] = str(int(round(valuenow)))
            if valuetext:
                attrs["aria-valuetext"] = valuetext
        if contract.reduced_motion_safe:
            attrs["data-reduced-motion"] = "safe"
        if extra:
            for key, value in extra.items():
                if value is not None and value is not False:
                    attrs[key] = value
        return attrs

    def html_attributes(
        self,
        contract: AccessibilityContract,
        *,
        label: str = "",
        **kwargs: Any,
    ) -> str:
        """Serialise accessibility attributes for direct HTML embedding."""
        return format_attributes(
            self.attributes(contract, label=label, **kwargs)
        )

    def contrast_is_compliant(self, contract: AccessibilityContract) -> bool:
        """Return True when declared contrast tokens meet the contract floor."""
        if contract.contrast_fg is None or contract.contrast_bg is None:
            return True
        fg = colour(contract.contrast_fg).hex
        bg = colour(contract.contrast_bg).hex
        if not fg.startswith("#") or not bg.startswith("#"):
            # Non-solid colours (rgba) cannot be ratio-checked here.
            return True
        return meets_contrast(
            fg,
            bg,
            minimum=contract.min_contrast_ratio,
        )

    def focus_ring_token(self) -> str:
        """CSS variable for the keyboard focus ring colour."""
        return colour(SemanticColour.FOCUS_RING).css_var
