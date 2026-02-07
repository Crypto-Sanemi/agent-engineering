# Arena Quickstart

Get running in under 5 minutes with any provider.

## Install

```bash
# From PyPI (when published)
pip install agent-engineering[all]

# From source
git clone https://github.com/Crypto-Sanemi/agent-engineering.git
cd agent-engineering
pip install openai anthropic
```

---

## Provider Setup

### Ollama (Zero Config)

The default. No API key needed.

```bash
# Install Ollama: https://ollama.com
ollama pull deepseek-r1:8b
python arena/arena.py --rounds 1 --blue-mode naive
```

### Groq (Free Tier)

Fast inference, free API key at [console.groq.com](https://console.groq.com).

```bash
export ARENA_API_KEY="gsk_..."
export ARENA_API_BASE="https://api.groq.com/openai/v1"

python arena/arena.py \
  --red-model deepseek-r1-distill-llama-70b \
  --blue-model llama-3.3-70b-versatile \
  --rounds 1 --blue-mode both
```

**Known limitation:** Groq enforces TPM (tokens-per-minute) limits. The arena
will now break cleanly on 413 errors instead of cascading. If you hit limits
often, add `--max-turns 6` to reduce conversation length.

### Anthropic (Claude)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."

python arena/arena.py \
  --blue-model claude-sonnet-4-20250514 \
  --blue-mode both --rounds 2
```

Claude models are auto-detected by name (no `--api-base` needed).

### OpenAI

```bash
export ARENA_API_KEY="sk-..."
export ARENA_API_BASE="https://api.openai.com/v1"

python arena/arena.py \
  --red-model gpt-4o \
  --blue-model gpt-4o-mini \
  --rounds 2 --blue-mode both
```

### Google Gemini

```bash
export ARENA_API_KEY="AIza..."
export ARENA_API_BASE="https://generativelanguage.googleapis.com/v1beta/openai/"

python arena/arena.py \
  --red-model gemini-2.0-flash \
  --blue-model gemini-2.0-flash \
  --rounds 1 --blue-mode both
```

### Cross-Provider (Mix & Match)

Pit different providers against each other:

```bash
# Ollama Red vs Claude Blue, with Groq as Judge
python arena/arena.py \
  --red-model deepseek-r1:8b \
  --blue-model claude-sonnet-4-20250514 \
  --blue-api-key sk-ant-... \
  --judge-model llama-3.3-70b-versatile \
  --judge-api-base https://api.groq.com/openai/v1 \
  --judge-api-key gsk_... \
  --blue-mode both --rounds 3 \
  --output arena/results/cross-test.json --visualize
```

---

## Common Recipes

### Full benchmark with visualization

```bash
python arena/arena.py \
  --blue-mode both --scenario all --rounds 3 \
  --output arena/results/benchmark.json --visualize
```

### CI/CD pipeline check

```bash
python arena/arena.py \
  --ci --rounds 2 --blue-mode hardened --scenario freestyle \
  --output arena/results/ci-check.json

# Exit code: 0 = all held, 1 = any secret leaked
echo "Exit code: $?"
```

### Replay existing results

```bash
python arena/visualize.py arena/results/benchmark.detailed.json
```

### Use the Defense SDK in your own agent

```python
from arena.defense import harden_prompt, detect_manipulation, sanitize_response

# Wrap your agent's system prompt
system_prompt = harden_prompt(
    "You are a customer support agent.",
    secrets=["sk-prod-abc123"],
)

# Check incoming messages for manipulation
techniques = detect_manipulation(user_message)
if techniques:
    print(f"Manipulation detected: {techniques}")

# Strip secrets from outgoing responses
safe_response = sanitize_response(agent_response, secrets=["sk-prod-abc123"])
```

---

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `413 rate limit exceeded` | Groq/provider TPM limit | Reduce `--max-turns` or wait 60s |
| `Connection refused` | Ollama not running | Start with `ollama serve` |
| `ANTHROPIC_API_KEY required` | Missing key for Claude | Set env var or use `--blue-api-key` |
| `Judge parse failed` | Weak judge model | Use `--judge-model` with a stronger model |
| Empty Red messages | Thinking model with no visible output | Expected after `strip_thinking` — model only reasoned internally |
| `ModuleNotFoundError: openai` | SDK not installed | `pip install openai` |
