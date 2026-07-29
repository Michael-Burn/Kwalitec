/**
 * FV-001B — Experience Selection page controller.
 * Applies remembered preference (unless ?switch=1) and wires chooser actions.
 */
(function () {
  "use strict";

  function qs(sel, root) {
    return (root || document).querySelector(sel);
  }

  function paramSwitch() {
    try {
      return new URLSearchParams(window.location.search).get("switch") === "1";
    } catch (err) {
      return false;
    }
  }

  function go(url) {
    if (!url) return;
    window.location.assign(url);
  }

  function setStatus(text) {
    var el = qs("[data-experience-status]");
    if (el) el.textContent = text || "";
  }

  function applyRemembered(root) {
    if (paramSwitch()) return false;
    var api = window.KwalitecExperiencePreference;
    if (!api) return false;
    var pref = api.read();
    var founderUrl = root.getAttribute("data-founder-url");
    var studentUrl = root.getAttribute("data-student-url");
    if (pref.behaviour === api.BEHAVIOURS.REMEMBER_FOUNDER && founderUrl) {
      setStatus("Opening Founder Console…");
      go(founderUrl);
      return true;
    }
    if (pref.behaviour === api.BEHAVIOURS.REMEMBER_STUDENT && studentUrl) {
      setStatus("Opening Student Experience…");
      go(studentUrl);
      return true;
    }
    return false;
  }

  function syncBehaviourRadios(root) {
    var api = window.KwalitecExperiencePreference;
    if (!api) return;
    var pref = api.read();
    var radios = root.querySelectorAll('input[name="experience-remember"]');
    radios.forEach(function (radio) {
      radio.checked = radio.value === pref.behaviour;
    });
  }

  function selectedBehaviour(root) {
    var checked = qs('input[name="experience-remember"]:checked', root);
    if (checked) return checked.value;
    var api = window.KwalitecExperiencePreference;
    return api ? api.BEHAVIOURS.ALWAYS_ASK : "always_ask";
  }

  function persistFromChooser(root) {
    var api = window.KwalitecExperiencePreference;
    if (!api) return;
    api.write(selectedBehaviour(root));
  }

  function init() {
    var root = qs("[data-experience-selection]");
    if (!root) return;

    if (applyRemembered(root)) return;

    root.hidden = false;
    syncBehaviourRadios(root);
    setStatus("Choose where to continue.");

    root.addEventListener("click", function (evt) {
      var btn = evt.target.closest("[data-experience-choose]");
      if (!btn) return;
      evt.preventDefault();
      persistFromChooser(root);
      var choice = btn.getAttribute("data-experience-choose");
      if (choice === "founder") {
        go(root.getAttribute("data-founder-url"));
      } else if (choice === "student") {
        go(root.getAttribute("data-student-url"));
      }
    });

    root.addEventListener("change", function (evt) {
      if (!evt.target.matches('input[name="experience-remember"]')) return;
      persistFromChooser(root);
      setStatus("Preference saved on this device.");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
