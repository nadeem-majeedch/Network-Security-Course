---
lecture: L25
title: IR Lifecycle & Preparation
module: 7
week: 13
hours: 2
clos: [CLO-11]
difficulty: advanced
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-07-incident-response/lectures/lecture-25-ir-lifecycle-preparation.md
---

# L25 — IR Lifecycle & Preparation

## 1. Learning Objectives

By the end of this session you can: (1) walk the NIST SP 800-61 lifecycle and place any incident activity in it; (2) define IR roles and the pre-delegated authority model; (3) draft an incident playbook (trigger, first-hour checklist, evidence steps, escalation, comms); (4) apply evidence-handling basics — order of volatility, acquisition logging, chain of custody; (5) explain why preparation is the highest-leverage phase.

## 2. Key Definitions

| Term | Definition |
|---|---|
| IR lifecycle (NIST 800-61) | Preparation → Detection & Analysis → Containment/Eradication/Recovery → Post-Incident |
| Playbook | Pre-written response procedure: trigger, roles, actions, evidence steps, escalation |
| Pre-delegated authority | Decisions responders may make unilaterally (e.g., isolate a host) vs sign-off-required |
| Order of volatility | Evidence decay order: memory → network state → disk → archives |
| Acquisition log | Who/what/when/how + hash for every evidence acquisition |
| Chain of custody | Signed transfer history proving evidence integrity |
| Out-of-band comms | Alternate channel when the compromised network can't be trusted |
| Tabletop exercise | Discussion-based rehearsal with scenario injects and decision logging |

## 3. Detailed Explanations

