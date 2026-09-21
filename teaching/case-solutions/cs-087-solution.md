---
case: cs-087
title: Rebuilding the Intrusion Timeline from Five Sources (Solution)
difficulty: expert
module: 7
lecture-anchor: L26
clos: [CLO-11, CLO-12]
status: complete
artifact-type: instructor-solution
instructor-only: true
distribution: never-publish-to-students
---

# cs-087 — Solution: Five-Source Timeline Reconstruction

> **INSTRUCTOR ONLY.** Model solution for cs-087.

## Model Solution

### 1. Corroborated timeline

| T (day:time) | Event | Sources | Confidence |
|---|---|---|---|
| 20 22:14 | W-31 authenticates as svc_erp (no MFA) | AD | Supported (single strong source; EDR on ERP would corroborate) |
| 20 22:2x | Credential-access tool run on ERP | EDR | Supported |
| 21 daily | SMB flows ERP ← W-31 | FW + Zeek | **Corroborated** |
| 22 03:00 | LDAP reads ERP → DC (recon of directory) | Zeek | Supported |
| 22 04:00 | EDR agent goes offline | EDR | Supported (tamper hypothesis — see §2) |
| 22 (time unknown) | 1.2 GB egress ERP → unknown domain | FW + Proxy | **Corroborated** (volume; content unknown) |
| 23 11:00 | EDR uninstalled | EDR (+ absence in Zeek/FW) | Supported |

Initial access: **day 20 ~22:14** via svc_erp credentials on W-31
(corroboration would strengthen with FW showing W-31→ERP:445 *at
22:14*, not just daily).

### 2. The EDR gap (day 22 04:00 → day 23 11:00)

**What the other sources support:** the gap contains the egress —
1.2 GB left via proxy while the agent was dark, and LDAP recon
preceded it. Inference: attacker *blinded the agent* (offline at
04:00, uninstalled later = deliberate tamper pattern, not crash).
**What cannot be concluded:** anything about on-host actions in the
gap — process execution, file access, lateral moves from ERP are
unknown. State the bound: "host-level activity day 22 04:00–day 23
11:00 is unobserved; perimeter and directory telemetry bound but do
not fill this gap."

### 3. Exfiltration question

1.2 GB to an unknown domain via the corporate proxy is **strong
circumstantial evidence of exfiltration** but not a defensible
finding alone. Upgrade path for legal:
- Identify the destination (proxy category/WHOIS/PCAP if retained) —
  known-bad infrastructure upgrades it decisively.
- Determine *what* left: ERP database export size vs 1.2 GB; file-
  server or DB audit logs showing reads of matching volume day 22.
- Rule out benign (backup misroute, large update) via job schedules.
With destination + matching reads + no benign job, the finding is
defensible: "data matching ERP exports moved to unattributed
infrastructure on day 22."

### 4. Retention failures

- **Proxy at 7 days:** the destination domain's *early* access
  (day 20–21, if any) is already gone — was 1.2 GB one burst or a
  ramp? Unknowable now. Policy: security-relevant proxy logs ≥90
  days.
- **EDR coverage gap:** not retention but *coverage* — agent tamper
  created a hole; policy: tamper protection + alert-on-agent-offline.

## Alternative Solutions

- **Decline the timeline until more data:** never viable — legal
  needs the best defensible version *now* with confidence labels;
  refusing produces an un-labeled rumor mill instead.
- **Treat proxy volume as proven exfiltration:** over-claims;
  insurers/auditors will find the benign-explanation hole.

## Tradeoffs

- Confidence labeling vs readability: every entry carries provenance;
  a "clean" timeline without labels is less defensible, not more.
- Speed vs provenance: the insurer audit punishes unsourced entries —
  do it right the first time.

## Common Mistakes

- Presenting single-source entries as facts.
- Missing that the EDR offline event is itself evidence (tamper).
- Forgetting log-vs-event clock skew when merging sources (state the
  NTP status or note skew as unknown).
- Ignoring the retention boundary — claiming "no earlier access"
  when the logs can't show it.

## Instructor Prompts

- "Which single entry, if corroborated, most changes the legal
  posture?"
- "Why is 'agent uninstalled' stronger evidence of intent than
  'agent crashed'?"
- "What would you have needed *before* day 20 to make this timeline
  easy?"

## Rubric (10 pts)

| Criterion | Pts |
|---|---|
| Timeline entries correctly source-tagged with confidence levels | 3 |
| EDR-gap: correct inferences + explicit unknowns | 2 |
| Exfiltration: upgrade path for legal complete | 3 |
| Retention failures + policy fixes identified | 2 |

## Safety Notes

- Simulated; no real IOCs or exploit content.
