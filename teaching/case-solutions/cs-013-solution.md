---
case: cs-013
solution-for: modules/module-02-network-threats/case-studies/cs-013-arp-spoofing-incident-containment.md
difficulty: beginner
module: 2
lecture-anchor: L06
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-013 Solution — ARP Spoofing Incident (INSTRUCTOR ONLY)

## Model Solution

**Two bindings vs one:** binding the **gateway IP** pulls *outbound/off-subnet*
traffic through .77; binding the **file server IP** captures *intra-subnet*
traffic that would never cross the gateway. Together they cover both traffic
classes — the attacker sees the full conversation, not half of it. (Also
enables selective forwarding: drop what you don't want users to notice.)

**Symptom mechanics:**

- **Certificate warnings:** the tool at .77 is attempting TLS interception
  (client thinks it's talking to the internal tool; the interception
  presents a certificate that isn't trusted for that name). Modern apps pin
  or validate strictly → warning. It *partially fails* because internal
  tools use either HSTS, pinning, or certs the clients reject — but every
  warning is also proof someone *tried*. Plaintext protocols would produce
  **no** warning — silence is not safety here.
- **Share re-auth prompts:** ARP flapping means the SMB session's TCP
  connection resets mid-conversation when MACs swap between real and spoofed
  paths; the OS re-establishes and re-authenticates. The "sometimes asks
  again" cadence matches the ~2/min re-poison cycle. (Teams audio drops for
  the same flapping reason, recovering when the cache re-stabilizes.)

**Containment order:**

1. **Disable .77's switch port(s)** — stops the poison at the source; CAM
   logs already give you the port history, so this is minutes of work.
2. **Flush ARP caches** on clients (or at least on gateway + file server) and
   **force .77's owner to surrender the laptop for review** — determine
   whether the "debugging tool" was configured for interception and what it
   captured (contractor's credentials? others'?).
3. **Enable DAI + DHCP snooping on the VLAN** (change window) and shorten ARP
   cache timeouts — prevention; plus re-verify contractor tool policy.

**Board one-liner:** "A contractor's laptop ran a network-interception tool
that let it position itself between staff and internal systems for about two
hours; we stopped it at the switch within minutes of detection, no evidence
of data leaving the company, and we're deploying switch-level protections
that make this technique fail automatically in future."

## Alternative Solutions

- **Treat as user error, reboot everything.** Rejected: the ARP alert + CAM
  mobility is attacker-pattern evidence; reboots don't remove the tool.
- **Isolate the whole VLAN mid-day.** Disproportionate; targeted port kill
  achieves containment with zero business interruption.
- **Immediately accuse the contractor.** Evidence first — the tool may be
  legitimately installed but misconfigured; the *interview* follows the
  containment, not the reverse.

## Tradeoffs

- Port-kill now vs interviewing first: port-kill; evidence of *intent* survives
  on the machine, but ongoing interception does not pause politely.
- DAI everywhere vs DAI on this VLAN: DAI is cheap on managed switches —
  do the VLAN now, fleet it later; don't let perfect block urgent.
- Cert-warning fatigue: users dismissing warnings is itself a finding —
  the debrief should land "warnings are telemetry."

## Common Mistakes

- Explaining cert warnings as "the certificates expired."
- Missing the two-binding return-path logic.
- Containment order that flushes ARP before killing the source.
- Board answer that leads with jargon instead of impact-and-action.

## Instructor Prompts

- "Why does the attacker re-send every ~30 s? What would happen if they stopped?"
- "What does the CAM-port mobility tell you about the contractor's movements?"
- "Would 802.1X have prevented this? What about it would need to be configured?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Symptom→mechanism mapping; two-binding logic |
| Technical accuracy | 25% | Correct TLS-interception failure and SMB-reset mechanics |
| Alternatives considered | 20% | Proportionate containment choices |
| Communication | 15% | Board-ready non-jargon one-liner |

**Timing:** reveal at 5:00; the cert-warning discussion is the debrief anchor —
"silence is not safety."

## CLO Mapping

- **CLO-2** — L2 attack mechanics → incident interpretation.
