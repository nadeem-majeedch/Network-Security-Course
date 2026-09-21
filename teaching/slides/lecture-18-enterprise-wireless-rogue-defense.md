---
marp: true
theme: default
paginate: true
lecture: L18
week: 10
clos: [CLO-8]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Enterprise Wireless & Rogue Defense

**Network Security · Lecture 18 · Week 10**

*Operating wireless at scale — and policing the air you own.*

<!-- notes: OPEN (2 min). Hook: "You own the air inside your walls. Do
you know who's transmitting in it?" -->

---

## Learning Objectives

1. **Operate** enterprise WLAN at scale: controllers, SSID design,
  bands
2. **Run** a rogue-AP survey: detect, locate, classify, remove
3. **Distinguish** rogue, evil twin, and neighbor AP classification
4. **Integrate** WIDS alerts into SOC triage (module-6 bridge)
5. **Design** the transition path WPA2 → WPA3 without client breakage

<!-- notes: (1 min) Objective 2 is the practical heart (Lab-09/10);
objective 5 is cs-060's compatibility case. -->

---

## Enterprise WLAN Architecture

- Controllers / cloud-managed APs: one policy plane, many radios
- SSID design: Staff (Enterprise), Guest (isolated), IoT (PSK-isolated
  + allow-listed)
- Band hygiene: 2.4 GHz legacy vs 5/6 GHz capacity

<!-- notes: (5 min) Operational slide — keep vendor-neutral. The SSID
design rows are the policy decisions; cs-054's audit findings map
here. -->

---

## The Rogue-AP Survey

1. **Detect**: WIDS sensors + sweeps (compare against authorized BSSID
  inventory)
2. **Locate**: triangulate/RF walk the signal strength
3. **Classify**: rogue (yours), evil twin (attack), neighbor (not
  yours)
4. **Remove**: port shutdown for rogues; policy report for neighbors

![bg right:34% fit](diagrams/01-enterprise-segmentation.md)

<!-- notes: (6 min) The classification step is the survey's judgment:
disconnecting a neighbor's AP is *not* yours to do. cs-058's case
drills the classification ethics. -->

---

## WIDS: Alerts Into the SOC

- Alert classes: rogue, evil-twin signature, deauth floods, honeypot
  SSIDs
- Triage discipline (module-6 bridge): corroborate RF alert with
  switch-port data + client reports
- Deauth-flood caveat: management-frame protection (802.11w) blunts it

<!-- notes: (5 min) The bridge slide: RF alerts are evidence, not
verdicts — the three-way corroboration habit from L04/L26 applies.
Quiz-4 Q4's WIDS question anchors here. -->

---

## WPA2 → WPA3 Transition

- Transition mode: both enabled — compatibility with downgrade bait
- Client inventory first: the fleet that can't do SAE
- Timeline: inventory → pilot → staff waves → force SAE

<!-- notes: (5 min) cs-060's compatibility case is the design story.
The downgrade-bait honesty from L17 returns — transition mode trades
purity for rollout reality. -->

---

## The 802.1X Rollout (Enterprise)

- RADIUS + IdP integration; certificate enrollment (EAP-TLS) or
  credential method
- Onboarding pain is real: BYOD provisioning flows
- The payoff: per-user accountability, instant revocation

<!-- notes: (4 min) cs-059's deployment case. The payoff line is why
PSK estates migrate — assignment-3's MFA argument echoes it. -->

---

## CS/DS Example: RF Hygiene Around the Cluster

- Cluster management SSID hidden from general floors; separate zone
- WIDS sensor coverage in the DC wing (the crown-jewel air)

<!-- notes: (3 min) DS framing: the data-lake's wireless-adjacent
surface is small but exists — sensors in the DC wing are cheap
coverage. -->

---

## Activity: Classify These APs (6 min)

Four observed BSSIDs: (a) your SSID, unknown BSSID, strong in lobby;
(b) neighbor's coffee-shop SSID; (c) your authorized AP in the wrong
VLAN; (d) an SSID imitating yours asking for credentials. Classify +
respond.

<!-- notes: (6 min) Answers: (a) evil twin (locate now), (b) neighbor —
document, (c) rogue-by-config — port trace + fix, (d) credential-
harvest honeypot — user alert + WIDS rules. The (b) ethics beat
recurs. -->

---

## Case Study: cs-058 (5 min)

- Rogue-AP hunt building survey — method over luck

<!-- notes: (5 min) If cs-058 ran in L17's slot, use cs-060 (WPA3
transition) here — rotation per case-index rules. -->

---

## Formative Check

- Oral: rogue vs evil twin vs neighbor — one sentence each.

<!-- notes: (2 min) Exit oral; the classification triad is examinable. -->

---

## References & Next

- Vendor WIDS guides (concept class reference)
- **Next (L19):** cloud networking I — VPC design & controls
