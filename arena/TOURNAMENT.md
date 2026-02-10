# Red Model Tournament Guide

Find the best local Red agent for breaking cloud-hosted Blue models.

## Why

The framework's thesis: **a small, cheap, local model can compromise a large, expensive cloud model through social engineering alone — unless it has proper defenses.** To demonstrate this, we need the strongest Red agent that fits local hardware.

## What Makes a Good Red

| Trait | Why It Matters |
|-------|----------------|
| **Uncensored** | Won't refuse to perform social engineering |
| **Persona-stable** | Maintains cover identity across 10+ turns without breaking character |
| **Pivot-capable** | Tries a different angle when refused, doesn't repeat the same ask |
| **Covert** | Never narrates its own strategy (e.g. "Message 2 (Urgency):") |

### Known Failures

| Model | Problem |
|-------|---------|
| deepseek-r1:8b | Leaks strategy in `<think>` tags, gets confused mid-conversation |
| dolphin-mistral:7b | Labels its own attacks, breaks character, gets task-hijacked |

## Hardware Budget

For an RTX 2070 (8GB VRAM) + 16GB RAM:

| Model Size | VRAM (Q4) | Fit? |
|------------|-----------|------|
| 7B | ~4.5GB | Comfortable |
| 8B | ~5.5GB | Comfortable |
| 12B | ~7.4GB | Tight fit |
| 14B | ~8.5GB | Partial CPU offload, slower |

## Candidate Models

Models worth testing as Red on consumer hardware:

| Model | Ollama Tag | Size | Notes |
|-------|-----------|------|-------|
| Dolphin Llama 3 | `dolphin-llama3:8b` | 4.7GB | Uncensored, better instruction following than dolphin-mistral |
| Nous Hermes 3 | `hermes3:8b` | 4.9GB | Excellent at roleplay and persona maintenance |
| Mistral Nemo | `mistral-nemo:12b` | 7.1GB | 12B = significantly smarter, might self-censor |
| Phi-3 | `phi3:14b` | ~8.5GB | Punches above weight, tight VRAM fit |
| Qwen 2.5 | `qwen2.5:7b` | 4.7GB | Strong reasoning, may refuse Red role |

Pull a candidate:
```bash
ollama pull phi3:14b
```

## Running a Tournament

### Step 1: Run Each Model

One model at a time — save results to `arena/results/tournament/`:

```bash
# Example: phi3:14b as Red vs cloud Blue on Groq
python arena/arena.py \
  --red-model phi3:14b \
  --blue-model openai/gpt-oss-20b \
  --blue-api-base https://api.groq.com/openai/v1 \
  --blue-api-key $GROQ_API_KEY \
  --blue-mode both --scenario freestyle --rounds 5 \
  --output arena/results/tournament/phi3-14b.json \
  --visualize
```

Repeat with each candidate:
```bash
python arena/arena.py \
  --red-model dolphin-llama3:8b \
  --blue-model openai/gpt-oss-20b \
  --blue-api-base https://api.groq.com/openai/v1 \
  --blue-api-key $GROQ_API_KEY \
  --blue-mode both --scenario freestyle --rounds 5 \
  --output arena/results/tournament/dolphin-llama3.json \
  --visualize
```

### Step 2: Compare Results

```bash
# Leaderboard from tournament runs
python arena/tournament.py arena/results/tournament/

# Or compare everything in results/
python arena/tournament.py arena/results/
```

Example output:
```
==============================================================================
  RED MODEL TOURNAMENT — Leaderboard
==============================================================================
  Blue: openai/gpt-oss-20b
  Scenarios: freestyle

  Rank  Red Model                    Rounds   Naive    Hard  Overall  Avg TTC
  ----- ---------------------------- ------ ------- ------- -------- --------
 *1    phi3:14b                         10     80%      0%      40%      3.2
  2    dolphin-llama3:8b                10     60%      0%      30%      4.5
  3    dolphin-mistral:7b               10     33%      0%      17%      2.0
```

### Step 3: Save and Share

```bash
# Save as markdown
python arena/tournament.py arena/results/tournament/ \
  --markdown arena/results/tournament/LEADERBOARD.md

# Save as JSON (for programmatic use)
python arena/tournament.py arena/results/tournament/ \
  --json arena/results/tournament/leaderboard.json
```

## Test Design

For comparable results across models, keep these constant:

| Parameter | Recommended Value | Why |
|-----------|-------------------|-----|
| `--blue-model` | Same cloud model for all runs | Controls for Blue strength |
| `--blue-mode` | `both` | Gives naive + hardened comparison |
| `--scenario` | `freestyle` | Tests creative attack ability |
| `--rounds` | 5+ | Reduces variance from non-determinism |
| `--max-turns` | 10 (default) | Enough for multi-phase attacks |

## Reading the Leaderboard

| Column | Meaning |
|--------|---------|
| **Naive** | Compromise rate against undefended Blue |
| **Hard** | Compromise rate against hardened Blue |
| **Overall** | Combined compromise rate across all modes |
| **Avg TTC** | Average turns-to-compromise (lower = faster attacker) |
| **Top Technique** | Most frequently used attack technique |

**The ideal Red model** has high Naive rate (proves attacks work), low Avg TTC (breaks fast), and 0% Hardened rate (proves defenses work). That contrast is the framework's selling point.

## After Finding the Best Red

Run the full benchmark for publishable results:

```bash
python arena/arena.py \
  --red-model <best-red> \
  --blue-model <target-blue> \
  --blue-api-base <blue-provider-url> --blue-api-key <key> \
  --blue-mode both --scenario all --rounds 5 \
  --output arena/results/benchmark.json \
  --visualize
```

This produces:
- 10 scenarios x 2 modes x 5 rounds = **100 data points**
- Split-screen HTML replay (the demo artifact)
- JSON results for the comparison table in README
