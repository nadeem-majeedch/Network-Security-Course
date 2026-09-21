---
lecture: L01
title: Security Mindset & the Network Threat Landscape
module: 1
week: 1
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: teaching-plan
---

# L01 — Security Mindset & the Network Threat Landscape (Teaching Plan)

## 1. Overview & Prerequisites

- **Prerequisites:** none within the course (opening lecture). Incoming co-requisites from prior coursework: Computer Networks (layer models, addressing), basic Linux familiarity.
- **Position in course:** establishes the vocabulary (asset, threat, vulnerability, risk, control) and the authorization/ethics contract that every later lab depends on.
- **Faculty prep:** stage the lab range roster and credential distribution for Lab-01; prepare the campus-network topology poster; review the institutional computer-use policy to quote verbatim.
- **Common misconceptions to anticipate:** "security = buying a product"; "insiders are not attackers"; "a firewall makes a network secure."

## 2. Learning Objectives

By the end of this lecture, students can:

1. Define asset, threat, threat actor, vulnerability, exploit, control, residual risk, and use each term correctly in a scenario (Understand).
2. Relate the CIA triad — and DAD triad (Disclosure, Alteration, Destruction) — to concrete network failure examples (Understand).
3. Categorize threat actors (external, internal, opportunistic, targeted, state-linked) by capability, intent, and targeting (Understand/Analyze).
4. Explain why modern attacks are network-centric and name the four network vantage points an attacker seeks (Understand).
5. State the course authorization rules and explain why they exist (Comprehension/Affect).

## 3. Detailed Concepts

### 3.1 Security as risk management
- Security is the continuous process of reducing **risk = likelihood × impact** to an acceptable level; it is never "done."
- Control classes: administrative (policy), technical (firewall, crypto), physical (locked wiring closet). Every network control is compensating for some protocol-level trust assumption.
- Residual risk and why 100% security is not a design goal; the defender's job is to make attacks expensive and detectable.

### 3.2 CIA triad and its network expressions
- **Confidentiality:** eavesdropping on a shared segment; unencrypted backup traffic; DNS queries leaking browsing history.
- **Integrity:** ARP-rewritten traffic; modified firmware downloaded over HTTP; BGP/route manipulation.
- **Availability:** SYN floods, DHCP exhaustion, link-flooding DoS.
- Extensions students will meet later: authenticity, non-repudiation (Module 4).

### 3.3 Threat landscape taxonomy
- Attacker classes: script kiddies (opportunistic, volume), cybercrime (monetized: ransomware, fraud), hacktivism, insider threat (negligent vs malicious), state/near-state (persistent, patient).
- Attack economics: as-a-service ecosystems (botnet rental, phishing kits) mean low skill can achieve high impact — defenders must assume commodity attacks succeed.
- Kill-chain intuition preview (full treatment L05): attackers chain many small steps; defenders must break at least one.

### 3.4 The four network vantage points
- On-link (same broadcast domain), on-path (MITM position), off-path (remote, volume attacks), infrastructure (compromised router/switch/DHCP/DNS). Most lecture-6–8 attacks are classified by vantage point.

### 3.5 Course ethics and authorization contract
- Lab-only rule; written authorization concept; the difference between security research, pentesting, and unauthorized access in law (brief, non-jurisdiction-specific framing + institutional policy).
- Why defenders learn attack mechanics: detection engineering, control verification, incident triage.

## 4. Teaching Sequence (120 Minutes)

| Time | Segment | Instructor moves |
|---|---|---|
| 0–10 | Warm-up: "What does 'secure' mean?" | Cold-call 3 students; park answers on whiteboard; map to CIA |
| 10–35 | Core: risk & CIA | Chalk-talk with the campus-network poster; tie each CIA leg to a service students use daily |
| 35–50 | Mini-case discussion (ns-01 intro) | Think-pair-share on the stolen-laptop scenario (cs-002 setup) |
| 50–60 | Break + questions | Preview of lab range; distribute credentials |
| 60–85 | Core: threat actors & vantage points | Table: actor class × capability × motivation; students place 5 headlines into the table |
| 85–110 | Student activity: trust-zone inventory | Teams of 3 inventory the classroom/department network on the topology poster (cs-001 groundwork) |
| 110–120 | Wrap + formative | Exit ticket (§9); preview L02 "we go one layer down into the packets themselves" |

