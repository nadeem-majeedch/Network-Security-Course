---
lecture: L01
title: Security Mindset & the Network Threat Landscape
module: 1
week: 1
hours: 2
clos: [CLO-1]
difficulty: beginner
status: complete
artifact-type: student-lecture-material
instructor-plan: modules/module-01-network-foundations/lectures/lecture-01-security-mindset-threat-landscape.md
---

# L01 — Security Mindset & the Network Threat Landscape

> **Student material.** Companion to the Week-1 lecture. Bring this to class; the
> in-session activities reference it. Full teaching detail lives with your instructor.

## 1. Why This Lecture Exists

Before any tool, command, or attack technique, this course gives you a way of
*thinking*. Security is not a product you install — it is a continuous process of
managing **risk** on a network built from protocols that were designed for
cooperation, not confrontation. Everything else in the next 16 weeks (protocols,
attacks, firewalls, crypto, forensics) hangs off the vocabulary and the mental model
you build today.

## 2. Detailed Explanations

### 2.1 Security as risk management
- **Risk** = the likelihood that a threat exploits a vulnerability × the impact when it does. Defenders do not eliminate risk; they reduce it to an acceptable level and *know* what remains.
- The reduction happens through **controls**, and controls come in three classes:
  - **Administrative** — policies, procedures, training ("who may install software?").
  - **Technical** — firewalls, encryption, ACLs (most of this course).
  - **Physical** — locked wiring closets, badge access (often forgotten, frequently decisive).
- **Residual risk** is what remains after controls. A professional never claims zero risk; they can *name* the risk they accept and why.

### 2.2 The CIA triad — the defender's impact language
| Leg | Meaning | Network failure example |
|---|---|---|
| **Confidentiality** | Only authorized parties can read data | Traffic sniffed on a shared segment; backups exposed |
| **Integrity** | Data is not altered without detection | ARP-rewritten traffic; tampered firmware downloaded over HTTP |
| **Availability** | Services work when needed | SYN flood; DHCP pool exhaustion |
- Extensions you will meet in Module 4: **authenticity** (is this really from the claimed sender?) and **non-repudiation** (can the sender deny it?).
- The attacker's mirror image is the **DAD triad**: Disclosure, Alteration, Destruction — the three things attackers *do* to CIA.

### 2.3 The vocabulary that makes analysis precise
| Term | Definition | Example on a campus |
|---|---|---|
| **Asset** | Anything of value | DNS server, research data, student records DB |
| **Threat** | A potential cause of harm | Ransomware operator, water leak |
| **Threat actor** | The agent behind a threat | Cybercrime group, negligent insider |
| **Vulnerability** | A weakness in an asset | Unpatched service, default password |
| **Exploit** | Technique/code that uses a vulnerability | Malicious document, scanner-driven attack |
| **Control** | Something that reduces risk | Firewall rule, MFA, backups |
| **Impact** | Harm if the threat succeeds | Records breach, week-long outage |

### 2.4 Threat actors: capability × intent × targeting
| Class | Capability | Targeting | Typical example |
|---|---|---|---|
| Opportunistic ("script kiddies") | Low; uses existing tools | Anyone reachable (volume) | Mass router scanning |
| Organized cybercrime | High; monetized | Whoever pays or is profitable | Ransomware, fraud |
| Hacktivists | Medium | Ideological targets | Defacement, DDoS |
| Insiders | Varies — but *position* | Their own organization | Negligent admin; malicious leaver |
| State / near-state | Very high; patient | Specific, strategic | Long-duration espionage |

Modern attack **economics** matter: ransomware-as-a-service, phishing kits, and botnet rental mean low-skill actors achieve high impact. Defenders must assume *commodity* attacks succeed, not just sophisticated ones.

### 2.5 The four network vantage points
Where an attacker *stands* determines what they can do:

```
        (off-path: remote, volume attacks — floods, scans)
                        |
  [on-link] ---- [target network] ---- [infrastructure]
  same segment      the victim         compromised router/
  (sniffing, ARP)   itself             DHCP/DNS (sees all)
                        |
                 (on-path: traffic
                  transits attacker)
```

1. **On-link** — same broadcast domain: sees local traffic, can poison ARP/CAM.
2. **On-path (MITM)** — traffic flows through them: read/modify anything unencrypted.
3. **Off-path** — remote, no position: floods, scans, protocol abuse against services.
4. **Infrastructure** — controls the plumbing (router, DNS, DHCP): sees and steers *everything*.

Most Module-2 attacks are classified by which vantage point they require — keep this map.

## 3. Key Definitions (memorize these)

- **CIA triad** — confidentiality, integrity, availability; the impact vocabulary.
- **Risk** — likelihood × impact of a threat exploiting a vulnerability.
- **Vulnerability vs exploit** — the weakness vs the thing that uses it.
- **Control** — any administrative/technical/physical measure that reduces risk.
- **Residual risk** — the risk left after controls; must be *named*, not ignored.
- **Attack surface** — the set of points where an unauthorized actor could interact.
- **Vantage point** — the network position an attacker needs for a given attack.

