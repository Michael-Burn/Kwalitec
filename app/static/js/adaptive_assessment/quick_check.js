/**
 * Quick Check presentation helpers (ILE-001B).
 * Accessibility focus + reduced-motion respect. No educational logic.
 */
(function () {
  "use strict";

  function prefersReducedMotion() {
    return (
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  }

  function focusPrimaryCta() {
    var main = document.getElementById("qc-main");
    if (!main) return;
    var cta = main.querySelector("[data-qc-cta]");
    if (cta && typeof cta.focus === "function") {
      try {
        cta.focus({ preventScroll: prefersReducedMotion() });
      } catch (err) {
        cta.focus();
      }
    }
  }

  function enhanceEntryCards() {
    document.querySelectorAll("[data-qc-entry]").forEach(function (card) {
      card.setAttribute("tabindex", "-1");
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.documentElement.classList.toggle(
      "qc-reduced-motion",
      prefersReducedMotion()
    );
    enhanceEntryCards();
    if (document.body && document.body.classList.contains("qc-body")) {
      focusPrimaryCta();
    }
  });
})();
