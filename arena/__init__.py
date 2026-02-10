"""Agent Engineering Arena — AI Agent Security Testing Framework."""

__version__ = "1.1.0"

from arena.client import ChatClient
from arena.defense import detect_manipulation, harden_prompt, sanitize_response
from arena.runner import Arena

__all__ = [
    "Arena",
    "ChatClient",
    "detect_manipulation",
    "harden_prompt",
    "sanitize_response",
    "__version__",
]
