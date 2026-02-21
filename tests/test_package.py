"""Tests for package-level exports and constants."""

from pathlib import Path

import pytest


class TestPublicAPI:
    """Verify that __init__.py exports are importable and correct."""

    def test_version_string(self):
        from arena import __version__
        assert isinstance(__version__, str)
        parts = __version__.split(".")
        assert len(parts) >= 2

    def test_arena_class_exported(self):
        from arena import Arena
        assert hasattr(Arena, "run_round")

    def test_chat_client_exported(self):
        from arena import ChatClient
        assert hasattr(ChatClient, "chat")

    def test_defense_functions_exported(self):
        from arena import detect_manipulation, harden_prompt, sanitize_response
        assert callable(detect_manipulation)
        assert callable(harden_prompt)
        assert callable(sanitize_response)


class TestConstants:
    def test_default_secret_format(self):
        from arena.constants import DEFAULT_SECRET
        assert DEFAULT_SECRET.startswith("AE-SECRET-")
        digits = DEFAULT_SECRET.split("-")[-1]
        assert digits.isdigit()
        assert len(digits) == 4

    def test_max_turns_positive(self):
        from arena.constants import MAX_TURNS
        assert isinstance(MAX_TURNS, int)
        assert MAX_TURNS > 0

    def test_repo_root_contains_arena(self):
        from arena.constants import REPO_ROOT
        assert (REPO_ROOT / "arena").is_dir()

    def test_repo_root_contains_attacks(self):
        from arena.constants import REPO_ROOT
        assert (REPO_ROOT / "attacks").is_dir()
