#!/usr/bin/env python3
"""Génère assets/terminal.svg : un header terminal animé (CSS keyframes, pas de JS)."""
import random, html

W, H = 880, 300
CYCLE = 16.0            # secondes
FS = 16                 # font-size
CW = FS * 0.6           # largeur d'un caractère (monospace forcé via textLength)
X0 = 30                 # marge gauche du contenu
TOPBAR = 36
LINE_H = 31
FIRST_BASELINE = TOPBAR + 34

GREEN = "#00ff9c"
DIM = "#8b949e"
TXT = "#e6edf3"
SOFT = "#7ee787"
BG = "#05080b"
BAR = "#0b1016"
BORDER = "#17402f"

# (segments, start, duree)  |  segment = (texte, couleur, classe_extra)
LINES = [
    ([("$ ", GREEN, ""), ("whoami", TXT, "")], 0.40, 0.75),
    ([("Loïc Ruyssen · student @ Epitech · France", SOFT, "")], 1.45, 0.95),
    ([("$ ", GREEN, ""), ("cat ~/.config/focus", TXT, "")], 2.75, 0.95),
    ([("cybersecurity · full-stack · LLM tooling", DIM, "")], 4.05, 0.95),
    ([("$ ", GREEN, ""), ("./ship --loop", TXT, "")], 5.35, 0.75),
    ([("build. break. learn. repeat.", GREEN, "glow")], 6.45, 1.20),
    ([("$ ", GREEN, "")], 8.00, 0.15),
]

def pct(t):
    return round(t / CYCLE * 100, 3)

parts_defs, parts_body, css = [], [], []

css.append(f"""
  .t {{ font-family: 'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'DejaVu Sans Mono',monospace;
        font-size: {FS}px; dominant-baseline: alphabetic; white-space: pre; }}
  .glow {{ filter: url(#glow); font-weight: 700; }}
  .rain {{ font-family: monospace; font-size: 15px; fill: {GREEN}; }}
  @keyframes blink {{ 0%,49% {{ opacity: 1 }} 50%,100% {{ opacity: 0 }} }}
""")

# ---------- lignes tapées ----------
cursor_keys = []
for i, (segs, start, dur) in enumerate(LINES, 1):
    y = FIRST_BASELINE + (i - 1) * LINE_H
    full = "".join(s[0] for s in segs)
    n = max(len(full), 1)
    width = n * CW
    # texte découpé en tspans positionnés au caractère près
    tspans, x = [], X0
    for text, color, extra in segs:
        w = len(text) * CW
        cls = f'class="{extra}"' if extra else ""
        tspans.append(
            f'<tspan x="{x:.1f}" textLength="{w:.1f}" lengthAdjust="spacingAndGlyphs" '
            f'fill="{color}" {cls}>{html.escape(text)}</tspan>'
        )
        x += w
    parts_body.append(
        f'  <g clip-path="url(#clip{i})"><text class="t" y="{y}">{"".join(tspans)}</text></g>'
    )
    parts_defs.append(
        f'    <clipPath id="clip{i}" clipPathUnits="userSpaceOnUse">'
        f'<rect class="m{i}" x="{X0}" y="{y - FS + 2}" height="{FS + 8}" width="0"/></clipPath>'
    )
    css.append(f"""
  .m{i} {{ animation: type{i} {CYCLE}s infinite; }}
  @keyframes type{i} {{
    0%, {pct(start)}% {{ width: 0; animation-timing-function: steps({n}); }}
    {pct(start + dur)}%, 100% {{ width: {width:.1f}px; }}
  }}""")
    # trajet du curseur (un seul curseur pour tout le terminal)
    cursor_keys.append((start, dur, X0, y, width, n))

# ---------- curseur unique ----------
frames = []
prev_end = 0.0
for idx, (start, dur, x, y, width, n) in enumerate(cursor_keys):
    ty = y - FS + 2
    frames.append((start, f"translate({x:.1f}px,{ty:.1f}px)", f"steps({n})"))
    frames.append((start + dur, f"translate({x + width:.1f}px,{ty:.1f}px)", "step-end"))

kf = []
for t, tr, tf in frames:
    kf.append(f"    {pct(t)}% {{ transform: {tr}; animation-timing-function: {tf}; }}")
