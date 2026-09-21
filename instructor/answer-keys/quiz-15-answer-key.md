---
quiz: quiz-15
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-9, CLO-10]
marks: 10
status: complete
---

# Answer Key — Self-Check Quiz 15 (Week 12)

1. **B** — unauthenticated = outside view: exposed services/reachable
   flaws, blind to internal state; package truth needs credentials; scan
   ≠ exploit proof.
2. **B** — discovery→authorization→scan→prioritize→remediate→verify is
   the lifecycle; skipping discovery/verify is the classic failure.
3. **B** — environmental scoring/reachability/business context drives
   real priority (the cs-076 debate); scanners and randomness are noise.
4. **B** — verification = re-test against the baseline *and* confirm the
   service still functions (hardening that breaks the app gets reverted
   quietly).
5. **B** — isolation-to-required-flows + monitoring is the canonical
   compensating control; deleting from inventory hides risk.
6. **(2)** An undiscovered asset is scanned by nobody, patched by nobody,
   and monitored by nobody — the program's coverage claim is false at
   exactly the point where the asset is weakest (usually why it was
   forgotten).
7. **(2)** Scan traffic must be explicitly allowed: management VLAN →
   each scanned segment (scanner is *in* the mgmt VLAN); most-forgotten
   pair: **DMZ scan allow** (mgmt→DMZ is often blocked by design) and
   the **return/established** rule for the scanner.
8. **(2)** Remediation: removes the vulnerability (patch, upgrade,
   replace). Mitigation: reduces exploitability/impact without removing
   the flaw. Acceptable permanent mitigation: network isolation to
   required flows only (with monitoring) for an unpatchable asset —
   documented, reviewed, owned.
