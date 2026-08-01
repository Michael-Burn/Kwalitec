# PR-001 — Volume Register

**Programme:** Production Readiness Programme PR-001 — Educational Production Pipeline Execution  
**Phase:** Educational Production Operations  
**Status:** Binding — Volume dossier for CS1-001 (Campaign Alpha)  
**Effective:** 2026-08-01  
**Authority:** EO-001 Educational Volume Standard · EP-001 Campaign Alpha PASS · EA-001…EA-008 COMPLETE  
**Nature:** Operational Volume dossier — no new governance; no content authored; no Runtime/application changes  

---

## 1. Volume identity (EO-001 §3)

| Field | Value |
|-------|-------|
| `volume_id` | **CS1-001** |
| `volume_title` | Campaign Alpha — From Purpose to Exploratory Judgement |
| `subject_id` | `cs1` |
| `curriculum_package_version` | IFoA CS1 2026 |
| `cmp_edition` | IFoA CS1 Core Reading / CMP · 2026 syllabus alignment |
| `scope_class` | `pilot_arc` |
| `series` | CS1 Educational Volumes |
| `sequence_in_series` | **1** |
| `reference_bar` | `CS1-EP001-CAMPAIGN-ALPHA@ep001-1.0.0` (self — founding reference Volume) |
| `created_at` | 2026-08-01 |
| `owner_role` | Founder (Subject Lead unstaffed) |
| `volume_version` | `1.0.0` |
| `edition_label` | 2026 First Edition (catalogue) |

### Identity tests (VI-01…VI-05)

| ID | Result |
|----|--------|
| VI-01 Unique `volume_id` | **PASS** — CS1-001 first in series |
| VI-02 Journey-named title | **PASS** — purpose → exploratory judgement |
| VI-03 Scope matches membership | **PASS** — Pilot Arc only |
| VI-04 CMP + curriculum pins | **PASS** — declared |
| VI-05 Reference bar cited | **PASS** — founding bar (self) |

---

## 2. Campaign membership (EO-001 §4)

| Field | Value |
|-------|-------|
| `campaign_id` | `CS1-EP001-CAMPAIGN-ALPHA` |
| `campaign_version` | `ep001-1.0.0` |
| `gate_cg` | **PASS** |
| `order_index` | 1 |
| `role_in_volume` | `primary` |
| `package_inventory_ref` | `app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/` |
| `continuity_index` | **8.75** |
| `bridge_integrity` | **100%** |

### Package inventory

| Order | Package ID | Day | Mode | Topic / LO |
|------:|------------|-----|------|------------|
| 1 | `CS1-EP001-PKG-1.1-PURPOSE-FUNCTION` | CA-D1 | Learning | 1.1 |
| 2 | `CS1-EP001-PKG-1.2-EDA-SUMMARIES` | CA-D2 | Learning | 1.2 · 1.2.1 |
| 3 | `CS1-EP001-PKG-1.2-EDA-ASSOCIATION` | CA-D3 | Learning | 1.2 · 1.2.2 |
| 4 | `CS1-EP001-PKG-REV-PURPOSE-EDA` | CA-R1 | Revision | Return 1.1 · 1.2.1 · 1.2.2 |

**Membership rules:** All members Gate CG–certified; joint inventory; no grandfather absorption of 4.2; scope honesty = Pilot Arc; Alpha floor is self.

**Minimum publishable Volume:** Met (≥ 3 contiguous Learning + Revision).

---

## 3. Publication status (EO-001 §5)

| Field | Value |
|-------|-------|
| **Current status** | `publication_ready` |
| Student-reachable? | **No** |
| Prior status path | `draft` → `in_review` → `certified` → **`publication_ready`** |
| Next lawful status | `approved` (requires Publication Approver) then `released` (requires activation engineering) |

### Status transition log

| Date | From | To | Authority / evidence |
|------|------|----|----------------------|
| 2026-08-01 | — | `draft` | EP-001 authoring opened |
| 2026-08-01 | `draft` | `in_review` | Tutor / Auditor / Founder review cycle |
| 2026-08-01 | `in_review` | `certified` | Gate CG PASS · `EP001_CAMPAIGN_CERTIFICATION.md` |
| 2026-08-01 | `certified` | `publication_ready` | `EP001_PUBLICATION_READINESS.md` + PR-001 Volume formalisation |

**Status honesty:** `publication_ready` ≠ `approved` ≠ `released`. Catalogue-certified, pathway-gated.