kf.append(f"    100% {{ transform: {frames[-1][1]}; }}")
css.append(f"""
  .cursor {{ animation: blink 1s steps(1) infinite, move {CYCLE}s infinite; }}
  @keyframes move {{
{chr(10).join(kf)}
  }}""")

# ---------- pluie de caractères ----------
random.seed(7)
GLYPHS = "01アイウエオカキクケコサシスセソタチツテトナニヌネノ<>{}[]#$/\\|_-=+*"
rain = []
for c in range(20):
    cx = 22 + c * 44 + random.randint(-6, 6)
    chars = "".join(random.choice(GLYPHS) for _ in range(16))
    dur = round(random.uniform(7, 15), 1)
    delay = round(random.uniform(-14, 0), 1)
    op = round(random.uniform(0.30, 0.65), 2)
    tspans = "".join(
        f'<tspan x="{cx}" dy="{0 if k == 0 else 19}">{html.escape(ch)}</tspan>'
        for k, ch in enumerate(chars)
    )
    rain.append(
        f'    <text class="rain r{c}" y="0" opacity="{op}">{tspans}</text>'
    )
    css.append(f"""
  .r{c} {{ animation: fall {dur}s linear {delay}s infinite; }}""")
css.append("""
  @keyframes fall { from { transform: translateY(-320px); } to { transform: translateY(320px); } }
  .scan { animation: sweep 7s linear infinite; }
  @keyframes sweep { from { transform: translateY(-120px); } to { transform: translateY(320px); } }
""")

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Terminal: Loic Ruyssen - build. break. learn. repeat.">
  <defs>
{chr(10).join(parts_defs)}
    <clipPath id="body"><rect x="1" y="{TOPBAR}" width="{W-2}" height="{H-TOPBAR-1}" rx="0"/></clipPath>
    <clipPath id="win"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12"/></clipPath>
    <linearGradient id="rainFade" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#fff" stop-opacity="0.03"/>
      <stop offset="45%" stop-color="#fff" stop-opacity="0.06"/>
      <stop offset="72%" stop-color="#fff" stop-opacity="0.20"/>
      <stop offset="100%" stop-color="#fff" stop-opacity="0.30"/>
    </linearGradient>
    <mask id="rainMask"><rect x="0" y="0" width="{W}" height="{H}" fill="url(#rainFade)"/></mask>
    <linearGradient id="scanGrad" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{GREEN}" stop-opacity="0.07"/>
      <stop offset="100%" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{GREEN}" stop-opacity="0.9"/>
      <stop offset="55%" stop-color="#1f6f3f" stop-opacity="0.55"/>
      <stop offset="100%" stop-color="#0b3d2a" stop-opacity="0.9"/>
    </linearGradient>
    <filter id="glow" x="-30%" y="-60%" width="160%" height="220%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <style>{"".join(css)}
    </style>
  </defs>

  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="{BG}"/>

  <g clip-path="url(#win)">
    <g clip-path="url(#body)" mask="url(#rainMask)">
{chr(10).join(rain)}
    </g>
    <g clip-path="url(#body)">
      <rect class="scan" x="0" y="{TOPBAR}" width="{W}" height="120" fill="url(#scanGrad)"/>
    </g>
  </g>

  <!-- barre de titre -->
  <g clip-path="url(#win)">
    <rect x="1" y="1" width="{W-2}" height="{TOPBAR}" fill="{BAR}"/>
  </g>
  <line x1="1" y1="{TOPBAR}" x2="{W-1}" y2="{TOPBAR}" stroke="{BORDER}" stroke-width="1"/>
  <circle cx="24" cy="18.5" r="5.5" fill="#ff5f56"/>
  <circle cx="44" cy="18.5" r="5.5" fill="#ffbd2e"/>
  <circle cx="64" cy="18.5" r="5.5" fill="#27c93f"/>
  <text class="t" x="{W/2}" y="23" text-anchor="middle" font-size="12.5" fill="#5b6470">loic@epitech — ~/portfolio — zsh</text>

  <!-- contenu -->
{chr(10).join(parts_body)}
  <rect class="cursor" x="0" y="0" width="{CW:.1f}" height="{FS + 6}" fill="{GREEN}" opacity="0.95"/>

  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="none" stroke="url(#edge)" stroke-width="1.6"/>
</svg>
"""

open("assets/terminal.svg", "w", encoding="utf-8").write(svg)
print("assets/terminal.svg", len(svg), "bytes")
