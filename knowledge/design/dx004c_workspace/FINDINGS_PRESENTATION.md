# Findings Presentation

**Programme:** DX-004C  
**Status:** Binding for workspace findings hierarchy  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-003 Status System, domain `ValidationFindingSeverity`

---

## 1. Purpose

Findings exist to change the decision or enable recovery — not to decorate the page. Severity drives prominence.

---

## 2. Severity → placement

| Severity (domain) | Prominence | Placement |
|---|---|---|
| **Blocking** / **Error** (`is_blocking`) | Highest | **L0** count + L1 list with recovery |
| **Warning** | Medium | L1 or L2; never L0 strip |
| **Info** | Lowest | L2 or L3; omit if idle |

Only **blocking** findings appear at L0.

```
L0:  Blocking: 2
L1:  Full blocking list + recovery actions
L2:  Warnings (if useful)
L3:  Codes / diagnostics
```

---

## 3. L0 blocking presentation

| Element | Rule |
|---|---|
| Count | `Blocking: N` adjacent to Primary |
| Zero blockers | Omit count entirely — do not show `Blocking: 0` |
| Primary | Prefer **Resolve findings** (or stage recovery) when N > 0 |
| Colour | Semantic danger/attention only — not gold chrome (DX-001) |

---

## 4. Finding row content (L1)

Each blocking finding shows:

| Field | Required | Notes |
|---|---|---|
| Message | Yes | Human, one line preferred |
| Why it matters | Optional | One short line |
| Recovery action | Yes when known | What to do |
| Code | L3 | Technical token |

Example:

```
Missing topic mapping in Section 3
Why: Structure cannot pass readiness.
What to do: Re-process sources after correcting the CMP mapping.
```

Do not dump stack traces in L1.

---

## 5. Interaction

| Action | Behaviour |
|---|---|
| Resolve inline | Prefer stay on workspace; fix → re-validate |
| Deep link to section | Scroll/focus L1 content; no route away |
| After fix | Re-run validation (Primary or secondary); update L0 count immediately |

Never redirect to a separate “Findings” catalogue page for recoverable workspace issues.

---

## 6. Warnings & info

- Do not inflate warnings into L0.  
- Do not badge the entire page “Attention” for warnings alone.  
- If only warnings remain and stage may advance, Primary is the stage advance / confirm — not “Resolve findings.”

---

## 7. Empty findings

When validation has not run: no findings section (or quiet “Validation not run yet” inside L1 Validate content — not a KPI card).

When passed with zero blockers: omit findings block; Primary advances.

---

## 8. Success test

With 2 blockers and 5 warnings, the Founder’s eye hits blockers and Primary first; warnings require deliberate secondary reading.
