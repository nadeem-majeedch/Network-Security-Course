---
lab: Lab-11
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-11 (Flow Collector + Suricata Ruleset)

## Flow ground truth (generated, seed 411)
79 records: 40 background (mixed hosts/ports, 0.05–3 s durations); **planted
scan:** 15 one-way SYN flows (tcp_flags="S") from 10.20.0.66 to 10.20.30.10
across ports 21–8080, 60 B each; **planted beacon:** 24 DNS flows from
10.20.0.102 → 10.20.30.53 at exact 30 s cadence (first_switched spaced 30),
2 pkts / 196 B each, flags ".".

## Reference ruleset (grading anchor — syntax shape; ⚠️ verified as Suricata 7
documentation shape, not executed in authoring env)

```
# (a) scan tell — one-way SYNs to HOME_NET server subnet
alert tcp any any -> $HOME_NET !53 (msg:"NS401 one-way SYN (scan candidate)";
  flags:S; flow:stateless; threshold:type both, track by_src, count 10, seconds 10;
  sid:1000001; rev:1;)   # author: <student>

# (b) beacon cadence hint — TXT qtype to EXTERNAL_NET
alert dns any any -> $EXTERNAL_NET 53 (msg:"NS401 DNS TXT to external
  (beacon candidate)"; dns.query; content:"."; pcre:"/[a-z2-7]{20,}\./";
  threshold:type both, track by_src, count 5, seconds 120; sid:1000002; rev:1;)

# (c) exfil-shaped POST volume
alert http $HOME_NET any -> $EXTERNAL_NET any (msg:"NS401 periodic POST
  (exfil candidate)"; http.method; content:"POST"; flow:established,to_server;
  threshold:type both, track by_src, count 4, seconds 600; sid:1000003; rev:1;)
```

## Expected alert counts (grading anchor)
- On `lab13-incident.pcap` (malignant): (a) fires on the 5-port sweep
  (threshold-dependent — accept 1–5 alerts with documented threshold), (b)
  fires on the 24 TXT beacons (grouped by threshold), (c) fires on the 6
  POSTs. All three rules must fire *some* alert; exact counts depend on
  student thresholds — grade the documentation, not the number.
- On `lab11-clean.pcap` (benign range share): initial runs commonly fire (b)
  on benign periodic DNS (the planted lesson) — after scoping (TXT + entropy-
  shaped labels via pcre + threshold), expected clean-corpus count → 0.
  The before/after pair *is* the deliverable.

## Tuning exemplar (census → scope → document)
1. Census: rule (b) fires 12× on clean corpus — inspect eve.json fields:
   benign periodic queries are A-records with short labels.
2. Scope: add `pcre` length/entropy-shape + keep threshold; *do not* delete.
3. Document: exclusion note in the rule comment + expiry (re-review 90 d).

## Analysis-question model answers
1. **Aggregation level:** per-(src,dst,port) grouping revealed cadence that
   per-host totals hid — pipeline aggregation is a detection decision, not a
   storage detail.
2. **FN trade:** TXT-only misses A/AAAA beacons; threshold misses slow
   beacons — accept when clean-corpus precision demands; revisit at each
   tuning cycle (expiry discipline).
3. **CI for detection:** every rule faces malignant + clean corpora per merge;
   alert-count deltas gate the merge — the course's own validator habit
   applied to rules.
4. **Inline?** (b)'s residual FP rate → no inline blocking; IDS + SOC review;
   blocking decisions are change-controlled (L26).
5. **6 h beacons:** (b)'s threshold breaks; anomaly/baseline class (L23)
   replaces it — cadence-relative detection survives rotation better than
   signature.

## Grading notes
- Rules without intent+author comments lose hygiene marks (Lab-06 carryover).
- Clean-corpus "explicable" counts: students may leave *documented* benign
  firings with expiry — that's the honest professional state, not a failure.
- ⚠️ Suricata runs are range steps; ✅ the Python flow shapes in §6 executed.

## Command status
✅ Dataset + Python baseline shapes executed at authoring; ⚠️ Suricata
invocations are documentation-verified shapes (7.x).
