---
case: cs-065
solution-for: modules/module-05-wireless-cloud/case-studies/cs-065-flow-log-investigation-of-anomalous-cloud-traffic.md
difficulty: advanced
module: 5
lecture-anchor: L20
clos: [CLO-13]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-065 Solution — Flow-Log Adjudication (INSTRUCTOR ONLY)

## Model Solution

**Verdict: exfiltration — high confidence.** Discriminating features:

| Feature | Documented sync predicts | Observed 01:40–07:30 | Verdict |
|---|---|---|---|
| Direction | ingress-heavy (pull from lake) | **egress 700 GB out** | negation of profile |
| Peer class | private endpoint (data-lake) | **shared-NAT → external :443** | undocumented path for the DS fleet |
| Timing | bounded 22:00–01:00 | **starts 40 min after sync ends, runs 6 h** | post-window continuation = different job |
| Shape | bulk transfers | ~26 MB/s steady, small flows interleaved (beacon-ish chunking) | staged upload pattern |
| DNS | none external | **external :53 query at 03:10** from a node with no documented external DNS | C2/bootstrap-class signal — small in bytes, huge in meaning |

The legitimate 74 GB ingress (22:00–01:00) *matches* the documented
profile — which is exactly why it makes the 700 GB egress **more**
suspicious, not less: a real sync job's profile predicts egress near
zero (acks + status), bounded to the window and the private peer. The
observed egress isn't the sync's continuation; it's a *second actor* on
the same node after the legitimate job ends. Confidence-raising evidence:
packet capture at the NAT (SNI/hostname for 185.x), node memory/disk
image (process holding the connections), and the workload-identity audit
log (which *bucket* API calls the node made — if the unused
bucket-writer role lit up, data-custody scope is known).

**The "nightly sync" trap:** teams pattern-match on *volume similarity*
(74 GB nightly ≈ "the node moves big numbers") and stop. The discipline:
adjudicate on the **profile** (direction/peer/window/shape), not the
volume; the volume merely explains why the *bill* noticed. The platform
team's defense is honest but answers a different question ("is 74 GB
normal?") than the one asked ("is *this* traffic the sync?").

**Containment + fix:**

*Tonight:*
1. **Isolate ds-compute-07** (security-group quarantine / stop-and-snapshot;
   preserve memory+disk for forensics before reimage).
2. **Revoke the node's workload identity session** + rotate; **strip the
   unused bucket-writer role** from the DS fleet's identity (the
   over-grant that made exfil *possible* — least privilege per fleet).
3. **Block the observed external IPs** at the NAT/firewall; alert on any
   sibling nodes reaching them.

*This week:*
4. **Egress policy for ds-compute class**: deny internet via NAT entirely
   (the DS fleet's documented path is private-endpoint only); if egress
   is ever needed (package installs), route via a proxy allow-list.
   The 700 GB needed the shared-NAT path — remove the path, the class
   dies.
5. **Detection that fires at 01:45:** flow-log alert on
   `ds-compute` class: egress-to-internet bytes > threshold (the class's
   documented baseline is **zero** — even 1 GB alarms; the design goal
   is "no internet egress to deviate from"), plus per-node egress-rate
   anomaly vs the sync window. Zero-baseline classes are the cheapest
   detections in cloud security.
6. Image-update governance: the "new python base image" 5 days prior gets
   a provenance check (was it built/signed internally?) — the entry
   vector hypothesis; scope check on sibling nodes with the same image.

## Alternative Solutions

- **"Wait for the platform team to confirm the job" (defer):** the job's
  owner is also the closest to being compromised *by their own pipeline*
  (supply-chain entry) — adjudicate on evidence; confirm in parallel,
  not instead.
- **"700 GB is plausible for model artifacts upload":** would be
  documented, scheduled, private-peered, and *ingress to a registry*, not
  NAT-bound :443 — the shape doesn't fit the hypothesis; name it and
  reject it.
- **Kill the node immediately without snapshot:** stops the bleed but
  destroys the custody evidence governance needs (what left, when, from
  which dataset) — snapshot-then-quarantine is the order.

## Tradeoffs

- Quarantine speed vs forensics completeness: snapshot costs ~15 min;
  700 GB/hour of ongoing loss rates it cheap.
- Zero-baseline egress denial vs DS flexibility (ad-hoc downloads): the
  proxy allow-list is the pressure valve; without one, users hotspot the
  workflow into shadow paths (worse).
- Revoke-credentials-now vs preserve-audit: revocation logs *the
  revocation*; the access audit trail already exists — revoke.

## Common Mistakes

- Adjudicating on volume ("that node always moves terabytes").
- Treating the legitimate 74 GB as exculpatory (it's the contrast that
  convicts).
- Missing the :53 detail (the smallest record, biggest signal).
- Fixing the node but not the *path* (shared NAT) or the *grant*
  (bucket-writer) — all three layers needed.

## Instructor Prompts

- "State the sync profile's four predictions — and mark which two the
  anomaly violates hardest."
- "Why is zero-baseline the best detection design here?"
- "What does the workload-identity audit log add to the custody answer?"

## Rubric (instructor grading anchor)

| Dimension | Weight | Full-credit anchor |
|---|---|---|
| Reasoning quality | 40% | Profile-based adjudication; contrast-not-consistency logic |
| Technical accuracy | 25% | Flow-log reading; NAT/endpoint/identity mechanics |
| Alternatives considered | 20% | Sync/benign hypotheses tested and rejected |
| Communication | 15% | Verdict + confidence + evidence-to-raise-it |

**Timing:** reveal at 5:00 + 10; the "profile, not volume" rule is the
transferable takeaway.

## CLO Mapping

- **CLO-13** — Cloud flow forensics and adjudication.
