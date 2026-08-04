(function () {
    'use strict';
    function ready(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }

    function showFallback(message) {
        var fallback = document.getElementById('confirm-modal-fallback');
        if (fallback) {
            fallback.hidden = false;
            fallback.classList.remove('visually-hidden');
            fallback.textContent = message;
        }
        try {
            window.alert(message);
        } catch (err) {
            /* ignore */
        }
    }

    ready(function () {
        var el = document.getElementById('confirm-modal');
        if (!el) return;

        // PX-B-023: visible failure if Bootstrap Modal is unavailable.
        if (!window.bootstrap || !window.bootstrap.Modal) {
            document.addEventListener('click', function (event) {
                var trigger = event.target.closest && event.target.closest('[data-confirm-trigger]');
                if (!trigger) return;
                event.preventDefault();
                showFallback(
                    'Confirmation dialog is unavailable. Reload the page, or cancel this action and try again.'
                );
            });
            return;
        }

        var title = document.getElementById('confirm-modal-title');
        var body = document.getElementById('confirm-modal-body');
        var btn = document.getElementById('confirm-modal-confirm');
        var modal = new window.bootstrap.Modal(el);
        var form = null;
        document.addEventListener('click', function (event) {
            var trigger = event.target.closest && event.target.closest('[data-confirm-trigger]');
            if (!trigger) return;
            event.preventDefault();
            form = trigger.closest('form');
            title.textContent = trigger.getAttribute('data-confirm-title') || 'Confirm';
            body.textContent = trigger.getAttribute('data-confirm-body') || '';
            btn.textContent = trigger.getAttribute('data-confirm-label') || 'Confirm';
            btn.className = 'btn ' + (trigger.getAttribute('data-confirm-variant') === 'danger' ? 'btn-danger' : 'btn-primary');
            try {
                modal.show();
            } catch (err) {
                showFallback(
                    'Confirmation dialog failed to open. Reload the page, or cancel this action and try again.'
                );
            }
        });
        btn.addEventListener('click', function () {
            modal.hide();
            if (form) form.submit();
        });
    });
})();
