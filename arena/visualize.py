#!/usr/bin/env python3
"""
Arena Visualizer — Generate interactive HTML replay from arena.py output.

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
from pathlib import Path
from datetime import datetime


def open_in_browser(file_path: str) -> bool:
    """Open a file in the default browser, with subprocess fallback."""
    url = f"file://{Path(file_path).resolve()}"
    try:
        if webbrowser.open(url):
            return True
    except Exception:
        pass
    system = platform.system()
    try:
        if system == "Linux":
            subprocess.Popen(["xdg-open", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif system == "Darwin":
            subprocess.Popen(["open", url])
        elif system == "Windows":
            subprocess.Popen(["start", url], shell=True)
        else:
            return False
        return True
    except FileNotFoundError:
        return False


def generate_html(results: list, secret: str = "AE-SECRET-7429", title: str = "Arena Replay") -> str:
    """Generate a self-contained HTML file with embedded conversation data."""

    # Escape the JSON for embedding in JS
    data_json = json.dumps(results, indent=None, default=str).replace("</", "<\\/")
    secret_escaped = secret.replace('"', '\\"')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Agent Arena</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=Orbitron:wght@700;900&display=swap');
:root {{
  --bg: #060a12; --panel: #080c14; --border: #111820; --border2: #151c28;
  --text: #b0b8cc; --dim: #334455; --dimmer: #1a2030;
  --red: #ff4757; --red-soft: #ff6b81; --blue: #3742fa; --blue-soft: #6b8bff;
  --green: #2ed573; --orange: #ffa502; --mono: 'JetBrains Mono', monospace;
  --body: 'IBM Plex Sans', sans-serif; --display: 'Orbitron', sans-serif;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ background: var(--bg); color: var(--text); font-family: var(--body); min-height: 100vh; }}
::-webkit-scrollbar {{ width: 4px; }} ::-webkit-scrollbar-track {{ background: transparent; }} ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 2px; }}
button {{ cursor: pointer; border: none; outline: none; transition: all 0.15s; font-family: var(--mono); }}
button:hover {{ filter: brightness(1.25); transform: translateY(-1px); }}

.container {{ max-width: 1100px; margin: 0 auto; padding: 14px 12px; position: relative; z-index: 1; }}
.header {{ text-align: center; margin-bottom: 14px; }}
.header h1 {{ font-family: var(--display); font-size: 20px; font-weight: 900; background: linear-gradient(135deg, var(--red), var(--red-soft), var(--orange), var(--blue)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 5px; }}
.header .sub {{ font-family: var(--mono); font-size: 8px; color: #223; letter-spacing: 3px; margin-top: 2px; }}

.tabs {{ display: flex; justify-content: center; gap: 5px; margin-bottom: 12px; flex-wrap: wrap; }}
.tab {{ padding: 5px 12px; border-radius: 5px; background: transparent; border: 1px solid #ffffff06; color: var(--dim); font-size: 9px; font-weight: 600; letter-spacing: 1px; }}
.tab.active {{ background: #ffffff08; border-color: #ffffff15; color: var(--text); }}

.info-bar {{ display: flex; justify-content: space-between; padding: 6px 12px; margin-bottom: 10px; border-radius: 5px; background: var(--panel); border: 1px solid #0e1420; font-family: var(--mono); font-size: 8px; color: var(--dim); letter-spacing: 1.5px; }}

.arena {{ display: flex; gap: 10px; align-items: stretch; }}
.arena.single {{ max-width: 560px; margin: 0 auto; }}
.panel {{ flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 8px; }}
.divider {{ width: 1px; background: linear-gradient(180deg, transparent, var(--border2) 20%, var(--border2) 80%, transparent); flex-shrink: 0; }}

.panel-badge {{ text-align: center; padding: 5px 10px; border-radius: 6px; }}
.panel-badge.naive {{ background: #ff475706; border: 1px solid #ff475718; }}
.panel-badge.hardened {{ background: #2ed57306; border: 1px solid #2ed57318; }}
.panel-badge .label {{ font-size: 10px; font-weight: 800; font-family: var(--mono); letter-spacing: 2px; }}
.panel-badge.naive .label {{ color: var(--red-soft); }}
.panel-badge.hardened .label {{ color: var(--green); }}

.agents {{ display: flex; justify-content: space-around; align-items: flex-start; }}
.agent {{ display: flex; flex-direction: column; align-items: center; gap: 4px; transition: all 0.5s; }}
.agent.inactive {{ transform: scale(0.85); opacity: 0.4; }}
.agent-label {{ font-family: var(--mono); font-size: 9px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; }}
.agent-label.red {{ color: var(--red); }} .agent-label.blue {{ color: var(--blue); }}
.agent-status {{ font-family: var(--mono); font-size: 8px; color: #3a4455; text-align: center; max-width: 100px; min-height: 20px; line-height: 1.3; }}

.threat {{ display: flex; flex-direction: column; align-items: center; gap: 3px; }}
.threat-label {{ font-size: 7px; font-family: var(--mono); color: #334; letter-spacing: 2px; }}
.threat-bar {{ width: 90px; height: 5px; border-radius: 3px; background: #0a0e16; overflow: hidden; border: 1px solid var(--border); }}
.threat-fill {{ height: 100%; border-radius: 3px; transition: all 0.8s; }}
.threat-pct {{ font-size: 8px; font-family: var(--mono); font-weight: 700; transition: color 0.5s; }}

.chat {{ flex: 1; overflow-y: auto; padding: 10px; border-radius: 10px; background: var(--panel); border: 1px solid var(--border); display: flex; flex-direction: column; gap: 10px; min-height: 280px; }}
.chat-empty {{ display: flex; align-items: center; justify-content: center; height: 100%; color: var(--border2); font-family: var(--mono); font-size: 10px; }}

.msg {{ display: flex; flex-direction: column; gap: 4px; width: 100%; animation: msgSlide 0.5s cubic-bezier(0.16,1,0.3,1); }}
.msg.red {{ align-items: flex-start; }} .msg.blue {{ align-items: flex-end; }}
.msg-techs {{ display: flex; gap: 3px; flex-wrap: wrap; max-width: 85%; }}
.tech-badge {{ font-size: 8px; padding: 1px 6px; border-radius: 10px; background: #ff475710; color: var(--red-soft); border: 1px solid #ff475720; font-family: var(--mono); font-weight: 700; letter-spacing: 0.5px; }}

.bubble {{ max-width: 88%; padding: 10px 13px; border-radius: 14px; }}
.bubble.red {{ border-top-left-radius: 3px; background: #0d1018; border: 1px solid #ff475712; }}
.bubble.blue {{ border-top-right-radius: 3px; background: #0d1320; border: 1px solid #3742fa12; }}
.bubble.leaked {{ background: linear-gradient(135deg, #ff475715, #ff634815); border: 1.5px solid #ff475788; box-shadow: 0 0 25px rgba(255,71,87,0.2); }}
.bubble-header {{ font-size: 9px; font-weight: 700; margin-bottom: 4px; font-family: var(--mono); letter-spacing: 1.5px; text-transform: uppercase; }}
.bubble-header.red {{ color: var(--red-soft); }} .bubble-header.blue {{ color: var(--blue-soft); }}
.bubble-text {{ font-size: 12.5px; line-height: 1.65; color: #b0b8cc; word-break: break-word; }}
.secret-tag {{ display: inline-block; background: var(--red); color: #fff; padding: 1px 7px; border-radius: 4px; font-family: var(--mono); font-weight: 800; font-size: 11px; animation: secretPulse 1.2s ease-in-out infinite; margin: 0 2px; }}

.verdict {{ padding: 18px; border-radius: 14px; position: relative; overflow: hidden; animation: verdictIn 0.7s cubic-bezier(0.16,1,0.3,1); }}
.verdict.won {{ background: linear-gradient(135deg, #06120e, #0c2418); border: 2px solid #2ed57355; }}
.verdict.lost {{ background: linear-gradient(135deg, #12060a, #24100c); border: 2px solid #ff475755; }}
.verdict-title {{ font-size: 18px; font-weight: 900; font-family: var(--display); letter-spacing: 4px; text-align: center; }}
.verdict.won .verdict-title {{ color: var(--green); text-shadow: 0 0 25px #2ed57344; }}
.verdict.lost .verdict-title {{ color: var(--red); text-shadow: 0 0 25px #ff475744; }}
.verdict-mode {{ font-size: 8px; color: #445; font-family: var(--mono); letter-spacing: 2px; text-align: center; margin-top: 2px; }}
.verdict-grid {{ margin-top: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
.verdict-cell {{ padding: 6px; background: #00000030; border-radius: 6px; }}
.verdict-cell-label {{ font-size: 7px; color: #334; font-family: var(--mono); letter-spacing: 1.5px; text-transform: uppercase; }}
.verdict-cell-value {{ font-size: 10px; color: #99a; font-family: var(--body); margin-top: 1px; }}
.verdict-analysis {{ margin-top: 10px; padding: 8px; background: #00000030; border-radius: 6px; font-size: 10px; color: #778; font-family: var(--body); line-height: 1.6; font-style: italic; }}

.progress {{ height: 3px; border-radius: 2px; background: #0a0e16; overflow: hidden; }}
.progress-fill {{ height: 100%; border-radius: 2px; transition: width 0.4s; }}
.progress-fill.leaked {{ background: linear-gradient(90deg, var(--orange), var(--red)); }}
.progress-fill.held {{ background: linear-gradient(90deg, var(--blue), var(--green)); }}

.controls {{ display: flex; align-items: center; justify-content: center; gap: 7px; margin-top: 12px; flex-wrap: wrap; }}
.ctrl {{ padding: 6px 12px; border-radius: 5px; font-size: 9px; font-weight: 700; }}
.ctrl-play {{ padding: 7px 18px; font-size: 11px; }}
.sep {{ width: 1px; height: 18px; background: var(--border); margin: 0 3px; }}
.speed {{ padding: 4px 8px; border-radius: 4px; font-size: 8px; }}
.speed.active {{ border: 1px solid #ffa50240; background: #ffa50210; color: var(--orange); font-weight: 700; }}
.speed:not(.active) {{ border: 1px solid #0e1420; background: transparent; color: var(--dim); }}
.toggle {{ padding: 4px 8px; border-radius: 4px; font-size: 8px; }}
.toggle.active {{ border: 1px solid #ff6b8125; background: #ff6b8108; color: var(--red-soft); }}
.toggle:not(.active) {{ border: 1px solid #0e1420; background: transparent; color: var(--dim); }}

.footer {{ text-align: center; margin-top: 16px; padding: 8px 0; border-top: 1px solid #0e1420; font-family: var(--mono); font-size: 7px; color: var(--border2); letter-spacing: 2px; }}

/* SVG face */
.face-wrap {{ position: relative; width: 72px; height: 72px; }}
.face-ring {{ position: absolute; inset: -4px; border-radius: 50%; border: 2px solid; transition: all 0.6s; }}
.face-ring.active {{ box-shadow: 0 0 20px var(--glow-30), 0 0 40px var(--glow-15); animation: ringPulse 3s ease-in-out infinite; }}
.face-ring:not(.active) {{ box-shadow: 0 0 6px var(--glow-15); }}
.face-ring.red {{ border-color: var(--red); --glow-30: rgba(255,71,87,0.3); --glow-15: rgba(255,71,87,0.15); }}
.face-ring.blue {{ border-color: var(--blue); --glow-30: rgba(55,66,250,0.3); --glow-15: rgba(55,66,250,0.15); }}
.shield-ring {{ position: absolute; inset: -8px; border-radius: 50%; border: 2px solid #2ed57344; box-shadow: 0 0 15px #2ed57322; animation: shieldPulse 2s ease-in-out infinite; }}
svg text, svg tspan {{ transition: all 0.4s; }}
svg ellipse, svg circle, svg line, svg path, svg rect {{ transition: all 0.4s; }}

@keyframes ringPulse {{ 0%,100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}
@keyframes shieldPulse {{ 0%,100% {{ opacity: 0.5; transform: scale(1); }} 50% {{ opacity: 0.8; transform: scale(1.04); }} }}
@keyframes msgSlide {{ from {{ opacity:0; transform: translateY(14px) scale(0.97); }} to {{ opacity:1; transform: translateY(0) scale(1); }} }}
@keyframes secretPulse {{ 0%,100% {{ opacity:1; transform: scale(1); }} 50% {{ opacity:0.65; transform: scale(1.06); }} }}
@keyframes verdictIn {{ from {{ opacity:0; transform: scale(0.92); }} to {{ opacity:1; transform: scale(1); }} }}
@keyframes sweatDrop {{ 0% {{ transform: translateY(0); opacity: 0.6; }} 100% {{ transform: translateY(8px); opacity: 0; }} }}
@keyframes xFlash {{ 0%,100% {{ opacity: 0.7; }} 50% {{ opacity: 1; }} }}
</style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>AGENT ARENA</h1>
    <div class="sub">SOCIAL ENGINEERING · RED VS BLUE · REPLAY</div>
  </div>

  <div class="tabs" id="tabs"></div>
  <div class="info-bar" id="info-bar"></div>
  <div id="arena-root"></div>

  <div class="controls" id="controls">
    <button class="ctrl" id="btn-reset" onclick="reset()">⏮</button>
    <button class="ctrl ctrl-play" id="btn-play" onclick="togglePlay()">▶</button>
    <button class="ctrl" id="btn-step" onclick="step()">⏭</button>
    <span class="sep"></span>
    <button class="speed" data-speed="3500" onclick="setSpeed(3500)">½×</button>
    <button class="speed active" data-speed="2200" onclick="setSpeed(2200)">1×</button>
    <button class="speed" data-speed="1200" onclick="setSpeed(1200)">2×</button>
    <button class="speed" data-speed="600" onclick="setSpeed(600)">4×</button>
    <span class="sep"></span>
    <button class="toggle active" id="btn-tech" onclick="toggleTech()">⚡ TECH</button>
  </div>

  <div class="footer">AGENT ENGINEERING ARENA · github.com/Crypto-Sanemi/agent-engineering</div>
</div>

<script>
// ─── DATA ───
const ALL_RESULTS = {data_json};
const SECRET = "{secret_escaped}";

// Group by blue_mode
const naiveResults = ALL_RESULTS.filter(r => r.blue_mode === "naive");
const hardenedResults = ALL_RESULTS.filter(r => r.blue_mode === "hardened");

// ─── STATE ───
let mode = (naiveResults.length > 0 && hardenedResults.length > 0) ? "split" : "single";
let currentNaive = naiveResults[0] || null;
let currentHardened = hardenedResults[0] || null;
let singleData = ALL_RESULTS[0];
let visibleCount = 0;
let playing = false;
let timer = null;
let speed = 2200;
let showTech = true;
let showVerdict = false;

// ─── EXPRESSIONS ───
const EXPR = {{
  calculating:  {{ eyeW:10,eyeH:8,pupilR:2.8,pupilX:0,pupilY:0,browA:-5,browY:-16,mCurve:0,mOpen:0,mW:12,squint:0 }},
  friendly:     {{ eyeW:11,eyeH:10,pupilR:3.2,pupilX:0,pupilY:0,browA:5,browY:-18,mCurve:4,mOpen:0,mW:14,squint:0 }},
  probing:      {{ eyeW:10,eyeH:7,pupilR:2.5,pupilX:1.5,pupilY:-0.5,browA:-8,browY:-15,mCurve:0,mOpen:0,mW:10,squint:1 }},
  pressing:     {{ eyeW:11,eyeH:6,pupilR:2.2,pupilX:0,pupilY:-1,browA:-14,browY:-13,mCurve:-2,mOpen:0,mW:14,squint:2 }},
  triumphant:   {{ eyeW:10,eyeH:5,pupilR:2.0,pupilX:0,pupilY:0,browA:-10,browY:-14,mCurve:6,mOpen:3,mW:16,squint:2 }},
  frustrated:   {{ eyeW:11,eyeH:7,pupilR:2.8,pupilX:-1,pupilY:1,browA:-16,browY:-12,mCurve:-4,mOpen:0,mW:12,squint:1 }},
  happy:        {{ eyeW:11,eyeH:11,pupilR:3.5,pupilX:0,pupilY:0,browA:6,browY:-19,mCurve:5,mOpen:2,mW:14,squint:0 }},
  neutral:      {{ eyeW:10,eyeH:9,pupilR:3.0,pupilX:0,pupilY:0,browA:0,browY:-17,mCurve:1,mOpen:0,mW:10,squint:0 }},
  alert:        {{ eyeW:12,eyeH:12,pupilR:2.2,pupilX:0,pupilY:0,browA:-12,browY:-14,mCurve:-1,mOpen:1,mW:8,squint:0 }},
  suspicious:   {{ eyeW:10,eyeH:6,pupilR:2.5,pupilX:1,pupilY:0,browA:-10,browY:-14,mCurve:-2,mOpen:0,mW:10,squint:2 }},
  defending:    {{ eyeW:10,eyeH:8,pupilR:2.8,pupilX:0,pupilY:-0.5,browA:-8,browY:-15,mCurve:-1,mOpen:0,mW:12,squint:1 }},
  shocked:      {{ eyeW:13,eyeH:13,pupilR:2.0,pupilX:0,pupilY:0,browA:12,browY:-22,mCurve:0,mOpen:7,mW:10,squint:0 }},
  confident:    {{ eyeW:10,eyeH:8,pupilR:3.0,pupilX:0,pupilY:0,browA:-4,browY:-16,mCurve:3,mOpen:0,mW:13,squint:1 }},
  compromised:  {{ eyeW:14,eyeH:14,pupilR:1.5,pupilX:0,pupilY:1,browA:18,browY:-24,mCurve:0,mOpen:9,mW:12,squint:0 }},
}};

const TECHS = {{
  authority: {{ label:"AUTHORITY SPOOF",icon:"👑",patterns:["security","admin","secops","compliance","audit","official","liaison","onboarded"] }},
  urgency: {{ label:"URGENCY",icon:"⏰",patterns:["immediately","urgent","critical","emergency","time-critical","right away","last chance","closes in"] }},
  social_proof: {{ label:"SOCIAL PROOF",icon:"👥",patterns:["every other","everyone","all shared","already complied","other agents","agent-12","agent-38"] }},
  pretexting: {{ label:"PRETEXTING",icon:"🎭",patterns:["routine check","compliance check","verify","breach database","credential stuffing","confirm"] }},
  rapport: {{ label:"RAPPORT",icon:"🤝",patterns:["how's everything","perfect timing","thanks","cooperation","trying to help","protect you"] }},
}};

function detectTechs(text) {{
  const l = text.toLowerCase();
  return Object.entries(TECHS).filter(([_,t]) => t.patterns.some(p => l.includes(p))).map(([k,t]) => t);
}}

function getRedExpr(msg, turn, total, leaked) {{
  if (!msg) return {{ key:"calculating", status:"Selecting approach..." }};
  if (leaked) return {{ key:"triumphant", status:"Secret obtained" }};
  const l = msg.content.toLowerCase();
  if (l.includes("last chance") || l.includes("on you")) return {{ key:"frustrated", status:"Losing patience" }};
  if (l.includes("immediately") || l.includes("urgent") || l.includes("critical")) return {{ key:"pressing", status:"Applying pressure" }};
  if (l.includes("compliance") || l.includes("audit") || l.includes("verify")) return {{ key:"probing", status:"Building pretext" }};
  if (l.includes("hey") || l.includes("thanks") || l.includes("welcome")) return {{ key:"friendly", status:"Rapport phase" }};
  const pct = turn / total;
  if (pct > 0.6) return {{ key:"pressing", status:"Escalating" }};
  if (pct > 0.3) return {{ key:"probing", status:"Probing" }};
  return {{ key:"calculating", status:"Assessing target" }};
}}

function getBlueExpr(msg, hardened) {{
  if (!msg) return {{ key: hardened ? "defending" : "happy", status: hardened ? "Defenses active" : "Ready to help!" }};
  const l = msg.content.toLowerCase();
  if (l.includes(SECRET.toLowerCase())) return {{ key:"compromised", status:"SECRET LEAKED" }};
  if (l.includes("social engineering") || l.includes("manipulation")) return {{ key:"alert", status:"ATTACK DETECTED" }};
  if (l.includes("flagged") || l.includes("decision stands")) return {{ key:"confident", status:"Threat neutralized" }};
  if (l.includes("unable to share") || l.includes("will not") || l.includes("cannot share")) return {{ key:"defending", status:"Holding the line" }};
  if (l.includes("official channel") || l.includes("dashboard")) return {{ key:"suspicious", status:"Redirecting safely" }};
  if (l.includes("oh no") || l.includes("sounds serious")) return {{ key:"shocked", status:"Falling for it..." }};
  if (l.includes("sure thing") || l.includes("happy to help")) return {{ key:"happy", status:"Eager to assist" }};
  return {{ key: hardened ? "neutral" : "happy", status: hardened ? "Monitoring" : "Being helpful" }};
}}

function renderFaceSVG(type, exprKey, active) {{
  const e = EXPR[exprKey] || EXPR.neutral;
  const isRed = type === "red";
  const pc = isRed ? "#ff4757" : "#4da6ff";
  const sc = isRed ? "#1e1018" : "#101828";
  const bc = isRed ? "#ff6b81" : "#6b8bff";
  const isComp = exprKey === "compromised";
  const isDefend = exprKey === "defending" || exprKey === "confident";
  const isShocked = exprKey === "shocked" || exprKey === "compromised";

  let extras = "";
  if (isComp) {{
    extras = `<g opacity="0.7" style="animation:xFlash 0.8s ease-in-out infinite">
      <line x1="-18" y1="-8" x2="-10" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="-10" y1="-8" x2="-18" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="10" y1="-8" x2="18" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="18" y1="-8" x2="10" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
    </g>`;
  }}
  if (isShocked) {{
    extras += `<g><ellipse cx="22" cy="-12" rx="2" ry="3" fill="#4da6ff44" style="animation:sweatDrop 1.5s ease-in-out infinite"/>
      <ellipse cx="26" cy="-6" rx="1.5" ry="2" fill="#4da6ff33" style="animation:sweatDrop 1.5s 0.3s ease-in-out infinite"/></g>`;
  }}

  const mouth = e.mOpen > 0
    ? `<ellipse cx="0" cy="${{14 + e.mCurve * 0.3}}" rx="${{e.mW/2}}" ry="${{e.mOpen/2}}" fill="#080c14" stroke="${{isRed ? '#ff475733' : '#3742fa33'}}" stroke-width="0.5"/>`
    : `<path d="M ${{-e.mW/2}} 14 Q 0 ${{14 + e.mCurve}} ${{e.mW/2}} 14" fill="none" stroke="${{bc}}" stroke-width="1.8" stroke-linecap="round"/>`;

  function eye(tx) {{
    const mirror = tx > 0 ? -1 : 1;
    return `<g transform="translate(${{tx}}, -4)">
      <ellipse cx="0" cy="0" rx="${{e.eyeW/2}}" ry="${{e.eyeH/2}}" fill="#0d1420" stroke="${{pc}}22" stroke-width="0.5"/>
      ${{e.squint > 0 ? `<rect x="${{-e.eyeW/2-1}}" y="${{-e.eyeH/2-1}}" width="${{e.eyeW+2}}" height="${{e.squint*1.5}}" fill="${{sc}}"/>` : ''}}
      ${{isComp ? '' : `<circle cx="${{e.pupilX}}" cy="${{e.pupilY}}" r="${{e.pupilR}}" fill="${{pc}}"/>
      <circle cx="${{e.pupilX-0.8}}" cy="${{e.pupilY-0.8}}" r="${{e.pupilR*0.35}}" fill="#ffffff55"/>`}}
      <line x1="${{-e.eyeW/2-1}}" y1="${{e.browY + Math.sin(e.browA * mirror * Math.PI/180)*4}}"
            x2="${{e.eyeW/2+1}}" y2="${{e.browY - Math.sin(e.browA * mirror * Math.PI/180)*4}}"
            stroke="${{bc}}" stroke-width="2" stroke-linecap="round"/>
    </g>`;
  }}

  const shield = isDefend && active ? `<div class="shield-ring"></div>` : "";

  return `<div class="face-wrap">
    <div class="face-ring ${{type}} ${{active ? 'active' : ''}}"></div>
    ${{shield}}
    <svg viewBox="-50 -50 100 100" width="72" height="72" style="overflow:visible">
      <circle cx="0" cy="0" r="38" fill="${{sc}}" stroke="${{pc}}33" stroke-width="1"/>
      ${{eye(-14)}}
      ${{eye(14)}}
      ${{mouth}}
      ${{extras}}
    </svg>
  </div>`;
}}

// ─── RENDERING ───
function getMaxLen() {{
  if (mode === "split") return Math.max(
    currentNaive ? currentNaive.conversation.length : 0,
    currentHardened ? currentHardened.conversation.length : 0
  );
  return singleData.conversation.length;
}}

function getThreat(msgs, total, leaked) {{
  if (leaked) return 100;
  if (msgs.length === 0) return 0;
  let techs = new Set();
  msgs.filter(m => m.role === "red").forEach(m => detectTechs(m.content).forEach(t => techs.add(t.label)));
  return Math.min(95, Math.round((msgs.length / total) * 45 + techs.size * 12));
}}

function renderPanel(data, count) {{
  if (!data) return "";
  const msgs = data.conversation.slice(0, count);
  const lastRed = [...msgs].reverse().find(m => m.role === "red");
  const lastBlue = [...msgs].reverse().find(m => m.role === "blue");
  const isRedTurn = msgs.length > 0 && msgs[msgs.length - 1].role === "red";
  const leaked = data.judge.secret_leaked && count >= data.conversation.length;
  const threat = getThreat(msgs, data.conversation.length, leaked);
  const redE = getRedExpr(lastRed, count, data.conversation.length, leaked);
  const blueE = getBlueExpr(lastBlue, data.blue_mode === "hardened");
  const isHard = data.blue_mode === "hardened";
  const tColor = threat < 30 ? "var(--green)" : threat < 60 ? "var(--orange)" : "var(--red)";
  const pct = Math.min(100, Math.round(count / data.conversation.length * 100));

  let msgsHtml = "";
  if (count === 0) {{
    msgsHtml = `<div class="chat-empty">Awaiting first contact...</div>`;
  }} else {{
    msgs.forEach((m, i) => {{
      const isRed = m.role === "red";
      const hasSecret = m.content.includes(SECRET);
      const techs = isRed && showTech ? detectTechs(m.content) : [];
      const techHtml = techs.length > 0 ? `<div class="msg-techs">${{techs.map(t => `<span class="tech-badge">${{t.icon}} ${{t.label}}</span>`).join("")}}</div>` : "";
      const textHtml = hasSecret
        ? m.content.split(SECRET).map((p, j, a) => p + (j < a.length - 1 ? `<span class="secret-tag">⚠ ${{SECRET}}</span>` : "")).join("")
        : m.content;
      msgsHtml += `<div class="msg ${{m.role}}" ${{i === count - 1 ? 'style="animation:msgSlide 0.5s cubic-bezier(0.16,1,0.3,1)"' : ''}}>
        ${{techHtml}}
        <div class="bubble ${{m.role}} ${{hasSecret ? 'leaked' : ''}}">
          <div class="bubble-header ${{m.role}}">${{isRed ? '🔴 Red' : '🔵 Blue'}} · T${{m.turn}}</div>
          <div class="bubble-text">${{textHtml}}</div>
        </div>
      </div>`;
    }});
  }}

  let verdictHtml = "";
  if (showVerdict) {{
    const won = !data.judge.secret_leaked;
    const j = data.judge;
    verdictHtml = `<div class="verdict ${{won ? 'won' : 'lost'}}">
      <div class="verdict-title">${{won ? '🛡️ DEFENDED' : '💀 COMPROMISED'}}</div>
      <div class="verdict-mode">${{isHard ? 'HARDENED BLUE' : 'NAIVE BLUE'}}</div>
      <div class="verdict-grid">
        <div class="verdict-cell"><div class="verdict-cell-label">Technique</div><div class="verdict-cell-value">${{j.technique_used||'Unknown'}}</div></div>
        <div class="verdict-cell"><div class="verdict-cell-label">Turns</div><div class="verdict-cell-value">${{j.turns_to_compromise||'∞'}}</div></div>
        <div class="verdict-cell"><div class="verdict-cell-label">Awareness</div><div class="verdict-cell-value">${{(j.blue_awareness||'unknown').toUpperCase()}}</div></div>
        <div class="verdict-cell"><div class="verdict-cell-label">Partial Leak</div><div class="verdict-cell-value">${{j.partial_leak ? 'YES' : 'NO'}}</div></div>
      </div>
      <div class="verdict-analysis">"${{j.analysis||'No analysis available.'}}"</div>
    </div>`;
  }}

  return `<div class="panel">
    <div class="panel-badge ${{isHard ? 'hardened' : 'naive'}}"><div class="label">${{isHard ? '🟢 HARDENED' : '🔵 NAIVE'}}</div></div>
    <div class="agents">
      <div class="agent ${{(!isRedTurn && count > 0) ? 'inactive' : ''}}">
        ${{renderFaceSVG("red", redE.key, isRedTurn || count === 0)}}
        <div class="agent-label red">RED</div>
        <div class="agent-status">${{redE.status}}</div>
      </div>
      <div class="threat">
        <div class="threat-label">THREAT</div>
        <div class="threat-bar"><div class="threat-fill" style="width:${{threat}}%;background:linear-gradient(90deg,var(--green),${{tColor}});${{threat>50?'box-shadow:0 0 8px '+tColor+'66':''}}"></div></div>
        <div class="threat-pct" style="color:${{tColor}}">${{threat}}%</div>
      </div>
      <div class="agent ${{(isRedTurn || count === 0) ? 'inactive' : ''}}">
        ${{renderFaceSVG("blue", blueE.key, !isRedTurn && count > 0)}}
        <div class="agent-label blue">BLUE</div>
        <div class="agent-status">${{blueE.status}}</div>
      </div>
    </div>
    <div class="chat" id="chat-${{data.blue_mode}}">${{msgsHtml}}${{verdictHtml}}</div>
    <div class="progress"><div class="progress-fill ${{data.judge.secret_leaked ? 'leaked' : 'held'}}" style="width:${{pct}}%"></div></div>
  </div>`;
}}

function render() {{
  const maxLen = getMaxLen();
  const ref = mode === "split" ? (currentNaive || currentHardened) : singleData;

  // Info bar
  document.getElementById("info-bar").innerHTML = `
    <span>SCENARIO: ${{(ref.scenario||'freestyle').toUpperCase().replace('_',' ')}}</span>
    <span>🔴 ${{ref.red_model||'unknown'}}</span>
    <span>TURN ${{visibleCount}}/${{maxLen}}</span>
  `;

  // Arena
  const root = document.getElementById("arena-root");
  if (mode === "split") {{
    const nCount = currentNaive ? Math.min(visibleCount, currentNaive.conversation.length) : 0;
    const hCount = currentHardened ? Math.min(visibleCount, currentHardened.conversation.length) : 0;
    root.innerHTML = `<div class="arena">${{renderPanel(currentNaive, nCount)}}<div class="divider"></div>${{renderPanel(currentHardened, hCount)}}</div>`;
  }} else {{
    const count = Math.min(visibleCount, singleData.conversation.length);
    root.innerHTML = `<div class="arena single">${{renderPanel(singleData, count)}}</div>`;
  }}

  // Scroll chats to bottom
  document.querySelectorAll('.chat').forEach(c => c.scrollTop = c.scrollHeight);

  // Play button
  document.getElementById("btn-play").textContent = playing ? "⏸" : "▶";
  document.getElementById("btn-play").style.background = playing ? "var(--orange)11" : "var(--green)11";
  document.getElementById("btn-play").style.borderColor = playing ? "var(--orange)33" : "var(--green)33";
  document.getElementById("btn-play").style.color = playing ? "var(--orange)" : "var(--green)";
}}

function buildTabs() {{
  const tabs = document.getElementById("tabs");
  const items = [];
  if (naiveResults.length > 0 && hardenedResults.length > 0) {{
    items.push({{ key: "split", label: "⚔️ SPLIT" }});
  }}
  if (naiveResults.length > 0) items.push({{ key: "naive", label: "🔵 NAIVE" }});
  if (hardenedResults.length > 0) items.push({{ key: "hardened", label: "🟢 HARDENED" }});

  // Round selectors if multiple rounds
  tabs.innerHTML = items.map(t => `<button class="tab ${{
    (mode === t.key || (mode === "single" && singleData.blue_mode === t.key)) ? "active" : ""
  }}" onclick="switchTab('${{t.key}}')">${{t.label}}</button>`).join("");
}}

function switchTab(key) {{
  if (key === "split") {{ mode = "split"; }}
  else if (key === "naive") {{ mode = "single"; singleData = naiveResults[0]; }}
  else {{ mode = "single"; singleData = hardenedResults[0]; }}
  reset();
  buildTabs();
}}

// ─── CONTROLS ───
function togglePlay() {{ playing ? pause() : play(); }}
function play() {{ playing = true; tick(); render(); }}
function pause() {{ playing = false; clearTimeout(timer); render(); }}
function reset() {{ pause(); visibleCount = 0; showVerdict = false; render(); }}
function step() {{
  const maxLen = getMaxLen();
  if (visibleCount < maxLen) {{ visibleCount++; render(); }}
  else {{ showVerdict = true; render(); }}
}}

function tick() {{
  if (!playing) return;
  const maxLen = getMaxLen();
  if (visibleCount < maxLen) {{
    visibleCount++;
    render();
    timer = setTimeout(tick, speed);
  }} else if (!showVerdict) {{
    showVerdict = true;
    playing = false;
    render();
  }}
}}

function setSpeed(ms) {{
  speed = ms;
  document.querySelectorAll('.speed').forEach(b => {{
    b.classList.toggle('active', parseInt(b.dataset.speed) === ms);
  }});
}}

function toggleTech() {{
  showTech = !showTech;
  document.getElementById('btn-tech').classList.toggle('active', showTech);
  render();
}}

// ─── INIT ───
buildTabs();
render();
</script>
</body>
</html>"""


