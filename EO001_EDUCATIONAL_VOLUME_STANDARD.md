# EO-001 — Educational Volume Standard

**Programme:** Educational Operations Programme EO-001 — Educational Publishing Operations  
**Status:** Binding — operational publishing artefact standard  
**Effective:** 2026-08-01  
**Authority:** EA-001 through EA-008 COMPLETE · EP-001 PASS  
**Nature:** Publishing operations law — not educational architecture redesign, not application code, not Runtime/SCI work, not educational content authoring  
**Parents:** `EA008_EDUCATIONAL_CAMPAIGN_ARCHITECTURE.md` · `EA008_CAMPAIGN_PUBLICATION_POLICY.md` · `EA002_PUBLICATION_WORKFLOW.md` · `EP001_PUBLICATION_READINESS.md`  
**Reference quality bar:** Campaign Alpha (`CS1-EP001-CAMPAIGN-ALPHA` · `ep001-1.0.0`)  

---

## 1. Purpose

Define the **Educational Volume** as Kwalitec’s operational publishing artefact — the unit of record that Editorial Operations produce, review, version, approve, maintain, retire, replace, and archive.

### Governing distinction

| Layer | Artefact | Question answered |
|-------|----------|-------------------|
| Educational architecture (EA) | Mission / Package / Campaign | What educational law must substance obey? |
| Educational production (EP) | Certified Campaign inventory | Was this journey authored to bar? |
| **Publishing operations (EO)** | **Educational Volume** | May we **operate** this journey as a durable publication product — with identity, editions, approvals, errata, and retirement — without quality drift? |

EA defines education. EP produces education. **EO governs how education is published as an enduring house product.**

---

## 2. Definition

### 2.1 Educational Volume

An **Educational Volume** is a named, versioned, Board-governed publishing product that packages one or more certified Educational Campaigns (or certified Pilot Arcs) into a single operational unit of record for production, approval, maintenance, and retirement.

```text
Educational Volume
  ├── Volume identity + edition metadata
  ├── Campaign membership (ordered certified Campaigns / Pilot Arcs)
  │     └── Educational Packages (Mission bundles + Revision placements)
  ├── Publication status + approval history
  ├── Version / revision / errata history
  ├── Dependencies (CMP edition, curriculum package, prior Volumes)
  └── Retirement / replacement / archive policy
```

### 2.2 What a Volume is not

| Is not | Why |
|--------|-----|
| A single Mission or Educational Package | Day inventory remains atomic inside Campaigns (EA-002 / EA-008) |
| A substitute for Gate CG | Volumes may advance only when member Campaigns hold Gate CG PASS |
| An application release | Technical deploy ≠ educational publication (EA-002 §8) |
| A marketing claim of semester readiness | Scope class honesty remains mandatory (EA-008) |
| A Runtime or SCI object | No Twin / recommendation / readiness redesign lives here |

### 2.3 Relationship to Campaign (publication primacy preserved)

| Rule | Statement |
|------|-----------|
| **Educational primacy** | The **Campaign** remains the primary *educational* publication unit (EA-008). |
| **Operational primacy** | The **Volume** is the primary *operational* publishing unit for Editorial Operations. |
| **Membership** | A Volume may expose student-reachable inventory only through certified Campaign members. |
| **No Golden Volume** | A Volume that contains an orphan premium day without certified Campaign membership is **REJECTED** (inherits FP-01). |

**One-line law:** Students experience Campaigns; the house publishes Volumes.

---

## 3. Volume identity

Every Educational Volume records a stable identity block. Identity fields are immutable after first Publication Approval except via a new Volume ID (replacement) or Board-recorded rename with redirect.

