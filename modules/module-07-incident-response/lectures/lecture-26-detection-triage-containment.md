---
lecture: L26
title: Detection, Triage & Containment
module: 7
week: 13
hours: 2
clos: [CLO-11, CLO-12]
difficulty: advanced
status: complete
artifact-type: teaching-plan
---

# L26 — Detection, Triage & Containment (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L25 (lifecycle, playbooks, authority), L23 (Zeek log fluency), L22 (alert/detection vocabulary), L21 (pipeline).
- **Position:** the live-fire hour: a staged incident starts mid-lecture and teams triage it using every module-6 artifact they built. Assignment 6 (due today) grades the triage workflow; L27 handles the back half (eradication/recovery).
- **Faculty prep:** arm the staged incident (beacon + lateral SMB sweep + one data-staging pattern across range hosts, per cs-081 design); prepare the triage packet (initial alert, access to L23-style logs, flow window).
- **Common misconceptions:** "the alert is the incident"; "contain everything immediately"; "scope = the alerted host"; "eradication is an antivirus scan."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Execute alert triage: validate true-positive, enrich (asset/owner/telemetry), classify severity, and decide escalation with documented reasoning (Apply/Evaluate).
2. Scope an intrusion across hosts/accounts/data using cross-source correlation (logs + flows + directory) — the "who else is touched?" question (Analyze).
3. Build an incident timeline from heterogeneous evidence with clock-discipline notes (Create).
4. Rank containment options by disruption vs evidence-preservation trade-offs and execute the chosen least-disruptive step (Evaluate/Apply).
5. Document the incident state so a handoff responder can continue without oral briefing (Create).

## 3. Detailed Concepts