### 3.1 The lifecycle as a loop
- **Preparation** decides whether the other phases work: logging coverage (L21), detection quality (L22–L23), playbooks, authority pre-delegation, contact trees, out-of-band comms.
- **Detection & analysis:** triage and scoping (L26's craft).
- **Containment → Eradication → Recovery:** staged and evidence-aware (short-term containment → preserve → eradicate → validated recovery — L26/L27 cover execution).
- **Post-incident:** lessons learned that *change controls* — feeding back into preparation. The loop, not the line, is the model.

### 3.2 Roles and the 03:00 problem
Core roles: **incident lead** (owns decisions), technical responders (network/systems/malware), comms lead, executive sponsor, legal/HR liaisons (insider cases). **Pre-delegated authority** answers the 03:00 question: what may the on-call junior do alone (isolate a host — yes), what needs sign-off (segment-wide disconnection, takedown requests)? Ambiguity at 03:00 is the real risk. **Out-of-band comms:** if the network is the crime scene, your comms channel cannot be the network.

### 3.3 Playbook anatomy (the graded artifact)
- **Trigger:** what activates this playbook (alert id, criteria).
- **First-hour checklist:** verify (true positive?) → scope-lite (how many hosts?) → **preserve** (snapshot flows/pcap *before* containment) → contain (least-disruptive option) → escalate criteria → notify list.
- **Evidence steps embedded:** order-of-volatility sequence; acquisition-log template fields.
- **Comms templates:** initial internal notice, exec update, external/regulatory hold — pre-written, legally reviewed.
- **Scenario families:** malware/beacon, credential compromise, data exfil, DDoS (L08 callback), insider (legal-involving).

### 3.4 Evidence-handling fundamentals
**Order of volatility** for network evidence: flows expire, pcap ring buffers overwrite, DHCP/DNS logs rotate — network artifacts often decay *fastest*, so pull them first among accessible items. **Acquisition discipline:** documented tool + version, source, time (with clock-source note), hash at acquisition; work on copies, originals sealed. **Chain of custody:** signed transfer log; the "defensible report" standard (L30) rests on this discipline.

### 3.5 Preparation metrics and exercises
Readiness metrics: MTTD from the pipeline (L21), playbook coverage of ATT&CK-informed scenarios (L05), contact-tree test cadence, restore-test results. **Tabletops:** scenario injects, decision logging, gap capture → the preparation backlog. (L27 runs one; L31 runs the capstone-scale version.)

## 4. Network Diagram: lifecycle + evidence volatility

```
        ┌───────────── Post-Incident (lessons → controls) ─────────────┐
        ▼                                                              │
 [Preparation] → [Detection & Analysis] → [Containment] → [Eradication/Recovery]
   playbooks        triage/scoping (L26)     staged, evidence-aware (L27)

 Volatility (acquire in this order):  memory → flows/pcap window →
                                      conn/NAT state → disk → backups
```

## 5. Protocol Examples

- Acquisition-log template (the class fills this during the exercise):

```
 Case ID: INC-2026-0117
 Evidence: pcap slice 10.0.20.0/24, 02:00-02:40 UTC, sensor zeek-01
 Tool: tcpdump 5.0.1 (+ zeek-cut), clock: NTP-synced, drift <50ms
 Acquired by: A. Student, 2026-09-20 09:12 UTC
 SHA256: <computed at acquisition>
 Transfers: → evidence vault (signed), 09:30 UTC
```

- Order-of-volatility applied to a beacon host: memory (if authorized) → flow/pcap window → routing/conntrack state → disk image → backups.

## 6. Configuration Concepts (concept level)

- Alert-to-playbook mapping in the SIEM (each alert id links its playbook).
- Evidence vault: immutable storage (WORM/object-lock), access logging.
- Contact tree + out-of-band channel tested quarterly.

## 7. Security Implications

- Preparation is the phase you're in *right now* — logging, authority, playbooks decide everything downstream.
- Playbooks embed evidence steps; containment is ranked by disruptiveness *and* evidence cost.
- Chain of custody turns observations into defensible facts — the standard L30 grades.

## 8. Realistic Organizational Scenario

**The peer university's ransomware (running case).** Their post-mortem shows failures at every phase: backups untested, no pre-delegated authority, comms over the compromised network, evidence overwritten by reboots. Your deliverable: map each failure to a lifecycle phase, rewrite the five highest-impact preparation items as actionable controls with owners, adapt the class beacon playbook into a ransomware variant (isolation doctrine changes: *segment*, not host), and define the tabletop that would have caught each gap. Full case: **cs-079**; the playbook drafting is the in-session exercise.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "IR starts when the alarm fires" | It starts in preparation — everything after reflects it. |
| "Containment first, evidence later — always" | Sometimes right (active destruction); the playbook decides, with trade-offs stated. |
| "IR is the security team's job alone" | Legal, HR, comms, and executives have scripted roles. |
| "Chain of custody is court paperwork" | It's what makes internal conclusions defensible too. |
| "Tabletops are theater" | They are the cheapest way to find broken authority and contact trees. |

## 10. Classroom Activities

1. **Playbook drafting (teams of 4, role cards):** beacon-compromise playbook — trigger, first-hour checklist, evidence steps with acquisition-log template, notify list, ranked containment options. Best draft becomes the class reference for L26's staged incident.
2. **Authority-matrix build:** 10 decisions → unilateral vs sign-off, with rationale.
3. **Volatility ordering drill:** six artifacts → acquisition order with justification.

## 11. Problem-Solving Questions

1. Why does containment *before* evidence capture sometimes destroy the case — and when is it still the right call?
2. Your best analyst is unreachable and the beacon is spreading: what does the authority matrix allow the on-call junior to do alone?
3. Which single preparation investment buys the most MTTR reduction — argue from your L21/L22 work?
4. Who owns the comms decision when the incident involves student records?
5. A tabletop reveals no one can restore from backups: which phase failed, and what changes?

## 12. Exit Ticket

1. Name the four NIST lifecycle phases in order — and the loop back.
2. Order by volatility: disk image, running memory, DHCP logs, archived backups.
3. What three fields must every acquisition-log entry include?
4. Give one unilateral action and one sign-off-required action — and why the line sits there.
5. What makes a playbook "ready" rather than "written"?

*(Answers: `teaching/answer-keys/answer-key-module-07.md`.)*

## 13. References

- NIST SP 800-61 Rev. 2 — Computer Security Incident Handling Guide.
- NIST SP 800-86 — forensic integration (order of volatility, evidence).
- SANS IR Handbook — playbook patterns.
- RFC 2350 — expectations for CSIRTs.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-11 | §3 lifecycle/preparation/playbook craft | Assignment 6 (W13), Capstone IR, Final |
