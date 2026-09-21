---
artifact-type: question-bank
status: complete
questions: 50
instructor-key: instructor/answer-keys/question-bank-answer-key.md
---

# Question Bank — Network Security (Student Version)

> Questions only. Validated answers, distractor rationales, and marking
> guidance live in the instructor answer key. Every question carries its
> Bloom level and CLO in the key; CLO/module/difficulty maps are in
> `docs-meta/assessment-coverage.md`.


## Module 1 Questions

**QB-001** (1 mark)

Which OSI layer do TCP ports belong to?

- **A.** Layer 2
- **B.** Layer 3
- **C.** Layer 4
- **D.** Layer 7

**QB-002** (1 mark)

A host receives an ARP reply for an IP it never queried. This is:

- **A.** Normal ARP behavior
- **B.** A gratuitous/unsolicited reply — possible poisoning
- **C.** A DNS error
- **D.** A DHCP lease renewal

**QB-003** (2 marks)

A packet has TTL=1 arriving at a router one hop from the destination. What happens?

- **A.** Delivered
- **B.** Dropped, ICMP time exceeded sent
- **C.** Fragmented
- **D.** Looped

**QB-004** (2 marks)

Why does ARP only resolve addresses on the local subnet?

- **A.** Routers translate ARP
- **B.** Broadcasts do not cross routers
- **C.** ARP requires DNS
- **D.** ARP uses multicast only

**QB-005** (2 marks)

A TCP connection shows SYN, SYN-ACK, then RST. Most consistent interpretation?

- **A.** Normal close
- **B.** Port open but application reset
- **C.** SYN-flood defense triggered on the server
- **D.** DNS failure


## Module 2 Questions

**QB-006** (1 mark)

Which attack poisons a switch's MAC address table?

- **A.** ARP spoofing
- **B.** MAC flooding
- **C.** DHCP starvation
- **D.** VLAN hopping

**QB-007** (1 mark)

The 'amplification' in a reflection DDoS refers to:

- **A.** Multiple bots
- **B.** Response size exceeding request size
- **C.** Packet count
- **D.** DNS TTL values

**QB-008** (2 marks)

An attacker on a switched LAN wants traffic between host A and the gateway. Best first move?

- **A.** MAC flood the switch
- **B.** ARP-poison A and the gateway
- **C.** DHCP starvation
- **D.** STP root claim

**QB-009** (2 marks)

Which control set best breaks a DHCP-rogue-server attack end to end?

- **A.** Port security alone
- **B.** DHCP snooping + option-82 filtering on untrusted ports
- **C.** MAC flooding defense
- **D.** BPDU guard

**QB-010** (2 marks)

A DNS-spoofing campaign survives resolver restarts. Why?

- **A.** Cache persistence on clients
- **B.** Long TTL values set on forged records
- **C.** Encrypted transport
- **D.** Zone transfer abuse


## Module 3 Questions

**QB-011** (1 mark)

An implicit deny at the end of an ACL means:

- **A.** All traffic is logged
- **B.** Unmatched traffic is dropped
- **C.** The ACL is invalid
- **D.** Only TCP is filtered

**QB-012** (1 mark)

The DMZ's defining property:

- **A.** Fastest routing
- **B.** A buffer zone exposing only required services to untrusted networks
- **C.** Wireless coverage
- **D.** NAT translation point

**QB-013** (2 marks)

Egress filtering on the internal firewall primarily limits:

- **A.** Inbound scans
- **B.** Compromised hosts calling out / exfiltrating
- **C.** Broadcast storms
- **D.** VPN throughput

**QB-014** (2 marks)

Zero trust differs from classic NAC chiefly in:

- **A.** Cost
- **B.** Continuous per-request authorization vs one-time admission
- **C.** Wireless support
- **D.** Certificate length

**QB-015** (2 marks)

A microsegmentation rollout shows east-west traffic dropping 40% after enforcement. Interpretation?

- **A.** Attack stopped
- **B.** Shadow flows existed — previously unknown dependencies now blocked; tune or accept
- **C.** Routing failure
- **D.** Denial of service


## Module 4 Questions

**QB-016** (1 mark)

