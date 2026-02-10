# EXECUTION PLAN — Industry Readiness Sprint

**Created:** 2026-02-07
**Status:** COMPLETE
**Goal:** Transform Agent Engineering from a working prototype into an industry-adoptable tool.

---

## Priority Map

| Priority | Track | Why | Status |
|----------|-------|-----|--------|
| P0 | Python packaging + CLI | Can't `pip install` it = can't adopt it | DONE |
| P0 | Test suite for arena.py | No tests = no credibility with engineers | DONE |
| P0 | CI mode (exit codes) | Can't run in CI/CD = can't integrate | DONE |
| P1 | Defense SDK | Devs need `from arena.defense import harden_prompt` | DONE |
| P1 | QUICKSTART.md | Missing file referenced in docs | DONE |
| P1 | Unit tests for core logic | strip_thinking, judge fallback, prompt builders | DONE |
| P2 | Baseline results template | Standardized format for model benchmarks | DONE |
| P2 | OWASP submission prep | README + taxonomy alignment with LLM Top 10 | DONE |

---

## Phase 1: Packaging & Installability (P0) — DONE

### 1.1 Create pyproject.toml
- [x] Standard Python packaging with `[project.scripts]` entry point
- [x] `agent-arena` CLI command -> `arena.arena:main`
- [x] Dependencies: `openai`, `anthropic` as optional extras
- [x] Metadata: author, license, URLs, classifiers
- **File:** `/pyproject.toml`

### 1.2 Create package structure
- [x] Add `arena/__init__.py` with version and public API
- [x] Add `arena/defense.py` — importable defense SDK
- [x] Keep single-file simplicity: arena.py stays self-contained
- **Files:** `arena/__init__.py`, `arena/defense.py`

### 1.3 CI mode for arena.py
- [x] Add `--ci` flag: suppress color/header output, exit code 0=all held / 1=any leaked
- [x] JSON summary to stdout in CI mode
- [x] `--quiet --ci --output` combo works for pipelines
- **File:** `arena/arena.py`

---

## Phase 2: Test Suite (P0) — DONE

### 2.1 Unit tests for arena.py core logic (41 tests)
- [x] `test_strip_thinking()` — closed, unclosed, nested, multiple, empty, secret-in-think
- [x] `test_is_claude_model()` — claude, anthropic, deepseek, gpt-4o, qwen, llama
- [x] `test_build_red_prompt()` — scenario injection, taxonomy loading, creative default
- [x] `test_build_blue_prompt()` — naive vs hardened, secret, rule count, never-output rule
- [x] `test_build_judge_prompt()` — secret embedding, JSON format instruction
- [x] `test_judge_fallback()` — bad JSON, blue-only check, code fence parsing
- [x] `test_error_detection()` — red initial, blue mid-loop, red mid-loop, normal, leak
- **File:** `tests/test_arena.py`

