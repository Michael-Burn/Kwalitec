(function () {
    'use strict';
    function ready(fn) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', fn);
        } else {
            fn();
        }
    }
    ready(function () {
        var el = document.getElementById('confirm-modal');
        if (!el || !window.bootstrap) return;
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
            modal.show();
        });
        btn.addEventListener('click', function () {
            modal.hide();
            if (form) form.submit();
        });
    });
})();
