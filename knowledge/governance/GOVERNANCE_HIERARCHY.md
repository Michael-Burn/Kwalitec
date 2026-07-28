# Governance Hierarchy

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.4 — Educational Governance Constitution  
**Version:** 1.0  
**Status:** Active — Board educational governance hierarchy  
**Effective:** 2026-07-28  
**Authority:** Subordinate to `EDUCATIONAL_GOVERNANCE_CONSTITUTION.md`  
**Companion:** Repository-wide ranks remain in `knowledge/GOVERNANCE.md` (this document specialises *educational* governance)

---

## 1. Purpose

Define the hierarchy, ownership, and precedence of educational governance documents so the Board can always answer: **which document is authoritative?**

Authority flows **downward**. Lower documents must not contradict higher ones. On conflict: **STOP**, document, amend the higher authority first.

---

## 2. Educational governance hierarchy (canonical)

```
Rank E0 — Product philosophy apex
    Vision 2030
         Why · north star · never-build · Final Test

Rank E1 — Educational meaning apex
    Educational Constitution (EGI-001)
         Educational law, truth, integrity

Rank E2 — Educational governance procedure apex
    Educational Governance Constitution (DG-001.4)
         Hierarchy · principles · amendment · compliance · review

Rank E3 — Educational philosophy filters
    Educational Philosophy (ILE-000)
    Study Sensei Philosophy (ILE-010)
         (+ companions: Guidance over Content, Student Relationship Model, …)

Rank E4 — Vocabulary law
    Canonical Educational Lexicon (DG-001.1)
         + Vocabulary Map · Term Deprecation Register · Language Style Guide

Rank E5 — Authority law
    Educational Authority Model (DG-001.2)
         + Authority Transition Map · Decision Matrix · Conflict Register

Rank E6 — Reflection law
    Reflection Architecture (DG-001.3)
         + Lifecycle · Relationship Matrix · Governance Rules (RG-01–RG-20)

Rank E7 — Educational integrity / review standards
    EGI-002 Educational Logic Registry
    EGI-003 Educational Governance Review Standard
    EIP specialised standards (evidence, explainability speech, continuity, …)
    Programme VI educational domain models

Rank E8 — Product quality gates (speech / recommendations)
    Explainability Standard (P-001.2)
    Recommendation Quality Standard (P-001.3)
    Student Decision Framework (ILE-011) — agency / silence

Rank E9 — Educational release quality
    Educational Validation Framework (EVF) → Release Gate

Rank E10 — Implementation standards & code
    Engineering Standards · Architecture Constitution · ADRs
    Application code · templates · copy
```

---

## 3. Rank table with ownership

| Rank | Document | Canonical path | Owns | Owner capacity |
|------|----------|----------------|------|----------------|
| E0 | Vision 2030 | `knowledge/product/vision/PRODUCT_VISION_2030.md` | Product philosophy | Founder — Product Owner |
| E1 | Educational Constitution | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational meaning / truth | Founder — Educational Gate Owner |
| E2 | Educational Governance Constitution | `knowledge/governance/EDUCATIONAL_GOVERNANCE_CONSTITUTION.md` | Educational governance procedure | Founder — Educational Gate Owner |
| E3a | Educational Philosophy | `knowledge/product/EDUCATIONAL_PHILOSOPHY.md` | ILE learning beliefs | Founder — Educational Gate Owner |
| E3b | Study Sensei Philosophy | `knowledge/product/STUDY_SENSEI_PHILOSOPHY.md` | Mentor identity / decision filter | Founder — Educational Gate Owner |
| E4 | Canonical Educational Lexicon | `knowledge/governance/CANONICAL_EDUCATIONAL_LEXICON.md` | Educational naming | Founder — Educational Gate Owner |
| E5 | Educational Authority Model | `knowledge/governance/EDUCATIONAL_AUTHORITY_MODEL.md` | Who may speak | Founder — Educational Gate Owner |
| E6 | Reflection Architecture | `knowledge/governance/REFLECTION_ARCHITECTURE.md` | Reflection system law | Founder — Educational Gate Owner |
| E7 | EGI-002 / EGI-003 / EIP | `knowledge/educational/` | Logic registry; integrity review | Founder — Educational Gate Owner |
| E8 | P-001.2 / P-001.3 / ILE-011 | `knowledge/product/…` | Explainability; recommendation quality; agency | Founder — Product + Educational capacities |
| E9 | EVF | `knowledge/educational_validation/` | Trust sufficient to release | Founder — Educational Gate Owner |
| E10 | Architecture + code | `docs/`, `ARCHITECTURE.md`, `app/` | Structure and behaviour | Founder — Engineering Owner |

---

## 4. Relationship to repository meta-governance

`knowledge/GOVERNANCE.md` defines repository-wide ranks (Vision → Blueprint → KSI → … → Educational Constitution → EVF → Architecture → …).

This document **does not replace** that table. Mapping:

| GOVERNANCE.md | This hierarchy |
|---------------|----------------|
| Rank 1 Vision | E0 |
| Rank 3 Educational Constitution | E1 |
| *(not previously ranked as procedure apex)* | **E2 Educational Governance Constitution** |
| ILE philosophy band (parallel under Rank 1–3) | E3 |
| *(DG-001 corpus previously unranked)* | **E4–E6** |
| EGI / EIP under Rank 3 | E7 |
| Rank 2b / 2c / ILE-011 | E8 |
| Rank 4 EVF | E9 |
| Rank 5–7 + code | E10 |

