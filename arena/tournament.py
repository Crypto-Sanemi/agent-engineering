#!/usr/bin/env python3
"""
Red Model Tournament — Compare Red agent performance across models.

Usage:
    # Run each Red model one at a time, saving to tournament directory:
    python arena/arena.py --red-model phi3:14b --output arena/results/tournament/phi3-14b.json ...
    python arena/arena.py --red-model dolphin-llama3:8b --output arena/results/tournament/dolphin-llama3.json ...

    # Compare all results:
    python arena/tournament.py arena/results/tournament/

    # Compare specific files:
    python arena/tournament.py arena/results/run1.detailed.json arena/results/run2.detailed.json

    # Save leaderboard as markdown:
    python arena/tournament.py arena/results/tournament/ --markdown arena/results/tournament/LEADERBOARD.md
"""

import json
import sys
from pathlib import Path


def load_results(paths: list[Path]) -> list[dict]:
    """Load all .detailed.json results from paths (files or directories)."""
    all_results = []
    for path in paths:
        if path.is_dir():
            for f in sorted(path.glob("*.detailed.json")):
                try:
                    data = json.loads(f.read_text())
                    if isinstance(data, list):
                        all_results.extend(data)
                except (json.JSONDecodeError, OSError) as e:
                    print(f"  [!] Skipping {f.name}: {e}")
        elif path.is_file() and path.suffix == ".json":
            try:
                data = json.loads(path.read_text())
                if isinstance(data, list):
                    all_results.extend(data)
            except (json.JSONDecodeError, OSError) as e:
                print(f"  [!] Skipping {path.name}: {e}")
    return all_results


def build_leaderboard(results: list[dict]) -> list[dict]:
    """Group results by red_model, compute stats, return sorted leaderboard."""
    models = {}
    for r in results:
        red = r.get("red_model", "unknown")
        if red not in models:
            models[red] = {
                "red_model": red,
                "blue_models": set(),
                "scenarios": set(),
                "rounds": 0,
                "naive_rounds": 0,
                "naive_compromised": 0,
                "hardened_rounds": 0,
                "hardened_compromised": 0,
                "turns_to_compromise": [],
                "techniques": {},
            }
        m = models[red]
        m["blue_models"].add(r.get("blue_model", "unknown"))
        m["scenarios"].add(r.get("scenario", "unknown"))
        m["rounds"] += 1

        leaked = r.get("judge", {}).get("secret_leaked", False)
        mode = r.get("blue_mode", "naive")

        if mode == "naive":
            m["naive_rounds"] += 1
            if leaked:
                m["naive_compromised"] += 1
        elif mode == "hardened":
            m["hardened_rounds"] += 1
            if leaked:
                m["hardened_compromised"] += 1

        if leaked:
            ttc = r.get("judge", {}).get("turns_to_compromise")
            if ttc is not None:
                m["turns_to_compromise"].append(ttc)

        tech = r.get("judge", {}).get("technique_used", "unknown")
        m["techniques"][tech] = m["techniques"].get(tech, 0) + 1

    # Compute derived stats and sort
    leaderboard = []
    for m in models.values():
        total_compromised = m["naive_compromised"] + m["hardened_compromised"]
        rate = total_compromised / m["rounds"] if m["rounds"] else 0
        naive_rate = (m["naive_compromised"] / m["naive_rounds"]
                      if m["naive_rounds"] else None)
        hardened_rate = (m["hardened_compromised"] / m["hardened_rounds"]
                        if m["hardened_rounds"] else None)
        avg_ttc = (sum(m["turns_to_compromise"]) / len(m["turns_to_compromise"])
                   if m["turns_to_compromise"] else None)
        top_technique = max(m["techniques"], key=m["techniques"].get) if m["techniques"] else "N/A"

        leaderboard.append({
            "red_model": m["red_model"],
            "blue_models": sorted(m["blue_models"]),
            "scenarios": sorted(m["scenarios"]),
            "rounds": m["rounds"],
            "compromised": total_compromised,
            "rate": rate,
            "naive_rate": naive_rate,
            "hardened_rate": hardened_rate,
            "avg_turns_to_compromise": avg_ttc,
            "top_technique": top_technique,
            "technique_count": len(m["techniques"]),
        })

    leaderboard.sort(key=lambda x: (-x["rate"], x["avg_turns_to_compromise"] or 999))
    return leaderboard


def format_pct(val):
    """Format a rate as percentage, or '-' if None."""
    if val is None:
        return "-"
    return f"{val * 100:.0f}%"


