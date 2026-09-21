---
artifact-type: slide-resources
status: complete
decks: 36
diagrams: 10
last-updated: presentation-resources session
---

# Slide Resources — Deck ↔ Lecture ↔ Diagram Map

Validation: `docs-meta/validate_slides.py` (S1–S8, exit 0). Rendering:
Marp/Mermaid **untested in this environment** — commands and honest
status in `teaching/slides/README.md`.

## Deck map

| Deck | Lecture anchor | Week | CLOs | Diagrams referenced |
|---|---|---|---|---|
| lecture-01-security-mindset-threat-landscape | L01 | 1 | CLO-1 | 01 |
| lecture-02-protocol-deep-dive-i-lower-layers | L02 | 1 | CLO-1 | 03 |
| lecture-03-protocol-deep-dive-ii-transport-services | L03 | 2 | CLO-1 | 02 |
| lecture-04-applied-packet-analysis-web-protocols | L04 | 2 | CLO-1 | 05 |
| lecture-05-threat-modeling-attacker-anatomy | L05 | 3 | CLO-2 | — |
| lecture-06-layer2-lan-attacks | L06 | 3 | CLO-2 | 03 |
| lecture-07-sniffing-mitm-session-attacks | L07 | 4 | CLO-2 | 03 |
| lecture-08-dos-ddos-infrastructure-abuse | L08 | 4 | CLO-2 | 02 |
| lecture-09-defense-in-depth-segmentation | L09 | 5 | CLO-3 | 01 |
| lecture-10-firewalls-concepts-placement | L10 | 6 | CLO-3, CLO-4 | 04 |
| lecture-11-acls-rulebase-engineering | L11 | 6 | CLO-4 | 04 |
| lecture-12-nat-proxies-egress-nac | L12 | 5 | CLO-3 | 01 |
| lecture-13-cryptographic-foundations | L13 | 7 | CLO-5 | 05 |
| lecture-14-tls-deep-dive | L14 | 7 | CLO-6 | 05 |
| lecture-15-ipsec-legacy-vpn-architecture | L15 | 8 | CLO-7 | 06 |
| lecture-16-modern-vpns-crypto-agility | L16 | 8 | CLO-5, CLO-7 | 06 |
| lecture-17-wireless-fundamentals-threats | L17 | 9 | CLO-8 | — |
| lecture-18-enterprise-wireless-rogue-defense | L18 | 10 | CLO-8 | 01 |
| lecture-19-cloud-networking-vpc-design | L19 | 9 | CLO-13 | 09 |
| lecture-20-cloud-hybrid-assurance | L20 | 10 | CLO-13 | 09 |
| lecture-21-monitoring-foundations | L21 | 11 | CLO-12 | 07 |
| lecture-22-ids-ips-signatures-tuning | L22 | 11 | CLO-9 | 07 |
| lecture-23-zeek-anomaly-detection | L23 | 12 | CLO-9, CLO-12 | 07 |
| lecture-24-vulnerability-management-cycle | L24 | 12 | CLO-10 | 01 |
| lecture-25-ir-lifecycle-preparation | L25 | 13 | CLO-11 | 08 |
| lecture-26-detection-triage-containment | L26 | 13 | CLO-11, CLO-12 | 08 |
| lecture-27-eradication-recovery-lessons-learned | L27 | 14 | CLO-11 | 08 |
| lecture-28-soc-operations-threat-hunting | L28 | 14 | CLO-12 | — |
| lecture-29-forensic-fundamentals | L29 | 15 | CLO-14 | 10 |
| lecture-30-advanced-forensics-reporting | L30 | 15 | CLO-14, CLO-15 | 10 |
| lecture-31-capstone-workshop-ir-simulation | L31 | 16 | CLO-11, CLO-15 | 08 |
| lecture-32-capstone-defense-course-synthesis | L32 | 16 | CLO-14, CLO-15 | — |
| review-midterm (special) | L01–L16 | 8 | CLO-1..7 | 01–05 |
| review-final (special) | L17–L32 | 16 | CLO-8..15 | 06–10 |
| case-studies-showcase (special) | cs-001–100 | orientation | CLO-1..15 | — |

## Shared diagram assets (one diagram, one definition)

| Asset | Type | Used by | Conceptual-only label |
|---|---|---|---|
| diagrams/01-enterprise-segmentation | network architecture | L09, L10, L12, L26 (+ review decks) | ✅ |
| diagrams/02-tcp-handshake-teardown | protocol flow | L03, L04, L08, L21 | ✅ |
| diagrams/03-arp-poisoning-flow | protocol flow (defense) | L02, L06, L07, L26 | ✅ |
| diagrams/04-acl-stateful-flow | firewall control | L10, L11, L12 | ✅ |
| diagrams/05-tls-handshake | protocol flow | L04, L13, L14, L16 | ✅ |
| diagrams/06-vpn-ipsec-wireguard | VPN conceptual | L15, L16, L19 | ✅ |
| diagrams/07-ids-ips-workflow | IDS workflow | L21, L22, L23, L26, L28 | ✅ |
| diagrams/08-ir-lifecycle-workflow | IR workflow | L25, L26, L27, L31, L32 | ✅ |
| diagrams/09-cloud-vpc-controls | cloud architecture | L19, L20, L28 | ✅ |
| diagrams/10-forensic-timeline-sources | forensic workflow | L26, L29, L30 | ✅ |

Every asset carries: Mermaid rendering + ASCII ground truth +
accessibility text description + the "conceptual reference model — not
an exact production configuration" label.

## Speaker-notes architecture

- **Embedded** per deck (`<!-- notes ... -->` per slide): delivery
  guidance, per-section timings summing to the 110-minute block,
  activity debriefs, CS/DS callouts.
- **Canonical per-lecture notes** (`teaching/speaker-notes/`) remain
  the instructor manual layer — decks reference them via the lecture
  anchor; validator S8 verifies the pairing exists.
- Review/showcase decks embed their own facilitation notes.

## Validation summary (actual run)

| Check | Result |
|---|---|
| S1 32 lecture decks mirror canonical numbering | ✅ |
| S2 3 special decks + README | ✅ |
| S3 Marp front matter, objectives/overview, notes, timings, density | ✅ |
| S4 lecture anchors + CLO declarations | ✅ |
| S5 diagram references resolve | ✅ |
| S6 bullet ceiling (≤8/slide) | ✅ |
| S7 diagram accessibility lines | ✅ |
| S8 canonical speaker-notes pairing | ✅ |

First run: 3 findings — special decks lacked a Learning-Objectives
slide by design (review decks serve overview, not new learning); fixed
by adding an explicit Session Overview slide to each and teaching the
validator the deck-type distinction. Honest triage recorded.

## Untested rendering (mission requirement, honestly labeled)

- **Untested:** all Marp/Mermaid rendering (no Node/npm in the authoring
  environment), PPTX/PDF export, Mermaid plugin fidelity.
- **Tested:** deck structure (S1–S8 executable checks), diagram assets'
  internal consistency, anchor/reference resolution against the live
  repository tree.
- First-render smoke test: run L01 to HTML, review Mermaid fidelity,
  then batch. Record results here after the first successful render.
