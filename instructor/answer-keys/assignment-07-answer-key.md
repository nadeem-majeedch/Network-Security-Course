---
assignment: assignment-07
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-13, CLO-15]
marks: 100
status: complete
---

# Answer Key — Assignment 7 (Cloud Posture Review & Board Briefing)

> **INSTRUCTOR ONLY.** Expected findings and grading anchors.

## Expected findings register (the answer core)

| # | Finding | Class | First attack path enabled | Severity |
|---|---|---|---|---|
| F1 | Root without MFA | Identity | Full account takeover from any credential leak | H |
| F2 | IAM long-lived access keys | Identity | Key leak → persistent API access, no rotation story | H |
| F3 | Public S3 bucket | Data exposure | Direct data listing/download — no identity needed | H |
| F4 | SG `0.0.0.0/0` on 22/3389 (×6) | Network exposure | Brute-force/credential-stuffing straight to instances | H |
| F5 | No flow logs (prod) | Visibility | Exfil/C2 invisible until impact symptoms | M (H in combination) |
| F6 | No config recording/audit trail | Visibility | Changes unattributable; incident forensics blind | M |
| F7 | Prod/sandbox peering unexamined | Network design | Sandbox compromise pivots to prod | M |

*Top-band submissions find the F5+F6 combination risk ("blind during
incident") and rank F1–F2 at least equal to F3 — the bucket is loud, the
identity findings are deeper.*

## Grading anchors

### 1. Findings (30)
Seven core findings with correct *class* labels = 24+; realistic attack
path per finding = 6. Class-label confusion (calling F2 "network")
penalized per the precision constraint.

### 2. Remediation sequence (25)
Dependency logic graded: **root MFA + logging/audit trail first** (they
are cheap, fast, and make every later change visible/attributable) (10);
then identity keys → SG cleanup → bucket → peering review (10); the
workflow-changing fix named (SG cleanup forces dev rework — sell via
SSM/session-manager alternatives replacing SSH entirely) (5). Ordering
that starts with the bucket (the loud one) caps at 18/25 — the dependency
argument is the point.

### 3. Visibility plan (20)
Flow logs + audit trail + config recording with retention numbers (12);
one immediately-writable detection with signal + threshold (e.g.,
"SG/ingress rule change granting 0.0.0.0/0 → alert; any `AuthorizeSecurity-
GroupIngress` with cidr /0" — measurable) (8).

### 4. Board slide (15)
cs-094 structure: trend/risk in board language (5), two honest limits
stated (5), specific ask with deferral cost (5). Jargon on the slide
("VPC SG misconfig") caps at 10; "one-third of our cloud servers accept
login attempts from the entire internet" is the register.

### 5. Honesty section (10)
Expected unknowns: runtime processes (flow logs ≠ host state), actual
data sensitivity (bucket contents unknown), identity *usage* patterns
(keys may be unused or critical), sandbox's real blast radius. Next
checks named per unknown.

## Common failure patterns

- Bucket-only submissions (hard 70% cap per the brief).
- Detection defined as "monitor for anomalies" — no signal, no threshold.
- Board slide that narrates the findings list instead of the decision
  ask.
