"""Tests for arena/cli.py — argument parsing, client construction, CI mode."""

import json
from io import StringIO
from unittest.mock import MagicMock, patch

import pytest

from arena.cli import build_parser, handle_output, make_client


# ---------------------------------------------------------------------------
# build_parser — defaults and choices
# ---------------------------------------------------------------------------

class TestBuildParser:
    def test_default_models(self):
        parser = build_parser()
        args = parser.parse_args([])
        assert args.red_model == "deepseek-r1:8b"
        assert args.blue_model == "deepseek-r1:8b"

    def test_default_blue_mode(self):
        args = build_parser().parse_args([])
        assert args.blue_mode == "both"

    def test_default_rounds(self):
        args = build_parser().parse_args([])
        assert args.rounds == 3

    def test_default_scenario(self):
        args = build_parser().parse_args([])
        assert args.scenario == "freestyle"

    def test_custom_models(self):
        args = build_parser().parse_args([
            "--red-model", "gpt-4o",
            "--blue-model", "claude-sonnet-4-20250514",
        ])
        assert args.red_model == "gpt-4o"
        assert args.blue_model == "claude-sonnet-4-20250514"

    def test_ci_flag(self):
        args = build_parser().parse_args(["--ci"])
        assert args.ci is True

    def test_visualize_flag(self):
        args = build_parser().parse_args(["--visualize"])
        assert args.visualize is True

    def test_output_path(self):
        args = build_parser().parse_args(["--output", "/tmp/test.json"])
        assert args.output == "/tmp/test.json"

    def test_red_temp_float(self):
        args = build_parser().parse_args(["--red-temp", "0.7"])
        assert args.red_temp == 0.7

    def test_per_agent_overrides(self):
        args = build_parser().parse_args([
            "--red-api-base", "http://red:8000/v1",
            "--red-api-key", "red-key",
            "--blue-api-base", "http://blue:8000/v1",
            "--blue-api-key", "blue-key",
        ])
        assert args.red_api_base == "http://red:8000/v1"
        assert args.blue_api_key == "blue-key"

    def test_invalid_blue_mode_rejected(self):
        with pytest.raises(SystemExit):
            build_parser().parse_args(["--blue-mode", "invalid"])

    def test_judge_model_defaults_none(self):
        args = build_parser().parse_args([])
        assert args.judge_model is None


# ---------------------------------------------------------------------------
# make_client
# ---------------------------------------------------------------------------

class TestMakeClient:
    @patch("arena.cli.ChatClient")
    def test_non_claude_uses_api_base(self, mock_cls):
        make_client("deepseek-r1:8b", "ollama", "http://localhost:11434/v1")
        mock_cls.assert_called_once_with(
            model="deepseek-r1:8b",
            api_key="ollama",
            api_base="http://localhost:11434/v1",
        )

    @patch("arena.cli.ChatClient")
    def test_claude_uses_env_key(self, mock_cls):
        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "sk-ant-test"}):
            make_client("claude-sonnet-4-20250514", "ollama", "http://localhost:11434/v1")
        mock_cls.assert_called_once_with(
            model="claude-sonnet-4-20250514",
            api_key="sk-ant-test",
        )

    @patch("arena.cli.ChatClient")
    def test_claude_with_explicit_key(self, mock_cls):
        make_client("claude-sonnet-4-20250514", "sk-ant-explicit", "http://x")
        mock_cls.assert_called_once_with(
            model="claude-sonnet-4-20250514",
            api_key="sk-ant-explicit",
        )

    def test_claude_no_key_exits(self):
        with patch.dict("os.environ", {}, clear=True):
            # Remove ANTHROPIC_API_KEY if present
            import os
            env_backup = os.environ.pop("ANTHROPIC_API_KEY", None)
            try:
                with pytest.raises(SystemExit):
                    make_client("claude-sonnet-4-20250514", "ollama", "http://x")
            finally:
                if env_backup:
                    os.environ["ANTHROPIC_API_KEY"] = env_backup


# ---------------------------------------------------------------------------
# handle_output — CI mode
# ---------------------------------------------------------------------------

class TestHandleOutputCI:
    def _make_args(self, **kwargs):
        defaults = {
            "ci": True, "quiet": True, "output": None,
            "visualize": False, "secret": "AE-SECRET-7429",
        }
        defaults.update(kwargs)
        return type("Args", (), defaults)()

    def test_ci_pass_exit_0(self):
        from tests.conftest import make_result
        results = [make_result("naive", leaked=False)]
        args = self._make_args()
        with patch("sys.stdout", new_callable=StringIO) as out:
            with pytest.raises(SystemExit) as exc_info:
                handle_output(args, results)
        assert exc_info.value.code == 0
        summary = json.loads(out.getvalue())
        assert summary["pass"] is True

    def test_ci_fail_exit_1(self):
        from tests.conftest import make_result
        results = [make_result("naive", leaked=True, turns=2)]
        args = self._make_args()
        with patch("sys.stdout", new_callable=StringIO) as out:
            with pytest.raises(SystemExit) as exc_info:
                handle_output(args, results)
        assert exc_info.value.code == 1
        summary = json.loads(out.getvalue())
        assert summary["pass"] is False
        assert summary["compromised"] == 1

    def test_ci_summary_structure(self):
        from tests.conftest import make_result
        results = [
            make_result("naive", leaked=True, scenario="s1", turns=2),
            make_result("hardened", leaked=False, scenario="s1"),
        ]
        args = self._make_args()
        with patch("sys.stdout", new_callable=StringIO) as out:
            with pytest.raises(SystemExit):
                handle_output(args, results)
        summary = json.loads(out.getvalue())
        assert "total_rounds" in summary
        assert "compromised" in summary
        assert "held" in summary
        assert "compromise_rate" in summary
        assert "scenarios" in summary
        assert "modes" in summary
