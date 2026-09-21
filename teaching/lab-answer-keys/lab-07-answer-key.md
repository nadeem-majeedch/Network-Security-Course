---
lab: Lab-07
status: complete
artifact-type: lab-answer-key
instructor-only: true
distribution: never-publish-to-students
---

# Answer Key — Lab-07 (Lab PKI & TLS Configuration Audit)

## PKI build reference
- Root: RSA-4096, 10 y, `basicConstraints=critical,CA:TRUE` (no pathlen on
  root), `keyUsage=critical,keyCertSign,cRLSign`; kept "offline" (role-played).
- Issuing: RSA-4096, 5 y, `CA:TRUE,pathlen:0` (prevents sub-CAs), keyCertSign.
- Server: RSA-2048, 365 d, SAN `DNS:lab-range.local`,
  `CA:FALSE`, `digitalSignature,keyEncipherment`, EKU `serverAuth`.
- `openssl verify -CAfile root-ca.crt -untrusted issuing-ca.crt server.crt`
  → OK; s_client shows chain order leaf→issuing→root, `Verify return code: 0`.

## Endpoint audit answers (grading anchor)
| Endpoint | Planted defect | Class | Mechanism of harm | Evidence lines |
|---|---|---|---|---|
| good | none (control) | — | — | verify 0, TLS 1.3 suite, SAN match |
| bad | expired leaf (or self-signed; per-semester variant) | chain/trust lifetime | validation fails → users click-through → MITM normalizes | `notAfter` past / issuer==subject |
| ugly | TLS 1.0/1.1 + CBC/SHA1 suites offered; SAN missing alt-name | version/suite + identity | downgrade + legacy-cipher exposure; hostname mismatch trains users to bypass | `-tls1_2` probes accepted at 1.0; suite list; SAN grep |

(Per-semester variants: swap which defect sits on which endpoint — key the
*classes*, and the config export pinned that semester is ground truth.)

## Analysis-question model answers
1. **Offline root:** blast-radius isolation — daily signing key compromise
   doesn't reach the root; `pathlen:0` prevents the issuing CA minting
   sub-CAs (limits delegation depth).
2. **TLS 1.3:** passive observers lose cert/SNI-adjacent visibility (SNI
   itself via ECH only); audit workflow moves to `-servername` probes and
   keylog-based local decode (teaching-only) — fields remaining visible:
   IPs, sizes, timing.
3. **FS suites:** (EC)DHE ephemeral — non-FS (RSA key transport) makes a
   future private-key leak decrypt captured history.
4. **Disabling validation:** breaks *authentication* (server identity), not
   encryption — active MITM with any cert becomes possible; E-A-I precision
   is the graded core (manual model-answers-index §2.4).
5. **CT:** logs mis-issued certs for *public* trust; your lab CA is private —
   CT would not have caught the lab-internal defects (reward the scoping
   honesty).

## Grading notes
- Findings must cite probe output *lines*, not conclusions.
- The E-A-I paragraph: watch for "TLS authorizes the client" — it does not;
  authorization lives app-side.
- Trust-store cleanup: screenshot or statement — the temporary root import is
  a real hygiene habit.
- ⚠️ Range steps (service deploy, s_client against range endpoints) untested
  in authoring env; OpenSSL syntax in §6 verified against 3.x shapes.

## Command status
✅ genrsa/req/x509/verify shapes verified at authoring (OpenSSL 3.x semantics);
✅ SAN grep; ⚠️ s_client against range endpoints is a range step.
