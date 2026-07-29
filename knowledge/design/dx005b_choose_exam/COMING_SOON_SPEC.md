# Coming Soon Specification

**Programme:** DX-005B  
**Status:** Binding for Coming Soon on Choose Exam  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-003 Status System; DX-005B Discovery Architecture  
**Companion:** `READY_STATE_SPEC.md`

---

## 1. Law

Coming Soon curricula may expose **Notify when available**.

They must **never** expose **Begin Learning**.

Coming Soon is visually **secondary** to Ready. It must not dominate the viewport when Ready offerings exist (addresses FV-001C density: long Soon lists with repeated essays).

---

## 2. Definition (student-facing)

| Term | Meaning |
|---|---|
| **Coming Soon** | Verified curriculum is still under preparation; student cannot begin yet |

Forbidden student badges for this state: Draft, Unavailable (as peer to Ready), Published, Live.

Unavailable / not-supported offerings are **omitted**, not listed as Coming Soon.

---

## 3. Placement

| Rule | Value |
|---|---|
| Band | Separate section **below** Ready |
| Interleaving | Forbidden — never mix Soon rows into Ready radios |
| Visual weight | Quieter type, lighter rules, no selection radios |
| First viewport | Ready owns the fold; Soon may peek or sit below |
| Collapse | Allowed: collapsed “Coming soon (N)” disclosure when N is large |

When Ready is empty and Soon exists: empty Ready Reason remains L0; Soon stays secondary underneath (`DISCOVERY_WIREFRAME.md`).

---

## 4. Row content

| Allowed | Forbidden |
|---|---|
| Subject title | Begin Learning |
| One short preparation line (shared canonical) | Repeated multi-paragraph essays per row |
| **Notify when available** (Secondary) | Filled Primary weight |
| Quiet Coming Soon label | Decorative badge clusters |

### Canonical preparation line (one shared string)

> This subject’s verified curriculum is still under preparation. You cannot start studying this exam yet.

Prefer **once per band** or once per row as a single short line — do not paste long identical essays on every row. If band-level copy exists, rows may show title + Notify only.

---

## 5. Notify when available

| Attribute | Value |
|---|---|
| Label | **Notify when available** |
| Weight | Secondary / text / quiet button — never filled Primary |
| Effect | Record interest (email/in-app) **or** quiet acknowledgement if notify infrastructure is not yet shipped |
| Failure | Honest: if notify cannot be stored, say so — do not fake Begin |

### Implementation honesty

If Alpha has no notify backend yet:

- Ship the Secondary control as **disabled with quiet reason**, **or**  
- Omit the control and keep Coming Soon informational only  

Do **not** ship a fake success that implies enrolment.

When notify ships: success Feedback is a quiet flash / inline “We’ll notify you.” — not celebration theatre.

---

## 6. Filter interaction

Status filter **Coming Soon** may show only the Soon band (Ready empty message may hide). Status **Ready** hides Soon. Default: both bands (Ready first).

Search matches titles in both bands but does not promote Soon into Ready selection.

---

## 7. Success test

Coming Soon never enables Begin Learning. With Ready present, Soon does not out-shout Ready. Repeated essay walls are gone. Notify (if present) is clearly secondary.
