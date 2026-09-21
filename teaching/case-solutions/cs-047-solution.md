---
case: cs-047
solution-for: modules/module-04-crypto-protocols/case-studies/cs-047-weak-cipher-suite-audit-and-remediation-plan.md
difficulty: advanced
module: 4
lecture-anchor: L14
clos: [CLO-6]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-047 Solution — Weak-Cipher Audit (INSTRUCTOR ONLY)

## Model Solution

**Risk ranking (weakness × reachability × clients):**

| Rank | Finding | Mechanism | Why here |
|---|---|---|---|
| 1 | **Admin tools: RC4 enabled** | RC4 is *prohibited* with no safe configuration (biases → practical plaintext recovery historically); enabled "for an old tool" with **no owner** | Internet-adjacent admin plane + unowned exposure = fix today; one flag |
| 2 | **Imaging modalities: TLS 1.0 + 3DES + RC4** | Weakest stack in the estate; RC4 presence again the hard line; 3DES's ~2³²-record birthday bound (Sweet32) is real for imaging sessions | Isolated VLAN *gates* reachability (raises effort) but the suite state is indefensible — compensating controls now, firmware campaign next |
| 3 | **HL7 engines: TLS 1.0 negotiable + 3DES** | Deprecated protocol floor on internal interfaces; Sweet32 bound applies to long-lived HL7 streams (chatty!) | Internal reach lowers external risk; long-lived clinical streams raise record-count exposure |
| 4 | **Portal CBC-SHA alongside GCM** | CBC suites are *degraded-but-defended* (Lucky13-class mitigations in modern stacks); server prefers GCM if ordered so | Public-facing but modern clients negotiate AEAD; ordering fix, not a fire |

**RC4 vs 3DES in one paragraph:** both are deprecated, but they fail
differently. **RC4** is *prohibited* (RFC 7465) — its keystream biases are a
design flaw with no configuration remedy; TLS 1.3 dropped it, every
guideline bans it, and leaving it enabled is indefensible anywhere — that's
why the admin-tools line is a today-fix. **3DES** is *deprecated*
(RFC 8996-era guidance) rather than categorically broken: its concrete
weakness is the 64-bit block → Sweet32 birthday-bound plaintext recovery
after ~2³² records under one key — an attack *gated on volume and session
length*, mitigable by rekeying/short sessions, and irrelevant for
short-lived handshakes. So 3DES remediation is *urgent where sessions are
long and chatty* (HL7, imaging streams) and merely important elsewhere —
which is exactly the nuance the sequencing plan needs.

**Sequenced plan:**

*Phase 0 — today:* admin tools: disable RC4 (and CBC while there; 3 users,
one LB flag); add the "old tool" mystery to the asset register with an
owner. Re-scan to prove.
*Phase 1 — this month (no clinical risk):* portal LB: reorder preference to
AEAD-only (GCM/ChaCha), drop CBC-SHA, drop 1.0/1.1 if any crept into the
default templates; HL7 engines: raise floor to 1.2 where clinical apps
support it (coordinate: most modern HL7-over-TLS stacks do), enforce
session rekey limits for the engines that can't.
*Phase 2 — this quarter, modalities:* **compensating controls immediately**
(micro-segment the modality VLAN: modality↔PACS only, deny egress, deny
inter-modality; IDS signatures for RC4/3DES negotiation *attempts* on that
VLAN as tamper-detection; no remote admin to devices from outside the VLAN);
**vendor campaign** opened with the 10 devices' firmware status documented,
target: TLS 1.2+AEAD or replacement at next capital cycle; risk acceptance
signed by CISO with expiry (6 months) — the acceptance *with controls and a
date* is what makes "can't fix yet" defensible to assessors.

## Alternative Solutions

- **Estate-wide TLS 1.3-only mandate:** the right end-state; as phase 1 it
  breaks clinical apps and invites shadow HTTP — the sequencing *is* the
  plan.
- **Bridge proxy in front of modalities (terminate modern TLS, re-encrypt
  to device):** genuinely strong interim — costs an appliance and vendor
  validation; name it as the phase-2 accelerator if firmware stalls.
- **Accept-and-document for HL7 engines too:** weaker — engines are
  software and updatable; acceptance is reserved for the truly frozen.

## Tradeoffs

- Floor-raising vs clinical-app compatibility: test per engine; the
  interface-engine owners must be in the loop or phase 1 stalls.
- Compensating controls vs firmware campaign speed: controls buy the time
  the vendor needs — without the *dated* acceptance they buy nothing.
- CBC ordering fix (cheap) vs AEAD-only (correct): AEAD-only where client
  population allows; ordering where it doesn't.

## Common Mistakes

- Ranking portal-CBC above modality-RC4 (reachability inverted the math).
- Treating 3DES and RC4 as equally urgent (different mechanisms).
- "Vendor-frozen = done" (the compensating trio is the professional answer).
- No dated risk acceptance — assessors read undated acceptances as open
  findings.

## Instructor Prompts

- "Which endpoint is a 10-minute fix with outsized audit value?"
- "Why does HL7's chattiness change 3DES's urgency?"
- "What exactly does the risk-acceptance document have to contain?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Multiplicative risk logic; RC4/3DES distinction |
| Technical accuracy | 25% | Suite/protocol attack mechanics correct |
| Alternatives considered | 20% | Bridge-proxy/acceptance design |
| Communication | 15% | Ranking + 3-phase plan readable by board |

**Timing:** reveal at 5:00 + 2; "today-fix" identification is the practical
payoff.

## CLO Mapping

- **CLO-6** — Cipher-suite risk analysis and constrained remediation.
