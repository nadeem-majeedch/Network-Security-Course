---
marp: true
theme: default
paginate: true
lecture: L20
week: 10
clos: [CLO-13]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Cloud Networking II — Hybrid & Assurance

**Network Security · Lecture 20 · Week 10**

*Trusting the cloud: verify, log, and govern the API.*

<!-- notes: OPEN (2 min). Hook: "Module 5 ends where the capstone
starts: how do you *assure* a network you don't physically own?" -->

---

## Learning Objectives

1. **Design** hybrid connectivity: VPN/dedicated links, routing hygiene
2. **Govern** identity-plane risks: root, keys, roles
3. **Build** cloud detection: flow logs + audit trail + config
  recording
4. **Respond** to cloud incidents with the cs-065 discipline
5. **State** the shared-responsibility boundary precisely

<!-- notes: (1 min) Objectives 3–4 are the cs-065/assignment-7 arc;
objective 5 is the exam's conceptual framing. -->

---

## Hybrid Connectivity

- Site-to-site VPN (L15's IPsec, cloud-terminated) or dedicated
  circuits
- Route propagation hygiene: no accidental 0.0.0.0/0 leaks
- Asymmetric routing & stateful appliance quirks (the classic hybrid
  pain)

<!-- notes: (5 min) cs-063's overly-permissive-route case is the
failure story: one propagated route exposes an estate. The asymmetric-
routing note keeps the slide honest. -->

---

## The Identity Plane Is the New Perimeter

- Root account: MFA, break-glass only — the crown credential
- IAM users with long-lived keys = the eternal finding (assignment-7's
  F2)
- Roles + short-lived tokens: the direction (L16's per-job pattern)

<!-- notes: (5 min) Assignment-7's findings F1/F2 echo verbatim. The
root-MFA-first remediation argument is graded there. -->

---

## Cloud Detection Stack

| Source | Answers |
|---|---|
| Flow logs | what talked to what, accepted/rejected |
| Audit trail (API) | *who changed what, when* |
| Config recording | what did the estate look like |

- SG/IAM changes as alerts: changes are incidents-in-waiting
  (assignment-7's detection)

<!-- notes: (6 min) The three-source stack is the cloud's version of
L04's correlation triangle. cs-063/assignment-7's detection design
("alert on /0 ingress rules") lives here. -->

---

## Responding in the Cloud

- Attribution first: instance agents/jobs vs destination history
  (cs-065's two-step)
- Containment without touching: NACL/egress constructs, not instance
  surgery
- Preserve: snapshot before reaping — evidence survives

<!-- notes: (6 min) cs-065's case is the full story. The "contain
without touching" pattern (L19) becomes IR practice; the snapshot rule
is forensic continuity (module 8 preview). -->

---

## Shared Responsibility: The Precise Line

- Provider: *of* the cloud — physical, hypervisor, managed-service
  internals
- Customer: *in* the cloud — SG rules, IAM, data, configurations
- "The provider secures it" is the failure phrase in audits

<!-- notes: (5 min) The exam loves this boundary; phrase it with the
of/in distinction. Assignment-7's posture review is the customer-side
of this line. -->

---

## CS/DS Example: Data-Lake Assurance

- Lake access logs + VPC flow logs + IAM audit = the assurance triad
- Anomalous reads (volume/identity/time) = the detection (cs-065's
  shape)

<!-- notes: (3 min) DS framing: the lake is the crown jewel; its
assurance triad is module-8's forensic readiness, cloud edition. -->

---

## Activity: Build the Detection (6 min)

Write the alert logic for: (a) any SG rule granting 0.0.0.0/0 on
22/3389, (b) root-account login, (c) IAM key created for a user.
Threshold + severity each.

<!-- notes: (6 min) All three are page/immediate: (a) config-change
alert, (b) root login = always (it should never happen), (c)
key-creation with review. Assignment-7's visibility task rehearses
this. -->

---

## Case Study: cs-063 (5 min)

- Overly permissive route/NAT exposure — the one-route incident

<!-- notes: (5 min) If used in L19's slot, run cs-064/case-index
rotation here. The route-leak story is hybrid's cautionary tale. -->

---

## Formative Check

- Oral: name the three detection sources and one question each
  answers.

<!-- notes: (2 min) Exit oral — the triad is the takeaway. -->

---

## References & Next

- Provider audit-trail/config documentation (control classes)
- Diagrams: `diagrams/09-cloud-vpc-controls.md`
- **Next (L21):** monitoring foundations — the SOC's senses
