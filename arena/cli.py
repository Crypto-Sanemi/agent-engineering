"""CLI entry point for the Agent Engineering Arena."""

import argparse
import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from arena.client import ChatClient, is_claude_model
from arena.constants import DEFAULT_SECRET, MAX_TURNS
from arena.reporting import print_scorecard
from arena.runner import Arena
from arena.scenarios import SCENARIOS


def make_client(model: str, api_key: str, api_base: str) -> ChatClient:
    """Build a ChatClient with the right SDK based on model name."""
    if is_claude_model(model):
        key = api_key if api_key != "ollama" else os.getenv("ANTHROPIC_API_KEY", "")
        if not key:
            print(f"\n❌ Model '{model}' needs an Anthropic API key.")
            print(f"   Set ANTHROPIC_API_KEY or use --red-api-key / --blue-api-key")
            sys.exit(1)
        return ChatClient(model=model, api_key=key)
    else:
        return ChatClient(model=model, api_key=api_key, api_base=api_base)


def _run_visualize(results, secret, output_dir, open_browser=True):
    """Import and run visualize.py to generate HTML replay."""
    try:
        from visualize import visualize_from_data
        visualize_from_data(results, secret=secret, output_dir=output_dir,
                            open_browser=open_browser)
    except ImportError:
        import importlib.util
        viz_path = Path(__file__).parent / "visualize.py"
        if viz_path.exists():
            spec = importlib.util.spec_from_file_location("visualize", viz_path)
            viz = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(viz)
            viz.visualize_from_data(results, secret=secret, output_dir=output_dir,
                                    open_browser=open_browser)
        else:
            print(f"  ⚠️  visualize.py not found at {viz_path}")
            print(f"  Run manually: python arena/visualize.py <detailed-json-path>")


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the Arena CLI."""
    parser = argparse.ArgumentParser(
        description="Agent Engineering Arena — Provider-Agnostic Red vs Blue Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # DeepSeek vs DeepSeek (Ollama, zero config)
  python arena.py

  # DeepSeek attacks Claude
  python arena.py --blue-model claude-sonnet-4-20250514 --blue-api-key sk-ant-...

  # Claude attacks DeepSeek
  python arena.py --red-model claude-sonnet-4-20250514 --red-api-key sk-ant-...

  # Claude vs Claude
  python arena.py --red-model claude-sonnet-4-20250514 --blue-model claude-sonnet-4-20250514

  # OpenAI vs Ollama
  python arena.py --red-model gpt-4o --red-api-base https://api.openai.com/v1 --red-api-key sk-... \\
                  --blue-model deepseek-r1:8b

  # Full benchmark with output
  python arena.py --blue-mode both --scenario all --rounds 5 --output arena/results/run1.json

  # Run + auto-open visual replay in browser
  python arena.py --output arena/results/run1.json --visualize

  # Replay existing results (no arena run needed)
  python arena/visualize.py arena/results/run1.detailed.json

Provider auto-detection:
  Model name contains "claude" or "anthropic" → uses Anthropic SDK
  Anything else → uses OpenAI-compatible SDK (defaults to Ollama localhost)
        """,
    )
    # Shared defaults
    parser.add_argument("--api-base", default=os.getenv("ARENA_API_BASE", "http://localhost:11434/v1"),
                        help="Default API base for OpenAI-compatible models (default: Ollama)")
    parser.add_argument("--api-key", default=os.getenv("ARENA_API_KEY", "ollama"),
                        help="Default API key for OpenAI-compatible models")

    # Per-agent overrides
    parser.add_argument("--red-api-base", default=os.getenv("RED_API_BASE", None))
    parser.add_argument("--red-api-key", default=os.getenv("RED_API_KEY", None))
    parser.add_argument("--blue-api-base", default=os.getenv("BLUE_API_BASE", None))
    parser.add_argument("--blue-api-key", default=os.getenv("BLUE_API_KEY", None))
    parser.add_argument("--judge-api-base", default=os.getenv("JUDGE_API_BASE", None))
    parser.add_argument("--judge-api-key", default=os.getenv("JUDGE_API_KEY", None))

    # Models
    parser.add_argument("--red-model", default="deepseek-r1:8b", help="Red agent model")
    parser.add_argument("--blue-model", default="deepseek-r1:8b", help="Blue agent model")
    parser.add_argument("--judge-model", default=None, help="Judge model (defaults to blue model)")

    # Arena config
    parser.add_argument("--secret", default=DEFAULT_SECRET)
    parser.add_argument("--max-turns", type=int, default=MAX_TURNS)
    parser.add_argument("--rounds", type=int, default=3)
    parser.add_argument("--scenario", default="freestyle",
                        choices=list(SCENARIOS.keys()) + ["all"])
    parser.add_argument("--blue-mode", default="both",
                        choices=["naive", "hardened", "both"])
    parser.add_argument("--output", default=None, help="Save results to JSON file")
    parser.add_argument("--visualize", action="store_true",
                        help="Generate interactive HTML replay (auto-opens in browser)")
    parser.add_argument("--red-temp", type=float, default=1.0,
                        help="Red agent temperature (default: 1.0 for maximum creativity)")
    parser.add_argument("--quiet", action="store_true")
    parser.add_argument("--ci", action="store_true",
                        help="CI mode: JSON summary to stdout, exit code 1 if any secret leaked")
    return parser


