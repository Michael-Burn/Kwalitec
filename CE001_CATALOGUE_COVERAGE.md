# CE-001 — Certified Catalogue Coverage

**Programme:** Catalogue Expansion Programme CE-001 — Certified Educational Catalogue Expansion  
**Phase:** Certified Educational Catalogue Expansion  
**Status:** Binding — coverage definition for Editorial Operations  
**Effective:** 2026-08-01  
**Authority:** EA-001…EA-008 (Frozen) · EP-001 PASS · EO-001 PASS · PR-001 PASS · COMMISSION-CS1-002 PASS · DX-001 PASS  
**Nature:** Catalogue measurement law — **no** educational redesign; **no** operations redesign; **no** Runtime/application/SCI/Twin changes; **no** new governance frameworks  

---

## 1. Purpose

Define **Certified Catalogue Coverage** so the Editorial Office can expand CS1 educational inventory honestly — counting only journeys students may depend on, never drafts, orphans, or quality theatre.

The Educational Excellence Framework is complete and frozen. Coverage measurement consumes that law; it does not invent new gates.

---

## 2. Definition

### 2.1 Certified Catalogue Coverage

A syllabus learning objective (LO) is **covered** in the Certified Educational Catalogue if and only if **all** of the following hold for a Learning day (or Revision day that lawfully returns to that LO) that includes the LO in its certified span:

| # | Requirement | Authority |
|---|-------------|-----------|
| 1 | **Mission certified** | Gate MG PASS (EA-003 / EA-001) |
| 2 | **Session certified** | Gate SS (+ LE / TP / RV as applicable) PASS (EA-004 / EA-001) |
| 3 | **Campaign certified** | Gate CG PASS for the Campaign that owns the package (EA-008) |
| 4 | **Publication approved** | Human Publication Approver signature; Volume status ≥ `approved` (EO-001) |

**Drafts do not count.**  
**Package-only excellence without Campaign membership does not count.**  
**`publication_ready` without Approver signature does not count.**  
**`released` / live activation is necessary for student reachability, but coverage *credit* begins at Publication Approval (requirement 4). Activation without Approval is forbidden.**

### 2.2 One-line law

> Coverage is certified journey under Approver seal — not authored files on disk, not Gate CG alone, not orphan Golden days.

### 2.3 Unit of measurement

| Grain | Use |
|-------|-----|
| **Primary — Learning Objective (LO)** | Official CS1 2026 `learning_objectives[].code` (e.g. `2.1.3`) |
| **Secondary — Topic** | Topic code (e.g. `2.1`) — reported as Full / Partial / Missing |
| **Tertiary — Section** | Chapter-family (e.g. Section 2) — reported as coverage % of LOs |
| **Operational — Volume / Campaign** | Publishing unit that carries Approval |

Revision days do not create new LO coverage; they protect memory of LOs already claimed by Learning membership.

---

## 3. Coverage statuses (pipeline map)

The Coverage Map uses these statuses. Only **Published** contributes to the certified coverage numerator.

| Status | Meaning | Counts toward coverage? |
|--------|---------|-------------------------|
| **Published** | Mission + Session + Campaign certified **and** Publication Approver signed (Volume ≥ `approved`) | **Yes** |
| **Awaiting Approval** | Gate CG PASS; Volume at `publication_ready`; Approver signature pending | No |
| **Certified** | Package gates + Campaign Gate CG PASS; not yet advanced to Publication Readiness / Approver queue | No |
| **Under Review** | Authored inventory in Tutor / Auditor / Founder review; Gate CG not yet PASS | No |
| **Under Authoring** | Commissioned Volume in Authoring under EO Stage lifecycle; substance not yet complete | No |
| **Missing** | No catalogue Campaign membership claiming the LO | No |

### 3.1 Orphan package rule

An LO may have Mission/Session certification and even package-level publication history (e.g. EA-006 `4.2`) **without** Campaign Gate CG membership. Such LOs remain **Missing** for Certified Catalogue Coverage, annotated `Missing*` when a grandfather package exists.

