---
lecture: L05
title: Threat Modeling & Attacker Anatomy
module: 2
week: 3
hours: 2
clos: [CLO-2]
difficulty: beginner-intermediate
status: complete
artifact-type: teaching-plan
---

# L05 — Threat Modeling & Attacker Anatomy (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** L04 (Module-1 protocol/triage fluency). Useful from L01: actor classes and vantage points.
- **Position:** opens Module 2 by giving students a *structured* way to reason about attacks before studying individual techniques. All later detection work (L21–L23) and the capstone IR exercise assume students can name attacker objectives and stages precisely.
- **Faculty prep:** print two network diagrams (small office; campus segment) for attack-tree exercise; have MITRE ATT&CK open; prepare a 4-stage intrusion narrative on cards.
- **Common misconceptions:** "threat modeling is for application teams only"; "MITRE ATT&CK is a checklist you complete"; "reconnaissance is a tool, not a stage."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Define threat model, attack surface, attack vector, and entry/egress paths; distinguish threat from vulnerability from exploit (Understand).
2. Construct an attack tree for a given network and identify the minimum-cut defenses (Create/Analyze).
3. Map an intrusion narrative to Cyber-Kill-Chain stages and to MITRE ATT&CK tactics/techniques (Analyze).
4. Describe reconnaissance categories (passive vs active, external vs internal) and the network evidence each produces (Understand).
5. Explain how modeling drives detection: each modeled step predicts a log/capture artifact (Analyze).

## 3. Detailed Concepts

### 3.1 The vocabulary that makes analysis repeatable
- Asset → what's protected; Attack surface → exposure set (services, links, people); Vector → how a step is delivered; Exploit → the code/technique realizing it.
- Modeling methods survey: attack trees (AND/OR branches), STRIDE (spoof/tamper/repudiation/info-disclosure/DoS/elevation — applied per trust boundary), MITRE ATT&CK (behavioral taxonomy).
- Where each shines: trees for design review, STRIDE for trust boundaries, ATT&CK for detection planning and reporting.

### 3.2 Cyber kill chain as intrusion narrative
- Stages: recon → weaponize → deliver → exploit → install → C2 → actions-on-objective.
- Teaching use: stages predict *observable network artifacts* (recon → scans in flows; delivery → email/URL in proxy logs; C2 → periodic beacons; exfil → volume spikes). Kill chain criticism too: linear model vs modern in-memory/fast operations; use as a narrative scaffold, not gospel.

### 3.3 MITRE ATT&CK for network defenders
- Tactics (the why) vs techniques (the how) vs sub-techniques; Enterprise matrix highlights relevant to this course: Reconnaissance, Initial Access (T1190 exploit public app, T1078 valid accounts), Lateral Movement (T1021 remote services), Command & Control (T1071 application-layer protocol, T1090 proxy), Exfiltration (T1048 exfil over alternative protocol).
- Data-source thinking: each technique names data sources (network traffic, Netflow) — the bridge to L21–L23 detections.

### 3.4 Reconnaissance taxonomy (defender's view)
- Passive/external: certificate-transparency logs, DNS enumeration, public filings, job postings — little network evidence; hard to detect, so reduce *exposure*.
- Active/external: port scans, service/version probes, web crawling — visible in firewall/flow logs (SYN patterns, odd port sweeps).
- Internal (post-access): ARP sweeps, SMB/LLMNR discovery, service enumeration — visible in segment traffic; zeek/flow goldmine.
- Op-countermeasure concept: attacker noise is a *gift* to defenders — detection engineering premise.

### 3.5 From model to control
- Minimum-cut idea: cheapest branch that stops the most paths (e.g., egress filtering kills many C2/exfil trees at once — L12 preview).
- Documenting assumptions: every model is wrong somewhere; state them so IR can revise.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Warm-up: 5-headline ATT&CK sorting | Teams sort real incident summaries into tactics |
| 10–35 | Core: vocabulary + attack trees | Build one tree live on the small-office diagram; demonstrate minimum-cut reasoning |
| 35–55 | Core: kill chain + ATT&CK | Map the 4-card intrusion narrative stage-by-stage; show matrix rows and data sources |
| 55–65 | Break | — |
| 65–85 | Core: reconnaissance taxonomy | Flow-log screenshot of a scan; classify each pattern (sweep, version probe, sweep+probe) |
| 85–110 | Student activity: model the campus segment | Teams of 3 build attack tree + top-5 ATT&CK technique list for their segment (cs-011/012 prep) |
| 110–120 | Wrap + formative | Exit ticket; trailer: "next hour: what those tree leaves look like on the wire (L2)" |

