# RO1-R1 — Regression Report

**Programme:** RO1-R1 — Tomorrow Preview Honesty Remediation  
**Date:** 2026-08-01  
**Authority:** RO-001A · EF-001 · PB-002 selection invariants  

---

## Verdict

# **Local regression: PASS — no educational package / selection / authoring regressions detected**

---

## Scope checked

| Area | Expectation | Result |
|------|-------------|--------|
| PB-002 package selection / campaign chain | Unchanged successor resolution | **PASS** (`test_pb002_package_selection`) |
| EA-006 publication load / 4.2 golden | Unchanged | **PASS** (`test_ea006_publication`) |
| KWP-015 Educational Authoring (synthetic topics) | No accidental CS1 package overlay via title keywords | **PASS** (`test_kwp015_educational_authoring`) |
| KWP-005 Sitting Report | Still projects completion chrome | **PASS** (`test_kwp005_sitting_reports`) |
| RO1-R1 tomorrow chrome binding | Package id / day-complete / compose / sitting report | **PASS** (`test_ro1r1_tomorrow_chrome`) |
| Educational packages on disk | Unmodified | **PASS** (no JSON diffs) |
| Educational Framework | Unmodified | **PASS** |
| Recommendation logic | Untouched | **PASS** (no files changed) |

## Commands

```bash
python3 -m pytest \
  tests/application/educational_packages/test_ro1r1_tomorrow_chrome.py \
  tests/test_kwp015_educational_authoring.py \
  tests/test_kwp005_sitting_reports.py \
  tests/application/educational_packages/test_ea006_publication.py \
  tests/application/educational_packages/test_pb002_package_selection.py -q
# 39 passed
```

```bash
python3 -m ruff check \
  app/application/educational_packages/tomorrow_chrome.py \
  app/application/educational_packages/composition_overlay.py \
  app/application/educational_authoring/dto.py \
  app/application/educational_authoring/engine.py \
  app/presentation/session/sitting_report.py \
  app/presentation/student/adaptive_workspace.py \
  … # all RO1-R1 touched modules
# All checks passed
```

## Failure-mode regression (documented)

Bare `find_educational_package(topic_code="2.1")` still returns Beta discrete first-match — that path is **no longer used** for Tomorrow Preview chrome. Chrome resolution requires package id, campaign journey state, or a **unique** topic code.

## Educational regressions

None observed on package bodies, CMP reading delivery path, or campaign chain selection tests.

## Fallback

No new fallback shells introduced. When package identity cannot be resolved for chrome, Finish uses strategy/syllabus tomorrow language instead of a wrong sibling-day package.

---

Signed: RO1-R1 Regression · 2026-08-01
