---
lecture: L18
module: 5
week: 10
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L18 Speaker Notes — Enterprise Wireless & Rogue Defense

## Delivery Guide
The SAE-vs-Enterprise precision point (WPA3-Enterprise uses 802.1X; SAE is Personal)
is the quiz-bait moment — say it twice. The evil-twin-with-EAP-TLS story ("the fake
AP fails visibly") is the lecture's payoff: it converts L07's phishing narrative
into a cryptographic defense. The wired-side correlation demo (BSSID + switch port)
is the killer evidence pattern — stage it carefully. Quiz 4 runs at session end
(10 min, per calendar); Pract-3 is the wireless build.

## Timing Plan
0–10 recap (L17 survey findings) · 10–35 802.1X + EAP methods · 35–55 WPA3-Ent +
deployment design · 55–65 break · 65–90 rogue program + wired-correlation demo ·
90–110 enterprise build + rogue hunt · 110–120 exit ticket + **Quiz 4**. 
**Compression:** roaming (11r/k/v) to one slide; the correlation demo and build
window are the graded spine.

## Teaching Demonstrations
1. RADIUS Accept anatomy: the attribute lines (VLAN 10) — identity-driven policy made visible.
2. Supplicant profile walkthrough: the EAP-TLS config fragment; what each line defends against.
3. Wired-side correlation: range AP bridging the LAN — new MAC on port 24 + BSSID pairing in the same window.

## Expected Student Difficulties
1. SAE/Enterprise conflation — the precision slide + the quiz tag.
2. PEAP feels safe — the fake-portal-before-TLS story is the eye-opener; client validation is the defense.
3. Containment eagerness — governance/RF-legal review before deauth authority; policy before power.

## Discussion Facilitation
Q1 (why PEAP still phishes): the strongest answers place the attack *before* the
tunnel starts. Q4 (containment authority): require the policy artifact, not the
opinion — "who signs the deauth order?"

## Lab Troubleshooting (build + hunt context)
- EAP-TLS supplicant fails: client cert expired or CA not imported — checklist order: cert → CA → identity.
- RADIUS rejects: shared-secret mismatch between AP and RADIUS — compare both configs.
- Planted rogue not found: students scanning wrong band — the rogue is on the documented channel.

## Accessibility Notes
- Supplicant configs: text files distributed; GUI paths described.
- Survey hunts: pair-based (visual RSSI work shared); textual evidence required so non-visual contributors participate fully.

## CS & Data Science Applications
- **CS:** RADIUS attributes are policy-as-data — attribute-driven enforcement maps to their configuration-management instincts.
- **DS:** rogue classification from survey features is the second labeled-classification mini-task this module (L17 + L18 pair nicely as a DS stretch assignment).

## Links
Plan: `modules/module-05-wireless-cloud/lectures/lecture-18-enterprise-wireless-rogue-defense.md` · Student page: `docs/lectures/lecture-18-enterprise-wireless-rogue-defense.md` · Answers: `teaching/answer-keys/answer-key-module-05.md`
