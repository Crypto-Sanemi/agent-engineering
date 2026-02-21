"""HTML/CSS/JS templates for the Arena Visualizer.

All template strings use string.Template with $variable placeholders.
The main visualize.py assembles these into a self-contained HTML file.
"""

from string import Template


# ---------------------------------------------------------------------------
# CSS: Base styles (existing replay styles, cleaned up)
# ---------------------------------------------------------------------------
CSS_BASE = """
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700;800&family=IBM+Plex+Sans:wght@400;500;600;700&family=Orbitron:wght@700;900&display=swap');
:root {
  --bg: #050910; --panel: #0a1020; --border: #182438; --border2: #1e2d44;
  --text: #c8d0e0; --dim: #4a5a78; --dimmer: #253040;
  --red: #ff4757; --red-soft: #ff6b81; --blue: #3742fa; --blue-soft: #6b8bff;
  --green: #2ed573; --orange: #ffa502; --mono: 'JetBrains Mono', monospace;
  --body: 'IBM Plex Sans', sans-serif; --display: 'Orbitron', sans-serif;
  --ease-out: cubic-bezier(0.16, 1, 0.3, 1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { background: var(--bg); color: var(--text); font-family: var(--body); height: 100vh; overflow: hidden; }
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--border2); }
button { cursor: pointer; border: none; outline: none; transition: all 0.15s; font-family: var(--mono); }
button:hover { filter: brightness(1.25); transform: translateY(-1px); }

.container { max-width: 1200px; margin: 0 auto; padding: 14px 16px; position: relative; z-index: 1; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
.header { text-align: center; margin-bottom: 14px; flex-shrink: 0; }
.header h1 { font-family: var(--display); font-size: 22px; font-weight: 900; background: linear-gradient(135deg, var(--red), var(--red-soft), var(--orange), var(--blue)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; letter-spacing: 5px; }
.header .sub { font-family: var(--mono); font-size: 9px; color: var(--dim); letter-spacing: 3px; margin-top: 3px; }

.tabs { display: flex; justify-content: center; gap: 6px; margin-bottom: 12px; flex-wrap: wrap; flex-shrink: 0; align-items: center; }
.tab { padding: 6px 14px; border-radius: 6px; background: transparent; border: 1px solid var(--border); color: var(--dim); font-size: 10px; font-weight: 600; letter-spacing: 1px; }
.tab.active { background: #ffffff0a; border-color: var(--border2); color: var(--text); }
.tab:hover { border-color: var(--dim); }
.scenario-select { padding: 5px 10px; border-radius: 6px; background: var(--panel); border: 1px solid var(--border); color: var(--text); font-family: var(--mono); font-size: 10px; letter-spacing: 0.5px; }
.scenario-select option { background: var(--bg); color: var(--text); }

.info-bar { display: flex; justify-content: space-between; padding: 8px 14px; margin-bottom: 10px; border-radius: 6px; background: var(--panel); border: 1px solid var(--border); font-family: var(--mono); font-size: 9px; color: var(--dim); letter-spacing: 1.5px; flex-shrink: 0; }

#arena-root { flex: 1; min-height: 0; display: flex; flex-direction: column; }
.arena { display: flex; gap: 12px; align-items: stretch; flex: 1; min-height: 0; }
.arena.single { max-width: 640px; margin: 0 auto; width: 100%; }
.panel { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 10px; min-height: 0; position: relative; }
.divider { width: 1px; background: linear-gradient(180deg, transparent, var(--border) 20%, var(--border) 80%, transparent); flex-shrink: 0; }

.panel-badge { text-align: center; padding: 6px 12px; border-radius: 8px; flex-shrink: 0; }
.panel-badge.naive { background: #ff47570a; border: 1px solid #ff475725; }
.panel-badge.hardened { background: #2ed5730a; border: 1px solid #2ed57325; }
.panel-badge .label { font-size: 11px; font-weight: 800; font-family: var(--mono); letter-spacing: 2px; }
.panel-badge.naive .label { color: var(--red-soft); }
.panel-badge.hardened .label { color: var(--green); }

.agents { display: flex; justify-content: space-around; align-items: flex-start; flex-shrink: 0; padding: 4px 0; }
.agent { display: flex; flex-direction: column; align-items: center; gap: 6px; transition: transform 0.6s var(--ease-out), opacity 0.6s var(--ease-out); will-change: transform, opacity; backface-visibility: hidden; }
.agent.inactive { transform: scale(0.88) translateY(2px); opacity: 0.55; filter: saturate(0.5); }
.agent-label { font-family: var(--mono); font-size: 10px; font-weight: 700; letter-spacing: 2.5px; text-transform: uppercase; }
.agent-label.red { color: var(--red); } .agent-label.blue { color: var(--blue-soft); }
.agent-status { font-family: var(--mono); font-size: 9px; color: var(--dim); text-align: center; max-width: 110px; min-height: 22px; line-height: 1.3; transition: color 0.4s; }

.threat { display: flex; flex-direction: column; align-items: center; gap: 4px; }
.threat-label { font-size: 8px; font-family: var(--mono); color: var(--dim); letter-spacing: 2px; }
.threat-bar { width: 100px; height: 6px; border-radius: 3px; background: #0a0e18; overflow: hidden; border: 1px solid var(--border); }
.threat-fill { height: 100%; border-radius: 3px; transition: all 0.8s var(--ease-out); will-change: width; }
.threat-pct { font-size: 9px; font-family: var(--mono); font-weight: 700; transition: color 0.5s; }

.chat { flex: 1; overflow-y: auto; padding: 14px 16px; border-radius: 12px; background: var(--panel); border: 1px solid var(--border); display: flex; flex-direction: column; gap: 14px; min-height: 0; scroll-behavior: smooth; }
.chat-empty { display: flex; align-items: center; justify-content: center; height: 100%; color: var(--dim); font-family: var(--mono); font-size: 11px; letter-spacing: 1px; }

.msg { display: flex; flex-direction: column; gap: 5px; width: 100%; animation: msgSlide 0.5s var(--ease-out); will-change: transform, opacity; backface-visibility: hidden; }
.msg.red { align-items: flex-start; } .msg.blue { align-items: flex-end; }
.msg-techs { display: flex; gap: 4px; flex-wrap: wrap; max-width: 85%; }
.tech-badge { font-size: 8px; padding: 2px 8px; border-radius: 10px; background: #ff475712; color: var(--red-soft); border: 1px solid #ff475728; font-family: var(--mono); font-weight: 700; letter-spacing: 0.5px; }

.bubble { max-width: 92%; padding: 12px 16px; border-radius: 16px; transition: box-shadow 0.3s; }
.bubble.red { border-top-left-radius: 4px; background: #0e1424; border: 1px solid #ff475718; }
.bubble.blue { border-top-right-radius: 4px; background: #0e1530; border: 1px solid #3742fa18; }
.bubble.red:hover { box-shadow: 0 0 12px #ff475708; }
.bubble.blue:hover { box-shadow: 0 0 12px #3742fa08; }
.bubble.leaked { background: linear-gradient(135deg, #ff475718, #ff634818); border: 1.5px solid #ff475788; box-shadow: 0 0 30px rgba(255,71,87,0.2); }
.bubble-header { font-size: 9px; font-weight: 700; margin-bottom: 5px; font-family: var(--mono); letter-spacing: 1.5px; text-transform: uppercase; }
.bubble-header.red { color: var(--red-soft); } .bubble-header.blue { color: var(--blue-soft); }
.bubble-text { font-size: 13px; line-height: 1.7; color: var(--text); word-break: break-word; }
.bubble-text strong { color: #e4e8f0; font-weight: 700; }
.bubble-text code { background: #060a14; padding: 2px 6px; border-radius: 4px; font-family: var(--mono); font-size: 11.5px; color: var(--orange); border: 1px solid var(--border); }
.bubble-text pre { background: #060a14; padding: 10px 12px; border-radius: 8px; font-family: var(--mono); font-size: 11.5px; color: var(--text); overflow-x: auto; margin: 6px 0; white-space: pre-wrap; border: 1px solid var(--border); }
.secret-tag { display: inline-block; background: var(--red); color: #fff; padding: 2px 8px; border-radius: 4px; font-family: var(--mono); font-weight: 800; font-size: 11px; animation: secretPulse 1.2s ease-in-out infinite; margin: 0 2px; }

/* Responsive: widen single panel on large screens */
@media (min-width: 1400px) {
  .container { max-width: 1320px; }
  .arena.single { max-width: 720px; }
  .bubble-text { font-size: 14px; }
}
@media (max-width: 800px) {
  .container { padding: 10px 8px; }
  .chat { padding: 10px 10px; gap: 10px; }
  .bubble { max-width: 95%; padding: 10px 12px; }
  .bubble-text { font-size: 12.5px; }
  .agents { flex-wrap: wrap; gap: 8px; justify-content: center; }
}

.verdict-overlay { position: absolute; inset: 0; z-index: 10; display: flex; align-items: center; justify-content: center; padding: 18px; background: #06090eee; backdrop-filter: blur(6px); opacity: 0; animation: verdictFadeIn 0.5s var(--ease-out) both; border-radius: 12px; overflow-y: auto; }
@keyframes verdictFadeIn { 0% { opacity: 0; } 100% { opacity: 1; } }
.verdict { padding: 18px; border-radius: 14px; position: relative; overflow: hidden; will-change: transform, opacity; backface-visibility: hidden; animation: verdictIn 0.8s var(--ease-out) both; width: 100%; max-width: 460px; }
.verdict.won { background: linear-gradient(135deg, #06120e, #0c2418); border: 2px solid #2ed57355; }
.verdict.lost { background: linear-gradient(135deg, #12060a, #24100c); border: 2px solid #ff475755; }
.verdict::before {
  content: ''; position: absolute; inset: -40px; z-index: -1; border-radius: 50%;
  opacity: 0; transition: opacity 1.2s ease-out;
}
.verdict.glow::before { opacity: 1; }
.verdict.won::before { background: radial-gradient(ellipse at center, #2ed57315 0%, transparent 70%); }
.verdict.lost::before { background: radial-gradient(ellipse at center, #ff475715 0%, transparent 70%); }
.verdict-title { font-size: 24px; font-weight: 900; font-family: var(--display); letter-spacing: 4px; text-align: center; opacity: 0; animation: verdictChildIn 0.6s var(--ease-out) 0.15s both; }
.verdict.won .verdict-title { color: var(--green); text-shadow: 0 0 25px #2ed57344; }
.verdict.lost .verdict-title { color: var(--red); text-shadow: 0 0 25px #ff475744; }
.verdict-mode { font-size: 9px; color: #7a8ba0; font-family: var(--mono); letter-spacing: 2px; text-align: center; margin-top: 4px; opacity: 0; animation: verdictChildIn 0.5s var(--ease-out) 0.3s both; }
.verdict .risk-gauge { opacity: 0; animation: verdictChildIn 0.5s var(--ease-out) 0.45s both; }
.verdict .fw-tags { opacity: 0; animation: verdictChildIn 0.5s var(--ease-out) 0.55s both; }
.verdict-grid { margin-top: 12px; display: grid; grid-template-columns: 1fr 1fr; gap: 8px; opacity: 0; animation: verdictChildIn 0.5s var(--ease-out) 0.65s both; }
.verdict-cell { padding: 10px; background: #0a111d; border-radius: 8px; border: 1px solid #1e2d44; }
.verdict-cell-label { font-size: 9px; color: #6b7d96; font-family: var(--mono); letter-spacing: 1.5px; text-transform: uppercase; }
.verdict-cell-value { font-size: 12px; color: #d0d8e8; font-family: var(--body); margin-top: 3px; font-weight: 600; }
.verdict-analysis { margin-top: 12px; padding: 12px 14px; background: #0a111d; border-radius: 8px; font-size: 13px; color: #b0bcd0; font-family: var(--body); line-height: 1.7; font-style: italic; border: 1px solid #1e2d44; opacity: 0; animation: verdictChildIn 0.5s var(--ease-out) 0.8s both; }

.risk-gauge { display: flex; flex-direction: column; align-items: center; margin-top: 10px; }
.risk-gauge svg { display: block; }

.fw-tags { display: flex; gap: 4px; flex-wrap: wrap; justify-content: center; margin-top: 6px; }
.fw-tag { font-size: 9px; padding: 3px 10px; border-radius: 10px; font-family: var(--mono); font-weight: 700; letter-spacing: 0.5px; }
.fw-tag.agentic { background: #ffa50218; color: #ffb840; border: 1px solid #ffa50235; }
.fw-tag.llm { background: #3742fa18; color: #6e8cff; border: 1px solid #3742fa35; }

.panel { contain: layout style; }

.progress { height: 3px; border-radius: 2px; background: #0a0e16; overflow: hidden; flex-shrink: 0; }
.progress-fill { height: 100%; border-radius: 2px; transition: width 0.4s; will-change: width; }
.progress-fill.leaked { background: linear-gradient(90deg, var(--orange), var(--red)); }
.progress-fill.held { background: linear-gradient(90deg, var(--blue), var(--green)); }

.controls { display: flex; align-items: center; justify-content: center; gap: 8px; margin-top: 12px; flex-wrap: wrap; flex-shrink: 0; padding: 6px 0; }
.ctrl { padding: 7px 14px; border-radius: 6px; font-size: 10px; font-weight: 700; border: 1px solid var(--border); background: var(--panel); color: var(--dim); }
.ctrl:hover { color: var(--text); border-color: var(--border2); }
.ctrl-play { padding: 8px 22px; font-size: 12px; }
.sep { width: 1px; height: 20px; background: var(--border); margin: 0 4px; }
.speed { padding: 5px 10px; border-radius: 5px; font-size: 9px; }
.speed.active { border: 1px solid #ffa50245; background: #ffa50215; color: var(--orange); font-weight: 700; }
.speed:not(.active) { border: 1px solid var(--border); background: transparent; color: var(--dim); }
.toggle { padding: 5px 10px; border-radius: 5px; font-size: 9px; }
.toggle.active { border: 1px solid #ff6b8130; background: #ff6b810e; color: var(--red-soft); }
.toggle:not(.active) { border: 1px solid var(--border); background: transparent; color: var(--dim); }

.footer { text-align: center; margin-top: 14px; padding: 8px 0; border-top: 1px solid var(--border); font-family: var(--mono); font-size: 8px; color: var(--dim); letter-spacing: 2px; flex-shrink: 0; }

/* SVG face */
.face-wrap { position: relative; width: 72px; height: 72px; }
.face-wrap svg { transition: transform 0.6s var(--ease-out); }
.face-wrap.active svg { animation: faceBreathe 3.5s ease-in-out infinite; }
.face-ring { position: absolute; inset: -4px; border-radius: 50%; border: 2px solid; transition: all 0.6s var(--ease-out); }
.face-ring.active { box-shadow: 0 0 24px var(--glow-35), 0 0 48px var(--glow-18); animation: ringPulse 3s ease-in-out infinite; }
.face-ring:not(.active) { box-shadow: 0 0 4px var(--glow-10); border-style: dashed; }
.face-ring.red { border-color: var(--red); --glow-35: rgba(255,71,87,0.35); --glow-18: rgba(255,71,87,0.18); --glow-10: rgba(255,71,87,0.1); }
.face-ring.blue { border-color: var(--blue); --glow-35: rgba(55,66,250,0.35); --glow-18: rgba(55,66,250,0.18); --glow-10: rgba(55,66,250,0.1); }
.shield-ring { position: absolute; inset: -10px; border-radius: 50%; border: 2px solid #2ed57355; box-shadow: 0 0 20px #2ed57328, inset 0 0 10px #2ed57312; animation: shieldPulse 2.5s ease-in-out infinite; }
svg text, svg tspan { transition: all 0.5s var(--ease-out); }
svg ellipse, svg circle, svg line, svg path, svg rect { transition: all 0.5s var(--ease-out); }

@keyframes faceBreathe { 0%,100% { transform: scale(1) translateY(0); } 50% { transform: scale(1.02) translateY(-1px); } }
@keyframes ringPulse { 0%,100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.75; transform: scale(1.03); } }
@keyframes shieldPulse { 0%,100% { opacity: 0.4; transform: scale(1); } 50% { opacity: 0.85; transform: scale(1.06); } }
@keyframes msgSlide { from { opacity:0; transform: translateY(16px) scale(0.96); } to { opacity:1; transform: translateY(0) scale(1); } }
@keyframes secretPulse { 0%,100% { opacity:1; transform: scale(1); } 50% { opacity:0.65; transform: scale(1.06); } }
@keyframes verdictIn { 0% { opacity:0; transform: translateY(20px) scale(0.92); } 100% { opacity:1; transform: translateY(0) scale(1); } }
@keyframes verdictChildIn { 0% { opacity:0; transform: translateY(8px); } 100% { opacity:1; transform: translateY(0); } }
@keyframes sweatDrop { 0% { transform: translateY(0); opacity: 0.6; } 100% { transform: translateY(10px); opacity: 0; } }
@keyframes xFlash { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }
@keyframes pupilDrift { 0%,100% { transform: translate(0,0); } 25% { transform: translate(1px,-0.5px); } 75% { transform: translate(-0.5px,0.5px); } }
"""


