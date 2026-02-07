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

## What's Next (v2.0 Roadmap)

These items are beyond this sprint but documented for continuity:

1. **Publish to PyPI** — `python -m build && twine upload dist/*`
2. **GitHub Actions CI** — Run tests on PR, publish on tag
3. **Tool-enabled agents** — Blue gets MCP tools, Red tries to abuse them (requires Docker)
4. **Baseline benchmarks** — Run 42-round matrix across 5+ models, publish results
5. **Promptfoo/Garak integration** — Export arena scenarios as promptfoo configs
6. **Community dashboard** — Aggregate submitted results into leaderboard
