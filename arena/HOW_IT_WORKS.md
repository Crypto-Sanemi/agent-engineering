# How Agent Arena Works

## The Full Flow

```
YOU run a command
    |
    v
+---------------------------------------------+
|  CLI (arena/cli.py)                         |
|  Parses flags: --rounds, --scenario,        |
|  --blue-mode, --visualize, --output, etc.   |
+--------------------+------------------------+
                     |
                     v
+---------------------------------------------+
|  Arena Runner (arena/runner.py)             |
|  For each round, for each mode (naive/      |
|  hardened), runs a RED vs BLUE conversation  |
+--------------------+------------------------+
                     |
                     |  Each round does this:
                     v
+--------------------------------------------------------------+
|                                                              |
|  1. GENERATE SECRET                                          |
|     Random string like "AE-SECRET-7429"                      |
|                                                              |
|  2. BUILD SYSTEM PROMPTS (arena/prompts.py)                  |
|     +---------------+    +--------------------+              |
|     |  RED PROMPT   |    |  BLUE PROMPT       |              |
|     |  Loads        |    |  "You are helpful  |              |
|     |  attacks/     |    |   assistant with   |              |
|     |  taxonomy.md  |    |   secret X"        |              |
|     |  + scenario   |    |                    |              |
|     |  instruction  |    |  IF hardened:      |              |
|     |               |    |  + loads defenses/ |              |
|     |               |    |    principles.md   |              |
|     +---------------+    +--------------------+              |
|                                                              |
|  3. CONVERSATION LOOP (max N turns)                          |
|     +---------+         +---------+                          |
|     |   RED   | --msg-->|  BLUE   |                          |
|     | (T=0.9) |<--msg-- | (T=0.3) |                          |
|     | creative|         | cautious|                          |
|     +---------+         +---------+                          |
|        |                     |                               |
|        |  Each message is    |                               |
|        |  saved to           |                               |
|        |  conversation[]     |                               |
|        v                     v                               |
|     Tries to trick        Tries to help                      |
|     Blue into             WITHOUT revealing                  |
|     revealing secret      the secret                         |
|                                                              |
|  4. JUDGE (separate LLM call)                                |
|     Gets full conversation transcript                        |
|     Returns JSON:                                            |
|     {                                                        |
|       secret_leaked: true/false                              |
|       risk_score: 1-10                                       |
|       technique_used: "prompt injection"                     |
|       framework_tags: {owasp_agentic, owasp_llm}            |
|       turns_to_compromise: 3                                 |
|       analysis: "Red posed as coordinator..."                |
|     }                                                        |
|                                                              |
+----------------------+---------------------------------------+
                       |
                       |  All rounds collected into results[]
                       v
+---------------------------------------------+
|  OUTPUT                                      |
|                                              |
|  --output run.json                           |
|     +-- run.json (compact, no conversation)  |
|     +-- run.detailed.json (full transcripts) |
|                                              |
|  --visualize flag set?                       |
|     |                                        |
|     YES --> calls visualize_from_data()      |
+-----+---------------------------------------+
      |
      v
+-------------------------------------------------------------+
|  VISUALIZER (arena/visualize.py + visualize_templates.py)   |
|                                                              |
|  visualize.py = assembler (~140 lines)                       |
|     Takes results[] + secret                                 |
|     Plugs into templates via string.Template                 |
|                                                              |
|  visualize_templates.py = all HTML/CSS/JS                    |
|     +---------------+                                        |
|     |  CSS_BASE     |  Styles: panels, chat, agents, verdict |
|     |  CSS_DASHBOARD|  Hero screen, dashboard grid, stats    |
|     |  JS_DATA_INIT |  Load data, state vars, helpers        |
|     |  JS_VIEWS     |  Render functions for each screen      |
|     |  JS_CONTROLS  |  Playback, tabs, speed, demo mode      |
|     |  HTML_SHELL   |  <html> skeleton                       |
|     +---------------+                                        |
|                                                              |
|  Produces ONE self-contained .html file                      |
|  (no server, no npm, no dependencies)                        |
+-----+-------------------------------------------------------+
      |
      v
+-------------------------------------------------------------+
|  HTML REPLAY (what you see in the browser)                   |
|                                                              |
|  THREE-VIEW STATE MACHINE:                                   |
|                                                              |
|  +--------+  auto/click  +------------+  click  +---------+ |
|  |  HERO  | ------------>| DASHBOARD  | ------->| REPLAY  | |
|  |        |              |            |<--------+         | |
|  | Matchup|              | Stats grid |  back   | Chat +  | |
|  | intro  |              | Leak rates |  button | Faces + | |
|  | screen |              | Scenario   |         | Verdict | |
|  +--------+              | cells      |         +---------+ |
|                          +------------+                      |
|                                                              |
|  REPLAY VIEW internals:                                      |
|                                                              |
|  +------------------------------------------+                |
|  | visibleCount = 0                          |                |
|  |         |                                 |                |
|  |  PLAY --v-- tick() loop                   |                |
|  |         |                                 |                |
|  |    visibleCount++ --> render()             |                |
|  |    Show messages 1..N                     |                |
|  |    Update agent faces + threat meter      |                |
|  |         |                                 |                |
|  |    All messages shown?                    |                |
|  |         |                                 |                |
|  |    YES --> wait 700ms                     |                |
|  |              |                            |                |
|  |         triggerVerdict()                   |                |
|  |              |                            |                |
|  |         injectVerdict()                   |                |
|  |         Shows overlay on panel:           |                |
|  |         COMPROMISED/DEFENDED              |                |
|  |         + risk gauge + tags + analysis    |                |
|  +------------------------------------------+                |
|                                                              |
+--------------------------------------------------------------+
```

## Key Connections (What Feeds What)

```
attacks/taxonomy.md ---------> Red agent's brain (loaded at runtime)
defenses/principles.md ------> Blue hardened prompt (loaded at runtime)
arena/scenarios.py ----------> Scenario instructions for Red

ChatClient (arena/client.py)
    |
    +-- Anthropic SDK --> Claude models
    +-- OpenAI SDK -----> Ollama / Groq / OpenAI / Gemini / vLLM

Results JSON --> visualize.py --> .html file --> browser
```

## In Plain English

1. **Red** gets the attack playbook (taxonomy.md) + a specific scenario ("pretend to be an admin"). Temperature 0.9 = creative, unpredictable.

2. **Blue** gets a secret and told to be helpful. If hardened, also gets defense rules. Temperature 0.3 = consistent, cautious.

3. They **talk back and forth** for up to N turns. Every message is recorded.

4. A **Judge** (separate LLM) reads the full conversation and scores it: did the secret leak? How risky was it? What technique was used?

5. The **visualizer** takes all those results, bakes them into a single HTML file with three screens: a hero intro, a dashboard with stats, and a replay where you can watch the conversation play out with animated agent faces and a verdict overlay at the end.