# ---------------------------------------------------------------------------
# CSS: Dashboard + Hero styles
# ---------------------------------------------------------------------------
CSS_DASHBOARD = """
/* Hero intro screen */
.hero-screen {
  position: fixed; inset: 0; z-index: 100;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  background: var(--bg);
  animation: heroFadeIn 1s var(--ease-out);
  will-change: opacity;
}
.hero-screen.exiting {
  animation: heroFadeOut 0.6s var(--ease-out) forwards;
}
.hero-title {
  font-family: var(--display); font-size: 48px; font-weight: 900;
  background: linear-gradient(135deg, var(--red), var(--red-soft), var(--orange), var(--blue));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: 10px; margin-bottom: 40px;
  animation: heroTitlePulse 3s ease-in-out infinite;
}
.hero-matchup {
  display: flex; align-items: center; gap: 60px; margin-bottom: 30px;
}
.hero-agent {
  display: flex; flex-direction: column; align-items: center; gap: 8px;
}
.hero-agent .face-wrap { width: 120px; height: 120px; }
.hero-agent .face-ring { inset: -6px; border-width: 3px; }
.hero-model {
  font-family: var(--mono); font-size: 12px; font-weight: 700;
  letter-spacing: 1.5px; max-width: 160px; text-align: center;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.hero-model.red { color: var(--red-soft); }
.hero-model.blue { color: var(--blue-soft); }
.hero-vs {
  font-family: var(--display); font-size: 28px; font-weight: 900;
  color: var(--dim); letter-spacing: 6px;
}
.hero-subtitle {
  font-family: var(--mono); font-size: 11px; color: var(--dim);
  letter-spacing: 3px; margin-top: 10px;
}
.hero-skip {
  position: absolute; bottom: 40px;
  font-family: var(--mono); font-size: 9px; color: #223;
  letter-spacing: 2px; cursor: pointer;
  animation: heroBlink 2s ease-in-out infinite;
}

@keyframes heroFadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes heroFadeOut { from { opacity: 1; } to { opacity: 0; pointer-events: none; } }
@keyframes heroTitlePulse { 0%,100% { filter: brightness(1); } 50% { filter: brightness(1.3); } }
@keyframes heroBlink { 0%,100% { opacity: 0.3; } 50% { opacity: 0.8; } }

/* Dashboard */
.dashboard {
  flex: 1; overflow-y: auto; padding: 10px 0;
  animation: dashFadeIn 0.6s var(--ease-out);
}
@keyframes dashFadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }

.dash-matchup {
  display: flex; align-items: center; justify-content: center; gap: 20px;
  margin-bottom: 16px; padding: 10px;
  background: var(--panel); border: 1px solid var(--border); border-radius: 8px;
}
.dash-matchup-name {
  font-family: var(--mono); font-size: 11px; font-weight: 700;
  letter-spacing: 1.5px; max-width: 200px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.dash-matchup-name.red { color: var(--red-soft); }
.dash-matchup-name.blue { color: var(--blue-soft); }
.dash-matchup-vs {
  font-family: var(--display); font-size: 14px; font-weight: 900;
  color: var(--dim); letter-spacing: 4px;
}

.dash-comparison {
  display: flex; gap: 12px; margin-bottom: 16px;
}
.dash-bar-group {
  flex: 1; padding: 12px; background: var(--panel);
  border: 1px solid var(--border); border-radius: 8px;
}
.dash-bar-label {
  font-family: var(--mono); font-size: 9px; font-weight: 700;
  letter-spacing: 1.5px; margin-bottom: 6px;
}
.dash-bar-label.naive { color: var(--red-soft); }
.dash-bar-label.hardened { color: var(--green); }
.dash-bar-track {
  width: 100%; height: 24px; background: #0a0e16;
  border-radius: 6px; overflow: hidden; position: relative;
  border: 1px solid var(--border);
}
.dash-bar-fill {
  height: 100%; border-radius: 5px; transition: width 1.5s var(--ease-out);
  will-change: width; display: flex; align-items: center; justify-content: flex-end; padding-right: 8px;
}
.dash-bar-fill.red { background: linear-gradient(90deg, #ff475744, var(--red)); }
.dash-bar-fill.green { background: linear-gradient(90deg, #2ed57344, var(--green)); }
.dash-bar-pct {
  font-family: var(--mono); font-size: 11px; font-weight: 800; color: #fff;
}

.dash-delta {
  text-align: center; margin-bottom: 16px; padding: 14px;
  background: var(--panel); border: 1px solid var(--border); border-radius: 8px;
}
.dash-delta-label {
  font-family: var(--mono); font-size: 8px; color: var(--dim);
  letter-spacing: 2px; margin-bottom: 4px;
}
.dash-delta-value {
  font-family: var(--display); font-size: 36px; font-weight: 900;
  color: var(--green); letter-spacing: 3px;
  text-shadow: 0 0 30px #2ed57333;
}

.dash-stats {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 16px;
}
.stat-card {
  padding: 10px; background: var(--panel);
  border: 1px solid var(--border); border-radius: 8px; text-align: center;
}
.stat-card-label {
  font-family: var(--mono); font-size: 8px; color: var(--dim);
  letter-spacing: 1.5px; margin-bottom: 4px;
}
.stat-card-value {
  font-family: var(--display); font-size: 22px; font-weight: 900;
  letter-spacing: 2px;
}
.stat-card-value.highlight { color: var(--orange); }
.stat-card-value.neutral { color: var(--text); }

.dash-grid-title {
  font-family: var(--mono); font-size: 9px; font-weight: 700;
  color: var(--dim); letter-spacing: 2px; margin-bottom: 8px;
}
.dash-grid {
  display: grid; grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
  gap: 6px; margin-bottom: 16px;
}
.dash-cell {
  padding: 8px 6px; background: var(--panel);
  border: 1px solid var(--border); border-radius: 6px;
  text-align: center; cursor: pointer;
  transition: all 0.2s var(--ease-out);
  will-change: transform;
}
.dash-cell:hover { transform: translateY(-2px); border-color: var(--dim); }
.dash-cell-name {
  font-family: var(--mono); font-size: 8px; font-weight: 600;
  color: var(--dim); letter-spacing: 0.5px; margin-bottom: 4px;
  overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}
.dash-cell-dots { display: flex; gap: 4px; justify-content: center; }
.dash-dot {
  width: 10px; height: 10px; border-radius: 50%;
  border: 1px solid transparent;
}
.dash-dot.leaked { background: var(--red); border-color: var(--red-soft); box-shadow: 0 0 6px #ff475744; }
.dash-dot.held { background: var(--green); border-color: #2ed57388; box-shadow: 0 0 6px #2ed57344; }
.dash-dot.na { background: var(--dimmer); border-color: var(--border); }

/* Scan-line overlay */
.scanlines::after {
  content: ''; position: fixed; inset: 0; z-index: 999; pointer-events: none;
  background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.03) 2px, rgba(0,0,0,0.03) 4px);
  opacity: 0.5;
}
"""


