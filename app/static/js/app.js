var FOCUSABLE_SELECTOR = [
    'a[href]',
    'button:not([disabled])',
    'textarea:not([disabled])',
    'input:not([disabled]):not([type="hidden"])',
    'select:not([disabled])',
    '[tabindex]:not([tabindex="-1"])'
].join(',');

function getFocusable(container) {
    return Array.prototype.slice
        .call(container.querySelectorAll(FOCUSABLE_SELECTOR))
        .filter(function (el) {
            return el.offsetParent !== null || el === document.activeElement;
        });
}

// Traps Tab/Shift+Tab within `container` while `isActive()` returns true.
// Returns a keydown handler suitable for addEventListener('keydown', ...).
function makeFocusTrap(container, isActive) {
    return function (e) {
        if (e.key !== 'Tab' || !isActive()) {
            return;
        }
        var focusable = getFocusable(container);
        if (focusable.length === 0) {
            e.preventDefault();
            container.focus();
            return;
        }
        var first = focusable[0];
        var last = focusable[focusable.length - 1];
        if (e.shiftKey && document.activeElement === first) {
            e.preventDefault();
            last.focus();
        } else if (!e.shiftKey && document.activeElement === last) {
            e.preventDefault();
            first.focus();
        } else if (focusable.indexOf(document.activeElement) === -1) {
            // Focus escaped the container (e.g. via mouse) — pull it back in.
            e.preventDefault();
            first.focus();
        }
    };
}

(function () {
    'use strict';

    var sidebar = document.querySelector('.sidebar');
    var toggle = document.querySelector('[data-sidebar-toggle]');
    var backdrop = document.querySelector('[data-sidebar-close]');

    if (sidebar && toggle) {
        var lastFocusedBeforeDrawer = null;

        function isSidebarOpen() {
            return sidebar.classList.contains('is-open');
        }

        // The drawer is only ever opened via `toggle`, which is hidden at the
        // >=992px breakpoint (see `.d-lg-none` in topnav.html) — so dialog
        // semantics are applied only for the off-canvas (mobile) presentation
        // and never mislabel the always-visible desktop sidebar landmark.
        function openSidebar() {
            lastFocusedBeforeDrawer = document.activeElement;
            sidebar.classList.add('is-open');
            if (backdrop) backdrop.classList.add('is-visible');
            document.body.style.overflow = 'hidden';
            toggle.setAttribute('aria-expanded', 'true');
            if (!sidebar.hasAttribute('tabindex')) {
                sidebar.setAttribute('tabindex', '-1');
            }
            sidebar.setAttribute('role', 'dialog');
            sidebar.setAttribute('aria-modal', 'true');
            sidebar.setAttribute('aria-label', 'Primary navigation');
            var focusable = getFocusable(sidebar);
            if (focusable.length > 0) {
                focusable[0].focus();
            } else {
                sidebar.focus();
            }
        }

        function closeSidebar() {
            sidebar.classList.remove('is-open');
            if (backdrop) backdrop.classList.remove('is-visible');
            document.body.style.overflow = '';
            toggle.setAttribute('aria-expanded', 'false');
            sidebar.removeAttribute('role');
            sidebar.removeAttribute('aria-modal');
            sidebar.removeAttribute('aria-label');
            if (lastFocusedBeforeDrawer && typeof lastFocusedBeforeDrawer.focus === 'function') {
                lastFocusedBeforeDrawer.focus();
            } else {
                toggle.focus();
            }
            lastFocusedBeforeDrawer = null;
        }

        toggle.setAttribute('aria-expanded', 'false');
        if (sidebar.id) {
            toggle.setAttribute('aria-controls', sidebar.id);
        }

        toggle.addEventListener('click', function () {
            if (isSidebarOpen()) {
                closeSidebar();
            } else {
                openSidebar();
            }
        });

        if (backdrop) {
            backdrop.addEventListener('click', function () {
                closeSidebar();
            });
        }

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && isSidebarOpen()) {
                closeSidebar();
                return;
            }
            if (isSidebarOpen()) {
                makeFocusTrap(sidebar, isSidebarOpen)(e);
            }
        });

        var resizeTimer;
        window.addEventListener('resize', function () {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(function () {
                if (window.innerWidth >= 992 && isSidebarOpen()) {
                    closeSidebar();
                }
            }, 150);
        });
    }

    var welcome = document.getElementById('welcome-modal');
    if (!welcome) {
        return;
    }

    document.body.classList.add('welcome-open');

    var welcomeCard = welcome.querySelector('.welcome-modal-card');
    var focusBeforeWelcome = document.activeElement;

    // B4 (PX-003): focus entry — move focus into the dialog on open. The
    // card itself (not a specific control) is the WAI-ARIA APG-recommended
    // target when a dialog's accessible name/description already cover its
    // content, so screen readers announce title + description immediately.
    if (welcomeCard) {
        welcomeCard.focus();
    }

    function restoreFocusAfterWelcome() {
        if (focusBeforeWelcome && document.contains(focusBeforeWelcome) && typeof focusBeforeWelcome.focus === 'function') {
            focusBeforeWelcome.focus();
        } else {
            // Falls back across every shell this dialog can render on:
            // main-content (legacy layouts/base.html), student-main/
            // session-main (student/session shells) — all share role="main".
            var main = document.getElementById('main-content') || document.querySelector('[role="main"]');
            if (main) {
                main.focus();
            }
        }
    }

    function dismissWelcome(thenHref) {
        var form = document.getElementById('welcome-dismiss-form');
        if (!form) {
            welcome.remove();
            document.body.classList.remove('welcome-open');
            restoreFocusAfterWelcome();
            if (thenHref) {
                window.location.href = thenHref;
            }
            return;
        }
        if (thenHref) {
            var next = document.createElement('input');
            next.type = 'hidden';
            next.name = 'next';
            next.value = thenHref;
            form.appendChild(next);
        }
        // Submitting navigates the page (full reload back to the same
        // canonical surface), which is itself a valid focus return per
        // WCAG 2.4.3 — the next document starts with a clean focus order.
        form.submit();
    }

    welcome.addEventListener('click', function (event) {
        var target = event.target.closest('[data-welcome-dismiss]');
        if (!target) {
            return;
        }
        event.preventDefault();
        var href = target.getAttribute('data-welcome-href') || target.getAttribute('href');
        dismissWelcome(href || null);
    });

    document.addEventListener('keydown', function (e) {
        if (!document.getElementById('welcome-modal')) {
            return;
        }
        if (e.key === 'Escape') {
            dismissWelcome(null);
            return;
        }
        if (welcomeCard) {
            makeFocusTrap(welcomeCard, function () {
                return !!document.getElementById('welcome-modal');
            })(e);
        }
    });
})();
