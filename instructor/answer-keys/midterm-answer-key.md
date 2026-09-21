---
exam: midterm
type: answer-key
instructor-only: true
distribution: never-publish-to-students
clos: [CLO-1, CLO-2, CLO-3, CLO-4, CLO-5, CLO-6, CLO-7]
marks: 100
status: complete
---

# Answer Key & Marking Scheme — Midterm Examination

> **INSTRUCTOR ONLY.** Model answers + marking bands. Verified against
> L01–L16 teaching plans and the course's protocol references.

## Section A — MCQ (2 marks each; 20 total)

| Q | Answer | One-line rationale |
|---|---|---|
| A1 | **B** | L2 forwarding = destination MAC. |
| A2 | **B** | Unauthenticated, unsolicited-accepting protocol. |
| A3 | **B** | CAM overflow → fail-open flooding. |
| A4 | **B** | Top-down first match; implicit deny closes. |
| A5 | **B** | State table matches replies to sessions. |
| A6 | **B** | Keyed = integrity + origin authentication. |
| A7 | **B** | Unbroken unexpired unrevoked path to a trust anchor. |
| A8 | **B** | Tunnel mode encapsulates the whole inner packet. |
| A9 | **B** | TLS 1.3 = client sends key share in first flight. |
| A10 | **B** | Trust toward legitimate DHCP servers only. |

*All answers are B by design — distractors are position-shuffled per
question in live delivery (the bank generator randomizes in the online
version); check the delivered paper before grading.*

## Section B — Short answers (7.5 each; 30 total)

**B1 (7.5).** Threat = actor/event that could harm (ransomware operator);
vulnerability = weakness on the asset (unpatched file server, flat share
permissions); risk = the quantified combination (likelihood × impact of
ransomware reaching that server this quarter). *(2.5 each; same-asset
coherence required for full marks.)*

**B2 (7.5).** Effects: (1) lease starvation — clients get no addresses /
fallback APIPA (no connectivity); (2) malicious options — attacker's DNS/
gateway → redirection and interception. *(2.5 + 2.5)* Prevention:
**DHCP snooping** (untrusted ports' offers dropped; rate-limiting).
*(2.5)*

**B3 (7.5).** Encryption = confidentiality (unreadable without key);
authentication = verifying identity of peer/origin; integrity = detecting
modification. *(2 each = 6)* Signature *beyond HMAC*: **non-repudiation**
— asymmetric signing binds the act to a private key only the signer holds
(anyone verifies with the public key; HMAC's shared secret means either
party could have produced the MAC). *(1.5)*

**B4 (7.5).** Split tunnel on unmanaged devices: the device's other
traffic rides the local untrusted LAN while the corporate session is
active — malware on the laptop, or a hostile local network, bridges into
the corporate path (session theft, lateral movement from the device).
*(4)* Compensating controls: MDM/device attestation before the tunnel
splits, host firewall/EDR on the device, or browser-isolated access
instead of network-level split. *(3.5)*

## Section C — Applied (15 each; 30 total)

### C1 — ACL design (15) — model

```
! 1. SSH from jump host only
permit tcp host 10.99.0.10 10.99.0.0/24 eq 22
! 2. HTTPS monitoring from monitoring subnet only
permit tcp 10.99.5.0/24 10.99.0.0/24 eq 443
! 3. All other management-plane traffic: deny + log
deny   tcp any 10.99.0.0/24 eq 22 log
deny   tcp any 10.99.0.0/24 eq 443 log
! 4. Established returns
permit tcp any 10.99.0.0/24 established
! implicit deny all (closes the list)
```

| Element | Marks |
|---|---|
| Jump-host SSH permit correctly scoped | 3 |
| Monitoring-subnet HTTPS permit correctly scoped | 3 |
| Explicit deny-with-log for both management ports | 4 |
| `established` return rule present | 2 |
| Order argument: permits precede denies (first-match); denies precede any broad permit; implicit deny noted | 3 |

*Pseudocode acceptable; logic errors (src/dst swap) −2 each, capped.*

### C2 — Packet analysis (15) — model

| Behavior | Attack class | Immediate containment | Marks |
|---|---|---|---|
| (i) 3,000 gateway-claiming ARP replies from 3 MACs | ARP cache poisoning (multiple attackers or spoofed sources) | Enable/verify DAI; isolate the three source MACs' ports; flush ARP caches on hosts | 5 |
| (ii) 900 unique-subdomain queries to `update-cdn[random].com` | DNS tunneling / DGA-based C2 | Sinkhole the domain at the resolver; block the domain pattern at proxy/DNS | 5 |
| (iii) 50 SYNs/s from `.66` to gateway:445 | Internal SMB scanning/staging toward the gateway | Rate-limit or block `.66` east-west; EDR-check the host | 4 |
| Preventing (i): **Dynamic ARP Inspection** (with DHCP snooping bindings) | — | — | 1 |

*Full marks require connecting `.66` across (ii)+(iii) — the same host
exhibits C2 and staging; top students state that correlation.*

## Section D — Scenario design (20; choose one)

### D1 — Hospital segmentation (20)

| Element | Marks |
|---|---|
| ≥5 sensible zones (patient records / workstations / guest / medical IoT / BMS / mgmt) | 6 |
| 5 critical flow-matrix rows (workstation→records; IoT→vendor cloud **or** brokered; guest→internet-only; mgmt→all (restricted); records→backup) | 5 |
| Patient-care phasing: observe-first (flows before enforcement); IoT zone enforced *last* with fallback (device safety > security policy) | 5 |
| Vendor-cloud path for IoT/BMS handled explicitly (brokered/allow-listed, not ignored) | 4 |

*Patient-safety over-security framing distinguishes the top band —
"IoT devices must never lose function due to segmentation" arguments
(with compensating monitoring) are the expected maturity.*

### D2 — Secure access migration (20)

| Element | Marks |
|---|---|
| MFA per class (phishing-resistant for admins/privileged; app-based for staff; no SMS) | 5 |
| Tunnel policy per class with unmanaged-device reasoning | 5 |
| Certificate lifecycle: internal CA or managed PKI, automated issuance/rotation, monitored expiry (the assignment-2 lesson) | 5 |
| Migration sequencing (pilot → staff waves → decommission password path) | 5 |

## Band descriptors (per section)

- **First:** correct mechanism vocabulary + the *why*; states assumptions;
  connects behaviors across sub-questions (C2's `.66` correlation).
- **Pass:** mechanisms named but unconnected; minor scoping errors in ACL.
- **Fail:** threat/asset confusion; ACL without order logic; treats
  poisoning as availability-only.

## Post-exam calibration note

If Section C1 class average <60%, schedule the ACL remediation clinic
before the final (the final's forensic practical assumes rule-order
fluency). Record actual class statistics here after marking — do not
pre-fill estimates.