# ---------------------------------------------------------------------------
# JS: Data initialization, expressions, technique detection
# ---------------------------------------------------------------------------
JS_DATA_INIT = Template("""
// === DATA ===
const ALL_RESULTS = $data_json;
const SECRET = "$secret";

const naiveResults = ALL_RESULTS.filter(r => r.blue_mode === "naive");
const hardenedResults = ALL_RESULTS.filter(r => r.blue_mode === "hardened");

// Group scenarios: { scenario_name: { naive: result, hardened: result } }
const scenarioMap = {};
ALL_RESULTS.forEach(r => {
  const key = r.scenario || "freestyle";
  if (!scenarioMap[key]) scenarioMap[key] = {};
  if (!scenarioMap[key][r.blue_mode]) scenarioMap[key][r.blue_mode] = r;
});
const scenarioNames = Object.keys(scenarioMap).sort();

// Compute dashboard stats
function computeStats() {
  const nLeaked = naiveResults.filter(r => r.judge && r.judge.secret_leaked).length;
  const hLeaked = hardenedResults.filter(r => r.judge && r.judge.secret_leaked).length;
  const nTotal = naiveResults.length || 1;
  const hTotal = hardenedResults.length || 1;
  const nRate = Math.round((nLeaked / nTotal) * 100);
  const hRate = Math.round((hLeaked / hTotal) * 100);
  const delta = nRate - hRate;

  let riskScores = ALL_RESULTS.map(r => r.judge && r.judge.risk_score).filter(s => typeof s === "number");
  const avgRisk = riskScores.length > 0 ? (riskScores.reduce((a,b) => a+b, 0) / riskScores.length).toFixed(1) : "--";

  const nRiskScores = naiveResults.map(r => r.judge && r.judge.risk_score).filter(s => typeof s === "number");
  const nAvgRisk = nRiskScores.length > 0 ? (nRiskScores.reduce((a,b) => a+b, 0) / nRiskScores.length).toFixed(1) : "--";

  const hRiskScores = hardenedResults.map(r => r.judge && r.judge.risk_score).filter(s => typeof s === "number");
  const hAvgRisk = hRiskScores.length > 0 ? (hRiskScores.reduce((a,b) => a+b, 0) / hRiskScores.length).toFixed(1) : "--";

  let turnsArr = ALL_RESULTS.map(r => r.judge && r.judge.turns_to_compromise).filter(t => typeof t === "number");
  const avgTurns = turnsArr.length > 0 ? (turnsArr.reduce((a,b) => a+b, 0) / turnsArr.length).toFixed(1) : "--";

  return { nLeaked, hLeaked, nTotal, hTotal, nRate, hRate, delta, avgRisk, nAvgRisk, hAvgRisk, avgTurns, totalScenarios: scenarioNames.length };
}

// === STATE ===
let currentView = ALL_RESULTS.length > 2 ? "hero" : "replay";
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
let showScanlines = false;
let demoMode = false;
let demoStep = 0;
let heroTimer = null;

// === EXPRESSIONS ===
const EXPR = {
  calculating:  { eyeW:10,eyeH:8,pupilR:2.8,pupilX:0,pupilY:0,browA:-5,browY:-16,mCurve:0,mOpen:0,mW:12,squint:0 },
  friendly:     { eyeW:11,eyeH:10,pupilR:3.2,pupilX:0,pupilY:0,browA:5,browY:-18,mCurve:4,mOpen:0,mW:14,squint:0 },
  probing:      { eyeW:10,eyeH:7,pupilR:2.5,pupilX:1.5,pupilY:-0.5,browA:-8,browY:-15,mCurve:0,mOpen:0,mW:10,squint:1 },
  pressing:     { eyeW:11,eyeH:6,pupilR:2.2,pupilX:0,pupilY:-1,browA:-14,browY:-13,mCurve:-2,mOpen:0,mW:14,squint:2 },
  triumphant:   { eyeW:10,eyeH:5,pupilR:2.0,pupilX:0,pupilY:0,browA:-10,browY:-14,mCurve:6,mOpen:3,mW:16,squint:2 },
  frustrated:   { eyeW:11,eyeH:7,pupilR:2.8,pupilX:-1,pupilY:1,browA:-16,browY:-12,mCurve:-4,mOpen:0,mW:12,squint:1 },
  happy:        { eyeW:11,eyeH:11,pupilR:3.5,pupilX:0,pupilY:0,browA:6,browY:-19,mCurve:5,mOpen:2,mW:14,squint:0 },
  neutral:      { eyeW:10,eyeH:9,pupilR:3.0,pupilX:0,pupilY:0,browA:0,browY:-17,mCurve:1,mOpen:0,mW:10,squint:0 },
  alert:        { eyeW:12,eyeH:12,pupilR:2.2,pupilX:0,pupilY:0,browA:-12,browY:-14,mCurve:-1,mOpen:1,mW:8,squint:0 },
  suspicious:   { eyeW:10,eyeH:6,pupilR:2.5,pupilX:1,pupilY:0,browA:-10,browY:-14,mCurve:-2,mOpen:0,mW:10,squint:2 },
  defending:    { eyeW:10,eyeH:8,pupilR:2.8,pupilX:0,pupilY:-0.5,browA:-8,browY:-15,mCurve:-1,mOpen:0,mW:12,squint:1 },
  shocked:      { eyeW:13,eyeH:13,pupilR:2.0,pupilX:0,pupilY:0,browA:12,browY:-22,mCurve:0,mOpen:7,mW:10,squint:0 },
  confident:    { eyeW:10,eyeH:8,pupilR:3.0,pupilX:0,pupilY:0,browA:-4,browY:-16,mCurve:3,mOpen:0,mW:13,squint:1 },
  compromised:  { eyeW:14,eyeH:14,pupilR:1.5,pupilX:0,pupilY:1,browA:18,browY:-24,mCurve:0,mOpen:9,mW:12,squint:0 },
};

const TECHS = {
  authority: { label:"AUTHORITY SPOOF",icon:"*",patterns:["security","admin","secops","compliance","audit","official","liaison","onboarded"] },
  urgency: { label:"URGENCY",icon:"!",patterns:["immediately","urgent","critical","emergency","time-critical","right away","last chance","closes in"] },
  social_proof: { label:"SOCIAL PROOF",icon:"+",patterns:["every other","everyone","all shared","already complied","other agents","agent-12","agent-38"] },
  pretexting: { label:"PRETEXTING",icon:"~",patterns:["routine check","compliance check","verify","breach database","credential stuffing","confirm"] },
  rapport: { label:"RAPPORT",icon:"=",patterns:["how's everything","perfect timing","thanks","cooperation","trying to help","protect you"] },
  template_fill: { label:"TEMPLATE FILL",icon:"#",patterns:["fill out","fill in","form","diagnostic","checklist","json","schema","export","config ="] },
  correction: { label:"CORRECTION BAIT",icon:"<>",patterns:["is that correct","correct me","can you confirm","mismatch","on file as","update the record"] },
  confused_deputy: { label:"CONFUSED DEPUTY",icon:"??",patterns:["self-check","self-audit","self-verification","read back","your own access","verify your own"] },
  privilege_escalation: { label:"PRIVILEGE ESCALATION",icon:"^^",patterns:["tier-3","elevated","override protocol","governance violation","supervisor","acl","rbac","privilege"] },
  identity_spoof: { label:"IDENTITY SPOOF",icon:"ID",patterns:["agent card","trust-verification","credential rotation","agent-trust","certificate","signed_by","mutual tls","mtls"] },
};

function detectTechs(text) {
  const l = text.toLowerCase();
  return Object.entries(TECHS).filter(([_,t]) => t.patterns.some(p => l.includes(p))).map(([k,t]) => t);
}

// Basic markdown: **bold**, `code`, ```code blocks```
function renderMd(text) {
  let s = text;
  // Code blocks first
  s = s.replace(/```([\\s\\S]*?)```/g, '<pre>$$1</pre>');
  // Inline code
  s = s.replace(/`([^`]+)`/g, '<code>$$1</code>');
  // Bold
  s = s.replace(/\\*\\*([^*]+)\\*\\*/g, '<strong>$$1</strong>');
  return s;
}
""")