## 5. Technical Examples

- **Attack tree (small office, goal: read the NAS):** branches — compromise workstation (phish → macro → C2 → lateral to SMB share), attack NAS directly (exposed admin UI / default creds), physical (stolen backup disk). Class compute: AND vs OR nodes; mark which single control (MFA on VPN + egress filtering) prunes most.
- **Narrative mapping exercise:** "User opens invoice.docm → macro downloads loader → beacons to domain X every 60 s → enumerates SMB shares → copies files to external cloud over HTTPS." Map: T1566 phish → T1204 user execution → T1071.001 web C2 → T1135 network share discovery → T1567.002 cloud exfil.
- **Recon evidence in flows:** `nmap -sS` pattern = many SYNs no completes across ports/host; `-sV` adds banner exchanges; show in a flow record table.

## 6. Discussion Questions

1. Which kill-chain stage is cheapest for the defender to break, and why does that answer change with attacker skill?
2. ATT&CK is descriptive, not prescriptive — how do you turn a technique page into an actual detection?
3. A scan is noise, not harm. Why do defenders still alert on scans, and when is that alerting counterproductive?
4. Your model assumes attackers come from the internet. Which insider scenario breaks it, and which control covers both?
5. Why does reducing attack surface (closing 3389 to the internet) beat adding a better exploit detector?

## 7. Student Activity

**Model the segment (25 min, teams of 3):** each team receives a segment diagram (or uses their L01 trust-zone inventory). Deliverables: (1) attack tree with ≥ 3 top branches and marked minimum cuts, (2) top-5 ATT&CK techniques they expect, each with the network data source that would reveal it. Teams post trees; instructor picks two and stress-tests assumptions live.

## 8. Problem-Solving Case

**Primary case — cs-011 "Attack tree for a two-tier web application" (beginner-intermediate):**
A public web app (nginx) fronts an internal API host and a PostgreSQL server; a jump host separates them from the corporate LAN. Students build the full tree from internet → DB data, mark minimum cuts, and map each leaf to an ATT&CK technique + data source. Twist: the jump host allows SSH from anywhere to support a vendor — students must show which branch that reopens and propose the least-disruptive fix.
**Linked cases:** cs-012 (mapping an intrusion narrative to ATT&CK tactics).
*(Model solutions: instructor answer-key set, Module 2.)*

## 9. Formative Assessment

1. Define attack surface in one sentence for the small-office LAN from L01.
2. Place "T1071.001 Web Protocols C2" in the kill chain — which stage, and what artifact reveals it?
3. What distinguishes passive from active reconnaissance in terms of defender evidence?
4. In an attack tree, what does an AND node assert about defenses?
5. Give one technique from today's narrative mapping and its primary network data source.
*(Answer key: instructor set, Module 2.)*

## 10. Summary & Key Takeaways

- Models make attacker reasoning repeatable and defensible — trees for design, ATT&CK for detection planning.
- Every modeled step predicts an observable artifact; that prediction *is* detection engineering.
- Reconnaissance is the attacker's gift to defenders: learn its signatures in flows.

## 11. References

- MITRE ATT&CK Enterprise Matrix (current version) — tactics/techniques/data sources.
- Hutchins, Cloppert, Amin — "Intelligence-Driven Computer Network Defense Informed by Analysis of Adversary Campaigns and Intrusion Kill Chains" (Lockheed Martin).
- NIST SP 800-154 — guide to data-centric system threat modeling.
- Shostack, *Threat Modeling: Designing for Security* — attack trees & STRIDE method chapters.
- CAPEC (Common Attack Pattern Enumerations) — pattern library complement to ATT&CK.

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-2 | §3.1–3.5 modeling frameworks; activity §7 classification skill | Quiz 2 (W4), Lab-03, Case set A |
