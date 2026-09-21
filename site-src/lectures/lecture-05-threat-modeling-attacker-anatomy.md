# L05 — Threat Modeling & Attacker Anatomy

## 1. Learning Objectives

By the end of this session you can: (1) build an attack tree for a given network and identify minimum-cut defenses; (2) map an intrusion narrative to Cyber-Kill-Chain stages and MITRE ATT&CK techniques; (3) classify reconnaissance as passive/active × external/internal and name the network evidence each produces; (4) turn a modeled attacker step into a *predicted observable artifact*.

## 2. Key Definitions

| Term | Definition |
|---|---|
| Threat model | Structured description of who might attack, how, and what matters |
| Attack surface | Exposure set: services, links, people — where unauthorized interaction is possible |
| Attack tree | AND/OR branching diagram from attacker goal down to leaf actions |
| Minimum cut | Smallest set of defenses whose removal disconnects the goal from all paths |
| Kill chain | Staged intrusion narrative: recon → weaponize → deliver → exploit → install → C2 → actions-on-objective |
| MITRE ATT&CK | Behavioral taxonomy: tactics (the *why*) → techniques (the *how*) → data sources |
| Passive recon | Information gathering without touching the target's network (little/no evidence) |
| Active recon | Probing the target (scans, banners) — leaves evidence in flows/logs |

## 3. Detailed Explanations

### 3.1 Why model at all
Unstructured attacker thinking produces vague defenses ("we need better security"). A model makes reasoning **repeatable and testable**: each modeled step predicts an artifact — a log line, a flow pattern, a packet field. That prediction *is* a detection requirement, and Module 6 builds detections from exactly these predictions.

### 3.2 Attack trees: AND/OR logic from goal to leaves
Start from the attacker's goal ("read the NAS") and branch downward. **OR nodes**: any one child suffices. **AND nodes**: all children required — so a single control on any child kills the whole AND branch. The design question is the **minimum cut**: which few controls prune the most paths? Example: MFA on the VPN + egress filtering together sever most remote-compromise trees at once.

```
 Goal: read NAS blueprints
 ├── OR: compromise a workstation
 │      ├── AND: phish user -> macro runs -> C2 -> lateral to SMB share
 │      └── AND: unpatched service -> exploit -> same
 ├── OR: attack the NAS directly
 │      └── exposed admin UI / default creds
 └── OR: physical: stolen backup disk

 Minimum cuts: MFA+egress (kills branch 1), NAS UI lockdown (2), encrypted+offsite backups (3)
```

### 3.3 The kill chain as narrative scaffold
Stages: **recon → weaponize → deliver → exploit → install → C2 → actions-on-objective**. Its teaching value: each stage predicts observable network artifacts — recon → scan patterns in flows; delivery → mail/URL in proxy logs; C2 → periodic beacons; exfil → volume spikes. Its limitation: modern intrusions are non-linear and fast; treat the chain as a *narrative scaffold*, not a checklist.

### 3.4 MITRE ATT&CK: the defender's shared language
Tactics = objectives (Initial Access, Lateral Movement, C2, Exfiltration…); techniques = methods (T1566 phishing, T1021 remote services, T1071 application-layer C2, T1048 exfil over alternative protocol). Each technique page names **data sources** (network traffic, Netflow) — the bridge from model to detection. In reports, ATT&CK IDs make findings shareable and comparable across teams.

### 3.5 Reconnaissance taxonomy (defender's view)
- **Passive/external:** CT logs, DNS records, job postings, public filings — *no* target-side evidence; answer is exposure reduction, not detection.
- **Active/external:** port scans, version probes, web crawling — visible in firewall/flow logs (many SYNs, odd port sweeps).
- **Internal (post-access):** ARP sweeps, SMB/LLMNR discovery — visible in segment traffic; a Zeek/flow goldmine.
Attacker noise is a **gift**: every probe is free telemetry about attacker intent — if (and only if) your pipelines exist (L21).

## 4. Network Diagram: model → artifact mapping