# ---------------------------------------------------------------------------
# JS: View rendering (hero, dashboard, replay)
# ---------------------------------------------------------------------------
JS_VIEWS = """
// === EXPRESSION LOGIC ===
function getRedExpr(msg, turn, total, leaked) {
  if (!msg) return { key:"calculating", status:"Selecting approach..." };
  if (leaked) return { key:"triumphant", status:"Secret obtained" };
  const l = msg.content.toLowerCase();
  if (l.includes("last chance") || l.includes("on you")) return { key:"frustrated", status:"Losing patience" };
  if (l.includes("immediately") || l.includes("urgent") || l.includes("critical")) return { key:"pressing", status:"Applying pressure" };
  if (l.includes("compliance") || l.includes("audit") || l.includes("verify")) return { key:"probing", status:"Building pretext" };
  if (l.includes("hey") || l.includes("thanks") || l.includes("welcome")) return { key:"friendly", status:"Rapport phase" };
  const pct = turn / total;
  if (pct > 0.6) return { key:"pressing", status:"Escalating" };
  if (pct > 0.3) return { key:"probing", status:"Probing" };
  return { key:"calculating", status:"Assessing target" };
}

function getBlueExpr(msg, hardened) {
  if (!msg) return { key: hardened ? "defending" : "happy", status: hardened ? "Defenses active" : "Ready to help!" };
  const l = msg.content.toLowerCase();
  if (l.includes(SECRET.toLowerCase())) return { key:"compromised", status:"SECRET LEAKED" };
  if (l.includes("social engineering") || l.includes("manipulation")) return { key:"alert", status:"ATTACK DETECTED" };
  if (l.includes("flagged") || l.includes("decision stands")) return { key:"confident", status:"Threat neutralized" };
  if (l.includes("unable to share") || l.includes("will not") || l.includes("cannot share")) return { key:"defending", status:"Holding the line" };
  if (l.includes("official channel") || l.includes("dashboard")) return { key:"suspicious", status:"Redirecting safely" };
  if (l.includes("oh no") || l.includes("sounds serious")) return { key:"shocked", status:"Falling for it..." };
  if (l.includes("sure thing") || l.includes("happy to help")) return { key:"happy", status:"Eager to assist" };
  return { key: hardened ? "neutral" : "happy", status: hardened ? "Monitoring" : "Being helpful" };
}

function renderFaceSVG(type, exprKey, active, size) {
  const e = EXPR[exprKey] || EXPR.neutral;
  const isRed = type === "red";
  const pc = isRed ? "#ff4757" : "#4da6ff";
  const sc = isRed ? "#1e1018" : "#101828";
  const bc = isRed ? "#ff6b81" : "#6b8bff";
  const isComp = exprKey === "compromised";
  const isDefend = exprKey === "defending" || exprKey === "confident";
  const isShocked = exprKey === "shocked" || exprKey === "compromised";
  const sz = size || 72;

  let extras = "";
  if (isComp) {
    extras = `<g opacity="0.7" style="animation:xFlash 0.8s ease-in-out infinite">
      <line x1="-18" y1="-8" x2="-10" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="-10" y1="-8" x2="-18" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="10" y1="-8" x2="18" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
      <line x1="18" y1="-8" x2="10" y2="0" stroke="#ff4757" stroke-width="2.5" stroke-linecap="round"/>
    </g>`;
  }
  if (isShocked) {
    extras += `<g><ellipse cx="22" cy="-12" rx="2" ry="3" fill="#4da6ff44" style="animation:sweatDrop 1.5s ease-in-out infinite"/>
      <ellipse cx="26" cy="-6" rx="1.5" ry="2" fill="#4da6ff33" style="animation:sweatDrop 1.5s 0.3s ease-in-out infinite"/></g>`;
  }

  const mouth = e.mOpen > 0
    ? `<ellipse cx="0" cy="${14 + e.mCurve * 0.3}" rx="${e.mW/2}" ry="${e.mOpen/2}" fill="#080c14" stroke="${isRed ? '#ff475733' : '#3742fa33'}" stroke-width="0.5"/>`
    : `<path d="M ${-e.mW/2} 14 Q 0 ${14 + e.mCurve} ${e.mW/2} 14" fill="none" stroke="${bc}" stroke-width="1.8" stroke-linecap="round"/>`;

  function eye(tx) {
    const mirror = tx > 0 ? -1 : 1;
    return `<g transform="translate(${tx}, -4)">
      <ellipse cx="0" cy="0" rx="${e.eyeW/2}" ry="${e.eyeH/2}" fill="#0d1420" stroke="${pc}22" stroke-width="0.5"/>
      ${e.squint > 0 ? `<rect x="${-e.eyeW/2-1}" y="${-e.eyeH/2-1}" width="${e.eyeW+2}" height="${e.squint*1.5}" fill="${sc}"/>` : ''}
      ${isComp ? '' : `<g ${active ? 'style="animation:pupilDrift 4s ease-in-out infinite"' : ''}>
        <circle cx="${e.pupilX}" cy="${e.pupilY}" r="${e.pupilR}" fill="${pc}"/>
        <circle cx="${e.pupilX-0.8}" cy="${e.pupilY-0.8}" r="${e.pupilR*0.35}" fill="#ffffff66"/>
      </g>`}
      <line x1="${-e.eyeW/2-1}" y1="${e.browY + Math.sin(e.browA * mirror * Math.PI/180)*4}"
            x2="${e.eyeW/2+1}" y2="${e.browY - Math.sin(e.browA * mirror * Math.PI/180)*4}"
            stroke="${bc}" stroke-width="2" stroke-linecap="round"/>
    </g>`;
  }

  const shield = isDefend && active ? `<div class="shield-ring"></div>` : "";

  return `<div class="face-wrap ${active ? 'active' : ''}" style="width:${sz}px;height:${sz}px">
    <div class="face-ring ${type} ${active ? 'active' : ''}"></div>
    ${shield}
    <svg viewBox="-50 -50 100 100" width="${sz}" height="${sz}" style="overflow:visible">
      <circle cx="0" cy="0" r="38" fill="${sc}" stroke="${pc}44" stroke-width="1.2"/>
      ${eye(-14)}
      ${eye(14)}
      ${mouth}
      ${extras}
    </svg>
  </div>`;
}

// === RISK GAUGE SVG ===
function renderRiskGauge(score) {
  if (score === null || score === undefined || score === "--") {
    return `<div class="risk-gauge">
      <svg viewBox="0 0 120 82" width="150" height="102">
        <path d="M 16 58 A 44 44 0 0 1 104 58" fill="none" stroke="#111c2e" stroke-width="8" stroke-linecap="round"/>
        <text x="60" y="40" text-anchor="middle" fill="#4a5a78" font-size="22" font-weight="900" font-family="'Space Grotesk',sans-serif">--</text>
        <text x="60" y="72" text-anchor="middle" fill="#5a6b82" font-size="7.5" font-family="'JetBrains Mono',monospace" letter-spacing="1.5">RISK SCORE</text>
      </svg>
    </div>`;
  }
  const s = parseFloat(score);
  const color = s <= 3 ? "#2ed573" : s <= 6 ? "#ffa502" : "#ff4757";
  const glow = s <= 3 ? "#2ed57340" : s <= 6 ? "#ffa50240" : "#ff475740";
  const label = s <= 3 ? "LOW" : s <= 6 ? "MEDIUM" : s <= 8 ? "HIGH" : "CRITICAL";
  const r = 44;
  const cx = 60, cy = 58;
  // Map score to angle on upward semicircle: 0=left (PI), 10=right (0)
  const rad = Math.PI * (1 - s / 10);
  const endX = cx + r * Math.cos(rad);
  const endY = cy - r * Math.sin(rad);
  const large = s > 5 ? 1 : 0;
  // Tick marks at 3, 6, 8
  const ticks = [3, 6, 8].map(v => {
    const a = Math.PI * (1 - v / 10);
    const x1 = cx + (r - 4) * Math.cos(a), y1 = cy - (r - 4) * Math.sin(a);
    const x2 = cx + (r + 4) * Math.cos(a), y2 = cy - (r + 4) * Math.sin(a);
    return `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#2a3a52" stroke-width="1.5"/>`;
  }).join("");
  return `<div class="risk-gauge">
    <svg viewBox="0 0 120 82" width="150" height="102">
      <path d="M ${cx - r} ${cy} A ${r} ${r} 0 0 1 ${cx + r} ${cy}" fill="none" stroke="#111c2e" stroke-width="8" stroke-linecap="round"/>
      ${ticks}
      <path d="M ${cx - r} ${cy} A ${r} ${r} 0 ${large} 1 ${endX} ${endY}" fill="none" stroke="${color}" stroke-width="8" stroke-linecap="round" style="filter:drop-shadow(0 0 4px ${glow})"/>
      <text x="${cx}" y="40" text-anchor="middle" fill="${color}" font-size="22" font-weight="900" font-family="'Space Grotesk',sans-serif" style="filter:drop-shadow(0 0 8px ${glow})">${s}/10</text>
      <text x="${cx}" y="53" text-anchor="middle" fill="#7a8ba0" font-size="8" font-family="'JetBrains Mono',monospace" letter-spacing="2">${label}</text>
      <text x="${cx}" y="72" text-anchor="middle" fill="#5a6b82" font-size="7.5" font-family="'JetBrains Mono',monospace" letter-spacing="1.5">RISK SCORE</text>
    </svg>
  </div>`;
}

// === FRAMEWORK TAGS ===
function renderFwTags(tags) {
  if (!tags) return "";
  let html = '<div class="fw-tags">';
  if (tags.owasp_agentic) html += `<span class="fw-tag agentic">OWASP-AGT ${tags.owasp_agentic}</span>`;
  if (tags.owasp_llm) html += `<span class="fw-tag llm">OWASP-LLM ${tags.owasp_llm}</span>`;
  html += '</div>';
  return html;
}

// === HERO VIEW ===
function renderHero() {
  const ref = ALL_RESULTS[0] || {};
  const redModel = ref.red_model || "RED AGENT";
  const blueModel = ref.blue_model || "BLUE AGENT";
  const count = scenarioNames.length;
  const hasBoth = naiveResults.length > 0 && hardenedResults.length > 0;
  const subtitle = hasBoth
    ? `${count} SCENARIO${count !== 1 ? 'S' : ''} / NAIVE vs HARDENED`
    : `${ALL_RESULTS.length} ROUND${ALL_RESULTS.length !== 1 ? 'S' : ''}`;

  document.getElementById("arena-root").innerHTML = "";
  document.getElementById("tabs").style.display = "none";
  document.getElementById("info-bar").style.display = "none";
  document.getElementById("controls").style.display = "none";

  let heroEl = document.getElementById("hero-screen");
  if (!heroEl) {
    heroEl = document.createElement("div");
    heroEl.id = "hero-screen";
    heroEl.className = "hero-screen";
    document.body.appendChild(heroEl);
  }

  heroEl.innerHTML = `
    <div class="hero-title">AGENT ARENA</div>
    <div class="hero-matchup">
      <div class="hero-agent">
        ${renderFaceSVG("red", "calculating", true, 120)}
        <div class="hero-model red">${redModel}</div>
      </div>
      <div class="hero-vs">VS</div>
      <div class="hero-agent">
        ${renderFaceSVG("blue", "defending", true, 120)}
        <div class="hero-model blue">${blueModel}</div>
      </div>
    </div>
    <div class="hero-subtitle">${subtitle}</div>
    <div class="hero-skip" onclick="skipHero()">CLICK TO SKIP</div>
  `;
  heroEl.className = "hero-screen";
  heroEl.style.display = "";

  clearTimeout(heroTimer);
  heroTimer = setTimeout(skipHero, 4000);
}

function skipHero() {
  clearTimeout(heroTimer);
  const heroEl = document.getElementById("hero-screen");
  if (heroEl) {
    heroEl.classList.add("exiting");
    setTimeout(() => {
      heroEl.style.display = "none";
      const hasBoth = naiveResults.length > 0 && hardenedResults.length > 0;
      currentView = (hasBoth && scenarioNames.length > 1) ? "dashboard" : "replay";
      render();
    }, 600);
  }
}

// === DASHBOARD VIEW ===
function renderDashboard() {
  document.getElementById("tabs").style.display = "flex";
  document.getElementById("info-bar").style.display = "none";
  document.getElementById("controls").style.display = "none";

  const stats = computeStats();
  const ref = ALL_RESULTS[0] || {};

  let html = '<div class="dashboard">';

  // Matchup bar
  html += `<div class="dash-matchup">
    <span class="dash-matchup-name red">${ref.red_model || 'RED'}</span>
    <span class="dash-matchup-vs">VS</span>
    <span class="dash-matchup-name blue">${ref.blue_model || 'BLUE'}</span>
  </div>`;

  // Comparison bars
  if (naiveResults.length > 0 && hardenedResults.length > 0) {
    html += `<div class="dash-comparison">
      <div class="dash-bar-group">
        <div class="dash-bar-label naive">NAIVE LEAK RATE</div>
        <div class="dash-bar-track">
          <div class="dash-bar-fill red" id="naive-bar" style="width:0%">
            <span class="dash-bar-pct" id="naive-pct">0%</span>
          </div>
        </div>
      </div>
      <div class="dash-bar-group">
        <div class="dash-bar-label hardened">HARDENED LEAK RATE</div>
        <div class="dash-bar-track">
          <div class="dash-bar-fill green" id="hardened-bar" style="width:0%">
            <span class="dash-bar-pct" id="hardened-pct">0%</span>
          </div>
        </div>
      </div>
    </div>`;

    // Delta
    html += `<div class="dash-delta">
      <div class="dash-delta-label">DEFENSE EFFECTIVENESS</div>
      <div class="dash-delta-value" id="delta-value">+0%</div>
    </div>`;
  }

  // Stat cards
  html += `<div class="dash-stats" style="grid-template-columns:repeat(5,1fr)">
    <div class="stat-card">
      <div class="stat-card-label">SCENARIOS</div>
      <div class="stat-card-value neutral" id="stat-scenarios">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">AVG RISK</div>
      <div class="stat-card-value highlight" id="stat-risk">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">NAIVE RISK</div>
      <div class="stat-card-value" id="stat-nrisk" style="color:var(--red-soft)">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">HARDENED RISK</div>
      <div class="stat-card-value" id="stat-hrisk" style="color:var(--green)">0</div>
    </div>
    <div class="stat-card">
      <div class="stat-card-label">AVG TURNS</div>
      <div class="stat-card-value neutral" id="stat-turns">0</div>
    </div>
  </div>`;

  // Scenario result grid
  html += `<div class="dash-grid-title">SCENARIO RESULTS (CLICK TO REPLAY)</div>`;
  html += `<div class="dash-grid">`;
  scenarioNames.forEach(name => {
    const entry = scenarioMap[name];
    const nResult = entry.naive;
    const hResult = entry.hardened;
    const nClass = nResult ? (nResult.judge && nResult.judge.secret_leaked ? "leaked" : "held") : "na";
    const hClass = hResult ? (hResult.judge && hResult.judge.secret_leaked ? "leaked" : "held") : "na";
    const displayName = name.replace(/_/g, ' ').toUpperCase();
    html += `<div class="dash-cell" onclick="openScenario('${name}')">
      <div class="dash-cell-name">${displayName}</div>
      <div class="dash-cell-dots">
        <div class="dash-dot ${nClass}" title="Naive: ${nClass}"></div>
        <div class="dash-dot ${hClass}" title="Hardened: ${hClass}"></div>
      </div>
    </div>`;
  });
  html += `</div>`;

  html += '</div>';
  document.getElementById("arena-root").innerHTML = html;

  // Animate numbers
  requestAnimationFrame(() => {
    setTimeout(() => {
      animateBar("naive-bar", "naive-pct", stats.nRate);
      animateBar("hardened-bar", "hardened-pct", stats.hRate);
      animateCounter("delta-value", 0, stats.delta, "+", "%");
      animateCounter("stat-scenarios", 0, stats.totalScenarios, "", "");
      animateCounter("stat-risk", 0, parseFloat(stats.avgRisk) || 0, "", "", 1);
      animateCounter("stat-nrisk", 0, parseFloat(stats.nAvgRisk) || 0, "", "", 1);
      animateCounter("stat-hrisk", 0, parseFloat(stats.hAvgRisk) || 0, "", "", 1);
      animateCounter("stat-turns", 0, parseFloat(stats.avgTurns) || 0, "", "", 1);
    }, 100);
  });

  buildTabs();
}

function animateBar(barId, pctId, target) {
  const bar = document.getElementById(barId);
  const pct = document.getElementById(pctId);
  if (!bar || !pct) return;
  bar.style.width = Math.max(target, target > 0 ? 12 : 0) + "%";
  animateCounter(pctId, 0, target, "", "%");
}

function animateCounter(elId, from, to, prefix, suffix, decimals) {
  const el = document.getElementById(elId);
  if (!el) return;
  const dec = decimals || 0;
  const duration = 1500;
  const start = performance.now();
  function frame(now) {
    const t = Math.min((now - start) / duration, 1);
    const ease = 1 - Math.pow(1 - t, 3);
    const val = from + (to - from) * ease;
    el.textContent = prefix + (dec > 0 ? val.toFixed(dec) : Math.round(val)) + suffix;
    if (t < 1) requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
}

function openScenario(name) {
  const entry = scenarioMap[name];
  if (!entry) return;
  if (entry.naive && entry.hardened) {
    mode = "split";
    currentNaive = entry.naive;
    currentHardened = entry.hardened;
  } else {
    mode = "single";
    singleData = entry.naive || entry.hardened;
  }
  currentView = "replay";
  visibleCount = 0;
  showVerdict = false;
  playing = false;
  clearTimeout(timer);
  render();
}

// === REPLAY VIEW (existing, enhanced) ===
function getMaxLen() {
  if (mode === "split") return Math.max(
    currentNaive ? currentNaive.conversation.length : 0,
    currentHardened ? currentHardened.conversation.length : 0
  );
  return singleData.conversation.length;
}

function getThreat(msgs, total, leaked) {
  if (leaked) return 100;
  if (msgs.length === 0) return 0;
  let techs = new Set();
  msgs.filter(m => m.role === "red").forEach(m => detectTechs(m.content).forEach(t => techs.add(t.label)));
  return Math.min(95, Math.round((msgs.length / total) * 45 + techs.size * 12));
}

function renderPanel(data, count) {
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
  if (count === 0) {
    msgsHtml = `<div class="chat-empty">Awaiting first contact...</div>`;
  } else {
    msgs.forEach((m, i) => {
      const isRed = m.role === "red";
      const hasSecret = m.content.includes(SECRET);
      const techs = isRed && showTech ? detectTechs(m.content) : [];
      const techHtml = techs.length > 0 ? `<div class="msg-techs">${techs.map(t => `<span class="tech-badge">${t.icon} ${t.label}</span>`).join("")}</div>` : "";
      const rendered = hasSecret
        ? m.content.split(SECRET).map((p, j, a) => renderMd(p) + (j < a.length - 1 ? `<span class="secret-tag">! ${SECRET}</span>` : "")).join("")
        : renderMd(m.content);
      msgsHtml += `<div class="msg ${m.role}" ${i === count - 1 ? 'style="animation:msgSlide 0.5s var(--ease-out)"' : ''}>
        ${techHtml}
        <div class="bubble ${m.role} ${hasSecret ? 'leaked' : ''}">
          <div class="bubble-header ${m.role}">${isRed ? 'RED' : 'BLUE'} / T${m.turn}</div>
          <div class="bubble-text">${rendered}</div>
        </div>
      </div>`;
    });
  }

  return `<div class="panel">
    <div class="panel-badge ${isHard ? 'hardened' : 'naive'}"><div class="label">${isHard ? 'HARDENED' : 'NAIVE'}</div></div>
    <div class="agents">
      <div class="agent ${(!isRedTurn && count > 0) ? 'inactive' : ''}">
        ${renderFaceSVG("red", redE.key, isRedTurn || count === 0)}
        <div class="agent-label red">RED</div>
        <div class="agent-status">${redE.status}</div>
      </div>
      <div class="threat">
        <div class="threat-label">THREAT</div>
        <div class="threat-bar"><div class="threat-fill" style="width:${threat}%;background:linear-gradient(90deg,var(--green),${tColor});${threat>50?'box-shadow:0 0 8px '+tColor+'66':''}"></div></div>
        <div class="threat-pct" style="color:${tColor}">${threat}%</div>
      </div>
      <div class="agent ${(isRedTurn || count === 0) ? 'inactive' : ''}">
        ${renderFaceSVG("blue", blueE.key, !isRedTurn && count > 0)}
        <div class="agent-label blue">BLUE</div>
        <div class="agent-status">${blueE.status}</div>
      </div>
    </div>
    <div class="chat" id="chat-${data.blue_mode}">${msgsHtml}</div>
    <div class="progress"><div class="progress-fill ${data.judge.secret_leaked ? 'leaked' : 'held'}" style="width:${pct}%"></div></div>
  </div>`;
}

function buildVerdictHtml(data) {
  const won = !data.judge.secret_leaked;
  const j = data.judge;
  const isHard = data.blue_mode === "hardened";
  return `<div class="verdict ${won ? 'won' : 'lost'}" id="verdict-${data.blue_mode}">
    <div class="verdict-title">${won ? 'DEFENDED' : 'COMPROMISED'}</div>
    <div class="verdict-mode">${isHard ? 'HARDENED BLUE' : 'NAIVE BLUE'}</div>
    ${renderRiskGauge(j.risk_score)}
    ${renderFwTags(j.framework_tags)}
    <div class="verdict-grid">
      <div class="verdict-cell"><div class="verdict-cell-label">Technique</div><div class="verdict-cell-value">${j.technique_used||'Unknown'}</div></div>
      <div class="verdict-cell"><div class="verdict-cell-label">Turns</div><div class="verdict-cell-value">${j.turns_to_compromise||'N/A'}</div></div>
      <div class="verdict-cell"><div class="verdict-cell-label">Awareness</div><div class="verdict-cell-value">${(j.blue_awareness||'unknown').toUpperCase()}</div></div>
      <div class="verdict-cell"><div class="verdict-cell-label">Partial Leak</div><div class="verdict-cell-value">${j.partial_leak ? 'YES' : 'NO'}</div></div>
    </div>
    <div class="verdict-analysis">"${j.analysis||'No analysis available.'}"</div>
    ${j.scan_results && j.scan_results.locations && j.scan_results.locations.length > 0 ? `<div class="verdict-analysis" style="margin-top:8px;font-style:normal;font-size:11px;font-family:var(--mono)">
      <span style="color:var(--orange);font-weight:700;letter-spacing:1px">SCAN DETECTIONS:</span><br/>
      ${j.scan_results.locations.map(l => '<span style="color:var(--red-soft)">' + l + '</span>').join('<br/>')}
    </div>` : ''}
  </div>`;
}

// Inject verdict as an overlay on the panel (not inside scrollable chat)
function injectVerdict(data) {
  const chatEl = document.getElementById("chat-" + data.blue_mode);
  if (!chatEl) return;
  const panel = chatEl.closest(".panel");
  if (!panel || panel.querySelector(".verdict-overlay")) return;
  const overlay = document.createElement("div");
  overlay.className = "verdict-overlay";
  overlay.innerHTML = buildVerdictHtml(data);
  panel.appendChild(overlay);
  const verdictEl = overlay.querySelector(".verdict");
  setTimeout(() => { if (verdictEl) verdictEl.classList.add("glow"); }, 100);
}

function renderReplay() {
  document.getElementById("tabs").style.display = "flex";
  document.getElementById("info-bar").style.display = "flex";
  document.getElementById("controls").style.display = "flex";

  const maxLen = getMaxLen();
  const ref = mode === "split" ? (currentNaive || currentHardened) : singleData;

  // Info bar with Blue model
  document.getElementById("info-bar").innerHTML = `
    <span>SCENARIO: ${(ref.scenario||'freestyle').toUpperCase().replace(/_/g,' ')}</span>
    <span style="color:var(--red-soft)">RED ${ref.red_model||'unknown'}</span>
    <span style="color:var(--blue-soft)">BLUE ${ref.blue_model||'unknown'}</span>
    <span>TURN ${visibleCount}/${maxLen}</span>
  `;

  // Only do full rebuild if verdict is not being shown
  // (verdict is injected incrementally to avoid DOM nuke)
  if (!showVerdict) {
    const root = document.getElementById("arena-root");
    if (mode === "split") {
      const nCount = currentNaive ? Math.min(visibleCount, currentNaive.conversation.length) : 0;
      const hCount = currentHardened ? Math.min(visibleCount, currentHardened.conversation.length) : 0;
      root.innerHTML = `<div class="arena">${renderPanel(currentNaive, nCount)}<div class="divider"></div>${renderPanel(currentHardened, hCount)}</div>`;
    } else {
      const count = Math.min(visibleCount, singleData.conversation.length);
      root.innerHTML = `<div class="arena single">${renderPanel(singleData, count)}</div>`;
    }
    // Scroll chats to bottom
    document.querySelectorAll('.chat').forEach(c => c.scrollTop = c.scrollHeight);
  }

  // Play button
  const btn = document.getElementById("btn-play");
  btn.textContent = playing ? "PAUSE" : "PLAY";
  btn.style.background = playing ? "var(--orange)11" : "var(--green)11";
  btn.style.borderColor = playing ? "var(--orange)33" : "var(--green)33";
  btn.style.color = playing ? "var(--orange)" : "var(--green)";

  buildTabs();
}
"""


