# BF-001 — Regression Report

**Programme:** Blocker Fix Programme BF-001  
**Date:** 2026-07-31  
**Verdict:** PASS

---

## Regression path exercised

```
Create Subject → Upload → Preview → Approve → Publish
       ↑__________________________________|
              Restart (→ Upload/SUBJECT)
Delete draft (unpublished) / Archive (published)
```

Automated coverage maps each RF blocker to HTTP or static evidence.

---

## Evidence matrix

| Blocker | Test / evidence | Result |
|---------|-----------------|--------|
| 1 Expand/Collapse | `test_preview_tree_js_uses_plain_objects_not_object_constructor` — asserts `{}` maps + `keydown` | PASS |
| 2 Back navigation | `test_workspace_exposes_retreat_and_reset`, `test_retreat_moves_stage_back_without_duplicate` | PASS |
| 3 Version assignment | `test_assign_version_rejects_invalid_label_with_clear_flash`, `test_assign_version_succeeds_with_year_dot_n`, form validator tests | PASS |
| 4 Restart | `test_reset_returns_to_upload_subject_stage` — stage → `subject` | PASS |
| 5 Lifecycle | `test_delete_draft_removes_workspace`, `test_archive_published_protects_from_delete` | PASS |
| 6 Duplicate rows | `test_catalogue_css_hides_mobile_list_on_desktop`, `test_subjects_catalogue_renders_one_logical_row_per_subject` | PASS |

---

## Commands run

```bash
python3 -m pytest \
  tests/presentation/curriculum_studio/test_bf001_blocker_remediation.py \
  tests/presentation/curriculum_studio/test_forms.py \
  tests/presentation/curriculum_studio/test_messaging.py \
  tests/presentation/curriculum_studio/test_product_language.py \
  tests/presentation/curriculum_studio/test_rendering.py \
  tests/test_dx006b_founder_subjects.py \
  tests/certification/test_pr001a_founder_operations.py::TestOperationalErrorRecovery \
  -q
# → 111+ related cases green in combined runs; BF-001 file: 13 passed

python3 -m ruff check app/presentation/curriculum_studio/ \
  app/application/curriculum_studio/workspace_service.py \
  app/application/curriculum_studio/version_history_service.py
# → All checks passed
```

---

## Behavioural guarantees verified

1. **Expand/Collapse** — forest built on plain objects; keyboard bindings present.
2. **Back** — retreat one domain stage; single workspace retained.
3. **Version** — `1.0.0` rejected with recovery copy; `2026.1` succeeds even after Management subject loss.
4. **Restart** — returns to `subject` (Founder Upload) without creating a second workspace.
5. **Delete draft** — removes unpublished workspace; published delete blocked with explanation.
6. **Archive** — published → `archived`; retained for history.
7. **Catalogue** — one logical subject per id; mobile list CSS-hidden on desktop.

---

## Residual risk

- Full Create→Publish browser dogfood (RF-001A) should re-run once on a staging Founder session to confirm Expand All with live CIP preview nodes.
- Hard restart that clears upload facts is not covered (by design).

---

## Residual debt

See `BF001_IMPLEMENTATION_REPORT.md` § Technical Debt.

---

## Conclusion

Category A workflow blockers are remediated. Application is ready to resume **RF-001A**.
