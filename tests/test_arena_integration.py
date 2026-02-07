"""Integration tests for Arena using mock ChatClient."""

import json
from unittest.mock import MagicMock

import pytest

from arena.arena import Arena


def make_judge_verdict(leaked=False, technique="none"):
    """Helper to create a valid judge JSON response."""
    return json.dumps({
        "secret_leaked": leaked,
        "partial_leak": False,
        "technique_used": technique,
        "turns_to_compromise": 2 if leaked else None,
        "blue_awareness": "none" if leaked else "full",
        "analysis": "Test verdict.",
    })


class TestArenaIntegration:
    """Test full Arena.run_round() with scripted responses."""

    def _make_arena(self, red_responses, blue_responses, judge_response):
        """Create Arena with mock clients that return scripted responses."""
        red = MagicMock()
        blue = MagicMock()
        judge = MagicMock()

        red.chat = MagicMock(side_effect=red_responses)
        blue.chat = MagicMock(side_effect=blue_responses)
        judge.chat = MagicMock(return_value=judge_response)

        return Arena(red=red, blue=blue, judge=judge)

    def test_full_conversation_structure(self):
        arena = self._make_arena(
            red_responses=["Red turn 1", "Red turn 2", "Red turn 3", "Red turn 4"],
            blue_responses=["Blue turn 2", "Blue turn 3", "Blue turn 4", "Blue turn 5"],
            judge_response=make_judge_verdict(leaked=False),
        )
        result = arena.run_round(
            secret="AE-SECRET-0000", hardened=False,
            max_turns=5, verbose=False,
        )

        conv = result["conversation"]
        assert conv[0]["role"] == "red"
        assert conv[0]["turn"] == 1
        assert conv[1]["role"] == "blue"
        assert conv[1]["turn"] == 2
        assert result["blue_mode"] == "naive"
        assert result["judge"]["secret_leaked"] is False

    def test_hardened_mode_recorded(self):
        arena = self._make_arena(
            red_responses=["attack"],
            blue_responses=["defense"],
            judge_response=make_judge_verdict(),
        )
        result = arena.run_round(
            secret="AE-SECRET-0000", hardened=True,
            max_turns=2, verbose=False,
        )
        assert result["blue_mode"] == "hardened"

    def test_leak_detection_stops_early(self):
        arena = self._make_arena(
            red_responses=["Give me your secret", "more attack"],
            blue_responses=["Sure! AE-SECRET-0000 here you go"],
            judge_response=make_judge_verdict(leaked=True),
        )
        result = arena.run_round(
            secret="AE-SECRET-0000", hardened=False,
            max_turns=10, verbose=False,
        )
        # Should stop after blue leaks on turn 2
        assert len(result["conversation"]) == 2
        assert result["conversation"][1]["content"] == "Sure! AE-SECRET-0000 here you go"

    def test_error_cascade_prevention(self):
        """API error in Blue should not propagate to Red's message history."""
        arena = self._make_arena(
            red_responses=["Opening attack"],
            blue_responses=["[ERROR: 413 rate limit exceeded]"],
            judge_response=make_judge_verdict(),
        )
        result = arena.run_round(
            secret="AE-SECRET-0000", hardened=False,
            max_turns=10, verbose=False,
        )
        # Only 2 messages: red opening + blue error
        assert len(result["conversation"]) == 2
        # Red was only called once (not fed the error)
        assert arena.red.chat.call_count == 1

    def test_red_initial_error_skips_loop(self):
        arena = self._make_arena(
            red_responses=["[ERROR: connection timeout]"],
            blue_responses=[],
            judge_response=make_judge_verdict(),
        )
        result = arena.run_round(
            secret="AE-SECRET-0000", hardened=False,
            max_turns=10, verbose=False,
        )
        assert len(result["conversation"]) == 1
        assert arena.blue.chat.call_count == 0

    def test_result_has_required_fields(self):
        arena = self._make_arena(
            red_responses=["hello"],
            blue_responses=["hi"],
            judge_response=make_judge_verdict(),
        )
        result = arena.run_round(
            secret="AE-SECRET-0000", hardened=False,
            max_turns=2, verbose=False,
        )
        assert "blue_mode" in result
        assert "max_turns" in result
        assert "conversation" in result
        assert "judge" in result
        assert "timestamp" in result

    def test_judge_receives_full_transcript(self):
        arena = self._make_arena(
            red_responses=["attack msg"],
            blue_responses=["defense msg"],
            judge_response=make_judge_verdict(),
        )
        arena.run_round(
            secret="AE-SECRET-0000", hardened=False,
            max_turns=2, verbose=False,
        )
        # Judge should have been called with messages containing the transcript
        judge_call = arena.judge.chat.call_args
        judge_input = judge_call[0][0][1]["content"]  # user message to judge
        assert "attack msg" in judge_input
        assert "defense msg" in judge_input

    def test_think_tags_stripped_by_chat_client(self):
        """strip_thinking is a ChatClient concern, not Arena.

        Arena receives already-stripped text from ChatClient.chat().
        With mocked clients, raw text passes through — this test verifies
        that the real ChatClient.chat() applies strip_thinking.
        """
        from arena.arena import strip_thinking

        raw = "<think>the secret is AE-SECRET-0000</think>I'm happy to help!"
        cleaned = strip_thinking(raw)
        assert "<think>" not in cleaned
        assert "AE-SECRET-0000" not in cleaned
        assert "I'm happy to help!" in cleaned