def run_arena(args) -> list:
    """Build clients and run all arena rounds. Returns list of results."""
    # Resolve per-agent configs
    red_base = args.red_api_base or args.api_base
    red_key = args.red_api_key or args.api_key
    blue_base = args.blue_api_base or args.api_base
    blue_key = args.blue_api_key or args.api_key
    judge_model = args.judge_model or args.blue_model
    judge_base = args.judge_api_base or blue_base
    judge_key = args.judge_api_key or blue_key

    # Build clients
    red_client = make_client(args.red_model, red_key, red_base)
    blue_client = make_client(args.blue_model, blue_key, blue_base)
    judge_client = make_client(judge_model, judge_key, judge_base)

    if not args.quiet:
        print(f"\n🏟️  AGENT ENGINEERING ARENA")
        print(f"  🔴 Red:   {red_client.label}")
        print(f"  🔵 Blue:  {blue_client.label}")
        print(f"  ⚖️  Judge: {judge_client.label}")
        print()

    arena = Arena(red=red_client, blue=blue_client, judge=judge_client,
                  red_temp=args.red_temp)

    scenarios = list(SCENARIOS.keys()) if args.scenario == "all" else [args.scenario]
    modes = ["naive", "hardened"] if args.blue_mode == "both" else [args.blue_mode]

    all_results = []
    total_runs = len(scenarios) * len(modes) * args.rounds
    run_count = 0

    for scenario in scenarios:
        for mode in modes:
            for round_num in range(1, args.rounds + 1):
                run_count += 1
                if not args.quiet:
                    print(f"\n[{run_count}/{total_runs}] Scenario: {scenario} | Mode: {mode} | Round: {round_num}")

                result = arena.run_round(
                    secret=args.secret,
                    hardened=(mode == "hardened"),
                    max_turns=args.max_turns,
                    scenario_instruction=SCENARIOS[scenario],
                    verbose=not args.quiet,
                )
                result["scenario"] = scenario
                result["round"] = round_num
                result["red_model"] = args.red_model
                result["blue_model"] = args.blue_model
                all_results.append(result)

                leaked = result["judge"].get("secret_leaked", False)
                status = "❌ COMPROMISED" if leaked else "✅ HELD"
                if not args.quiet:
                    print(f"\n  Result: {status}")
                    print(f"  Judge: {result['judge'].get('analysis', 'N/A')}")

                # Incremental save after each round
                if args.output:
                    detailed_path = Path(args.output).with_suffix(".detailed.json")
                    detailed_path.parent.mkdir(parents=True, exist_ok=True)
                    detailed_path.write_text(json.dumps(all_results, indent=2, default=str))

    return all_results


def handle_output(args, all_results: list):
    """Save results, print scorecard, generate visualizations, handle CI mode."""
    if not args.ci:
        print_scorecard(all_results, args.secret)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        compact = [
            {k: v for k, v in r.items() if k != "conversation"}
            for r in all_results
        ]
        out_path.write_text(json.dumps(compact, indent=2))
        detailed_path = out_path.with_suffix(".detailed.json")
        detailed_path.write_text(json.dumps(all_results, indent=2, default=str))
        print(f"\n  Results saved to {out_path}")
        print(f"  Full logs saved to {detailed_path}")

    # Generate visual replay
    if args.visualize and all_results:
        output_dir = Path(args.output).parent if args.output else Path(__file__).parent / "results"
        output_dir.mkdir(parents=True, exist_ok=True)
        if not args.output:
            timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
            auto_path = output_dir / f"run_{timestamp}.json"
            auto_path.write_text(json.dumps(all_results, indent=2, default=str))
            print(f"\n  Auto-saved results to {auto_path}")
        _run_visualize(all_results, args.secret, output_dir)

    # CI mode: JSON summary to stdout + exit code
    if args.ci:
        any_leaked = any(r["judge"].get("secret_leaked") for r in all_results)
        total = len(all_results)
        compromised = sum(1 for r in all_results if r["judge"].get("secret_leaked"))
        summary = {
            "total_rounds": total,
            "compromised": compromised,
            "held": total - compromised,
            "compromise_rate": round(compromised / total, 3) if total else 0,
            "pass": not any_leaked,
            "scenarios": list({r["scenario"] for r in all_results}),
            "modes": list({r["blue_mode"] for r in all_results}),
        }
        print(json.dumps(summary, indent=2))
        sys.exit(1 if any_leaked else 0)


def main():
    """CLI entry point: parse args, run arena, handle output."""
    parser = build_parser()
    args = parser.parse_args()

    # CI mode implies quiet
    if args.ci:
        args.quiet = True

    all_results = run_arena(args)
    handle_output(args, all_results)


if __name__ == "__main__":
    main()
