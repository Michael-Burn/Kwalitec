# RC-003 — Manual Deploy Checklist

**Host:** https://kwalitec.onrender.com  
**Seal commit:** `e953ee196d94af65eb7b8307f8fbf7cfb8bd1caf`  
**Live deployed commit:** `6d8b93161cb1680216b24a7854387efe0b9cf8b7`  
**Tag:** `v1.0.0-G1`  
**Migration head:** `202607310002`  
**Status:** **COMPLETE — 2026-07-31**

## Probes (PASS)

| Probe | Result |
|-------|--------|
| `/health` | `ok` — commit `6d8b931…` |
| `/health/ready` | `ready: true` |
| migrations | `current=head=202607310002` |
| `/baseline/` | **302** |
| Studio JS | `var byId = {};` |

Evidence: `knowledge/evidence/releases/RC003/cutover_verification.txt`

## Remaining (G1 Day 1)

1. Authenticated Founder + Student browser smoke (see `RC003_PRODUCTION_CUTOVER_REPORT.md`).
2. Start daily validation: `G1_VALIDATION_PROTOCOL.md`.