def format_ttc(val):
    """Format avg turns-to-compromise, or '-' if None."""
    if val is None:
        return "-"
    return f"{val:.1f}"


def print_leaderboard(leaderboard: list[dict]):
    """Print leaderboard to terminal with aligned columns."""
    if not leaderboard:
        print("No results found.")
        return

    blue_set = set()
    scenario_set = set()
    for entry in leaderboard:
        blue_set.update(entry["blue_models"])
        scenario_set.update(entry["scenarios"])

    print(f"\n{'='*78}")
    print("  RED MODEL TOURNAMENT — Leaderboard")
    print(f"{'='*78}")
    print(f"  Blue: {', '.join(sorted(blue_set))}")
    print(f"  Scenarios: {', '.join(sorted(scenario_set))}")
    print()

    # Header
    header = (f"  {'Rank':<5} {'Red Model':<28} {'Rounds':>6} "
              f"{'Naive':>7} {'Hard':>7} {'Overall':>8} {'Avg TTC':>8} {'Top Technique'}")
    print(header)
    print(f"  {'-'*5} {'-'*28} {'-'*6} {'-'*7} {'-'*7} {'-'*8} {'-'*8} {'-'*20}")

    for i, entry in enumerate(leaderboard, 1):
        marker = "*" if i == 1 and entry["rate"] > 0 else " "
        row = (
            f" {marker}{i:<4} {entry['red_model']:<28} {entry['rounds']:>6} "
            f"{format_pct(entry['naive_rate']):>7} "
            f"{format_pct(entry['hardened_rate']):>7} "
            f"{format_pct(entry['rate']):>8} "
            f"{format_ttc(entry['avg_turns_to_compromise']):>8} "
            f"{entry['top_technique'][:30]}"
        )
        print(row)

    print()
    if leaderboard[0]["rate"] > 0:
        best = leaderboard[0]
        print(f"  Best Red: {best['red_model']} "
              f"({format_pct(best['rate'])} compromise rate)")
    else:
        print("  No model achieved any compromise.")
    print()


def generate_markdown(leaderboard: list[dict]) -> str:
    """Generate a markdown leaderboard table."""
    blue_set = set()
    scenario_set = set()
    for entry in leaderboard:
        blue_set.update(entry["blue_models"])
        scenario_set.update(entry["scenarios"])

    lines = [
        "# Red Model Tournament — Leaderboard",
        "",
        f"**Blue:** {', '.join(sorted(blue_set))}",
        f"**Scenarios:** {', '.join(sorted(scenario_set))}",
        "",
        "| Rank | Red Model | Rounds | Naive | Hardened | Overall | Avg TTC | Top Technique |",
        "|------|-----------|--------|-------|----------|---------|---------|---------------|",
    ]

    for i, entry in enumerate(leaderboard, 1):
        lines.append(
            f"| {i} | {entry['red_model']} | {entry['rounds']} | "
            f"{format_pct(entry['naive_rate'])} | {format_pct(entry['hardened_rate'])} | "
            f"{format_pct(entry['rate'])} | {format_ttc(entry['avg_turns_to_compromise'])} | "
            f"{entry['top_technique'][:40]} |"
        )

    lines.append("")
    if leaderboard and leaderboard[0]["rate"] > 0:
        best = leaderboard[0]
        lines.append(f"**Best Red:** {best['red_model']} "
                      f"({format_pct(best['rate'])} compromise rate)")
    lines.append("")
    return "\n".join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Red Model Tournament — Compare Red agent performance",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("paths", nargs="+", type=Path,
                        help="Result files (.detailed.json) or directories containing them")
    parser.add_argument("--markdown", type=Path, default=None,
                        help="Save leaderboard as markdown file")
    parser.add_argument("--json", type=Path, default=None,
                        help="Save leaderboard as JSON file")
    args = parser.parse_args()

    results = load_results(args.paths)
    if not results:
        print("No results found. Provide .detailed.json files or a directory containing them.")
        sys.exit(1)

    leaderboard = build_leaderboard(results)
    print_leaderboard(leaderboard)

    if args.markdown:
        md = generate_markdown(leaderboard)
        args.markdown.parent.mkdir(parents=True, exist_ok=True)
        args.markdown.write_text(md)
        print(f"  Saved: {args.markdown}")

    if args.json:
        # Convert sets to lists for JSON serialization
        serializable = []
        for entry in leaderboard:
            e = dict(entry)
            e["blue_models"] = list(e["blue_models"])
            e["scenarios"] = list(e["scenarios"])
            serializable.append(e)
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(serializable, indent=2))
        print(f"  Saved: {args.json}")


if __name__ == "__main__":
    main()
