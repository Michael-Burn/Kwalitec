# FV-001B Re-run — Launch Blockers

These blockers prevent a Founder from publishing a verified curriculum without assistance.

---

## LB-R1 — Validation dead end after Ready documents

**Symptom:** With Official CMP and Official Syllabus both Ready and extraction complete, **Validate Curriculum** fails: “blocking findings remain… Review the Validation findings below.” The page shows **0 validation errors** and does not list blocking findings.

**Why it blocks:** Founder cannot clear validation or know what to fix.

**Evidence:** `screenshots/phase5_validate_blocked.png`, `_evidence/complete.json` → `C2_validate`

---

## LB-R2 — Preview success contradicts not_ready

**Symptom:** Flash claims preview built successfully with topics; status card still says `not_ready`; topic counts disagree with Structure/Overview.

**Why it blocks:** Founder cannot trust Preview as a gate before Approve/Publish.

**Evidence:** `phase6_preview_contradiction.png`, `phase6_structure_topics.png`

---

## LB-R3 — Approve action reports Publish failure

**Symptom:** Clicking **Approve Curriculum** shows “We couldn't **publish** this curriculum… complete approval…” Version already shows `2026.1 (preview_ready)`. No approval success state.

**Why it blocks:** Approval cannot be completed; Founder believes Approve and Publish are entangled.

**Evidence:** `phase7_approve_confused.png`

---

## LB-R4 — Publish never completes; Ready never appears

**Symptom:** Publish Verified Curriculum refuses. Subjects catalogue leaves CS1U at `2026.1 · Validation` (and peers similarly non-Ready). No published date. Student surface does not present the new subject as Ready.

**Why it blocks:** Acceptance criteria for publish + catalogue Ready + student discoverability fail.

**Evidence:** `phase8_publish_refused.png`, `phase9_subjects_not_ready.png`, `phase9_student_orientation.png`

---

## LB-R5 — Stale / contradictory workflow guidance

**Symptom:** NEXT STEP and status chips disagree with documents Ready, topic extraction, and action flashes throughout the mid/late journey.

**Why it blocks:** Even a diligent Founder cannot self-correct without assistance.

**Evidence:** `FOUNDER_STUDIO_REVIEW.md` Phases 5–8; `NAVIGATION_AUDIT.md`

---

## Non-blockers (observed positives)

- Empty preview refused (`regression_empty_preview.png`)
- Incomplete publish refused (`regression_incomplete_publish.png`)
- Create Subject + labelled upload slots work when files are chosen correctly
- Primary chrome free of Educational Intelligence jargon (`TERMINOLOGY_AUDIT.md`)
