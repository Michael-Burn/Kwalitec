(function () {
    "use strict";

    var STATUS_RUNNING = "RUNNING";
    var STATUS_PAUSED = "PAUSED";
    var STATUS_COMPLETED = "COMPLETED";
    var STATUS_NOT_STARTED = "NOT_STARTED";

    function pad(value) {
        return String(value).padStart(2, "0");
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

    function timerStorageKey(missionId) {
        return "kwalitec.studySession.timer." + missionId;
    }

    function finalizedStorageKey(missionId) {
        return "kwalitec.studySession.finalizedSeconds." + missionId;
    }

    function defaultState() {
        return {
            status: STATUS_NOT_STARTED,
            accumulated_seconds: 0,
            running_since_ms: null,
        };
    }

    function loadState(missionId) {
        try {
            var raw = window.localStorage.getItem(timerStorageKey(missionId));
            if (!raw) {
                return defaultState();
            }
            var parsed = JSON.parse(raw);
            if (!parsed || typeof parsed !== "object") {
                return defaultState();
            }
            return {
                status: parsed.status || STATUS_NOT_STARTED,
                accumulated_seconds: Math.max(
                    0,
                    Number(parsed.accumulated_seconds) || 0
                ),
                running_since_ms:
                    parsed.running_since_ms == null
                        ? null
                        : Number(parsed.running_since_ms),
            };
        } catch (err) {
            return defaultState();
        }
    }

    function saveState(missionId, state) {
        window.localStorage.setItem(
            timerStorageKey(missionId),
            JSON.stringify(state)
        );
    }

    function elapsedSeconds(state, nowMs) {
        if (state.status === STATUS_RUNNING && state.running_since_ms != null) {
            var open = Math.max(
                0,
                Math.floor((nowMs - state.running_since_ms) / 1000)
            );
            return state.accumulated_seconds + open;
        }
        return state.accumulated_seconds;
    }

    function startOrEnsureRunning(state, nowMs) {
        if (state.status === STATUS_RUNNING) {
            return state;
        }
        if (state.status === STATUS_PAUSED) {
            return state;
        }
        if (state.status === STATUS_COMPLETED) {
            return state;
        }
        return {
            status: STATUS_RUNNING,
            accumulated_seconds: 0,
            running_since_ms: nowMs,
        };
    }

    function pauseState(state, nowMs) {
        if (state.status !== STATUS_RUNNING || state.running_since_ms == null) {
            return state;
        }
        var segment = Math.max(
            0,
            Math.floor((nowMs - state.running_since_ms) / 1000)
        );
        return {
            status: STATUS_PAUSED,
            accumulated_seconds: state.accumulated_seconds + segment,
            running_since_ms: null,
        };
    }

    function resumeState(state, nowMs) {
        if (state.status !== STATUS_PAUSED) {
            return state;
        }
        return {
            status: STATUS_RUNNING,
            accumulated_seconds: state.accumulated_seconds,
            running_since_ms: nowMs,
        };
    }

    function finalizeState(state, nowMs) {
        if (state.status === STATUS_COMPLETED) {
            return state;
        }
        var frozen =
            state.status === STATUS_RUNNING
                ? pauseState(state, nowMs)
                : state;
        return {
            status: STATUS_COMPLETED,
            accumulated_seconds: frozen.accumulated_seconds || 0,
            running_since_ms: null,
        };
    }

    function updatePausedUi(isPaused, toggle, statusLabel) {
        if (toggle) {
            toggle.textContent = isPaused
                ? "Resume Study Session"
                : "Pause Study Session";
            toggle.setAttribute(
                "aria-pressed",
                isPaused ? "true" : "false"
            );
        }
        if (statusLabel) {
            statusLabel.hidden = !isPaused;
        }
    }

    function initTimer() {
        var display = document.querySelector("[data-session-timer]");
        if (!display) {
            return;
        }
        var missionId = display.dataset.missionId || "session";
        var toggle = document.querySelector("[data-session-pause-toggle]");
        var statusLabel = document.querySelector("[data-session-paused-label]");
        var finishLink = document.querySelector("[data-session-finish]");

        var state = loadState(missionId);
        var now = Date.now();
        if (
            state.status === STATUS_NOT_STARTED ||
            state.status === STATUS_COMPLETED
        ) {
            state = startOrEnsureRunning(defaultState(), now);
            saveState(missionId, state);
        }

        function render() {
            var seconds = elapsedSeconds(state, Date.now());
            display.textContent = formatElapsed(seconds);
            updatePausedUi(state.status === STATUS_PAUSED, toggle, statusLabel);
        }

        render();
        window.setInterval(function () {
            if (state.status === STATUS_RUNNING) {
                render();
            }
        }, 1000);

        if (toggle) {
            toggle.addEventListener("click", function () {
                var t = Date.now();
                if (state.status === STATUS_RUNNING) {
                    state = pauseState(state, t);
                } else if (state.status === STATUS_PAUSED) {
                    state = resumeState(state, t);
                }
                saveState(missionId, state);
                render();
            });
        }

        if (finishLink) {
            finishLink.addEventListener("click", function () {
                var t = Date.now();
                state = finalizeState(state, t);
                saveState(missionId, state);
                window.localStorage.setItem(
                    finalizedStorageKey(missionId),
                    String(state.accumulated_seconds)
                );
            });
        }
    }

    function initActivityChecklist() {
        var items = document.querySelectorAll("[data-session-activity]");
        items.forEach(function (checkbox) {
            var key =
                "kwalitec.studySession.activity." +
                (checkbox.dataset.missionId || "session") +
                "." +
                (checkbox.dataset.activityIndex || "0");
            var saved = window.sessionStorage.getItem(key);
            if (saved === "1") {
                checkbox.checked = true;
            }
            checkbox.addEventListener("change", function () {
                window.sessionStorage.setItem(
                    key,
                    checkbox.checked ? "1" : "0"
                );
            });
        });
    }

    function initDurationPrefill() {
        var field = document.querySelector("[data-session-duration-prefill]");
        if (!field) {
            return;
        }
        if (field.value) {
            return;
        }
        var missionId = field.dataset.missionId || "session";
        var raw =
            window.localStorage.getItem(finalizedStorageKey(missionId)) ||
            "";
        var activeSeconds = Number(raw);
        if (!activeSeconds || activeSeconds <= 0) {
            var live = loadState(missionId);
            activeSeconds = elapsedSeconds(live, Date.now());
        }
        if (activeSeconds <= 0) {
            return;
        }
        var minutes = Math.max(1, Math.ceil(activeSeconds / 60));
        field.value = String(minutes);
    }

    function init() {
        initTimer();
        initActivityChecklist();
        initDurationPrefill();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