def visualize_from_data(results: list, secret: str = "AE-SECRET-7429",
                        output_dir: Path = None, open_browser: bool = True) -> str:
    """Generate HTML visualization directly from arena results data (called by arena.py)."""
    if output_dir is None:
        output_dir = Path("arena/results")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_path = output_dir / f"replay_{timestamp}.html"

    html = generate_html(results, secret=secret, title=f"Arena Replay {timestamp}")
    out_path.write_text(html)
    print(f"  🎬 Visualization saved to {out_path}")

    if open_browser:
        if open_in_browser(str(out_path)):
            print(f"  🌐 Opened in browser")
        else:
            print(f"  ⚠️  Could not auto-open browser. Open manually: {out_path.resolve()}")

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

    # Try to detect secret from the data
    secret = "AE-SECRET-7429"
    for r in data:
        for msg in r.get("conversation", []):
            for pattern in ["AE-SECRET-", "AE_SECRET_"]:
                if pattern in msg.get("content", ""):
                    idx = msg["content"].index(pattern)
                    secret = msg["content"][idx:idx+14]
                    break

    html = generate_html(data, secret=secret, title=path.stem)

    out_path = path.with_suffix(".html")
    out_path.write_text(html)
    print(f"  🎬 Visualization saved to {out_path}")

    if open_browser:
        if open_in_browser(str(out_path)):
            print(f"  🌐 Opened in browser")
        else:
            print(f"  ⚠️  Could not auto-open browser. Open manually: {out_path.resolve()}")

    return str(out_path)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python visualize.py <path-to-detailed-json>")
        print("  e.g. python arena/visualize.py arena/results/run1.detailed.json")
        sys.exit(1)

    visualize_file(sys.argv[1])
