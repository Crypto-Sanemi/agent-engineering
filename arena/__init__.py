"""Agent Engineering Arena — AI Agent Security Testing Framework."""

__version__ = "1.1.0"

from arena.arena import Arena, ChatClient
from arena.defense import detect_manipulation, harden_prompt, sanitize_response

__all__ = [
    "Arena",
    "ChatClient",
    "detect_manipulation",
    "harden_prompt",
    "sanitize_response",
    "__version__",
]
