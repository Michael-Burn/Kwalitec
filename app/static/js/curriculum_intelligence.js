/**
 * Curriculum Intelligence (CIP-002 / CIP-003) Founder workspace tabs.
 * Educational concepts only — no storage keys, vector ids, or model internals.
 */
(function () {
  "use strict";

  function csrfToken() {
    var meta = document.querySelector('meta[name="csrf-token"]');
    return meta ? meta.getAttribute("content") : "";
  }

  function qs(root, sel) {
    return root.querySelector(sel);
  }

  function qsa(root, sel) {
    return Array.prototype.slice.call(root.querySelectorAll(sel));
  }

  function fetchJson(url, options) {
    var opts = options || {};
    opts.headers = opts.headers || {};
    opts.headers.Accept = "application/json";
    if (opts.method && opts.method !== "GET") {
      opts.headers["Content-Type"] = "application/json";
      opts.headers["X-CSRFToken"] = csrfToken();
    }
    return fetch(url, opts).then(function (res) {
      return res.json().then(function (body) {
        if (!res.ok || body.ok === false) {
          throw new Error((body && body.error) || "Request failed");
        }
        return body;
      });
    });
  }

  function pct(value) {
    if (value == null || isNaN(value)) return "—";
    return Math.round(Number(value) * 100) + "%";
  }

  function activateTab(root, name) {
    qsa(root, "[data-cip-tab]").forEach(function (btn) {
      btn.classList.toggle("is-active", btn.getAttribute("data-cip-tab") === name);
    });
    qsa(root, "[data-cip-panel]").forEach(function (panel) {
      var active = panel.getAttribute("data-cip-panel") === name;
      panel.classList.toggle("is-active", active);
      if (active) {
        panel.removeAttribute("hidden");
      } else {
        panel.setAttribute("hidden", "hidden");
      }
    });
  }

  function renderOverview(root, data) {
    var ov = data.overview || {};
    var set = function (sel, val) {
      var el = qs(root, sel);
      if (el) el.textContent = val;
    };
    set("[data-cip-ov-docs]", ov.document_count != null ? ov.document_count : "—");
    set("[data-cip-ov-entities]", ov.entity_count != null ? ov.entity_count : "—");
    set("[data-cip-ov-review]", ov.review_queue_count != null ? ov.review_queue_count : "—");
    set("[data-cip-ov-errors]", ov.validation_errors != null ? ov.validation_errors : "—");
    var badge = qs(root, "[data-cip-overview-badge]");
    if (badge) {
      badge.textContent =
        (ov.review_queue_count || 0) + " awaiting review · " +
        (ov.validation_errors || 0) + " validation errors";
    }
  }

  function renderValidation(root, data) {
    var host = qs(root, "[data-cip-validation-list]");
    if (!host) return;
    var reports = data.reports || [];
    if (!reports.length) {
      host.innerHTML =
        '<p class="text-muted mb-0">No validation reports yet. Run the intelligence pipeline on uploaded documents.</p>';
      return;
    }
    host.innerHTML = reports
      .map(function (r) {
        var issues = (r.issues || [])
          .map(function (i) {
            return (
              '<li class="mb-2"><strong>' +
              escapeHtml(i.severity) +
              "</strong> · " +
              escapeHtml(i.kind) +
              "<br><span>" +
              escapeHtml(i.message) +
              "</span></li>"
            );
          })
          .join("");
        return (
          '<article class="cip-review-card mb-3">' +
          "<header><strong>Document " +
          escapeHtml(String(r.document_id)) +
          "</strong> · " +
          (r.passed ? "Passed" : "Needs attention") +
          " · " +
          escapeHtml(String(r.issue_count)) +
          " issues</header>" +
          "<ul class='list-unstyled mb-0 mt-2'>" +
          (issues || "<li class='text-muted'>No issues</li>") +
          "</ul></article>"
        );
      })
      .join("");
  }

  function renderReview(root, data) {
    var host = qs(root, "[data-cip-review-list]");
    if (!host) return;
    var items = data.items || [];
    if (!items.length) {
      host.innerHTML = '<p class="text-muted mb-0">No entities awaiting review.</p>';
      return;
    }
    var workspaceId = root.getAttribute("data-workspace-id");
    host.innerHTML = items
      .map(function (item) {
        var pages = (item.source_pages || []).join(", ") || "—";
        var evidence = (item.supporting_evidence || [])
          .map(function (e) {
            return (
              "Paragraph " +
              (e.paragraph != null ? e.paragraph : "—") +
              (e.excerpt ? ": " + e.excerpt.slice(0, 120) : "")
            );
          })
          .join("; ");
        return (
          '<article class="cip-review-card mb-3" data-review-entity="' +
          escapeAttr(item.entity_id) +
          '">' +
          "<h3 class='h6 mb-1'>" +
          escapeHtml(item.title) +
          "</h3>" +
          "<p class='mb-1'><strong>Confidence</strong> " +
          escapeHtml(String(item.confidence_percent)) +
          "%</p>" +
          "<p class='mb-1 text-muted'>" +
          escapeHtml(item.confidence_reason || "") +
          "</p>" +
          "<p class='mb-1'><strong>Detected from</strong> document " +
          escapeHtml(String(item.document_id)) +
          " page " +
          escapeHtml(pages) +
          "</p>" +
          (evidence
            ? "<p class='mb-1'><strong>Supporting evidence</strong> " +
              escapeHtml(evidence) +
              "</p>"
            : "") +
          (item.suggested_learning_objective
            ? "<p class='mb-1'><strong>Suggested learning objective</strong> " +
              escapeHtml(item.suggested_learning_objective) +
              "</p>"
            : "") +
          "<p class='mb-2'><strong>Status</strong> " +
          escapeHtml(item.review_status) +
          "</p>" +
          '<div class="cip-review-actions">' +
          '<button type="button" class="btn btn-outline-success btn-sm" data-review-approve>Approve</button> ' +
          '<button type="button" class="btn btn-outline-danger btn-sm" data-review-reject>Reject</button> ' +
          '<button type="button" class="btn btn-outline-secondary btn-sm" data-review-remap>Remap</button> ' +
          '<button type="button" class="btn btn-link btn-sm" data-review-details>Details</button>' +
          "</div></article>"
        );
      })
      .join("");

    qsa(host, "[data-review-approve]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var card = btn.closest("[data-review-entity]");
        var id = card && card.getAttribute("data-review-entity");
        if (!id) return;
        postDecision(root, workspaceId, id, "approve").then(function () {
          return loadReview(root);
        });
      });
    });
    qsa(host, "[data-review-reject]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var card = btn.closest("[data-review-entity]");
        var id = card && card.getAttribute("data-review-entity");
        if (!id) return;
        postDecision(root, workspaceId, id, "reject").then(function () {
          return loadReview(root);
        });
      });
    });
    qsa(host, "[data-review-remap]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var card = btn.closest("[data-review-entity]");
        var id = card && card.getAttribute("data-review-entity");
        if (!id) return;
        var target = window.prompt("Remap to learning objective or entity id:");
        if (!target) return;
        postDecision(root, workspaceId, id, "remap", {
          remap_target_id: target,
        }).then(function () {
          return loadReview(root);
        });
      });
    });
    qsa(host, "[data-review-details]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var card = btn.closest("[data-review-entity]");
        var id = card && card.getAttribute("data-review-entity");
        if (!id) return;
        var input = qs(root, "[data-cip-entity-input]");
        if (input) input.value = id;
        activateTab(root, "entity");
        loadEntity(root, id);
      });
    });
  }

  function entityActionUrl(root, entityId, action) {
    var base = root.getAttribute("data-overview-url") || "";
    // …/intelligence/overview → …/intelligence/entities/<id>/<action>
    var prefix = base.replace(/\/overview\/?$/, "");
    return (
      prefix +
      "/entities/" +
      encodeURIComponent(entityId) +
      (action ? "/" + action : "")
    );
  }

  function postDecision(root, workspaceId, entityId, action, extra) {
    void workspaceId;
    return fetchJson(entityActionUrl(root, entityId, action), {
      method: "POST",
      body: JSON.stringify(extra || {}),
    });
  }

  function renderMetrics(root, data) {
    var m = data.metrics || {};
    var set = function (sel, val) {
      var el = qs(root, sel);
      if (el) el.textContent = val;
    };
    set("[data-cip-met-conf]", pct(m.mean_mapping_confidence));
    set("[data-cip-met-complete]", pct(m.graph_completeness));
    set(
      "[data-cip-met-approvals]",
      m.founder_approvals != null ? m.founder_approvals : "—"
    );
    var host = qs(root, "[data-cip-metrics-docs]");
    if (!host) return;
    var docs = m.documents || [];
    if (!docs.length) {
      host.innerHTML = '<li class="text-muted">No metrics recorded yet.</li>';
      return;
    }
    host.innerHTML = docs
      .map(function (d) {
        return (
          "<li class='mb-2'><strong>Document " +
          escapeHtml(String(d.document_id)) +
          "</strong> · confidence " +
          pct(d.mean_mapping_confidence) +
          " · review " +
          escapeHtml(String(d.entities_requiring_review)) +
          " · entities " +
          escapeHtml(String(d.entity_count)) +
          "</li>"
        );
      })
      .join("");
  }

  function renderGraph(root, data) {
    var nodes = data.nodes || [];
    var edges = data.edges || [];
    var summary = qs(root, "[data-cip-graph-summary]");
    if (summary) {
      summary.textContent =
        nodes.length + " entities · " + edges.length + " relationships";
    }
    var host = qs(root, "[data-cip-graph-nodes]");
    if (!host) return;
    host.innerHTML = nodes
      .slice(0, 40)
      .map(function (n) {
        return (
          "<li class='mb-2'><strong>" +
          escapeHtml(n.title) +
          "</strong> <span class='text-muted'>(" +
          escapeHtml(n.kind) +
          ", " +
          pct(n.confidence) +
          (n.needs_review ? ", needs review" : "") +
          ")</span></li>"
        );
      })
      .join("");
  }

  function renderAudit(root, data) {
    var host = qs(root, "[data-cip-audit-list]");
    if (!host) return;
    var events = data.events || [];
    if (!events.length) {
      host.innerHTML = '<li class="text-muted">No audit events yet.</li>';
      return;
    }
    host.innerHTML = events
      .slice(0, 40)
      .map(function (e) {
        return (
          "<li class='mb-2'><strong>" +
          escapeHtml(e.action) +
          "</strong> · " +
          escapeHtml(e.message) +
          " <span class='text-muted'>" +
          escapeHtml(e.created_at || "") +
          "</span></li>"
        );
      })
      .join("");
  }

  function loadEntity(root, entityId) {
    var host = qs(root, "[data-cip-entity-detail]");
    if (!host || !entityId) return;
    host.innerHTML = '<p class="text-muted mb-0">Loading…</p>';
    var url = entityActionUrl(root, entityId, "");
    fetchJson(url)
      .then(function (body) {
        var e = body.entity || {};
        var conf = e.confidence || {};
        var prov = e.provenance || {};
        var chain = (prov.chain || [])
          .map(function (c) {
            return escapeHtml(c.stage) + " → " + escapeHtml(String(c.ref));
          })
          .join("<br>");
        host.innerHTML =
          "<h3 class='h6'>" +
          escapeHtml(e.title || "") +
          "</h3>" +
          "<p><strong>Kind</strong> " +
          escapeHtml(e.kind || "") +
          "</p>" +
          "<p><strong>Confidence</strong> " +
          pct(conf.score) +
          " — " +
          escapeHtml(conf.reason || "") +
          "</p>" +
          "<p><strong>Review status</strong> " +
          escapeHtml(e.review_status || "") +
          "</p>" +
          "<p><strong>Version</strong> " +
          escapeHtml(e.version_label || "—") +
          "</p>" +
          "<p><strong>Provenance chain</strong><br>" +
          (chain || "—") +
          "</p>";
      })
      .catch(function (err) {
        host.innerHTML =
          '<p class="text-danger mb-0">' + escapeHtml(err.message) + "</p>";
      });
  }

  function loadOverview(root) {
    return fetchJson(root.getAttribute("data-overview-url")).then(function (body) {
      renderOverview(root, body);
    });
  }

  function loadValidation(root) {
    return fetchJson(root.getAttribute("data-validation-url")).then(function (body) {
      renderValidation(root, body);
    });
  }

  function loadReview(root) {
    return fetchJson(root.getAttribute("data-review-url")).then(function (body) {
      renderReview(root, body);
    });
  }

  function loadMetrics(root) {
    return fetchJson(root.getAttribute("data-metrics-url")).then(function (body) {
      renderMetrics(root, body);
    });
  }

  function loadGraph(root) {
    return fetchJson(root.getAttribute("data-graph-url")).then(function (body) {
      renderGraph(root, body);
    });
  }

  function loadAudit(root) {
    return fetchJson(root.getAttribute("data-audit-url")).then(function (body) {
      renderAudit(root, body);
    });
  }

  function renderEmbeddingStatus(root, data) {
    var s = (data && data.status) || {};
    var set = function (sel, val) {
      var el = qs(root, sel);
      if (el) el.textContent = val;
    };
    set("[data-cip-embed-indexed]", s.indexed != null ? s.indexed : "—");
    set("[data-cip-embed-failed]", s.failed != null ? s.failed : "—");
    set("[data-cip-embed-model]", s.model_name || "—");
    set("[data-cip-embed-vectors]", s.vector_count != null ? s.vector_count : "—");
  }

  function bindEntityOpeners(root, host) {
    qsa(host, "[data-cip-open-entity]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-cip-open-entity");
        activateTab(root, "entity");
        var input = qs(root, "[data-cip-entity-input]");
        if (input) input.value = id || "";
        loadEntity(root, id);
      });
    });
  }

  function renderEvidence(root, data) {
    var host = qs(root, "[data-cip-evidence-results]");
    if (!host) return;
    var retrieval = data.retrieval || {};
    var results = retrieval.results || [];
    var diag = retrieval.diagnostics || {};
    if (!results.length) {
      host.innerHTML =
        '<p class="text-muted mb-0">No educational evidence matched this query.</p>';
      return;
    }
    var diagLine =
      "<p class='text-muted small mb-2'>Intent " +
      escapeHtml(retrieval.intent || "") +
      " · profile " +
      escapeHtml(retrieval.profile || "") +
      " · vector hits " +
      (diag.vector_hit_count != null ? diag.vector_hit_count : "—") +
      " · ranked " +
      (diag.ranked_count != null ? diag.ranked_count : results.length) +
      "</p>";
    host.innerHTML =
      diagLine +
      results
        .map(function (r) {
          var ranking = r.ranking || {};
          return (
            '<div class="cip-evidence-item mb-3">' +
            "<p class='mb-1'><button type='button' class='btn btn-link p-0' data-cip-open-entity='" +
            escapeAttr(r.entity_id) +
            "' data-cip-evidence-entity='" +
            escapeAttr(r.entity_id) +
            "'>" +
            escapeHtml(r.title || r.entity_id) +
            "</button> · " +
            escapeHtml(r.kind || "") +
            " · rank " +
            (r.rank_score != null ? Number(r.rank_score).toFixed(3) : "—") +
            " · conf " +
            pct(r.confidence) +
            (r.verified ? " · verified" : "") +
            "</p>" +
            "<p class='small text-muted mb-1'>" +
            escapeHtml((r.body || "").slice(0, 180)) +
            "</p>" +
            "<p class='small mb-0'>Ranking: semantic " +
            (ranking.semantic_similarity != null
              ? Number(ranking.semantic_similarity).toFixed(3)
              : "—") +
            " · graph " +
            (ranking.graph_proximity != null
              ? Number(ranking.graph_proximity).toFixed(3)
              : "—") +
            " · confidence " +
            (ranking.confidence != null ? Number(ranking.confidence).toFixed(3) : "—") +
            " · verification " +
            (ranking.founder_verification != null
              ? Number(ranking.founder_verification).toFixed(3)
              : "—") +
            "</p>" +
            (r.provenance_id
              ? "<p class='small mb-0'>Provenance " +
                escapeHtml(r.provenance_id) +
                "</p>"
              : "") +
            "</div>"
          );
        })
        .join("");
    bindEntityOpeners(root, host);
    qsa(host, "[data-cip-evidence-entity]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        loadNeighbours(root, btn.getAttribute("data-cip-evidence-entity"));
      });
    });
  }

  function loadNeighbours(root, entityId) {
    if (!entityId) return;
    var base =
      "/console/studio/workspaces/" +
      encodeURIComponent(root.getAttribute("data-workspace-id")) +
      "/intelligence/entities/" +
      encodeURIComponent(entityId) +
      "/neighbours";
    var wrap = qs(root, "[data-cip-evidence-neighbours]");
    var list = qs(root, "[data-cip-evidence-neighbours-list]");
    if (!wrap || !list) return;
    wrap.removeAttribute("hidden");
    list.innerHTML = "<li class='text-muted'>Loading neighbours…</li>";
    fetchJson(base)
      .then(function (body) {
        var items = body.neighbours || [];
        if (!items.length) {
          list.innerHTML = "<li class='text-muted'>No neighbours.</li>";
          return;
        }
        list.innerHTML = items
          .map(function (n) {
            return (
              "<li>" +
              escapeHtml(n.title || n.entity_id) +
              " · " +
              escapeHtml(n.relation_type || "") +
              " · hop " +
              (n.distance != null ? n.distance : "—") +
              "</li>"
            );
          })
          .join("");
      })
      .catch(function (err) {
        list.innerHTML =
          '<li class="text-danger">' + escapeHtml(err.message) + "</li>";
      });
  }

  function loadEmbeddingStatus(root) {
    var url = root.getAttribute("data-embedding-status-url");
    if (!url) return Promise.resolve();
    return fetchJson(url).then(function (body) {
      renderEmbeddingStatus(root, body);
    });
  }

  function runEvidenceSearch(root) {
    var input = qs(root, "[data-cip-evidence-input]");
    var profile = qs(root, "[data-cip-evidence-profile]");
    var q = input && input.value.trim();
    if (!q) return;
    var url =
      root.getAttribute("data-evidence-search-url") +
      "?q=" +
      encodeURIComponent(q) +
      "&profile=" +
      encodeURIComponent((profile && profile.value) || "founder_explorer");
    var host = qs(root, "[data-cip-evidence-results]");
    if (host) host.innerHTML = "<p class='text-muted mb-0'>Searching…</p>";
    fetchJson(url)
      .then(function (body) {
        renderEvidence(root, body);
      })
      .catch(function (err) {
        if (host) {
          host.innerHTML =
            '<p class="text-danger mb-0">' + escapeHtml(err.message) + "</p>";
        }
      });
  }

  function escapeHtml(value) {
    return String(value == null ? "" : value)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function escapeAttr(value) {
    return escapeHtml(value).replace(/'/g, "&#39;");
  }

  function init(root) {
    qsa(root, "[data-cip-tab]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var name = btn.getAttribute("data-cip-tab");
        activateTab(root, name);
        if (name === "validation") loadValidation(root);
        if (name === "review") loadReview(root);
        if (name === "metrics") loadMetrics(root);
        if (name === "graph") loadGraph(root);
        if (name === "pipeline") loadAudit(root);
        if (name === "overview") loadOverview(root);
        if (name === "evidence") {
          loadEmbeddingStatus(root).catch(function () {});
        }
      });
    });
    var loadBtn = qs(root, "[data-cip-entity-load]");
    if (loadBtn) {
      loadBtn.addEventListener("click", function () {
        var input = qs(root, "[data-cip-entity-input]");
        loadEntity(root, input && input.value.trim());
      });
    }
    var searchBtn = qs(root, "[data-cip-evidence-search]");
    if (searchBtn) {
      searchBtn.addEventListener("click", function () {
        runEvidenceSearch(root);
      });
    }
    var evidenceInput = qs(root, "[data-cip-evidence-input]");
    if (evidenceInput) {
      evidenceInput.addEventListener("keydown", function (ev) {
        if (ev.key === "Enter") {
          ev.preventDefault();
          runEvidenceSearch(root);
        }
      });
    }
    loadOverview(root).catch(function () {});
  }

  document.addEventListener("DOMContentLoaded", function () {
    qsa(document, "[data-cip-intelligence]").forEach(init);
  });
})();
