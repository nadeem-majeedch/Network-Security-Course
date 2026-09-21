---
case: cs-003
solution-for: modules/module-01-network-foundations/case-studies/cs-003-abnormal-arp-replies.md
difficulty: beginner
module: 1
lecture-anchor: L02
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-003 Solution — Abnormal ARP Replies (INSTRUCTOR ONLY)

## Model Solution

**Verdicts per line:**

| Time | Verdict | Reason |
| 0:12 | normal | gw MAC matches expected `...:01` |
| 0:31/1:21/2:06 | normal | request→reply pattern for real hosts |
| 0:58 | normal | gratuitous announce at boot, identity matches IP |
| 2:06 :99 | **decisive red flag** | a second MAC claiming to be the gateway |
| 2:07 :01 | normal | the real gateway reasserting; the conflict already happened |

**Name:** ARP spoofing (a.k.a. ARP cache-poisoning) attempt against the
gateway identity, directed at `10.20.0.44`.

**What it enables:** :44 will cache gateway-IP→:99 and send its off-subnet
traffic (including plaintext and TLS-*terminated* streams if TLS is proxied)
through the attacker — enabling traffic interception (on-path position),
selective tampering, or selective dropping (targeted DoS). It does **not**
automatically break TLS; HTTPS to a validating client resists passive
interception.

**Is one reply an incident?** Not yet an *incident*, but a confirmed
**attempt** with attacker infra on your LAN (`:99` exists as hardware). Escalate
a "suspicious activity, infra present" rather than closing it as noise.

**One additional evidence item:** the **switch CAM table** for the port where
`:99` lives. The capture proves intent; the CAM table gives you the physical
port to disable — turning detection into containment and identifying the actor
device. (Alternative defensible answer: DHCP lease audit to identify who was
using :99's OUI — acceptable if justified.)

## Alternative Solutions

- **Close as benign transient** (e.g., a misconfigured VM). Rejected without
  evidence: :99 never legitimately announced itself at any other time in the
  capture, and the conflict pattern is the classic on-path setup pattern.
- **Immediate broadcast warning "change your ARP cache"?** Not actionable for
  students; the right organizational move is port-level containment, not user edicts.

## Tradeoffs

- Escalate-now vs verify-longer: losing 10 minutes to get the CAM table buys
  certainty and a containment point; waiting too long lets :99 resume.
- Public disclosure to the class/lab vs discreet investigation — premature
  broadcasting teaches the actor what is watched.

## Common Mistakes

- Flagging the gratuitous announce as the attack (it is normal).
- Treating 2:07 as "so it's fine" — the spoof succeeded momentarily regardless.
- Claiming HTTPS makes the whole case moot: TLS protects content, not
  reachability; selective blocking still works from an on-path position.
- Proposing "static ARP entries on all 40 hosts" as *the* fix without noting
  its operational cost at scale vs switch-level DAI.

## Instructor Prompts

- "Why did the attacker target the gateway, not a printer?"
- "What would this look like in 2 minutes of Zeek `conn.log` instead of ARP?"
- "Which is better here: dynamic ARP inspection on the switch, or static ARP on hosts? Why?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Conflict judged *relative to* known-good MAC; timing understood |
| Technical accuracy | 25% | Correct on-path/enables/not-breaks-TLS claims |
| Alternatives considered | 20% | Escalate-vs-close justified with the missing-evidence ask |
| Communication | 15% | Per-line verdict table with one-line reasons |

**Timing:** reveal at 5:00; use the "why gateway" prompt to bridge into L06's
spoofing lecture.

## CLO Mapping

- **CLO-1** — Protocol-level indicator identification.
