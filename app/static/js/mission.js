// Mission-related JavaScript functionality
(function () {
    "use strict";

    // Initialize task toggle handlers
    const taskToggles = document.querySelectorAll(".task-toggle");

    if (!taskToggles.length) {
        return;
    }

    // Get CSRF token from meta tag or hidden input
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

    // Update progress bar and percentage display
    function updateProgress() {
        const allToggles = document.querySelectorAll(".task-toggle");
        const total = allToggles.length;
        const completed = Array.from(allToggles).filter(t => t.checked).length;
        const percentage = total > 0 ? Math.round((completed / total) * 100) : 100;

        const progressBar = document.querySelector(".progress-bar");
        const progressText = document.querySelector(".fw-semibold");

        if (progressBar) {
            progressBar.style.width = percentage + "%";
            progressBar.setAttribute("aria-valuenow", percentage);
        }

        if (progressText) {
            progressText.textContent = percentage + "%";
        }
    }

    taskToggles.forEach(toggle => {
        toggle.addEventListener("change", function () {
            const taskId = this.dataset.taskId;
            const completed = this.checked;
            const csrfToken = getCsrfToken();

            const headers = {
                "Content-Type": "application/json",
            };

            if (csrfToken) {
                headers["X-CSRFToken"] = csrfToken;
            }

            // Send request to mark task complete
            fetch(`/missions/tasks/${taskId}/toggle`, {
                method: "POST",
                headers: headers,
                body: JSON.stringify({ completed: completed })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update the label styling
                    const label = document.querySelector(`label[for="task-${taskId}"]`);
                    if (label) {
                        if (completed) {
                            label.classList.add("text-decoration-line-through", "text-secondary");
                        } else {
                            label.classList.remove("text-decoration-line-through", "text-secondary");
                        }
                    }

                    // Update progress bar dynamically
                    updateProgress();

                    // Check if all tasks are complete
                    if (data.mission.all_tasks_complete) {
                        // Redirect to mission review page
                        window.location.href = `/missions/review/${data.mission.id}`;
                    }
                } else {
                    // Revert the checkbox if the request failed
                    this.checked = !completed;
                    updateProgress();
                    console.error("Failed to update task:", data.error);
                }
            })
            .catch(error => {
                // Revert the checkbox if there was a network error
                this.checked = !completed;
                updateProgress();
                console.error("Error updating task:", error);
            });
        });
    });
})();