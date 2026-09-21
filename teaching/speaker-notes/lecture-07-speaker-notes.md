---
lecture: L07
module: 2
week: 4
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L07 Speaker Notes — Sniffing, MITM & Session Attacks

## Delivery Guide
Position is everything: sniffing needs on-link, MITM needs on-path — the L01
vantage map pays off here. The two-frame stripping story (302 rewrite → cleartext
POST) is the demo students remember; play it, then let them find the second frame.
Keep cookie-flag treatment concrete (five headers, five verdicts). Close the
Module-4 bridge explicitly: "you cannot prevent position theft — you make it
useless; that's L13–L14."

## Timing Plan
0–10 vantage-ladder recap · 10–35 sniffing + MITM patterns (capture playback) ·
35–55 sessions/tokens (cookie-flag demo) · 55–65 break · 65–75 detection-evidence
table (build together) · 75–110 MITM forensics workshop · 110–120 exit ticket +
Quiz-2 reminder. **Compression:** drop one workshop artifact (keep the strip
capture); the table stays.

## Teaching Demonstrations
1. Strip-attempt capture: 302 with `Location: http://…` then the POST — annotate both frames.
2. Cookie-flag verdicts: five set-cookie headers on slides; class votes per flag.
3. Duplicate-session log: same `sessid` from two IPs/UAs in four minutes — the sidejacking shape.

## Expected Student Difficulties
1. "HTTPS everywhere solves it" — first-visit exposure + user-clicks-through warnings persist; the HSTS timeline makes it visual.
2. Cookie flags feel like app-dev trivia — reframe: they decide whether a *network* theft is useful.
3. Evidence vs accusation: two device fingerprints ≠ theft (shared workstation!) — teach the discriminator questions.

## Discussion Facilitation
Q5 (enterprise root CA vs user CAs) is a governance discussion: steer to trust-store
scope, revocation, and audit rather than absolutism. In the red-team pass, your
innocent explanations must be *plausible* (dev redirects, labs) — that's what makes
the defense exercise real.

## Lab Troubleshooting (forensics-workshop context)
- Proxy-log timestamps misaligned: the prepared set is pre-normalized; if students use raw files, apply the offset table first.
- Strip capture unclear on small screens: distribute the two annotated frames as text.

## Accessibility Notes
- Frame evidence: always accompanied by textual transcription.
- The evidence table: distribute digitally before class for note-taking users.

## CS & Data Science Applications
- **CS:** TLS transcript authentication explains why injection fails — connect to their crypto-course intuition; session tokens map to their web-app coursework.
- **DS:** duplicate-session detection = entity-resolution across logs (same token, different context) — name it; it's a DS technique they own.

## Links
Plan: `modules/module-02-network-threats/lectures/lecture-07-sniffing-mitm-session-attacks.md` · Student page: `docs/lectures/lecture-07-sniffing-mitm-session-attacks.md` · Answers: `teaching/answer-keys/answer-key-module-02.md`
