# Lab-07 — Lab PKI, TLS Configuration Audit

## 1. Lab Overview & CLO Mapping

You will stand up a two-tier mini-PKI (offline root + issuing CA) for the lab
range, issue a server certificate, configure a TLS service, then audit three
supplied TLS endpoints for the failure classes from L14 (chain errors, weak
versions/ciphers, expired/self-signed, hostname mismatch). This is the graded
**Lab Pract-2**. *CLO-6* — analyze TLS behavior and detect/remediate
misconfigurations. Reference lectures: L13 (crypto foundations), L14 (TLS deep
dive).

## 2. Learning Objectives

By the end you can: (1) generate keys/CSRs and run a two-tier CA with correct
extensions (BasicConstraints, KeyUsage, SAN); (2) deploy a certificate chain
and verify it end-to-end; (3) enumerate and interpret a TLS configuration
(protocol versions, cipher suites, cert chain) with openssl; (4) classify
audit findings by severity *with* the mechanism that makes each exploitable;
(5) explain why the E-A-I mapping (L13) tells you what each fix actually fixes.

## 3. Prerequisites

Lab-06 submitted; L13/L14 attended; comfort with the CLI.

## 4. Estimated Duration

120 minutes: CA build 35 · service TLS 20 · audits 40 · write-up 25.

## 5. Required Software & Hardware

- Lab-range VM with OpenSSL ≥ 3.0 (pinned), a supplied lab web service
  (`tlslab` on the range, three configured endpoints: good/bad/ugly).
- Text editor; no internet access needed or used.

## 6. Setup Instructions

> **Command status:** ✅ = executed at authoring time (OpenSSL 3.x syntax
> verified); ⚠️ = range-step, reference shape.

1. ⚠️ Work in `~/lab07-ca/` on the range VM.
2. ✅ Root CA (offline-style; keep this key ceremonial — never on the web tier):

```bash
openssl genrsa -out root-ca.key 4096
openssl req -x509 -new -key root-ca.key -sha256 -days 3650 \
  -subj "/C=US/O=NS401 Lab/CN=NS401 Lab Root CA" -out root-ca.crt
```

3. ✅ Issuing CA + server key/CSR with SAN:

```bash
openssl genrsa -out issuing-ca.key 4096
openssl req -new -key issuing-ca.key \
  -subj "/C=US/O=NS401 Lab/CN=NS401 Lab Issuing CA" -out issuing-ca.csr
openssl genrsa -out server.key 2048
openssl req -new -key server.key \
  -subj "/C=US/O=NS401 Lab/CN=lab-range.local" -out server.csr
```

4. ✅ Sign with extensions (edit the two `keyUsage`/`basicConstraints` lines to
   match CA vs server per the extension card on the lab sheet), then verify the
   chain and the SAN:

```bash
openssl x509 -req -in issuing-ca.csr -CA root-ca.crt -CAkey root-ca.key \
  -days 1825 -sha256 -out issuing-ca.crt \
  -extfile <(printf "basicConstraints=critical,CA:TRUE,pathlen:0\nkeyUsage=critical,keyCertSign,cRLSign")
openssl x509 -req -in server.csr -CA issuing-ca.crt -CAkey issuing-ca.key \
  -days 365 -sha256 -out server.crt \
  -extfile <(printf "subjectAltName=DNS:lab-range.local\nbasicConstraints=critical,CA:FALSE\nkeyUsage=critical,digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth")
openssl verify -CAfile root-ca.crt -untrusted issuing-ca.crt server.crt   # ✅ prints OK
openssl x509 -in server.crt -noout -text | grep -A1 "Subject Alternative" # ✅ shows DNS:lab-range.local
```

5. ⚠️ Deploy `server.crt + issuing-ca.crt` (chain order matters) to the `tlslab`
   service per the sheet; browse `https://lab-range.local` from a range client
   (trust your root in the client store *for this lab only*).

## 7. Authorization & Safety Notes

- **Authorization basis:** all PKI work is lab-scope only — confined to the instructor-authorized lab range and issued keys; anything outside that boundary is prohibited.

- All PKI work is lab-scope; private keys generated here are lab throwaways —
  never reuse course keys elsewhere (and never paste them into submissions).
- The "bad/ugly" endpoints are instructor-configured for auditing; do not
  modify other students' services.

