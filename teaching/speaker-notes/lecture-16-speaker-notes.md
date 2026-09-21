---
lecture: L16
module: 4
week: 8
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L16 Speaker Notes — Modern VPNs & Crypto Agility

## Delivery Guide
The WireGuard demo (silent-by-design scan behavior + AllowedIPs-as-policy) is the
differentiator — run it after the IPsec comparison lands. The Midterm consumes
45 minutes mid-session; schedule around it strictly (see timing). The scenario-card
evaluation runs post-exam in a deliberately low-stakes mode — it's a rehearsal for
capstone design defense, so keep the tone exploratory. PQC stays directional:
status and migration thinking, not hype.

## Timing Plan
0–10 failure-taxonomy card game · 10–35 WireGuard design + demo · 35–55 TLS-VPN +
remote-access architecture · 55–70 agility + PQC · 70–75 short break · 75–105
**Midterm** · 105–115 scenario evaluation (low-stakes) · 115–120 wrap + Lab-08
reminder. **Compression:** if the midterm needs 50 minutes, drop Hypothesis-A card;
never compress the exam window.

## Teaching Demonstrations
1. WireGuard pair up on the range: `wg show` (handshake age, counters); then nmap the port — silence without keys.
2. AllowedIPs misuse: set `/0` on a peer → observe the leak/route grab; reset.
3. Hybrid-KEM status slide: FIPS 203/204/205 (2024) + hybrid X25519+ML-KEM in TLS 1.3/IKEv2 — current-state honesty.

## Expected Student Difficulties
1. "WireGuard is just better" — the ops trade-offs (rotation scripting, no dynamic routing, MFA at orchestration) reframe it.
2. Split-tunnel DNS leaks are invisible to them — the route-table + resolver-config exercise makes the leak findable.
3. PQC fatigue/hype — the "migrate key exchange first, via hybrids" plan is the sober takeaway.

## Discussion Facilitation
Q5 (IdP outage per model) is the availability-vs-security discussion: reward
break-glass designs (local cert fallback, scheduled exceptions). The post-exam
evaluation: no grades, no ridicule — the rubric is the criteria matrix itself.

## Lab Troubleshooting (demo + build context)
- WireGuard handshake stuck: key mismatch or `AllowedIPs` overlap — check both configs symmetric.
- Endpoint unreachable: `PersistentKeepalive` behind NAT — set 25; explain why.
- Post-exam brain fog: the evaluation is oral/pairs — no individual deliverable pressure today.

## Accessibility Notes
- Exam accommodations per institutional policy — pre-arranged, quiet room, time-and-a-half as documented.
- Scenario cards: digital text versions; evaluation may be written instead of oral.

## CS & Data Science Applications
- **CS:** Noise-IK handshake parallels TLS reading skills they built in L14 — transfer, don't reteach; crypto agility maps to dependency-management discipline.
- **DS:** PQC migration is an *inventory problem* — asset/algorithm corpora, gap analysis; a genuine DS-flavored capstone angle worth mentioning.

## Links
Plan: `modules/module-04-crypto-protocols/lectures/lecture-16-modern-vpns-crypto-agility.md` · Student page: `docs/lectures/lecture-16-modern-vpns-crypto-agility.md` · Answers: `teaching/answer-keys/answer-key-module-04.md`
