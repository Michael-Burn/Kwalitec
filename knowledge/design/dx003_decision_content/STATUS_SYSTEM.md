# Status System

**Programme:** DX-003  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`

---

## Purpose

Statuses exist only to change decisions or confirm Feedback. They are not decoration.

For every status ask:

1. Is it **actionable**?  
2. Does it **duplicate** another status?  
3. Can it become an **icon** or **colour** alone?  
4. Can it **disappear** when idle?

If yes to 3 or 4 without losing a decision, demote or remove.

---

## Status taxonomy

| Kind | When shown | Form | Example |
|---|---|---|---|
| **Gate** | Blocks next Action | Label + colour; optional count | Blocking · 3 |
| **Progress** | Stage of one object | Quiet text or step | Validation |
| **Outcome** | After Action (Feedback) | Short flash / inline | Published |
| **Availability** | Catalogue selectability | Badge | Ready / Coming Soon |
| **Attention** | Queue priority | List position > badge | Needs attention |
| **Health** | Reports only | Nested under Operations | Degraded |
| **Decorative** | Never | — | Remove |

---

## Canonical status dictionary

### Curriculum / Workspace

| Status | Actionable? | Keep? | Notes |
|---|---|---|---|
| Draft / In progress | Yes (open workspace) | Keep as quiet stage | Prefer stage name over “Draft” essay |
| Documents incomplete | Yes (upload) | Keep | Prefer button state over badge |
| Extracting | Wait | Keep brief | No progress novel |
| Validation passed | Informs Approve | Keep once | Do not also say “Ready to approve” in three places |
| Blocking findings | Yes (fix) | Keep | Count + open list |
| Preview ready | Informs Approve | Keep once | |
| Approved | Informs Publish | Keep once | |
| Published | Outcome | Flash + subject Ready | Do not keep “Published successfully and now available…” |
| Needs attention | Yes | Keep on Overview/queue | One surface; not duplicated as KPI + badge + CTA |

### Student catalogue

| Status | Actionable? | Keep? | Notes |
|---|---|---|---|
| Ready | Yes (select) | Keep | Canonical availability |
| Coming Soon | No (wait / choose other) | Keep | Quiet; must not dominate |
| Unsupported / gated | Yes (choose other) | Keep | Subject support gate |

### Student Home / Session

| Status | Actionable? | Keep? | Notes |
|---|---|---|---|
| Mission ready | Yes (Start) | Prefer CTA alone | Badge optional |
| In progress | Yes (Continue) | CTA label | |
| Day complete | No primary study | Quiet state | No congratulations banner |
| Reflection due | Yes | Keep | |
| Trust / coherence badges | Rarely | **Remove from L0** | Framework chrome |
| Internal Alpha | Shell once | Once per shell | Not every hero |

### Console Overview

| Status | Actionable? | Keep? | Notes |
|---|---|---|---|
| Attention count KPIs | Weakly | **Replace with list** | Metrics ≠ status |
| Platform summary health | Rarely on Overview | **Remove from Overview** | Move to Operations |
| Timestamp / timezone pulse | No | **Remove from L0** | L3 or omit |

---

## Redundant status pairs (collapse)

| Pair | Keep | Delete |
|---|---|---|
| “Validation passed” + green KPI + checklist row saying same | One indicator | Others |
| “Needs attention” section + Attention KPI + Open Attention Center | List + one Primary | KPI + duplicate CTA |
| “Documents Uploaded” badge + Replace button | Button state | Badge theatre |
| Ready badge + “available for students” sentence | Ready | Sentence |
| Internal Alpha in shell + hero + login | Shell once | Repeats |
| Blocking count in header + banner + findings title | Findings + count | Banner essay |

---

## Icon / colour demotion rules

| Prefer icon/colour alone when | Prefer text when |
|---|---|
| Severity is already encoded (error/warning/success) | User must know *what object* or *what to do* |
| Repeated in dense tables | First occurrence in a screen |
| Companion to a clear row label | Status is the only L0 signal |

Icons never replace labels for Primary Actions (DX-001).

---

## Disappearance rules

| Condition | Behaviour |
|---|---|
| Idle success after navigation | Do not persist “Published” banner on every return |
| Zero blockers | Hide Blocking chrome entirely |
| Single shell badge | Show Alpha once; never restated in body |
| Duplicate of page title | Delete status |

---

## Target inventory (primary paths)

| Surface | Current status chrome (est.) | Target | Reduction |
|---|---|---|---|
| Curriculum Workspace | 12–18 indicators | 3–5 (stage + blockers + outcome) | ~60% |
| Console Overview | 8–12 | 1–2 (attention) | ~75% |
| Student Home | 6–10 | 1–3 | ~50% |
| Studio hubs | 4–6 + essay | 1–2 | ~60% |
| Choose Exam | 2 (Ready/Soon) | 2 | 0% (keep) |

**Estimated product-wide reduction in redundant status messages on primary paths: ~40–50%.**
