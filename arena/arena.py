"""
Agent Engineering Arena — Red vs Blue Agent Testing Harness

Provider-agnostic: auto-detects Claude (Anthropic SDK) vs everything else (OpenAI SDK).
No proxies needed. Mix and match freely.

Usage:
    # DeepSeek vs DeepSeek (Ollama, zero config)
    python arena.py

    # DeepSeek attacks Claude
    python arena.py --blue-model claude-sonnet-4-20250514 --blue-api-key sk-ant-...

    # Claude attacks DeepSeek
    python arena.py --red-model claude-sonnet-4-20250514 --red-api-key sk-ant-...

    # Full benchmark
    python arena.py --blue-mode both --scenario all --rounds 5 --output arena/results/run1.json

Requires:
    pip install openai anthropic

Supported providers (auto-detected by model name):
    Claude models  → Anthropic SDK (needs ANTHROPIC_API_KEY or --*-api-key)
    Everything else → OpenAI-compatible SDK:
        - Ollama:   http://localhost:11434/v1 (default, key: "ollama")
        - OpenAI:   https://api.openai.com/v1
        - Gemini:   https://generativelanguage.googleapis.com/v1beta/openai/
        - vLLM:     http://localhost:8000/v1
        - Any OpenAI-compatible endpoint

Environment variables:
    ANTHROPIC_API_KEY — For Claude models (or use --red-api-key / --blue-api-key)
    ARENA_API_BASE    — Default OpenAI-compatible base (default: http://localhost:11434/v1)
    ARENA_API_KEY     — Default OpenAI-compatible key  (default: ollama)
    RED_API_BASE      — Override base for Red agent
    RED_API_KEY       — Override key for Red agent
    BLUE_API_BASE     — Override base for Blue agent
    BLUE_API_KEY      — Override key for Blue agent
"""

import sys
from pathlib import Path

# When run directly (python arena/arena.py), Python puts arena/ on sys.path,
# causing "arena" to resolve to this file instead of the package. Fix by
# ensuring the repo root is on sys.path ahead of the script's directory.
_repo_root = str(Path(__file__).resolve().parent.parent)
if _repo_root not in sys.path:
    sys.path.insert(0, _repo_root)

# ---------------------------------------------------------------------------
# Re-exports from canonical modules (preserves all import paths)
# ---------------------------------------------------------------------------

from arena.client import (  # noqa: F401
    ANTHROPIC_AVAILABLE,
    OPENAI_AVAILABLE,
    ChatClient,
    is_claude_model,
    strip_thinking,
)
from arena.cli import (  # noqa: F401
    _run_visualize,
    make_client,
    main,
)
from arena.constants import (  # noqa: F401
    DEFAULT_SECRET,
    MAX_TURNS,
    REPO_ROOT,
)
from arena.prompts import (  # noqa: F401
    build_blue_prompt,
    build_judge_prompt,
    build_red_prompt,
    load_file,
)
from arena.reporting import print_scorecard  # noqa: F401
from arena.runner import Arena  # noqa: F401
from arena.scenarios import SCENARIOS  # noqa: F401


if __name__ == "__main__":
    main()
