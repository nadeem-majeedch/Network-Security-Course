# cs-043 — Hash-Collision Implications for Integrity Checks

> **Simulated scenario.** The archive, processes, and claims are fictional.

## Difficulty & Domain

- **Difficulty:** Intermediate · **Domain:** VPN and secure remote access · **CLO:** CLO-5
- **Est. time:** 12 minutes · **Anchor:** L13 (Cryptographic Foundations)

## Scenario

A research-data archive publishes dataset integrity as "MD5 checksums,
published alongside downloads." A contributor submits a paper claiming MD5
is "broken since 2004" and the archive is therefore untrustworthy. The
archive director asks you for a **precise** technical brief: what MD5
collisions actually enable, what they don't, whether *this* process is
exposed, and what to migrate to — with the distinction between collision
and preimage attacks front and center.

## Stakeholders

- **Archive director** — wants the truth, not panic or dismissal.
- **Contributors** — checksums are part of the trust contract.
- **Researchers citing datasets** — integrity claims ripple into papers.
- **The contributor** — may be right for the wrong reasons.

## Network Context

- Process: contributor uploads dataset → archive computes MD5 → publishes
  alongside; downstream users recompute to verify transfer integrity.
- No signatures, no auth on checksums (both published on the same page).
- Optional second process: the archive *mirrors* datasets to 3 partner
  sites; mirrors compare MD5s nightly.

## Student Task

1. Write the **technical brief** (3 paragraphs): collision vs preimage vs
   second-preimage — what each attack class would require here; what MD5
   collisions *actually enable* (chosen-prefix craft) and what they don't.
2. Assess **this process**: which threat does the MD5 scheme actually face
   (transfer-corruption detection vs adversarial substitution), and where
   does the scheme's real weakness live (hint: it's not the hash function).
3. Give the **migration plan**: replacement algorithm, process change
   (signatures?), and the honest statement about what any checksum scheme
   can and cannot guarantee.

## How to Approach This (Reasoning Scaffold)

- "Broken" means specific things: collisions are *craftable*; preimages are
  not (for MD5). Which one does each use case need?
- The archive's trust model: users trust *the archive*, not the hash —
  if the archive is honest, MD5 catches accidents; if the archive (or its
  host) is malicious, no checksum published beside the file helps.
- Chosen-prefix collisions have a famous real-world use (crafted
  certificates) — know why *that* scenario differs from "verify my
  download."

## CLO Mapping

- **CLO-5** — Hash-function properties mapped to actual use cases.

## Safety Notes

- Educational brief; no collision-crafting tooling instructions.
