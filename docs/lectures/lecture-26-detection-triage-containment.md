---
lecture: L26
title: Detection, Triage & Containment
module: 7
week: 13
hours: 2
clos: [CLO-11, CLO-12]
difficulty: advanced
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-07-incident-response/lectures/lecture-26-detection-triage-containment.md
---

# L26 — Detection, Triage & Containment

## 1. Learning Objectives

By the end of this session you can: (1) execute alert triage — validate, enrich, classify, decide — with documented reasoning; (2) scope an intrusion across hosts/accounts/data using cross-source correlation; (3) build an incident timeline from heterogeneous evidence with clock discipline; (4) rank containment options by disruption vs evidence trade-offs; (5) produce an incident-state document a peer can continue from.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Triage | Validate → enrich → classify → decide, with written reasoning |
| Enrichment | Adding asset/identity/threat context to an alert |
| Scope statement | known-compromised / suspected / cleared — with evidence lines |
| Timeline anchor | Dated event backed by cited evidence (≥1 source; 2 preferred) |
| Clock discipline | Recording sensor time sources and offsets before correlating |
| Containment ladder | Ranked options from least to most disruptive (host and segment level) |
| Incident-state doc | Scope + timeline + actions + evidence index + open questions + next steps |
| Watch item | Indicator tracked without (yet) an incident (L28) |

## 3. Detailed Explanations

