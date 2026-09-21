#!/usr/bin/env python3
"""Generate the Network Security question bank (student + instructor key).

Deterministic, versioned generation so every answer stays verifiable and
the arithmetic (marks, counts, Bloom distribution) is guaranteed correct.
Re-run to regenerate; edit here, never the outputs.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # repo root (script is at assessments/question-bank/)
OUT_STUDENT = ROOT / "assessments" / "question-bank" / "question-bank.md"
OUT_KEY = ROOT / "instructor" / "answer-keys" / "question-bank-answer-key.md"

# Each question: (id, module, clo, difficulty, bloom, marks, stem, mcq or None,
#                 answer, explanation)
# For MCQs: mcq = list of options, answer = letter. For open questions:
# mcq = None, answer = model answer.
Q = []
def q(id, module, clo, diff, bloom, marks, stem, options, answer, expl):
    Q.append(dict(id=id, module=module, clo=clo, diff=diff, bloom=bloom,
                  marks=marks, stem=stem, options=options, answer=answer,
                  expl=expl))

# ---------------- Module 1: Foundations (CLO-1) ----------------
q("QB-001", 1, "CLO-1", "beginner", "Remember", 1,
  "Which OSI layer do TCP ports belong to?",
  ["Layer 2", "Layer 3", "Layer 4", "Layer 7"], "C",
  "Ports are L4 (transport) addressing.")
q("QB-002", 1, "CLO-1", "beginner", "Understand", 1,
  "A host receives an ARP reply for an IP it never queried. This is:",
  ["Normal ARP behavior", "A gratuitous/unsolicited reply — possible poisoning",
   "A DNS error", "A DHCP lease renewal"], "B",
  "Unsolicited replies are the ARP-poisoning vector.")
q("QB-003", 1, "CLO-1", "beginner", "Apply", 2,
  "A packet has TTL=1 arriving at a router one hop from the destination. What happens?",
  ["Delivered", "Dropped, ICMP time exceeded sent", "Fragmented", "Looped"], "B",
  "TTL expires in transit → drop + ICMP Time Exceeded.")
q("QB-004", 1, "CLO-1", "intermediate", "Analyze", 2,
  "Why does ARP only resolve addresses on the local subnet?",
  ["Routers translate ARP", "Broadcasts do not cross routers",
   "ARP requires DNS", "ARP uses multicast only"], "B",
  "ARP is link-local broadcast; routers terminate broadcast domains.")
q("QB-005", 1, "CLO-1", "intermediate", "Analyze", 2,
  "A TCP connection shows SYN, SYN-ACK, then RST. Most consistent interpretation?",
  ["Normal close", "Port open but application reset", "SYN-flood defense triggered on the server",
   "DNS failure"], "C",
  "SYN-ACK proves the port listened; RST then aborts — typical of backlog/reset defense or app failure.")

# ---------------- Module 2: Threats (CLO-2) ----------------
q("QB-006", 2, "CLO-2", "beginner", "Remember", 1,
  "Which attack poisons a switch's MAC address table?",
  ["ARP spoofing", "MAC flooding", "DHCP starvation", "VLAN hopping"], "B",
  "MAC flooding overflows the CAM table.")
q("QB-007", 2, "CLO-2", "beginner", "Understand", 1,
  "The 'amplification' in a reflection DDoS refers to:",
  ["Multiple bots", "Response size exceeding request size",
   "Packet count", "DNS TTL values"], "B",
  "Amplification = reply ≫ request with a spoofed source.")
q("QB-008", 2, "CLO-2", "intermediate", "Analyze", 2,
  "An attacker on a switched LAN wants traffic between host A and the gateway. Best first move?",
  ["MAC flood the switch", "ARP-poison A and the gateway",
   "DHCP starvation", "STP root claim"], "B",
  "ARP poisoning inserts the attacker on the A↔gateway path.")
q("QB-009", 2, "CLO-2", "intermediate", "Evaluate", 2,
  "Which control set best breaks a DHCP-rogue-server attack end to end?",
  ["Port security alone", "DHCP snooping + option-82 filtering on untrusted ports",
   "MAC flooding defense", "BPDU guard"], "B",
  "Snooping designates trusted DHCP sources; untrusted offers are dropped.")
q("QB-010", 2, "CLO-2", "expert", "Evaluate", 2,
  "A DNS-spoofing campaign survives resolver restarts. Why?",
  ["Cache persistence on clients", "Long TTL values set on forged records",
   "Encrypted transport", "Zone transfer abuse"], "B",
  "Forged records with long TTL persist in caches until expiry.")

# ---------------- Module 3: Architecture (CLO-3, CLO-4) ----------------
q("QB-011", 3, "CLO-3", "beginner", "Remember", 1,
  "An implicit deny at the end of an ACL means:",
  ["All traffic is logged", "Unmatched traffic is dropped",
   "The ACL is invalid", "Only TCP is filtered"], "B",
  "Unmatched = denied by default.")
q("QB-012", 3, "CLO-3", "beginner", "Understand", 1,
  "The DMZ's defining property:",
  ["Fastest routing", "A buffer zone exposing only required services to untrusted networks",
   "Wireless coverage", "NAT translation point"], "B",
  "DMZ = exposed-services segment between trust boundaries.")
q("QB-013", 3, "CLO-3", "intermediate", "Apply", 2,
  "Egress filtering on the internal firewall primarily limits:",
  ["Inbound scans", "Compromised hosts calling out / exfiltrating",
   "Broadcast storms", "VPN throughput"], "B",
  "Egress control breaks C2/exfil paths.")
q("QB-014", 3, "CLO-4", "intermediate", "Analyze", 2,
  "Zero trust differs from classic NAC chiefly in:",
  ["Cost", "Continuous per-request authorization vs one-time admission",
   "Wireless support", "Certificate length"], "B",
  "ZT evaluates identity+device+context continuously; NAC admits once.")
q("QB-015", 3, "CLO-4", "expert", "Evaluate", 2,
  "A microsegmentation rollout shows east-west traffic dropping 40% after enforcement. Interpretation?",
  ["Attack stopped", "Shadow flows existed — previously unknown dependencies now blocked; tune or accept",
   "Routing failure", "Denial of service"], "B",
  "Traffic deltas reveal undocumented dependencies — the observe-then-enforce lesson.")

# ---------------- Module 4: Crypto & protocols (CLO-5, CLO-6, CLO-7) ----------------
q("QB-016", 4, "CLO-5", "beginner", "Remember", 1,
  "AES is:",
  ["A hash function", "A symmetric block cipher", "An asymmetric cipher", "A key exchange"], "B",
  "AES = symmetric block cipher standard.")
q("QB-017", 4, "CLO-5", "intermediate", "Analyze", 2,
  "Why combine a hash with a shared secret (HMAC) instead of using the hash alone?",
  ["Faster", "A plain hash can be recomputed by anyone — the key adds origin authentication",
   "Shorter output", "Compression"], "B",
  "Keyed construction = integrity + origin authentication.")
q("QB-018", 4, "CLO-6", "beginner", "Understand", 1,
  "A certificate binds:",
  ["An IP to a MAC", "An identity to a public key (signed by an issuer)",
   "A user to a password", "A port to a process"], "B",
  "Certificates = signed identity↔key bindings.")
q("QB-019", 4, "CLO-6", "intermediate", "Apply", 2,
  "A browser warns 'certificate expired' though the site works. The immediate risk class is:",
  ["Confidentiality of the session", "Authentication/identity assurance (and click-through training)",
   "Routing integrity", "DNS poisoning"], "B",
  "Expiry breaks the identity claim; warnings train users to click through.")
q("QB-020", 4, "CLO-7", "intermediate", "Analyze", 2,
  "Split-tunnel VPN on an unmanaged laptop primarily risks:",
  ["Slower DNS", "The remote untrusted network bridging into the corporate path",
   "Certificate bloat", "MTU blackholes"], "B",
  "Split tunneling leaves the local untrusted LAN in the trust path.")
q("QB-021", 4, "CLO-7", "expert", "Evaluate", 2,
  "In IPsec site-to-site, 'PFS' (perfect forward secrecy) on rekeys protects:",
  ["Against weak pre-shared keys only", "Past session keys if the long-term key later leaks",
   "Against replay", "Header integrity"], "B",
  "PFS: new keys independent of long-term secret → past traffic stays sealed.")

# ---------------- Module 5: Wireless & cloud (CLO-8, CLO-13) ----------------
q("QB-022", 5, "CLO-8", "beginner", "Remember", 1,
  "802.1X wireless authentication's three roles:",
  ["Client, switch, firewall", "Supplicant, authenticator, authentication server",
   "User, AP, DHCP", "Client, CA, DNS"], "B",
  "Supplicant ↔ authenticator ↔ RADIUS/AAA.")
q("QB-023", 5, "CLO-8", "intermediate", "Analyze", 2,
  "Why does WPA3-Personal defeat offline dictionary attacks that work on WPA2-PSK captures?",
  ["Longer keys", "SAE derives keys per handshake — no reusable offline-verifiable material",
   "Stronger radios", "Mandatory certificates"], "B",
  "SAE's per-session derivation removes offline-verifiable handshake data.")
q("QB-024", 5, "CLO-8", "intermediate", "Apply", 2,
  "Rogue-AP/evil-twin detection is the job of:",
  ["Wired IDS", "Wireless IDS/monitoring (RF-side sensing)",
   "Firewall logs", "DHCP logs"], "B",
  "RF-domain threats need RF-side sensors.")
q("QB-025", 5, "CLO-13", "beginner", "Understand", 1,
  "A cloud security group is:",
  ["Stateless subnet filter", "Stateful instance-level allow-only filter",
   "A route policy", "An IAM role"], "B",
  "SG = stateful, instance-attached, allow-only.")
q("QB-026", 5, "CLO-13", "intermediate", "Analyze", 2,
  "VPC flow logs show an instance with a 24-hour periodic 40 MB outbound transfer to a new external IP. First verification step?",
  ["Block the IP", "Attribute: check instance agents/jobs against the destination and history",
   "Reboot the instance", "Open a firewall rule"], "B",
  "Attribution before action (cs-065 discipline).")
q("QB-027", 5, "CLO-13", "expert", "Evaluate", 2,
  "The strongest argument for a VPC egress allow-list over default allow-all:",
  ["Cheaper", "Breaks C2/exfil patterns and forces flows onto logged, approved paths",
   "Faster routing", "Avoids NAT"], "B",
  "Egress default-deny = exfil containment + logged paths.")

# ---------------- Module 6: Detection & vuln mgmt (CLO-9, CLO-10, CLO-12) ----------------
q("QB-028", 6, "CLO-9", "beginner", "Remember", 1,
  "A signature-based IDS misses:",
  ["Known exploits", "Novel/unknown attack patterns", "Encrypted headers", "All UDP"], "B",
  "Signatures match known patterns only.")
q("QB-029", 6, "CLO-9", "intermediate", "Apply", 2,
  "A Zeek log shows one host querying 400 unique high-entropy subdomains in 10 minutes. Best hypothesis:",
  ["Bulk mail", "DNS tunneling/exfiltration", "NTP drift", "ARP scanning"], "B",
  "High-entropy unique subdomain churn = DNS-tunnel signature.")
q("QB-030", 6, "CLO-9", "intermediate", "Analyze", 2,
  "The hidden cost of a 99%-false-positive alert class:",
  ["Storage", "Analyst trust decay — future true positives get ignored",
   "License fees", "Slower CPUs"], "B",
  "Trust erosion compounds beyond raw triage minutes (cs-070).")
q("QB-031", 6, "CLO-10", "beginner", "Understand", 1,
  "Authenticated vulnerability scans outperform unauthenticated chiefly by:",
  ["Speed", "Seeing installed-package truth — fewer false negatives", "Avoiding credentials", "Bypassing firewalls"], "B",
  "In-host state = accurate findings.")
q("QB-032", 6, "CLO-10", "intermediate", "Evaluate", 2,
  "Two CVEs share CVSS 9.8. One sits on an internet-facing payment server; one on an isolated build host. Prioritize:",
  ["Alphabetical", "Payment server first — reachability and asset criticality dominate",
   "Build host first — developers are busier", "Equal"], "B",
  "Environmental scoring: exposure × criticality beats base score alone.")
q("QB-033", 6, "CLO-12", "expert", "Evaluate", 2,
  "A TI feed lists an IP your domain controller just contacted. Before containment:",
  ["Contain immediately", "Corroborate locally (flow/proxy/EDR context) and check indicator provenance/age",
   "Ignore the feed", "Reboot the DC"], "B",
  "Local corroboration + provenance before action (cs-096 hunt discipline).")

# ---------------- Module 7: IR & governance (CLO-11, CLO-14, CLO-15) ----------------
q("QB-034", 7, "CLO-11", "beginner", "Remember", 1,
  "NIST IR lifecycle phases:",
  ["Prevention, patching, audit", "Preparation; detection & analysis; containment, eradication & recovery; post-incident",
   "Scan, patch, report", "Triage, fix, forget"], "B",
  "NIST SP 800-61 phase model.")
q("QB-035", 7, "CLO-11", "intermediate", "Apply", 2,
  "Mass file-renames fire on a file server at 02:00 (EDR, single source). The asymmetry argument says:",
  ["Wait for a second alert", "Contain now — act-wrong costs a reboot, wait-wrong costs the share",
   "Email the CISO and wait", "Reimage immediately"], "B",
  "Error asymmetry justifies acting on single-source when costs are lopsided (cs-082).")
q("QB-036", 7, "CLO-11", "intermediate", "Analyze", 2,
  "Why 'suspend, don't delete' a malicious scheduled task?",
  ["Deletion is impossible", "The artifact is evidence; suspension neutralizes execution",
   "Suspicion is illegal", "Tasks auto-respawn"], "B",
  "Evidence preservation + neutralization in one step.")
q("QB-037", 7, "CLO-14", "intermediate", "Analyze", 2,
  "In a forensic timeline, 'network-attributed, host-unattributed' means:",
  ["The host admitted it", "Network telemetry shows the event; host telemetry for that window is absent",
   "The network is guilty", "Logs were deleted by policy"], "B",
  "Stating the evidence boundary honestly (cs-087).")
q("QB-038", 7, "CLO-14", "expert", "Evaluate", 2,
  "Chain of custody is broken when:",
  ["An image is hashed at acquisition and after transfer", "An image is copied to an analyst's personal USB without records",
   "Evidence is stored encrypted", "Two analysts observe a transfer"], "B",
  "Undocumented custody transfer breaks defensibility.")
q("QB-039", 7, "CLO-15", "expert", "Evaluate", 2,
  "A board report claims 'MTTD improved to 9 days.' The strongest supporting artifact:",
  ["Vendor brochure", "Per-incident detection timestamps across the last N incidents with method notes",
   "A pie chart", "Alert counts"], "B",
  "Outcome metrics need sourced, reproducible provenance (cs-094).")

# ---------------- Cross-module applied questions ----------------
q("QB-040", 3, "CLO-3", "intermediate", "Apply", 3,
  "DESIGN (ACL): Write an ordered 5-rule ACL permitting SSH to subnet 10.5.5.0/24 only from jump host 10.5.5.9, denying other SSH, permitting established returns, logging denies.",
  None,
  "MODEL: (1) permit tcp host 10.5.5.9 10.5.5.0/24 eq 22 — admin path; (2) deny tcp any 10.5.5.0/24 eq 22 log — others; (3) permit tcp any 10.5.5.0/24 established — returns; (implicit deny closes). Order matters: permit precedes deny (first-match); denies precede any broad permits.",
  "First-match ordering + explicit-scope discipline; logging on denies.")
q("QB-041", 1, "CLO-1", "intermediate", "Analyze", 3,
  "PACKET ANALYSIS: A capture shows ARP reply '10.1.1.1 is-at 00:11:22:33:44:01' from MAC 00:11:22:33:44:99 (gateway's real MAC ends :01). Describe the attack, its effect on hosts, and two corroborating artifacts.",
  None,
  "MODEL: ARP spoofing of the gateway. Effect: victims' caches map the gateway IP to the attacker MAC → traffic intercepts (MITM) or drops. Corroboration: DAI switch drops/logs; capture shows unsolicited reply bursts; duplicate IP/MAC flapping in switch logs.",
  "Identify poisoning, state table effect, name two evidence sources.")
q("QB-042", 2, "CLO-2", "advanced", "Analyze", 3,
  "DIAGRAM: A topology shows internet → edge FW → DMZ (web, 10.2.0.10) → inner FW → LAN (10.3.0.0/16). The DMZ host initiates outbound 443 to any destination. Identify the design flaw and redesign the rule.",
  None,
  "MODEL: Flaw — unrestricted DMZ egress turns a compromise into a beaconing/exfil channel. Redesign: DMZ egress allow-list (update repos/CDN by FQDN or IP), deny+log the rest; optionally proxy updates through a controlled path.",
  "Egress discipline on exposed segments.")
q("QB-043", 6, "CLO-9", "advanced", "Analyze", 3,
  "PACKET/FLOW ANALYSIS: Flow records show workstation 10.4.1.57 → external IP on 443 every 60s ±3s, 2 KB each, for 6 hours, outside business hours. Classify, give the detection logic, and the next investigative step.",
  None,
  "MODEL: C2 beacon profile (fixed periodicity, low volume, off-hours). Detection: periodicity + low-byte + repeated-dst logic (e.g., N connections within jitter window). Next step: attribute the host — EDR process review / proxy SNI for the destination (which app made it).",
  "Beacon classification, detection shape, attribution next.")
q("QB-044", 7, "CLO-11", "advanced", "Evaluate", 3,
  "INCIDENT TASK: Ransomware staging suspected (EDR: new service + mass rename on FS01; staging egress 2 MB in proxy). Give the ordered containment with reversibility labels and the evidence-preservation rule.",
  None,
  "MODEL: (1) EDR isolate FS01 — reversible; (2) block staging domain (proxy+DNS) — reversible; (3) suspend new service/task (not delete) — reversible, preserves evidence; (4) then scope (backup generation check, other hosts) before any irreversible rebuild/restore. Preservation: suspend/don't delete; capture task/service definitions first.",
  "Reversibility ordering + preservation discipline (cs-082).")
q("QB-045", 8, "CLO-15", "expert", "Create", 4,
  "CAPSTONE SYNTHESIS: Your capstone estate has MTTD 9 days, EDR 100% of servers, ZT pilots on 2 apps. The board asks: 'why fund phase 3 now?' Compose the 3-sentence case: what it buys, what deferral costs, what evidence backs the trajectory.",
  None,
  "MODEL: (1) Phase 3 extends measured controls (2 apps, 98.5% decision success, ≤7% overhead) to the remaining concentration: branch + privileged access. (2) Deferral keeps location-trust on 12 sites and admin planes for another year while measured dwells run in days. (3) Evidence: phase-gate results, MTTD trend 34→9 days, tabletop findings — the method is proven, not promised.",
  "Board-language synthesis: trend + concentration + method evidence (cs-093/094).")
q("QB-046", 4, "CLO-6", "advanced", "Analyze", 3,
  "DIAGRAM/CONFIG: A certificate chain: root 'Corp-Root' (self-signed, in trust store) → intermediate 'Corp-Issuing' (valid 2024–2034) → leaf 'wiki.lab' (valid, SAN matches). A client still rejects it. Give the three most probable causes ranked.",
  None,
  "MODEL: (1) Intermediate not served/missing on the leaf's chain (client can't build the path — most common); (2) intermediate revoked or its validity window violates client policy; (3) clock skew on the client. (Also acceptable: name constraints on the CA blocking the SAN.)",
  "Chain-building diagnosis, ranked by base rate.")
q("QB-047", 5, "CLO-13", "advanced", "Create", 3,
  "CLOUD DESIGN: Design the NACL + SG division for a 3-tier VPC (web/app/DB) such that a future SG mistake cannot expose the DB to the internet. State rules on both constructs.",
  None,
  "MODEL: NACL on DB subnet: deny inbound 3306 (and all) from 0.0.0.0/0; allow inbound 3306 only from app-subnet CIDR; ephemeral returns out. SG on DB: allow 3306 from app-SG only. Defense in depth: NACL is the backstop — a permissive SG alone cannot override the subnet-level deny.",
  "Layered control division; NACL as SG-mistake backstop.")
q("QB-048", 7, "CLO-14", "advanced", "Analyze", 3,
  "FORENSICS: Host logs (NTP-synced) show an export at 14:10:00. Router flow records show the matching flow at 14:13:30. The router clock is skewed. Derive the offset and state how you'd prove it.",
  None,
  "MODEL: Offset = +3:30 (router ahead of true time). Proof: find a second event visible in both sources (e.g., session end), compute the same offset; or check against an NTP-disciplined reference. A single event pair is a hypothesis; two+ pairs corroborate.",
  "Clock-skew derivation requires corroborating pairs (cs-097).")
q("QB-049", 2, "CLO-2", "advanced", "Create", 3,
  "THREAT MODEL: For a university Wi-Fi with WPA2-PSK shared by 3,000 students, produce the top threat, the compounding factor, and the design fix with its tradeoff.",
  None,
  "MODEL: Top threat: passphrase harvest → offline crack/peer snooping (one secret for all). Compounding: no per-user identity → no accountability, rotation is network-wide. Fix: 802.1X/WPA2-Enterprise with RADIUS; tradeoff: identity infrastructure + device onboarding cost (plus guest network for BYOD convenience).",
  "Shared-secret blast radius → per-user identity (cs-054/059).")
q("QB-050", 8, "CLO-15", "expert", "Create", 4,
  "CAPSTONE SYNTHESIS: In ≤200 words, connect one protocol fact (module 1), one control design (module 3 or 5), one detection (module 6), and one response decision (module 7) into a single coherent defense story for your capstone estate.",
  None,
  "MODEL SHAPE (graded on coherence, not wording): e.g., 'ARP is unauthenticated broadcast (fact) → management VLANs are segmented with DAI (design) → Zeek flags gratuitous-ARP bursts (detection) → the runbook contains by isolating the switch port and rotating the affected credentials, reversible-first (response).' Each link must name its module's mechanism.",
  "Cross-module integration — the course's through-line in one chain.")


BLOOM_ORDER = ["Remember", "Understand", "Apply", "Analyze", "Evaluate", "Create"]

def render_student():
    lines = [
        "---",
        "artifact-type: question-bank",
        "status: complete",
        "questions: %d" % len(Q),
        "instructor-key: instructor/answer-keys/question-bank-answer-key.md",
        "---",
        "",
        "# Question Bank — Network Security (Student Version)",
        "",
        "> Questions only. Validated answers, distractor rationales, and marking",
        "> guidance live in the instructor answer key. Every question carries its",
        "> Bloom level and CLO in the key; CLO/module/difficulty maps are in",
        "> `docs-meta/assessment-coverage.md`.",
        "",
    ]
    cur_module = None
    for item in Q:
        if item["module"] != cur_module:
            cur_module = item["module"]
            lines += ["", "## Module %d Questions" % cur_module, ""]
        lines.append("**%s** (%d mark%s)" % (
            item["id"], item["marks"], "s" if item["marks"] > 1 else ""))
        lines.append("")
        lines.append(item["stem"])
        lines.append("")
        if item["options"]:
            for letter, opt in zip("ABCD", item["options"]):
                lines.append("- **%s.** %s" % (letter, opt))
            lines.append("")
    lines += ["", "## CLO Map (for instructors — students may ignore)", "",
              "| Question | Module | CLO | Difficulty |", "|---|---|---|---|"]
    for item in Q:
        lines.append("| %s | %d | %s | %s |" % (
            item["id"], item["module"], item["clo"], item["diff"]))
    OUT_STUDENT.parent.mkdir(parents=True, exist_ok=True)
    OUT_STUDENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_key():
    lines = [
        "---",
        "artifact-type: answer-key",
        "instructor-only: true",
        "distribution: never-publish-to-students",
        "status: complete",
        "questions: %d" % len(Q),
        "---",
        "",
        "# Question Bank — Instructor Answer Key",
        "",
        "> **INSTRUCTOR ONLY.** Every answer verified against the module teaching",
        "> plans and the linked case/lab evidence. Bloom levels and CLOs per question;",
        "> totals guaranteed by generation script (`assessments/question-bank/generate_question_bank.py`).",
        "",
        "## Summary counts",
        "",
    ]
    from collections import Counter
    bloom = Counter(item["bloom"] for item in Q)
    clos = Counter(item["clo"] for item in Q)
    diffs = Counter(item["diff"] for item in Q)
    marks_total = sum(item["marks"] for item in Q)
    lines.append("- Questions: %d · Total marks: %d" % (len(Q), marks_total))
    lines.append("- Bloom: " + ", ".join("%s %d" % (b, bloom[b]) for b in BLOOM_ORDER if bloom[b]))
    lines.append("- CLO: " + ", ".join("%s %d" % (c, clos[c]) for c in sorted(clos)))
    lines.append("- Difficulty: " + ", ".join("%s %d" % (d, diffs[d]) for d in ["beginner", "intermediate", "advanced", "expert"] if diffs[d]))
    lines += ["", "## Answers & Rationales", ""]
    cur_module = None
    for item in Q:
        if item["module"] != cur_module:
            cur_module = item["module"]
            lines += ["", "### Module %d" % cur_module, ""]
        if item["options"]:
            lines.append("**%s — Answer: %s** (%d mk, %s, %s, %s)" % (
                item["id"], item["answer"], item["marks"], item["bloom"],
                item["clo"], item["diff"]))
            lines.append("")
            lines.append(item["expl"])
        else:
            lines.append("**%s — Model answer** (%d mk, %s, %s, %s)" % (
                item["id"], item["marks"], item["bloom"], item["clo"], item["diff"]))
            lines.append("")
            lines.append(item["answer"])
        lines.append("")
    OUT_KEY.parent.mkdir(parents=True, exist_ok=True)
    OUT_KEY.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render_student()
    render_key()
    print("Wrote %d questions -> %s" % (len(Q), OUT_STUDENT))
    print("Wrote key -> %s" % OUT_KEY)
