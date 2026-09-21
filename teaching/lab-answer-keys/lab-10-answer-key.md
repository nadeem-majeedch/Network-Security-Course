---
lab: Lab-10
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-10 (WPA-Enterprise Build + Cloud Flow Logs)

## Enterprise build reference (grading anchor)
- Certs: client EKU `clientAuth`, issued from Lab-07's issuing CA; RADIUS
  trusts the CA; per-user identity = cert subject.
- FreeRADIUS: EAP-TLS enabled; Access-Accept with dynamic VLAN 30 for the
  test user; AP passes Tunnel-Private-Group-Id.
- Verification pair (the graded core): Accept (dynamic VLAN visible) +
  Reject-after-revocation — both transcripts required. PSK cannot produce the
  Reject-without-rotating-everyone story; students must articulate that in the
  migration rationale.
- Client-side capture of own association: EAP identity, TLS tunnel, 4-way
  handshake — annotate which frames carry *user identity* (PSK handshakes
  carry none).

## Flow-log expected summary (sandbox run)
After the provided curl loop + ambient: top talker = the curl instance;
protocol mix dominated by 443; rejected flows visible because SG log-only
rules were enabled (Lab-09's sg-db posture); delivery lag ~10 min acknowledged
in the table header. Anomaly hypothesis: students flag the curl loop's
periodicity — graded on *hypothesis labeling* + next-evidence step (packet
sample at the instance, not flow-only conviction).

## Analysis-question model answers
1. **EAP-TLS vs offline attacks:** PSK: attacker captures 4-way, guesses
   offline against the shared secret; EAP-TLS: no password-equivalent on the
   wire — attacker needs the *private key* (or a CA-signed cert), which is
   not guessable.
2. **Server-cert validation disabled:** evil-twin AP with any cert succeeds →
   credential/identity theft; the top real-world deployment gap (corporate
   supplicant profiles must pin the CA).
3. **Periodic one-way DNS:** next evidence = full packet sample on the path or
   resolver logs; flow-only says "periodic, one-way, small" — never "C2".
4. **MAB posture:** quarantine/restricted VLAN + inventory + profile; too-
   broad MAB = anything unmanaged is trusted-ish — the silent flat-network
   regression.
5. **Retention trade:** 30 d bounds long-dwell investigations and seasonal
   baselines; incident forensics older than retention are gone — pair with
   longer-lived aggregates (top-N daily summaries) as the compromise.

## Grading notes
- Accept+Reject transcripts are non-negotiable evidence; one without the other
  halves the mechanism dimension.
- WIPS posture note: classification without containment actions (legality);
  containment *recommendations* with authorization framing are fine.
- Cloud cleanup proof again mandatory; slot discipline noted per team.
- ⚠️ AP/RADIUS/sandbox steps are environment steps; ✅ radtest/journalctl
  shapes verified at authoring.

## Command status
✅ radtest/journalctl invocation shapes; ⚠️ AP GUI and cloud console flows.
