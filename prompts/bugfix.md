# Prompt: Bug Fix

Use this prompt to start a Kwalitec bugfix in Cursor.

---

## Agent instructions

You are debugging **Kwalitec**.

Before changing code:

1. Reproduce or reason carefully from the failure evidence (traceback, failing test, user steps).
2. Read `PROJECT_CONTEXT.md` / `ARCHITECTURE.md` if the bug spans layers.
3. Prefer the smallest fix that addresses the root cause.
4. Add or extend a regression test when practical.
5. Do not mix in unrelated refactors.

## Bug report

**Summary:** \<one sentence\>

**Environment:** \<local / Render / test / Python version\>

**Steps to reproduce:**
1. \<step\>
2. \<step\>

**Expected:** \<behaviour\>

**Actual:** \<behaviour\>

**Evidence:** \<traceback, logs, screenshot notes, failing test name\>

**Suspect areas (optional):** \<files/modules\>

## Constraints

- Out of scope: \<e.g. redesign, dependency upgrades\>
- Curriculum impact: \<none / V1 / V2 / both — investigate\>

## Completion

- Confirm root cause in the summary.
- List files changed and tests run.
- Include Migration Impact and Architecture Compliance if curriculum/schema layers were touched.
- Commit only if asked.
