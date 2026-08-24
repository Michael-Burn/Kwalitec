# EP-001 — Educational Production Programme Governance

**Programme:** EP-001 — Educational Production Programme (Production Era)  
**Phase:** Educational content production through CS1 exam coverage  
**Status:** Binding — production governance  
**Effective:** 2026-08-01  
**Authority:** EF-001 (Frozen Educational Law) · PB-002 PASS · CE-001 (Measurement) COMPLETE · EA-001…EA-008 · EO-001 · EJ-001 · EW-001  
**Nature:** Content production governance only — **no** Runtime, SCI, Recommendations, Educational Framework, or Product Architecture redesign  

---

## 1. Mission

Produce, certify, and publish the remaining CS1 educational inventory until a diligent student can travel from Baseline to the examination without encountering unpublished educational content or a reduction in educational quality.

This programme governs **educational content production** only.

---

## 2. Distinction from CE-001 (Measurement)

| Programme | Role | Status |
|-----------|------|--------|
| **CE-001** | Catalogue coverage definition, measurement, and continuity-first scheduling | **COMPLETE** — do not reopen or amend measurement law |
| **EP-001 (Production Era)** | Author → certify → approve → publish → verify educational packages | **Active** — this programme |

EP-001 **consumes** CE-001 coverage law (`CE001_CATALOGUE_COVERAGE.md`) and the CE-001 Continuity Front schedule. It does **not** redefine what counts as Published coverage.

**Coverage credit rule (unchanged):** An LO counts as Published only when Mission + Session + Campaign are certified **and** a human Publication Approver has signed the Volume to status ≥ `approved`.

---

## 3. Namespace rules

| Artefact family | Meaning | Rule |
|-----------------|---------|------|
| `EP001_GOVERNANCE.md`, `EP001_PRODUCTION_ROADMAP.md`, `EP001_COVERAGE_MAP.md`, `EP001_WAVE1_PLAN.md`, and successor Wave/Volume production dossiers under Production Era naming | EP-001 Production Era | Author and maintain here |
| Root `EP001_CAMPAIGN_*`, `EP001_TUTOR_REVIEW.md`, `EP001_FOUNDER_REVIEW.md`, `EP001_PUBLICATION_READINESS.md`, `EP001_IMPLEMENTATION_REPORT.md` | Historical **Campaign Alpha / CS1-001** Pilot Arc evidence | **Retain; do not overwrite** |
| `CS1002_*` | Historical **Campaign Beta / CS1-002** evidence | Retain |
| `CE001_*` | Measurement and schedule law | Frozen companion; update only when coverage status changes require map refresh |
| `knowledge/architecture/ep001_*` | Unrelated architecture track | **Out of scope** |

Campaign Alpha remains Volume CS1-001 under the Educational Volumes series. Production Era EP-001 continues that series (CS1-004, CS1-003, …) without renaming historical Alpha dossiers.

---

## 4. Production standard (every package)

Every educational package must satisfy:

- EF-001 (Frozen Educational Law)
- Educational Excellence (EA-001…EA-008)
- CMP Partnership (Q1–Q6)
- Educational Justification (EJ-001)
- Tutor Voice
- Retrieval and revision coherence
- Honest stop conditions
- Natural transition to the next mission

Reference quality bar: Campaign Alpha / CS1-001 (`ep001-1.0.0`).

---

## 5. Publication pipeline

For **each** package (and then for the Volume/Campaign that owns it):

```text
Author
  ↓
Educational Review
  ↓
Certification (Gates MG / SS / LE / TP / RV as applicable)
  ↓
Campaign Gate CG (Volume membership)
  ↓
Publication Approval  ← human Publication Approver
  ↓
LIVE Deployment
  ↓
Educational Verification
```

**Do not batch-certify.** Every package must independently earn publication. Campaign Gate CG does not waive per-package substance gates.

### Volume lifecycle (EO-001)

```text
draft → in_review → certified → publication_ready → approved → released
                                                      ↑
                                         coverage credit begins
```

`released` / LIVE activation is required for student reachability. Coverage *credit* under CE-001 begins at Publication Approval (`approved`).

---

## 6. Human-only gates

| Gate | Who | Agent may | Agent must not |
|------|-----|-----------|----------------|
| Educational / Peer Review (ER-*) | Human Educational Reviewer | Assemble worksheets; draft findings | Declare commercial PASS alone when dual-hat rules forbid |
| Tutor Review (TR-*) | Human Tutor Reviewer | Pre-fail checks; assemble pack | Declare Tutor Voice PASS |
| Academic / Curriculum Audit | Human Auditor | Assemble evidence | Forge Auditor PASS |
| Founder Review (FR-*) | Human Founder | Assemble FR pack | Forge Founder PASS |
| **Publication Approver** | Human Publication Approver | Assemble Approver dossier | Simulate or forge Approver signature; advance Volume to `approved` without human seal |

Unsigned signature blocks remain **Awaiting human**. Drafts and agent desk certification are not Publication Approval.

---

## 7. Wave discipline

1. Produce content only inside the active Wave named in `EP001_PRODUCTION_ROADMAP.md`.  
2. After each Wave: update `EP001_COVERAGE_MAP.md`, verify LIVE delivery for that Wave’s geography, then **stop**.  
3. Do not begin the next Wave until explicit approval.  
4. Do not claim until-examination educational trust until a final adversarial Private Beta rerun confirms the completed journey.

---

## 8. Validation after each published group

- Verify LIVE delivery.  
- Verify CMP partnership.  
- Verify educational continuity.  
- Verify no fallback / silent LO-shell experience on newly covered path (PB-002 withhold remains for unpublished topics).  
- Update educational coverage map.

---

## 9. Hard bans

| Forbidden | Why |
|-----------|-----|
| Redesign Runtime / SCI / Recommendations / Educational Framework / Product Architecture | Out of programme scope |
| Forge Founder, Tutor, Auditor, or Publication Approver approval | Governance integrity |
| Count drafts, orphans, or `publication_ready` as Published coverage | CE-001 law |
| Republish orphan Golden Days alone (FP-01) | EA-007 / EA-008 |
| Claim spine / exam-horizon readiness from partial LO % | Coverage mirage |
| Start Wave N+1 before Wave N exit + approval | Wave discipline |

---

## 10. Companion artefacts

| Artefact | Role |
|----------|------|
| `EP001_PRODUCTION_ROADMAP.md` | Waves from current inventory to exam coverage |
| `EP001_COVERAGE_MAP.md` | Live vs Approver-credit dual map |
| `EP001_WAVE1_PLAN.md` | Executable Wave 1 plan |
| `CE001_CATALOGUE_COVERAGE.md` | Binding coverage definition |
| `CE001_PRODUCTION_PRIORITY.md` | Continuity-first schedule ancestor |

---

## 11. Closing

EP-001 expands the catalogue the way a student walks it — one independently certified, human-approved day after another — advancing the Continuity Front without lowering the Alpha quality bar or forging human seals.

Signed notionally: Editorial Director · EP-001 · Governance · 2026-08-01