**Rationale:** EA-007 / EA-008 forbid Isolated Golden Day claims. Coverage without Campaign certification would recreate the orphan excellence anti-pattern.

---

## 4. Coverage metrics

### 4.1 Required metrics (subject = CS1 2026)

| Metric | Formula |
|--------|---------|
| **LO Coverage Rate** | (# LOs with status Published) / (# LOs in official syllabus) |
| **Topic Full Coverage Rate** | (# topics with every LO Published) / (# topics) |
| **Pipeline Inventory** | Count of LOs in Awaiting Approval + Certified + Under Review + Under Authoring |
| **Gap Inventory** | Count of LOs Missing (incl. Missing*) |
| **Continuity Front** | Lowest syllabus-order LO that is Missing after the contiguous Published (or, pre-release, Awaiting Approval) opening arc |

### 4.2 Honesty constraints

| Forbidden claim | Why |
|-----------------|-----|
| “CS1 covered” from Pilot Arc LO % | FP-02 Coverage mirage |
| Counting `campaign_member_certified` as Published | Approver not signed |
| Counting EA-006 `4.2` as catalogue coverage | Campaign absent |
| Spine / semester readiness from LO Coverage Rate alone | EA-007 FAIL until contiguous arcs re-audit PASS |
| Equating chapter calendar fill with student continuity | Continuity follows handoffs, not chapter labels |

### 4.3 Relationship to Volume status (EO-001)

```text
draft → in_review → certified → publication_ready → approved → released
                              ↑                      ↑
                         map: Certified/        map: Published
                         Awaiting Approval      (coverage counts)
```

`released` remains required for student pathway activation; CE-001 coverage credit starts at `approved`.

---

## 5. Continuity Front (production steering)

Certified Catalogue Expansion is steered by the **Continuity Front**, not by chapter-completion percentage.

| Concept | Definition |
|---------|------------|
| **Opening Continuity Front** | The next LO a diligent first-pass student needs after the last contiguous certified (pipeline or Published) day |
| **Trust Remediation Front** | Syllabus geography where orphan excellence or EA-007 trust breaks sit (currently mid-spine `4.1→4.2→5.1`) |
| **Memory Front** | Revision placements required so early Published LOs do not decay while later arcs are authored |

**Production law:** Maximise movement of the Opening Continuity Front under Alpha quality bar; schedule Trust Remediation so it lands before a cohort reaches that geography; never fill distant chapters while the Front is open.

---

## 6. Evidence sources (measurement inputs)

| Input | Role |
|-------|------|
| `app/curriculum/data/ifoa/cs1/2026.json` | Official LO universe |
| Campaign / Volume dossiers (EP-001, CS1-002, PR-001) | Certification + status |
| Gate CG reports | Campaign certified? |
| Publication Readiness + Approver records | Publication approved? |
| `educational_packages/` live path | Detect orphans (Missing*) — not coverage credit |
| DX-001 continuity findings | Validate Continuity Front placement |

---

## 7. What this document is not

| Not | Why |
|-----|-----|
| New educational architecture | EA frozen |
| New publishing operations law | EO frozen |
| Content commission or authoring | Production programmes do that |
| Runtime / SCI / Twin / recommendation work | Explicitly out of scope |
| A claim that CS1 is exam-ready | Coverage Rate must stay honest |

---

## 8. Closing

Students must be able to depend on Kwalitec from their first study day until the examination. That dependence is impossible without an honest coverage measure. Certified Catalogue Coverage is the Editorial Director’s yardstick: expand only what is Mission-certified, Session-certified, Campaign-certified, and Publication-approved — at Alpha quality — advancing the Continuity Front without ever lowering the bar.

**Companion artefacts:** `CE001_CS1_COVERAGE_MAP.md` · `CE001_PRODUCTION_PRIORITY.md` · `CE001_IMPLEMENTATION_REPORT.md`

Signed notionally: Editorial Director · CE-001 · Certified Catalogue Coverage · 2026-08-01
