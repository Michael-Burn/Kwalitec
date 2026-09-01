/**
 * KaTeX auto-render for Session learning content.
 * Requires katex.min.js and contrib/auto-render.min.js (CDN, defer).
 */
(function () {
  "use strict";

  var DELIMITERS = [
    { left: "$$", right: "$$", display: true },
    { left: "\\[", right: "\\]", display: true },
    { left: "$", right: "$", display: false },
    { left: "\\(", right: "\\)", display: false },
  ];

  function renderSessionMath() {
    if (typeof renderMathInElement !== "function") {
      return;
    }
    var target = document.querySelector("[data-katex-target]");
    if (!target) {
      return;
    }
    renderMathInElement(target, {
      delimiters: DELIMITERS,
      throwOnError: false,
      ignoredTags: [
        "script",
        "noscript",
        "style",
        "textarea",
        "pre",
        "code",
        "option",
      ],
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", renderSessionMath);
  } else {
    renderSessionMath();
  }
})();
