(function () {
    "use strict";

    var STORAGE_KEY = "kwalitec-appearance";
    var VALID = { light: true, dark: true, system: true };

    function getStoredAppearance() {
        try {
            var value = window.localStorage.getItem(STORAGE_KEY);
            if (value && VALID[value]) {
                return value;
            }
        } catch (_err) {

        }
        return "system";
    }

    function storeAppearance(appearance) {
        try {
            window.localStorage.setItem(STORAGE_KEY, appearance);
        } catch (_err) {

        }
    }

    function systemPrefersDark() {
        return (
            window.matchMedia &&
            window.matchMedia("(prefers-color-scheme: dark)").matches
        );
    }

    function resolveTheme(appearance) {
        if (appearance === "light" || appearance === "dark") {
            return appearance;
        }
        return systemPrefersDark() ? "dark" : "light";
    }

    function applyAppearance(appearance) {
        var resolved = resolveTheme(appearance);
        var root = document.documentElement;
        root.setAttribute("data-appearance", appearance);
        root.setAttribute("data-theme", resolved);
        root.setAttribute("data-bs-theme", resolved);
        root.style.colorScheme = resolved;
    }

    function setAppearance(appearance) {
        if (!VALID[appearance]) {
            appearance = "system";
        }
        storeAppearance(appearance);
        applyAppearance(appearance);
        syncControls(appearance);
    }

    function syncControls(appearance) {
        var controls = document.querySelectorAll(
            "[data-appearance-select], [data-appearance-option]"
        );
        for (var i = 0; i < controls.length; i++) {
            var el = controls[i];
            if (el.tagName === "SELECT") {
                el.value = appearance;
                continue;
            }
            var option = el.getAttribute("data-appearance-option");
            if (!option) {
                continue;
            }
            var active = option === appearance;
            el.classList.toggle("is-active", active);
            el.setAttribute("aria-pressed", active ? "true" : "false");
        }
    }

    var current = getStoredAppearance();
    applyAppearance(current);

    function onReady(fn) {
        if (document.readyState === "loading") {
            document.addEventListener("DOMContentLoaded", fn);
        } else {
            fn();
        }
    }

    onReady(function () {
        syncControls(getStoredAppearance());

        document.addEventListener("change", function (event) {
            var target = event.target;
            if (
                target &&
                target.matches &&
                target.matches("[data-appearance-select]")
            ) {
                setAppearance(target.value);
            }
        });

        document.addEventListener("click", function (event) {
            var btn = event.target.closest
                ? event.target.closest("[data-appearance-option]")
                : null;
            if (!btn) {
                return;
            }
            var option = btn.getAttribute("data-appearance-option");
            if (option && VALID[option]) {
                setAppearance(option);
            }
        });

        if (window.matchMedia) {
            var mq = window.matchMedia("(prefers-color-scheme: dark)");
            var onChange = function () {
                if (getStoredAppearance() === "system") {
                    applyAppearance("system");
                }
            };
            if (typeof mq.addEventListener === "function") {
                mq.addEventListener("change", onChange);
            } else if (typeof mq.addListener === "function") {
                mq.addListener(onChange);
            }
        }
    });

    window.KwalitecTheme = {
        getAppearance: getStoredAppearance,
        setAppearance: setAppearance,
        resolveTheme: resolveTheme,
    };
})();
