# EA-006 — Publication Report

**Programme:** Educational Excellence Programme EA-006 — Educational Package Publication  
**Phase:** Educational Package Publication  
**Date:** 2026-08-01  
**Authority:** EA-001 PASS · EA-002 PASS · EA-003 PASS · EA-004 PASS · EA-005 PASS · EV-001  
**Workflow:** `EA002_PUBLICATION_WORKFLOW.md`  

---

## 1. Publication principle applied

> Nothing educational reaches students unless it is certified and publication-approved for a named subject package version.

Technical schema validity alone is **not** sufficient. This publication rests on EA-005 Certification PASS + EA-006 Publication Approval for one Mission bundle.

---

## 2. Publication unit

| Field | Value |
|-------|-------|
| **Unit type** | Mission bundle (joint) |
| **Package ID** | `CS1-EA005-PKG-4.2-GLM-STRUCTURE` |
| **Golden ID** | `GOLDEN-EA005-CS1-4.2-GLM-STRUCTURE` |
| **Subject** | CS1 — Actuarial Statistics (2026) |
| **Syllabus node** | `4.2` — Understand and use generalised linear models |
| **Pilot version** | `ea005-pilot-1.0.0` |
| **Publication version** | `ea006-live-1.0.0` |
| **Mode** | Learning |
| **Replaces** | Live templated / syllabus-paste educational experience for topic 4.2 only |

### Inventory published together (atomic)

| Artefact | ID / locus | Status |
|----------|------------|--------|
| Mission | `msn-ea005-cs1-4.2-glm-structure` | Included |
| Session | `ssn-ea005-cs1-4.2-glm-structure` | Included |
| Reading Guidance | Guided Reading exit packet (CMP 4.2 setup) | Included |
| Knowledge Checks | `lep-ea005-4.2-ar-01` · `lep-ea005-4.2-cp-01` | Included |
| Reflection | Topic-specific GLM chain harvest | Included |
| Tomorrow Preview | Bridge to **5.1** Bayesian foundations | Included |

**Rule obeyed:** No partial artefacts. No orphan Mission. No Episode without Session story. Tomorrow Preview agrees with Mission `tomorrow_bridge`.

---

## 3. Preconditions (EA-002 §3)

| Precondition | Evidence | Result |
|--------------|----------|--------|
| Authoring pack complete | `EA005_EDUCATIONAL_PACKAGE.md` | PASS |
| Style / Tutor Voice self-check | EA-005 pack quality self-check + multi-review | PASS |
| Multi-stage certification PASS | `EA005_CERTIFICATION_REPORT.md` | PASS |
| EA-001 gates PASS | Gate MG/MX, SS/SX/LE, TP (EA-005) | PASS |
| Joint composition rules | Mission ⇄ Session ⇄ Episodes ⇄ Reflection ⇄ Tomorrow | PASS |
| Universal preconditions U1–U7 | EA-005 certification | PASS |
| Cross-surface truth audit prepared | Live Validation Report | PASS (application path) |

---

## 4. Publication Request

| Field | Value |
|-------|-------|
| Subject / package version | CS1 · `ea006-live-1.0.0` (node 4.2 only) |
| Artefact inventory | See §2 |
| Certification evidence | `EA005_CERTIFICATION_REPORT.md`, `EA005_MULTI_REVIEW_REPORT.md`, `EA005_GOLDEN_PACKAGE_ASSESSMENT.md` |
| Gate results | MG/MX, SS/SX/LE, TP — PASS (post-R2) |
| EV-001 regression checklist | See §7 — denied for TB-001/002/004/007/008/009 on this package |
| Scope statement | One educational package only — not a CS1 rewrite |

---

## 5. Publication Approval

| Field | Value |
|-------|-------|
| **Outcome** | **APPROVED** |
| Approver | Academic Board / Founder Educational Gate Owner (EA-006 programme) |
| Date | 2026-08-01 |
| HOLD items | None |
| Technical publish ≠ educational PASS | Acknowledged — curriculum Studio publish of syllabus JSON is separate; this approval is educational |
| Student exposure | Approved inventory may reach students via educational package loader when topic 4.2 is the Mission topic |

### Approval statement

The Golden Educational Package for CS1 topic **4.2 (GLM structure)** is publication-approved as a single Mission bundle at version `ea006-live-1.0.0`. Students may rely on these artefacts as primary study guidance for that node. Unapproved topics remain on prior templated paths.

---

## 6. Release to student surface

| Mechanism | Path |
|-----------|------|
| On-disk artefact | `app/curriculum/data/educational_packages/cs1/4.2-glm-structure-ea006.json` |
| Loader | `app/application/educational_packages/` |
| Session substance | `EducationalSubstancePlanner` prefers certified pack |
| Home / briefing composition | `compose_mission` overlay from pack |
| Mission chrome | Display title / why_now / expected benefit overlays |
| Reflection / Tomorrow | Pack prompts on matching topic |

Version pinning: students see `ea006-live-1.0.0` fields when topic resolves to this pack; mixed uncertified drafts do not load.

---

## 7. EV-001 regression checklist (publication pack)

| ID | Failure class | Denied by this pack? |
|----|---------------|----------------------|
| TB-001 | “Today’s topic” / placeholder collapse | Yes — real topic title + GLM guidance |
| TB-002 | Syllabus-paste Mission | Yes — display title + tutor brief |
| TB-003 | Contaminant topics | Out of scope (curriculum hygiene; not this pack) |
| TB-004 | Boilerplate explainability | Yes — unique why_now / explainability |
| TB-005 | Mastery/coverage theatre | Language denies Topic Complete / mastery |
| TB-007 | Empty reading shells | Yes — full Reading Guidance exit packet |
| TB-008 | Broken stage advance | Practice items advance through AR → Checkpoint |
| TB-009 | Timing disagrees | Pack duration 50–70 min overlaid |

---

## 8. Post-publish verification

See `EA006_LIVE_VALIDATION_REPORT.md`.

Spot-check summary: substance source = `educational_package`; no “Today’s topic”; CMP guidance present; Knowledge Checks present; Reflection topic-specific; Tomorrow = 5.1 continuity.

---

## 9. Maintenance note

| Trigger watch | Action |
|---------------|--------|
| CMP edition / locus change | Re-verify Reading Guidance open/stop; recertify |
| Syllabus weight update | Re-verify why_now / tomorrow chain |
| Contaminant discovery elsewhere | Does not unpublish this pack; separate curriculum HOLD |
| Package version bump | Full certification floor applies |

---

## 10. Closing

One certified Educational Package is publication-approved and released into the live educational pipeline for CS1 **4.2** only. This is a textbook-chapter revision, not a subject rewrite.