AES is:

- **A.** A hash function
- **B.** A symmetric block cipher
- **C.** An asymmetric cipher
- **D.** A key exchange

**QB-017** (2 marks)

Why combine a hash with a shared secret (HMAC) instead of using the hash alone?

- **A.** Faster
- **B.** A plain hash can be recomputed by anyone — the key adds origin authentication
- **C.** Shorter output
- **D.** Compression

**QB-018** (1 mark)

A certificate binds:

- **A.** An IP to a MAC
- **B.** An identity to a public key (signed by an issuer)
- **C.** A user to a password
- **D.** A port to a process

**QB-019** (2 marks)

A browser warns 'certificate expired' though the site works. The immediate risk class is:

- **A.** Confidentiality of the session
- **B.** Authentication/identity assurance (and click-through training)
- **C.** Routing integrity
- **D.** DNS poisoning

**QB-020** (2 marks)

Split-tunnel VPN on an unmanaged laptop primarily risks:

- **A.** Slower DNS
- **B.** The remote untrusted network bridging into the corporate path
- **C.** Certificate bloat
- **D.** MTU blackholes

**QB-021** (2 marks)

In IPsec site-to-site, 'PFS' (perfect forward secrecy) on rekeys protects:

- **A.** Against weak pre-shared keys only
- **B.** Past session keys if the long-term key later leaks
- **C.** Against replay
- **D.** Header integrity


## Module 5 Questions

**QB-022** (1 mark)

802.1X wireless authentication's three roles:

- **A.** Client, switch, firewall
- **B.** Supplicant, authenticator, authentication server
- **C.** User, AP, DHCP
- **D.** Client, CA, DNS

**QB-023** (2 marks)

Why does WPA3-Personal defeat offline dictionary attacks that work on WPA2-PSK captures?

- **A.** Longer keys
- **B.** SAE derives keys per handshake — no reusable offline-verifiable material
- **C.** Stronger radios
- **D.** Mandatory certificates

**QB-024** (2 marks)

Rogue-AP/evil-twin detection is the job of:

- **A.** Wired IDS
- **B.** Wireless IDS/monitoring (RF-side sensing)
- **C.** Firewall logs
- **D.** DHCP logs

**QB-025** (1 mark)

A cloud security group is:

- **A.** Stateless subnet filter
- **B.** Stateful instance-level allow-only filter
- **C.** A route policy
- **D.** An IAM role

**QB-026** (2 marks)

VPC flow logs show an instance with a 24-hour periodic 40 MB outbound transfer to a new external IP. First verification step?

- **A.** Block the IP
- **B.** Attribute: check instance agents/jobs against the destination and history
- **C.** Reboot the instance
- **D.** Open a firewall rule

**QB-027** (2 marks)

The strongest argument for a VPC egress allow-list over default allow-all:

- **A.** Cheaper
- **B.** Breaks C2/exfil patterns and forces flows onto logged, approved paths
- **C.** Faster routing
- **D.** Avoids NAT


## Module 6 Questions

**QB-028** (1 mark)

A signature-based IDS misses:

- **A.** Known exploits
- **B.** Novel/unknown attack patterns
- **C.** Encrypted headers
- **D.** All UDP

**QB-029** (2 marks)

A Zeek log shows one host querying 400 unique high-entropy subdomains in 10 minutes. Best hypothesis:

- **A.** Bulk mail
- **B.** DNS tunneling/exfiltration
- **C.** NTP drift
- **D.** ARP scanning

**QB-030** (2 marks)

The hidden cost of a 99%-false-positive alert class:

- **A.** Storage
- **B.** Analyst trust decay — future true positives get ignored
- **C.** License fees
- **D.** Slower CPUs

**QB-031** (1 mark)

Authenticated vulnerability scans outperform unauthenticated chiefly by:

- **A.** Speed
- **B.** Seeing installed-package truth — fewer false negatives
- **C.** Avoiding credentials
- **D.** Bypassing firewalls

**QB-032** (2 marks)

Two CVEs share CVSS 9.8. One sits on an internet-facing payment server; one on an isolated build host. Prioritize:

