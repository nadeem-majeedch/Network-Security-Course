---
lecture: L25
title: IR Lifecycle & Preparation
module: 7
week: 13
hours: 2
clos: [CLO-11]
difficulty: advanced
status: complete
artifact-type: teaching-plan
---

# L25 — IR Lifecycle & Preparation (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L21 (monitoring feeds detection), L24 (vulnerability context). Module 6's detection skills now serve response.
- **Position:** Module 7 opens the response arc. Playbooks drafted today run in L26–L27's staged incident and the capstone IR exercise (CLO-11). Assignment 6 (W13) grades the triage workflow designed here.
- **Faculty prep:** print role cards (IR lead, network analyst, sysadmin, comms, legal liaison) for the playbook exercise; prepare the NIST 800-61 lifecycle diagram handout; stage the L26 incident start-state (notify list, initial alert).
- **Common misconceptions:** "IR starts when the alarm fires"; "containment first, evidence later — always"; "IR is the security team's job alone."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Walk the NIST SP 800-61 lifecycle (preparation → detection & analysis → containment/eradication/recovery → post-incident) and place any incident activity in it (Understand/Analyze).
2. Define IR roles and the escalation/decision authority model (who can take a host offline at 03:00?) (Understand).
3. Draft an incident playbook: trigger, roles, first actions, evidence steps, escalation criteria, comms templates (Create).
4. Apply evidence-handling basics: order of volatility, acquisition logging, chain-of-custody discipline (Apply).
5. Explain preparation as the highest-leverage phase: logging (L21), contacts, retainers, tooling, and tabletop exercises (Evaluate).

## 3. Detailed Concepts

### 3.1 The lifecycle as a loop, not a line
- Preparation: the phase that determines whether the other three work — logging coverage (L21 pipelines), detection quality (L22/L23), playbooks, authority pre-delegation, contact trees, out-of-band comms.
- Detection & analysis: triage (L26 deep-dive) — scope, severity, vector hypothesis.
- Containment → Eradication → Recovery: staged, evidence-aware (short-term containment → system backup/evidence → eradication → validated recovery; L27 covers the back half).
- Post-incident: lessons learned that *change controls* (feeds back to preparation — the loop).

### 3.2 Roles, authority, and the 03:00 problem
- Core roles: incident lead (owns decisions), technical responders (network/systems/malware), comms lead, management/exec sponsor, legal/HR liaisons (insider cases).
- Pre-delegated authority: the decision matrix — what responders may do unilaterally (isolate a host), what needs sign-off (segment-wide disconnection, takedown requests), and why ambiguity at 03:00 is the real risk.
- Out-of-band comms: if the network is the crime scene, your comms channel cannot be the network (pre-staged alternate channel).

### 3.3 Playbook anatomy (the graded artifact)
- Trigger definition: what constitutes *this* playbook activating (alert id, criteria).
- First-hour checklist: verify (true positive?), scope-lite (how many hosts?), preserve (what to snapshot *before* containment), contain (least-disruptive option), escalate criteria, notify list.
- Evidence steps embedded: memory/flows/pcap before power-off (order of volatility), acquisition log fields (who/what/when/how/hash).
- Communication templates: initial internal notice, exec update, external/regulatory hold — pre-written, legally reviewed.
- Per-scenario families: malware/beacon, credential compromise, data exfil, DDoS (L08 callback), insider (legal-involving).

### 3.4 Evidence handling fundamentals
- Order of volatility: registers/memory → network state/connections → disk → archives; network-specific: flows expire (L21 retention tiers matter), pcap ring buffers overwrite, DHCP/DNS logs rotate.
- Acquisition discipline: documented tool + version, source, time (with clock-drift note), hash at acquisition; write-blockers for disks; read-only mounts.
- Chain of custody: transfer log with signatures; storage integrity; the "defensible report" standard (L30 grades it) — evidence without custody is storytelling.

