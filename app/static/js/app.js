(function () {
    'use strict';

    var sidebar = document.querySelector('.sidebar');
    var toggle = document.querySelector('[data-sidebar-toggle]');
    var backdrop = document.querySelector('[data-sidebar-close]');

    if (!sidebar || !toggle) {
        return;
    }

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

    // Close sidebar on Escape
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && isSidebarOpen()) {
            closeSidebar();
        }
    });

    // Close sidebar when window is resized beyond mobile breakpoint
    var resizeTimer;
    window.addEventListener('resize', function () {
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(function () {
            if (window.innerWidth >= 992 && isSidebarOpen()) {
                closeSidebar();
            }
        }, 150);
    });
})();