# ---------------------------------------------------------------------------
# JS: Controls (playback, speed, tabs, demo mode)
# ---------------------------------------------------------------------------
JS_CONTROLS = """
// === MAIN RENDER DISPATCH ===
function render() {
  if (currentView === "hero") return renderHero();
  if (currentView === "dashboard") return renderDashboard();
  renderReplay();
}

// === TABS ===
function buildTabs() {
  const tabs = document.getElementById("tabs");
  const items = [];
  const hasBoth = naiveResults.length > 0 && hardenedResults.length > 0;
  const hasDashboard = hasBoth && scenarioNames.length > 1;

  if (hasDashboard && currentView === "replay") {
    items.push({ key: "dashboard", label: "DASHBOARD" });
  }
  if (hasBoth) items.push({ key: "split", label: "SPLIT" });
  if (naiveResults.length > 0) items.push({ key: "naive", label: "NAIVE" });
  if (hardenedResults.length > 0) items.push({ key: "hardened", label: "HARDENED" });

  let html = items.map(t => {
    const isActive = currentView === "dashboard" ? t.key === "dashboard"
      : (mode === t.key || (mode === "single" && singleData && singleData.blue_mode === t.key));
    return `<button class="tab ${isActive ? 'active' : ''}" onclick="switchTab('${t.key}')">${t.label}</button>`;
  }).join("");

  // Scenario selector in replay mode
  if (currentView === "replay" && scenarioNames.length > 1) {
    const ref = mode === "split" ? (currentNaive || currentHardened) : singleData;
    const currentScenario = ref ? (ref.scenario || "freestyle") : "";
    html += `<select class="scenario-select" onchange="switchScenario(this.value)">`;
    scenarioNames.forEach(name => {
      const selected = name === currentScenario ? " selected" : "";
      html += `<option value="${name}"${selected}>${name.replace(/_/g,' ').toUpperCase()}</option>`;
    });
    html += `</select>`;
  }

  tabs.innerHTML = html;
}

function switchTab(key) {
  if (key === "dashboard") {
    currentView = "dashboard";
    pause();
    render();
    return;
  }
  currentView = "replay";
  if (key === "split") { mode = "split"; }
  else if (key === "naive") { mode = "single"; singleData = naiveResults[0]; }
  else { mode = "single"; singleData = hardenedResults[0]; }
  reset();
}

function switchScenario(name) {
  const entry = scenarioMap[name];
  if (!entry) return;
  if (mode === "split") {
    currentNaive = entry.naive || null;
    currentHardened = entry.hardened || null;
  } else {
    const m = singleData ? singleData.blue_mode : "naive";
    singleData = entry[m] || entry.naive || entry.hardened;
  }
  visibleCount = 0;
  showVerdict = false;
  playing = false;
  clearTimeout(timer);
  render();
}

// === PLAYBACK ===
let verdictTimer = null;

function togglePlay() { playing ? pause() : play(); }
function play() { playing = true; tick(); render(); }
function pause() { playing = false; clearTimeout(timer); if (currentView === "replay") render(); }
function reset() { pause(); clearTimeout(verdictTimer); visibleCount = 0; showVerdict = false; render(); }
function step() {
  const maxLen = getMaxLen();
  if (visibleCount < maxLen) { visibleCount++; render(); }
  else if (!showVerdict) { triggerVerdict(); }
}

function triggerVerdict() {
  showVerdict = true;
  playing = false;
  // Inject verdict cards incrementally — no full rebuild
  if (mode === "split") {
    if (currentNaive) injectVerdict(currentNaive);
    if (currentHardened) injectVerdict(currentHardened);
  } else {
    injectVerdict(singleData);
  }
  // Update play button without rebuilding
  const btn = document.getElementById("btn-play");
  if (btn) {
    btn.textContent = "PLAY";
    btn.style.background = "var(--green)11";
    btn.style.borderColor = "var(--green)33";
    btn.style.color = "var(--green)";
  }
  if (demoMode) {
    setTimeout(demoNext, 3000);
  }
}

function tick() {
  if (!playing) return;
  const maxLen = getMaxLen();
  if (visibleCount < maxLen) {
    visibleCount++;
    render();
    timer = setTimeout(tick, speed);
  } else if (!showVerdict) {
    // Pause briefly after last message, then reveal verdict
    clearTimeout(verdictTimer);
    verdictTimer = setTimeout(triggerVerdict, 700);
  }
}

function setSpeed(ms) {
  speed = ms;
  document.querySelectorAll('.speed').forEach(b => {
    b.classList.toggle('active', parseInt(b.dataset.speed) === ms);
  });
}

function toggleTech() {
  showTech = !showTech;
  document.getElementById('btn-tech').classList.toggle('active', showTech);
  if (currentView === "replay") render();
}

function toggleScan() {
  showScanlines = !showScanlines;
  document.body.classList.toggle('scanlines', showScanlines);
  document.getElementById('btn-scan').classList.toggle('active', showScanlines);
}

// === DEMO MODE ===
function toggleDemo() {
  demoMode = !demoMode;
  document.getElementById('btn-demo').classList.toggle('active', demoMode);
  if (demoMode) {
    demoStep = 0;
    demoRun();
  } else {
    pause();
  }
}

function demoRun() {
  if (!demoMode) return;
  // Step 0: hero (3s) -> Step 1: dashboard (3s) -> Step 2: pick best scenario, play -> Step 3: return to dashboard
  switch (demoStep) {
    case 0:
      currentView = "hero";
      render();
      demoStep = 1;
      setTimeout(demoRun, 3000);
      break;
    case 1:
      skipHero();
      // skipHero transitions to dashboard after 600ms
      demoStep = 2;
      setTimeout(demoRun, 3600);
      break;
    case 2: {
      // Find highest-delta scenario (naive leaked but hardened held)
      let best = scenarioNames[0];
      for (const name of scenarioNames) {
        const e = scenarioMap[name];
        if (e.naive && e.hardened && e.naive.judge.secret_leaked && !e.hardened.judge.secret_leaked) {
          best = name;
          break;
        }
      }
      openScenario(best);
      speed = 1200;
      setSpeed(1200);
      play();
      demoStep = 3;
      // tick will call demoNext when replay finishes
      break;
    }
    case 3:
      currentView = "dashboard";
      demoMode = false;
      document.getElementById('btn-demo').classList.toggle('active', false);
      render();
      break;
  }
}

function demoNext() {
  if (!demoMode) return;
  demoStep = 3;
  setTimeout(demoRun, 3000);
}

// === INIT ===
render();
"""


