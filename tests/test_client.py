"""Tests for arena/client.py — ChatClient error handling and properties."""

import arena.client as client_module
from unittest.mock import MagicMock, patch

import pytest

from arena.client import ChatClient, is_claude_model, strip_thinking


def _inject_openai_mock():
    """Inject a mock OpenAI class into arena.client when openai isn't installed."""
    mock_cls = MagicMock()
    if not hasattr(client_module, "OpenAI") or not client_module.OPENAI_AVAILABLE:
        client_module.OpenAI = mock_cls
    return mock_cls


# ---------------------------------------------------------------------------
# ChatClient construction
# ---------------------------------------------------------------------------

class TestChatClientInit:
    def test_openai_provider_for_non_claude(self):
        mock_cls = _inject_openai_mock()
        try:
            with patch.object(client_module, "OPENAI_AVAILABLE", True), \
                 patch.object(client_module, "OpenAI", mock_cls):
                client = ChatClient("deepseek-r1:8b", api_key="test",
                                    api_base="http://localhost:11434/v1")
            assert client.provider == "openai"
            mock_cls.assert_called_once()
        finally:
            pass

    @patch("arena.client.ANTHROPIC_AVAILABLE", True)
    @patch("arena.client.anthropic")
    def test_anthropic_provider_for_claude(self, mock_anthropic):
        mock_anthropic.Anthropic = MagicMock()
        client = ChatClient("claude-sonnet-4-20250514", api_key="sk-test")
        assert client.provider == "anthropic"


# ---------------------------------------------------------------------------
# ChatClient.chat() error handling
# ---------------------------------------------------------------------------

class TestChatClientChat:
    def test_returns_error_string_on_exception(self):
        mock_cls = MagicMock()
        mock_oai_client = MagicMock()
        mock_oai_client.chat.completions.create.side_effect = RuntimeError("connection refused")
        mock_cls.return_value = mock_oai_client
        with patch.object(client_module, "OPENAI_AVAILABLE", True), \
             patch.object(client_module, "OpenAI", mock_cls, create=True):
            client = ChatClient("test-model", api_key="test",
                                api_base="http://localhost:1")
            result = client.chat([{"role": "user", "content": "hi"}], 0.5)
        assert result.startswith("[ERROR:")
        assert "connection refused" in result

    def test_strips_thinking_from_response(self):
        mock_cls = MagicMock()
        mock_resp = MagicMock()
        mock_resp.choices = [MagicMock()]
        mock_resp.choices[0].message.content = "<think>reasoning</think>Clean output"
        mock_oai_client = MagicMock()
        mock_oai_client.chat.completions.create.return_value = mock_resp
        mock_cls.return_value = mock_oai_client
        with patch.object(client_module, "OPENAI_AVAILABLE", True), \
             patch.object(client_module, "OpenAI", mock_cls, create=True):
            client = ChatClient("test-model", api_key="test",
                                api_base="http://localhost:1")
            result = client.chat([{"role": "user", "content": "hi"}], 0.5)
        assert "<think>" not in result
        assert result == "Clean output"


# ---------------------------------------------------------------------------
# ChatClient.label
# ---------------------------------------------------------------------------

class TestChatClientLabel:
    @patch("arena.client.ANTHROPIC_AVAILABLE", True)
    @patch("arena.client.anthropic")
    def test_anthropic_label(self, mock_anthropic):
        mock_anthropic.Anthropic = MagicMock()
        client = ChatClient("claude-sonnet-4-20250514", api_key="sk-test")
        assert "claude-sonnet" in client.label
        assert "Anthropic" in client.label

    def test_openai_label_includes_base(self):
        mock_cls = MagicMock()
        mock_oai_client = MagicMock()
        mock_oai_client._base_url = "http://localhost:11434/v1"
        mock_cls.return_value = mock_oai_client
        with patch.object(client_module, "OPENAI_AVAILABLE", True), \
             patch.object(client_module, "OpenAI", mock_cls, create=True):
            client = ChatClient("deepseek-r1:8b", api_key="test",
                                api_base="http://localhost:11434/v1")
        assert "deepseek-r1:8b" in client.label
        assert "localhost" in client.label


# ---------------------------------------------------------------------------
# ChatClient._chat_anthropic system prompt extraction
# ---------------------------------------------------------------------------

class TestAnthropicSystemExtraction:
    @patch("arena.client.ANTHROPIC_AVAILABLE", True)
    @patch("arena.client.anthropic")
    def test_system_message_extracted(self, mock_anthropic):
        mock_resp = MagicMock()
        mock_block = MagicMock()
        mock_block.text = "Hello"
        mock_resp.content = [mock_block]
        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_resp
        mock_anthropic.Anthropic.return_value = mock_client_instance

        client = ChatClient("claude-sonnet-4-20250514", api_key="sk-test")
        messages = [
            {"role": "system", "content": "You are helpful."},
            {"role": "user", "content": "Hi"},
        ]
        client.chat(messages, 0.5)

        call_kwargs = mock_client_instance.messages.create.call_args
        assert call_kwargs.kwargs["system"] == "You are helpful."
        chat_msgs = call_kwargs.kwargs["messages"]
        assert all(m["role"] != "system" for m in chat_msgs)

    @patch("arena.client.ANTHROPIC_AVAILABLE", True)
    @patch("arena.client.anthropic")
    def test_empty_messages_adds_begin(self, mock_anthropic):
        """System-only messages should still produce a valid API call."""
        mock_resp = MagicMock()
        mock_block = MagicMock()
        mock_block.text = "OK"
        mock_resp.content = [mock_block]
        mock_client_instance = MagicMock()
        mock_client_instance.messages.create.return_value = mock_resp
        mock_anthropic.Anthropic.return_value = mock_client_instance

        client = ChatClient("claude-sonnet-4-20250514", api_key="sk-test")
        messages = [{"role": "system", "content": "System prompt only."}]
        client.chat(messages, 0.5)

        call_kwargs = mock_client_instance.messages.create.call_args
        chat_msgs = call_kwargs.kwargs["messages"]
        assert len(chat_msgs) == 1
        assert chat_msgs[0]["content"] == "Begin."


# ---------------------------------------------------------------------------
# Parametrized is_claude_model edge cases
# ---------------------------------------------------------------------------

class TestIsClaudeModelParametrized:
    @pytest.mark.parametrize("model,expected", [
        ("claude-3.5-haiku", True),
        ("anthropic.claude-v3-sonnet", True),
        ("CLAUDE-OPUS-4", True),
        ("my-claude-fine-tune", True),
        ("deepseek-r1:8b", False),
        ("gpt-4o-mini", False),
        ("llama-3.3-70b-versatile", False),
        ("gemini-1.5-pro", False),
        ("qwen/qwen3-32b", False),
        ("", False),
    ])
    def test_detection(self, model, expected):
        assert is_claude_model(model) is expected
