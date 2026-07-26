# Claim Decision Tree

**Programme:** P-003.5 — Evidence Hierarchy & Claim Standard  
**Version:** 1.0  
**Status:** Active — Product Board decision tree  
**Effective:** 2026-07-26  
**Companions:** [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md), [`EVIDENCE_CLASSIFICATION.md`](EVIDENCE_CLASSIFICATION.md)  
**Does not:** Change runtime, governance law, decisions, risks, assumptions, or release gates  

---

## 1. Purpose

Give the Product Board a single walkable tree so the question

> Can we say this publicly?

is answered by procedure, not debate.

---

## 2. Master tree

```
Question (exact claim statement + audience)
        │
        ▼
┌───────────────────┐
│ Evidence Level?   │  ← classify via EVIDENCE_CLASSIFICATION
│ E5 / E4 / E3 /    │
│ E2 / E1 / Unavail │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Permitted Claim?  │  ← CLAIM_STANDARD matrix + freezes
│ code C-* match?   │
└─────────┬─────────┘
          │
     No ──┼── Yes
     │    │
     ▼    ▼
  STOP   ┌───────────────────┐
  rewrite│ Board Approval?   │
  or     │ (scope: Board /   │
  gather │  Cohort / Public) │
  evid.  └─────────┬─────────┘
                   │
              No ──┼── Yes
              │    │
              ▼    ▼
           HOLD   ┌───────────────────┐
                  │ Public Statement? │
                  │ (C-COM + freezes) │
                  └─────────┬─────────┘
                            │
                       No ──┼── Yes
                       │    │
                       ▼    ▼
                    Board-  PUBLISH
                    only /  with
                    cohort  citations
```

---

## 3. Step detail

### Step A — Question

Write the **exact sentence** proposed for use.

| Field | Required |
|---|---|
| Claim text | Verbatim |
| Audience | Internal eng / Board / Cohort / Public |
| Channel | Slack / dossier / beta email / website / sales / press |
| Claim window | W-PROD / W-GATED / dates |
| Owner | Name |

If the sentence contains multiple claim families, **split** into separate walks.

---

### Step B — Evidence Level?

Use [`EVIDENCE_CLASSIFICATION.md`](EVIDENCE_CLASSIFICATION.md).

| Outcome | Next |
|---|---|
| E5…E1 assigned with paths | Continue |
| Unavailable for required level | **STOP** — claim prohibited; open evidence work |
| Stale | DEFER or re-measure; do not publish as fresh |
| Falsifier present | Continue only at **lower** permitted claim |

---

### Step C — Permitted Claim?

Use [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md) §§4–6.

| Check | Fail → |
|---|---|
| Minimum level met for intended C-* code? | Downgrade code or STOP |
| Standing freeze hit (§6)? | **STOP** (C-COM hard stop) |
| Flag-OFF vs student-visible lift? | Cap Δ = 0; STOP lift claim |
| Separable verdict confused (GO vs C-V1 vs C-EDU)? | Rewrite to correct code |

**Pass** only if a single C-* code is clearly satisfied.

---

### Step D — Board Approval?

| Audience | Approval needed |
|---|---|
| Internal eng (C-IMP/C-STR only) | Tech lead sufficient if no educational wording |
| Board memo | Product owner |
| Cohort messaging | Product + Educational governance if educational claim |
| Public / C-COM | Product Board ack (named) citing this tree + evidence paths |
| C-V1 or C-REC flip to GO | Full P-002.1 go/no-go board |

| Outcome | Next |
|---|---|
| Approved for Board/Cohort only | May circulate internally; **not** public |
| Approved for Public | Continue Step E |
| Rejected / HOLD | Record reason; no publish |

---

### Step E — Public Statement?

Public requires **all** of:

1. Underlying C-* permitted  
2. C-COM freezes clear for that wording  
3. Board ack recorded  
4. Evidence paths listed in the publish packet  
5. Prefer-lower wording if confidence &lt; High  

| Outcome | Action |
|---|---|
| Yes | Publish; archive packet under evidence or marketing review log |
| No | Keep Board-only; or rewrite to non-educational ops language if C-REL only |

---

## 4. Shortcut trees (common Board questions)

### 4.1 “Can we say Version 1 is ready?”

```
C-V1 required
 → Full G1–G12 package PASS?
     No → C-REC = NO GO / DEFER (current: NO GO)
     Yes → Board go/no-go signed?
         No → HOLD
         Yes → Public C-COM only after signed decision published
```

### 4.2 “Can we say we improve learning outcomes?”

```
C-EDU / C-BEN outcome
 → E5 present + educational Go not NO-GO?
     No → STOP (current)
     Yes → Freezes clear? → Board → Public?
```

### 4.3 “Can we say students like the new explanations?”

```
If Public “students” implies external:
 → Need C-VAL-E (E4)
     No (N_external=0) → STOP public
     Board-only: C-VAL-I (E3 Tier B) OK with N + Medium disclosed
```

### 4.4 “Can we say recommendations are effective?”

```
C-COM + recommendation-effectiveness freeze (DR-036)
 → STOP until freeze lifted by governing process
 (E2/E3 quality Pass does not lift this freeze)
```

### 4.5 “Can we say the feature is done?”

```
C-IMP
 → E2 for surface + flag state disclosed?
     Yes → Internal/Board OK
     Public OK only if no smuggled C-VAL/C-EDU language
```

### 4.6 “Can sales say Exam Ready?”

```
DR-035 / Never-Build / G6.3
 → STOP (banned)
```

---

## 5. Decision record template

Copy into Board notes or marketing review:

| Field | Value |
|---|---|
| Date | |
| Claim text | |
| Audience / channel | |
| Evidence level | |
| Evidence paths | |
| Claim code(s) | |
| Freezes checked | Pass / Fail (list) |
| Board approver | |
| Public allowed? | Yes / No |
| Rationale | |
| Review-by date | |

---

## 6. Current default path (2026-07-26)

For almost all **public educational** questions:

```
Question → Evidence ≤ E3 → Permitted = C-IMP / C-STR / (Board) C-VAL-I
        → Public Statement? → NO
```

For **Version 1 recommendation**:

```
Question → Gates incomplete / G1 FAIL → C-REC = NO GO → Public V1-ready? → NO
```

---

## 7. References

- [`CLAIM_STANDARD.md`](CLAIM_STANDARD.md)  
- [`EVIDENCE_HIERARCHY.md`](EVIDENCE_HIERARCHY.md)  
- [`CLAIM_TRACEABILITY.md`](CLAIM_TRACEABILITY.md)  
- `knowledge/product/p003_1_version1_release_dossier/Version_1_RELEASE_DOSSIER.md` §11  
- `knowledge/product/p002_1_version_1_release_framework/VERSION_1_GO_NO_GO_GUIDE.md`

---

**End of CLAIM_DECISION_TREE**
