# PB-015 ops — v3 runner process deaths (infra)

- at: 2026-08-04T00:18:28.388211+00:00
- educational_failure: false
- event: process_group_kill_or_silent_death
- detail: returning/average/struggling v3 processes vanished without traceback mid Continuity Front transit (CK-D*). Logs truncated at day 3 / day 1 / baseline. Fingerprint tip 8432f6a… still matched at start. Classified as infrastructure/process-lifecycle, not educational defect.
- accounts_abandoned:
  - pb015.co.returning.1785801265@example.com
  - pb015.co.average.1785801443@example.com
  - pb015.co.struggling.1785801624@example.com
- remediation: relaunch with setsid/nohup, serial (returning → average → struggling)
