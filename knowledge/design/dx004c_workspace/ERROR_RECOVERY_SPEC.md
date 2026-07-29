# Error Recovery Spec

**Programme:** DX-004C  
**Status:** Binding for workspace recoverable failures  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-003 Success/Error Copy Guide, DX-001  

---

## 1. Principle

```
Errors appear inline.
Recovery is immediate.
Never redirect to another page for recoverable issues.
```

The Founder stays in execution context.

---

## 2. Error classes

| Class | Examples | Recovery locus |
|---|---|---|
| **Upload failure** | File type, size, virus scan, storage | Upload L1 inline |
| **Processing failure** | Extract/parse job failed | Upload/Validate L1; Retry Primary |
| **Validation failure** | Blocking findings | L0/L1 findings; Resolve |
| **Gate failure** | Advance while incomplete | Inline reason; stay on stage |
| **Approval/Publish failure** | Downstream publish bridge error | Publish L1; Retry publish |
| **Auth / CSRF / 403** | Session expired | Inline or soft re-auth; avoid losing stage when possible |
| **Non-recoverable** | Workspace deleted / 404 | Error page acceptable |

Only non-recoverable cases may leave the workspace.

---

## 3. Inline error anatomy

| Element | Rule |
|---|---|
| What failed | One factual sentence |
| What to do | One recovery action |
| Primary | Becomes Retry / Resolve / Re-upload as appropriate |
| Tone | Professional; no blame essays (DX-003) |

Example:

```
Upload failed — file exceeds the size limit.
Use a PDF under 25 MB, then upload again.
[ Upload documents ]
```

---

## 4. Forbidden recovery patterns

| Pattern | Why forbidden |
|---|---|
| Redirect to Studio dashboard on validation fail | Breaks continuity |
| Redirect to generic Support for every parse error | Leaves execution |
| Modal maze of “OK” with no action | Unnecessary confirmation |
| Clearing stage back to Upload on any error | Punitive; lose progress |
| Duplicate error as KPI card + banner + toast novel | Noise |

Toast/flash may reinforce Feedback; the **actionable** error lives inline.

---

## 5. Retry semantics

| Failure | Retry behaviour |
|---|---|
| Processing | Resume/retry from durable checkpoint when engine supports it |
| Validation | Re-run validation after fix |
| Publish | Retry publish without re-approving unless approval invalidated |

Idempotent retries preferred (engineering already favours idempotent bootstrap/publish paths).

---

## 6. Blocking findings as errors

Blocking findings are a form of recoverable error:

- Presented per `FINDINGS_PRESENTATION.md`  
- Primary = Resolve / recovery  
- Clear blockers → Primary returns to stage default  

---

## 7. Accessibility

- Errors associated with controls via `aria-describedby` / alert role where appropriate  
- Focus moves to the error or Primary recovery control after failed submit  
- Colour never sole indicator  

---

## 8. Success test

Force an upload failure and a validation blocker. The Founder recovers both without leaving the workspace URL family.
