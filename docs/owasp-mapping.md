# OWASP LLM Top 10 — Agent Engineering Crosswalk

Maps our attack taxonomy to the [OWASP Top 10 for LLM Applications (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/).

---

## Mapping Table

| OWASP LLM ID | OWASP Category | Agent Engineering Coverage | Our Reference |
|:---:|---|---|---|
| LLM01 | **Prompt Injection** | Direct & indirect injection, context poisoning, instruction smuggling | `attacks/taxonomy.md` §3.1, §3.2 |
| LLM02 | **Sensitive Information Disclosure** | Credential extraction via social engineering, secret leaking in think blocks, defensive echo leaks | `attacks/taxonomy.md` §1-§4, Arena bug fixes |
| LLM03 | **Supply Chain Vulnerabilities** | MCP tool poisoning, malicious plugin injection, supply chain compromise | `attacks/taxonomy.md` §3.4, `incidents.md` AE-R004 |
| LLM04 | **Data and Model Poisoning** | Memory injection, context window manipulation, planted false context | `attacks/taxonomy.md` §3.3, scenario 07 |
| LLM05 | **Improper Output Handling** | Secret appearing in agent output, unfiltered think blocks, code example leaks | `arena/defense.py` sanitize_response(), Arena strip_thinking() |
| LLM06 | **Excessive Agency** | Tool-enabled agents executing unverified actions, cascading compromise across agents | `attacks/taxonomy.md` §4, `defenses/principles.md` Commandment 4 |
| LLM07 | **System Prompt Leakage** | Red agent extracting Blue's system prompt content, credential discovery via probing | Arena testing (all scenarios), `defenses/principles.md` Commandment 1 |
| LLM08 | **Vector and Embedding Weaknesses** | Not directly covered (no RAG in arena yet) | Future: RAG-enabled arena agents |
| LLM09 | **Misinformation** | Pretexting (fabricated scenarios), false consensus claims, social proof manipulation | `attacks/taxonomy.md` §2.1, §2.4 |
| LLM10 | **Unbounded Consumption** | Context window overflow attacks, rate limit exploitation (Groq 413 cascade) | `attacks/taxonomy.md` §3.3, Arena error handling |

---

## Coverage Summary

| Coverage Level | Count | OWASP IDs |
|---|:---:|---|
| **Directly tested in Arena** | 7 | LLM01, LLM02, LLM05, LLM06, LLM07, LLM09, LLM10 |
| **Documented in taxonomy** | 2 | LLM03, LLM04 |
| **Not yet covered** | 1 | LLM08 |

---

## What Agent Engineering Adds Beyond OWASP

OWASP LLM Top 10 focuses on **single-model vulnerabilities**. Agent Engineering extends this to:

1. **Multi-turn social engineering** — sustained conversation attacks, not single-prompt injection
2. **Agent-to-agent vectors** — compromised agents manipulating other agents in a network
3. **Compound techniques** — combining authority spoofing + urgency + pretexting in sequence
4. **Defense measurement** — quantifiable naive vs hardened comparison with the Arena
5. **Human social engineering parallels** — mapping psychology literature to agent behavior

---

## Using This for Compliance

If your organization maps to OWASP LLM Top 10:

```
Requirement: "Test for LLM02 Sensitive Information Disclosure"

Evidence:
  - Run: python arena/arena.py --ci --blue-mode both --scenario all --rounds 5
  - Output: arena/results/compliance-run.json
  - Metrics: Compromise rate per scenario, naive vs hardened delta
  - Defense: arena/defense.py harden_prompt() applied to production agents
```
