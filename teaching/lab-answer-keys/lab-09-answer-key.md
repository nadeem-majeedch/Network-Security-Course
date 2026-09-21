---
lab: Lab-09
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-09 (Wireless Characterization + VPC Segmentation)

## RF survey exemplar (grading anchor)
Expected ambient environment (instructor APs): `LAB-ENT` (WPA2/WPA3-Enterprise,
802.1X indicators), `LAB-PSK` (WPA3-SAE test SSID), possibly adjacent external
SSIDs (un-owned, classified *external* — do not touch). Table rows must carry
measured channel/band/dBm from the survey file — invented values are an
integrity incident, not a formatting nit. Over-coverage: corridor dBm ≥ −67
typical usable threshold; anything readable from outside the room is the
finding.

## VPC reference build (grading anchor)
- Public subnet: IGW route; NAT GW for private egress.
- App/data private subnets; route tables isolated; no direct IGW on private.
- SGs: sg-web (443 from 0.0.0.0/0 — *inbound only*), sg-app (8080 from sg-web
  only), sg-db (5432 from sg-app only). Egress: data subnet allow-list
  (patch mirror + DNS).
- Behavioral proof: app→db on unlisted port fails (SG); stateful return on
  allowed flows needs no inbound ephemeral rule; the *NACL* on the data subnet
  needs explicit ephemeral inbound for outbound-initiated flows — the contrast
  screenshot pair is the core evidence.
- Default VPC contrast: default SGs allow all egress + same-SG ingress — the
  design smell the lab exists to name.

## Analysis-question model answers
1. **Open SSID:** evil-twin harvesting, captive-portal compromise, session
   sniffing — client-side: 802.1X with *server-cert validation*, VPN on
   untrusted SSIDs; "just don't use it" is not a control.
2. **Hidden SSID:** beacons still carry the name (empty but probe responses
   leak it); clients actively probe known hidden names — worse discoverability
   + interoperability cost; tell the executive: measure, don't hide.
3. **SG/NACL failure scenarios:** SG — cannot explicitly *deny* a subset once
   a broad allow exists (allow-only model); NACL — order-dependent numbered
   rules + stateless ephemeral returns; one scenario each expected.
4. **Egress compliance:** pinned internal mirror (allow-list the mirror) or
   scheduled-window egress with proxy logging; trade-off: freshness vs
   surface.
5. **Shared responsibility:** SG/NACL/route/retention misconfigs = customer;
   fabric/hypervisor faults = provider — the audit boundary: who can *change*
   the control owns its failure.

## Grading notes
- Survey table with invented numbers = integrity flag (re-run or zero).
- The SG-vs-NACL behavioral pair must be *demonstrated*, not recited.
- Cleanup screenshot mandatory (budget discipline is CLO-13-adjacent policy).
- ⚠️ Console/CLI steps are sandbox steps; ✅ `iw dev` scan shapes verified.

## Command status
✅ iw scan/monitor-mode shapes verified at authoring; ⚠️ cloud console steps
and RF environment are environment-dependent.
