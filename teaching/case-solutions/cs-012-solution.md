---
case: cs-012
solution-for: modules/module-02-network-threats/case-studies/cs-012-attck-mapping-intrusion-narrative.md
difficulty: beginner
module: 2
lecture-anchor: L05
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-012 Solution — ATT&CK Mapping (INSTRUCTOR ONLY)

## Model Solution

**Step-by-tactic mapping (one defensible answer; IDs optional):**

| Step | Tactic | Technique phrase |
|---|---|---|
| 1. Bought password | (Pre-ATT&CK / Resource Development) | credential from criminal market |
| 2. VPN login 02:50 | **Initial Access** | valid accounts, external remote services |
| 3. Internal scan from VPN | **Discovery** | network service scanning |
| 4. `\\fs01\finance` access | **Discovery/Collection boundary** | remote system discovery → data from network shared drive |
| 5. 2 GB SMB copy | **Collection (+ Exfiltration preparation)** | data from network shared drive |
| 6. Deleted VPN logs | **Defense Evasion** | indicator removal / clear logs |

**Earliest current-logging detection point:** **step 2** — the VPN auth log at
02:50 from a residential IP for a staff member with no remote-work history.
(Rationale: steps 1 has no telemetry in-company; step 2 is the first
*company-side* event. Defensible alternative: step 5 if SMB access auditing is
on and 2 GB from a VPN session is anomalous — accept if justified.)

**Zero-detection tactics and the logging fix:**

- **Collection (step 5)** if file-share auditing is off: enable SMB/file-share
  audit + egress volume baselines.
- **Discovery (step 3)** if internal traffic is unlogged: enable switch/flow
  or endpoint-level connection logging. (Also accept: Defense Evasion —
  step 6 — because *by definition* successful log deletion means no detection
  happened; the fix is forwarding logs off-box in near-real-time, which makes
  deletion detectable *as it happens*.)

**Note the defense-evasion trap:** the narrative *ends* with log deletion —
everything after step 2 may be incomplete in the real evidence. Mapping the
story is not the same as trusting it.

## Alternative Solutions

- Mapping step 1 as "Initial Access (phishing-for-credentials)" — rejected:
  the narrative says purchased, not phished; precision matters.
- Calling step 4 "Lateral Movement" — defensible (remote services into a new
  system); the file-server access straddles Discovery/Collection/Lateral
  Movement; accept with justification.

## Tradeoffs

- Exact technique IDs vs own-words phrases: IDs show training; own-words show
  understanding. For 5-minute cases, own-words + correct tactic is the goal.
- Tactic-first vs technique-first storytelling: tactic-first exposes coverage
  gaps (this case's point); technique-first fits threat-intel matching (L28).

## Common Mistakes

- Treating every step as "Initial Access."
- Marking step 1 as detectable — purchased credentials leave no in-company trace.
- Missing the log-deletion trust problem entirely.
- Ignoring the stated logging constraints when answering "detectable when."

## Instructor Prompts

- "At which step could a $0 control (MFA) have broken the chain?"
- "Which step would Zeek logs have shown that the narrative's own logs couldn't?"
- "If the attacker had used DNS for exfil, which logging gap bites?" (foreshadows cs-010.)

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Correct tactic per step; detection reasoning tied to stated logging |
| Technical accuracy | 25% | Tactic semantics right (not every step = access) |
| Alternatives considered | 20% | Boundary-step disputes acknowledged |
| Communication | 15% | Clean step→tactic table |

**Timing:** reveal at 5:00; the "$0 control" prompt sets up Module 3.

## CLO Mapping

- **CLO-2** — ATT&CK framing of an intrusion narrative.