## 8. Student Tasks

1. **Deploy & verify:** serve the full chain; from a range client run
   `openssl s_client -connect lab-range.local:443 -servername lab-range.local`
   (⚠️ shape) and capture: chain order, verify return code, negotiated version
   and cipher.
2. **Audit three endpoints** (`good`, `bad`, `ugly` hostnames on the sheet).
   For each: protocol versions offered, cert chain validity, SAN match,
   key size, notable suites. Record evidence lines from your probes.
3. **Classify findings:** for every defect, name the failure class
   (chain/trust, version, suite, identity, lifetime) and the *mechanism* of
   harm (what attack it enables — e.g., downgrade exposure, MITM with
   unvalidated chain, E-A-I consequences).
4. **Remediation plan:** per finding, the config-level fix and how you would
   verify the fix (the test you'd re-run).
5. **E-A-I precision:** for your working service, state which component
   provides encryption, authentication, integrity — and where *authorization*
   lives (hint: not in TLS).

## 9. Expected Observations

- Chain order in `s_client` output: server → issuing → root; `Verify return
  code: 0 (ok)` when the client trusts the root.
- `bad` endpoint: expired or self-signed leaf (read the validity/issuer lines).
- `ugly` endpoint: offers TLS 1.0/1.1 suites (AES-CBC/SHA1 family) — negotiation
  proves it if your client allows; use `-tls1_2` probes to bound versions.
- Missing SAN entry → hostname-mismatch class even when the chain is valid.

## 10. Analysis Questions

1. Why is the root key kept offline while the issuing CA signs daily? What does
   pathlen:0 on the issuing cert prevent?
2. TLS 1.3 encrypts the certificate message. What does that change for passive
   observers *and* for your audit workflow (which fields moved, which remain)?
3. Forward secrecy: which of your negotiated suites have it, and what event
   would a non-FS suite make catastrophic?
4. A colleague "fixes" a hostname-mismatch warning by disabling validation in
   the client. Using E-A-I vocabulary, what did they actually break, and what
   attack is now possible?
5. What would Certificate Transparency have (and not have) caught in your
   `bad`/`ugly` findings?

## 11. Troubleshooting

- `openssl verify` fails with "unable to get local issuer" → you served/verified
  leaf-only; supply `-untrusted issuing-ca.crt` (or concatenate the chain).
- Browser still warns → you didn't import the *root* into the client trust
  store, or SAN lacks the exact hostname you typed.
- Extension file errors → the `<(...)` process-substitution needs bash; use
  `bash` not `sh`, or write the extfile to disk first.
- s_client shows TLS 1.3 only → that's the server's config; probe
  `-tls1_2`/`-tls1` to bound what's *offered*.

## 12. Cleanup Instructions

- Archive `~/lab07-ca/` to your course folder (keys included — they stay in the
  instructor-only submission channel if required); otherwise shred keys:
  ⚠️ `rm -P` (FreeBSD) / `shred -u` (GNU) or delete — lab keys are throwaways;
  state which you did.
- Remove your root from the client trust store (this lab's temporary trust).

## 13. Submission Requirements

- Chain-verification transcript (verify + s_client excerpts).
- Audit table for 3 endpoints: finding · class · mechanism of harm · evidence.
- Remediation plan with re-test commands.
- E-A-I mapping for your service (one paragraph).
- Analysis answers (5). Due: end of session (Pract-2 grading).

## 14. Expected Output & Evidence

| Artifact | Passing evidence |
|---|---|
| PKI artifacts | working chain: verify OK; SAN present; extensions correct |
| Audit table | every finding cites probe output lines |
| E-A-I paragraph | encryption≠authentication≠authorization named correctly |
| Remediation | fixes testable (re-run command stated) |

## 15. Grading Rubric

| Criterion | Weight | Full-credit behavior |
|---|---|---|
| Evidence discipline | 40% | probe transcripts attached; findings cite lines |
| Mechanism accuracy | 30% | TLS mechanics + E-A-I distinctions correct |
| Analysis depth | 20% | FS/CT/1.3 nuance (Q2/Q3/Q5) |
| Safety & policy | 10% | lab-scope keys; trust-store hygiene restored |

## 16. Instructor Answer Key

Endpoint audit answer key, extension card, grading notes:
`the instructor answer-key collection (not published)` (instructor-only).
