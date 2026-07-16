// Mission-related JavaScript functionality
(function () {
    "use strict";

    function getCsrfToken() {
        const meta = document.querySelector('meta[name="csrf-token"]');
        if (meta) {
            return meta.getAttribute("content");
        }
        const input = document.querySelector('input[name="csrf_token"]');
        if (input) {
            return input.value;
        }
        return null;
    }

    function authHeaders() {
        const headers = {
            "Content-Type": "application/json",
        };
        const csrfToken = getCsrfToken();
        if (csrfToken) {
            headers["X-CSRFToken"] = csrfToken;
        }
        return headers;
    }

    function getTaskToggles() {
        return Array.from(document.querySelectorAll(".task-toggle"));
    }

    function allTasksComplete() {
        const toggles = getTaskToggles();
        return toggles.length === 0 || toggles.every((t) => t.checked);
    }

    function updateProgress() {
        const allToggles = getTaskToggles();
        const total = allToggles.length;
        const completed = allToggles.filter((t) => t.checked).length;
        const percentage = total > 0 ? Math.round((completed / total) * 100) : 100;

        const progressBar = document.querySelector(".mission-hero-progress-bar .progress-bar");
        const progressText = document.querySelector(".mission-hero-progress-bar .fw-semibold");

        if (progressBar) {
            progressBar.style.width = percentage + "%";
            progressBar.setAttribute("aria-valuenow", percentage);
        }

        if (progressText) {
            progressText.textContent = percentage + "%";
        }

        const progressWrap = document.querySelector(".mission-hero-progress-bar .progress");
        if (progressWrap) {
            progressWrap.setAttribute("aria-valuenow", percentage);
        }

        syncMarkCompleteButton();
    }

    function syncMarkCompleteButton() {
        const button = document.querySelector(".btn-mark-complete");
        if (!button || button.dataset.sessionComplete === "true") {
            return;
        }

        const ready = allTasksComplete();
        button.disabled = !ready;
        button.setAttribute("aria-disabled", ready ? "false" : "true");
        button.title = ready
            ? "Mark this study session complete"
            : "Mark every mission point done before completing the session";
    }

    function markTaskLabel(taskId, completed) {
        const label = document.querySelector(`label[for="task-${taskId}"]`);
        if (!label) {
            return;
        }
        if (completed) {
            label.classList.add("text-decoration-line-through", "text-secondary");
        } else {
            label.classList.remove("text-decoration-line-through", "text-secondary");
        }
        const item = label.closest(".task-item");
        if (item) {
            item.classList.toggle("completed", completed);
        }
    }

    function bindTaskToggles() {
        const taskToggles = getTaskToggles();
        taskToggles.forEach((toggle) => {
            toggle.addEventListener("change", function () {
                const taskId = this.dataset.taskId;
                const completed = this.checked;

                // Keep the complete button in sync immediately; revert on failure.
                updateProgress();

                fetch(`/missions/tasks/${taskId}/toggle`, {
                    method: "POST",
                    headers: authHeaders(),
                    body: JSON.stringify({ completed: completed }),
                })
                    .then((response) => response.json())
                    .then((data) => {
                        if (data.success) {
                            markTaskLabel(taskId, completed);
                            updateProgress();
                        } else {
                            this.checked = !completed;
                            updateProgress();
                            console.error("Failed to update task:", data.error);
                        }
                    })
                    .catch((error) => {
                        this.checked = !completed;
                        updateProgress();
                        console.error("Error updating task:", error);
                    });
            });
        });
    }

    function bindMarkComplete() {
        const button = document.querySelector(".btn-mark-complete");
        if (!button) {
            return;
        }

        button.addEventListener("click", function () {
            if (this.dataset.sessionComplete === "true" || this.disabled) {
                return;
            }

            if (!allTasksComplete()) {
                window.alert(
                    "Mark every mission point done before completing the session."
                );
                syncMarkCompleteButton();
                return;
            }

            const missionId = this.dataset.missionId;
            if (!missionId) {
                return;
            }

            // PTP-002: Mark Complete is compatibility-only — never write
            // educational state here. Navigate to Practice Outcome Capture.
            window.location.href = `/missions/${missionId}/session/finish`;
        });
    }

    function init() {
        bindTaskToggles();
        bindMarkComplete();
        updateProgress();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
