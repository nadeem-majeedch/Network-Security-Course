---
lab: Lab-03
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-03 (Layer-2 Attack Evidence Analysis)

## Dataset ground truth (generated, seed 403)
54 packets. Background: 1 DORA (10.20.0.101, xid 0x33000001) + 1 DNS pair.
**ARP sweep:** 12 who-has probes from 10.20.0.66 (MAC 02:00:55:55:aa:aa)
probing 10.20.0.100–111 at ~20 ms cadence, unreplied. **ARP poisoning:** 6
unsolicited is-at replies binding 10.20.0.1 → attacker MAC, unicast to two
victim MACs (R1/R2), 0.5 s apart; followed by R1's HTTP session toward the
gateway IP but *attacker MAC* at L2 (the pivot). **DHCP starvation:** 8
Discover bursts (xid 0x44000000+i, MACs 02:00:55:55:dd:00–07), then 8 Offers
offering 10.20.0.200 from source IP 10.20.0.66 (option 54 absent from real
server pattern — the smoking gun is the *source IP* being the attacker).

## Analysis-question model answers
1. **Trust without request:** ARP caches accept is-at replies unconditionally;
   legitimate gratuitous ARP (failover, IP takeover) complicates naive
   "reply-needs-request" filters — DAI handles both via the binding table.
2. **Static-IP hosts:** no snooping binding → DAI must fall back to trusted
   ports, static bindings, or ARP ACLs; the professional answer names the
   operational cost (binding maintenance) not just the feature.
3. **Rogue with correct-looking options + own DNS:** pool exhaustion is an
   outage; DNS redirection is *silent interception* — worse because it
   persists invisibly and enables MITM/credential capture.
4. **IPv6:** starvation≈RAs/DHCPv6 exhaustion; poisoning≈NDP spoofing;
   RA Guard/DHCPv6 guard are the control family. Reward naming NDP as the
   ARP-equivalent *with* its own trust issues (not "IPv6 fixed it").
5. **Capture-window limits:** can claim observed poisoning events + victim
   transits; cannot claim start time, full victim set, or attacker intent —
   report phrasing "observed N unsolicited replies" not "the attacker began".

## Grading notes
- The control-mapping table is the core artifact: DAI+snooping must land on
  *switch ports with trust direction*, not "on the firewall".
- Watch for the misattribution that sweep == poisoning (different frames, different
  threat); and that the rogue Offer's tell is the source IP, not option 53.
- Students claiming attacks "must be reproduced" to verify: point at Lab-03 §7 —
  reproduction is instructor-demo only; analysis of evidence is the skill.

## Command status
✅ Generated + verified (24 ARP frames, 30 IPv4). Filters are Wireshark 4.x
shapes (⚠️ not executed in authoring env).
