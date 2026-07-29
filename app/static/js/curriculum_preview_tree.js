/**
 * FV-001B — Hierarchical curriculum preview tree.
 *
 * Builds a nested tree from flat nodes with parent_id. Supports expand /
 * collapse, Expand All / Collapse All, section/chapter counts, and a
 * windowed (virtualised) DOM for large curricula (thousands of topics).
 */
(function () {
  "use strict";

  var ROW_HEIGHT = 36;
  var OVERSCAN = 8;

  function kindIsSection(kind) {
    var k = String(kind || "").toLowerCase();
    return k === "section" || k === "chapter" || k === "unit" || k === "module";
  }

  function kindIsTopic(kind) {
    var k = String(kind || "").toLowerCase();
    return k === "topic" || k === "lesson" || k === "objective";
  }

  function buildForest(nodes) {
    var byId = Object
    var children = Object
    var roots = [];
    (nodes || []).forEach(function (n, idx) {
      var id = String(n.node_id || "");
      if (!id) return;
      byId[id] = {
        id: id,
        title: n.title || id,
        kind: n.kind || "topic",
        parentId: n.parent_id == null || n.parent_id === "" ? null : String(n.parent_id),
        order: Number(n.order_index != null ? n.order_index : idx),
        childIds: [],
        topicCount: 0,
        sectionCount: 0,
      };
      children[id] = children[id] || [];
    });
    Object.keys(byId).forEach(function (id) {
      var node = byId[id];
      var parent = node.parentId;
      if (parent && byId[parent]) {
        children[parent].push(id);
      } else {
        roots.push(id);
      }
    });
    Object.keys(children).forEach(function (id) {
      children[id].sort(function (a, b) {
        return byId[a].order - byId[b].order;
      });
      byId[id].childIds = children[id];
    });
    roots.sort(function (a, b) {
      return byId[a].order - byId[b].order;
    });

    function countDesc(id) {
      var node = byId[id];
      var topics = kindIsTopic(node.kind) ? 1 : 0;
      var sections = kindIsSection(node.kind) ? 1 : 0;
      node.childIds.forEach(function (cid) {
        var sub = countDesc(cid);
        topics += sub.topics;
        sections += sub.sections;
      });
      node.topicCount = topics;
      node.sectionCount = sections;
      return { topics: topics, sections: sections };
    }
    roots.forEach(countDesc);
    return { byId: byId, roots: roots };
  }

  function CurriculumPreviewTree(root) {
    this.root = root;
    this.viewport = root.querySelector("[data-preview-viewport]");
    this.spacer = root.querySelector("[data-preview-spacer]");
    this.list = root.querySelector("[data-preview-rows]");
    this.meta = root.querySelector("[data-preview-meta]");
    this.expanded = {};
    this.visible = [];
    this.scrollTop = 0;
    var raw = [];
    try {
      raw = JSON.parse(root.getAttribute("data-preview-nodes") || "[]");
    } catch (err) {
      raw = [];
    }
    this.forest = buildForest(raw);
    this.lazyThreshold = Number(root.getAttribute("data-lazy-threshold") || 400);
    // Expand first level by default for orientation.
    this.forest.roots.forEach(
      function (id) {
        this.expanded[id] = true;
      }.bind(this)
    );
    this._bind();
    this.rebuildVisible();
    this.render();
    this.updateMeta();
  }

  CurriculumPreviewTree.prototype._bind = function () {
    var self = this;
    this.root.querySelectorAll("[data-preview-expand-all]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        self.expandAll();
      });
    });
    this.root.querySelectorAll("[data-preview-collapse-all]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        self.collapseAll();
      });
    });
    if (this.viewport) {
      this.viewport.addEventListener("scroll", function () {
        self.scrollTop = self.viewport.scrollTop;
        self.renderWindow();
      });
    }
    if (this.list) {
      this.list.addEventListener("click", function (evt) {
        var toggle = evt.target.closest("[data-preview-toggle]");
        if (!toggle) return;
        var id = toggle.getAttribute("data-preview-toggle");
        if (!id) return;
        self.toggle(id);
      });
    }
  };

  CurriculumPreviewTree.prototype.toggle = function (id) {
    if (this.expanded[id]) delete this.expanded[id];
    else this.expanded[id] = true;
    this.rebuildVisible();
    this.render();
  };

  CurriculumPreviewTree.prototype.expandAll = function () {
    var self = this;
    var ids = Object.keys(this.forest.byId);
    // Chunked expand keeps the main thread responsive for large curricula.
    var i = 0;
    function chunk() {
      var end = Math.min(i + 500, ids.length);
      for (; i < end; i += 1) {
        var node = self.forest.byId[ids[i]];
        if (node && node.childIds.length) self.expanded[ids[i]] = true;
      }
      if (i < ids.length) {
        window.requestAnimationFrame(chunk);
      } else {
        self.rebuildVisible();
        self.render();
      }
    }
    chunk();
  };

  CurriculumPreviewTree.prototype.collapseAll = function () {
    this.expanded = {};
    this.rebuildVisible();
    this.render();
  };

  CurriculumPreviewTree.prototype.rebuildVisible = function () {
    var visible = [];
    var byId = this.forest.byId;
    var expanded = this.expanded;
    function walk(id, depth) {
      var node = byId[id];
      if (!node) return;
      visible.push({ id: id, depth: depth });
      if (expanded[id]) {
        node.childIds.forEach(function (cid) {
          walk(cid, depth + 1);
        });
      }
    }
    this.forest.roots.forEach(function (id) {
      walk(id, 0);
    });
    this.visible = visible;
  };

  CurriculumPreviewTree.prototype.updateMeta = function () {
    if (!this.meta) return;
    var sections = 0;
    var topics = 0;
    var byId = this.forest.byId;
    Object.keys(byId).forEach(function (id) {
      var node = byId[id];
      if (kindIsSection(node.kind)) sections += 1;
      if (kindIsTopic(node.kind)) topics += 1;
    });
    this.meta.textContent =
      sections +
      " section" +
      (sections === 1 ? "" : "s") +
      " · " +
      topics +
      " topic" +
      (topics === 1 ? "" : "s") +
      " · " +
      this.visible.length +
      " visible";
  };

  CurriculumPreviewTree.prototype.render = function () {
    if (this.spacer) {
      this.spacer.style.height = this.visible.length * ROW_HEIGHT + "px";
    }
    this.renderWindow();
    this.updateMeta();
  };

  CurriculumPreviewTree.prototype.renderWindow = function () {
    if (!this.list || !this.viewport) return;
    var height = this.viewport.clientHeight || 320;
    var start = Math.max(0, Math.floor(this.scrollTop / ROW_HEIGHT) - OVERSCAN);
    var end = Math.min(
      this.visible.length,
      Math.ceil((this.scrollTop + height) / ROW_HEIGHT) + OVERSCAN
    );
    var frag = document.createDocumentFragment();
    for (var i = start; i < end; i += 1) {
      frag.appendChild(this._rowEl(this.visible[i], i));
    }
    this.list.innerHTML = "";
    this.list.style.transform = "translateY(" + start * ROW_HEIGHT + "px)";
    this.list.appendChild(frag);
  };

  CurriculumPreviewTree.prototype._rowEl = function (entry, index) {
    var node = this.forest.byId[entry.id];
    var row = document.createElement("div");
    row.className = "ds-curriculum-preview__row";
    row.style.height = ROW_HEIGHT + "px";
    row.style.paddingLeft = 0.75 + entry.depth * 1.1 + "rem";
    row.setAttribute("data-preview-row", entry.id);
    row.setAttribute("role", "treeitem");
    row.setAttribute("aria-level", String(entry.depth + 1));
    var hasChildren = node.childIds.length > 0;
    row.setAttribute("aria-expanded", hasChildren ? String(!!this.expanded[node.id]) : "false");

    if (hasChildren) {
      var toggle = document.createElement("button");
      toggle.type = "button";
      toggle.className = "ds-curriculum-preview__toggle";
      toggle.setAttribute("data-preview-toggle", node.id);
      toggle.setAttribute("aria-label", (this.expanded[node.id] ? "Collapse " : "Expand ") + node.title);
      toggle.textContent = this.expanded[node.id] ? "▾" : "▸";
      row.appendChild(toggle);
    } else {
      var spacer = document.createElement("span");
      spacer.className = "ds-curriculum-preview__toggle-spacer";
      spacer.setAttribute("aria-hidden", "true");
      row.appendChild(spacer);
    }

    var badge = document.createElement("span");
    badge.className = "ds-badge ds-badge--neutral";
    badge.textContent = node.kind;
    row.appendChild(badge);

    var title = document.createElement("strong");
    title.className = "ds-curriculum-preview__title";
    title.textContent = node.title;
    row.appendChild(title);

    if (hasChildren) {
      var counts = document.createElement("span");
      counts.className = "ds-list__meta";
      var parts = [];
      if (node.sectionCount) parts.push(node.sectionCount + " sec");
      if (node.topicCount) parts.push(node.topicCount + " topics");
      counts.textContent = parts.join(" · ");
      row.appendChild(counts);
    }
    return row;
  };

  function initAll() {
    document.querySelectorAll("[data-curriculum-preview-tree]").forEach(function (el) {
      if (el.getAttribute("data-preview-ready") === "1") return;
      el.setAttribute("data-preview-ready", "1");
      new CurriculumPreviewTree(el);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initAll);
  } else {
    initAll();
  }
})();
