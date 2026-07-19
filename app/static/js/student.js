/**
 * Student Experience UI — presentation behaviours only.
 * No educational calculations.
 */
(function () {
  "use strict";

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
  }

  document.addEventListener("DOMContentLoaded", function () {
    enhancePrimaryCta();
    announceSurface();
  });
})();
