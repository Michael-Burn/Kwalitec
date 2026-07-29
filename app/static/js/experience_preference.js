/**
 * FV-001B — versioned device preference for Experience Selection.
 *
 * Schema (localStorage):
 * {
 *   "v": 1,
 *   "behaviour": "always_ask" | "remember_founder" | "remember_student",
 *   "updatedAt": "<ISO-8601>"
 * }
 *
 * Device-specific only. No cookies / no account setting / no logout required
 * to switch — open Experience Selection with ?switch=1 to force the chooser.
 */
(function (global) {
  "use strict";

  var STORAGE_KEY = "kwalitec.experiencePreference.v1";
  var SCHEMA_VERSION = 1;
  var BEHAVIOURS = {
    ALWAYS_ASK: "always_ask",
    REMEMBER_FOUNDER: "remember_founder",
    REMEMBER_STUDENT: "remember_student",
  };

  function defaultPreference() {
    return {
      v: SCHEMA_VERSION,
      behaviour: BEHAVIOURS.ALWAYS_ASK,
      updatedAt: new Date().toISOString(),
    };
  }

  function normalize(raw) {
    if (!raw || typeof raw !== "object") return defaultPreference();
    var behaviour = String(raw.behaviour || "").trim().toLowerCase();
    if (
      behaviour !== BEHAVIOURS.ALWAYS_ASK &&
      behaviour !== BEHAVIOURS.REMEMBER_FOUNDER &&
      behaviour !== BEHAVIOURS.REMEMBER_STUDENT
    ) {
      behaviour = BEHAVIOURS.ALWAYS_ASK;
    }
    return {
      v: SCHEMA_VERSION,
      behaviour: behaviour,
      updatedAt: raw.updatedAt || new Date().toISOString(),
    };
  }

  function read() {
    try {
      var text = global.localStorage.getItem(STORAGE_KEY);
      if (!text) return defaultPreference();
      return normalize(JSON.parse(text));
    } catch (err) {
      return defaultPreference();
    }
  }

  function write(behaviour) {
    var pref = normalize({
      behaviour: behaviour,
      updatedAt: new Date().toISOString(),
    });
    try {
      global.localStorage.setItem(STORAGE_KEY, JSON.stringify(pref));
    } catch (err) {
      /* private mode / quota — fail soft */
    }
    return pref;
  }

  function clear() {
    try {
      global.localStorage.removeItem(STORAGE_KEY);
    } catch (err) {
      /* ignore */
    }
  }

  global.KwalitecExperiencePreference = {
    STORAGE_KEY: STORAGE_KEY,
    BEHAVIOURS: BEHAVIOURS,
    read: read,
    write: write,
    clear: clear,
    defaultPreference: defaultPreference,
  };
})(window);