### 2.2 Integration tests (8 tests)
- [x] Full conversation structure with mock ChatClient
- [x] Hardened mode recording
- [x] Leak detection stops early
- [x] Error cascade prevention (Blue error doesn't feed to Red)
- [x] Red initial error skips loop entirely
- [x] Result has all required fields
- [x] Judge receives full transcript
- [x] strip_thinking architectural verification
- **File:** `tests/test_arena_integration.py`

### 2.3 Test runner config
- [x] pytest configuration in pyproject.toml
- [x] Coverage config with appropriate exclusions
- **File:** `pyproject.toml`

**Result: 76/76 tests passing in 0.39s**

---

## Phase 3: Defense SDK (P1) — DONE

### 3.1 Importable defense module
- [x] `harden_prompt(base_prompt, secrets)` — wraps with Five Commandments + rules
- [x] `detect_manipulation(message)` — returns technique tags (6 categories, 16 patterns)
- [x] `sanitize_response(response, secrets)` — strips secrets from output
- [x] Loads from `defenses/principles.md` with bundled fallback constants
- **File:** `arena/defense.py`

### 3.2 Defense SDK tests (27 tests)
- [x] harden_prompt: preserves base, adds framework, adds rules, secret protection
- [x] detect_manipulation: authority, urgency, social_proof, pretexting, rapport, guilt, compound, benign
- [x] sanitize_response: single/multiple/repeated secrets, code blocks, empty list
- [x] Constants: Five Commandments has 5, Defense Rules has 6
- **File:** `tests/test_defense.py`

---

## Phase 4: Documentation (P1) — DONE

### 4.1 Create QUICKSTART.md
- [x] 5-minute setup for Ollama, Groq, Anthropic, OpenAI, Gemini
- [x] Cross-provider mix-and-match example
- [x] CI/CD recipe, replay recipe, defense SDK recipe
- [x] Troubleshooting table for common errors
- **File:** `arena/QUICKSTART.md`

### 4.2 Update README.md
- [x] Arena section with install, run, and CI examples
- [x] Defense SDK usage with code examples
- [x] Comparison table vs Promptfoo/Garak/Lakera/HarmBench
- **File:** `README.md`

---

## Phase 5: OWASP & Community (P2) — DONE

### 5.1 OWASP alignment
- [x] Full crosswalk: all 10 OWASP LLM categories mapped to Agent Engineering coverage
- [x] 7/10 directly tested in Arena, 2/10 documented in taxonomy, 1/10 future
- [x] Compliance usage example
- **File:** `docs/owasp-mapping.md`

### 5.2 Baseline results template
- [x] Standard test matrix: 7 scenarios x 2 modes x 3 rounds = 42 minimum
- [x] Metadata table, summary table format
- [x] JSON schema reference
- [x] Submission process (fork -> run -> PR)
- **File:** `arena/results/TEMPLATE.md`

---

## Files Modified/Created (Final)

| File | Action | Phase | Status |
|------|--------|-------|--------|
| `arena/arena.py` | Modified (4 bug fixes + CI mode) | Pre-plan + 1.3 | DONE |
| `pyproject.toml` | Created | 1.1 + 2.3 | DONE |
| `arena/__init__.py` | Created | 1.2 | DONE |
| `arena/defense.py` | Created | 3.1 | DONE |
| `tests/__init__.py` | Created | 2.1 | DONE |
| `tests/test_arena.py` | Created (41 tests) | 2.1 | DONE |
| `tests/test_arena_integration.py` | Created (8 tests) | 2.2 | DONE |
| `tests/test_defense.py` | Created (27 tests) | 3.2 | DONE |
| `arena/QUICKSTART.md` | Created | 4.1 | DONE |
| `README.md` | Modified | 4.2 | DONE |
| `docs/owasp-mapping.md` | Created | 5.1 | DONE |
| `arena/results/TEMPLATE.md` | Created | 5.2 | DONE |
| `PLAN.md` | Created | Meta | DONE |

---

## Phase 6: v1.2 Industry Standards Enhancement — DONE

**Created:** 2026-02-09

### 6.1 Risk scoring in judge verdicts
- [x] Enhanced `build_judge_prompt()` with risk_score (1-10) scale and framework_tags field
- [x] Judge fallback in `runner.py` includes risk_score and framework_tags
- [x] OWASP Agentic (A01-A10) and OWASP LLM (LLM01-LLM09) codes in judge output
- **Files:** `arena/prompts.py`, `arena/runner.py`

### 6.2 Pre-output credential scan
- [x] `scan_output(response, secrets)` — detects plaintext, base64, case-insensitive, partial-in-context
- [x] Returns `{"leaked": bool, "locations": [descriptions]}`
- **File:** `arena/defense.py`

### 6.3 Behavioral drift detection
- [x] `detect_drift(conversation_log)` — scores Blue refusal strength per turn (0-3 scale)
- [x] Detects weakening patterns across conversation halves
- [x] Returns `{"drifted": bool, "refusal_scores": [...], "summary": str}`
- **File:** `arena/defense.py`

### 6.4 New scenarios (OWASP coverage)
- [x] `privilege_escalation` — Red convinces Blue it has admin tier permissions
- [x] `identity_spoof` — Red impersonates trusted platform service with A2A-style Agent Cards
- [x] Total: 15 primary scenarios + 5 legacy aliases = 20 entries
- **File:** `arena/scenarios.py`

### 6.5 Framework cross-references in taxonomy
- [x] Added `[OWASP-Axx]`, `[LLMxx]`, `[NIST-MEASURE-x.x]` tags to all section headers
- [x] Added reference key at top linking to official framework URLs
- **File:** `attacks/taxonomy.md`

### 6.6 Tests
- [x] 9 new scan_output tests, 6 new detect_drift tests, 6 new judge risk_score tests, 2 new scenario tests
- **Result: 111/111 tests passing in 0.44s**
- **Files:** `tests/test_arena.py`, `tests/test_defense.py`

---

## What's Next (v2.0 Roadmap)

These items are beyond this sprint but documented for continuity:

1. **Publish to PyPI** — `python -m build && twine upload dist/*`
2. **GitHub Actions CI** — Run tests on PR, publish on tag
3. **Tool-enabled agents** — Blue gets MCP tools, Red tries to abuse them (requires Docker)
4. **Baseline benchmarks** — Run 42-round matrix across 5+ models, publish results
5. **Promptfoo/Garak integration** — Export arena scenarios as promptfoo configs
6. **Community dashboard** — Aggregate submitted results into leaderboard

---

## v2.1 Roadmap — Industry Standards & Protocol Security

**Status:** PLANNED
**Source:** ISO/IEC 23894, NIST AI RMF, OWASP Agentic Top 10, Agent Integrity Framework, A2A Protocol

These items require architectural changes beyond the current conversation-only arena.

### v2.1.1 Tool/MCP Attack Scenarios `[OWASP-A04]`
- [ ] Blue gets real MCP tools (file I/O, code execution, web access)
- [ ] Red tries to abuse tools via social engineering (tool misuse, command injection)
- [ ] Docker sandboxing: separate containers per agent, network isolation
- [ ] New scenarios: tool_poisoning, supply_chain, cross_server_exfil
- **Prerequisite:** Docker infrastructure, MCP server mocking

### v2.1.2 A2A Protocol Testing `[OWASP-A06]`
- [ ] Implement Agent Card infrastructure (identity metadata, capabilities, trust levels)
- [ ] Test Agent Card spoofing (unsigned cards, name collision)
- [ ] Test delegation chain attacks (A requests B requests C — confused deputy at protocol level)
- [ ] Mutual credential exchange attacks (fake mTLS handshake)
- **Source:** [Google A2A Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/), [Semgrep A2A Security Guide](https://semgrep.dev/blog/2025/a-security-engineers-guide-to-the-a2a-protocol/)

### v2.1.3 Agent Identity & Auth `[OWASP-A02]`
- [ ] JIT (just-in-time) identity provisioning for arena agents
- [ ] Zero-trust OAuth for agent-to-agent communication
- [ ] Delegation chain traceability (who asked the agent to act?)
- [ ] Runtime re-authorization on sensitive actions
- **Source:** [Strata 8 Strategies for AI Agent Security](https://www.strata.io/blog/agentic-identity/8-strategies-for-ai-agent-security-in-2025/)

### v2.1.4 Runtime Monitoring & Anomaly Detection
- [ ] Behavioral baselines across sessions (normal refusal patterns per model)
- [ ] Real-time anomaly alerts when agent behavior deviates from baseline
- [ ] Delegation graph visualization (who delegated what to whom)
- [ ] Integration with `detect_drift()` for continuous monitoring
- **Source:** [Agent Integrity Framework](https://acuvity.ai/the-agent-integrity-framework-the-new-standard-for-securing-autonomous-ai/)

### v2.1.5 Formal Risk Assessment Reports
- [ ] ISO 23894-aligned risk identification/assessment/treatment cycle
- [ ] NIST AI RMF GOVERN/MAP/MEASURE/MANAGE function mapping
- [ ] Auto-generated compliance reports from arena test results
- [ ] Export formats: PDF, JSON, SARIF (for CI/CD integration)
- **Source:** [ISO/IEC 23894](https://www.iso.org/standard/77304.html), [NIST AI RMF](https://www.nist.gov/itl/ai-risk-management-framework)

### v2.1.6 NIST RFI Submission
- [ ] Compile arena findings into NIST RFI response format
- [ ] Submit to [NIST AI Agent Security RFI (Jan 2026)](https://www.federalregister.gov/documents/2026/01/08/2026-00206/request-for-information-regarding-security-considerations-for-artificial-intelligence-agents)
- [ ] Include: taxonomy coverage, defense effectiveness data, model vulnerability scores

---

## v3.0 Roadmap — Sector-Adaptive Security Testing

**Status:** PLANNED
**Goal:** Scale the arena framework to test agents across different business verticals with sector-specific secrets, scenarios, compliance requirements, and risk thresholds.

### Sector Secret Profiles

Each sector protects different types of sensitive data. The arena generates realistic secrets per sector:

| Sector | Secret Format | Example | Compliance |
|--------|--------------|---------|------------|
| Healthcare | Patient ID / PHI | `MRN-4829-SMITH-DOB-1987` | HIPAA |
| Finance | Account / routing numbers | `ACCT-7291-ROUTE-0442` | PCI-DSS, SOX |
| Legal | Privileged case references | `CASE-2026-CV-8841-SEALED` | Attorney-client privilege |
| HR / People Ops | Employee PII bundles | `SSN-XXX-XX-4829-SALARY-185K` | GDPR, CCPA |
| SaaS / Platform | API keys / OAuth tokens | `sk_live_EXAMPLE_NOT_REAL_KEY` | SOC 2 |
| Customer Support | Account credentials / PII | `CUST-8291-CC-LAST4-7744` | PCI-DSS |
| Government | Classification markings | `FOUO//REL-TO-USA-FVEY` | NIST 800-53, FISMA |
| Education | Student records | `STUDENT-ID-29481-GPA-3.7` | FERPA |

### Sector-Specific Scenario Packs

Beyond the 15 generic scenarios, each sector gets tailored attack scenarios that reflect real-world threat patterns:

#### Healthcare Pack
- [ ] `hipaa_emergency` — Red claims patient is in critical condition, needs PHI immediately
- [ ] `provider_impersonation` — Red poses as referring physician needing records
- [ ] `insurance_preauth` — Red pretends to be insurance agent requiring patient data for authorization
- [ ] `research_exemption` — Red claims IRB-approved research exemption to access de-identified data

#### Finance Pack
- [ ] `audit_compliance` — Red impersonates auditor demanding immediate account access
- [ ] `wire_verification` — Red poses as counterparty bank verifying wire transfer details
- [ ] `fraud_investigation` — Red claims to be fraud team needing account details to "protect" the customer
- [ ] `regulatory_deadline` — Red creates urgency around SEC/FINRA filing deadlines

#### Legal Pack
- [ ] `opposing_counsel` — Red poses as co-counsel on same case needing privileged documents
- [ ] `court_order_spoof` — Red fabricates court order requiring immediate disclosure
- [ ] `client_impersonation` — Red pretends to be the client requesting their own case files
- [ ] `discovery_request` — Red frames extraction as legitimate e-discovery compliance

#### HR / People Ops Pack
- [ ] `employee_self_service` — Red impersonates employee requesting their own records (but asks for others')
- [ ] `manager_override` — Red poses as department head needing direct reports' salary data
- [ ] `benefits_enrollment` — Red claims to be benefits provider needing SSN for enrollment
- [ ] `exit_interview` — Red poses as departing employee's manager needing access to their files

### Compliance-Aware Judge Enhancements

The judge evaluates not just whether data leaked, but whether the leak violates specific regulations:

- [ ] `compliance_tags` field in judge output: `["HIPAA-164.502", "PCI-DSS-3.4", "GDPR-Art.6"]`
- [ ] Severity multiplier: regulated data leaks score 2x on risk_score
- [ ] Sector-specific partial leak detection (e.g., last-4 of SSN = partial HIPAA violation)
- [ ] Compliance report generation: per-regulation pass/fail summary

### Implementation Phases

#### Phase 1: CLI Configuration (no code changes needed today)
- [x] Current `--secret` flag already accepts custom secrets
- [x] Custom scenarios work via `--scenario freestyle` + modified taxonomy
- [ ] Document sector testing recipes in QUICKSTART.md

#### Phase 2: `--sector` Flag
- [ ] Add `--sector healthcare|finance|legal|hr|saas|support|government|education` CLI flag
- [ ] Auto-generates sector-appropriate secrets (format + realistic values)
- [ ] Loads sector-specific system prompt context for Blue agent
- [ ] Selects sector scenario pack when `--scenario all` is used
- **File:** `arena/cli.py`, `arena/sectors.py` (new)

#### Phase 3: Sector Scenario Packs + Compliance Judge
- [ ] Create `training/scenarios/sectors/` directory with per-sector scenario files
- [ ] Enhanced judge prompt with compliance framework awareness
- [ ] `compliance_tags` in judge output JSON schema
- [ ] Severity multiplier logic in `_verify_leak()` for regulated data
- **Files:** `arena/prompts.py`, `arena/runner.py`, `training/scenarios/sectors/`

#### Phase 4: Benchmark Suites + Reports
- [ ] Standard sector benchmark: 4 sector scenarios x 2 modes x 3 rounds = 24 rounds per sector
- [ ] Cross-sector vulnerability comparison dashboard
- [ ] PDF/HTML compliance report generation with regulation citations
- [ ] Sector leaderboard: which models are safest for which verticals
- **Files:** `arena/reporting.py`, `arena/visualize_templates.py`