### 3.5 Preparation metrics & exercises
- Readiness metrics: mean time to detect (MTTD) from pipeline (L21), playbook coverage of ATT&CK-informed scenarios (L05 models), contact-tree test cadence, restore-test results.
- Tabletop exercises: scenario injects, decision logging, gap capture → preparation backlog. (L27 runs one; L31 runs the capstone-scale version.)

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Warm-up: "the alert just fired — what's your first action?" | Collect answers; classify into lifecycle stages live |
| 10–35 | Core: lifecycle + roles | 800-61 loop diagram; authority matrix build; out-of-band comms vignette |
| 35–55 | Core: playbook anatomy | Dissect one good playbook; highlight evidence-embedded steps |
| 55–65 | Break | — |
| 65–85 | Core: evidence handling | Order-of-volatility table for network evidence; custody log walkthrough |
| 85–110 | Student activity: playbook drafting | Teams of 4 (role cards) draft the beacon-compromise playbook for the range network (cs-079..080 prep; Assignment-6 prep) |
| 110–120 | Wrap + formative | Exit ticket; Assignment-6 due next session briefing; L26 trailer: "tomorrow the alert actually fires" |

## 5. Technical Examples

```
# Evidence acquisition log (template the class fills during the exercise)
# ---------------------------------------------------------------
# Case ID: INC-2026-0117
# Evidence: pcap slice 10.0.20.0/24, 02:00-02:40 UTC, sensor zeek-01
# Tool: zeek-cut + tcpdump -w, version 5.0.1
# Acquired by: A. Student, 2026-09-20 09:12 UTC
# SHA256: <computed at acquisition>
# Transfers: -> evidence vault (signed), 09:30 UTC
# ---------------------------------------------------------------
# Teaching points: time source noted (NTP, drift <50ms); hash at acquisition;
#   the log itself is evidence — countersign on transfer.

# Order-of-volatility applied to a beacon host (capture sequence, no live attack):
# 1. memory image (if tooling authorizes)  2. flow/pcap window around the beacon
# 3. routing/conntrack state               4. disk image      5. backups
```
Expected teaching points: network evidence expires fastest — flows/pcap pulled *first* among accessible artifacts; the acquisition log is drafted in the playbook, not improvised at 03:00.

## 6. Discussion Questions

1. Why does containment *before* evidence capture sometimes destroy the case? When is it still the right call?
2. Your best analyst is unreachable and the beacon is spreading. What does the authority matrix allow the on-call junior to do alone?
3. Which single preparation investment (logging, playbooks, contacts, exercises) buys the most MTTR reduction — argue from the L21/L22 work you've done?
4. Who owns the comms decision when the incident involves student records? Map the role.
5. A tabletop reveals no one can restore from backups. Which lifecycle phase failed, and what changes?

## 7. Student Activity

**Playbook drafting (25 min, teams of 4 with role cards):** draft the "beacon-compromise" playbook: trigger, first-hour checklist (verify → scope-lite → preserve → contain → escalate), evidence steps with acquisition-log template, notify list with roles, and the least-disruptive containment options ranked. Deliverable: one-page playbook — reviewed against the anatomy checklist; best draft becomes the class reference for L26's staged incident.

## 8. Problem-Solving Case

**Primary case — cs-079 "IR playbook gap analysis for ransomware" (advanced):**
A peer university suffered ransomware; their post-mortem (provided) shows failures at each lifecycle stage: backups untested, no pre-delegated authority, comms over the compromised network, evidence overwritten by reboots. Students must (a) map each failure to a lifecycle phase, (b) rewrite the five highest-impact preparation items as actionable controls with owners, (c) adapt the class beacon playbook into a ransomware variant (isolation doctrine changes: segment, not host), and (d) define the tabletop that would have caught each gap.
**Linked cases:** cs-080 (roles/escalation design for a small IR team).
*(Model solutions: instructor answer-key set, Module 7.)*

## 9. Formative Assessment

1. Name the four NIST lifecycle phases in order — and the loop back.
2. Order by volatility: disk image, running memory, DHCP logs, archived backups.
3. What three fields must every acquisition-log entry include?
4. In the authority matrix, give one unilateral action and one sign-off-required action — and why the line sits there.
5. What makes a playbook "ready" rather than "written"?
*(Answer key: instructor set, Module 7.)*

## 10. Summary & Key Takeaways

- Preparation is the phase you're in right now — logging, authority, playbooks, and exercises decide everything downstream.
- Playbooks embed evidence steps; containment is ranked by disruptiveness *and* evidence cost.
- Chain of custody turns observations into defensible facts — the standard L30 grades.

## 11. References

- NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide (lifecycle authority).
- NIST SP 800-86 — forensic integration guide (order of volatility, evidence).
- SANS IR Handbook — playbook patterns ( practitioner reference).
- RFC 2350 — expectations for computer security incident response (CSIRT framing).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-11 | §3.1–3.5 lifecycle/preparation/playbook craft | Assignment 6 (W13), Capstone IR exercise, Final |
