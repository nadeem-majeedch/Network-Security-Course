---
lecture: L17
module: 5
week: 9
status: complete
artifact-type: speaker-notes
instructor-only: true
---

# L17 Speaker Notes — Wireless Fundamentals & Threats

## Delivery Guide
Module 5 opens with the safety framing verbatim (authorized lab APs only; capture
of non-course networks out of scope). The 4-way handshake correction — "the
password never crosses the air" — is the misconception centerpiece; the EAPOL
playback makes it stick. The evolution table (WEP→WPA3) is taught *by break*: each
row exists because something failed. The survey-capture read (RSN IE, PMF) is the
hands-on skill Lab-09 uses.

## Timing Plan
0–10 spectrum warm-up (channel overlap plot) · 10–35 frames + handshake (EAPOL
playback) · 35–55 evolution table · 55–65 break · 65–85 threat classes + PMF ·
85–110 survey characterization · 110–120 exit ticket + L19 trailer. 
**Compression:** spectrum warm-up to 5 min; the survey read stays full-length.

## Teaching Demonstrations
1. EAPOL 4-way playback (prepared capture): annotate the four frames; ask what's secret (nothing — that's the point).
2. RSN-IE read: two beacons side by side (WPA2-CCMP vs legacy TKIP profile) — the camera SSID finding appears on screen.
3. Rogue-candidate exhibit: same SSID, two BSSIDs, mismatched security IEs — the detection seed for L18.

## Expected Student Difficulties
1. "Hidden SSIDs are secure" — probes still leak; hiding breaks clients (mention zero-len probe behavior).
2. Handshake capture = credentials confusion — it's an offline *guessing oracle*; the distinction matters ethically and technically.
3. MAC-randomization policy surprises — DHCP reservations and allowlists break; 802.1X (L18) is the answer.

## Discussion Facilitation
Q2 (transition-mode downgrade): the phased-migration answer (per-building, PMF-on,
monitor) is the design thinking Quiz-4 will sample. Q5 (why not all-Enterprise):
elicit the real blockers — PKI logistics, IoT fleets, cost — not "it's hard."

## Lab Troubleshooting (survey context)
- Monitor mode fails on student adapters: use the range's pre-configured adapters; chipset notes in the lab sheet.
- Capture empty: wrong channel — survey tools hop; set fixed channel for the target AP.
- Beacon filter misses frames: `wlan.fc.type_subtype == 8` exactness check.

## Accessibility Notes
- Spectrum plots: verbal description of overlap/congestion; text table alternative.
- Beacon field reads: screen-reader-friendly field lists distributed.

## CS & Data Science Applications
- **CS:** 802.11 management frames are control-plane messages without auth — parallels to unauthenticated control APIs in their systems courses.
- **DS:** survey captures are labeled datasets (per-BSSID features: cipher, PMF, clients) — classification of rogue candidates is a genuine DS mini-task; offer as stretch.

## Links
Plan: `modules/module-05-wireless-cloud/lectures/lecture-17-wireless-fundamentals-threats.md` · Student page: `docs/lectures/lecture-17-wireless-fundamentals-threats.md` · Answers: `teaching/answer-keys/answer-key-module-05.md`