- **A.** Alphabetical
- **B.** Payment server first — reachability and asset criticality dominate
- **C.** Build host first — developers are busier
- **D.** Equal

**QB-033** (2 marks)

A TI feed lists an IP your domain controller just contacted. Before containment:

- **A.** Contain immediately
- **B.** Corroborate locally (flow/proxy/EDR context) and check indicator provenance/age
- **C.** Ignore the feed
- **D.** Reboot the DC


## Module 7 Questions

**QB-034** (1 mark)

NIST IR lifecycle phases:

- **A.** Prevention, patching, audit
- **B.** Preparation; detection & analysis; containment, eradication & recovery; post-incident
- **C.** Scan, patch, report
- **D.** Triage, fix, forget

**QB-035** (2 marks)

Mass file-renames fire on a file server at 02:00 (EDR, single source). The asymmetry argument says:

- **A.** Wait for a second alert
- **B.** Contain now — act-wrong costs a reboot, wait-wrong costs the share
- **C.** Email the CISO and wait
- **D.** Reimage immediately

**QB-036** (2 marks)

Why 'suspend, don't delete' a malicious scheduled task?

- **A.** Deletion is impossible
- **B.** The artifact is evidence; suspension neutralizes execution
- **C.** Suspicion is illegal
- **D.** Tasks auto-respawn

**QB-037** (2 marks)

In a forensic timeline, 'network-attributed, host-unattributed' means:

- **A.** The host admitted it
- **B.** Network telemetry shows the event; host telemetry for that window is absent
- **C.** The network is guilty
- **D.** Logs were deleted by policy

**QB-038** (2 marks)

Chain of custody is broken when:

- **A.** An image is hashed at acquisition and after transfer
- **B.** An image is copied to an analyst's personal USB without records
- **C.** Evidence is stored encrypted
- **D.** Two analysts observe a transfer

**QB-039** (2 marks)

A board report claims 'MTTD improved to 9 days.' The strongest supporting artifact:

- **A.** Vendor brochure
- **B.** Per-incident detection timestamps across the last N incidents with method notes
- **C.** A pie chart
- **D.** Alert counts


## Module 3 Questions

**QB-040** (3 marks)

DESIGN (ACL): Write an ordered 5-rule ACL permitting SSH to subnet 10.5.5.0/24 only from jump host 10.5.5.9, denying other SSH, permitting established returns, logging denies.


## Module 1 Questions

**QB-041** (3 marks)

