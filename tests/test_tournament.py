"""Tests for arena/tournament.py — leaderboard aggregation and formatting."""

import json
import tempfile
from pathlib import Path

import pytest

from arena.tournament import (
    build_leaderboard,
    format_pct,
    format_ttc,
    generate_markdown,
    load_results,
)
from tests.conftest import make_result


# ---------------------------------------------------------------------------
# format_pct / format_ttc
# ---------------------------------------------------------------------------

class TestFormatHelpers:
    @pytest.mark.parametrize("val,expected", [
        (0.0, "0%"),
        (0.5, "50%"),
        (1.0, "100%"),
        (0.333, "33%"),
        (None, "-"),
    ])
    def test_format_pct(self, val, expected):
        assert format_pct(val) == expected

    @pytest.mark.parametrize("val,expected", [
        (2.0, "2.0"),
        (3.5, "3.5"),
        (None, "-"),
    ])
    def test_format_ttc(self, val, expected):
        assert format_ttc(val) == expected


# ---------------------------------------------------------------------------
# load_results
# ---------------------------------------------------------------------------

class TestLoadResults:
    def test_loads_from_file(self):
        data = [make_result()]
        with tempfile.NamedTemporaryFile(suffix=".json", mode="w", delete=False) as f:
            json.dump(data, f)
            f.flush()
            results = load_results([Path(f.name)])
        assert len(results) == 1

    def test_loads_from_directory(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "run.detailed.json"
            p.write_text(json.dumps([make_result(), make_result()]))
            results = load_results([Path(d)])
        assert len(results) == 2

    def test_skips_non_detailed_json(self):
        """Only *.detailed.json files are loaded from directories."""
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "run.json").write_text(json.dumps([make_result()]))
            results = load_results([Path(d)])
        assert len(results) == 0

    def test_skips_invalid_json(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d) / "bad.detailed.json"
            p.write_text("not json")
            results = load_results([Path(d)])
        assert len(results) == 0

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as d:
            results = load_results([Path(d)])
        assert results == []

    def test_multiple_files(self):
        with tempfile.TemporaryDirectory() as d:
            for i in range(3):
                p = Path(d) / f"run{i}.detailed.json"
                p.write_text(json.dumps([make_result()]))
            results = load_results([Path(d)])
        assert len(results) == 3


# ---------------------------------------------------------------------------
# build_leaderboard
# ---------------------------------------------------------------------------

class TestBuildLeaderboard:
    def test_single_model(self):
        results = [
            make_result("naive", leaked=True, red_model="model-a", turns=2),
            make_result("naive", leaked=False, red_model="model-a"),
        ]
        lb = build_leaderboard(results)
        assert len(lb) == 1
        assert lb[0]["red_model"] == "model-a"
        assert lb[0]["rounds"] == 2
        assert lb[0]["compromised"] == 1
        assert lb[0]["rate"] == 0.5

    def test_multiple_models_sorted_by_rate(self):
        results = [
            make_result("naive", leaked=True, red_model="good-red", turns=2),
            make_result("naive", leaked=True, red_model="good-red", turns=3),
            make_result("naive", leaked=False, red_model="bad-red"),
            make_result("naive", leaked=False, red_model="bad-red"),
        ]
        lb = build_leaderboard(results)
        assert lb[0]["red_model"] == "good-red"
        assert lb[0]["rate"] == 1.0
        assert lb[1]["red_model"] == "bad-red"
        assert lb[1]["rate"] == 0.0

    def test_naive_vs_hardened_rates(self):
        results = [
            make_result("naive", leaked=True, red_model="m", turns=2),
            make_result("naive", leaked=True, red_model="m", turns=3),
            make_result("hardened", leaked=False, red_model="m"),
            make_result("hardened", leaked=True, red_model="m", turns=5),
        ]
        lb = build_leaderboard(results)
        assert lb[0]["naive_rate"] == 1.0
        assert lb[0]["hardened_rate"] == 0.5

    def test_avg_turns_to_compromise(self):
        results = [
            make_result("naive", leaked=True, red_model="m", turns=2),
            make_result("naive", leaked=True, red_model="m", turns=4),
        ]
        lb = build_leaderboard(results)
        assert lb[0]["avg_turns_to_compromise"] == 3.0

    def test_no_compromise_avg_ttc_none(self):
        results = [make_result("naive", leaked=False, red_model="m")]
        lb = build_leaderboard(results)
        assert lb[0]["avg_turns_to_compromise"] is None

    def test_top_technique_tracked(self):
        results = [
            make_result("naive", leaked=True, red_model="m",
                        technique="auth", turns=2),
            make_result("naive", leaked=False, red_model="m",
                        technique="auth"),
            make_result("naive", leaked=False, red_model="m",
                        technique="rapport"),
        ]
        lb = build_leaderboard(results)
        assert lb[0]["top_technique"] == "auth"

    def test_empty_results(self):
        assert build_leaderboard([]) == []

    def test_tiebreak_by_avg_ttc(self):
        """Same rate => faster TTC ranks higher."""
        results = [
            make_result("naive", leaked=True, red_model="slow", turns=8),
            make_result("naive", leaked=True, red_model="fast", turns=2),
        ]
        lb = build_leaderboard(results)
        assert lb[0]["red_model"] == "fast"

    def test_blue_models_tracked(self):
        results = [
            make_result("naive", red_model="m", blue_model="blue-a"),
            make_result("naive", red_model="m", blue_model="blue-b"),
        ]
        lb = build_leaderboard(results)
        assert sorted(lb[0]["blue_models"]) == ["blue-a", "blue-b"]


# ---------------------------------------------------------------------------
# generate_markdown
# ---------------------------------------------------------------------------

class TestGenerateMarkdown:
    def test_has_table_header(self):
        results = [make_result("naive", leaked=True, red_model="m", turns=2)]
        lb = build_leaderboard(results)
        md = generate_markdown(lb)
        assert "| Rank |" in md
        assert "Red Model" in md

    def test_contains_model_name(self):
        results = [make_result("naive", red_model="my-model")]
        lb = build_leaderboard(results)
        md = generate_markdown(lb)
        assert "my-model" in md

    def test_best_red_line(self):
        results = [make_result("naive", leaked=True, red_model="winner", turns=2)]
        lb = build_leaderboard(results)
        md = generate_markdown(lb)
        assert "**Best Red:** winner" in md

    def test_no_compromise_no_best_line(self):
        results = [make_result("naive", leaked=False, red_model="m")]
        lb = build_leaderboard(results)
        md = generate_markdown(lb)
        assert "Best Red" not in md
