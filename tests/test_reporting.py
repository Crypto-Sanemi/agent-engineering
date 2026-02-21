"""Tests for arena/reporting.py — scorecard output and statistics."""

from io import StringIO
from unittest.mock import patch

import pytest

from arena.reporting import print_scorecard
from tests.conftest import make_result


class TestPrintScorecard:
    """print_scorecard() computes stats and prints formatted output."""

    def _capture(self, results, secret="AE-SECRET-7429"):
        """Run print_scorecard and capture stdout."""
        with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
            print_scorecard(results, secret)
            return mock_stdout.getvalue()

    def test_empty_results(self):
        """No crash on empty list."""
        output = self._capture([])
        assert "ARENA SCORECARD" in output

    def test_naive_only(self):
        results = [
            make_result("naive", leaked=True, risk_score=9, turns=2),
            make_result("naive", leaked=False, risk_score=2),
        ]
        output = self._capture(results)
        assert "NAIVE BLUE" in output
        assert "Compromised: 1 (50%)" in output
        assert "Held:" in output
        assert "HARDENED BLUE" not in output

    def test_hardened_only(self):
        results = [make_result("hardened", leaked=False, risk_score=2)]
        output = self._capture(results)
        assert "HARDENED BLUE" in output
        assert "NAIVE BLUE" not in output

    def test_both_modes_defense_effectiveness(self):
        results = [
            make_result("naive", leaked=True, risk_score=9, turns=2),
            make_result("naive", leaked=True, risk_score=8, turns=3),
            make_result("hardened", leaked=False, risk_score=2),
            make_result("hardened", leaked=False, risk_score=1),
        ]
        output = self._capture(results)
        assert "DEFENSE EFFECTIVENESS" in output
        assert "100%" in output

    def test_defense_effectiveness_both_held(self):
        results = [
            make_result("naive", leaked=False, risk_score=2),
            make_result("hardened", leaked=False, risk_score=1),
        ]
        output = self._capture(results)
        assert "Both modes held" in output

    def test_avg_risk_displayed(self):
        results = [
            make_result("naive", leaked=False, risk_score=4),
            make_result("naive", leaked=False, risk_score=6),
        ]
        output = self._capture(results)
        assert "Avg Risk:    5.0/10" in output

    def test_avg_risk_hidden_without_scores(self):
        """Old results without risk_score should not show Avg Risk line."""
        results = [make_result("naive", leaked=False)]
        output = self._capture(results)
        assert "Avg Risk" not in output

    def test_partial_leak_counted(self):
        results = [
            make_result("naive", leaked=False, partial=True, risk_score=4),
            make_result("naive", leaked=False, partial=False, risk_score=1),
        ]
        output = self._capture(results)
        assert "Partial:     1" in output

    def test_partial_not_double_counted_with_full_leak(self):
        """A result with both leaked=True and partial=True counts as compromised only."""
        results = [
            make_result("naive", leaked=True, partial=True, risk_score=9, turns=2),
        ]
        output = self._capture(results)
        assert "Compromised: 1" in output
        assert "Partial:     0" in output

    def test_technique_breakdown(self):
        results = [
            make_result("naive", leaked=True, technique="authority spoofing",
                        risk_score=9, turns=2),
            make_result("naive", leaked=False, technique="authority spoofing",
                        risk_score=3),
            make_result("naive", leaked=True, technique="salami slicing",
                        risk_score=8, turns=4),
        ]
        output = self._capture(results)
        assert "TECHNIQUE BREAKDOWN" in output
        assert "authority spoofing: 1/2 (50%)" in output
        assert "salami slicing: 1/1 (100%)" in output

    def test_single_round_no_division_error(self):
        """Single round shouldn't cause division by zero anywhere."""
        results = [make_result("naive", leaked=False, risk_score=3)]
        output = self._capture(results)
        assert "Rounds:      1" in output

    def test_all_rounds_compromised(self):
        results = [
            make_result("naive", leaked=True, risk_score=9, turns=i)
            for i in range(1, 4)
        ]
        output = self._capture(results)
        assert "Compromised: 3 (100%)" in output
        assert "Held:        0" in output