```
 Attack tree leaf (attacker step)         Predicted network artifact
 ─────────────────────────────────       ─────────────────────────────
 "scan the perimeter"           ────►    many SYNs, no completes (flows)
 "phish -> macro -> C2"         ────►    DNS to fresh domain; beacon cadence
 "enumerate SMB shares"         ────►    many 445/tcp flows from one origin
 "exfil over HTTPS"             ────►    volume spike to one external host
```

## 5. Protocol Examples

- Scan shapes in flows: `-sS` scan = SYN without completion across ports/hosts; `-sV` adds banner exchanges after open ports. Reading the *shape* (sweep vs sweep+probe) tells you the actor's intent level.
- C2 beacon shape: regular ~60 s small HTTPS flows to a fresh domain — same shape you met in cs-010.

## 6. Configuration Concepts (concept level)

- Asset + exposure inventory: internet-facing services list (feeds attack-surface discussion).
- Flow retention window: long enough to answer "was this scanned before?" (L21).
- Detection backlog seeded from your model's unmapped leaves (L22 work).

## 7. Security Implications

- Models convert attacker reasoning into *defensible engineering requirements*.
- Minimum-cut thinking beats control shopping: prune the most paths with the fewest controls.
- Passive recon is invisible on your network — reduce exposure (public records, cert sprawl) instead of trying to "detect" it.

## 8. Realistic Organizational Scenario

**The two-tier web app (running case).** Public nginx fronts an internal API host and a PostgreSQL server; a jump host separates them from the corporate LAN — and, for vendor support, allows SSH from anywhere. Your attack tree's cheapest path now runs through that jump host. The question set: which leaf did the vendor exception reopen, what single control closes it with least disruption (restrict source, not close), and which ATT&CK techniques + data sources apply? This is **case cs-011**, and the tree you build feeds every Module-2 lab.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "Threat modeling is for app teams" | Network defenders model paths, positions, and tools — same discipline. |
| "ATT&CK is a checklist to complete" | It is a shared language for describing behavior and planning coverage. |
| "Recon is a tool, not a stage" | Recon predicts everything downstream; its *shapes* are detectable. |
| "A scan alert means an attack" | Scans are noise until correlated; alert, then judge intent with context. |
| "More controls = better" | Minimum-cut reasoning: prune most paths with fewest, independent controls. |

## 10. Classroom Activities

1. **Build the tree (teams of 3):** attack tree + top-5 expected ATT&CK techniques + data sources for your assigned segment diagram.
2. **Narrative mapping:** four-stage intrusion on cards → place each in kill-chain stage + ATT&CK technique.
3. **Minimum-cut debate:** which single control prunes the most paths on the class tree — argue with branches, not opinions.

## 11. Problem-Solving Questions

1. Which kill-chain stage is cheapest for the defender to break, and why does the answer change with attacker skill?
2. How do you turn an ATT&CK technique page into an actual detection? Name the intermediate artifact.
3. Why do defenders still alert on scans, and when is that alerting counterproductive?
4. Your model assumes attackers come from the internet. Which insider scenario breaks it, and which control covers both cases?
5. Why does closing 3389 to the internet beat adding a better exploit *detector* for that same exposure?

## 12. Exit Ticket

1. Define attack surface in one sentence for the small-office LAN from L01.
2. Place "T1071.001 Web Protocols C2" in the kill chain — which stage, which artifact?
3. Passive vs active reconnaissance: what distinguishes them in terms of defender evidence?
4. In an attack tree, what does an AND node assert about defenses?
5. Give one technique from today's mapping and its primary network data source.

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- MITRE ATT&CK Enterprise Matrix — https://attack.mitre.org (current).
- Hutchins, Cloppert, Amin — "Intelligence-Driven Computer Network Defense… Kill Chains" (Lockheed Martin).
- NIST SP 800-154 — data-centric system threat modeling.
- Shostack, *Threat Modeling: Designing for Security* — attack trees, STRIDE.
- CAPEC — Common Attack Pattern Enumeration (https://capec.mitre.org).

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-2 | §3 frameworks + mapping skill | Quiz 2 (W4), Lab-03, Case set A |
