---
case: cs-043
solution-for: modules/module-04-crypto-protocols/case-studies/cs-043-hash-collision-integrity-impact.md
difficulty: intermediate
module: 4
lecture-anchor: L13
clos: [CLO-5]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-043 Solution — Hash-Collision Brief (INSTRUCTOR ONLY)

## Model Solution

**Technical brief (3 paragraphs):**

*1. The attack classes.* A **collision** finds any two distinct inputs with
the same hash — for MD5, craftable in seconds on laptops (identical-prefix
and chosen-prefix collisions exist). A **second-preimage** attack, given a
specific file F, finds a *different* F′ with the same hash — MD5 remains
unbroken for second preimages at meaningful scale. A **preimage** attack,
given only a hash h, finds any input mapping to it — also unbroken for MD5.
"Broken since 2004" refers to collisions (Wang et al.), not to the
properties a download-verifier actually needs.

*2. What collisions enable here — and what they don't.* Chosen-prefix
collisions let an attacker craft *two* files that collide — the classic
weaponized scenario was crafted X.509 certificates on colliding serial
numbers (2008 rogue-CA proof-of-concept), where the attacker controlled
*both* documents and a third party vouched for one. The archive scenario
differs structurally: the contributor would need to craft a *malicious
dataset* that collides with a *specific benign dataset the archive already
published* — that's second preimage, not collision, and it's out of MD5's
broken reach. What collisions do enable: an attacker who can get the
archive to publish checksums of *both* their files (e.g., a malicious
contributor submitting a "clean" and a "dirty" variant through the same
pipeline, then swapping post-publication) can make the swap look
checksum-valid.

*3. Where the real weakness lives.* The scheme's exposure is not MD5's
math — it's that **the checksum is published on the same page, under the
same control, with no signature**: if an attacker controls the archive (or
its host), they substitute file *and* checksum together. Integrity here
rests on the archive's honesty and its host's security; the hash is
accident-detection plus tamper-*evidence* under audit, not tamper-proofing.
Any migration that adds SHA-256 but leaves the "same page, no signature"
model retains the same fundamental property — better collision resistance
against crafted swaps, identical trust model.

**Process assessment:** the *dominant* threat this process faces is
**transfer corruption** (bit rot, truncation, mirror drift) — MD5 handles
that fine today. The *adversarial* threat (crafted substitution) is real
but narrow: it requires the contributor to push both variants through the
archive's own pipeline. Mirrors comparing MD5 nightly are also
accident-detection — fine. Verdict: the contributor is **right about the
direction, wrong about the mechanism** — migrate, but for supply-chain and
future-proofing reasons, with signatures being the substantive upgrade.

**Migration plan:**

1. Publish **SHA-256** alongside MD5 now (dual-publish for transition);
   MD5 sunset in 12 months.
2. **Sign the manifest** — the substantive fix: archive signs
   (ed25519/RSA) a manifest of filename→hash (SHA-256); users verify
   signature against a *pinned* archive public key distributed out-of-band.
   Now substitution requires the archive's *signing key*, not page access.
3. Optional: **reproducible-build-friendly** per-file hashes + timestamped
   transparency log if the archive's trust ambitions grow.
4. Honest statement for the brief: *any* checksum scheme verifies that
   "what you received is what the archive intended to publish" — it cannot
   verify the dataset's *scientific* integrity or the archive's own
   trustworthiness; signatures shift the trust root to a key you control,
   which is the strongest available answer.

## Alternative Solutions

- **"MD5 is fine here, change nothing":** defensible on collision-vs-
  second-preimage grounds alone, but ignores the crafted-swap path and
  supply-chain expectations; half credit for the analysis, not the
  conclusion.
- **"Switch to SHA-3/BLAKE3":** fine algorithms; the distinction that
  matters (signatures + trust root) is orthogonal to SHA-2-vs-3 — naming
  that is the sophistication marker.
- **Per-file GPG signatures by contributors:** stronger per-file provenance;
  key-management burden moves to contributors — a real tradeoff to name.

## Tradeoffs

- Dual-publishing during transition: doubles surface for confusion but
  keeps mirrors/users unbroken.
- Signature key custody: the archive now runs *key management* (cs-041's
  lesson in miniature) — HSM/token + escrow or the signature is theater.
- Contributor signatures vs archive-only: provenance vs onboarding
  friction.

## Common Mistakes

- "MD5 collisions = anyone can replace any file" (that's second preimage).
- Missing the same-page/no-signature trust-model point entirely.
- Migrating hash function while calling it "the fix" (the real fix is
  signatures).
- Treating mirrors' MD5 comparison as adversarial verification.

## Instructor Prompts

- "Which attack would the crafted-certificate scenario need, and why
  doesn't it transfer here?"
- "What does the signature change about *who* can lie?"
- "Why does the archive run key management the moment it signs?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Attack-class mapping; trust-root insight |
| Technical accuracy | 25% | Collision/second-preimage/preimage precision |
| Alternatives considered | 20% | Hash-choice-vs-signature distinction |
| Communication | 15% | Brief readable by a director, not just engineers |

**Timing:** reveal at 5:00 + 2; "right about the direction, wrong about the
mechanism" is the verdict to land.

## CLO Mapping

- **CLO-5** — Hash-function properties mapped to actual use cases.
