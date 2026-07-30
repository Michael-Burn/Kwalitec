# REPORT INDEX — Version 2.0.0-beta.1 Archive

**Purpose:** Index every major programme report preserved under this release archive, with purpose, status, relationship to the beta.1 baseline, and historical significance.

**Rule:** Status values are the decisions recorded in the original reports.

---

## Primary lineage (required by AR-001)

### EI-001 — Curriculum Intelligence Engine

| Field | Detail |
|---|---|
| **Paths** | `reports/ei001/EI001A_IMPLEMENTATION_REPORT.md` … `EI001D_IMPLEMENTATION_REPORT.md` |
| **Purpose** | Build generations, memory, regression, Gen7 certification, Decision Ledger, Review Pack. |
| **Status** | Phases A–D **COMPLETE** (reports dated 2026-07-30). |
| **Relationship** | Supplies the certified educational artefact layer that Student Runtime and Founder Preview consume. |
| **Historical significance** | First durable Curriculum Intelligence Engine with certification — without which “certified curriculum” at beta.1 would not exist. |

### EI-002 — Educational Intelligence Integration

| Field | Detail |
|---|---|
| **Paths** | `reports/ei002/EI002A_IMPLEMENTATION_REPORT.md`, `EI002B_IMPLEMENTATION_REPORT.md` |
| **Purpose** | A: Founder publish / certified package gates. B: Student certified learning experience (missions, KG, tutor, progress, observatory). |
| **Status** | EI-002A / EI-002B **COMPLETE**. |
| **Relationship** | Bridges certified engine output into Founder publish and Student EOS surfaces used in Private Beta. |
| **Historical significance** | Marks the moment certified curricula became the student learning path, not only a Founder laboratory artefact. |

### EQ-001 — Educational Quality

| Field | Detail |
|---|---|
| **Path** | `reports/eq001/EQ001_EDUCATIONAL_QUALITY_REPORT.md` |
| **Purpose** | Fix CIP noise (thousands of spurious sections/topics); syllabus-first CS1 structure (5 / 15 / 73). |
| **Status** | Report decision: **EDUCATIONAL QUALITY BLOCKED** (CMP topic over-production residual; live reprocess still required for full realisation) — nonetheless foundational for RR-001’s certified shape. |
| **Relationship** | Defines the educational coherence target that RR-001 later made active in Student Runtime. |
| **Historical significance** | Documents the before/after of curriculum pollution vs syllabus-authoritative hierarchy — the educational quality baseline of beta.1. |

### RR-001 — Release Readiness

| Field | Detail |
|---|---|
| **Path** | `reports/rr001/RR001_RELEASE_READINESS_REPORT.md` |
| **Purpose** | Clear PL-001A closed-beta blockers: active certified package, Gen2 confidence, calibration re-certification. |
| **Status** | **READY FOR CLOSED BETA**. |
| **Relationship** | Immediate predecessor to UX-001 / PB-001 / RC-001 packaging. |
| **Historical significance** | The unblock decision that made Private Beta operationally honest (students see certified CS1, not FV-002 noise). |

### UX-001 — Premium Beta Experience

| Field | Detail |
|---|---|
| **Path** | `reports/ux001/UX001_PREMIUM_BETA_REPORT.md` |
| **Purpose** | Mission-first premium UX polish for Student EOS + Founder Curriculum Health without new educational architecture. |
| **Status** | **PREMIUM PRIVATE BETA READY**. |
| **Relationship** | Defines the look-and-feel and primary CTAs of the beta.1 student/founder journeys. |
| **Historical significance** | Separates “engineering complete” from “invite-ready product surface.” |

### PB-001 — Private Beta Validation

| Field | Detail |
|---|---|
| **Paths** | `reports/pb001/PB001_IMPLEMENTATION_REPORT.md`, `PB001_PRIVATE_BETA_REPORT.md` |
| **Purpose** | Implement beta instrumentation; measure adoption once cohort exists. |
| **Status** | Implementation shipped; validation decision **PRIVATE BETA EXTENSION REQUIRED** (cohort size 0 at report time). |
| **Relationship** | Schema `202607300005` and Beta Dashboard/metrics are part of the deployed beta.1 platform; live cohort validation remains post-archive work. |
| **Historical significance** | Honest empty-cohort baseline — proves the archive captures readiness infrastructure before first users, not fabricated adoption. |

### RC-001 — Release Candidate / Private Beta Deployment

| Field | Detail |
|---|---|
| **Path** | `reports/rc001/RC001_RELEASE_REPORT.md` |
| **Purpose** | Version, document, audit, deploy, and smoke-test `2.0.0-beta.1` on Render. |
| **Status** | **DEPLOYED FOR PRIVATE BETA**. |
| **Relationship** | Official production identity of this archive. |
| **Historical significance** | The deploy certificate of the first Private Beta production release. |

---

## Supporting reports (context)

| Report | Path | Status | Why preserved |
|---|---|---|---|
| PL-001A Live Dogfood | `reports/supporting/PL001A_LIVE_DOGFOOD_REPORT.md` | **BLOCKED** | Explains why RR-001 existed; certified engine vs active catalogue gap. |
| FV-002 Founder Dogfood | `reports/supporting/FV002_END_TO_END_FOUNDER_DOGFOOD_REPORT.md` | End-to-end Founder→Student pipeline certified earlier | Establishes Founder workflow proof preceding EI/EQ/RR refinements. |

---

## Relationship map

```
FV-002 (Founder→Student pipeline)
   → EQ-001 (structure quality)
   → EI-001 (generations + certification)
   → EI-002 (Founder + Student integration)
   → PL-001A (live dogfood BLOCKED)
   → RR-001 (READY FOR CLOSED BETA)
   → UX-001 (premium surfaces)
   → PB-001 (beta infra; empty cohort)
   → RC-001 (DEPLOYED 2.0.0-beta.1)
   → AR-001 (this archive)
```

---

## Completeness

| Required programme | Archived? |
|---|---|
| EI-001 | Yes (A–D) |
| EI-002 | Yes (A–B) |
| EQ-001 | Yes |
| RR-001 | Yes |
| UX-001 | Yes |
| PB-001 | Yes (implementation + validation) |
| RC-001 | Yes |

Original paths under `knowledge/engineering/` remain the living tree; copies here are the **release-bound** historical set.

---

*AR-001 evidence preservation index.*
