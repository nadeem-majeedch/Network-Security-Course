---
marp: true
theme: default
paginate: true
lecture: L02
week: 1
clos: [CLO-1]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Protocol Deep Dive I — Ethernet, ARP, IP, ICMP

**Network Security · Lecture 2 · Week 1**

*Attacks exploit protocol mechanics. Today: the mechanics.*

<!-- notes: OPEN (2 min). Hook: "Every Layer-2 attack this course
teaches is possible because of a 1982 design decision you'll meet in 20
minutes." -->

---

## Learning Objectives

By the end you can:

1. **Dissect** an Ethernet frame and identify each field's security role
2. **Trace** ARP resolution — and explain why it's trustable by design
   (and why that's a problem)
3. **Read** an IPv4 header, naming TTL's security function
4. **Classify** ICMP types by their diagnostic and abuse potential
5. **Predict** which fields an attacker can spoof freely

<!-- notes: (1 min) Objective 5 is the spoiler for module 2 — say so. -->

---

## Encapsulation in One Slide

```
 DATA → [TCP/UDP header] → [IP header] → [Ethernet frame] → wire
         segment              packet         frame
```

- Each layer trusts the one below — attacks live in that trust
- Naming discipline: segment / packet / frame (Quiz 6 Q1)

<!-- notes: (3 min) Have students recite the order. Emphasize
"encapsulation = trust transfer" — the course's framing. -->

---

## Ethernet Frame Anatomy

| Field | Role | Security note |
|---|---|---|
| Dst MAC | Local-link addressing | Switch forwards on this |
| Src MAC | Claimed sender | **Spoofable freely** |
| EtherType | Payload protocol | 0x0806 = ARP |
| Payload | L3 packet | — |
| FCS | Integrity (physical) | Not a security control |

- Switches build MAC tables from **claimed** source addresses

<!-- notes: (6 min) Walk a real frame hexdump if the lab projector
allows. Key line: "FCS protects against electrical noise, not against
attackers." The claimed-source point seeds MAC flooding (L06). -->

---

## Switches vs Routers: Trust Boundaries

- **Switch** — forwards frames by MAC, *inside* a broadcast domain
- **Router** — forwards packets by IP, *terminates* broadcast domains
- Broadcast domain = the blast radius of broadcast-based attacks

<!-- notes: (4 min) Reference diagram 01: every line between zones is a
router or firewall. Quiz 6 Q8 tests exactly this picture. -->

---

## ARP: The Address Nobody Verifies

- IP says *"deliver to 10.0.5.1"* — the NIC needs a MAC
- `ARP Request` (broadcast): *"who has 10.0.5.1?"*
- `ARP Reply`: *"I do — MAC aa:bb:cc:00:11:22"*
- Caches the answer — **no authentication anywhere**

<!-- notes: (6 min) The one-liner to land: "ARP trusts whoever shouts
first." Draw the two-host exchange live. This is the setup slide for
diagram 03 — show the same exchange with a hostile third host next
lecture. -->

---

## ARP Cache: State & Poisoning Preview

- Cache entries age out — but *unsolicited replies update them too*
- Attacker's move: shout *"gateway is at my MAC"* → traffic detours
- Defense (L09 preview): DAI validates replies against bindings

<!-- notes: (4 min) Show diagram 03's sequence half — stop before the
full MITM. Quiz 1 Q8 reads exactly this evidence. -->

---

## IPv4 Header: The Security Fields

```
 0                   1                   2                   3
 ┌───────────────────┬───────────────────┬───────────────────┐
 │ Ver │ IHL │  TOS  │         Total Length              │
 │  Identification    │ Flags │     Fragment Offset      │
 │  TTL   │ Protocol  │        Header Checksum            │
 │                 Source Address                          │
 │               Destination Address                       │
 └─────────────────────────────────────────────────────────┘
```

- **TTL** — decremented per hop; kills routing loops
- **Source Address** — *claimed*, not proven (spoofable)
- **Fragment Offset** — reassembly games (cs-004's case!)

<!-- notes: (7 min) Draw the header by hand; students annotate. Three
security callouts: TTL (loop + traceroute abuse), source (every spoofing
attack), fragmentation (evasion history). Keep to 7 min — depth comes
in the lab. -->

---

## Fragmentation: Why It Matters

- Paths have MTUs; packets larger than MTU get split
- Reassembly happens at the destination — *off the wire*
- Overlapping/odd fragments = historical evasion + DoS vectors
- Modern lesson: **firewalls that don't reassemble can be bluffed**

<!-- notes: (4 min) cs-004 presents this as evidence analysis. Don't
teach evasion recipes — teach "why reassembly state matters." -->

---

## ICMP: Diagnostics & Abuse

| Type | Use | Abuse |
|---|---|---|
| Echo (0/8) | ping | Sweeps (recon), floods (DoS) |
| Time Exceeded (11) | traceroute | Topology mapping |
| Dest Unreachable (3) | errors | Recon oracle |
| Redirect (5) | route hint | **Route manipulation** |

- ICMP is *informational* — networks leak inventory through it

<!-- notes: (5 min) Traceroute demo story: each TTL-exceeded reveals a
hop — the attacker's map draws itself. cs-005 is the case here. Table
density is fine: it's a reference slide, read it row by row. -->

---

## Who Can Be Spoofed? (The Honest Ledger)

| Layer | Field | Spoofable? |
|---|---|---|
| L2 | Source MAC | Yes — freely |
| L2.5 | ARP claims | Yes — no auth by design |
| L3 | Source IP | Yes — freely (ingress filtering mitigates) |
| L4 | Ports/seq | Ports yes; seq via PRNG strength |

- Identity on the wire = **claim**, until a control proves otherwise
- The course's controls (DAI, ACLs, crypto) turn claims into proofs

<!-- notes: (5 min) This slide is L02's thesis. Have students write it
down verbatim: "identity on the wire is a claim." Every defense module
answers it. -->

---

## CS/DS Example: The Lab's Own Subnet

- GPU cluster on 10.50.0.0/24; notebooks reach it via the same router
- ARP poison the cluster's gateway = intercept dataset traffic
- Same protocol facts, research-crown-jewel stakes

<!-- notes: (3 min) DS framing per course standard: the DS cluster is
not "just another subnet" — the data lake credentials live on those
nodes (cs-088's lesson, previewed). -->

---

## Activity: Packet Autopsy (5 min)

Given a frame: `Dst MAC: ff:ff:ff:ff:ff:ff · Src MAC: 00:11:22:33:44:55 ·
EtherType: 0x0806 · "Who has 10.0.5.1? Tell 10.0.5.66"`

1. Which host(s) process this? 2. What does 10.0.5.66 gain? 3. One risk?

<!-- notes: (5 min) Answers: broadcast = everyone; 10.0.5.66 learns the
gateway's MAC mapping (that's normal); the risk slide: it also *claims*
an IP — a rogue-DHCP/ARP setup move. Debrief fast, 1 min. -->

---

## Case Study: cs-003 (5 min)

- Abnormal ARP replies in a "clean" capture — spot the tell
- Reason first; reveal follows the protocol

<!-- notes: (5 min) The tell: reply volume from an MAC that never sent
requests. Classroom protocol per case-index. -->

---

## Formative Check

- Name the field that kills routing loops; name the ARP design flaw
- Both appear in Quiz 1

<!-- notes: (2 min) Exit-ticket style, oral. -->

---

## References & Next

- RFC 826 (ARP), IEEE 802.3 (Ethernet framing)
- Diagrams: `diagrams/03-arp-poisoning-flow.md`
- **Next (L03):** TCP, UDP, DNS, DHCP — where sessions begin
