---
diagram: 05-tls-handshake
type: protocol-flow
used-by: [L14, L16, L20]
status: complete
---

# Diagram — TLS 1.2 vs TLS 1.3 Handshake

> Simplified property view; certificate-chain validation applies to both.

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    Note over C,S: TLS 1.2 — two round trips before data
    C->>S: ClientHello (ciphers, random)
    S->>C: ServerHello + Certificate + ServerKeyExchange
    C->>S: ClientKeyExchange, ChangeCipherSpec, Finished
    S->>C: ChangeCipherSpec, Finished
    Note over C,S: TLS 1.3 — one round trip; key share in first flight
    C->>S: ClientHello + key_share
    S->>C: ServerHello + key_share + Certificate + Finished
    C->>S: Finished
    Note over C,S: Both: all records then protected by AEAD (confidentiality + integrity)
```

ASCII ground truth (1.3, the property story):

```
 CLIENT                              SERVER
   │ ClientHello + key_share ────────►│
   │◄── ServerHello + key_share ──────│
   │◄── Certificate (chain) ──────────│   client validates:
   │◄── Finished (AEAD-protected) ────│     • path to trusted root
   │ Finished (AEAD-protected) ──────►│     • hostname (SAN)
   │                                   │     • expiry/revocation
   ├────────── APPLICATION DATA ──────┤   ← AEAD = encryption + integrity
        (1-RTT; 0-RTT exists with replay caveats)
```

**Text description (accessibility):** TLS 1.3 reaches encrypted
application data in one round trip — the client sends its key share
immediately, the server answers with its own plus its certificate chain,
and both finish under AEAD protection, which bundles confidentiality and
integrity into one primitive (why 1.3 has no separate record MAC). The
client's three validation duties — trusted chain, hostname match,
expiry/revocation — are the same failure modes the course's TLS-audit
assignment hunts.
