---
diagram: 03-arp-poisoning-flow
type: protocol-flow
used-by: [L02, L06, L07, L26]
status: complete
---

# Diagram — ARP Poisoning Flow & DAI Defense

> Attack mechanics shown **conceptually for defense teaching**; no tool
> names or commands. Pair with cs-003/cs-013 evidence analysis.

```mermaid
sequenceDiagram
    participant A as Attacker host
    participant V as Victim PC
    participant G as Gateway
    Note over A,G: Normal state: V↔G via correct MACs
    A->>V: Unsolicited ARP reply: "gateway IP is at attacker-MAC"
    A->>G: Unsolicited ARP reply: "victim IP is at attacker-MAC"
    Note over A,G: V and G now both route through A (if A forwards = MITM)
    V->>A: Traffic meant for gateway
    A->>G: Forwards (copying payloads)
    G->>A: Replies
    A->>V: Forwards back
```

Defense sequence (the same wires, defended):

```
 SWITCH with Dynamic ARP Inspection
   ├─ DHCP snooping builds IP↔MAC binding table (trusted ports only)
   ├─ ARP replies on UNTRUSTED ports checked against bindings
   ├─ mismatch → frame DROPPED + logged (the attack above dies here)
   └─ no binding → drop (no exceptions without static entries)
```

ASCII ground truth (the poisoning):

```
  VICTIM                ATTACKER               GATEWAY
    │  fake ARP:          │                       │
    │ "GW is at ATK-MAC"  │                       │
    │◄────────────────────│   fake ARP:           │
    │                     │ "VICTIM is at ATK-MAC"│
    │                     ├──────────────────────►│
    │═══ V→GW traffic ═══►│═══ forwarded ════════►│   (payloads copied)
    │◄═══ GW→V traffic ═══│◄═══ forwarded ════════│
```

**Text description (accessibility):** the attacker sends unsolicited ARP
replies to both the victim and the gateway, each claiming the other's
address lives at the attacker's MAC. Both hosts update their ARP caches,
so their traffic flows through the attacker, who forwards it to stay
undetected. The switch's Dynamic ARP Inspection defeats this by
validating every ARP reply against the DHCP-snooping binding table and
dropping mismatches.
