// Study Session screen helpers (LXP-002) — local checklist + elapsed timer.
(function () {
    "use strict";

    function pad(value) {
        return String(value).padStart(2, "0");
    }

    function formatElapsed(totalSeconds) {
        const hours = Math.floor(totalSeconds / 3600);
        const minutes = Math.floor((totalSeconds % 3600) / 60);
        const seconds = totalSeconds % 60;
        if (hours > 0) {
            return pad(hours) + ":" + pad(minutes) + ":" + pad(seconds);
        }
        return pad(minutes) + ":" + pad(seconds);
    }

    function initTimer() {
        const display = document.querySelector("[data-session-timer]");
        if (!display) {
            return;
        }
        const missionId = display.dataset.missionId || "session";
        const storageKey = "kwalitec.studySession.start." + missionId;
        let startedAt = window.sessionStorage.getItem(storageKey);
        if (!startedAt) {
            startedAt = String(Date.now());
            window.sessionStorage.setItem(storageKey, startedAt);
        }
        const startMs = Number(startedAt);

        function tick() {
            const elapsed = Math.max(0, Math.floor((Date.now() - startMs) / 1000));
            display.textContent = formatElapsed(elapsed);
        }

        tick();
        window.setInterval(tick, 1000);
    }

    function initActivityChecklist() {
        const items = document.querySelectorAll("[data-session-activity]");
        items.forEach(function (checkbox) {
            const key =
                "kwalitec.studySession.activity." +
                (checkbox.dataset.missionId || "session") +
                "." +
                (checkbox.dataset.activityIndex || "0");
            const saved = window.sessionStorage.getItem(key);
            if (saved === "1") {
                checkbox.checked = true;
            }
            checkbox.addEventListener("change", function () {
                window.sessionStorage.setItem(key, checkbox.checked ? "1" : "0");
            });
        });
    }

    function init() {
        initTimer();
        initActivityChecklist();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