PACKET ANALYSIS: A capture shows ARP reply '10.1.1.1 is-at 00:11:22:33:44:01' from MAC 00:11:22:33:44:99 (gateway's real MAC ends :01). Describe the attack, its effect on hosts, and two corroborating artifacts.


## Module 2 Questions

**QB-042** (3 marks)

DIAGRAM: A topology shows internet → edge FW → DMZ (web, 10.2.0.10) → inner FW → LAN (10.3.0.0/16). The DMZ host initiates outbound 443 to any destination. Identify the design flaw and redesign the rule.


## Module 6 Questions

**QB-043** (3 marks)

PACKET/FLOW ANALYSIS: Flow records show workstation 10.4.1.57 → external IP on 443 every 60s ±3s, 2 KB each, for 6 hours, outside business hours. Classify, give the detection logic, and the next investigative step.


## Module 7 Questions

**QB-044** (3 marks)

INCIDENT TASK: Ransomware staging suspected (EDR: new service + mass rename on FS01; staging egress 2 MB in proxy). Give the ordered containment with reversibility labels and the evidence-preservation rule.


## Module 8 Questions

**QB-045** (4 marks)

CAPSTONE SYNTHESIS: Your capstone estate has MTTD 9 days, EDR 100% of servers, ZT pilots on 2 apps. The board asks: 'why fund phase 3 now?' Compose the 3-sentence case: what it buys, what deferral costs, what evidence backs the trajectory.


## Module 4 Questions

**QB-046** (3 marks)

DIAGRAM/CONFIG: A certificate chain: root 'Corp-Root' (self-signed, in trust store) → intermediate 'Corp-Issuing' (valid 2024–2034) → leaf 'wiki.lab' (valid, SAN matches). A client still rejects it. Give the three most probable causes ranked.


## Module 5 Questions

**QB-047** (3 marks)

CLOUD DESIGN: Design the NACL + SG division for a 3-tier VPC (web/app/DB) such that a future SG mistake cannot expose the DB to the internet. State rules on both constructs.


## Module 7 Questions

**QB-048** (3 marks)

FORENSICS: Host logs (NTP-synced) show an export at 14:10:00. Router flow records show the matching flow at 14:13:30. The router clock is skewed. Derive the offset and state how you'd prove it.


## Module 2 Questions

**QB-049** (3 marks)

THREAT MODEL: For a university Wi-Fi with WPA2-PSK shared by 3,000 students, produce the top threat, the compounding factor, and the design fix with its tradeoff.


## Module 8 Questions

**QB-050** (4 marks)

CAPSTONE SYNTHESIS: In ≤200 words, connect one protocol fact (module 1), one control design (module 3 or 5), one detection (module 6), and one response decision (module 7) into a single coherent defense story for your capstone estate.


## CLO Map (for instructors — students may ignore)

| Question | Module | CLO | Difficulty |
|---|---|---|---|
| QB-001 | 1 | CLO-1 | beginner |
| QB-002 | 1 | CLO-1 | beginner |
| QB-003 | 1 | CLO-1 | beginner |
| QB-004 | 1 | CLO-1 | intermediate |
| QB-005 | 1 | CLO-1 | intermediate |
| QB-006 | 2 | CLO-2 | beginner |
| QB-007 | 2 | CLO-2 | beginner |
| QB-008 | 2 | CLO-2 | intermediate |
| QB-009 | 2 | CLO-2 | intermediate |
| QB-010 | 2 | CLO-2 | expert |
| QB-011 | 3 | CLO-3 | beginner |
| QB-012 | 3 | CLO-3 | beginner |
| QB-013 | 3 | CLO-3 | intermediate |
| QB-014 | 3 | CLO-4 | intermediate |
| QB-015 | 3 | CLO-4 | expert |
| QB-016 | 4 | CLO-5 | beginner |
| QB-017 | 4 | CLO-5 | intermediate |
| QB-018 | 4 | CLO-6 | beginner |
| QB-019 | 4 | CLO-6 | intermediate |
| QB-020 | 4 | CLO-7 | intermediate |
| QB-021 | 4 | CLO-7 | expert |
| QB-022 | 5 | CLO-8 | beginner |
| QB-023 | 5 | CLO-8 | intermediate |
| QB-024 | 5 | CLO-8 | intermediate |
| QB-025 | 5 | CLO-13 | beginner |
| QB-026 | 5 | CLO-13 | intermediate |
| QB-027 | 5 | CLO-13 | expert |
| QB-028 | 6 | CLO-9 | beginner |
| QB-029 | 6 | CLO-9 | intermediate |
| QB-030 | 6 | CLO-9 | intermediate |
| QB-031 | 6 | CLO-10 | beginner |
| QB-032 | 6 | CLO-10 | intermediate |
| QB-033 | 6 | CLO-12 | expert |
| QB-034 | 7 | CLO-11 | beginner |
| QB-035 | 7 | CLO-11 | intermediate |
| QB-036 | 7 | CLO-11 | intermediate |
| QB-037 | 7 | CLO-14 | intermediate |
| QB-038 | 7 | CLO-14 | expert |
| QB-039 | 7 | CLO-15 | expert |
| QB-040 | 3 | CLO-3 | intermediate |
| QB-041 | 1 | CLO-1 | intermediate |
| QB-042 | 2 | CLO-2 | advanced |
| QB-043 | 6 | CLO-9 | advanced |
| QB-044 | 7 | CLO-11 | advanced |
| QB-045 | 8 | CLO-15 | expert |
| QB-046 | 4 | CLO-6 | advanced |
| QB-047 | 5 | CLO-13 | advanced |
| QB-048 | 7 | CLO-14 | advanced |
| QB-049 | 2 | CLO-2 | advanced |
| QB-050 | 8 | CLO-15 | expert |
