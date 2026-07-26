# Change Control

**Programme:** P-003.7 — Product Board Charter  
**Version:** 1.0  
**Status:** Active — Board procedure  
**Effective:** 2026-07-26  
**Companion:** [`PRODUCT_BOARD_CHARTER.md`](PRODUCT_BOARD_CHARTER.md)  
**Does not:** Amend higher-authority documents; rewrite registers in this programme  

---

## 1. Purpose

Define how **governance artefacts** evolve so Version 1 remains auditable: authority is clear, supersession leaves history, and Board approval is required when change alters release or claim posture.

---

## 2. Artefact classes

| Class | Examples | Change sensitivity |
|---|---|---|
| **Higher law** | Vision 2030; Educational Constitution; Architecture Constitution; PSF; P-001.2/1.3; P-002.1 gates | Highest — amend via that document’s own process first |
| **Board procedure** | This Charter folder (P-003.7) | High — version bump + Board ack for material change |
| **Board registers** | Decision / Risk / Assumption registers; Evidence Hierarchy; Claim Standard | High — Lifecycle / Review Process + Board for material posture |
| **Board synthesis** | Release Dossier; Maturity assessment numbers | High when recommendation or heat/level story changes |
| **Programme records** | EP/P completion reports; SIAs; blind reviews | Medium — author owned; must not contradict ACTIVE law |
| **Operational trackers** | `VERSION_1_READINESS.md` | Medium — must mirror evidence; never invent PASS |

---

## 3. When Board approval is required

| Change | Board approval? |
|---|---|
| Material Charter / procedure rewrite | **Yes** (Chair + Product Governance Lead minimum; full Board if release rules change) |
| New ACTIVE DR law/posture or supersession affecting Version 1 behaviour/claims | **Yes** |
| Risk Accepted / Closed that changes release story | **Yes** |
| Assumption Validated / Rejected that underpins GO narrative | **Yes** |
| Evidence Hierarchy level definitions or claim freeze changes | **Yes** |
| Release recommendation class change (GO ↔ NO GO etc.) | **Yes** — Release review |
| Maturity Level 3→4/5 or Red→Green heat on Release Readiness / Effectiveness | **Yes** note (requires E4/E5 citations) |
| Typo / path fix / non-semantic clarification in Board docs | No — Product Governance Lead may land; note in changelog if useful |
| Docs-only programme with ΔKSI = 0 and no posture flip | No meeting required; Lead spot-check |
| Higher-law amendment | Board may **recommend**; cannot silently patch Vision/Constitution/gates via Charter edit |

---

## 4. How artefacts evolve

```
Propose change → Hierarchy check → Evidence / rationale
    → Approval (if required) → Edit with version/date
    → Supersede / archive prior meaning if IDs or recommendations change
    → Cross-link updates (without rewriting foreign law bodies unless that programme allows)
```

### 4.1 Hierarchy check

If the proposed text contradicts a higher-authority document → **STOP**. Document the conflict. Recommend amendment of the higher authority. Do not paper over with Board minutes.

### 4.2 Version control expectations

| Expectation | Rule |
|---|---|
| Git history | Prefer clear commits when a later programme requests them; this P-003.7 package itself required **no commits** |
| Document Version field | Bump on material change (e.g. 1.0 → 1.1) |
| Effective date | Update when Board ack lands |
| IDs | Never reuse `DR-NNN` / `PR-NNN` / `PA-NNN` for a new meaning |
| Supersession | Keep prior text readable (SUPERSEDED / CLOSED / REJECTED indexes) |
| Prefer path-specific changes | Do not mix unrelated WIP in governance commits when commits are requested |

### 4.3 Superseded documents

| Situation | Handling |
|---|---|
| Procedure replaced | New version in place; note prior version in changelog section or completion report |
| Decision meaning changes | Supersede via Decision Lifecycle (`SD-NNN`) |
| Risk closed | Move to CLOSED with proof; keep card history |
| Assumption rejected | Remain in REJECTED index; do not delete |
| Dossier recommendation changes | New synthesis date; prior NO GO/GO remains citable |

Do **not** delete authoritative history to make the present look cleaner.

---

## 5. Change control for this Charter (P-003.7)

| Change type | Process |
|---|---|
| Clarification (no rule change) | Product Governance Lead; bump patch version optional |
| Role / quorum / meeting cadence change | Board ack; minor version bump |
| Release recommendation authority or GO rules change | Full Release-capable quorum; minor/major bump; consistency check vs P-002.1 (P-002.1 wins on conflict) |
| Withdrawal of Charter | Board + Product owner; higher-law note if GOVERNANCE index later links it |

**Conflict rule:** If this Charter ever disagrees with P-002.1 gate law or Vision / Educational Constitution, **those win** until formally amended. Fix the Charter.

---

## 6. What this programme (P-003.7) intentionally did not change

Per constraints, P-003.7 creates this folder only. It does **not**:

- edit `GOVERNANCE.md` or product README indexes,  
- edit Decision / Risk / Assumption / Evidence / Maturity / Dossier bodies,  
- edit release gates,  
- flip NO GO,  
- modify runtime.

A later index programme may link here under change control §3.

---

## 7. Success check

Auditors can answer:

- who approved a governance change,  
- what version is effective,  
- what prior posture was superseded,  
- whether higher law was respected —

from Board records and register history alone.

---

**End of Change Control**
