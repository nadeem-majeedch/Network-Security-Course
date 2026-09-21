---
lab: Lab-10
title: WPA-Enterprise Build + Cloud Flow Logs
week: 10
module: 5
clos: [CLO-8, CLO-13]
lectures: [L18, L20]
duration: 2h (embedded in lecture block)
status: complete
artifact-type: student-lab-handout
instructor-key: teaching/lab-answer-keys/lab-10-answer-key.md
---

# Lab-10 — WPA-Enterprise Build + Cloud Flow Logs

## 1. Lab Overview & CLO Mapping

Part A migrates the lab's test SSID from PSK to **WPA2/WPA3-Enterprise**
(802.1X with EAP-TLS) and verifies per-user authorization end-to-end. Part B
turns on cloud flow logs and reads them — the cloud twin of L21's pipeline.
This is the graded **Lab Pract-3**. *CLO-8* (enterprise wireless, rogue
defense posture) + *CLO-13* (cloud controls, flow logs). Reference lectures:
L18 (enterprise wireless & rogue defense), L20 (cloud/hybrid assurance).

## 2. Learning Objectives

By the end you can: (1) deploy 802.1X with a RADIUS server and per-user
certificates; (2) verify EAP-TLS negotiation and dynamic authorization results;
(3) enable and read VPC flow logs; (4) baseline cloud flows and spot
anomalous-shaped records; (5) articulate the rogue-AP defense posture for the
wired enterprise (L18's WIPS lifecycle, conceptually).

## 3. Prerequisites

Lab-09 submitted (survey + sandbox still clean); Lab-07's PKI skills reused
here for EAP-TLS certs; L18/L20 attended.

## 4. Estimated Duration

120 minutes: RADIUS+certs 35 · SSID migration 25 · flow logs 35 · write-up 25.

## 5. Required Software & Hardware

- Lab range: instructor AP (management access per team slot), FreeRADIUS VM
  (pinned image), issued client adapters; cloud sandbox from Lab-09 (rebuilt).

## 6. Setup Instructions

> **Command status:** ✅ verified shapes at authoring time; ⚠️ environment steps.

1. ⚠️ Issue EAP-TLS client certs from the Lab-07 issuing CA (cert template card
   on the lab sheet: clientAuth EKU).
2. ⚠️ FreeRADIUS: import CA + server cert; add one test user per team with the
   client cert; enable EAP-TLS in `mods-enabled/eap`.
3. ✅ Verify RADIUS before touching the AP:

```bash
# on the FreeRADIUS VM — shape verified; credentials per sheet
radtest -t eap-tls user01@lab.local  # (full invocation on lab sheet)
sudo journalctl -u freeradius -f      # ✅ watch: Access-Accept with EAP-TLS Success
```

4. ⚠️ AP: clone the PSK SSID to `LAB-ENT` — WPA2/WPA3 Enterprise, RADIUS
   10.20.30.181, dynamic VLAN 30 for the test user; join from the issued client.
5. ⚠️ Cloud: enable VPC flow logs (ALL, to the sandbox log store); generate
   traffic per the sheet (small instance curl loop to a TEST-NET address is
   provided as a script), wait ~10 min for delivery.

## 7. Authorization & Safety Notes

- **Authorization basis:** only the course AP, RADIUS VM, issued adapters, and instructor-managed sandbox org may be configured; per-team slots are the boundary and budget caps are binding.

- The AP/RADIUS are course infrastructure; config windows are per-team slots —
  breaking another team's slot by unsaved roaming changes is a policy incident.
- 802.1X credentials are personal: do not share certs between teams.
- Cloud: budget caps as Lab-09; flow logs cost money — set the retention the
  sheet specifies, not "forever" (retention is itself a CLO-13 point).

## 8. Student Tasks

1. **Pre-migration posture:** document the PSK SSID's weaknesses from L17
   (shared secret, revocation = rotating everyone) — your migration rationale.
2. **Deploy Enterprise:** complete RADIUS + AP config; join with the issued
   cert; capture the association + 4-way handshake frames (client-side capture
   on your own association — authorized).
3. **Verify authorization:** show in RADIUS logs the per-user Accept and the
   dynamic VLAN assignment; then *revoke* your test user (disable), attempt
   re-auth, record the Reject. That's the revocation story PSK cannot tell.
4. **Flow logs:** export the delivered flow records; build the 5-row summary
   table: top talkers, protocol mix, one-way flows, rejected-by-SG flows
   (log-only SG rules on), any beacon-cadence candidates.
5. **Rogue posture (conceptual):** using Lab-09's survey, write the WIPS-style
   classification for each SSID found (known/external/rogue-candidate) and the
   response for each class — no containment actions (legality + range policy).

## 9. Expected Observations

- EAP-TLS: Identity exchange, TLS tunnel establishment, then Success — visible
  in RADIUS debug logs; PSK 4-way handshakes carry no per-user identity.
- Revocation is immediate and per-user — the entire enterprise-vs-PSK argument
  in one drill.
- Flow logs: expect ~10 min delivery lag (teach patience + the pipeline cost);
  rejected flows appear because you enabled SG log-only rules.

## 10. Analysis Questions

1. Why does EAP-TLS resist offline passphrase attacks that WPA-PSK allows?
   State precisely what the attacker would need instead.
2. 802.1X validates the *server* cert too — what happens client-side if that
   validation is disabled (the top real-world deployment gap)?
3. Your flow summary shows periodic small one-way DNS flows to one external IP.
   What is the next evidence you would pull, and what would you *not* conclude
   from flow data alone?
4. MAB devices (printers) can't do 802.1X — what's the professional posture,
   and what does a too-broad MAB fallback cost you?
5. Retention: you set flow-log retention per the sheet (30 days). What trade
   did you make, and which investigation classes would outlive it?

## 11. Troubleshooting

- Client loops on auth → cert EKU missing clientAuth, or CA not trusted by
  RADIUS; read the RADIUS debug line that names the failure (it does name it).
- Dynamic VLAN ignored → switch/AP must support and pass the attribute; check
  the AP's RADIUS attribute mapping.
- No flow logs after 15 min → delivery is lazy; generate more traffic and
  re-check; verify the log destination and IAM path (sandbox org policy).

## 12. Cleanup Instructions

- Restore AP to the instructor baseline config (snapshot revert); disable your
  test user; remove client certs from the issued adapter profile.
- Cloud: flow logs stopped, log data deleted or per-sheet retention; resources
  deleted; screenshot proof.

## 13. Submission Requirements

- Migration rationale (pre/post table: PSK vs Enterprise per L17 criteria).
- RADIUS Accept/Reject transcript excerpts + association capture (annotated).
- Flow-log summary table + one anomaly hypothesis (explicitly labeled
  hypothesis).
- WIPS-classification posture note + analysis answers (5). Due: end of session
  (Pract-3 grading).

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| Enterprise build | Accept with dynamic VLAN + Reject-after-revoke both shown |
| Flow table | real numbers from delivered logs; lag acknowledged |
| Hypothesis | anomaly labeled as hypothesis with next-evidence step |
| Posture note | classification without illegal containment fantasies |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | transcripts/excerpts cited; hypothesis labeling |
| Mechanism accuracy | 30% | 802.1X/EAP-TLS + flow-log semantics correct |
| Analysis depth | 20% | revocation story; MAB; retention trade-offs |
| Safety & policy | 10% | slot discipline; budget; personal-credential hygiene |

## 16. Instructor Answer Key

RADIUS config reference, flow-log expected summary, grading notes:
`teaching/lab-answer-keys/lab-10-answer-key.md` (instructor-only).
