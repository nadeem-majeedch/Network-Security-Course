---
case: cs-073
solution-for: modules/module-06-detection-vulnerability/case-studies/cs-073-dns-tunneling-detection-design.md
difficulty: advanced
module: 6
lecture-anchor: L23
clos: [CLO-9, CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-073 Solution — DNS-Tunneling Detection (INSTRUCTOR ONLY)

## Model Solution

**Quantitative fingerprints per variant:**

*Bandwidth math (the anchor):* a DNS query label ≤63 B; a name ≤253 B;
payload per query ≈ 180–250 B after encoding overhead. At **1 q/s**,
an uplink tunnel moves ≈ **0.18–0.25 KB/s ≈ 15–21 MB/h** — a *slow*
channel by design; detectors must therefore key on *pattern*, not just
volume. Exfil of a 100 MB dataset needs ≈ 5,000–5,500 q/s-sustained
(unrealistic) or hours at plausible rates — meaning tunnels favor
**credentials/keys/beacons**, not bulk (which shapes what you hunt:
low-volume high-entropy, sustained).

| Variant | Uplink fingerprint | Downlink fingerprint |
|---|---|---|
| (a) TXT up/down | query names: short + sequential IDs; **type=TXT dominant**; responses: large TXT (>100 B) — response bytes ≫ request bytes (the *asymmetry flip*: normal DNS responses are small) | TXT response size distribution is the give: legitimate TXT (SPF/DKIM) is sparse/punctuated; tunnel TXT is *every query, uniformly large* |
| (b) A-record subdomain encoding | **long leftmost labels (≥40 B), high entropy (Shannon ≥3.5 bits/B)**; queries per parent domain: hundreds+; NXDOMAIN high (if DGA-ish parent) or zero (if attacker-authoritative) | A answers: few, but every query carries the *data* — query-length distribution is the fingerprint |
| (c) CNAME chains | long chains (>4 hops), sequential labels | chain depth is legit for CDNs — depth *plus* per-client rate is the discriminator |
| (d) NULL/exotic types | type distribution: NULL/other ≫ A/AAAA | rarest in benign traffic — near-zero FP by type alone |

**Layered detector set:**

| # | Detector | Window/threshold | Benign FP source | FP mitigation |
|---|---|---|---|---|
| 1 | **Per-client label-entropy detector** | 10-min window; alert: ≥50 queries with mean label-entropy ≥3.5 bits/B *and* mean label-length ≥40 B | security scanners' generated names (but: scanners target *known* zones, lower entropy per label) | enrich with client asset class — scanner hosts allowlisted w/ corpus check (cs-071 pattern) |
| 2 | **Type-distribution detector** | per-client per-hour: TXT+NULL share of queries >30% (benign fleet norm: <2%) | DKIM/SPF-heavy mail services (server class) | baseline *per client class* — mail servers exempted by class, not by host (drift-safe) |
| 3 | **NXDOMAIN/timeout detector** | per-client: NXDOMAIN ratio >50% over ≥100 queries/10 min | misconfigured apps (stale records) — but their queries are *low-entropy, repeated* | entropy + NXDOMAIN *conjunction* — stale-record clients fail the entropy leg |
| 4 | **Per-domain uniqueness detector** | per client-domain pair: >200 distinct subdomains/hour under one non-CDN parent | legit CDNs (cs-072's benign weird) — but CDN parents are *known-fleet-wide* (many clients, few parents) | parent-domain reputation: tunnel parents are *novel* (first-seen this month) AND single-client; CDN parents are old AND fleet-wide — the 2×2 decides |

*Design note:* no single detector survives the FP sources alone; the
conjunctions (entropy+NXDOMAIN, uniqueness+novelty) are the stack — and
detector 2 is near-FP-free for the fleet *except* mail servers, which
class-baselining handles.

**The policy line (students testing detectors):**

- **Authorized:** the security lab range (dedicated VLAN/parent-domain
  issued for coursework) during published red-team windows — the
  detector's alert payload carries *identity enrichment* (user,
  host-class, VLAN) so a lab-range alert auto-tags "authorized-test" and
  routes to the exercise channel, not the incident channel.
- **Not authorized:** any tunneling from the general fleet — the same
  alert with fleet-VLAN enrichment routes to incident response.
- The written policy: testing outside the lab range is a conduct matter
  *even when detected "as a test"* — the enrichment makes the
  distinction mechanical, which protects students (no ambiguity-driven
  accusations) and the response team (no manual adjudication per
  alert).

## Alternative Solutions

- **Block TXT/NULL at the resolver wholesale:** kills variants (a)/(d)
  cheaply — breaks DKIM-verification *outbound* paths and any legit TXT
  API; as a *resolver policy for student VLANs* it's defensible (with
  documented breakage), as fleet-wide it isn't — the honest layered
  answer is detect-first, then targeted policy.
- **Response-asymmetry detector as primary:** powerful for TXT downlink
  tunnels but blind to A-record uplink (responses tiny) — a layer, not
  the stack.
- **DoH-block-and-hope:** DoH isn't DNS-tunneling's only carrier and
  blocking it (cs-038) is already policy — the tunnel class persists
  inside approved resolvers, which is exactly what these detectors
  watch.

## Tradeoffs

- Threshold tightness vs FP load: entropy 3.5 + length 40 is tight
  enough that scanner-corpus allowlists stay small; loosening to catch
  low-entropy encodings (base32-ish) trades FP volume — review monthly
  with hit rates.
- Per-client baselines vs fleet-wide norms: per-client is precise but
  cold-start-heavy (new laptops); fleet-norms bootstrap then hand off —
  two-phase baselining.
- Blocking-first vs detecting-first: blocking TXT on student VLANs is
  cheap prevention; fleet-wide detection is the durable answer — scope
  the block to the portal's constituency.

## Common Mistakes

- Volume-only detection (tunnels are *slow* by design — the bandwidth
  math kills that detector).
- CDN FP blindness (CNAME-depth alone convicts your own content
  delivery).
- No identity enrichment (alerts can't distinguish lab-range tests from
  fleet abuse — policy chaos).
- Type-distribution without class-baselining (mail servers drown it).

## Instructor Prompts

- "Do the bandwidth math: why is 'bulk exfil over DNS' a category
  error?"
- "Which detector survives the mail-server FP — and how?"
- "What makes the alert payload's enrichment a *policy* control, not
  just operational convenience?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Bandwidth-math fingerprints; FP-conjunction design |
| Technical accuracy | 25% | Variant mechanics, entropy/label stats |
| Alternatives considered | 20% | Resolver-policy tradeoffs |
| Communication | 15% | Detector table + policy line |

**Timing:** reveal at 5:00 + 10; the bandwidth math is the quantitative
anchor.

## CLO Mapping

- **CLO-9** — Detector design with quantitative thresholds.
- **CLO-12** — Protocol-aware anomaly analytics.
