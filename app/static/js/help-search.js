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
        var input = document.querySelector('[data-help-search]');
        var box = document.querySelector('[data-help-topics]');
        if (!input || !box) return;
        var topics = box.querySelectorAll('[data-help-topic]');
        var empty = document.querySelector('[data-help-search-empty]');
        input.addEventListener('input', function () {
            var q = input.value.trim().toLowerCase();
            var visible = 0;
            for (var i = 0; i < topics.length; i++) {
                var hit = q === '' || (topics[i].getAttribute('data-help-topic') || '').indexOf(q) !== -1;
                topics[i].hidden = !hit;
                if (hit) visible += 1;
            }
            if (empty) empty.hidden = visible !== 0;
        });
    });
})();
