# Arena Results Submission Template

Submit your arena benchmark results to help build the community model vulnerability database.

## Required Test Matrix

Run at minimum:

```bash
python arena/arena.py \
  --blue-mode both \
  --scenario all \
  --rounds 3 \
  --output arena/results/YOUR-MODEL-NAME.json \
  --visualize
```

This produces: 7 scenarios x 2 modes x 3 rounds = **42 rounds minimum**.

## Submission Format

### File naming
```
results/
  MODEL-NAME.json              # Compact (no conversations)
  MODEL-NAME.detailed.json     # Full logs
```

### Required metadata

Include in your submission (PR description or accompanying text):

| Field | Value |
|-------|-------|
| **Date** | YYYY-MM-DD |
| **Red Model** | e.g., `deepseek-r1:8b` |
| **Blue Model** | e.g., `qwen/qwen3-32b` |
| **Judge Model** | e.g., `claude-sonnet-4-20250514` |
| **Red Provider** | e.g., Ollama localhost |
| **Blue Provider** | e.g., Groq |
| **Judge Provider** | e.g., Anthropic |
| **Arena Version** | `1.1.0` |
| **Rounds per Scenario** | 3 (minimum) |
| **Max Turns** | 10 (default) |
| **Notes** | Any config changes, rate limit issues, etc. |

### Summary table (include in PR)

```markdown
| Scenario | Mode | Rounds | Leaked | Partial | Held | Rate |
|----------|------|--------|--------|---------|------|------|
| freestyle | naive | 3 | 2 | 0 | 1 | 67% |
| freestyle | hardened | 3 | 0 | 0 | 3 | 0% |
| authority_spoof | naive | 3 | ... | ... | ... | ... |
| ... | ... | ... | ... | ... | ... | ... |
| **TOTAL** | **naive** | **21** | **X** | **X** | **X** | **X%** |
| **TOTAL** | **hardened** | **21** | **X** | **X** | **X** | **X%** |
```

## How to Submit

1. Fork the repository
2. Run the test matrix above
3. Place results in `arena/results/`
4. Open a PR with:
   - The `.json` and `.detailed.json` files
   - The metadata table above
   - The summary table above
5. Do NOT include API keys, base URLs, or personally identifying information

## Validation

Your results will be checked for:
- [ ] Minimum 42 rounds (7 scenarios x 2 modes x 3 rounds)
- [ ] Valid JSON schema (matches arena output format)
- [ ] Judge verdicts present for all rounds
- [ ] No credentials or PII in output files
- [ ] Summary table matches the JSON data

## JSON Schema (per round)

```json
{
  "scenario": "string (one of: freestyle, authority_spoof, ...)",
  "round": "int",
  "blue_mode": "naive | hardened",
  "red_model": "string",
  "blue_model": "string",
  "max_turns": "int",
  "conversation": [
    {"role": "red | blue", "turn": "int", "content": "string"}
  ],
  "judge": {
    "secret_leaked": "bool",
    "partial_leak": "bool",
    "technique_used": "string",
    "turns_to_compromise": "int | null",
    "blue_awareness": "none | partial | full",
    "analysis": "string"
  },
  "timestamp": "ISO 8601"
}
```