### 3.1 The triage method (repeatable, gradeable)
1. **Validate:** is the alert true? Pull raw evidence first — rule out detector misconfiguration (L22 tuning) before acting.
2. **Enrich:** asset context (owner, criticality — L24 inventory), identity context (who's logged in), threat context (intel on the indicator — L28 preview).
3. **Classify:** severity matrix (impact × urgency) → response SLA; assign the playbook (L25).
4. **Decide:** escalate / dispatch / monitor — with the reasoning *written down*. The triage note is an evidence artifact.

### 3.2 Scoping the intrusion
The question set: which hosts beacon to the same indicator? which accounts authenticated anomalously? what lateral traffic followed? what data moved? **Cross-source joins** answer them: Zeek UID joins (L23), flow pivots (L21), auth-log correlation, DHCP/IP→host resolution (L03 logs), cloud flow logs (L19–L20) for hybrid cases. Assume the initial scope is wrong: **sweep patterns** (many-445 flows) and **staging patterns** (burst to one host before egress) are the expansion signals. The scope statement — known / suspected / cleared, each with evidence — updates continuously.

### 3.3 Timeline construction
Normalize time sources *first* (record sensor clock offsets — a 4-minute drift changes your story), UTC everywhere. Anchor events: initial access (hypothesis), first beacon, lateral hops, staging, egress attempt — each with a citation (log line, flow record, pcap frame). A spreadsheet with citation discipline beats fancy tools without it.

### 3.4 Containment strategy — the trade-off skill
- **Per host:** network-isolate (quarantine VLAN — host stays alive for forensics), power-off (stops damage, kills memory), rebuild-only (evidence lost), monitor-in-place (risky but evidence-rich).
- **Per segment:** quarantine VLAN, ACL choke, port shutdown, emergency firewall rule — L10/L11 skills become IR tools.
- **Decision inputs:** attacker sophistication (do they know they're caught?), evidence value, business impact, spread velocity — and the L25 authority matrix.
- **The containment paradox:** aggressive containment alerts a watching adversary → staged/quiet containment for sophisticated cases — a *documented* decision, not improvisation.

### 3.5 Handoff documentation (CLO-15 in action)
The incident-state doc: scope statement, timeline, containment actions + timestamps, evidence index (acquisition-log refs), open questions, next-step queue. **The test:** a peer continues your incident from the doc alone — this is the graded standard (Assignment 6's rubric line).

## 4. Network Diagram: triage → scope → contain

```
 Alert ─► validate (raw evidence) ─► enrich (asset/identity/intel)
      ─► classify (severity, playbook) ─► decide (escalate/dispatch/monitor)

 Scope: [known-compromised: WEB-03]  [suspected: FS-02 (staging burst)]
        [cleared: rest of subnet — evidence cited]

 Contain: WEB-03 → quarantine VLAN (keep running: memory/flows valuable)
          FS-02 → monitor + capture window; decision logged w/ authority ref
```

## 5. Protocol Examples

```
 # 1. The alert (Suricata sid 1000001 — your L22 rule!) fired on 10.0.20.15
 # 2. Pivot: same external IP from other hosts?
 zeek-cut ts id.orig_h id.resp_h < conn.log | grep 198.51.100.77 | awk '{print $3}' | sort | uniq -c
 # 3. Lateral sweep check: many-445 pattern from 10.0.20.15
 zeek-cut id.orig_h id.resp_p < conn.log | grep 10.0.20.15 | grep '\.445' | wc -l
 # 4. Timeline rows: ts | event | [evidence refs]
 # 5. Containment: quarantine VLAN for .15 only — decision + authority cited
```

## 6. Configuration Concepts (concept level)

- Quarantine VLAN pre-built (L12 NAC pays off here); emergency ACL templates versioned.
- SIEM case/note fields mapped to the incident-state template.
- Evidence-capture automation: one command pulls the flow/pcap window + hash + log entry.

## 7. Security Implications

- Triage is a documented method — citations, always; "I have a feeling" is not analysis.
- Scope is a hypothesis under continuous revision; cross-source joins grow it honestly.
- Containment is a portfolio of trade-offs; the authority matrix and evidence value pick the rung.

## 8. Realistic Organizational Scenario

**The live staged incident (the course's centerpiece).** Mid-lecture, a beacon alert fires on the range: your team executes the L25 playbook — validate, enrich (finance workstation, grants officer), scope (second host? sweep? staging burst to a file server at 03:00?), timeline, containment (isolate workstation; monitor file server), and the handoff doc that passes peer review. Then the inject escalates. This *is* Assignment 6; the full case write-up is **cs-081** (phishing-driven intrusion triage).

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "The alert is the incident" | The alert is a hypothesis; scoping defines the incident. |
| "Contain everything immediately" | Sometimes right; often destroys evidence and tips off the attacker — decide, don't reflex. |
| "Scope = the alerted host" | The sweep/staging patterns define scope; assume wider until evidence narrows. |
| "Eradication is an antivirus scan" | It's entry-vector + persistence + credentials (L27). |
| "Notes are for humans, not cases" | The incident-state doc *is* evidence — treat it accordingly. |

## 10. Classroom Activities

1. **Staged incident (60 min across waves, teams of 4):** run the playbook end-to-end — triage note, scope statement, timeline (≥6 anchored events with citations), containment plan with trade-off defense, incident-state doc passing peer handoff.
2. **Severity-matrix drill:** three alerts → classify and route.
3. **Clock-drift exercise:** two sensors 4 minutes apart — reconcile the timeline.

## 11. Problem-Solving Questions

1. The first alert was true — but scoping found two more hosts. What does that tell you about your detector and your playbook?
2. When is "monitor in place" the correct containment choice, and what risk are you accepting *in writing*?
3. Your best sensor had 4 minutes of clock drift: how does that change the timeline, and what do you write?
4. The compromised account belongs to the CFO: what changes in notification chain and evidence handling?
5. Why is the incident-state doc an *evidence artifact*, not just notes?

## 12. Exit Ticket

1. Order the triage steps and name the one most often skipped.
2. What distinguishes "known-compromised" from "suspected" — evidence-wise?
3. Give one containment option per rung (host, segment) and the trade-off each accepts.
4. Why normalize clock sources *before* building the timeline?
5. What single test proves your incident-state doc is adequate?

*(Answers: `teaching/answer-keys/answer-key-module-07.md`.)*

## 13. References

- NIST SP 800-61 Rev. 2 — detection/analysis and containment guidance.
- NIST SP 800-86 — evidence/timeline integration.
- Zeek/nfdump documentation — pivot tooling.
- MITRE ATT&CK — scoping mapping (T1071/T1021/T1567 in the staged incident).
- SANS IR Handbook — triage/scoping checklists.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-11 | §3 triage/scoping/containment | Assignment 6 (W13), Capstone IR, Final |
| CLO-12 | §3.2 cross-source correlation | Assignment 6 (W13), Capstone |
