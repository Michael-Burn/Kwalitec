# Architecture Decision Record Standard

**Programme:** OA-001 — Operational Architecture & Product Lifecycle Framework  
**Version:** 1.0  
**Status:** Active  
**Effective:** 2026-07-28  
**Authority:** Architecture Constitution · `knowledge/GOVERNANCE.md` §5 · Product Constitution PC-06  
**Constraint:** Process standard only — does not itself change runtime behaviour.

---

## 1. Purpose

Architecture Decision Records (ADRs) are the **binding record** of structural choices. This standard defines when an ADR is required, where it lives, what it must contain, and how it is accepted, amended, or superseded.

**Law (Product Constitution PC-06):** Architecture decisions are documented **before** implementation.

---

## 2. When an ADR is required

An ADR (new or amended) is **mandatory** before merge when the change:

- Alters runtime, layering, or composition-root boundaries.
- Changes educational authority ownership (who may decide missions, plans, progress, recommendations, explanations).
- Introduces or retires a dual path (e.g. Contained legacy vs sole-runtime).
- Changes Curriculum Engine traversal contracts or V1/V2 coexistence rules.
- Adds a new persistence model for educational truth or evidence.
- Introduces network calls, CDNs, or third-party intelligence into learning paths.
- Changes feature-flag architecture that affects educational claim classes.
- Creates a new bounded context or splits an existing one.

### ADR not required (still document in PR / completion report)

- Pure documentation / governance process (unless it redefines architectural law).
- Local bugfixes within an Accepted ADR’s envelope.
- Presentation-only copy under Contained rules with no authority change.
- Test-only or CI-config changes that do not alter architectural invariants (architecture *tests* that encode new law may need an ADR).

**When uncertain:** write the ADR. Prefer a short Accepted ADR over silent divergence.

---

## 3. ADR trees (canonical homes)

| Tree | Use for | Index |
|------|---------|-------|
| `docs/adr/` | Educational OS / Version 2 boundary decisions (primary) | `docs/adr/README.md` |
| `knowledge/architecture/` | Historical Flask / curriculum ADRs | `knowledge/architecture/adrs/README.md` |
| `knowledge/version2/ARCHITECTURE_DECISIONS/` | V2 Learning Journey educational architecture | `knowledge/version2/README.md` |
| `docs/architecture/` | Additional specialised architecture ADRs | Linked from indexes |

**Rule:** New EOS boundary decisions go to **`docs/adr/`** unless a programme explicitly authorises another tree. Do not fork the same decision into two Accepted ADRs.

---

## 4. Required ADR structure

Every new ADR must include:

```markdown
# ADR-NNN — Title

**Status:** Proposed | Accepted | Superseded | Deprecated  
**Date:** YYYY-MM-DD  
**Programme / Milestone:** …  
**Authority:** Architectural  

---

## Context
Why a decision is needed; constraints; evidence of the problem.

## Decision
The choice, stated normatively.

## Alternatives Considered
At least two realistic alternatives and why rejected / deferred.

## Consequences
Benefits, trade-offs, migration impact, curriculum V1/V2 effects, claim-language impact.

## Governance Alignment
- Vision 2030
- Product Blueprint
- Educational Constitution / DG-001 (if educational authority touched)
- Architecture Constitution articles implicated
- Product Constitution (OA-001) principles implicated

## Related
Links to prior ADRs, registers, programmes.
```

### Status meanings

| Status | Meaning |
|--------|---------|
| **Proposed** | Under review; must not be implemented as if Accepted |
| **Accepted** | Binding; implementation may proceed within its envelope |
| **Superseded** | Replaced by a named newer ADR; keep file for history |
| **Deprecated** | No longer recommended; migration path required |

---

## 5. Decision process

1. **Confirm** Vision / Blueprint / Educational Constitution do not forbid the change (`GOVERNANCE.md` §5).
2. **Draft** ADR in the correct tree with Status = Proposed.
3. **Review** — Founder Review with Engineering Owner (architecture lens); Educational Gate Owner if educational authority is touched; Privacy Owner if data boundaries change.
4. **Accept** — set Status = Accepted; update the tree’s README index.
5. **Implement** — only after Accepted (or under an explicit spike exception that cannot merge to `main` without Acceptance).
6. **Enforce** — prefer architecture tests under `tests/architecture/` for durable invariants.
7. **Supersede** — when replacing, leave the old ADR file; point both ways.

### Forbidden

- Merging structural changes with “ADR to follow”.
- Quietly editing an Accepted ADR’s Decision section without versioned amendment notes.
- Using governance or docs programmes to change educational algorithms without ADR + educational review.

---

## 6. Compatibility and migration

ADRs that affect runtime must state:

- Additive vs breaking posture (prefer additive shims).
- Curriculum V1/V2 load/traversal impact.
- Dual-stack / Contained residual impact (RR-002 / ER-002).
- StartupService / idempotent bootstrap safety.
- Required follow-up debt items (register IDs).

---

## 7. Relationship to other artefacts

| Artefact | Relationship |
|----------|--------------|
| Architecture Constitution | ADRs interpret and specialise; they do not override |
| PRDs | May require an ADR; PRD is not a substitute for ADR |
| Technical debt register | Records deferred consequences of Accepted ADRs |
| Release governance | Releases that ship ADR-backed changes must cite ADR IDs |

---

**End of Architecture Decision Record Standard**
