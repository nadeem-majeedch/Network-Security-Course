# Lab-09 — Wireless Characterization + VPC Segmentation

## 1. Lab Overview & CLO Mapping

Two-part week: characterize the *authorized* lab RF environment (which SSIDs,
channels, encryption, signal — no attacks), then design a three-tier VPC in the
cloud sandbox using the security-group model from L19. *CLO-8* — secure
wireless networks and evaluate deployments against attack classes. Reference
lectures: L17 (wireless fundamentals/threats), L19 (VPC design & controls).

## 2. Learning Objectives

By the end you can: (1) survey an authorized RF environment passively and
document SSIDs/channels/security postures; (2) reason about coverage vs
over-coverage as a security control; (3) design a VPC with public/private
subnets, security groups, and NACLs that implement a stated policy; (4)
distinguish SG (stateful, instance-level) from NACL (stateless, subnet-level)
behaviorally; (5) justify egress controls in both domains.

## 3. Prerequisites

Labs 01–08 submitted; L17/L19 attended; cloud sandbox account issued (free
tier, instructor-managed org).

## 4. Estimated Duration

120 minutes: RF survey 35 · VPC build 45 · policy verification 25 · write-up 15.

## 5. Required Software & Hardware

- Lab-range VM with a pinned USB Wi-Fi adapter (monitor-capable; instructor
  issued) — **passive survey only**.
- Cloud sandbox console + CLI (instructor-managed org; budget-capped).
- VPC reference diagram on the lab sheet.

## 6. Setup Instructions

> **Command status:** ✅ verified at authoring time (tool shapes); ⚠️ =
> environment steps.

1. ⚠️ Plug in the issued adapter; confirm presence (`ip link` / `iw dev`).
2. ✅ Passive survey shapes (no injection, no deauth, no association attempts):

```bash
sudo iw dev wlan0 scan | grep -E 'SSID:|freq:|signal:|capability:' > survey.txt
# Wireshark alternative: monitor mode on the issued adapter, capture 60 s, then
# Statistics → WLAN Traffic / Wireless toolbar channel view
```

3. ⚠️ Cloud: log into the sandbox org; accept the budget alert; CLI auth per
   the sheet (`aws configure` / equivalent).

## 7. Authorization & Safety Notes

- RF work is **passive characterization of the instructor-authorized lab space
  only** — no deauthentication, no association to SSIDs you don't own, no
  handshakes beyond ambient. Rogue-AP *defense* is L18/Lab-10; attack
  technique stays out of student hands per policy.
- Cloud sandbox: stay within the issued budget; no instances outside the
  provided region; delete resources in §12.

## 8. Student Tasks

1. **Survey:** from `survey.txt`, build the RF table: SSID · channel/band ·
   security (Open/WPA2/WPA3/802.1X indicators) · signal (dBm) · BSSID count.
   Which SSIDs broadcast beyond the lab room (over-coverage), and what does
   that expose?
2. **Coverage-as-control:** propose a coverage map for the fictional Meridian
   office (Lab-05): which zones need coverage, which must not have it (OT
   floor?), and how you'd verify.
3. **VPC build:** in the sandbox, create a VPC with: public subnet (NAT GW),
   private app subnet, private data subnet; route tables per subnet; SGs:
   `sg-web` (443 from world), `sg-app` (8080 from sg-web only), `sg-db` (5432
   from sg-app only); default-deny NACL posture on the data subnet.
4. **Behavioral proof:** attempt (and record) an instance in sg-app reaching
   sg-db on an *unlisted* port — observe the SG's stateful return-traffic
   behavior and the NACL's stateless asymmetry (ephemeral-port return rule
   needed on data-subnet NACL for outbound-initiated flows).
5. **Egress:** restrict data-subnet egress to a short allow-list (patching
   endpoint + DNS); note what breaks and why that's the point.
6. Write-up: RF findings + VPC design decisions + one paragraph mapping
   SG/NACL to the firewall/ACL concepts from Lab-06 (same discipline, new
   enforcement point).

## 9. Expected Observations

- Ambient lab SSIDs: expect the instructor AP (802.1X) + a WPA3 PSK test SSID;
  over-coverage is measurable in dBm at the corridor.
- SG return traffic: stateful — no inbound ephemeral rule needed for
  outbound-initiated flows; NACL: you *must* add ephemeral-range inbound or
  the flow hangs — the classic symptom is "connection starts, never completes".
- Default VPC posture (all-allow SGs) vs your design: the contrast is the
  lesson.

## 10. Analysis Questions

1. Your survey found an Open SSID in the corridor. Which L17 attack classes
   does that enable against *clients*, and what client-side control reduces it?
2. Why is "hide the SSID" not a control (state the beacon/PR behavior), and
   what would you tell an executive who insists?
3. Map SG/NACL to stateful/stateless from L10/L11: where does each model
   *fail* (give one scenario each)?
4. The data-subnet egress allow-list breaks package updates. Design the
   compliant alternative (proxy? mirror? scheduled egress?) and its trade-off.
5. Shared responsibility: which of today's misconfigurations would be
   *customer-side* vs *provider-side*, and why does the boundary matter for
   audit?

## 11. Troubleshooting

- `iw dev` shows no adapter → driver/firmware on the pinned dongle; use the
  spare issued unit; personal adapters are unsupported.
- Scan output empty → regulatory domain mismatch; set country per the sheet.
- NACL blocks everything → check rule *order* (lowest number first) and the
  ephemeral return range (1024–65535 for modern clients).
- NAT GW unreachable → elastic IP attached? route table actually pointing to
  it? (The two-step check.)

## 12. Cleanup Instructions

- **Cloud (mandatory, graded):** delete VPC/subnets/NAT/instances you created;
  screenshot the empty resource list. Budget abuse = policy incident.
- RF: return the adapter; no config changes persist on it.

## 13. Submission Requirements

- RF survey table + coverage proposal (map or table).
- VPC diagram (as-built) + SG/NACL tables.
- Behavioral-proof screenshots (SG stateful vs NACL ephemeral).
- Egress note + write-up + analysis answers (5). Due: start of Week 10 session.

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| RF table | SSIDs/channels/security from real survey data, no invented entries |
| VPC as-built | route tables + SG/NACL tables match the diagram |
| Behavioral proof | the stateful-vs-stateless contrast actually demonstrated |
| Cleanup | empty-resource screenshot attached |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | survey numbers real; screenshots annotated; cleanup proven |
| Mechanism accuracy | 30% | SG/NACL semantics + RF vocabulary correct |
| Analysis depth | 20% | coverage-as-control + shared-responsibility reasoning |
| Safety & policy | 10% | passive-only RF; budget respected |

## 16. Instructor Answer Key

Survey exemplar, VPC reference build, grading notes:
`the instructor answer-key collection (not published)` (instructor-only).
