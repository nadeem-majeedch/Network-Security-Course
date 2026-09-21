---
lecture: L14
module: 4
week: 7
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L14 Speaker Notes — TLS Deep Dive

## Delivery Guide
The handshake side-by-side (1.2 vs 1.3) is the lecture's centerpiece — run it with
the lab VM's keylog so decryption works and students see both the cleartext fields
and where encryption begins. The audit method (protocols → suites → groups → cert →
extras) is the graded skill: model it on the good endpoint, then hand them the bad
one. Connect back to L07 at the Finished-message moment: "this is why the MITM
became a certificate error."

## Timing Plan
0–10 PKI chain quiz · 10–40 handshakes (Wireshark side-by-side) · 40–60 suites +
agility (decode + deleted-algorithms) · 60–70 break · 70–95 config-audit method
(good vs bad endpoint) · 95–110 audit+fix pairs · 110–120 exit ticket + Pract-2
briefing. **Compression:** 1.2 walkthrough to slide if behind; the bad-endpoint
audit is the graded skill — protect it.

## Teaching Demonstrations
1. Handshake side-by-side: same fetch under 1.2 and 1.3; annotate ClientHello fields, encryption boundaries, Finished.
2. Suite decode relay: two suites on the board; teams fill the kx/auth/bulk/hash grid.
3. Audit method modeled: sslyze/testssl-style output on the good endpoint — classify each line; then reveal the bad endpoint.

## Expected Student Difficulties
1. "Finished authenticates the transcript" is abstract — the MITM-callback framing makes it land.
2. 0-RTT replay hazard: the replayed-POST thought experiment (two identical requests, one unintended) does it.
3. Missing-intermediate confusion ("works in browser!"): the curl-fails case is the canonical demo.

## Discussion Facilitation
Q4 (TLS inspection everywhere) is a governance+tech debate — steer to breakage
(pinning), the enterprise-CA trust decision (L07 callback), and metadata analytics
as the 80% substitute. Q5 (expired cert vs TLS 1.0): demand exploitability
reasoning, not vibes — the best answers discuss attacker prerequisites for each.

## Lab Troubleshooting (audit context)
- Audit tool missing on laptops: containerized runner provided; or use the range's preinstalled copy.
- `s_client` hangs on the bad endpoint: it negotiates legacy — use `-tls1_2` explicitly; that's a *technique*, not a bug.
- Keylog decryption not working: SSLKEYLOGFILE path/env mismatch — check the profile notes.

## Accessibility Notes
- Wireshark hex/decrypt views: provide annotated screenshots + verbal narration of each field.
- Audit reports: template with plain-language finding descriptions provided.

## CS & Data Science Applications
- **CS:** the handshake is a protocol-negotiation state machine — map to their networking/security theory; ALPN = in-band negotiation they've seen in HTTP/2.
- **DS:** JA3/JA4 fingerprints are feature vectors for classification — a real DS application on TLS metadata; note stability caveats (L29 revisits).

## Links
Plan: `modules/module-04-crypto-protocols/lectures/lecture-14-tls-deep-dive.md` · Student page: `docs/lectures/lecture-14-tls-deep-dive.md` · Answers: `teaching/answer-keys/answer-key-module-04.md`
