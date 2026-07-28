/**
 * Quick Check presentation helpers (ILE-001B/C).
 * Accessibility focus, reduced-motion respect, framing expand telemetry.
 * No educational logic.
 */
(function () {
  "use strict";

  function prefersReducedMotion() {
    return (
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  }

  function csrfToken() {
    var meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") || "" : "";
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

  function expandUrl() {
    var body = document.body;
    if (body && body.getAttribute("data-qc-expand-url")) {
      return body.getAttribute("data-qc-expand-url");
    }
    return "/adaptive-assessment/quick-check/expand";
  }

  function experienceId() {
    var body = document.body;
    if (!body) return "";
    return body.getAttribute("data-qc-experience-id") || "";
  }

  function subjectCode() {
    var body = document.body;
    if (!body) return "";
    return body.getAttribute("data-qc-subject") || "";
  }

  function recordExpand(surface) {
    var token = csrfToken();
    if (!token) return;
    var body = new URLSearchParams();
    body.set("csrf_token", token);
    body.set("surface", surface || "explanation_expanded");
    body.set("experience_id", experienceId());
    body.set("subject_code", subjectCode());
    try {
      fetch(expandUrl(), {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": token,
        },
        body: body.toString(),
        credentials: "same-origin",
        keepalive: true,
      }).catch(function () {
        /* behavioural telemetry best-effort */
      });
    } catch (err) {
      /* ignore */
    }
  }

  function wireExpandPanels() {
    document.querySelectorAll("[data-qc-expand]").forEach(function (panel) {
      if (panel.getAttribute("data-qc-expand-wired") === "1") return;
      panel.setAttribute("data-qc-expand-wired", "1");
      panel.addEventListener("toggle", function () {
        if (!panel.open) return;
        var surface =
          panel.getAttribute("data-qc-surface") ||
          panel.getAttribute("data-qc-expand") ||
          "explanation_expanded";
        recordExpand(surface);
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.documentElement.classList.toggle(
      "qc-reduced-motion",
      prefersReducedMotion()
    );
    enhanceEntryCards();
    wireExpandPanels();
    if (document.body && document.body.classList.contains("qc-body")) {
      focusPrimaryCta();
    }
  });
})();
