---
diagram: 02-tcp-handshake-teardown
type: protocol-flow
used-by: [L03, L04, L08, L21]
status: complete
---

# Diagram — TCP Handshake, Data Transfer, and Teardown

> Sequence per RFC 793/9293 semantics; simplified for teaching.

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    Note over C,S: Three-way handshake (establishes ISNs, windows)
    C->>S: SYN, seq=x
    S->>C: SYN+ACK, seq=y, ack=x+1
    C->>S: ACK, ack=y+1
    Note over C,S: Data transfer (ACKs carry byte ranges; window = flow control)
    C->>S: [PSH,ACK] data
    S->>C: [ACK] window update
    Note over C,S: Cooperative close (FIN exchange) vs abort (RST)
    C->>S: FIN
    S->>C: ACK
    S->>C: FIN
    C->>S: ACK
```

ASCII ground truth:

```
 CLIENT                          SERVER
   │  SYN seq=x ─────────────────►│   (listen: socket open)
   │◄───────────── SYN+ACK seq=y  │
   │  ACK ───────────────────────►│   ← ESTABLISHED (both sides)
   │  [PSH,ACK] data ────────────►│
   │◄───────────── [ACK] win+ ────│   (window = receiver's buffer)
   │  FIN ───────────────────────►│   cooperative close (4-way)
   │◄───────────── ACK ───────────│
   │◄───────────── FIN ───────────│
   │  ACK ───────────────────────►│   ← CLOSED

 Abnormal: RST = abort NOW (no listening port, or hostile reset).
 Scan signature: SYN→RST/ACK means "port closed, host alive".
```

**Text description (accessibility):** the client opens with a SYN, the
server answers SYN-ACK, the client acknowledges — connection established.
Data flows with cumulative ACKs and a receiver-advertised window. A clean
close is a four-way FIN exchange; a RST aborts immediately. In security
terms: unanswered SYNs suggest filtering or a flood; RST to unrequested
ports is the signature scanners look for.
