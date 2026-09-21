---
case: cs-017
solution-for: modules/module-02-network-threats/case-studies/cs-017-passive-sniffing-flat-lan.md
difficulty: beginner
module: 2
lecture-anchor: L07
clos: [CLO-2]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-017 Solution — Passive-Sniffing Exposure (INSTRUCTOR ONLY)

## Model Solution

**Exposure table (rogue laptop on any port, passive only):**

| Class | Traffic | Bytes % | Reason |
|---|---|---|---|
| **Content-readable** | Internal wiki (HTTP) | **12%** | plaintext page content + session cookies |
| | SMB1 on legacy NAS (assume part of 15%) | **~7%** | SMB1 lacks encryption; signing only authenticates, doesn't hide |
| | Backup job (unknown encryption) | **up to 12%** | "unknown" must be treated as *exposed until verified* — risk-management stance |
| | Internal-leg RTP | ~4–8% | audio content on the internal leg |
| **Metadata-only** | Git-HTTPS, web/mail TLS | 40% | SNI/DNS/timing/size visible; content safe |
| | SRTP VoIP leg | (in the 8%) | signaling metadata |
| **Content-protected** | SSH repo | 10% | SSH-2 encrypted+authenticated |
| | SMB3-encrypted shares | ~8% | encryption on new servers |
| | DNS queries | 3% | full query names visible (metadata that leaks internal hostnames) |

**Headline numbers:** content-readable ≈ **31–39%** of bytes (wiki 12 + SMB1 ~7
+ backup ≤12 + RTP leg up to 8); metadata-only ≈ 43%; protected ≈ 18–26%.
(Students' numbers vary with assumptions — the *reasoning* is what's graded,
but a defensible total is required.)

**Two census rows that break "switches make sniffing impossible":**

1. **The conference-room hub** — a hub repeats *every frame to every port*;
   anything traversing it (presentations, casting, whatever plugs in) is
   readable regardless of switching. The switch's unicast delivery guarantee
   ends at the hub's leg.
2. **Broadcast/multicast/flood traffic** — ARP, DHCP, mDNS, discovery
   protocols reach every port *by design* on the flat LAN, leaking hostname/
   service maps; and any CAM-flooding event (see cs-014) temporarily converts
   the switch into a hub.

**Top-3 fixes by bytes-protected-per-effort:**

1. **Kill the HTTP wiki (12% in one afternoon):** enable TLS (internal CA or
   Let's Encrypt) + HSTS. Highest single-row win; trivial effort.
2. **Retire SMB1 / encrypt SMB on the NAS (~7%):** move legacy shares to SMB3
   encryption or decommission the NAS; also removes a patching liability.
3. **Verify the backup encryption (≤12%):** if the backup tool encrypts,
   document it (reclassify as protected); if not, enable it. One hour of work
   resolves the biggest *uncertainty* in the exposure number.

## Alternative Solutions

- **Segment-first (VLANs) instead of encrypt-first.** Defensible, but on a
  flat 40-person LAN, per-class encryption closed more bytes per unit of
  effort; segmentation is the right *structural* follow-up (Module 3 arc).
- **Ban the hub only.** Necessary, insufficient — it removes the worst leg but
  leaves 30%+ of bytes plaintext-eligible elsewhere.

## Tradeoffs

- Encrypt-in-place vs segment-then-encrypt: encryption is per-service work;
  segmentation is one architectural change but touches everything and can
  break workflows.
- "Unknown = exposed" vs "unknown = fine": treating unknown as exposed spends
  an hour of verification to potentially reclassify 12% of bytes — cheap
  information.

## Common Mistakes

- Answering "switches mean nothing is visible" (the co-founder's belief, inverted).
- Forgetting metadata visibility: even TLS-heavy networks leak hostname maps.
- Leaving the backup job unexamined — "unknown" is a finding, not a shrug.
- Fix list without %-closed arithmetic.

## Instructor Prompts

- "Which row would you verify first, and what changes if it's already encrypted?"
- "Why does DNS visibility matter even when all content is encrypted?"
- "If the co-founder only funds one fix, which one and why?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Per-class classification with correct mechanisms; %-arithmetic |
| Technical accuracy | 25% | Hub/flooding/broadcast exceptions correct; SMB1 vs SMB3 distinction |
| Alternatives considered | 20% | Segment-first weighed honestly |
| Communication | 15% | Clean exposure table + ordered fixes with %-closed |

**Timing:** reveal at 5:00; the "verify the unknown" prompt reinforces
risk-management discipline.

## CLO Mapping

- **CLO-2** — Sniffing exposure quantification and control ranking.
