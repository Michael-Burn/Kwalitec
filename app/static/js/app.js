(function () {
    'use strict';

    // ── Sidebar ──────────────────────────────────────────────────────────
    var sidebar = document.querySelector('.sidebar');
    var toggle = document.querySelector('[data-sidebar-toggle]');
    var backdrop = document.querySelector('[data-sidebar-close]');

    if (sidebar && toggle) {
        function openSidebar() {
            sidebar.classList.add('is-open');
            if (backdrop) backdrop.classList.add('is-visible');
            document.body.style.overflow = 'hidden';
        }

        function closeSidebar() {
            sidebar.classList.remove('is-open');
            if (backdrop) backdrop.classList.remove('is-visible');
            document.body.style.overflow = '';
        }

        function isSidebarOpen() {
            return sidebar.classList.contains('is-open');
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

    // ── Welcome modal (Capability 4.4) ────────────────────────────────────
    var welcome = document.getElementById('welcome-modal');
    if (!welcome) {
        return;
    }

    document.body.classList.add('welcome-open');

    function dismissWelcome(thenHref) {
        var form = document.getElementById('welcome-dismiss-form');
        if (!form) {
            welcome.remove();
            document.body.classList.remove('welcome-open');
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
        if (e.key === 'Escape' && document.getElementById('welcome-modal')) {
            dismissWelcome(null);
        }
    });
})();
