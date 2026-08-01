# EO-001 — Versioning Guide

**Programme:** Educational Operations Programme EO-001 — Educational Publishing Operations  
**Status:** Binding — Volume version and edition discipline  
**Effective:** 2026-08-01  
**Authority:** EA-001 through EA-008 COMPLETE · EP-001 PASS  
**Nature:** Publishing operations law — not educational architecture redesign, not application code, not Runtime/SCI work, not educational content authoring  
**Parents:** `EO001_EDUCATIONAL_VOLUME_STANDARD.md` · `EO001_PUBLISHING_WORKFLOW.md` · `EA002_PUBLICATION_WORKFLOW.md` §9.3  
**Reference quality bar:** Campaign Alpha (`CS1-EP001-CAMPAIGN-ALPHA` · `ep001-1.0.0`)  

---

## 1. Purpose

Define how Educational Volumes are **versioned, edition-labelled, compared, and superseded** so students and operators always know which guidance is authoritative — and so quality cannot drift through silent overwrite.

### Governing principle

> **A Volume without version discipline is a rumour. A Volume with version discipline is a publication.**

---

## 2. Version identity

### 2.1 Volume version string

Educational Volumes use a three-part version:

```text
MAJOR.MINOR.PATCH
```

Example: `1.0.0` (Campaign Alpha operational mapping may cite Campaign version `ep001-1.0.0` as the member pin inside Volume `1.0.0`).

| Part | Increments when |
|------|-----------------|
| **MAJOR** | Scope class change; membership span redesign; curriculum package major realignment; Replacement that breaks prior completion assumptions; honesty rewrite of journey purpose |
| **MINOR** | Additive educational improvement within same scope class; new certified member day that preserves arc intent; CMP locus refresh that changes teaching moves but not Volume identity |
| **PATCH** | Errata E2 fixes; cosmetic corrections that still require a stamped release; dependency pin clarification without educational redesign |

### 2.2 Pre-release labels (optional)

| Label | Use |
|-------|-----|
| `1.1.0-draft` | Workfile only — never student-reachable |
| `1.1.0-rc.1` | Review candidate — staging / Board only |
| `1.1.0` | Publication-Approvable / releasable form |

Pre-release labels **never** appear as `released` without stripping to a final version via Approval.

### 2.3 Campaign version vs Volume version

| Artefact | Versions | Rule |
|----------|----------|------|
| Educational Package | Package version | Nested; may bump inside Campaign |
| Educational Campaign | Campaign version (e.g. `ep001-1.0.0`) | Gate CG is per Campaign version |
| **Educational Volume** | **Volume version** | Membership snapshot pins exact Campaign versions |

A Volume version **must** record the exact Campaign versions it contains. Changing a member Campaign version requires a Volume version bump of at least PATCH (if errata-equivalent) or MINOR/MAJOR per change class.

---

## 3. Edition labels

### 3.1 Edition vs version

| Concept | Meaning | Example |
|---------|---------|---------|
| **Version** | Machine/ops stamp for exact inventory | `1.2.0` |
| **Edition** | Human publishing label for market/catalogue | `2026 First Edition` · `2026 Second Edition (CMP refresh)` |

Every released Volume carries **both**.

### 3.2 Edition bump rules

Bump the edition label when:

1. CMP edition pin changes  
2. Curriculum package year/alignment changes in a student-meaningful way  
3. MAJOR Volume version increments  
4. Board designates a named catalogue relaunch  

Minor/patch educational improvements may remain within the same edition label if the CMP pin and curriculum package pin are unchanged — but the **version** still increments.

### 3.3 Edition pin fields (required)

| Field | Required |
|-------|----------|
| `edition_label` | Yes |
| `curriculum_package_version` | Yes |
| `cmp_edition` | Yes |
| `effective_from` | Yes for released |
| `effective_to` | When superseded/retired |

---

## 4. Change classes → version impact

Aligned with EA-002 maintenance change classes, extended for Volume operations:

| Change class | Typical version impact | Review depth |
|--------------|------------------------|--------------|
| **Cosmetic** | PATCH (if released stamp needed) or notice-only E1 | Abbreviated Peer Review |
| **Errata E2** | PATCH | Delta Peer + Approver |
| **Errata E3 / Truth-risk** | PATCH minimum after HOLD; MINOR/MAJOR if redesign | Full chain including Founder if arc/claims affected |
| **Educational** | MINOR (same scope) or MAJOR (purpose/span shift) | Full stages for affected artefacts |
| **Structural** | MINOR or MAJOR | Full Gate LE/SS/MG + Gate CG re-entry as needed |
| **Membership add within Pilot intent** | MINOR | Gate CG re-score + Audit |
| **Scope class change** | MAJOR | Full lifecycle from Authoring evidence upward |
| **Retirement / Replacement** | New Volume ID and/or MAJOR; prior → superseded | Full lifecycle for Replacement |

