/**
 * Assessment Delivery — optional response timing capture.
 * Server remains authoritative; this only fills response_time_ms.
 */
(function () {
  "use strict";

  function initResponseTiming() {
    var form = document.querySelector("[data-assessment-response]");
    if (!form) {
      return;
    }
    var started = Date.now();
    var field = document.getElementById("assessment-response-time");
    form.addEventListener("submit", function () {
      if (field) {
        field.value = String(Math.max(0, Date.now() - started));
      }
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initResponseTiming);
  } else {
    initResponseTiming();
  }
})();
