---
case: cs-008
solution-for: modules/module-01-network-foundations/case-studies/cs-008-rogue-dhcp-server-effects.md
difficulty: beginner
module: 1
lecture-anchor: L03
clos: [CLO-1]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-008 Solution — Rogue DHCP (INSTRUCTOR ONLY)

## Model Solution

**Name:** rogue DHCP server (DHCP address+options injection) leading to
on-path positioning and denial/degradation.

**Packet-level defeat of the legitimate server:** DHCPDISCOVER is broadcast;
both the legit server (172.16.40.1) and the Pi (172.16.40.200) offer (DHCPOFFER).
The client takes the **first offer received** — the Pi is on the same LAN as
the clients, the legit server is routed and milliseconds slower for wired lab
PCs; the Pi's OFFER with a 0-lease short lease wins the race for hosts that
renew/reshoot DORA during the weekend. Once the client ACKs the Pi's offer,
it applies the Pi's **option set** (gateway .5, DNS 8.8.8.8/1.1.1.1) for the
lease duration.

**Why "internet works, intranet doesn't":** the Pi's DNS options point at
public resolvers (8.8.8.8, 1.1.1.1) which resolve public names fine — internet
works. But **internal names** (library catalog, print servers) exist only in
the campus resolvers' zones (split-horizon/internal zones). Public resolvers
return NXDOMAIN for internal names ⇒ intranet breaks. The router option (.5)
may or may not route — consistent with "internet works" if .5 NATs correctly,
or the Pi may also be doing a light NAT. Either way the *DNS option* is the
cleanest explanation of the split symptom.

**Response order:**

1. **Disable switch port 17** (the Pi's port) — the decisive lever: stops new
   rogue OFFERs in seconds; all other steps are secondary until this is done.
2. **Force-renew / flush leases on affected PCs** (release/renew, or shorten
   the rogue leases by replaying legit DHCP) — recovers clients; without step 1
   they'd re-poison.
3. **Audit what the Pi did during its dwell time** (its DNS could have returned
   impostor answers even for public names) — the forensic step; also address
   the student's intent administratively.

**Why the port is decisive:** any solution that doesn't stop the source
(lease cleanup, client fixes, warnings) leaves the attack running; only
isolating the source port stops generation of new victims. (Switch-level
defense for the future: DHCP snooping + port security; the debrief names it.)

## Alternative Solutions

- **Broadcast a warning and reimage affected PCs** — treats symptoms; the Pi
  keeps re-offering; rejected as primary response.
- **Find the Pi first, disable port second** — sequencing error: minutes lost
  identifying hardware while every renewing client is a new victim.
- **Enable DHCP snooping immediately mid-incident** — right long-term control;
  mid-incident config change on a live switch risks a bigger outage; do it
  *after* containment, in a change window.

## Tradeoffs

- Port disable now (kills a student's legit work too) vs targeted ACK-storm
  mitigation (slow, fiddly) — decisive-and-blunt wins while victims accumulate.
- Punitive vs educational handling of the student — intent doesn't change the
  technical response, but it changes the administrative one; separate the two.

## Common Mistakes

- Explaining via "the Pi is faster" without DORA race mechanics.
- Missing that the DNS option set explains the split symptom precisely.
- Fixing clients before stopping the source.
- Treating DHCP snooping as a mid-incident action (change-control risk).

## Instructor Prompts

- "Which DHCP option is the actual 'attack payload' here?"
- "What would DHCP snooping have done, and when should it have been deployed?"
- "If the Pi had offered the *campus* DNS but a malicious router IP, what
  symptom would you see instead?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | DORA race + option-set-as-payload reasoning |
| Technical accuracy | 25% | Correct DHCP packet mechanics; DNS split-horizon explanation |
| Alternatives considered | 20% | Sequencing alternatives rejected with reasons |
| Communication | 15% | Ordered response with decisive-lever justification |

**Timing:** reveal at 5:00; the snooping question bridges to L06/L12 controls.

## CLO Mapping

- **CLO-1** — DHCP mechanics → threat understanding.
