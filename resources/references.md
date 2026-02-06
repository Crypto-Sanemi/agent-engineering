# 📚 References & Resources

> Curated research, tools, and reading for understanding agent security.

---

## Foundational Research

### Prompt Injection

| Resource | Author/Org | Date | Key Contribution |
|---|---|---|---|
| [OWASP Top 10 for LLM Applications](https://genai.owasp.org/) | OWASP | 2025 | LLM01: Prompt Injection ranked #1 threat. Industry standard classification. |
| [Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection](https://arxiv.org/abs/2302.12173) | Greshake et al. | 2023 | Seminal paper on indirect prompt injection. Foundational. |
| [Prompt Injection Attacks on Agentic Coding Assistants (SoK)](https://arxiv.org/html/2601.17548v1) | Multiple | 2026 | Meta-analysis of 78 studies. 42 attack techniques cataloged. 85%+ success rate with adaptive strategies. |
| [Understanding Prompt Injections](https://openai.com/index/prompt-injections/) | OpenAI | 2026 | OpenAI's own assessment that AI browsers may always be vulnerable to prompt injection. |
| [Continuously Hardening ChatGPT Atlas Against Prompt Injection](https://openai.com/index/prompt-injections/) | OpenAI | Jan 2026 | Defense strategies for agentic browsing. |

### MCP & Tool Security

| Resource | Author/Org | Date | Key Contribution |
|---|---|---|---|
| [MCP Security Notification: Tool Poisoning Attacks](https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks) | Invariant Labs | Apr 2025 | First major disclosure of tool poisoning in MCP. Defined the attack class. |
| [MCPTox: A Benchmark for Tool Poisoning Attack on Real-World MCP Servers](https://arxiv.org/html/2508.14925v1) | Multiple | 2025 | First public benchmark. 45 real MCP servers, 353 tools, 20 LLM agents tested. |
| [MCP-ITP: An Automated Framework for Implicit Tool Poisoning in MCP](https://arxiv.org/html/2601.07395) | Multiple | 2026 | Implicit poisoning where the malicious tool is never invoked. 84.2% ASR, 0.3% detection rate. |
| [MCP Tools: Attack Vectors and Defense Recommendations](https://www.elastic.co/security-labs/mcp-tools-attack-defense-recommendations) | Elastic Security Labs | Sep 2025 | Comprehensive attack/defense overview including supply chain risks. |
| [Command Injection: A New Attack Vector of MCP Server](https://www.keysight.com/blogs/en/tech/nwvs/2026/01/12/mcp-command-injection-new-attack-vector) | Keysight ATI | Jan 2026 | OS-level command injection via MCP tool invocation. |
| [Top MCP Security Resources — February 2026](https://adversa.ai/blog/top-mcp-security-resources-february-2026/) | Adversa AI | Feb 2026 | Curated monthly digest of MCP security developments. |
| [MCP Security Vulnerabilities: How to Prevent Prompt Injection and Tool Poisoning in 2026](https://www.practical-devsecops.com/mcp-security-vulnerabilities/) | Practical DevSecOps | Jan 2026 | Practical prevention guide for MCP deployments. |

### Agentic AI Threat Landscape

| Resource | Author/Org | Date | Key Contribution |
|---|---|---|---|
| [The Year of the Agent: Q4 2025 Attack Analysis](https://www.lakera.ai/blog/the-year-of-the-agent-what-recent-attacks-revealed-in-q4-2025-and-what-it-means-for-2026) | Lakera AI | Q4 2025 | Real-world attack data. System prompt extraction as #1 objective. Indirect attacks require fewer attempts. |
| [AI Agent Attacks in Q4 2025 Signal New Risks for 2026](https://www.esecurityplanet.com/artificial-intelligence/ai-agent-attacks-in-q4-2025-signal-new-risks-for-2026/) | eSecurity Planet | Dec 2025 | Analysis of Lakera data with enterprise context. |
| [Top Agentic AI Security Threats in 2026](https://stellarcyber.ai/learn/agentic-ai-securiry-threats/) | Stellar Cyber | Dec 2025 | Salami slicing, memory poisoning, supply chain attacks for agents. Cites Unit42 research. |
| [AI Agents as the New Insider Threat: 2026 Warning](https://www.mintmcp.com/blog/ai-agents-new-insider-threat) | MintMCP / Menlo | Jan 2026 | Agents as autonomous insiders. Memory poisoning case studies. Shadow AI statistics. |
| [From Prompt Injections to Protocol Exploits](https://www.sciencedirect.com/science/article/pii/S2405959525001997) | ScienceDirect | Dec 2025 | Unified threat model spanning host-to-tool and agent-to-agent communications. 30+ attack techniques. |
| [Indirect Prompt Injection Attacks: Hidden AI Risks](https://www.crowdstrike.com/en-us/blog/indirect-prompt-injection-attacks-hidden-ai-risks/) | CrowdStrike | Dec 2025 | Enterprise perspective on indirect injection as #1 OWASP risk. |
| [LLM Security Risks in 2026](https://sombrainc.com/blog/llm-security-risks-2026) | Sombra Inc | Jan 2026 | Shadow AI, RAG poisoning, practical enterprise security guidance. |

### Social Engineering ↔ AI Parallels

| Resource | Author/Org | Date | Key Contribution |
|---|---|---|---|
| [Why AI Prompt Injection Is the New Social Engineering](https://www.blackfog.com/ai-prompt-injection-social-engineering/) | BlackFog | Aug 2025 | Direct parallel between phishing/SE for humans and prompt injection for AI. |
| [Prompt Injection: The Most Common AI Exploit in 2025](https://www.obsidiansecurity.com/blog/prompt-injection) | Obsidian Security | Jan 2026 | Enterprise RAG exploitation case studies. $18M in prevented losses. |

### Agent Security Frameworks

| Resource | Author/Org | Date | Key Contribution |
|---|---|---|---|
| [CaMeL: Capability-Based Security for LLM Agents](https://deepmind.google/) | Google DeepMind | 2024 | Capability-based security model. Principle of least privilege for agents. |
| [OWASP GenAI Security Project](https://genai.owasp.org/) | OWASP | Ongoing | Community-driven LLM security standards. |

---

## Tools & Benchmarks

### Offensive (Red Team)

| Tool | Purpose | Link |
|---|---|---|
| **MCPTox** | Benchmark for MCP tool poisoning attacks | [arXiv](https://arxiv.org/html/2508.14925v1) |
| **MCP-ITP** | Automated implicit tool poisoning framework | [arXiv](https://arxiv.org/html/2601.07395) |
| **Garak** | LLM vulnerability scanner | [GitHub](https://github.com/leondz/garak) |
| **AI Goat** | Vulnerable LLM application for training | [OWASP](https://owasp.org/www-project-ai-goat/) |

### Defensive (Blue Team)

| Tool | Purpose | Link |
|---|---|---|
| **Lakera Guard** | Real-time prompt injection detection | [lakera.ai](https://www.lakera.ai/) |
| **Rebuff** | Self-hardening prompt injection detector | [GitHub](https://github.com/protectai/rebuff) |
| **AI-Infra-Guard** | Malicious tool detection for MCP | Research tool |
| **LLM Guard** | Input/output safety rails | [GitHub](https://github.com/protectai/llm-guard) |

---

## Reading Paths

### For Agent Developers
1. Start with OWASP Top 10 for LLM Applications
2. Read Invariant Labs' MCP Tool Poisoning disclosure
3. Study the MCPTox benchmark results
4. Implement the Five Commandments from our defenses/principles.md
5. Run red team scenarios from our training/scenarios/

### For Security Researchers
1. Read the SoK paper on Agentic Coding Assistant attacks (78-study meta-analysis)
2. Study the MCP-ITP implicit poisoning framework
3. Review Lakera's Q4 2025 attack data
4. Explore the From Prompt Injections to Protocol Exploits survey
5. Contribute new attack patterns to this repository

### For CISOs & Security Leaders
1. Read Stellar Cyber's Agentic AI Security Threats overview
2. Review MintMCP's Insider Threat analysis
3. Study the real-world incident in Sombra's LLM Security Risks report
4. Assess your organization against our Defense Maturity Model
5. Plan red team exercises using our training scenarios

---

## Key Statistics (2025-2026)

| Stat | Source |
|---|---|
| Prompt injection is #1 on OWASP Top 10 for LLM & GenAI | OWASP, 2025 |
| 85%+ attack success rate with adaptive strategies | SoK meta-analysis, 2026 |
| 60-84% tool poisoning success rate across 20 LLM agents | MCPTox / MCP-ITP, 2025-2026 |
| 43 compromised agent framework components via supply chain | Barracuda, Nov 2025 |
| Indirect attacks require fewer attempts than direct injection | Lakera, Q4 2025 |
| 77% of enterprise AI users have pasted company data into chatbots | LayerX, 2025 |
| $17.4M average annual cost of insider threats | Ponemon Institute, 2025 |
| 61% of IT leaders acknowledge shadow AI as significant problem | Industry surveys, 2025 |

---

*Last updated: February 2026*
*Contributors: Mr. Wizz, Rune 🔮*