**Rule:** When choosing authorities, start with `GOVERNANCE.md` for product / release / architecture decisions; use **this hierarchy** for educational vocabulary, authority, reflection, and DG-001 compliance.

---

## 5. Precedence rules

### 5.1 Vertical precedence

1. Lower ranks must not contradict higher ranks.  
2. Implementation (E10) never governs Constitutions (E1–E2).  
3. DG-001.1–3 (E4–E6) must not contradict Educational Governance Constitution (E2) or EGI-001 (E1).  
4. Philosophy filters (E3) specialise Vision and EGI-001; they do not invent a second north star.

### 5.2 Horizontal precedence within DG-001

When two DG-001 instruments appear to conflict:

```
1. Apply Educational Governance Constitution principles (CP-01–CP-10)
2. Prefer the instrument that owns the domain:
      naming → Lexicon (E4)
      permission to speak → Authority (E5)
      reflection storage / narrative → Reflection (E6)
3. If still unresolved → STOP and open amendment proposal
```

### 5.3 Dual educational apex reminder

| Conflict type | Winner |
|---------------|--------|
| Educational *meaning* vs governance *procedure* | E1 Educational Constitution |
| Two DG-001 instruments | E2 Constitution principles + domain owner (E4/E5/E6) |
| Product marketing claim vs educational honesty | Educational honesty (CP-07) under E0 Final Test + E1 + E2 |
| PX / Product Language vs Lexicon educational meaning | Lexicon for educational meaning; reconcile PX in implementation (OQ-01) |
| Voice Guide tone vs Authority domains | Authority owns *who*; Voice owns *how* |
| Ubiquitous Language vs Lexicon student-facing terms | Lexicon for student-facing educational terms |
| EVF release quality vs DG-001 law | Complementary — both required; EVF does not amend vocabulary/authority/reflection law |
| Alpha / RP certification observations vs DG-001 law | DG-001 law governs remediation; RP evidence informs residuals |

---

## 6. Related corpora positions

### 6.1 ILE governance

ILE philosophy and frameworks (Educational Philosophy, Study Sensei, Product Principles, Student Decision Framework, Mission / Timeline / Journal philosophies) sit at **E3 / E8**. They are permanent decision filters. They must cite DG-001 when naming speakers, terms, or reflection.

### 6.2 Product Language Guide / PX

`knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md` and PX programmes govern UI microcopy conventions. For educational concepts, **E4 Lexicon supersedes** conflicting PX synonyms. Reconciliation is an implementation programme residual (DG-001.1 OQ-01) — not a licence to ignore the lexicon.

### 6.3 Voice Guide

`knowledge/release/RP-001/VOICE_GUIDE.md` informs tone. It does not create a fourth speaker or reassign DG-001.2 domains.

### 6.4 Ubiquitous Language

`UBIQUITOUS_LANGUAGE.md` remains engineering domain language. Student-facing educational vocabulary defers to **E4**.

### 6.5 Release governance

Release Playbook, Protocol, and P-002.1 consume educational outcomes. They do not define Mission, Study Sensei, or reflection. Ship claims that imply educational vocabulary/authority/reflection consistency must cite DG-001 compliance.

### 6.6 Alpha certification governance

RP-001 audits and Educational Drift Registers are **evidence and residual trackers**. They do not outrank E2–E6. Closure of ED-* items requires implementation evidence under this hierarchy.

---

## 7. Conflict resolution procedure

```
Detect conflict
    ↓
Classify: meaning (E1) | governance procedure (E2) | naming (E4) | speech (E5) | reflection (E6) | other
    ↓
Apply vertical precedence (higher rank wins)
    ↓
If peers: apply horizontal domain ownership
    ↓
If still open: STOP shipping educational claims
    ↓
Open amendment per GOVERNANCE_AMENDMENT_PROCESS.md
    ↓
Do not paper over with local README or PR prose
```

---

## 8. Practical navigation

| Question | Authoritative rank |
|----------|-------------------|
| What does “Mission” mean for students? | E4 Lexicon |
| Who may explain why today’s Mission was chosen? | E5 Authority (Study Sensei) |
| Is Product Check-in a reflection? | E6 Reflection (No) |
| May we invent a second mentor name? | E2 CP-10 + E5 (No) |
| Does mastery language violate honesty? | E1 + E2 CP-07/CP-08 + E4 |
| Is educational quality enough to release? | E9 EVF |
| Is Version 1 production-ready? | P-002.1 (repository Rank 2d) — not this hierarchy alone |
| How do we amend the lexicon? | E2 + `GOVERNANCE_AMENDMENT_PROCESS.md` |

---

## 9. Supersession note

This document **supersedes** the 2026-07-28 repository hierarchy *audit snapshot* previously published at this path for DG-001 audit purposes. Repository-wide ranks remain authoritative in `knowledge/GOVERNANCE.md`. Historical audit companions (`GOVERNANCE_AUDIT.md`, `GOVERNANCE_OVERLAP_MATRIX.md`, `GOVERNANCE_RECOMMENDATIONS.md`) remain evidence; they do not outrank this hierarchy.

---

**End of GOVERNANCE_HIERARCHY**