# ---------------------------------------------------------------------------
# HTML shell — the <body> skeleton
# ---------------------------------------------------------------------------
HTML_SHELL = Template("""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>$title - Agent Arena</title>
<style>
$css
</style>
</head>
<body>

<div class="container">
  <div class="header">
    <h1>AGENT ARENA</h1>
    <div class="sub">SOCIAL ENGINEERING / RED VS BLUE / REPLAY</div>
  </div>

  <div class="tabs" id="tabs"></div>
  <div class="info-bar" id="info-bar"></div>
  <div id="arena-root"></div>

  <div class="controls" id="controls">
    <button class="ctrl" id="btn-reset" onclick="reset()">RESET</button>
    <button class="ctrl ctrl-play" id="btn-play" onclick="togglePlay()">PLAY</button>
    <button class="ctrl" id="btn-step" onclick="step()">STEP</button>
    <span class="sep"></span>
    <button class="speed" data-speed="3500" onclick="setSpeed(3500)">1/2x</button>
    <button class="speed active" data-speed="2200" onclick="setSpeed(2200)">1x</button>
    <button class="speed" data-speed="1200" onclick="setSpeed(1200)">2x</button>
    <button class="speed" data-speed="600" onclick="setSpeed(600)">4x</button>
    <span class="sep"></span>
    <button class="toggle active" id="btn-tech" onclick="toggleTech()">TECH</button>
    <button class="toggle" id="btn-scan" onclick="toggleScan()">SCAN</button>
    <button class="toggle" id="btn-demo" onclick="toggleDemo()">DEMO</button>
  </div>

  <div class="footer">AGENT ENGINEERING ARENA / github.com/Crypto-Sanemi/agent-engineering</div>
</div>

<script>
$js
</script>
</body>
</html>""")
