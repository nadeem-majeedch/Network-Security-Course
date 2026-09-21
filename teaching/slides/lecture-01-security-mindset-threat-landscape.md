---
marp: true
theme: default
paginate: true
lecture: L01
week: 1
clos: [CLO-1]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Security Mindset & the Network Threat Landscape

**Network Security · Lecture 1 · Week 1**

*Every security control in this course grounds in a protocol — today we
build the vocabulary that makes that possible.*

<!-- notes: OPEN (3 min). Ask: "How many of you use a VPN? A password
manager?" — hands normalize security as ordinary engineering, not
hacker-movie mystique. State the course contract: defensive focus,
authorized environments only. -->

---

## Learning Objectives

By the end of this session you can:

1. **Define** confidentiality, integrity, and availability (CIA) with a
   concrete example each
2. **Distinguish** threat, vulnerability, and risk — and compute a
   qualitative risk statement
3. **Describe** the main threat categories facing networks today
4. **Explain** why *defense in depth* beats any single control
5. **Locate** the course's lab environment and its authorization rules

<!-- notes: Read objectives aloud; tell students these map to Quiz 1 and
the midterm's Section B. Objective 5 is compliance-relevant: the lab
range is the only authorized target. (1 min) -->

---

## Why "Security Mindset"?

- Two engineers look at the same system:
  - Engineer A: *"How does this work?"*
  - Engineer B: *"How does this **fail**? Who benefits from the failure?"*
- Security mindset = systematically asking Engineer B's questions
- The attacker's advantage: they choose **where** and **when**
- The defender's advantage: they choose **what is hard, observed, and
  logged**

<!-- notes: (4 min) Anecdote frame (no real incidents named): a door
lock is engineering; a door lock plus a logged entry list plus a second
gate is security engineering. CS tie-in: code review asks "does this
work"; security review asks "what input makes this lie?" DS tie-in:
notebook with credentials = door propped open with the key taped to it. -->

---

## The CIA Triad

| Property | Protects against | Example |
|---|---|---|
| **C**onfidentiality | Disclosure | Patient records readable only by care team |
| **I**ntegrity | Tampering | Invoice amounts altered in transit |
| **A**vailability | Disruption | Ransomware-encrypted file share |

- Real incidents chain all three: breach → alteration → outage
- Authentication/authorization/non-repudiation build **on** CIA

<!-- notes: (5 min) Drill: lost laptop with unreleased financials —
which property? (Confidentiality primary.) A corrupted scientific
dataset? (Integrity.) DDoS against the campus portal? (Availability.)
This is Quiz-1 Q6 verbatim — flag that. -->

---

## Threat, Vulnerability, Risk

- **Threat** — the actor or event that could do harm
  *(ransomware operator, flood, insider)*
- **Vulnerability** — the weakness that could be exploited
  *(unpatched server, flat network, reused password)*
- **Risk** — the combination, quantified:
  `risk ≈ likelihood × impact`
- Control choice follows: reduce likelihood, reduce impact, or both

<!-- notes: (5 min) Worked example on the board: flood threat + no
offsite backup = high risk; same flood + verified backups = impact cut,
risk drops. Ask students to restate one threat/vuln pair from their own
life (phone, laptop). Midterm B1 asks exactly this triad. -->

---

## The Threat Landscape (Categories)

- **Reconnaissance** — learning the target (often silent, often legal-ish)
- **Interception** — reading traffic (sniffing, MITM)
- **Impersonation** — spoofing identity (ARP/DNS/phishing)
- **Disruption** — denying service (DoS/DDoS)
- **Compromise & persistence** — getting in, staying in
- **Exfiltration** — taking the data out

<!-- notes: (6 min) For each category, one-line example students will
meet in module 2's labs. Emphasize: categories chain — recon feeds
impersonation feeds interception. The course's 100 case studies follow
exactly these chains. -->

---

## Case Preview: The Small-Office LAN (cs-001)

- 25-person office: PCs, printer, file server, guest Wi-Fi
- Question: *what do you protect, from whom, and where are the trust
  zones?*
- You'll draw its trust boundaries in the first lab

![bg right:35% fit](diagrams/01-enterprise-segmentation.md)

<!-- notes: (3 min) Don't teach the diagram yet — pose it: "which lines
on this picture are trust boundaries?" Students meet the full
segmentation model in L09; today it's a puzzle, not an answer. -->

---

## Defense in Depth (Preview)

- Any single control fails eventually
- Layered controls: **prevent → detect → respond**
  - Prevent: segmentation, encryption, MFA
  - Detect: logging, IDS, anomaly analysis
  - Respond: IR plan, backups, practice
- Course arc = exactly these three layers, in order

<!-- notes: (4 min) Map the course: modules 3–5 = prevent, module 6 =
detect, modules 7–8 = respond. Students should hear the syllabus as a
story, not a list. -->

---

## Ethics & Authorization (Course Contract)

- All labs run in the **isolated, instructor-authorized range**
- Never scan, probe, or attack systems you don't own — course or real
- Attack *concepts* are taught to build **defense**
- Deliverables follow the tested-vs-untested labeling standard

<!-- notes: (3 min) Read as contract, not lecture. Cite the course's
safety rules: no unauthorized scanning, no credential theft, no
destructive payloads. Institutions vary — the range is the boundary. -->

---

## Activity: Classify the Incident (5 min)

For each, name the primary CIA property hit and one vulnerability:

1. USB drive with client data lost on a train
2. Gradebook file edited so marks change silently
3. Campus Wi-Fi down during exams

<!-- notes: (5 min including debrief) Pairs. Answers: 1-confidentiality
(no encryption), 2-integrity (no access control/audit), 3-availability
(single point of failure). Expect "availability, but also integrity"
debate on 2 — that's the point. -->

---

## Case Study: cs-001 (5 min reasoning)

- Projected: the small-office LAN case
- Reason in pairs; we discuss approaches, not solutions
- Solution reveals in the case index debrief

<!-- notes: (5 min) Classroom protocol per case-index: projector → 5 min
reasoning → discuss approaches → reveal. Today's focus: stakeholders and
trust zones, not technical depth. -->

---

## Formative Check (Exit Ticket)

- One CIA property + one threat/vuln/risk chain, written in your words
- Bring one question to L02

<!-- notes: (2 min) Collect digitally or on cards. Skim before L02 —
the misconceptions feed the speaker-notes' difficulty section. -->

---

## References & Next

- NIST SP 800-12 (security terminology) — concept framing
- Course case index: cs-001 (today), cs-002 (CIA impact)
- **Next (L02):** Ethernet, ARP, IP, ICMP — the wire's actual mechanics
- Reading: student page `docs/lectures/lecture-01-*.md`

<!-- notes: (1 min) Preview hook: "Next lecture, we make packets
confess." -->
