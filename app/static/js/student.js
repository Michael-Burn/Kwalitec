/**
 * Student Experience UI — presentation behaviours only (PX-004 polish).
 * No educational calculations.
 */
(function () {
  "use strict";

  function prefersReducedMotion() {
    return (
      window.matchMedia &&
      window.matchMedia("(prefers-reduced-motion: reduce)").matches
    );
  }

  function enhancePrimaryCta() {
    var ctas = document.querySelectorAll('[data-student-cta="primary"]');
    if (ctas.length <= 1) {
      return;
    }
    // Keep the first primary CTA as the sole visual primary on the page.
    for (var i = 1; i < ctas.length; i += 1) {
      ctas[i].classList.add("btn-outline-secondary");
      ctas[i].classList.remove("student-btn-primary", "btn-primary");
    }
  }

  function announceSurface() {
    var body = document.body;
    if (!body) {
      return;
    }
    var surface = body.getAttribute("data-student-surface");
    if (!surface) {
      return;
    }
    body.setAttribute("data-student-ready", "true");
    var live = document.getElementById("student-live-region");
    if (live && !prefersReducedMotion()) {
      live.textContent = "Showing " + surface.replace(/_/g, " ");
    }
  }

  function markOptimisticNav() {
    document.addEventListener("click", function (event) {
      var link = event.target && event.target.closest
        ? event.target.closest("a.student-nav-link")
        : null;
      if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
        return;
      }
      document.body.setAttribute("data-nav-pending", "true");
    });
  }

  function csrfToken() {
    var meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") || "" : "";
  }

  function postTelemetry(eventType, extras) {
    var token = csrfToken();
    if (!token || !eventType) {
      return;
    }
    var body = new URLSearchParams();
    body.set("csrf_token", token);
    body.set("event_type", eventType);
    if (extras && extras.resource_type) {
      body.set("resource_type", extras.resource_type);
    }
    if (extras && extras.resource_id) {
      body.set("resource_id", String(extras.resource_id));
    }
    if (extras && extras.surface) {
      body.set("surface", extras.surface);
    }
    try {
      fetch("/alpha/telemetry", {
        method: "POST",
        headers: {
          "Content-Type": "application/x-www-form-urlencoded",
          "X-CSRFToken": token,
        },
        body: body.toString(),
        credentials: "same-origin",
        keepalive: true,
      }).catch(function () {
        /* Telemetry must never break the student UI. */
      });
    } catch (_err) {
      /* ignore */
    }
  }

  function wirePresentationTelemetry() {
    var coach = document.querySelector('[data-dashboard-panel="coach"]');
    if (coach) {
      coach.addEventListener(
        "focusin",
        function () {
          postTelemetry("coach_opened", { surface: "home" });
        },
        { once: true }
      );
      coach.addEventListener(
        "click",
        function () {
          postTelemetry("coach_opened", { surface: "home" });
        },
        { once: true }
      );
    }

    var readiness = document.querySelector('[data-dashboard-panel="readiness"]');
    if (readiness) {
      readiness.addEventListener(
        "focusin",
        function () {
          postTelemetry("readiness_opened", { surface: "home" });
        },
        { once: true }
      );
      readiness.addEventListener(
        "click",
        function () {
          postTelemetry("readiness_opened", { surface: "home" });
        },
        { once: true }
      );
    }

    document.querySelectorAll("[data-provenance]").forEach(function (node) {
      node.addEventListener("toggle", function () {
        if (node.open) {
          postTelemetry("provenance_expanded", { surface: "explanation" });
        }
      });
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    enhancePrimaryCta();
    announceSurface();
    markOptimisticNav();
    wirePresentationTelemetry();
  });
})();
