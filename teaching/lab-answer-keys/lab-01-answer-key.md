---
lab: Lab-01
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-01 (Range Orientation, Baseline & Topology)

## Analysis-question model answers
1. **ARP asymmetry:** requests broadcast because the requester doesn't know the
   target MAC; replies unicast once known. Trust assumption: replies are
   accepted *without a request* — enables gratuitous-ARP-style cache poisoning
   (Lab-03/L06). Reward answers naming the trust gap, not just the mechanics.
2. **Trust boundaries:** internet↔range (firewall/egress policy) and
   user↔server nets (segmentation + ACL). Any defensible boundary with a named
   inspection point earns credit; a diagram with no enforcement points caps at
   pass (consistent with manual §2 grading philosophy).
3. **TTL:** low TTL suggests hop distance; OS-guessing from TTL is unreliable
   (overlapping default ranges 64/128/255, configurable, NAT-rewrites absent
   at L3). Full credit names the range overlap explicitly.
4. **30 s vs 2 min:** low-frequency events (DHCP renewals, periodic
   applications) miss short windows — the sampling/coverage trade-off that
   L21 formalizes; reward the "what can't I see" framing.
5. **Boundary:** lab-host list = authorization; exceeding it = policy incident
   under signed rules. Answer must be in the student's own words.

## Expected observations (grading notes)
- Baseline paragraph: require ≥3 *quantitative* anchors (host count, protocol
  mix, broadcast rate) — qualitative-only paragraphs lose the 40% evidence
  dimension.
- Capture: ARP + ICMP + handshake must all be present; frame numbers cited in
  answers, not just "I found them".
- The tooling smoke test (§6.2) doubles as the needs check: students failing
  it get the fixed help session **before L02** — calendar it same week.

## Common failure modes
- Topology drawn from the sheet instead of observed (hosts missing MACs).
- "Trust boundary" used as decoration without a policy sentence.
- Capture file analyzed without verifying SHA256SUMS (evidence-habit miss —
  noted but not fatal here; fatal from Lab-03 onward).

## Command status
✅ `generate_lab_datasets.py` + `sha256sum -c` verified at authoring (Run log:
2026-09-20, 6 datasets, verification OK). ⚠️ VM/tool-version checks are
range steps, untested in the authoring environment.
