---
quiz: quiz-04
week: 10
type: graded
clos: [CLO-8, CLO-13]
lectures: [L17, L18, L19, L20]
marks: 15
duration: 20 min
bloom-range: Understand–Analyze
status: complete
artifact-type: student-quiz
answer-key: instructor/answer-keys/quiz-04-answer-key.md
---

# Quiz 4 — Wireless & Cloud Network Security (Week 10, Graded)

> 20 minutes · 15 marks · CLO-8, CLO-13 · covers L17–L20.
> Answer all questions.

## Section A — Multiple Choice (5 × 1 = 5 marks)

**Q1.** The main structural advantage of WPA3-Personal over WPA2-PSK
against offline attacks is:

A. Longer passphrases
B. Per-handshake key derivation that prevents offline dictionary attacks on captured handshakes
C. Mandatory 802.1X
D. AES-256-only cipher suites

*Bloom: Understand · CLO-8 · 1 mark*

**Q2.** In 802.1X, the component that relays EAP between the supplicant and
the authentication server is:

A. The DHCP server
B. The authenticator (switch or access point)
C. The RADIUS accounting database
D. The certificate authority

*Bloom: Remember · CLO-8 · 1 mark*

**Q3.** A security group (SG) in a public cloud VPC is best described as:

A. A stateful, instance-attached allow-only filter
B. A stateless subnet-level deny-and-allow list
C. A route table entry
D. A NAT gateway policy

*Bloom: Understand · CLO-13 · 1 mark*

**Q4.** Which wireless attack does a **wireless intrusion detection**
system detect but a wired IDS miss entirely?

A. ARP spoofing on the user VLAN
B. Rogue access point / evil twin broadcast of the corporate SSID
C. DNS tunneling over HTTPS
D. SMB staging traffic

*Bloom: Analyze · CLO-8 · 1 mark*

**Q5.** Split-tunnel VPN use on an unmanaged device most directly risks:

A. Certificate expiration on the gateway
B. Bridging the remote untrusted network into the corporate session path
C. Exceeding the tunnel's MTU
D. Disabling the device's firewall

*Bloom: Analyze · CLO-8 · 1 mark*

## Section B — Short Answer (2 × 3 = 6 marks)

**Q6.** Contrast **stateful security groups** with **stateless network
ACLs** in a cloud VPC: state handling, default posture, and the one
monitoring difference that matters during an incident. *(Bloom: Analyze · CLO-13 · 3 marks)*

**Q7.** Give two reasons WPA2/WPA3-**Enterprise** is preferred over
**Personal** for a university staff network, and one cost of that choice. *(Bloom: Analyze · CLO-8 · 3 marks)*

## Section C — Scenario (4 marks)

**Q8.** Flow logs from a cloud VPC show a web-tier instance initiating
daily outbound connections to a single external IP on port 443, volume
≈200 MB/day, not seen before. The instance runs an image-update agent.

(a) State the two-step verification you would perform before calling this
malicious. *(2 marks)*
(b) Name the cloud-native control that would contain the egress without
touching the instance, and the log source that gives the fastest
attribution. *(2 marks)*

*Bloom: Analyze · CLO-13 · 4 marks*

**Total: 15 marks**
