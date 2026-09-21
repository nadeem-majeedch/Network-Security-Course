---
marp: true
theme: default
paginate: true
lecture: L03
week: 2
clos: [CLO-1]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Protocol Deep Dive II — TCP, UDP, DNS, DHCP

**Network Security · Lecture 3 · Week 2**

*Sessions, names, and addresses — the three things attackers hijack
first.*

<!-- notes: OPEN (2 min). Hook: "Before an attacker steals anything, they
borrow an identity: a session, a name, or an address." -->

---

## Learning Objectives

1. **Narrate** the TCP handshake, data transfer, and teardown — and read
   them in captures
2. **Contrast** TCP's reliability guarantees with UDP's speed bargain
3. **Walk** a DNS resolution end-to-end, flagging every trust assumption
4. **Explain** DHCP's lease dance and the rogue-server failure mode
5. **Predict** the attack surface each protocol's design implies

<!-- notes: (1 min) Objective 1 maps to diagram 02; objectives 3–4 map
to Quiz 1 and the L2-attack labs. -->

---

## TCP: The Handshake

- `SYN → SYN-ACK → ACK` — ISNs exchanged, windows opened
- State created on **both** ends before any data
- Half-open connections = server memory held for *unanswered* SYNs

![bg right:38% fit](diagrams/02-tcp-handshake-teardown.md)

<!-- notes: (6 min) Trace diagram 02 left-to-right. The half-open point
is the seed of the SYN-flood lesson (L08): state is a resource; floods
exhaust resources. Quiz 1 Q2 is this slide. -->

---

## TCP: Sequence, ACK, Window

- Every byte numbered; ACKs carry *next-expected*
- Window = receiver's buffer headroom (**flow control**)
- Out-of-order → retransmit; duplicates → discard
- Security lens: seq numbers = session identity (hijack history lives
  here)

<!-- notes: (5 min) Keep it behavioral, not mathematical. "Seq = the
session's bloodstream" — hijacking means injecting with the right seq.
cs-019's case reads exactly this evidence. -->

---

## TCP: FIN vs RST

- FIN exchange: cooperative, 4-way, both sides finish
- RST: abort **now** — no socket, hostile reset, or teardown-on-failure
- Scanner's oracle: SYN→RST/ACK = "closed but alive"

<!-- notes: (4 min) Quiz 1 Q7 asks exactly this. Live-demo story:
telnet to a dead port, watch the RST arrive instantly. -->

---

## UDP: The Speed Bargain

- No handshake, no delivery guarantee, no congestion promise
- Header = 8 bytes; perfect for one-shot queries (DNS, DHCP, VoIP)
- Security lens: **statelessness** — spoofing is trivially cheap
- Amplification lives here (L08's reflection attacks)

<!-- notes: (4 min) Contrast slide against TCP's state. "UDP doesn't
remember you" = spoofable + reflexive. Don't demonize UDP: DNS/DHCP are
the course's own cases. -->

---

## DNS: Names to Addresses

- Resolver → root → TLD → authoritative chain, with caching at each hop
- Records: A, AAAA, MX, NS, CNAME, TXT
- UDP/53 for queries; TCP/53 for large answers & zone transfers
- **Trust assumption:** the resolver believes *whoever answers first*

<!-- notes: (7 min) Walk the chain on the board; every arrow is a trust
assumption. "First answer wins" is the poisoning setup (L07). CS/DS
tie-in: notebook jobs resolving package mirrors — a poisoned mirror is
a supply-chain event. -->

---

## DNS Caching & TTL

- Caches make DNS fast — and *sticky*
- Forged record + long TTL = poisoning that survives restarts
- Mitigations preview: randomized ports/IDs, DNSSEC, DoH/DoT (L14+)

<!-- notes: (4 min) cs-020's case is a campaign built on this. The
"survives resolver restarts" detail is bank question QB-010. -->

---

## DHCP: The Lease Dance

`DISCOVER` (broadcast) → `OFFER` → `REQUEST` → `ACK` — then lease time

- Client trusts **any OFFER** that arrives
- Server offers: address, gateway, **DNS server** — your whole network
  identity
- Rogue server = redirect everything (gateway + DNS) in one OFFER

<!-- notes: (6 min) Emphasize: DHCP configures trust *parameters*, not
just an address. Quiz 7 Q2's snooping answer previews L09. cs-008 is
the case. -->

---

## DHCP Starvation vs Rogue Server

| Attack | Mechanism | Effect |
|---|---|---|
| Starvation | request every lease | pool exhausts → legit clients fail |
| Rogue server | answer first with evil options | clients *work* — through the attacker |

- Starvation = availability attack; rogue = interception attack
- Defense seeds: snooping trust, rate-limiting, port security

<!-- notes: (4 min) The distinction matters — students conflate them.
"Rogue server victims don't notice" is the scary truth. -->

---

## Protocol Cheat Sheet (Reference Slide)

| Protocol | Port | Transport | Security Achilles heel |
|---|---|---|---|
| DNS | 53 | UDP/TCP | first-answer trust |
| DHCP | 67/68 | UDP | any-OFFER trust |
| HTTP | 80 | TCP | cleartext |
| HTTPS | 443 | TCP | config quality (L14) |

<!-- notes: (2 min) Reference slide — tell students it's the Quiz-6
one-pager. Move on quickly. -->

---

## CS/DS Example: Cluster Name Resolution

- GPU nodes resolve `dataset-lake.internal` every job run
- A poisoned answer = datasets fetched from attacker storage
- Same DNS facts; supply-chain stakes (module 2 revisits)

<!-- notes: (3 min) One slide, one point: research infrastructure runs
on the same protocols — the crown jewels move the stakes, not the
mechanics. -->

---

## Activity: Capture Reading (6 min)

From the seeded capture: identify the DHCP lease exchange, one DNS
query/response pair, and one full TCP handshake. Label trust moments on
each.

<!-- notes: (6 min) Lab-02's dataset; students annotate on the projector
copy. Answers are in the lab key. Pairs, 4 min work + 2 debrief. -->

---

## Case Study: cs-006 (5 min)

- Half-open flood symptoms in flow data — diagnose before mitigating

<!-- notes: (5 min) The tell: many distinct sources, SYNs without
handshake completion, backlog climbing. cs-006 reasoning per protocol. -->

---

## Formative Check

- Oral: why does UDP make amplification cheap? Why does DHCP OFFER
  trust matter?

<!-- notes: (2 min) Exit ticket oral — both appear in Quiz 2/7. -->

---

## References & Next

- RFC 9293 (TCP), RFC 1035 (DNS), RFC 2131 (DHCP)
- Diagrams: `diagrams/02-tcp-handshake-teardown.md`
- **Next (L04):** applied packet analysis — HTTP/HTTPS on the wire
