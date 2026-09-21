# L08 — DoS/DDoS & Infrastructure Abuse

> **Scope and safety note:** flood mechanics are taught for classification and
> mitigation design. Flood generation is performed only by the instructor inside the
> isolated lab range; generating attack traffic against systems you are not
> authorized to test is illegal.

## 1. Learning Objectives

By the end of this session you can: (1) classify DoS/DDoS by layer (volumetric / protocol / application); (2) explain reflection-amplification mechanics and compute amplification factors; (3) explain SYN-flood mechanics and SYN-cookie mitigation; (4) characterize botnet C2 models and their network signatures; (5) sequence mitigations by placement (upstream → edge → application) with justification.

## 2. Key Definitions

| Term | Definition |
|---|---|
| DoS / DDoS | Denial of service from one / many (distributed) sources |
| Volumetric attack | Bandwidth saturation (Gbps) |
| Protocol attack | State/table exhaustion (SYN flood class) |
| Application (L7) attack | Legitimate-looking requests exhausting expensive work |
| Amplification factor | Response bytes ÷ request bytes for a reflector service |
| Reflection | Spoofed-source requests so replies go to the victim |
| SYN cookies | Stateless encoding of connection state into the ISN — survive backlog exhaustion |
| BCP 38 | Ingress/egress source filtering — networks drop packets with spoofed sources |
| DGA | Domain Generation Algorithm — malware generates domains algorithmically |
| Sinkholing | Redirecting malicious domains to a defender-controlled host |

## 3. Detailed Explanations

### 3.1 The flood taxonomy — classify, then mitigate
- **Volumetric (L3/4):** saturate bandwidth — UDP/ICMP floods, amplification. Signature: traffic *volume*, sources spread wide.
- **Protocol (L4):** exhaust state — SYN floods fill the server's half-open backlog; ACK floods burn CPU. Signature: many SYNs, few completions, *low* bandwidth.
- **Application (L7):** look legitimate — HTTP GET floods, slowloris (hold connections open), expensive-search abuse. Signature: per-request rates, not bandwidth.
Why classification first: a 400 Gbps volumetric attack is an *upstream* problem (your server never sees it stop); a slowloris is an *application* problem (no amount of upstream scrubbing sees it).

### 3.2 Reflection & amplification: weaponizing open resolvers
Attacker sends a small spoofed-source request to thousands of third-party servers; the (larger) replies converge on the victim. Amplification factor = response/request bytes: DNS ≈ 28–54×, NTP `monlist` (historic) ≈ 200×+, memcached ≈ up to 10,000×. The enabling flaw is **spoofable UDP sources** — so the structural fix is network operators enforcing **BCP 38** source filtering at their edges. Your network's duty: never *originate* spoofed packets (L12 lab), and monitor *egress* floods (they mean compromised insiders — free detection).

### 3.3 SYN floods and SYN cookies
Each half-open connection consumes backlog memory; thousands of SYNs with no ACKs exhaust it and legitimate clients get dropped. Mitigations: backlog tuning (partial), **SYN cookies** (encode connection state into the sequence number — no memory until the ACK returns; costs some TCP options), upstream filtering, and RST-rate triggers. Placement matters: cookies buy time at the edge; scrubbing handles volume; neither helps a slowloris.

### 3.4 Botnets and C2 models
- **Centralized C2** (HTTP/IRC-era): single point of discovery → takedown is possible, signatures are clear (periodic beacons — L05/L28).
- **P2P:** no central point; resilient; harder to sinkhole; detection shifts to peer-exchange patterns.
- **DGA:** domains generated algorithmically; block-lists can't keep up → detection via NXDOMAIN ratios and name entropy (L23).
- **DDoS-for-hire:** attacks are cheap and frequent — defender math is capacity + runbooks, not motive analysis.

### 3.5 Mitigation architecture — order of operations
1. **Upstream:** ISP scrubbing / CDN-anycast absorption — buy capacity where it's cheap.
2. **Edge:** coarse ACLs and rate-limits — drop known-bad sources/protocols before they traverse your WAN.
3. **Application:** connection limits, request shaping, queues, graceful degradation ("load shedding").
Plus DNS-side resilience (anycast, registrar lock) and *egress* monitoring (L21) to catch your own hosts participating in someone else's attack.

## 4. Network Diagram: amplification + mitigation layers

