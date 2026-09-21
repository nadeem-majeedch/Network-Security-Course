---
marp: true
theme: default
paginate: true
lecture: L08
week: 4
clos: [CLO-2]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# DoS/DDoS & Infrastructure Abuse

**Network Security · Lecture 8 · Week 4**

*Availability is a security property — attack it like one.*

<!-- notes: OPEN (2 min). Hook: "Everything so far stole. Today: what
destroys — and why the internet's own helpers do the damage." -->

---

## Learning Objectives

1. **Classify** DoS vectors: volumetric, protocol-state, application
2. **Explain** reflection/amplification mathematics (the multiplier)
3. **Diagnose** a SYN flood from flow telemetry
4. **Design** layered rate-limiting that protects without strangling
5. **Evaluate** sinkhole/egress decisions during an active flood

<!-- notes: (1 min) Objective 3's diagnosis maps to cs-006/cs-021;
objective 5 to cs-025's judgment case. -->

---

## Three Vectors, One Goal

| Vector | Exhausts | Example |
|---|---|---|
| Volumetric | bandwidth | UDP floods, amplification |
| Protocol-state | connection tables | SYN flood, SLOWLORIS-class |
| Application | expensive operations | search/API abuse |

- Diagnosis first: *what resource is dying?* — then mitigation

<!-- notes: (5 min) The diagnosis-first rule prevents the classic
mistake: rate-limiting an app flood as if it were volumetric. Quiz 2's
Section C + cs-021 both drill it. -->

---

## SYN Flood: State as a Resource

- Unanswered SYNs → half-open backlog → memory/table exhaustion
- New legit connections refused while the table fills
- Server fix: SYN cookies (stateless handshake)
- Network fix: upstream filtering, rate-limiting, CDN absorption

![bg right:36% fit](diagrams/02-tcp-handshake-teardown.md)

<!-- notes: (6 min) Diagram 02's handshake side annotated: the server
holds state between SYN and ACK. "State = resource; flood = exhaustion"
is the module's unifying sentence. Quiz 2 Q7 asks exactly this. -->

---

## Reflection & Amplification: The Multiplier

- Attacker → service (spoofed source = victim) → service replies *to
  victim*
- Amplification = reply bytes ÷ request bytes (DNS, NTP, memcached
  historic)
- The botnet pays 1× bandwidth; the victim receives 50–5000×

<!-- notes: (7 min) Do the arithmetic live: 60-byte query, 4,000-byte
answer, 1 Gbps of attacker = 65+ Gbps at the victim. Quiz 2 Q4 tests
the mechanism; QB-007's rationale is here. -->

---

## Botnets: The Rented Army

- Compromised devices (servers, IoT, routers) commanded as one
- C2 channels: the *defense* target (cut C2 = cut coordination)
- Module 2 → module 6 continuity: beaconing detection (L23)

<!-- notes: (4 min) Keep to concept: rented capacity, C2 dependency.
The defense link — beacon patterns — is L23's Zeek lecture. cs-023's
case reads the beacon. -->

---

## Diagnosis from Flow Telemetry

- SYN flood: SYNs↑, no SYN-ACKs, many sources
- Amplification: inbound >> outbound, UDP, fixed service ports
- App flood: small packets, expensive URLs, few sources (sometimes one)

<!-- notes: (5 min) The three signatures side by side. cs-006's case
uses the first; the midterm's C-section loves this table. -->

---

## Mitigation Layer Cake

| Layer | Control |
|---|---|
| Upstream/ISP | scrubbing, blackhole/sinkhole |
| Edge (CDN/anti-DDoS) | absorb + filter |
| Firewall | rate-limit per class |
| Host | SYN cookies, backlog tuning |
| App | cache, queue, degrade gracefully |

- No single layer survives alone — layer cake = defense in depth for
  availability

<!-- notes: (5 min) The cake mirrors L09's philosophy before L09
teaches it. Quiz 2 Q7's two mitigation locations (host + network) come
from this table. -->

---

## Rate-Limit Design Judgment

- Rate-limit the *behavior*, not the user: legit bursts exist
- Per-class limits: new-conn/s, queries/s, bytes/s
- The strangling failure: limits tighter than legitimate demand =
  self-inflicted DoS

<!-- notes: (5 min) cs-024's design case. The failure mode is as
important as the control — operational realism per course standard. -->

---

## Sinkhole & Egress: Judgment Calls

- **Sinkhole** (your side): absorb attacker traffic to a controlled
  address — protects the service
- **Egress blocking** (your side): stop *your* devices joining botnets
- Both have collateral questions: legit traffic shape, abuse-desk
  duties

<!-- notes: (5 min) cs-025's tradeoff case. The sinkhole-vs-blackhole
distinction: sinkhole = controlled destination (can study), blackhole =
drop everything to a prefix (blunt). -->

---

## CS/DS Example: The GPU Cluster as Flood Target

- Training runs = expensive API endpoints; autoscaling = budget risk
- App-layer flood on a costly endpoint → cloud bill as collateral
- Rate-limit by token + queue by priority (course vocabulary)

<!-- notes: (3 min) DS framing: cloud-budget DoS is the modern variant
—flooding someone's *autoscaler*. Cost-aware rate-limiting is the
defense. -->

---

## Activity: Flood Triage (6 min)

Flow data given: 2 Gbps inbound UDP/123, 3 min duration, 40k sources.
Classify, name the service, pick the first two mitigation layers.

<!-- notes: (6 min) Answer: NTP amplification (UDP/123), volumetric;
first layers: upstream scrubbing + edge. The "why not host first?"
argument: bandwidth dies before it reaches hosts. -->

---

## Case Study: cs-022 (5 min)

- Reflection/amplification response plan — who calls whom, in order

<!-- notes: (5 min) The case rehearses the escalation: provider, CDN,
abuse desks. Order matters — bandwidth is dying while you argue. -->

---

## Formative Check

- Oral: classify — DNS query flood, 900 GB/s UDP, 5 req/s expensive
  search. Which vector is each?

<!-- notes: (2 min) Rapid exit: protocol-state (DNS state abuse),
volumetric, application. -->

---

## References & Next

- US-CERT guidance on amplification attacks (reference class)
- Diagrams: `diagrams/02-tcp-handshake-teardown.md`
- **Next (L09):** defense in depth — the counter-architecture begins
