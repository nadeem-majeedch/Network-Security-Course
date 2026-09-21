---
exam: final
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-8, CLO-9, CLO-10, CLO-11, CLO-12, CLO-13, CLO-14, CLO-15]
marks: 100
status: complete
---

# Answer Key & Marking Scheme — Final Examination

> **INSTRUCTOR ONLY.** Part I answers verified against L17–L32 plans.
> Part II anchors reference the seeded artifacts in the Lab-13/15 dataset
> (sha256-verified distribution; regenerate via
> `docs/labs/setup/generate_lab_datasets.py` if the range is rebuilt).

## Part I — Section A (2 each; 16 total)

| Q | Answer | Rationale |
|---|---|---|
| A1 | **B** | WPA2-PSK handshake = offline-verifiable; SAE (WPA3) removes it. |
| A2 | **B** | SG stateful instance-attached; NACL stateless subnet. |
| A3 | **B** | Zeek = protocol behavioral logging. |
| A4 | **B** | Environmental = asset context. |
| A5 | **B** | Reversibility protects evidence + limits wrong-action cost. |
| A6 | **B** | The evidence-boundary phrase (cs-087). |
| A7 | **B** | Outcome vs activity metric (cs-094). |
| A8 | **B** | Gates = measured evidence before next tranche (cs-093). |

## Part I — Section B (6 each; 24 total)

**B1 (6).** Attribution first: (1) enumerate the instance's agents/jobs and
match destination + volume history to a documented pattern (vendor
endpoint check); (2) compare with peer instances / 30-day baseline.
*(4)* Containment without touching it: subnet-level egress restriction
(NACL/egress-only route or edge firewall deny for that destination).
*(2)*

**B2 (6).** Three inputs beyond base score: **reachability/exposure**
(network path? internet-facing?), **asset criticality** (business impact
of compromise), **known-exploited/threat-intel status** (+ compensating
controls as a modifier). *(2 each)*

**B3 (6).** Eradication = removing attacker presence & persistence
(suspend tasks, rotate credentials, patch entry vector); recovery =
restoring service *after* eradication is verified (restore from clean
generations, monitor). *(3)* The most common restore gate: **persistence
mechanism confirmed bounded / eradication verified** (plus clean backup
generation). *(3)*

**B4 (6).** Falsifiable restatement, e.g.: *"If C2 beaconing exists, host
X will show outbound connections to a fixed external IP at regular
intervals (σ < 10% of interval) over ≥10 connections in 24 h; absence of
such periodicity in 90 days of proxy+flow data closes the hypothesis."*
Marks: measurable signal (3), stated data window/source (2), explicit
absence-condition (1).

## Part I — Section C (20) — model answer

Daily minutes: **A** = 900 × 4 = **3,600** · **B** = 1,400 × 2 =
**2,800** · **H** = 300 × 5 = **1,500** · **G** = 8 × 30 = **240**. *(4)*

Choose: **H first** (1,500 min + trust poisoning: a *broken* rule trains
analysts to dismiss a whole channel — fixing restores signal + reclaims
time; regression proof trivial — the rule fires on everything, replay
shows what it *should* fire on), then **A** (3,600 min at ~1% TP — the
largest true burden; scope by host-class baseline, replay must show zero
lost TPs from the ~9 real hits). *(6)*

**Why not B first despite the largest volume:** B's TPs ≈ 0 and its
2-minute triage is cheap per alert — it's policy noise; auto-close with
digest is the *third* change (defensible), but the trust-damage and
burden arguments rank H+A ahead. A pure "biggest number first" argument
misses that H's minutes are *signal-destroying* and A's are
*capacity-destroying*. *(6)*

Regression-safety proof: before/after replay on ≥30 days of historical
data; per-class TP diff = 0; document with the CISO artifact (the
assignment-4 discipline). *(4)*

## Part II — Forensic practical (40) — marking scheme

> Seeded artifacts (the dataset students analyzed in Lab-13/15): phishing
> entry via `invoice-portal` credential page → svc_ops-style account use →
> SMB staging from one workstation → 640 MB single-session TLS egress.
> Students have seen the *laboratory* version; the exam variant changes
> timestamps/hostnames, so pattern fluency (not memory) is tested.

### P1 — Evidence handling (8)

| Element | Marks |
|---|---|
| Hash the originals *before* analysis (`sha256sum` against the distributed SHA256SUMS; or `md5`/`sha256` over the working copy), record in the worksheet | 5 |
| Work on copies; originals read-only (stated or shown) | 3 |

*Commands in full credit shape: `sha256sum incident-week-pcap.pcap`,
`cp` to a working dir, `chmod a-w` on originals. Any two documented
integrity steps with commands earn 6–8.*

### P2 — Timeline (14)

Expected entries (source-tagged + confidence):

| Entry | Source | Confidence | Marks |
|---|---|---|---|
| Phishing link click / credential POST (proxy log) | log | supported | 2 |
| Account login/anomaly (auth log) | log | supported | 2 |
| Recon/scan from the compromised host (PCAP + flow) | PCAP+log | corroborated | 2 |
| SMB staging to the file server (PCAP/Zeek) | PCAP | corroborated | 3 |
| Large single-session TLS egress (PCAP/flow) | PCAP+log | corroborated | 3 |
| Any correct "absence" entry (e.g., no further staging post-T) with source cited | any | — | 2 |

*Confidence discipline graded: entries claiming "corroborated" without a
second source lose 1 each; timestamps need not match the lab version —
the exam set's own values do.*

### P3 — Attack-path synthesis (12)

| Element | Marks |
|---|---|
| Initial access named (credential phishing) with evidence pointer | 3 |
| Two chain-breaking controls (technical: e.g., MFA/phishing-resistant auth, egress allow-list, DAI not applicable — accept any defensible pair; process: mail filtering/report workflow, patch of the entry app) | 4 |
| First detection with logic (e.g., "single-session egress >500 MB to unlisted destination → alert"; or staging SMB burst rule) — measurable threshold required | 5 |

### P4 — Reporting (6)

| Element | Marks |
|---|---|
| Facts with sources named | 2 |
| Confidence labels present | 2 |
| One explicit unknown (e.g., payload contents of the encrypted session) | 2 |

*Invented certainty ("data stolen") loses the labels marks; the defensible
register is the entire course through-line.*

## Post-exam calibration note

Record the class's actual Part-II P2 median and the P1 command fluency
here after marking. If P1 hashes <50%, next cohort's Lab-01 gains an
explicit hash step — do not pre-fill.
