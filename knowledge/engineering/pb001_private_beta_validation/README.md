# PB-001 — Private Beta Validation (engineering)

**Programme:** PB-001 · Private Beta Validation · Version 1  
**Type:** Evidence infrastructure (no new educational architecture)  

> **Naming note:** Product Board programme `knowledge/product/pb001_stage1_go_no_go_review/`
> is a separate Stage 1 Go/No-Go review. This engineering folder is the
> operational Private Beta Validation stack (dashboard, feedback, metrics, report).

## Artefacts

| Path | Role |
|------|------|
| [`PB001_PRIVATE_BETA_REPORT.md`](PB001_PRIVATE_BETA_REPORT.md) | Live end-of-beta report (regenerate from Console) |
| [`PB001_IMPLEMENTATION_REPORT.md`](PB001_IMPLEMENTATION_REPORT.md) | Programme completion report |

## Operator entry points

- Founder Console → Settings → **Private Beta** (`/console/beta`)
- Student footer → **Report issue** (`/alpha/feedback/beta`)
- Generate report: POST `/console/beta/report`
