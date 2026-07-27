/**
 * Curriculum Studio document upload — Founder PDF workflow.
 * Generic over document kinds from the type registry (no CMP/Syllabus hardcoding).
 */
(function () {
  "use strict";

  function csrfToken() {
    var meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") || "" : "";
  }

  function formatBytes(bytes) {
    var n = Number(bytes) || 0;
    if (n < 1024) return n + " B";
    if (n < 1024 * 1024) return (n / 1024).toFixed(1) + " KB";
    return (n / (1024 * 1024)).toFixed(1) + " MB";
  }

  function formatTimestamp(iso) {
    if (!iso) return "";
    return String(iso).replace("T", " ").slice(0, 16);
  }

  function showToast(message, tone) {
    var live = document.querySelector("[data-doc-upload-live]");
    if (live) live.textContent = message || "";
    var existing = document.querySelector(".doc-upload-toast");
    if (existing) existing.remove();
    var el = document.createElement("div");
    el.className = "doc-upload-toast doc-upload-toast--" + (tone || "info");
    el.setAttribute("role", "status");
    el.textContent = message;
    document.body.appendChild(el);
    window.setTimeout(function () {
      el.remove();
    }, 4200);
  }

  function updateCtaBadge(root, ctaState) {
    var badge = root.querySelector("[data-doc-cta-badge]");
    if (!badge) return;
    var labels = {
      upload: "Upload Documents",
      replace: "Replace Documents",
      uploaded: "Documents Uploaded",
    };
    badge.textContent = labels[ctaState] || labels.upload;
    root.setAttribute("data-cta-state", ctaState || "upload");
  }

  function updateProcessingStages(root, documents) {
    var stages = root.querySelectorAll("[data-doc-processing-stages] [data-stage]");
    var present = {};
    var order = [
      "queued",
      "verified",
      "extracted",
      "normalized",
      "parsed",
      "mapped",
      "graph_built",
      "ready_for_embeddings",
      "ready",
    ];
    (documents || []).forEach(function (doc) {
      var stage = doc.processing_stage || "";
      if (stage === "ready") stage = "ready_for_embeddings";
      if (stage === "processing") stage = "queued";
      present[stage] = true;
      var idx = order.indexOf(stage);
      for (var i = 0; i <= idx; i += 1) present[order[i]] = true;
      // Founder strip skips normalized — mark parsed when normalized reached.
      if (stage === "normalized") present.parsed = true;
    });
    stages.forEach(function (li) {
      var key = li.getAttribute("data-stage");
      li.classList.toggle("is-complete", !!present[key]);
      li.classList.toggle("is-failed", false);
    });
    (documents || []).forEach(function (doc) {
      if (doc.processing_stage === "failed") {
        stages.forEach(function (li) {
          li.classList.add("is-failed");
        });
      }
    });
  }

  function renderPipelineJobs(root, jobs) {
    var host = root.querySelector("[data-doc-pipeline-jobs]");
    if (!host) return;
    host.innerHTML = "";
    (jobs || []).forEach(function (job) {
      var article = document.createElement("article");
      article.className = "doc-pipeline-job";
      article.setAttribute("data-pipeline-job", "");
      article.setAttribute("data-document-id", String(job.document_id));
      article.setAttribute("data-job-id", job.job_id);

      var header = document.createElement("header");
      header.className = "doc-pipeline-job-header";
      header.innerHTML =
        "<strong>Document " +
        job.document_id +
        "</strong> <span data-job-status>" +
        (job.status_label || job.status) +
        "</span>";
      article.appendChild(header);

      if (job.last_error) {
        var err = document.createElement("p");
        err.className = "text-danger mb-2";
        err.setAttribute("data-job-error", "");
        err.textContent = job.last_error;
        article.appendChild(err);
      }

      var list = document.createElement("ul");
      list.className = "doc-pipeline-events list-unstyled mb-2";
      var events = (job.events || []).slice(-6);
      events.forEach(function (event) {
        var li = document.createElement("li");
        li.className = "doc-pipeline-event";
        var parts = [event.stage_label || event.stage, event.status];
        if (event.duration_ms != null) parts.push(event.duration_ms + " ms");
        if (event.error_message) parts.push(event.error_message);
        li.textContent = parts.join(" · ");
        list.appendChild(li);
      });
      article.appendChild(list);

      var actions = document.createElement("div");
      actions.className = "doc-pipeline-actions";
      if (job.can_retry) {
        var retryBtn = document.createElement("button");
        retryBtn.type = "button";
        retryBtn.className = "btn btn-outline-secondary btn-sm";
        retryBtn.setAttribute("data-pipeline-retry", "");
        retryBtn.textContent = "Retry";
        actions.appendChild(retryBtn);
      }
      if (job.can_cancel) {
        var cancelBtn = document.createElement("button");
        cancelBtn.type = "button";
        cancelBtn.className = "btn btn-outline-danger btn-sm";
        cancelBtn.setAttribute("data-pipeline-cancel", "");
        cancelBtn.textContent = "Cancel";
        actions.appendChild(cancelBtn);
      }
      article.appendChild(actions);
      host.appendChild(article);
    });
  }

  function applyStatus(root, status) {
    if (!status) return;
    updateCtaBadge(root, status.cta_state);
    updateProcessingStages(root, status.documents);
    renderPipelineJobs(root, status.pipeline_jobs);
  }

  function pipelineAction(root, article, action) {
    var workspaceId = root.getAttribute("data-workspace-id");
    var documentId = article.getAttribute("data-document-id");
    if (!documentId) return;
    var url =
      "/console/studio/workspaces/" +
      encodeURIComponent(workspaceId) +
      "/documents/" +
      documentId +
      "/pipeline/" +
      action;
    fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken(),
      },
      body: JSON.stringify({}),
    })
      .then(function (res) {
        return res.json().then(function (body) {
          return { ok: res.ok, body: body };
        });
      })
      .then(function (result) {
        if (result.ok && result.body && result.body.ok) {
          applyStatus(root, result.body.status);
          showToast(result.body.message || "Pipeline updated.", "success");
        } else {
          showToast(
            (result.body && result.body.error) || "Pipeline action failed.",
            "danger"
          );
        }
      })
      .catch(function () {
        showToast("Pipeline action failed.", "danger");
      });
  }

  function applyDocumentToCard(card, doc, workspaceId) {
    if (!doc) return;
    card.setAttribute("data-has-document", "true");
    card.setAttribute("data-document-id", String(doc.document_id));
    var empty = card.querySelector("[data-doc-empty]");
    var meta = card.querySelector("[data-doc-meta]");
    var actions = card.querySelector("[data-doc-actions]");
    if (empty) empty.hidden = true;
    if (meta) meta.hidden = false;
    if (actions) actions.hidden = false;

    var set = function (sel, text) {
      var el = card.querySelector(sel);
      if (el) el.textContent = text;
    };
    set("[data-doc-filename]", doc.filename || "");
    set("[data-doc-version]", "v" + (doc.version_number || 1));
    set("[data-doc-uploaded]", formatTimestamp(doc.uploaded_at));
    set("[data-doc-size]", formatBytes(doc.byte_size));
    set("[data-doc-stage]", doc.processing_label || doc.processing_stage || "");
    set("[data-doc-by]", doc.uploaded_by || "—");

    var download = card.querySelector("[data-doc-download]");
    if (download) {
      download.hidden = false;
      download.href =
        "/console/studio/workspaces/" +
        encodeURIComponent(workspaceId) +
        "/documents/" +
        doc.document_id +
        "/download";
    }
    var removeBtn = card.querySelector("[data-doc-remove]");
    if (removeBtn) removeBtn.hidden = false;
  }

  function setCardError(card, message) {
    var err = card.querySelector("[data-doc-error]");
    var ok = card.querySelector("[data-doc-success]");
    if (ok) {
      ok.hidden = true;
      ok.textContent = "";
    }
    if (err) {
      err.hidden = !message;
      err.textContent = message || "";
    }
  }

  function setCardSuccess(card, message) {
    var err = card.querySelector("[data-doc-error]");
    var ok = card.querySelector("[data-doc-success]");
    if (err) {
      err.hidden = true;
      err.textContent = "";
    }
    if (ok) {
      ok.hidden = !message;
      ok.textContent = message || "";
    }
  }

  function setProgress(card, percent, label) {
    var wrap = card.querySelector("[data-doc-progress]");
    var bar = card.querySelector("[data-doc-progress-bar]");
    var text = card.querySelector("[data-doc-progress-label]");
    var track = wrap ? wrap.querySelector("[role='progressbar']") : null;
    if (!wrap) return;
    wrap.hidden = percent == null;
    if (percent == null) return;
    var value = Math.max(0, Math.min(100, percent));
    if (bar) bar.style.width = value + "%";
    if (track) track.setAttribute("aria-valuenow", String(value));
    if (text) text.textContent = label || "Uploading…";
  }

  function uploadFile(root, card, file) {
    var kind = card.getAttribute("data-doc-kind");
    var workspaceId = root.getAttribute("data-workspace-id");
    var uploadUrl = root.getAttribute("data-upload-url");
    var documentId = card.getAttribute("data-document-id");
    var hasDoc = card.getAttribute("data-has-document") === "true";

    if (!file) return;
    if (file.type && file.type.indexOf("pdf") === -1 && !/\.pdf$/i.test(file.name)) {
      setCardError(card, "Only PDF documents are accepted.");
      showToast("Only PDF documents are accepted.", "danger");
      return;
    }

    var form = new FormData();
    form.append("kind", kind);
    form.append("file", file);
    form.append("csrf_token", csrfToken());

    var url = uploadUrl;
    if (hasDoc && documentId) {
      url =
        "/console/studio/workspaces/" +
        encodeURIComponent(workspaceId) +
        "/documents/" +
        documentId +
        "/replace";
    }

    setCardError(card, "");
    setProgress(card, 15, "Uploading…");

    var xhr = new XMLHttpRequest();
    xhr.open("POST", url);
    xhr.setRequestHeader("X-CSRFToken", csrfToken());
    xhr.upload.addEventListener("progress", function (evt) {
      if (!evt.lengthComputable) return;
      var pct = Math.round((evt.loaded / evt.total) * 90);
      setProgress(card, pct, "Uploading… " + pct + "%");
    });
    xhr.addEventListener("load", function () {
      var payload = {};
      try {
        payload = JSON.parse(xhr.responseText || "{}");
      } catch (e) {
        payload = {};
      }
      if (xhr.status >= 200 && xhr.status < 300 && payload.ok) {
        setProgress(card, 100, "Uploaded");
        applyDocumentToCard(card, payload.document, workspaceId);
        if (payload.status) {
          applyStatus(root, payload.status);
        }
        setCardSuccess(card, payload.message || "Document uploaded successfully.");
        showToast(payload.message || "Document uploaded successfully.", "success");
        window.setTimeout(function () {
          setProgress(card, null);
        }, 600);
      } else {
        setProgress(card, null);
        var msg =
          (payload && payload.error) ||
          "Upload failed. Please try again.";
        setCardError(card, msg);
        showToast(msg, "danger");
      }
    });
    xhr.addEventListener("error", function () {
      setProgress(card, null);
      var msg = "Upload failed. Check your connection, then try again.";
      setCardError(card, msg);
      showToast(msg, "danger");
    });
    xhr.send(form);
  }

  function removeDocument(root, card) {
    var workspaceId = root.getAttribute("data-workspace-id");
    var documentId = card.getAttribute("data-document-id");
    if (!documentId) return;
    if (!window.confirm("Remove this document from the active workspace?")) return;

    var url =
      "/console/studio/workspaces/" +
      encodeURIComponent(workspaceId) +
      "/documents/" +
      documentId;
    fetch(url, {
      method: "DELETE",
      headers: {
        "X-CSRFToken": csrfToken(),
      },
    })
      .then(function (res) {
        return res.json().then(function (body) {
          return { ok: res.ok, body: body };
        });
      })
      .then(function (result) {
        if (!result.ok || !result.body.ok) {
          var msg =
            (result.body && result.body.error) ||
            "Could not remove document.";
          setCardError(card, msg);
          showToast(msg, "danger");
          return;
        }
        card.setAttribute("data-has-document", "false");
        card.removeAttribute("data-document-id");
        var empty = card.querySelector("[data-doc-empty]");
        var meta = card.querySelector("[data-doc-meta]");
        var actions = card.querySelector("[data-doc-actions]");
        if (empty) empty.hidden = false;
        if (meta) meta.hidden = true;
        if (actions) actions.hidden = true;
        if (result.body.status) {
          applyStatus(root, result.body.status);
        }
        setCardSuccess(card, result.body.message || "Document removed.");
        showToast(result.body.message || "Document removed.", "success");
      })
      .catch(function () {
        var msg = "Could not remove document. Please try again.";
        setCardError(card, msg);
        showToast(msg, "danger");
      });
  }

  function bindCard(root, card) {
    var input = card.querySelector("[data-doc-file-input]");
    var dropzone = card.querySelector("[data-doc-dropzone]");
    var removeBtn = card.querySelector("[data-doc-remove]");

    if (input) {
      input.addEventListener("change", function () {
        if (input.files && input.files[0]) {
          uploadFile(root, card, input.files[0]);
          input.value = "";
        }
      });
    }

    if (dropzone) {
      ["dragenter", "dragover"].forEach(function (evtName) {
        dropzone.addEventListener(evtName, function (evt) {
          evt.preventDefault();
          evt.stopPropagation();
          dropzone.classList.add("is-dragover");
        });
      });
      ["dragleave", "drop"].forEach(function (evtName) {
        dropzone.addEventListener(evtName, function (evt) {
          evt.preventDefault();
          evt.stopPropagation();
          dropzone.classList.remove("is-dragover");
        });
      });
      dropzone.addEventListener("drop", function (evt) {
        var files = evt.dataTransfer && evt.dataTransfer.files;
        if (files && files[0]) uploadFile(root, card, files[0]);
      });
      dropzone.addEventListener("keydown", function (evt) {
        if (evt.key === "Enter" || evt.key === " ") {
          evt.preventDefault();
          if (input) input.click();
        }
      });
    }

    if (removeBtn) {
      removeBtn.addEventListener("click", function () {
        removeDocument(root, card);
      });
    }
  }

  function init() {
    var root = document.querySelector("[data-document-upload]");
    if (!root) return;
    root.querySelectorAll(".doc-upload-card").forEach(function (card) {
      bindCard(root, card);
    });
    root.addEventListener("click", function (evt) {
      var retry = evt.target.closest("[data-pipeline-retry]");
      var cancel = evt.target.closest("[data-pipeline-cancel]");
      if (!retry && !cancel) return;
      var article = evt.target.closest("[data-pipeline-job]");
      if (!article) return;
      pipelineAction(root, article, retry ? "retry" : "cancel");
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