## 4. Network Diagram: where security lives on a simple network

```
 Internet
    |
[Edge firewall]------ DMZ: web proxy, mail gateway
    |
[Core router]------ SERVER ZONE: DNS, DHCP, file, DB
    |
[Access switch]---- CORP ZONE: workstations, printers
    |            \-- GUEST ZONE: visitor Wi-Fi (isolated)
    +------------- MGMT ZONE: switch/router admin (out-of-band)
```

Ask for every zone: *who can reach it, what would its compromise expose, which CIA
leg fails first?* That question chain is the whole course in miniature.

## 5. Protocol Examples (orientation level)

- **HTTP login page (no TLS):** confidentiality fails — anyone on-path reads the password.
- **Ping flood (ICMP echo):** availability attack at its simplest.
- **Modified download over HTTP:** integrity failure — the file is not what the server sent (Module 4 fixes this cryptographically).

## 6. Configuration Concepts (preview only)

You will *configure* controls starting Week 5. Today, know the three questions every
configuration answers: **what traffic (5-tuple), what action (allow/deny/log), what
evidence (logging)**. Module 3 turns these into firewall and ACL reality.

## 7. Security Implications

- Every protocol you meet in L02–L04 has trust assumptions; every attack in Module 2 abuses one of them.
- "Secure" is always relative to a threat model — say *against whom* and *for what*.
- The insider with legitimate access is often the highest-impact actor class on a campus.

## 8. Realistic Organizational Scenario

**The architecture firm (running case for Module 1).** A 25-person firm runs one flat
network: workstations, a NAS with client blueprints, IP cameras, guest Wi-Fi on the
same switch, and a fax-capable printer. Their insurer's renewal questionnaire asks:
what are your assets, what are your top risks, what controls exist?

- **Assets:** NAS (client blueprints — confidentiality, high), printer/fax (integrity of inbound faxes), cameras (availability + privacy), workstations (everything).
- **Top exposures:** guest and corporate traffic on the same switch (on-link sniffing), no backups verified, flat network (any compromise reaches everything), printer reachable from guest Wi-Fi.
- **$0-budget first fixes:** separate guest onto its own VLAN/SSID, verify+automate NAS backups, change default printer credentials.

You will formalize this as **case cs-001** and reuse the firm in later modules.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "We bought a firewall, so we're secure" | A control *class*, not a state. Unpatched hosts behind a firewall are still unpatched. |
| "Insiders aren't attackers" | Negligent insiders cause more incidents than malicious ones; both are threat actors. |
| "Security is IT's job" | Risk owners are the business; IT implements controls. |
| "Open-source crypto/tools are less secure" | Algorithm secrecy is not a security strategy (Kerckhoffs's principle — Module 4). |
| "100% security is achievable" | Defense is risk reduction + detection + response, priced against your threat model. |

## 10. Classroom Activities

1. **Headline sorting (in lecture):** five recent public incidents → classify actor class + primary CIA leg.
2. **Trust-zone inventory (teams of 3):** inventory the department network on the topology poster; pick the single most damaging compromise; 60-second pitches.
3. **Risk sentence drill:** write three risk statements in the form "If ⟨threat⟩ exploits ⟨vulnerability⟩ on ⟨asset⟩, ⟨impact⟩" — then rank them.

## 11. Problem-Solving Questions

1. A university publishes open guest Wi-Fi with a captive portal. Which CIA leg is weakest, and *for whom* (guest vs university)?
2. Why might a defender deliberately delay patching? What risk does that create and how would you document it?
3. Rank for campus risk: external ransomware operator vs negligent PhD student with admin rights. Defend your ordering with the vocabulary above.
4. Deconstruct: "We bought a next-gen firewall, so we are secure." Use at least four terms from §3.
5. Which vantage point does each require: ARP spoofing, internet-side scan, DNS poisoning by the ISP, Wi-Fi sniffing in a café?

## 12. Exit Ticket

*(Submitted at end of lecture; answers in instructor answer keys — Module 1.)*

1. Define "vulnerability" in one sentence and give a network example.
2. Name the CIA leg most affected by a SYN flood, with a one-line justification.
3. Which actor class fits a mass scanning campaign of home routers? Why?
4. State one course authorization rule and the reason it exists.
5. Threat vs risk — one sentence each.

## 13. References

- NIST Cybersecurity Framework 2.0 — functions vocabulary (Govern/Identify/Protect/Detect/Respond/Recover).
- NIST SP 800-12 Rev. 1 — glossary definitions (threat, vulnerability, risk).
- Verizon DBIR (current edition) — actor-class statistics used in the headline exercise.
- MITRE ATT&CK — https://attack.mitre.org (browse the tactics list).
- Stallings, *Cryptography and Network Security* — ch. 1 (any recent edition).
- Your institution's IT acceptable-use policy.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-1 | §2 risk/CIA/actor/vantage vocabulary; §11 protocol reasoning | Quiz 1 (W2), Midterm |
