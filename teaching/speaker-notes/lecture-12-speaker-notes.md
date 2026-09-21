---
lecture: L12
module: 3
week: 5
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L12 Speaker Notes — NAT, Proxies, Egress & NAC

## Delivery Guide
Week 5's second lecture (with L09). "NAT is not security" is the thesis to prove,
not assert: show the port-forward recreating exposure in one line. The egress pair
(proxy + firewall) demo is the technical heart — the bypass test makes the pair
*visible*. The 802.1X section sets up L18: roles, attributes, and the critical-auth
fallback design question. Quiz 3 runs at the end of this session (10 min, per
calendar).

## Timing Plan
0–10 recap (rulebases → "denies matter only if egress can't bypass") · 10–35 NAT
variants + truth · 35–55 proxies + egress pair (live bypass test) · 55–65 break ·
65–90 802.1X/NAC · 90–110 egress + BCP 38 lab · 110–120 exit ticket + **Quiz 3**. 
**Compression:** NAT variants to a table; the bypass demo and fallback-VLAN
discussion are non-negotiable.

## Teaching Demonstrations
1. Port-forward exposure recreation: one static NAT rule → the service is internet-reachable; "NAT did that by accident — policy on purpose."
2. Egress pair: direct-to-IP rejected (deny log!), same via proxy allowed — the pair works; then remove the proxy and watch the deny volume become the detection feed.
3. RADIUS Accept anatomy: the attribute lines (VLAN assignment) — identity-driven policy in four lines.

## Expected Student Difficulties
1. NAT-as-firewall intuition is *deep* — the one-line port-forward demo is the antidote; show, don't tell.
2. 802.1X role confusion — the three-role diagram plus "credentials never on the [wireless] air" anchor (full wireless treatment L18).
3. MAB feels pointless — reframe: identification for IoT, protected by isolation VLAN + posture.

## Discussion Facilitation
Q5 (critical-auth fallback) is the design question executives ask at 08:00 Monday —
require *specifics* (which VLAN, what access, what logging). Q3 (direct-to-IP 443)
has honest costs: name them (TLS/SNI-less tools, CDNs) before the value argument.

## Lab Troubleshooting (egress-lab context)
- Spoof test blocked by hypervisor: the range's test host is pre-authorized — use it, not personal VMs.
- Deny logs missing: rule logging flag off — check the log checkbox first.
- Proxy PAC not applying: browser cache — hard-refresh or use the provided test profile.

## Accessibility Notes
- Firewall GUIs: keyboard paths + text exports distributed.
- RADIUS attribute tables: pre-distributed as text.

## CS & Data Science Applications
- **CS:** NAT is a stateful translation table — same data-structure thinking as L10's state table; 802.1X is an authentication protocol they can map to their security courses.
- **DS:** egress deny logs are the highest-precision detection feeds — quantify it: baseline deny rates, then alert on deviation (L21 preview).

## Links
Plan: `modules/module-03-secure-architecture/lectures/lecture-12-nat-proxies-egress-nac.md` · Student page: `docs/lectures/lecture-12-nat-proxies-egress-nac.md` · Answers: `teaching/answer-keys/answer-key-module-03.md`