**Smuggling ban:** Cosmetic must not hide educational or truth-risk change.

---

## 5. Version history requirements

### 5.1 Append-only log

Volume version history is append-only. Do not rewrite prior version records. Corrections are new versions or errata linked to the affected version.

### 5.2 Snapshot contents (each version)

| Snapshot element | Required |
|------------------|----------|
| `volume_version` + `edition_label` | Yes |
| Campaign membership pins | Yes |
| Package inventory hashes or IDs | Yes |
| Gate CG refs | Yes |
| Approval record refs | Yes for ≥ `approved` |
| Claims allowed/forbidden | Yes for ≥ `publication_ready` |
| Change class + summary | Yes |
| Supersedes / superseded_by | If any |

### 5.3 Student pinning

Students on a pathway consume a **pinned Volume version**. Migration to a newer version requires:

1. New version APPROVED  
2. Migration / redirect plan  
3. Post-publish verification  
4. Explicit effective_from  

Silent overwrite of released inventory is forbidden.

---

## 6. Compatibility and supersession

### 6.1 Compatibility statements

When releasing a new Volume version, declare one of:

| Statement | Meaning |
|-----------|---------|
| **Drop-in patch** | Same membership intent; safe in-place for same cohort pin after Approval |
| **Additive minor** | New teaching moves; prior completion still meaningful |
| **Breaking major** | Prior Volume completion assumptions may not transfer; Replacement semantics |
| **Edition realignment** | CMP/curriculum pin change; remapping guidance required |

### 6.2 Supersession record

| Field | Required when superseding |
|-------|---------------------------|
| `prior_volume_id` + `prior_version` | Yes |
| `successor_volume_id` + `successor_version` | Yes |
| Redirect behaviour | Yes |
| Student-visible notice | Yes |
| Archive link | Yes |

---

## 7. Working with Campaign Alpha as reference

### 7.1 Baseline pin

| Item | Value |
|------|-------|
| Reference Campaign | `CS1-EP001-CAMPAIGN-ALPHA` |
| Reference Campaign version | `ep001-1.0.0` |
| Reference pattern | AP-01 Certified Pilot Arc |
| Operational lesson | Catalogue certification may precede live release — version status must stay honest |

### 7.2 When Alpha itself versions

If Campaign Alpha receives a new Campaign version:

1. Open Volume revision for the Volume that contains it (or create Volume record if formalising Alpha as Volume One).  
2. Bump Volume version per change class.  
3. Re-run required review depth.  
4. Do not silently treat `ep001-1.0.0` evidence as covering a changed Campaign.

### 7.3 Quality floor across versions

Later versions may improve CI, coverage, or teaching craft. They may **not** regress below Alpha’s operational evidence floor (Gate CG PASS, FP denial, Tutor/Founder/Auditor PASS, joint inventory, claim honesty).

---

## 8. Errata numbering

Errata IDs are independent of Volume versions:

```text
ERRATA-<volume_id>-<yyyy>-<nnn>
```

Example: `ERRATA-CS1-VOL-ALPHA-2026-001`

Each erratum references the Volume version it affects and, when closed via patch, the resulting Volume version.

---

## 9. Archive version preservation

On Archive Acceptance:

1. Freeze the version history log.  
2. Preserve all membership pins and evidence refs.  
3. Record final `effective_to`.  
4. Prohibit further PATCH/MINOR/MAJOR without restoring the Volume to an active lifecycle (which requires a new Commission — typically as Replacement).

---

## 10. Operator quick reference

| I need to… | Do this |
|------------|---------|
| Fix a misleading typo on a released Volume | E1 notice or PATCH + abbreviated review |
| Fix a wrong Tomorrow bridge | E2 → PATCH → delta review → Approver |
| Remove contaminant topic | E3 → HOLD → fix → full recertify → Approver |
| Add a fourth Learning day to a Pilot Arc | MINOR + Gate CG re-score + Audit (+ Founder if claims change) |
| Expand Pilot Arc to Chapter Campaign | MAJOR + full lifecycle |
| Change CMP edition pin | Edition bump + version bump + Founder re-entry |
| Replace Volume entirely | New Commission → new Volume ID or MAJOR Replacement → supersede prior |

---

## 11. Closing rules

1. Version + edition are mandatory for every released Volume.  
2. Membership is pinned by exact Campaign versions.  
3. Change class drives both review depth and version impact.  
4. Append-only history; no silent overwrite.  
5. Alpha floor applies to every future version.

**If you cannot say which version a student saw, you cannot defend what you taught.**

Signed notionally: Editorial Director · EO-001 · Versioning Guide · 2026-08-01
