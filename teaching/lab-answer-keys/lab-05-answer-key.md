---
lab: Lab-05
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-05 (Segmentation & Proxy Egress Design)

## Reference design (grading anchor)
- **Zones (5+):** Internet / DMZ (e-commerce web tier) / Corporate (staff +
  finance as a sub-scope) / OT-Warehouse (scanners, legacy flat segment) /
  Management (switches, hypervisors, jump path) / Servers (internal apps,
  optional).
- **Enforcement points:** internet↔DMZ (reverse proxy/WAF + firewall), DMZ↔
  internal (firewall, one-way initiations), corporate↔OT (firewall + protocol-
  specific allows for the legacy software — *not* flat), user↔management
  (jump host only, no direct routes), all egress via explicit proxy (corporate)
  and constrained NAT (DMZ/OT).
- **Egress allow-list exemplar rows:** corporate→SaaS (categories + FQDN list,
  443 via proxy, full log); corporate→DNS (internal resolvers only); DMZ→patch
  endpoints (allow-listed mirrors); OT→vendor endpoint (single FQDN, scheduled
  window, protocol pinned); printers→vendor cloud (time-boxed, rate-limited).
  Default-deny everywhere; proxy logs → SIEM (the Lab-13 storyline's fix).
- **L2 hygiene:** DHCP snooping (uplink trusted only), DAI on access ports,
  port security + 802.1X corporate, MAB quarantine VLAN for printers/IoT,
  BPDU/root guard on access ports (from L06 vocabulary).
- **Residual risks (≥3 expected):** legacy OT software needing intra-zone
  flatness (compensating: OT-dedicated monitoring + egress pinning); SaaS
  category drift (compensating: monthly allow-list review); TLS-inspected
  privacy/legal scope (compensating: scope document + logging of inspection
  events); printer vendor endpoints changing (compensating: FQDN monitoring).

## Analysis-question model answers (grading pointers)
1. Trust sentences: "internet trusts nothing; DMZ serves but never initiates
   inward; corporate authenticates for anything" — reward *policy sentences*,
   not topology recital.
2. Proxy costs: latency, privacy/legal scope, TLS-inspection breakage
   (pinning), bypass temptation (shadow egress); failure modes: proxy outage =
   egress outage (HA question), and implicit-trust of the proxy itself.
3. "443-only" insufficient: C2 rides 443; the value is destination policy +
   logging, not port arithmetic.
4. Microsegmentation beats VLANs for finance (PCI scope) and management plane;
   overkill for printers.
5. Pipeline: DNS/proxy logs shipped to SIEM with retention — beacon cadence
   becomes visible; the design must *state* the shipping, not assume it.

## Grading notes
- Diagrams without enforcement points on every inter-zone path cap at pass.
- Egress tables with "allow HTTPS" rows fail the function-split test.
- Peer-review notes must show a *changed* decision — reviews that changed
  nothing are graded as not performed.

## Command status
Design lab — no commands; ✅/⚠️ n/a (stated on handout).