### 3.1 Required identity fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `volume_id` | string | Yes | Stable house ID, e.g. `CS1-VOL-ALPHA` |
| `volume_title` | string | Yes | Human title, e.g. “Campaign Alpha — From Purpose to Exploratory Judgement” |
| `subject_id` | string | Yes | e.g. `cs1` |
| `curriculum_package_version` | string | Yes | Official syllabus package pin |
| `cmp_edition` | string | Yes | CMP / Core Reading edition pin |
| `scope_class` | enum | Yes | `pilot_arc` \| `chapter` \| `first_pass_spine` \| `revision` \| `multi_campaign` |
| `series` | string | Yes | Named series (e.g. `CS1 Educational Volumes`) |
| `sequence_in_series` | integer or null | Optional | Ordered place in series when known |
| `reference_bar` | string | Yes | Quality reference Volume/Campaign, initially `CS1-EP001-CAMPAIGN-ALPHA@ep001-1.0.0` |
| `created_at` | date | Yes | First dossier date |
| `owner_role` | enum | Yes | Current operational owner (see Roles) |

### 3.2 Identity tests

| ID | Test | Fail if |
|----|------|---------|
| VI-01 | `volume_id` unique within subject | Collision with another live or archived Volume |
| VI-02 | Title names educational journey, not calendar coverage alone | “CS1 Topics 1–14” without journey intent |
| VI-03 | Scope class matches contained Campaigns | Pilot Arc labelled as Spine |
| VI-04 | CMP + curriculum pins declared | Missing edition honesty |
| VI-05 | Reference bar cited | No quality anchor for peer comparison |

---

## 4. Campaign membership

### 4.1 Membership inventory

A Volume’s **Campaign membership** is the ordered list of certified Campaigns (or Pilot Arcs) that constitute the Volume’s educational substance.

| Field | Required | Notes |
|-------|----------|-------|
| `campaign_id` | Yes | EA-008 Campaign identity |
| `campaign_version` | Yes | Exact certified version |
| `gate_cg` | Yes | Must be `PASS` for publishable membership |
| `order_index` | Yes | Contiguous journey order inside the Volume |
| `role_in_volume` | Yes | `primary` \| `prerequisite` \| `revision_companion` \| `absorption_target` |
| `package_inventory_ref` | Yes | Pointer to Campaign package list |
| `continuity_index` | Yes | Recorded CI at membership certification |
| `bridge_integrity` | Yes | Recorded bridge integrity % |

### 4.2 Membership rules

1. **No uncertified members.** Draft Campaigns may appear in a Volume *workfile*; they may not appear in a Publication-Approved Volume inventory.  
2. **Joint inventory.** Publication Approval applies to the Volume’s declared membership set — not to a cherry-picked day.  
3. **Absorption explicit.** Grandfathered packages (e.g. EA-006 4.2 `pre-campaign-pilot`) enter a Volume only when absorbed into a Gate CG PASS Campaign first.  
4. **Scope honesty.** Membership span must match `scope_class`.  
5. **Alpha bar.** New Volumes must meet or exceed Campaign Alpha’s operational evidence floor (Gate CG PASS, Tutor/Founder/Auditor PASS, FP-01…FP-06 denied, CI and bridge integrity recorded).

### 4.3 Minimum publishable Volume

| Scope class | Minimum membership |
|-------------|-------------------|
| Pilot Arc Volume | ≥ 1 certified Pilot Arc (≥ 3 contiguous Learning packages + Revision Strategy minimum) |
| Chapter Volume | ≥ 1 certified Chapter Campaign |
| Spine Volume | Certified First-pass Spine Campaign + EA-007-method re-audit PASS |
| Revision Volume | Certified Revision Campaign returning to named prior Learning Volumes |
| Multi-Campaign Volume | Ordered certified Campaigns with inter-Campaign handoff declared |

---

## 5. Publication status

### 5.1 Status enum

| Status | Meaning | Student-reachable? |
|--------|---------|-------------------|
| `draft` | Workfile exists; authoring incomplete | No |
| `in_review` | Peer / audit / founder stages in progress | No |
| `certified` | Educational certification complete; Volume not yet Publication-Approved | No |
| `publication_ready` | All operational preconditions met; Approver worksheet open | No |
| `approved` | Publication Approver signed; activation may proceed | Gated until release |
| `released` | Approved inventory on student pathway | Yes (scoped) |
| `hold` | Temporary trust block; honesty required | No (or partial with honesty) |
| `errata_open` | Released with active errata cycle; severity governs exposure | Conditional |
| `superseded` | Replaced by a newer Volume/edition; redirect declared | No (redirect) |
| `retired` | Withdrawn from pathways; not deleted | No |
| `archived` | Cold storage; evidence preserved | No |

