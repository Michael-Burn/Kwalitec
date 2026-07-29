# KPI Audit

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Policy (DX-001):** Default **no KPI cards**. Keep only metrics that change the user’s next action.

---

## Evaluation rubric

For each metric:

- **Purpose** — why shown  
- **Decision enabled** — what changes if the number moves  
- **Frequency** — Daily / Weekly / Rare / Never for this role  
- **Remove?** — Yes / No / Relocate  

---

## Console Home

| Metric | Purpose | Decision enabled | Freq | Remove? |
|---|---|---|---|---|
| Pending content reviews | Attention | Open Support if >0 | Daily | **Relocate** to list item, not KPI card |
| Platform Health % | Vanity/ops | Rarely changes publish action | Rare | **Yes** from Overview (→ Operations) |
| High-severity findings | Attention | Open Findings if >0 | Daily | **Relocate** to list |
| Needs intervention count | Attention | Open Attention | Daily | **Relocate** to list |
| Active participants | Inventory | Does not change today | Weekly | **Yes** from Overview |
| Check-ins today | Research pulse | Rarely immediate action | Weekly | **Yes** from Overview |
| Avg experience /5 | Research | Not Overview action | Weekly | **Yes** (→ Research) |
| Would open tomorrow % | Research | Not Overview action | Weekly | **Yes** |
| Alpha health label + Build # | Ops/meta | Build never a user decision | Rare | **Yes** from L0 |

**Overview keep:** A single **Needs action (N)** count only if it is the Primary CTA label — not a card grid.

---

## Curriculum Workspace

| Metric | Purpose | Decision enabled | Freq | Remove? |
|---|---|---|---|---|
| Validation summary card | Readiness | Whether Validate/fix | Daily | **Relocate** — show as status line beside Primary, not card |
| Preview summary card | Readiness | Whether Preview | Daily | **Relocate** |
| Checklist summary card | Readiness | Whether Approve/Publish | Daily | **Relocate** |
| CIP Overview: Documents count | Inventory | No | Rare | **Yes** as hero metric |
| Topics count | Inventory | No | Rare | **Yes** unless review needed |
| Needs review count | Queue | Open Review tab | Daily | **Keep** as queue badge |
| Validation errors count | Blockers | Fix before publish | Daily | **Keep** as blocker |
| Indexed / Failed / Model / Vectors | Embeddings ops | Engineering | Rare | **Yes** from default UI (Advanced) |
| Mean mapping confidence | Quality | Soft signal | Weekly | Relocate Advanced |
| Graph completeness | Quality | Soft signal | Weekly | Relocate Advanced |
| Founder approvals | Audit | Rare | Rare | Relocate Advanced |
| Pipeline event duration_ms | Debug | Never for publish decision | Never | **Yes** from default UI |

---

## Student History

| Metric | Purpose | Decision enabled | Freq | Remove? |
|---|---|---|---|---|
| Total study time | Orientation | Rarely changes today | Weekly | Relocate quiet caption or remove |
| Session count | Orientation | No | Weekly | Caption only |
| Readiness trend list | Analytics | Journey/Home already guide | Weekly | **Yes** from History (→ Journey if anywhere) |

---

## Student Profile

| Metric | Purpose | Decision enabled | Freq | Remove? |
|---|---|---|---|---|
| Learning statistics cards | Display | No | Rare | **Yes** |
| Goal progress bars | Motivation | Only if editable here | Weekly | Keep only if action |

---

## Student Home

| Metric | Purpose | Decision enabled | Freq | Remove? |
|---|---|---|---|---|
| Estimated duration | Plan session | Yes — sets expectation | Daily | **Keep** (L1 text, not KPI card) |
| Readiness / countdown cards | Context | Weak vs Start CTA | Daily | **Relocate** to Journey |
| Coherence / trust indicators | Framework chrome | Confused with Primary | Daily | **Remove** from L0 |

---

## Internal Alpha / Platform reports

| Metric | Purpose | Decision enabled | Freq | Remove? |
|---|---|---|---|---|
| Programme health summaries | Ops | Ops decisions | Weekly | Keep on **report** pages only |
| Changes since yesterday | Ops | Maybe | Daily | Report only |
| Telemetry event counts | Debug | Engineering | Rare | Advanced only |

---

## Login / marketing

| Metric | Purpose | Decision enabled | Freq | Remove? |
|---|---|---|---|---|
| Feature bullet list (not numeric KPIs) | Marketing | Soft | Once | Reduce to one sentence |

---

## KPI verdict

| Surface | KPI cards today | Target |
|---|---|---|
| Console Home | 8 | **0** cards; optional count in Primary CTA |
| Workspace readiness | 3 + CIP metrics | **0** cards; status + blocker list |
| History | 2 | **0** |
| Profile | Stats cluster | **0** |
| Report pages (Research, Ops) | Allowed | Charts/tables OK if decision-oriented |

**Any KPI that does not change user behaviour should be removed** — majority of current product KPIs fail this test.
