---
lab: Lab-12
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-12 (Zeek Analysis + Vulnerability→Hardening→Verify)

## Hunt ground truth (seed 413 corpus through Zeek)
- `dns.log`: beacon client **10.20.0.102** — 24 TXT queries to
  `*.cdn-metrics.example` (TEST-NET 203.0.113.7 as resolver answer target is
  *not* in this corpus; the beacon is resolver-facing), labels 26 chars,
  base32-alphabet (entropy ≈ log2(32)=5.0 bits/char → ≈130 bits per label),
  exact ~30 s cadence.
- Weakest single signal: TXT-concentration (legit DNSSEC-heavy resolvers also
  query TXT) — the *combination* (length+entropy+cadence+qtype) convicts.
- `conn.log` for a beacon uid: short duration (~0.02 s), tiny byte counts,
  orig≈2 pkts — the flow-view twin of Lab-11's CSV rows.

## UID-join reference
One uid appearing in conn.log (duration/bytes/state) + dns.log (query/qtype/
rcode) — each contributes what the other lacks (timing+volume vs names+type);
state that explicitly per the worksheet.

## Scan-cycle grading anchors
- Unauth vs credentialed diff: expect ≥2 credentialed-only findings per roster
  host (local patch state / config issues / installed-software exposure).
- Context stack: base CVSS alone fails; full credit shows exposure (where the
  host sits per the range map) + criticality (sheet-assigned) + exploitation
  evidence (KEV-style list supplied on the sheet) reordering the queue.
- Hardening menu (per-semester pinned): service config hardening, package
  update, stale-service disable, SSH policy tightening — exactly-two required
  with change log (what/restart/timestamp).
- Verify: re-scan diff attached; honest non-closure + exception memo
  (owner/compensating control/expiry/approver) scores equal to closure —
  the memo's *expiry* is the load-bearing field (unbounded exceptions rot).

## Analysis-question model answers
1. **CVSS-alone wrongness:** base CVSS ignores exposure/exploitation — a 9.8
   on an isolated test box queues behind a 7.5 on an internet-facing gateway
   (the L24 inversion, now with their own host as the example).
2. **Entropy threshold FPs:** CDN-bundled assets (long hash-like labels),
   backup jobs with generated names; baseline bounding: per-host profiles
   (L21/L23) absorb expected legit patterns.
3. **Real-cycle additions:** inventory freshness (CMDB reconciliation) +
   scan-policy windows + SLA metrics; compressed here: verification cadence
   and exception lifecycle — risks: unverified closures, immortal exceptions.
4. **Exception memo:** expiry is load-bearing because review is forced —
   compensating controls decay silently otherwise.
5. **Escalation step:** payload capture at the egress boundary (full PCAP or
   TLS-keyed inspection per policy) — requires explicit authorization scope
   (privacy/legal), not analyst discretion.

## Grading notes
- Arithmetic must be *shown* (entropy formula + one worked label); the sheet's
  function is fine, hand-waving is not.
- Scan-window and roster compliance are safety marks; any out-of-roster probe
  = zero (manual §2.3).
- ⚠️ Scanner runs are range steps; ✅ zeek -r / UID-join shapes executed.

## Command status
✅ Zeek offline processing + join shapes executed at authoring; ⚠️ scanner
invocations are environment steps with the pinned safe-mode profile.
