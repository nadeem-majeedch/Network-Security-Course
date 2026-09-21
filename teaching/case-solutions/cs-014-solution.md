---
case: cs-014
solution-for: modules/module-02-network-threats/case-studies/cs-014-mac-flooding-signs.md
difficulty: beginner
module: 2
lecture-anchor: L06
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-014 Solution — MAC Flooding (INSTRUCTOR ONLY)

## Model Solution

**Technique:** **MAC flooding** (CAM-table overflow attack) from port 12.

**Mechanism:** a switch learns source MACs by populating its CAM table
(MAC → port). The flooder emits thousands of frames with **random source
MACs**; each new fake MAC occupies a table slot until aging. Once the table
is saturated (8,180/8,192), the switch cannot learn *real* MACs and must
**unicast-flood** frames for unknown destinations out every port in the VLAN.
Every guest's NIC now sees frames addressed to other guests (NICs normally
drop non-matching unicast, but sniffing tools or promiscuous-receiver
processes don't). When flooding stops, fake entries age out, real MACs
re-learn, and normal switching resumes — matching the 11:30+ recovery.

**HTTPS vs HTTP guests:** flooded frames are passive-sniffable by anyone in
the flood zone. **HTTP** content (login forms, cookies, rendered pages —
hence "pop-ups" = injected or replayed rendered content) is fully exposed;
**HTTPS** exposes only metadata (SNI/DNS, timings, sizes) because payloads
are encrypted. The **pop-ups imply active injection, not just passive
sniffing**: someone was crafting frames to render content on victims'
browsers — i.e., an on-path *injection* phase piggybacked on the flood,
which raises intent from "curiosity" to "active manipulation."

**Two switch defenses (exact features):**

1. **Port security** — limit MAC count per port (e.g., max 3), violation =
   shutdown/restrict. A 7,000-MAC burst from port 12 gets shut instantly.
2. **Storm control / broadcast-unknown-unicast limits** — caps the frame
   rate that flooding (and other storms) can drive; contains the blast radius
   even from a permitted device.

**Design-flaw policy fix:** guest wired + Wi-Fi in **one VLAN** means any
guest can attack every other guest — segment guest Wi-Fi into its own VLAN/subnet
with client isolation (PSPF/utcloak-style "guest isolation"), wired business
center into another, and route (not bridge) between them at a firewall.

## Alternative Solutions

- **Blame the AV contractor's streaming box.** The CAM trace points at port 12,
  not multicast/streaming patterns (which would show as *multicast* groups,
  not unknown unicast); keep it as a user but the evidence contradicts.
- **Replace the switch stack.** The stack did its job and logged the flooding;
  it needs *configuration*, not replacement.
- **Disable unknown-unicast flooding globally.** Not generally possible —
  flooding is required for legitimate unknown unicast; limiting MACs per port
  and storm control is the correct pair.

## Tradeoffs

- Port-security strictness (max=1 vs 3): tighter = safer but more help-desk
  tickets when users dock + phone + tablet. Pick per port class.
- Guest isolation vs usability (printing, Chromecast): full isolation breaks
  casting/printing; propose an isolated "device" SSID as compromise.

## Common Mistakes

- Calling it "ARP spoofing" — no identity claims are forged here; it's
  table *capacity* exhaustion.
- Explaining that victims "see traffic" without the unknown-unicast mechanism.
- Missing the injection implication in the pop-up reports.
- Proposing only Wi-Fi fixes for a wired-port attack.

## Instructor Prompts

- "Why is this attack self-limiting in time — and how would an attacker
  make it persistent?" (looping flooder; then port security beats it.)
- "Which evidence line distinguishes flooding from a multicast storm?"
- "How does this attack differ in goal from ARP spoofing?" (volume-DoS + sniff
  vs identity theft/on-path.)

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | CAM learning → unknown-unicast chain; intent inference from pop-ups |
| Technical accuracy | 25% | Correct feature names (port security, storm control); aging behavior |
| Alternatives considered | 20% | Rejected hypotheses tied to evidence |
| Communication | 15% | Clear mechanism narrative |

**Timing:** reveal at 5:00; the "how would an attacker make it persistent"
prompt lands port security's purpose.

## CLO Mapping

- **CLO-2** — Switch learning mechanics → L2 attack analysis.
