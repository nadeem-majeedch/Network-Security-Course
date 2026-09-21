---
marp: true
theme: default
paginate: true
lecture: L05
week: 3
clos: [CLO-2]
duration: 110 min teaching
status: complete
artifact-type: slide-deck
speaker-notes: embedded
---

# Threat Modeling & Attacker Anatomy

**Network Security · Lecture 5 · Week 3**

*You can't defend what you haven't modeled.*

<!-- notes: OPEN (2 min). Hook: "Last module, packets confessed. This
module, the attacker introduces themselves properly — with a project
plan." -->

---

## Learning Objectives

1. **Construct** a STRIDE threat model for a two-tier web service
2. **Map** an intrusion narrative to MITRE ATT&CK tactics
3. **Apply** the attack-tree method to quantify attack paths
4. **Differentiate** scripted opportunists from targeted operators
5. **Defend** a prioritized mitigation list from a model

<!-- notes: (1 min) Objectives map to cs-011/cs-012 cases and the
module-2 arc. Objective 5 previews the assignment-1 design discipline. -->

---

## Threat Modeling: The Four Questions

1. What are we building? *(assets + flows)*
2. What can go wrong? *(STRIDE per element)*
3. What are we doing about it? *(controls per threat)*
4. Did we do a good job? *(verification)*

- Shostack's framing — simple enough to actually use

<!-- notes: (5 min) Run the four questions against the cs-001 small
office live. "Did we do a good job" is the question orgs skip — flag
it; the capstone rubric grades it. -->

---

## STRIDE per Network Element

| Threat | Network example |
|---|---|
| **S**poofing | forged ARP/DNS identity |
| **T**ampering | payload modification in transit |
| **R**epudiation | "that wasn't my session" (no logs) |
| **I**nformation disclosure | sniffing, misrouted flows |
| **D**enial of service | floods, resource exhaustion |
| **E**levation of privilege | VLAN hop → server VLAN |

<!-- notes: (6 min) Quiz-7 Q1 tests the STRIDE mapping. Do two examples
deep (spoofing via ARP — L02's mechanics; EoP via VLAN hop — next
lecture) rather than six shallow. -->

---

## Attack Trees: Paths, Not Points

```
 GOAL: read payroll data
 ├── OR: compromise server directly
 │    ├── exploit unpatched service (needs: reachability)
 │    └── steal admin creds (needs: phishing path)
 ├── OR: intercept traffic
 │    ├── ARP poison user VLAN (needs: LAN access)
 │    └── compromise DNS (needs: resolver access)
 └── OR: insider copy (needs: access + motive)
```

- Interior nodes = prerequisites; OR branches = alternative paths
- Counting cheapest paths = prioritization input

<!-- notes: (6 min) Build one branch live from student answers. The
"needs:" annotations are quantitative hooks — each prerequisite is a
control opportunity. cs-011 is the full case. -->

---

## MITRE ATT&CK: The Attacker's Taxonomy

- Tactics = the *why* (Initial Access → Lateral Movement → Exfiltration)
- Techniques = the *how* (T1557 Adversary-in-the-Middle, T1071 App-Layer
  Protocol)
- Mapping narratives to tactics = shared language for defense planning

<!-- notes: (5 min) Show the cs-012 intrusion narrative mapped: phish →
valid account → lateral → staging → exfil. Teach tactic fluency, not
technique memorization. The SOC modules reuse this vocabulary. -->

---

## The Intrusion Narrative (Composite, Simulated)

```
 09:12 phish click ─ 09:40 session theft ─ 10:20 SaaS access
 ─ 11:05 anomaly alert ─ 11:40 containment ─ day 1: token hunt
```

- Every stage = one tactic + one technique + one control opportunity
- The narrative *is* the threat model's test set

<!-- notes: (4 min) This is cs-100's story compressed — deliberately.
"Where would *your* controls have broken this chain?" — rhetorical now,
answered in modules 3–7. -->

---

## Opportunist vs Targeted Operator

| Dimension | Opportunist | Targeted |
|---|---|---|
| Scope | anyone vulnerable | *this* org specifically |
| Effort | automated, cheap | manual, patient |
| Dwell | days | weeks–months |
| Indicator | loud, commodity IOCs | quiet, living-off-network |

- Defense design differs: commodity controls vs detection depth

<!-- notes: (5 min) The distinction drives architecture: opportunists
die to patching + MFA; targeted operators die to detection + response.
The Meridian capstone arc (cs-091+) is a targeted-operator story. -->

---

## Kill Chain → Courses of Action

- Recon → Weaponize → Deliver → Exploit → Install → C2 → Actions
- Each stage = a break point; **earliest break wins cheapest**
- Delivery (email/web) and C2 (egress) are the classic break points

<!-- notes: (4 min) Map kill-chain stages to controls students will
meet: mail filtering, egress allow-lists, MFA. "Earliest break" is the
assignment-1 prioritization argument in miniature. -->

---

## CS/DS Example: The Notebook Supply Chain

- Model: DS workstation → package mirror → GPU cluster
- STRIDE on the mirror: S (fake mirror), T (tampered wheel), I (source
  leak)
- Control: signed packages + pinned index + egress allow-list

<!-- notes: (4 min) DS tie-in per course standard: the package mirror is
the module-2 threat that becomes module-4's signing lecture. The chain
threat-model → control-pick is the assignment-2 skeleton. -->

---

## Activity: Model This Service (7 min)

Two-tier app: nginx front (internet) → PostgreSQL back (internal).
STRIDE one threat per element; pick the two you'd fix first and why.

<!-- notes: (7 min incl. debrief) Pairs. Expected: S/I on nginx (TLS,
WAF), E/I on the DB (segmentation, credentials). The "fix first"
argument must cite path-cost — the attack-tree logic. -->

---

## Case Study: cs-011 (5 min)

- Attack tree for the two-tier web app — quantify the cheapest path

<!-- notes: (5 min) Classroom protocol. Push on the "needs:" chain —
every prerequisite is a control. -->

---

## Formative Check

- Oral: one STRIDE threat per protocol you met in module 1.

<!-- notes: (2 min) Rapid oral round — cements module 1 → 2 continuity. -->

---

## References & Next

- Shostack, *Threat Modeling*; MITRE ATT&CK framework (cite as
  methodology reference)
- Diagrams: none new — cs-011's tree is the visual
- **Next (L06):** Layer-2 attacks — where the trust claims get abused