## 5. Technical Examples

- Walk through a residential-router admin page over HTTP and an SSH session side by side; ask which leg of CIA each protects and what vantage point defeats it.
- Show `traceroute` output for a campus host and label each hop's vantage-point class; explain why the first-hop router is the most dangerous compromise point for an insider.
- Anonymized headline pack (5 recent public incidents, no live links needed): students classify actor class and primary CIA impact.

## 6. Discussion Questions

1. A university publishes an open guest Wi-Fi with a captive portal. Which CIA leg is weakest, and for whom?
2. Why might a defender deliberately *not* patch a vulnerability immediately? What risks does that create?
3. Which is more dangerous to a campus network: an external ransomware operator or a negligent PhD student with admin rights? Defend your ranking.
4. "We bought a next-gen firewall, so we are secure." Deconstruct this claim using risk vocabulary.

## 7. Student Activity

**Trust-zone inventory (20 min, teams of 3):** using the department topology poster, each team lists assets (DNS/DHCP/DHCP-relay, Wi-Fi controllers, printers, lab VMs), assigns each an owner and a CIA priority, and marks the one asset whose compromise would be most damaging. Teams present in 60 seconds each. This artifact seeds cs-001 and the Module-3 segmentation design work.

## 8. Problem-Solving Case

**Primary case — cs-001 "Asset and trust-zone inventory of a small-office LAN" (beginner):**
A 25-person architectural firm runs one flat /24 network: workstations, a NAS with client blueprints, IP cameras, a guest Wi-Fi on the same switch, and a printer that also receives faxes. The firm's insurance renewal requires a security questionnaire. Students must (a) inventory assets and data flows, (b) assign CIA priorities, (c) identify the five highest-risk exposures, and (d) justify which two they would fix first with a $0 budget.
**Linked cases:** cs-002 (Classifying a lost-laptop incident by CIA impact).
*(Full case files and model solutions are authored in the case-study deliverable set; answers are not distributed in lecture plans.)*

## 9. Formative Assessment

Exit ticket (3 minutes, collected):

1. Define "vulnerability" in one sentence and give a network example.
2. Name the CIA leg most affected by a SYN flood, with a one-line justification.
3. Which actor class would you expect behind a mass scanning campaign of home routers? Why?
4. State one course authorization rule and the reason it exists.
5. What is the difference between a threat and a risk? One sentence each.
*(Answer key deferred to the instructor answer-key deliverable set, Module 1.)*

## 10. Summary & Key Takeaways

- Security is risk management on a network of imperfect protocols, not product procurement.
- CIA gives defenders a shared language for impact; attackers monetize its failure.
- Vantage point determines which attacks are feasible — the organizing idea of Module 2.
- The authorization contract is a professional obligation, not a course formality.

## 11. References

- NIST Cybersecurity Framework 2.0 (functions vocabulary: Govern/Identify/Protect/Detect/Respond/Recover).
- NIST SP 800-12 Rev. 1 (glossary definitions: threat, vulnerability, risk).
- Verizon DBIR (current-year edition) — actor-class statistics for the headline exercise.
- MITRE ATT&CK — browsed live for 5 minutes to show tactic taxonomy (preview of L05).
- Stallings, *Cryptography and Network Security* — ch. 1 (security concepts) any recent edition.
- Institutional IT acceptable-use policy (quote source text in class).

## 12. CLO Mapping

| CLO | Where in this lecture | Assessed via |
|---|---|---|
| CLO-1 | §3.2–3.4 protocol/landscape vocabulary; activity §7 grounds CIA in real assets | Quiz 1 (W2), Midterm |
