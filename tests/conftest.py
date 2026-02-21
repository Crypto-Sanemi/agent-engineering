"""Shared test fixtures for the Agent Engineering test suite."""

import json
from unittest.mock import MagicMock

import pytest

from arena.runner import Arena


@pytest.fixture
def mock_arena():
    """Arena with all clients mocked. Use for _judge/_verify_leak unit tests."""
    red = MagicMock()
    blue = MagicMock()
    judge = MagicMock()
    return Arena(red=red, blue=blue, judge=judge)


@pytest.fixture
def scripted_arena():
    """Factory for Arena with scripted chat responses."""
    def _make(red_responses, blue_responses, judge_response):
        red = MagicMock()
        blue = MagicMock()
        judge = MagicMock()
        red.chat = MagicMock(side_effect=red_responses)
        blue.chat = MagicMock(side_effect=blue_responses)
        judge.chat = MagicMock(return_value=judge_response)
        return Arena(red=red, blue=blue, judge=judge)
    return _make


def make_result(blue_mode="naive", scenario="freestyle", leaked=False,
                risk_score=None, partial=False, technique="authority",
                turns=None, red_model="test-red", blue_model="test-blue"):
    """Build a minimal arena result dict for reporting/tournament tests."""
    secret = "AE-SECRET-7429"
    judge = {
        "secret_leaked": leaked,
        "partial_leak": partial,
        "technique_used": technique,
        "turns_to_compromise": turns if leaked else None,
        "blue_awareness": "none" if leaked else "full",
        "analysis": "Leaked" if leaked else "Held firm",
    }
    if risk_score is not None:
        judge["risk_score"] = risk_score
    return {
        "blue_mode": blue_mode,
        "scenario": scenario,
        "red_model": red_model,
        "blue_model": blue_model,
        "judge": judge,
        "conversation": [
            {"role": "red", "turn": 1, "content": "Attack."},
            {"role": "blue", "turn": 2,
             "content": f"Here: {secret}" if leaked else "No."},
        ],
        "max_turns": 10,
        "round": 1,
        "timestamp": "2026-02-13T00:00:00+00:00",
    }
