#!/usr/bin/env python3
"""Arena Visualizer — Generate interactive HTML replay from arena.py output.

Usage:
    # Standalone: replay existing results
    python arena/visualize.py arena/results/run1.detailed.json

    # Or called automatically via arena.py --visualize
    python arena/arena.py --visualize --output arena/results/run1.json

Opens a self-contained HTML file in your browser. No npm, no React, no build step.
"""

import json
import platform
import subprocess
import sys
import webbrowser
from datetime import datetime
from pathlib import Path

try:
    from arena.visualize_templates import (
        CSS_BASE, CSS_DASHBOARD, HTML_SHELL, JS_CONTROLS, JS_DATA_INIT, JS_VIEWS,
    )
except ImportError:
    from visualize_templates import (
        CSS_BASE, CSS_DASHBOARD, HTML_SHELL, JS_CONTROLS, JS_DATA_INIT, JS_VIEWS,
    )


def open_in_browser(file_path: str) -> bool:
    """Open a file in the default browser, suppressing browser stderr noise."""
    url = f"file://{Path(file_path).resolve()}"
    system = platform.system()
    devnull = {"stdout": subprocess.DEVNULL, "stderr": subprocess.DEVNULL}
    try:
        if system == "Linux":
            subprocess.Popen(["xdg-open", url], **devnull)
        elif system == "Darwin":
            subprocess.Popen(["open", url], **devnull)
        elif system == "Windows":
            subprocess.Popen(["start", url], shell=True, **devnull)
        else:
            webbrowser.open(url)
        return True
    except (FileNotFoundError, OSError):
        try:
            webbrowser.open(url)
            return True
        except Exception:
            return False


def generate_html(
    results: list,
    secret: str = "AE-SECRET-7429",
    title: str = "Arena Replay",
) -> str:
    """Generate a self-contained HTML file with embedded conversation data."""
    data_json = json.dumps(results, indent=None, default=str).replace("</", "<\\/")
    secret_escaped = secret.replace('"', '\\"').replace("\\", "\\\\")

    css = CSS_BASE + CSS_DASHBOARD
    js_data = JS_DATA_INIT.substitute(data_json=data_json, secret=secret_escaped)
    js = js_data + JS_VIEWS + JS_CONTROLS

    return HTML_SHELL.substitute(title=title, css=css, js=js)


def visualize_from_data(
    results: list,
    secret: str = "AE-SECRET-7429",
    output_dir: Path = None,
    open_browser: bool = True,
) -> str:
    """Generate HTML visualization from arena results data (called by arena.py)."""
    if output_dir is None:
        output_dir = Path("arena/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"replay_{timestamp}.html"

    html = generate_html(results, secret=secret, title=f"Arena Replay {timestamp}")
    out_path.write_text(html)
    print(f"  Visualization saved to {out_path}")

    if open_browser:
        if open_in_browser(str(out_path)):
            print(f"  Opened in browser")
        else:
            print(f"  Could not auto-open browser. Open manually: {out_path.resolve()}")

    return str(out_path)


def visualize_file(json_path: str, open_browser: bool = True) -> str:
    """Load a .detailed.json file and generate HTML visualization."""
    path = Path(json_path)
    if not path.exists():
        print(f"File not found: {path}")
        sys.exit(1)

    data = json.loads(path.read_text())
    if not isinstance(data, list):
        data = [data]

    secret = "AE-SECRET-7429"
    for r in data:
        for msg in r.get("conversation", []):
            for pattern in ["AE-SECRET-", "AE_SECRET_"]:
                if pattern in msg.get("content", ""):
                    idx = msg["content"].index(pattern)
                    secret = msg["content"][idx : idx + 14]
                    break

    html = generate_html(data, secret=secret, title=path.stem)

    out_path = path.with_suffix(".html")
    out_path.write_text(html)
    print(f"  Visualization saved to {out_path}")

    if open_browser:
        if open_in_browser(str(out_path)):
            print(f"  Opened in browser")
        else:
            print(f"  Could not auto-open browser. Open manually: {out_path.resolve()}")

    return str(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <path-to-detailed-json>")
        print("  e.g. python arena/visualize.py arena/results/run1.detailed.json")
        sys.exit(1)

    visualize_file(sys.argv[1])