---

## 4. Version history (EO-001 §6)

| volume_version | edition_label | change_class | summary | membership snapshot | approval_refs | effective_from | supersedes |
|----------------|---------------|--------------|---------|---------------------|---------------|----------------|------------|
| `1.0.0` | 2026 First Edition (catalogue) | `educational` | Founding Pilot Arc Volume — Campaign Alpha Gate CG PASS | Alpha inventory ×4 @ `ep001-1.0.0` | Certification pack only; Approver pending | Catalogue effective 2026-08-01; pathway not released | — |

---

## 5. Certification history

| Record | Outcome | Date | Evidence |
|--------|---------|------|----------|
| Per-package Gate MG/SS/LE/TP/RV (D1–D3, R1) | **PASS** | 2026-08-01 | `EP001_CAMPAIGN_CERTIFICATION.md` §2 |
| Gate CG (journey) | **PASS** | 2026-08-01 | CI 8.75; bridges 100%; CG-01…CG-07 PASS |
| Continuity Index | **8.75** | 2026-08-01 | CL-01…CL-08 scored |
| FP-01…FP-06 | **DENIED** | 2026-08-01 | `EP001_PUBLICATION_READINESS.md` |
| Nested EA-002 substance (Board desk) | **PASS** | 2026-08-01 | Certification preconditions |

---

## 6. Reviewer history

| Role | Reviewer identity (programme) | Outcome | Date | Evidence |
|------|-------------------------------|---------|------|----------|
| Educational / Tutor Reviewer | Tutor Reviewer · EP-001 | **PASS** | 2026-08-01 | `EP001_TUTOR_REVIEW.md` |
| Academic Auditor | Educational Auditor · EP-001 | **PASS** (issues closed) | 2026-08-01 | `EP001_CAMPAIGN_CERTIFICATION.md` defect cycle |
| Founder | Founder / Academic Publisher · EP-001 | **PASS** | 2026-08-01 | `EP001_FOUNDER_REVIEW.md` |
| Publication Readiness Author | EP-001 | Ready to request Approver | 2026-08-01 | `EP001_PUBLICATION_READINESS.md` |

### Auditor defect cycle (closed)

| ID | Finding | Disposition |
|----|---------|-------------|
| EA-R1-02 | D2 stop condition risked PCA bleed | Fixed — explicit stop |
| EA-R1-03 | R1 terminal must not claim 1.2.3 done | Fixed — deferred LO named |
| RQ-04 candidate | D3 Reflection too close to D2 stem | Fixed — distinguish / choose / refuse triad |

---

## 7. Approval history (EO-001 §7)

| record_id | stage | outcome | signer_role | signer_name | date | evidence_refs | defects_closed | claims |
|-----------|-------|---------|-------------|-------------|------|---------------|-----------------|--------|
| CS1-001-PR-EP001 | Peer / Tutor Review | **PASS** | Educational Reviewer | Tutor Reviewer · EP-001 | 2026-08-01 | `EP001_TUTOR_REVIEW.md` | Voice issues none open | — |
| CS1-001-AUDIT-EP001 | Educational Audit | **PASS** | Academic Auditor | Educational Auditor · EP-001 | 2026-08-01 | `EP001_CAMPAIGN_CERTIFICATION.md` | EA-R1-* closed | — |
| CS1-001-FR-EP001 | Founder Review | **PASS** | Founder | Founder · EP-001 | 2026-08-01 | `EP001_FOUNDER_REVIEW.md` | FR-01…03 held in readiness | Pilot Arc only |
| CS1-001-PA-PENDING | Publication Approval | **PENDING** | Publication Approver | _unsigned_ | — | Approver worksheet open | — | See claims registry |

**Hard rule:** Automation / Board desk alone may not APPROVE commercial Volume publication. Human Publication Approver signature required.

---

## 8. Claims allowed / forbidden (current status)

| Allowed at `publication_ready` | Forbidden |
|--------------------------------|-----------|
| “Catalogue-certified Pilot Arc Volume CS1-001 (1.1–1.2.2 + revision)” | “Released to all CS1 students” |
| “Gate CG PASS; ready for Publication Approver” | “CS1 Educational Excellence complete” |
| “Sets house reference bar for successor Volumes” | “Semester / first-pass spine continuity PASS” |
| Honest deferral of PCA 1.2.3 | Silent claim Chapter 1 finished including PCA |
| 4.2 remains `pre-campaign-pilot` | Treating Alpha as absorption of 4.2 |

