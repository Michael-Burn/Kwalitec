# Operational Runbook — Founder Curriculum Publishing

**Programme:** PR-001A  
**Owner:** Founder operations  
**Systems:** Curriculum Studio Console, Curriculum Management, Curriculum Ingestion  

---

## Mission

Publish and maintain subjects so students receive authorised curriculum without developer involvement.

## Daily / weekly operations

| Cadence | Task |
|---|---|
| Per publication | Follow [Operational Checklist](OPERATIONAL_CHECKLIST.md) |
| Weekly | Review Studio dashboard pending validation / approval counts |
| On syllabus change | New version label → upload → validate → preview → approve → publish |

## Standard publish procedure

1. Authenticate as founder.
2. Open Curriculum Studio.
3. Create or select subject.
4. Open workspace.
5. Assign version.
6. Upload CMP + syllabus references.
7. Validate; clear blocking findings.
8. Preview; approve.
9. Publish; verify dashboard.

Detail: [Founder User Guide](FOUNDER_USER_GUIDE.md), [Subject Publishing Guide](SUBJECT_PUBLISHING_GUIDE.md).

## Incident classes

| Class | First response | Escalate when |
|---|---|---|
| Operator form/input error | Follow flash + findings | N/A |
| Validation blocked | [Validation Guide](VALIDATION_GUIDE.md) | Finding persists after corrected sources |
| Service unavailable | Retry after refresh | Repeated PortUnavailable across steps |
| Wrong published package | Stop further publishes; note version | Need rollback / archive assistance |

## Communication

- Prefer Console flashes and findings over ad-hoc engineering DMs.
- For support tickets include: subject code, workspace id, version label, flash text, finding codes, UTC time.

## Safety rules

- Never publish with blocking validation findings.
- Never reuse published version labels.
- Never paste secrets or PDF binaries into reference fields.
- Do not request Runtime A / Twin changes as part of publishing ops (out of scope).

## Related artefacts

- [Founder Workflow Specification](FOUNDER_WORKFLOW_SPECIFICATION.md)
- [Error Recovery Matrix](ERROR_RECOVERY_MATRIX.md)
- [Validation UX Review](VALIDATION_UX_REVIEW.md)
