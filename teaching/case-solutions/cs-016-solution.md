---
case: cs-016
solution-for: modules/module-02-network-threats/case-studies/cs-016-stp-manipulation-detection.md
difficulty: beginner
module: 2
lecture-anchor: L06
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-016 Solution — STP Manipulation (INSTRUCTOR ONLY)

## Model Solution

**Root-bridge election mechanics:** STP/RSTP elects the root bridge by
**lowest bridge ID = lowest priority, tie-broken by MAC**. Any switch (or
device speaking BPDUs) with priority 0 advertises itself as the best root.
When the desktop switch announced priority 0, every real switch re-elected
it: topology change → recalculation → ~30 s of storm/re-learning (RSTP
convergence), followed by recovery when the desktop switch was unplugged
(end of day one?) and the core re-won the election.

**Malicious vs accidental — evidence for each:**

| Malicious | Accidental |
|---|---|
| Priority 0 is *crafted* — a consumer switch never ships at 0 | Consumer switches don't send BPDUs by default — but many do STP after config or firmware quirks |
| Three repeats, each on new-hire day-one | New-hire clusters always get the *same* new desktop switches — same behavior each time |
| Timing during launch week (max damage) | No exfil, no scanning, no follow-on activity |

**Verdict: accidental** — the deciding fact is that the "attacker" is a
consumer desktop switch, repeated only when *facilities deploys more of the
same hardware* (evidence #3), and the same MAC reappears with the same
behavior. A malicious actor would more likely vary hardware/timing and pair
the root-theft with interception or DoS; here there's no follow-on activity.
(The pattern *is* indistinguishable from naive attack tooling at first
glance — hence the check list above matters.)

**Three-config fixes:**

| Fix | Prevents |
|---|---|
| 1. **BPDU guard** on all user-facing ports (`spanning-tree bpduguard enable`) | **both** — any BPDU on an access port shuts the port instantly (desktop switch *or* attack tool) |
| 2. **Root primary**: set core as `spanning-tree vlan X root primary` (priority low, e.g., 4096) | **malicious** priority-0 theft still wins the election — so also… |
| 3. **Root guard** on uplinks to untrusted switches | **malicious** — a better BPDU from below gets the port blocked, not the network re-rooted |

(Plus the *policy* fix: ban unmanaged desktop switches; provide managed
edge extensions or more ports.)

## Alternative Solutions

- **Treat as pure accident, no config change.** Rejected: the *same* failure
  mode is one tool away from malice; BPDU guard is minutes of work.
- **Disable STP.** Catastrophically wrong — loops then take the network down
  for real.
- **Upgrade all switches to RSTP-only/MSTP tuning.** Convergence tuning helps
  recovery speed but doesn't fix trust; keep the guard mechanisms as primary.

## Tradeoffs

- BPDU guard strictness: `errdisable` shutdown on access ports is the right
  default; requires an auto-recovery or help-desk path for false positives
  (e.g., hypervisor bridges).
- Root guard vs BPDU guard placement: guard *uplinks* with root guard
  (protect election), guard *access* ports with BPDU guard (protect the edge) —
  they're complements, not alternatives.

## Common Mistakes

- Calling it a "loop" — no loop occurred; the root *changed*.
- Missing that default priorities (32768 everywhere) made the network
  root-election-fragile by design.
- Assuming malice without weighing the facilities-hardware evidence.
- Fixing with "better switches" instead of protocol guards.

## Instructor Prompts

- "Why is priority 0 the smoking gun for *intent* — but not proof of it?"
- "What does an attacker *gain* by becoming root?" (traffic attraction, DoS.)
- "Which single config line would have turned all three outages into
  non-events?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Election mechanics; verdict with deciding fact |
| Technical accuracy | 25% | BPDU/root-guard placement correct |
| Alternatives considered | 20% | Malice-vs-accident evidence table |
| Communication | 15% | Clear narrative + mapped fix table |

**Timing:** reveal at 5:00; the "what does root give you" prompt frames STP
as a trust decision, not just a loop-prevention tool.

## CLO Mapping

- **CLO-2** — Control-protocol abuse mechanics and hardening.