### 5.2 Status transitions (normative summary)

```text
draft → in_review → certified → publication_ready → approved → released
                                                              ↓
                                                    errata_open ↔ released
                                                              ↓
                                                         hold → (recertify) → released
                                                              ↓
                                                         superseded → retired → archived
```

Illegal transitions include: `draft → released`, `in_review → approved`, `hold → released` without recertification, and `retired → released` without a new Volume/edition lifecycle.

### 5.3 Status honesty rules

1. `certified` ≠ `approved` ≠ `released`.  
2. Catalogue certification without live activation (EP-001 posture) maps to `certified` or `publication_ready`, never silent `released`.  
3. Marketing copy may only claim the status the Volume actually holds.  
4. `pre-campaign-pilot` packages are not Volumes and must not be labelled as Volumes.

---

## 6. Version history

Every Volume maintains an append-only **version history**. See `EO001_VERSIONING_GUIDE.md` for numbering rules.

### 6.1 Version record (minimum)

| Field | Required |
|-------|----------|
| `volume_version` | Yes (e.g. `1.0.0`) |
| `edition_label` | Yes (e.g. `2026 First Edition`) |
| `change_class` | Yes (`cosmetic` \| `educational` \| `structural` \| `truth_risk` \| `errata` \| `retirement`) |
| `summary` | Yes |
| `campaign_membership_snapshot` | Yes |
| `approval_refs` | Yes when status ≥ `approved` |
| `effective_from` | Yes for released versions |
| `supersedes` | If any |

### 6.2 History invariants

1. Prior released versions remain readable in the archive even after supersession.  
2. Students on a pathway are pinned to an approved Volume version (EA-002 version pinning extended to Volume).  
3. Mixing draft membership into a released version is forbidden.

---

## 7. Approval history

### 7.1 Approval record types

| Record | Signer | Required for |
|--------|--------|--------------|
| Peer Review PASS | Educational Reviewer | Enter Educational Audit |
| Educational Audit PASS | Academic Auditor | Enter Founder Review |
| Founder Review PASS | Founder (or Founder Educational Gate Owner) | Enter Publication Approval |
| Publication Approval | Publication Approver | `approved` / release |
| HOLD / Unpublish | Publication Approver or Gate Owner | Trust intervention |
| Retirement Approval | Publication Approver + Founder (for commercial Volumes) | `retired` |
| Archive Acceptance | Publication Approver | `archived` |

### 7.2 Approval history fields (minimum)

| Field | Required |
|-------|----------|
| `record_id` | Yes |
| `volume_id` + `volume_version` | Yes |
| `stage` | Yes |
| `outcome` | `PASS` \| `FAIL` \| `HOLD` \| `APPROVED` \| `REJECTED` \| `PARTIAL_HOLD` |
| `signer_role` + `signer_name` | Yes |
| `date` | Yes |
| `evidence_refs` | Yes |
| `defects_closed` | If rework loop |
| `claims_allowed` / `claims_forbidden` | For Publication Approval |

Automation may assemble packs. **Automation alone may not APPROVE commercial Volume publication.**

---

## 8. Dependencies

### 8.1 Dependency classes

| Class | Examples | Break action |
|-------|----------|--------------|
| **Curriculum** | Subject package version, leaf nodes, weights | Impact inventory + possible Volume HOLD |
| **CMP** | Edition / locus pagination | Re-verify Reading Guidance; recertify affected members |
| **Campaign** | Member Campaign versions, Gate CG validity | Volume cannot remain `released` if Gate CG revoked |
| **Prior Volume** | Prerequisite journey completion | Declare; do not silently assume |
| **Activation engineering** | Loader day-key support, joint inventory publish | May keep Volume `approved` but not `released` |
| **Grandfather / absorption** | EA-006 4.2 pilot | Explicit; scale claims frozen until absorbed |

### 8.2 Dependency register (required)

Every Volume dossier includes a dependency register with: dependency ID, class, pin/version, owner, break trigger, and remediation path.

---

## 9. Revision history

### 9.1 Revision vs version

