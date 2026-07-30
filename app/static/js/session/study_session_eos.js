/**
 * UX-001 — EOS Study Session chrome: live timer + focus mode.
 * Presentation only — does not change session completion semantics.
 */
(function () {
  "use strict";

  var root = document.querySelector("[data-ux='study-session']");
  if (!root) return;

  var missionId = root.getAttribute("data-mission-id") || root.getAttribute("data-session-id") || "session";
  var timerEl = root.querySelector("[data-session-timer]");
  var focusBtn = root.querySelector("[data-session-focus-toggle]");

  function pad(n) {
    return String(n).padStart(2, "0");
  }

  function formatElapsed(totalSeconds) {
    var hours = Math.floor(totalSeconds / 3600);
    var minutes = Math.floor((totalSeconds % 3600) / 60);
    var seconds = totalSeconds % 60;
    if (hours > 0) {
      return pad(hours) + ":" + pad(minutes) + ":" + pad(seconds);
    }
    return pad(minutes) + ":" + pad(seconds);
  }

  function storageKey() {
    return "kwalitec.eosSession.timer." + missionId;
  }

  function loadStart() {
    try {
      var raw = window.localStorage.getItem(storageKey());
      if (!raw) return null;
      var parsed = JSON.parse(raw);
      return parsed && parsed.started_at ? Number(parsed.started_at) : null;
    } catch (err) {
      return null;
    }
  }

  function ensureStart() {
    var existing = loadStart();
    if (existing) return existing;
    var now = Date.now();
    try {
      window.localStorage.setItem(
        storageKey(),
        JSON.stringify({ started_at: now })
      );
    } catch (err) {
      /* ignore quota */
    }
    return now;
  }

  if (timerEl) {
    var started = ensureStart();
    function tick() {
      var elapsed = Math.max(0, Math.floor((Date.now() - started) / 1000));
      timerEl.textContent = formatElapsed(elapsed);
    }
    tick();
    window.setInterval(tick, 1000);
  }

  if (focusBtn) {
    focusBtn.addEventListener("click", function () {
      var on = document.body.classList.toggle("ds-focus-mode");
      focusBtn.setAttribute("aria-pressed", on ? "true" : "false");
      focusBtn.textContent = on ? "Exit focus" : "Focus mode";
    });
  }
})();
