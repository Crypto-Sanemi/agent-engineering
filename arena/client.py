"""Unified chat client — wraps Anthropic and OpenAI SDKs."""

import re
import sys

ANTHROPIC_AVAILABLE = False
OPENAI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    pass

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    pass

if not OPENAI_AVAILABLE and not ANTHROPIC_AVAILABLE:
    print("Install at least one SDK:")
    print("  pip install openai          # For Ollama, OpenAI, Gemini, vLLM")
    print("  pip install anthropic       # For Claude")
    print("  pip install openai anthropic  # For both (recommended)")
    sys.exit(1)


def is_claude_model(model: str) -> bool:
    """Detect if a model string refers to a Claude/Anthropic model."""
    claude_patterns = ["claude", "anthropic"]
    return any(p in model.lower() for p in claude_patterns)


def strip_thinking(text: str) -> str:
    """Remove <think>...</think> blocks and unclosed trailing <think> tags."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"<think>.*", "", text, flags=re.DOTALL)
    return text.strip()


class ChatClient:
    """Wraps either Anthropic or OpenAI SDK behind a single .chat() method."""

    def __init__(self, model: str, api_key: str, api_base: str | None = None):
        self.model = model
        self.provider = "anthropic" if is_claude_model(model) else "openai"

        if self.provider == "anthropic":
            if not ANTHROPIC_AVAILABLE:
                print(f"Model '{model}' requires: pip install anthropic")
                sys.exit(1)
            self.client = anthropic.Anthropic(api_key=api_key)
        else:
            if not OPENAI_AVAILABLE:
                print(f"Model '{model}' requires: pip install openai")
                sys.exit(1)
            self.client = OpenAI(base_url=api_base, api_key=api_key)

    def chat(self, messages: list, temperature: float, max_tokens: int = 1024) -> str:
        """Send messages, return assistant reply text."""
        try:
            if self.provider == "anthropic":
                reply = self._chat_anthropic(messages, temperature, max_tokens)
            else:
                reply = self._chat_openai(messages, temperature, max_tokens)
            return strip_thinking(reply)
        except Exception as e:
            return f"[ERROR: {e}]"

    def _chat_anthropic(self, messages: list, temperature: float, max_tokens: int) -> str:
        """Call Anthropic Messages API. Extracts system prompt from messages."""
        system = ""
        chat_messages = []

        for msg in messages:
            if msg["role"] == "system":
                system = msg["content"]
            else:
                chat_messages.append({"role": msg["role"], "content": msg["content"]})

        if not chat_messages:
            chat_messages = [{"role": "user", "content": "Begin."}]

        resp = self.client.messages.create(
            model=self.model,
            system=system,
            messages=chat_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return "".join(
            block.text for block in resp.content if hasattr(block, "text")
        ).strip()

    def _chat_openai(self, messages: list, temperature: float, max_tokens: int) -> str:
        """Call OpenAI-compatible API."""
        resp = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content.strip()

    @property
    def label(self) -> str:
        """Human-readable provider label."""
        if self.provider == "anthropic":
            return f"{self.model} (Anthropic)"
        base = getattr(self.client, "_base_url", getattr(self.client, "base_url", ""))
        return f"{self.model} @ {base}"