| Term | Meaning |
|------|---------|
| **Revision request** | Operational ticket asking to change a Volume (defect, CMP drift, tutor complaint, erratum) |
| **Volume version bump** | Published outcome of accepted revision work under versioning rules |
| **In-Campaign Revision day** | Educational Revision placement (EA-008) — *not* the same as a publishing revision |

### 9.2 Revision history fields

| Field | Required |
|-------|----------|
| `revision_request_id` | Yes |
| `opened_by` / `date` | Yes |
| `trigger` | Yes (see Operations) |
| `severity` | Yes |
| `affected_membership` | Yes |
| `change_class` | Yes |
| `resolution` | `accepted` \| `rejected` \| `deferred` \| `errata` \| `supersede` |
| `resulting_volume_version` | If published |
| `closed_by` / `date` | Yes when closed |

---

## 10. Retirement policy

### 10.1 Retirement grounds (any one sufficient)

| ID | Ground |
|----|--------|
| RT-01 | Superseded by a certified Replacement Volume |
| RT-02 | Curriculum / CMP edition renders substance educationally unsafe |
| RT-03 | Persistent trust FAIL (EV-001 / EA-007 method) after HOLD and failed remediation |
| RT-04 | Scope class honesty breach (e.g. Pilot Arc marketed as Spine) that cannot be corrected by errata |
| RT-05 | Board strategic withdrawal (subject exit, series redesign) |

### 10.2 Retirement process (summary)

```text
RETIREMENT PROPOSAL
  → Impact inventory (students, pathways, dependent Volumes)
  → Replacement plan OR honest unavailable plan
  → Founder acknowledgement (commercial Volumes)
  → Publication Approver signs RETIRED
  → Pathway removal + student-visible honesty
  → Archive acceptance
```

### 10.3 Retirement rules

1. **Retirement ≠ deletion.** Evidence packs remain archived.  
2. **Replacement preferred.** Where a successor Volume exists, students are redirected.  
3. **No silent decay.** A released Volume that fails trust must HOLD or retire — not linger as premium theatre.  
4. **Member Campaign certification** may remain historically valid while Volume publication is withdrawn (EA-008 §13.2 posture extended).

---

## 11. Volume dossier (required work product)

Every Educational Volume maintains a **Volume Dossier** containing at minimum:

1. Identity block (§3)  
2. Campaign membership inventory (§4)  
3. Publication status + transition log (§5)  
4. Version history (§6)  
5. Approval history (§7)  
6. Dependency register (§8)  
7. Revision / errata history (§9; Operations)  
8. Retirement / replacement plan (§10)  
9. Reference-bar comparison worksheet (vs Campaign Alpha floor)  
10. Claims allowed / forbidden for the current status  

The dossier is the operational source of truth. Educational architecture docs remain superior for *educational* law; the dossier does not rewrite EA/EP.

---

## 12. Reference Volume (Campaign Alpha)

Until a later Board designation, **Campaign Alpha** is the **reference quality bar** for Educational Volumes:

| Dimension | Alpha floor (must meet or exceed) |
|-----------|-----------------------------------|
| Educational certification | Gate CG PASS |
| Continuity | CI recorded; bridge integrity 100% on Alpha |
| Voice | Tutor Review PASS |
| Catalogue bar | Founder Review PASS |
| Audit | Educational Auditor issues closed |
| Forbidden patterns | FP-01…FP-06 denied |
| Joint inventory | All days certified substance |
| Honesty | Scope claims constrained; PCA/spine non-claims explicit |
| Live activation | May remain gated — but status honesty required |

Future Volumes may improve on Alpha. They may not lower the floor by institutional memory or schedule pressure.

---

## 13. Closing rules

1. The Educational Volume is the operational publishing artefact.  
2. Campaigns remain the educational publication unit inside Volumes.  
3. Identity, membership, status, approvals, dependencies, revisions, and retirement are mandatory Volume fields.  
4. Campaign Alpha sets the quality bar; EO prevents drift below it.  
5. No Volume reaches students without Publication Approval for a named Volume version.

**The house publishes Volumes. Students trust journeys. Operations keep both true across years.**

Signed notionally: Editorial Director · EO-001 · Educational Volume Standard · 2026-08-01
