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

    function updateProgress() {
        const allToggles = document.querySelectorAll(".task-toggle");
        const total = allToggles.length;
        const completed = Array.from(allToggles).filter((t) => t.checked).length;
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
        const taskToggles = document.querySelectorAll(".task-toggle");
        taskToggles.forEach((toggle) => {
            toggle.addEventListener("change", function () {
                const taskId = this.dataset.taskId;
                const completed = this.checked;

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
            const missionId = this.dataset.missionId;
            if (!missionId) {
                return;
            }

            this.disabled = true;
            const originalLabel = this.innerHTML;
            this.innerHTML = "Saving…";

            fetch(`/missions/${missionId}/complete`, {
                method: "POST",
                headers: authHeaders(),
                body: JSON.stringify({}),
            })
                .then((response) => response.json().then((data) => ({ ok: response.ok, data })))
                .then(({ ok, data }) => {
                    if (ok && data.success) {
                        document.querySelectorAll(".task-toggle").forEach((toggle) => {
                            toggle.checked = true;
                            markTaskLabel(toggle.dataset.taskId, true);
                        });
                        updateProgress();

                        const badge = document.querySelector(".mission-hero-header .badge");
                        if (badge) {
                            badge.textContent = "Completed";
                            badge.className =
                                "badge rounded-pill fs-6 px-3 py-2 text-bg-success";
                        }

                        window.location.href = data.redirect_url || "/";
                        return;
                    }

                    this.disabled = false;
                    this.innerHTML = originalLabel;
                    console.error("Failed to complete mission:", data && data.error);
                    window.alert((data && data.error) || "Could not complete mission.");
                })
                .catch((error) => {
                    this.disabled = false;
                    this.innerHTML = originalLabel;
                    console.error("Error completing mission:", error);
                    window.alert("Could not complete mission. Please try again.");
                });
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
