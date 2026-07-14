/**
 * Founder Dashboard (FOS-004) — capability table filter only.
 * No frameworks. No charts. No animations.
 */
(function () {
  "use strict";

  var input = document.getElementById("capability-filter");
  var table = document.getElementById("capability-table");
  if (!input || !table) {
    return;
  }

  var rows = table.querySelectorAll("[data-capability-row]");
  if (!rows.length) {
    return;
  }

  input.addEventListener("input", function () {
    var query = (input.value || "").trim().toLowerCase();
    for (var i = 0; i < rows.length; i += 1) {
      var row = rows[i];
      var haystack = (row.textContent || "").toLowerCase();
      var match = !query || haystack.indexOf(query) !== -1;
      row.hidden = !match;
    }
  });
})();