```
 Attacker ──spoofed-src requests──► 50k open resolvers
                                          |  (28-54x replies)
                                          ▼
 Victim ◄═══════════ reply flood ═════════╝

 Mitigation stack:  [ISP scrubbing]  ── drops volumetric before your WAN
                    [Edge ACL/RL]    ── coarse, cheap, first policy point
                    [App tier]       ── per-request shaping, graceful degradation
```

## 5. Protocol Examples

- Flow shape of a SYN flood: thousands of flows, SYN-only, to one `dst:port`, bytes tiny — protocol class diagnosed from *shape*, not volume.
- Amplification shape: inbound UDP/53 (or /123, /11211) from thousands of sources; request absent (spoofed) — your edge only sees the replies.

## 6. Configuration Concepts (concept level)

- Edge rate-limiting classes (police/CAR): protocol-scoped limits with explicit exceed actions.
- TCP backlog/SYN-cookie activation triggers (OS/edge policy), connection limits per source.
- DNS anycast + registrar lock; RRL (response rate limiting) on authoritative servers you operate.

## 7. Security Implications

- Availability attacks exploit **state** and **bandwidth asymmetries**; classification drives mitigation choice.
- Amplification is a *source-network* hygiene failure (BCP 38) more than a victim misconfiguration.
- Egress floods = your compromised hosts — detection upside inside an availability incident.

## 8. Realistic Organizational Scenario

**Enrollment week (running case).** The registration service goes unresponsive: ~50k half-open connections to 443, steady SYN rate from thousands of sources, bandwidth *low*. Students classify (protocol flood — not volumetric), explain the backlog exhaustion, and order mitigations (edge SYN cookies/filtering first; *not* "add app servers"). The discriminating monitoring rule: SYN-completion ratio collapse vs the slow rise of a flash crowd. Full decision chain: **case cs-021**.

## 9. Common Misconceptions

| Misconception | Reality |
|---|---|
| "More bandwidth stops DDoS" | Buys seconds; volumetric attacks scale beyond budgets — absorb upstream. |
| "SYN cookies are a firewall product" | They are a TCP-stack technique available on hosts and edge devices. |
| "A flash crowd and an attack look the same" | Different shapes: completion ratios, source diversity, request patterns. |
| "Reflection attacks are the victim's fault" | The victim is a bystander; the *source networks* enabling spoofing are the fix point. |
| "Blocking the attacker's IP solves it" | Distributed sources + spoofing make single-IP blocks cosmetic. |

## 10. Classroom Activities

1. **Telemetry triage (teams of 3):** flood telemetry pack → classify attack, characterize sources (spoofed vs real via TTL reasoning), top mitigation with placement, monitoring rule that fires 10 minutes earlier.
2. **Amplification math:** compute factors for DNS/NTP/memcached from given request/response sizes; rank abuse potential.
3. **Order-of-operations drill:** five incident cards — sequence the mitigation stack aloud.

## 11. Problem-Solving Questions

1. Why does buying bandwidth fail, and when is CDN/anycast absorption the right buy?
2. BCP 38 requires source networks to filter egress — why is global deployment slow, and what changes it?
3. SYN cookies encode state in the ISN: which TCP options are lost, and what breaks?
4. You see a huge inbound NTP flood — give your first three response actions and who you call first.
5. Egress volumetric spikes from your own campus: what does that indicate, and which control catches it?

## 12. Exit Ticket

1. Classify: "10 Gbps of UDP/123 responses to one IP" — layer, type, enabling flaw.
2. What makes amplification possible with UDP but not (normally) TCP?
3. Which two counters distinguish a SYN flood from a flash crowd?
4. Why are DGA domains harder to block-list than static C2 domains?
5. Order: edge rate-limit, upstream scrubbing, app-tier load shedding — justify for a volumetric attack.

*(Answers: `the instructor answer-key collection (not published)`.)*

## 13. References

- RFC 4987 — TCP SYN flooding attacks and mitigations.
- BCP 38 / RFC 2827 — ingress filtering; RFC 3704 — uRPF.
- US-CERT/CISA alerts — DNS/NTP/memcached amplification (factors and guidance).
- MITRE ATT&CK — T1498 Network Denial of Service (sub-techniques).
- Kurose & Ross — congestion control context.

## 14. CLO Mapping

| CLO | Covered here | Assessed via |
|---|---|---|
| CLO-2 | §3 classification + mitigation placement | Quiz 2 (today), Lab-04, Case set A |
