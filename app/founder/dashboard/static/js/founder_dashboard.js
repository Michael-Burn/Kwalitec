(function () {
  "use strict";

  // Capability table filter (System Operations).
  var input = document.getElementById("capability-filter");
  var table = document.getElementById("capability-table");
  if (input && table) {
    var rows = table.querySelectorAll("[data-capability-row]");
    if (rows.length) {
      input.addEventListener("input", function () {
        var query = (input.value || "").trim().toLowerCase();
        for (var i = 0; i < rows.length; i += 1) {
          var row = rows[i];
          var haystack = (row.textContent || "").toLowerCase();
          var match = !query || haystack.indexOf(query) !== -1;
          row.hidden = !match;
        }
      });
    }
  }

  // Console mobile navigation (CONSOLE-001).
  var shell = document.querySelector(".console-shell");
  var toggle = document.querySelector("[data-console-nav-toggle]");
  var backdrop = document.querySelector("[data-console-nav-close]");
  var sidebar = document.getElementById("console-sidebar");

  function setNavOpen(open) {
    if (!shell || !toggle) {
      return;
    }
    shell.classList.toggle("is-nav-open", open);
    toggle.setAttribute("aria-expanded", open ? "true" : "false");
    toggle.setAttribute(
      "aria-label",
      open ? "Close console navigation" : "Open console navigation"
    );
    if (backdrop) {
      backdrop.hidden = !open;
    }
  }

  if (toggle && shell) {
    toggle.addEventListener("click", function () {
      setNavOpen(!shell.classList.contains("is-nav-open"));
    });
  }
  if (backdrop) {
    backdrop.addEventListener("click", function () {
      setNavOpen(false);
    });
  }
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      setNavOpen(false);
    }
  });
  if (sidebar) {
    sidebar.addEventListener("keydown", function (event) {
      if (event.key !== "Tab" || !shell || !shell.classList.contains("is-nav-open")) {
        return;
      }
      var focusable = sidebar.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled])'
      );
      if (!focusable.length) {
        return;
      }
      var first = focusable[0];
      var last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    });
  }
})();