### 3.1 Triage method (repeatable, gradeable)
- Validate: is the alert true (data supports it) — pull raw evidence *first* (rule out detector misconfig from L22 tuning).
- Enrich: asset context (owner, criticality — L24 inventory), identity context (who's logged in), threat context (intel on the indicator — L28 teaser).
- Classify: severity matrix (impact × urgency) → response SLA; assign playbook (L25's).
- Decide: escalate/dispatch/monitor — with the reasoning written down (the triage note is an evidence artifact).

### 3.2 Scoping the intrusion
- Question set: which hosts beacon to the same indicator? which accounts authenticated anomalously? what lateral traffic followed the beacon? what data moved?
- Cross-source joins: Zeek UID joins (L23), flow pivots (L21), auth-log correlation, DHCP/IP→host resolution (L03 logs), cloud flow logs (L19–L20) for hybrid cases.
- Scope expansion ethics: assume initial scope is wrong; the sweep pattern (many-445 flows) and staging pattern (burst to one host before egress) are the expansion signals.
- Scope statement template: known-compromised / suspected / cleared — with evidence lines; updated continuously.

### 3.3 Timeline construction
- Normalize time sources first (clock drift between sensors — record offsets); UTC discipline.
- Anchor events: initial access (hypothesis), first beacon, lateral hops, staging, egress attempt; each anchor cites evidence (log line/flow record/pcap frame).
- Timeline tools: simple spreadsheet discipline is fine (and auditable); the skill is the citation habit, not the tool.

### 3.4 Containment strategy (the trade-off skill)
- Option ladder per host: network-isolate (ACL/quarantine VLAN — keeps host alive for forensics), power-off (stops damage, kills memory), rebuild-only (evidence lost), monitor-in-place (risky but evidence-rich).
- Option ladder per segment: quarantine VLAN, ACL choke, disconnect switch ports, emergency firewall rule (L10/L11 skills return as IR tools).
- Decision inputs: attacker sophistication (do they know they're caught?), evidence value, business impact, spread velocity — and the authority matrix from L25.
- The containment paradox: aggressive containment alerts a watching adversary → staged/quiet containment for sophisticated cases (documented decision, not improvisation).

### 3.5 Handoff documentation (CLO-15 in action)
- Incident state doc: scope statement, timeline, containment actions taken + when, evidence index (acquisition log refs), open questions, next-step queue.
- Test: a peer continues your incident from the doc alone — the graded standard (Assignment 6's rubric line).

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Recap: playbook readiness check | Teams flash-review their L25 playbook (2 min each) — it runs today |
| 10–25 | Core: triage method | Triage packet walkthrough; severity matrix drill on 3 sample alerts |
| 25–45 | **Staged incident: first wave** | Alert fires (beacon). Teams execute playbook: validate → enrich → classify → first containment decision |
| 45–55 | Break | Instructor quietly arms second wave (lateral sweep + staging) |
| 55–85 | **Staged incident: second wave + scoping** | Teams scope: which hosts, which accounts, timeline build with citations |
| 85–105 | Containment decision council | Each team presents containment plan + trade-off defense; instructor plays adversary/business pushback |
| 105–115 | Debrief + doc check | Peer-handoff test: one team reads another's incident-state doc |
| 115–120 | Wrap + formative | Exit ticket; Assignment-6 collection; L27 trailer: "the incident isn't over when the noise stops" |

## 5. Technical Examples

```
# Triage packet walkthrough (staged data, range):
# 1. Alert (Suricata sid 1000001 fired on host 10.0.20.15, L22 artifact!)
zeek-cut ts id.orig_h id.resp_h id.resp_p proto < conn.log | grep 10.0.20.15 | head
# 2. Pivot: same external IP from other hosts?
grep 198.51.100.77 conn.log | awk '{print $3}' | sort | uniq -c
# 3. Lateral sweep check: many-445 pattern from 10.0.20.15
zeek-cut ts id.orig_h id.resp_p < conn.log | grep 10.0.20.15 | grep '\.445' | wc -l
# 4. Timeline anchors with citations (each row: ts, event, evidence ref)
# 5. Containment: quarantine VLAN for .15 only (keep running: memory evidence) —
#    decision + authority cited per L25 matrix.
```
Expected teaching points: every analytical claim has a citation; containment keeps the host *alive* because memory/flows outrank a fast shutdown here; the doc passes the peer-handoff test.

## 6. Discussion Questions

1. The first alert was true — but scoping found two more hosts. What does that tell you about your detector and your playbook?
2. When is "monitor in place" the correct containment choice, and what risk are you accepting in writing?
3. Your best evidence source (sensor) had clock drift of 4 minutes. How does that change your timeline, and what do you write?
4. The compromised account belongs to the CFO. What changes in your notification chain and evidence handling?
5. Why is the incident-state doc an *evidence artifact* and not just notes?

## 7. Student Activity

**Staged incident triage (60 min across waves, teams of 4):** run the playbook end-to-end: validation through containment decision. Deliverables: triage note, scope statement (known/suspected/cleared), timeline (≥ 6 anchored events with citations), containment plan with trade-off defense, incident-state doc that passes peer handoff. This *is* Assignment 6.

## 8. Problem-Solving Case

**Primary case — cs-081 "Phishing-driven intrusion: first-hour triage" (advanced):**
Scenario: user reports a weird login MFA prompt; SOC has one Suricata beacon alert on their workstation and nothing else. Provided: initial alert, Zeek logs for the subnet (2 h), flow window, DHCP/auth excerpts. Students execute: validate the beacon (true), enrich (host = finance workstation, user = grants officer), scope (beacon IP touched a second host? sweep pattern found? staging burst to a file server at 03:00?), timeline, containment (isolate workstation, reset credentials, monitor file server), and the handoff doc. The staged data mirrors the in-class incident for continuity.
**Linked cases:** cs-082 (containment decision trade-offs).
*(Model solutions: instructor answer-key set, Module 7.)*

## 9. Formative Assessment

1. Order the triage steps and name the one most often skipped.
2. What distinguishes "known-compromised" from "suspected" in a scope statement — evidence-wise?
3. Give one containment option per rung: host, segment — and the trade-off each accepts.
4. Why normalize clock sources *before* building the timeline?
5. What single test proves your incident-state doc is adequate?
*(Answer key: instructor set, Module 7.)*

## 10. Summary & Key Takeaways

- Triage is a documented method: validate → enrich → classify → decide — with citations, always.
- Scope is a hypothesis under continuous revision; cross-source joins are how it grows honestly.
- Containment is a portfolio of trade-offs; the authority matrix and evidence value pick the rung.

## 11. References

- NIST SP 800-61 Rev. 2 — detection/analysis and containment guidance.
- NIST SP 800-86 — evidence/timeline integration.
- Zeek/nfdump documentation — the pivot tooling used in the lab.
- MITRE ATT&CK — scoping mapping practice (T1071/T1021/T1567 in the staged incident).
- SANS IR Handbook — triage/scoping checklists.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-11 | §3.1–3.5 triage/scoping/containment; staged incident | Assignment 6 (today), Capstone IR, Final |
| CLO-12 | §3.2 cross-source correlation over L21–L23 telemetry | Assignment 6 (today), Capstone |