---

## 9. Dependency register (EO-001 §8)

| dep_id | class | pin / version | owner | break trigger | remediation |
|--------|-------|---------------|-------|---------------|-------------|
| DEP-CURR-01 | Curriculum | IFoA CS1 2026 | Editorial Office | Syllabus package change | Impact inventory; possible HOLD |
| DEP-CMP-01 | CMP | 2026 Core Reading / CMP | Editorial Office | Edition / locus drift | Re-verify Reading Guidance; recertify |
| DEP-CAMP-01 | Campaign | `CS1-EP001-CAMPAIGN-ALPHA@ep001-1.0.0` Gate CG PASS | Quality Gate Owner | Gate CG revoked | Volume cannot remain releasable |
| DEP-ACT-01 | Activation engineering | Multi-day `topic_code` 1.2 / day-key support | Engineering successor | Loader first-match only | Keep `approved` without `released` until fixed |
| DEP-GF-01 | Grandfather / absorption | EA-006 4.2 `pre-campaign-pilot` | Founder | Scale claims citing 4.2 | CS1-003 absorption Volume |
| DEP-SUCC-01 | Prior Volume | None (opening Volume) | — | — | — |
| DEP-SUCC-02 | Successor Volume | CS1-002 (PCA / Chapter 2 arc) | Founder commission | Terminal handoff assumes successor | Produce CS1-002 under EO lifecycle |
| DEP-SUCC-03 | Successor Volume | CS1-003 (4.1→4.2→5.1) | Founder commission | Orphan excellence persists | Produce CS1-003 |

---

## 10. Known defects (Volume-scoped)

| ID | Defect | Severity | Status |
|----|--------|----------|--------|
| VD-01 | Publication Approver signature unsigned | High | Open — blocks `approved` |
| VD-02 | Joint live activation unsupported | High | Open — blocks `released` |
| VD-03 | PCA 1.2.3 out of membership (honest deferral) | Medium | Accepted — successor CS1-002 |
| VD-04 | Does not clear EA-007 spine FAIL | Informational | Expected for Pilot Arc scope |
| VD-05 | Dual-hat staffing risk on early EP reviews | Low | Acknowledged — Approver must remain independent |

No open errata (Volume not released). Revision history: empty operational tickets (educational Revision day CA-R1 is membership, not a publishing revision).

---

## 11. Retirement / replacement plan

| Item | Plan |
|------|------|
| Current retirement status | Not applicable — founding Volume |
| Replacement preference | Successor Volumes extend series; do not silently retire Alpha |
| RT grounds watched | RT-02 CMP unsafe; RT-03 trust FAIL after release; RT-04 scope honesty breach |
| Archive posture | On future supersession, retain Gate CG evidence pack + this dossier |

---

## 12. Reference-bar comparison worksheet

| Alpha floor dimension | CS1-001 evidence | Met? |
|-----------------------|------------------|------|
| Gate CG PASS | Yes | **Yes** |
| CI recorded | 8.75 | **Yes** |
| Bridge integrity 100% | Yes | **Yes** |
| Tutor Review PASS | Yes | **Yes** |
| Founder Review PASS | Yes | **Yes** |
| Auditor issues closed | Yes | **Yes** |
| FP-01…FP-06 denied | Yes | **Yes** |
| Joint inventory | Four certified packages | **Yes** |
| Honesty (scope / PCA / spine) | Explicit non-claims | **Yes** |
| Live activation | Gated; status honest | **Yes** (honesty) / **No** (live path) |

CS1-001 **is** the reference bar. Future Volumes must meet or exceed this floor.

---

## 13. Catalogue paths (substance pointers — not authored in PR-001)

```text
app/curriculum/data/educational_campaigns/cs1/campaign-alpha-ep001/
  campaign.json
  packages/
    1.1-purpose-function-ep001.json
    1.2-eda-summaries-ep001.json
    1.2-eda-association-ep001.json
    revision-purpose-eda-ep001.json
```

Package status: `campaign_member_certified` — outside EA-006 live `publication_approved` loader set.

---

## 14. Closing

Campaign Alpha is formally registered as Educational Volume **CS1-001** under EO-001. Educational certification is complete. Operational publication awaits Approver signature and activation engineering — recorded honestly as `publication_ready`.

Signed notionally: Editorial Office · PR-001 · Volume Register CS1-001 · 2026-08-01
