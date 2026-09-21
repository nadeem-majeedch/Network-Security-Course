---
marp: true
theme: default
paginate: true
lecture: L21
week: 11
clos: [CLO-12]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Monitoring Foundations

**Network Security · Lecture 21 · Week 11**

*You can't detect what you never collected.*

<!-- notes: OPEN (2 min). Hook: "Modules 1–5 built the estate. Module 6
gives it a nervous system." -->

---

## Learning Objectives

1. **Place** monitoring sensors: SPAN/TAP vs inline, edge vs core
2. **Distinguish** packet, flow, and log telemetry by granularity
3. **Design** log-pipeline coverage against the blind-spot map
4. **Baseline** normal behavior as the anomaly reference
5. **Apply** three-way corroboration as the triage discipline

<!-- notes: (1 min) Objective 3 is cs-068's case; objective 5 is the
module's recurring discipline (cs-087/cs-097 test it at forensic
depth). -->

---

## Where Sensors Go

| Position | Sees | Misses |
|---|---|---|
| Edge SPAN | north-south traffic | east-west lateral |
| Core SPAN | east-west + server traffic | encrypted content |
| Inline IPS | everything (can act) | — at latency cost |
| Host agents | endpoint truth | network context |

- Placement = a coverage decision, not a shopping decision

<!-- notes: (5 min) Quiz-11 Q1/Q7's territory. Diagram 07's sensor
placement taught here. The "coverage decision" line is cs-066's case
frame. -->

---

## Three Telemetry Grain Sizes

| Source | Grain | Strength |
|---|---|---|
| PCAP | per-packet | total detail, short window |
| Flow | per-conversation | cheap, long window |
| Logs | per-event | app/identity context |

- Flows find **where**; PCAP explains **what**; logs say **who/why**

<!-- notes: (5 min) The L04 rhythm returns as doctrine. Quiz-11's
grain-size questions; cs-097's correlation case is the expert exam. -->

---

## The Blind-Spot Map

- For each segment: what telemetry covers it? (Draw the map!)
- Classic gaps: user-VLAN east-west, IoT zones, cloud VPC internals
- cs-068's case = finding your map's holes before attackers do

<!-- notes: (5 min) The map is a course artifact students can reuse in
the capstone's detection design. Quiz-11 Q7's two-paths question reads
it. -->

---

## Baselines: The Anomaly Reference

- Baseline = measured normal (volume, peers, timing) per asset class
- Static thresholds rot; per-class baselines flex
- The hunt program (L28) builds baselines as a *byproduct*

<!-- notes: (5 min) cs-067's baseline-deviation case is the worked
instance. The "byproduct" line previews L28's hunt economics. -->

---

## Corroboration: The Three-Way Rule

- One source = hypothesis. Two = supported. Three = corroborated.
- Triage discipline: IDS alert ↔ Zeek log ↔ flow record
- Reports inherit the labels (module 8's defensibility)

![bg right:35% fit](diagrams/07-ids-ips-workflow.md)

<!-- notes: (6 min) Diagram 07 fully taught: sensor→SIEM→triage→(tune|
runbook). The confidence ladder is the course's through-line — cs-087
labels it, cs-100's board paragraph depends on it. -->

---

## CS/DS Example: The Data Lake's Sensors

- Flow logs (cloud) + DNS logs + identity logs = the triad, cloud
  shape
- Baseline: per-service volumes/timings; anomaly = job-pattern shift

<!-- notes: (3 min) DS framing: the lake's telemetry triad is the
capstone's detection design starting point. -->

---

## Activity: Map the Blind Spots (6 min)

Estate: 2 DCs, cloud VPC, branch offices. List five blind spots you'd
expect, and one cheap sensor fix for each.

<!-- notes: (6 min) Expected: branch egress, user east-west, IoT zone,
VPC-internal, management plane. Cheap fixes: flow logs, SPAN, netflow
from switches. cs-066's sensor-placement case rehearses this. -->

---

## Case Study: cs-067 (5 min)

- Baseline deviation in flow data — spot the shift, name the cause

<!-- notes: (5 min) The case's numbers-first discipline mirrors the
lecture's baseline method. -->

---

## Formative Check

- Oral: flows vs PCAP vs logs — one question each answers.

<!-- notes: (2 min) Exit oral — the grain-size triad again, now as
doctrine. -->

---

## References & Next

- NIST SP 800-94 (IDS/IPS guidance)
- Diagrams: `diagrams/07-ids-ips-workflow.md`
- **Next (L22):** IDS/IPS signatures & tuning — the rules get real
