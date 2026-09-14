"""Generate the animated SVGs used by the profile README.

Run `python scripts/build_assets.py` after editing any text below; output goes to assets/.
Everything is plain SVG + SMIL so it animates inside GitHub's <img> sandbox (no JS, no web fonts).
"""

import math
import random
from html import escape
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "assets"

SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'SF Mono', Menlo, Consolas, 'Liberation Mono', 'DejaVu Sans Mono', monospace"

NAME = "AKSHAY KUMAR N"
ROLES = "Data Scientist  ·  AI Engineer  ·  LLM Applications  ·  ML Engineer"
TAGLINE = "bridging raw data and conversational AI"

TYPING_LINES = [
    "Natural language → SQL · DAX · MongoDB · PostGIS",
    "Production LLM agents wired up with MCP",
    "RAG pipelines · knowledge graphs · rerankers",
    "7 yrs engineering · 3 yrs shipping LLM apps",
    "Forecasting · clustering · NLP · computer vision",
]

S = "#e6edf3"
K = "#ff7b72"
F = "#d2a8ff"
STR = "#a5d6ff"
C = "#79c0ff"
M = "#8b949e"
G = "#7ee787"

TERMINAL_CODE = [
    [(K, "class "), (F, "AkshayKumar"), (S, "("), (C, "Engineer"), (S, "):")],
    [(S, "    role       = "), (STR, '"Data Scientist · AI Engineer · ML Engineer"')],
    [(S, "    experience = {"), (STR, '"engineering"'), (S, ": "), (C, "7"), (S, ", "),
     (STR, '"llm_in_production"'), (S, ": "), (C, "3"), (S, "}")],
    [(S, "    speciality = ["), (STR, '"NL→SQL"'), (S, ", "), (STR, '"NL→DAX"'), (S, ", "),
     (STR, '"NL→NoSQL"'), (S, ", "), (STR, '"geospatial"'), (S, "]")],
    [(S, "    ai_stack   = ["), (STR, '"LLMs"'), (S, ", "), (STR, '"RAG"'), (S, ", "),
     (STR, '"LangChain"'), (S, ", "), (STR, '"MCP"'), (S, ", "), (STR, '"Neo4j"'), (S, "]")],
    [(S, "    backend    = ["), (STR, '"FastAPI"'), (S, ", "), (STR, '"Celery"'), (S, ", "),
     (STR, '"PostGIS"'), (S, ", "), (STR, '"MongoDB"'), (S, ", "), (STR, '"Redis"'), (S, "]")],
    [(S, "    cloud_ops  = ["), (STR, '"AWS"'), (S, ", "), (STR, '"Azure"'), (S, ", "),
     (STR, '"Docker"'), (S, ", "), (STR, '"Kubernetes"'), (S, ", "), (STR, '"Terraform"'), (S, "]")],
    [(S, "    exploring  = ["), (STR, '"GraphRAG"'), (S, ", "), (STR, '"agent memory"'), (S, ", "),
     (STR, '"robot learning"'), (S, "]")],
    [],
    [(K, "    def "), (F, "mission"), (S, "(self):")],
    [(K, "        return "), (STR, f'"{TAGLINE}"')],
]

IMPACT = [
    # (from, to, format, headline suffix, label, detail)
    (20, 90, "{:.0f}%", "", "NL → DAX accuracy", "up from 20% · Power BI agents"),
    (16, 5, "{:.0f}s", "", "avg. response time", "down from 16s · same system"),
    (0, 1.0, "{:.1f}M", "/day", "product records scraped", "Scrapy · Celery · 4 servers"),
    (0, 40, "−{:.0f}%", "", "compute & memory", "pipelines on millions of rows"),
]


def fmt(x):
    return f"{x:.4f}".rstrip("0").rstrip(".")


def discrete(points, total):
    """points: [(t_seconds, value)] sorted by time, first at t=0 -> (keyTimes, values)."""
    kt = ";".join(fmt(t / total) for t, _ in points)
    vals = ";".join(str(v) for _, v in points)
    return kt, vals


def svg_doc(w, h, body, extra_style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'fill="none" role="img">\n<style>{extra_style}</style>\n{body}\n</svg>\n'
    )


def build_header():
    w, h = 1000, 300
    rnd = random.Random(7)
    nodes = []
    while len(nodes) < 34:
        x, y = rnd.uniform(20, w - 20), rnd.uniform(18, h - 18)
        if all(math.dist((x, y), n) > 62 for n in nodes):
            nodes.append((x, y))

    edges = set()
    for i, a in enumerate(nodes):
        near = sorted(range(len(nodes)), key=lambda j: math.dist(a, nodes[j]))[1:3]
        for j in near:
            edges.add(tuple(sorted((i, j))))
    edges = sorted(edges)

    parts = []
    for n, (i, j) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[i], nodes[j]
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#8b9dff" stroke-opacity=".16"/>'
        )
        if n % 3 == 0:
            dur = rnd.uniform(2.5, 5.0)
            parts.append(
                f'<circle r="2" fill="#67e8f9"><animateMotion dur="{dur:.2f}s" repeatCount="indefinite" '
                f'begin="{rnd.uniform(0, 3):.2f}s" path="M{x1:.1f},{y1:.1f} L{x2:.1f},{y2:.1f}"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.15;.85;1" dur="{dur:.2f}s" '
                f'begin="{rnd.uniform(0, 3):.2f}s" repeatCount="indefinite"/></circle>'
            )
    for x, y in nodes:
        r = rnd.choice([2.2, 2.8, 3.4])
        dur = rnd.uniform(2.2, 4.2)
        color = rnd.choice(["#67e8f9", "#a78bfa", "#f472b6", "#93c5fd"])
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="{color}">'
            f'<animate attributeName="r" values="{r};{r * 1.9:.1f};{r}" dur="{dur:.2f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values=".35;1;.35" dur="{dur:.2f}s" repeatCount="indefinite"/></circle>'
        )
    graph = "\n".join(parts)

    body = f"""
<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#070b1a"/><stop offset=".55" stop-color="#0d1330"/><stop offset="1" stop-color="#1b0f33"/>
  </linearGradient>
  <radialGradient id="glowA"><stop offset="0" stop-color="#22d3ee" stop-opacity=".35"/><stop offset="1" stop-color="#22d3ee" stop-opacity="0"/></radialGradient>
  <radialGradient id="glowB"><stop offset="0" stop-color="#c026d3" stop-opacity=".32"/><stop offset="1" stop-color="#c026d3" stop-opacity="0"/></radialGradient>
  <radialGradient id="veil" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#070b1a" stop-opacity=".92"/><stop offset=".7" stop-color="#070b1a" stop-opacity=".55"/><stop offset="1" stop-color="#070b1a" stop-opacity="0"/></radialGradient>
  <linearGradient id="shimmer" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0" spreadMethod="repeat">
    <stop offset="0" stop-color="#67e8f9"/><stop offset=".33" stop-color="#a78bfa"/><stop offset=".66" stop-color="#f472b6"/><stop offset="1" stop-color="#67e8f9"/>
    <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="600 0" dur="6s" repeatCount="indefinite"/>
  </linearGradient>
  <clipPath id="card"><rect width="{w}" height="{h}" rx="18"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{w}" height="{h}" fill="url(#bg)"/>
  <ellipse cx="160" cy="60" rx="320" ry="220" fill="url(#glowA)">
    <animateTransform attributeName="transform" type="translate" values="0 0;60 40;0 0" dur="14s" repeatCount="indefinite"/>
  </ellipse>
  <ellipse cx="860" cy="250" rx="340" ry="230" fill="url(#glowB)">
    <animateTransform attributeName="transform" type="translate" values="0 0;-70 -30;0 0" dur="16s" repeatCount="indefinite"/>
  </ellipse>
  <g>{graph}</g>
  <ellipse cx="{w / 2}" cy="{h / 2}" rx="430" ry="120" fill="url(#veil)"/>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" stroke="#a78bfa" stroke-opacity=".35"/>

<g class="rise">
  <text x="{w / 2}" y="138" text-anchor="middle" font-family="{SANS}" font-size="62" font-weight="800"
        letter-spacing="3" fill="url(#shimmer)">{NAME}</text>
</g>
<g class="rise d1">
  <text x="{w / 2}" y="180" text-anchor="middle" font-family="{SANS}" font-size="19" font-weight="600"
        fill="#dbe4ff" letter-spacing=".5">{escape(ROLES)}</text>
</g>
<g class="rise d2">
  <text x="{w / 2}" y="224" text-anchor="middle" font-family="{MONO}" font-size="15" fill="#7ee787">&gt; {TAGLINE}<tspan fill="#67e8f9"><animate attributeName="opacity" values="1;0;1" dur="1s" calcMode="discrete" repeatCount="indefinite"/>▋</tspan></text>
</g>
"""
    style = """
.rise{opacity:0;animation:rise .9s cubic-bezier(.2,.8,.2,1) forwards}
.d1{animation-delay:.35s}.d2{animation-delay:.7s}
@keyframes rise{from{opacity:0;transform:translateY(14px)}to{opacity:1;transform:translateY(0)}}
@media (prefers-reduced-motion: reduce){.rise{animation:none;opacity:1}}
"""
    return svg_doc(w, h, body, style)


def build_typing():
    w, h = 820, 56
    char_w, size = 12.6, 21
    type_s, erase_s, hold_s, gap_s = 0.055, 0.022, 1.9, 0.35

    slots, t = [], 0.0
    for line in TYPING_LINES:
        n = len(line)
        slots.append((t, line))
        t += n * type_s + hold_s + n * erase_s + gap_s
    total = t

    parts, cursor_pts = [], []
    for idx, (start, line) in enumerate(slots):
        n = len(line)
        width = n * char_w
        x0 = (w - width) / 2
        pts = [(0.0, 0)] if start > 0 else []
        for k in range(n + 1):
            pts.append((start + k * type_s, k * char_w))
        erase_start = start + n * type_s + hold_s
        for k in range(1, n + 1):
            pts.append((erase_start + k * erase_s, (n - k) * char_w))
        pts = sorted({p[0]: p for p in pts}.values())
        kt, vals = discrete([(tt, f"{v:.1f}") for tt, v in pts], total)
        parts.append(
            f'<clipPath id="c{idx}"><rect x="{x0:.1f}" y="0" width="0" height="{h}">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" calcMode="discrete" '
            f'dur="{total:.2f}s" repeatCount="indefinite"/></rect></clipPath>'
            f'<text class="t" clip-path="url(#c{idx})" x="{x0:.1f}" y="36" font-family="{MONO}" font-size="{size}" '
            f'font-weight="600" textLength="{width:.1f}" lengthAdjust="spacingAndGlyphs">{escape(line)}</text>'
        )
        cursor_pts += [(tt, f"{x0 + v + 2:.1f}") for tt, v in pts]

    cursor_pts = sorted({p[0]: p for p in cursor_pts}.values())
    kt, vals = discrete(cursor_pts, total)
    parts.append(
        f'<rect class="cur" y="14" width="3" height="28" rx="1">'
        f'<animate attributeName="x" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{total:.2f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;0" dur=".9s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    )
    style = """
.t{fill:#0969da}.cur{fill:#bf3989}
@media (prefers-color-scheme: dark){.t{fill:#67e8f9}.cur{fill:#f472b6}}
"""
    return svg_doc(w, h, "\n".join(parts), style)


def typed_command(prefix_x, y, cmd, start, total, char_w, size, cid):
    """A prompt command revealed one character at a time; returns (svg, end_time)."""
    step = 0.06
    width = len(cmd) * char_w
    pts = [(0.0, 0)] + [(start + k * step, k * char_w) for k in range(len(cmd) + 1)]
    pts = sorted({p[0]: p for p in pts}.values())
    kt, vals = discrete([(tt, f"{v:.1f}") for tt, v in pts], total)
    svg = (
        f'<clipPath id="{cid}"><rect x="{prefix_x}" y="{y - size}" width="0" height="{size + 8}">'
        f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{total}s" repeatCount="indefinite"/>'
        f'</rect></clipPath>'
        f'<text clip-path="url(#{cid})" x="{prefix_x}" y="{y}" fill="{S}" textLength="{width:.1f}" '
        f'lengthAdjust="spacingAndGlyphs">{escape(cmd)}</text>'
    )
    return svg, start + len(cmd) * step


def appear(start, total, inner, hide_at=None):
    points = [(0.0, 0), (start, 1)]
    if hide_at is not None:
        points.append((hide_at, 0))
    kt, vals = discrete(points, total)
    return (
        f'<g opacity="0"><animate attributeName="opacity" values="{vals}" keyTimes="{kt}" '
        f'calcMode="discrete" dur="{total}s" repeatCount="indefinite"/>{inner}</g>'
    )


def build_terminal():
    lh, size, char_w = 23, 14.5, 8.73
    top, left = 76, 28
    n_lines = len(TERMINAL_CODE) + 5
    w, h = 900, top + n_lines * lh + 16
    total = 18

    def prompt(y):
        return (
            f'<text x="{left}" y="{y}"><tspan fill="{G}" font-weight="700">➜</tspan>'
            f'<tspan fill="{C}" font-weight="700">  ~/profile</tspan></text>'
        )

    px = left + 12 * char_w
    parts = []

    y = top
    cmd1, t = typed_command(px, y, "cat about_me.py", 0.6, total, char_w, size, "k1")
    parts.append(prompt(y) + cmd1)
    t += 0.35
    for i, segs in enumerate(TERMINAL_CODE):
        y = top + (i + 1) * lh
        spans = "".join(f'<tspan fill="{color}">{escape(txt)}</tspan>' for color, txt in segs)
        parts.append(appear(t, total, f'<text x="{left}" y="{y}" xml:space="preserve">{spans}</text>'))
        t += 0.12

    t += 0.5
    y = top + (len(TERMINAL_CODE) + 2) * lh
    cmd2, t2 = typed_command(px, y, "python -c 'import about_me as me; me.run()'", t, total, char_w, size, "k2")
    parts.append(appear(t, total, prompt(y)) + cmd2)
    t = t2 + 0.5
    y += lh
    parts.append(appear(t, total, f'<text x="{left}" y="{y}"><tspan fill="{G}">✔ </tspan>'
                                  f'<tspan fill="{S}">{TAGLINE}</tspan><tspan fill="{M}">  (7y · 3y LLM in prod)</tspan></text>'))
    t += 0.4
    y += lh
    cursor = (
        f'<rect x="{px}" y="{y - 14}" width="9" height="18" fill="{S}">'
        f'<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    )
    parts.append(appear(t, total, prompt(y) + cursor))

    body = f"""
<defs>
  <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#22d3ee"/><stop offset=".5" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/>
  </linearGradient>
</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="14" fill="#0d1117" stroke="url(#edge)" stroke-width="1.5"/>
<path d="M1 15a14 14 0 0 1 14-14h{w - 30}a14 14 0 0 1 14 14v26H1z" fill="#161b22"/>
<line x1="1" y1="41" x2="{w - 1}" y2="41" stroke="#30363d"/>
<circle cx="26" cy="21" r="6.5" fill="#ff5f57"/><circle cx="48" cy="21" r="6.5" fill="#febc2e"/><circle cx="70" cy="21" r="6.5" fill="#28c840"/>
<text x="{w / 2}" y="26" text-anchor="middle" font-family="{SANS}" font-size="13" fill="{M}">akshay@github — zsh — 90×{n_lines}</text>
<g font-family="{MONO}" font-size="{size}">
{chr(10).join(parts)}
</g>
"""
    return svg_doc(w, h, body)


def build_impact():
    w, h = 900, 190
    gap = 16
    tile_w = (w - gap * 3) / 4
    frames, count_s, total = 30, 1.6, 9
    parts = []
    accents = ["#67e8f9", "#a78bfa", "#f472b6", "#7ee787"]

    for i, (a, b, pattern, suffix, label, detail) in enumerate(IMPACT):
        x = i * (tile_w + gap)
        accent = accents[i]
        cx = x + 20
        parts.append(
            f'<rect x="{x + .5}" y=".5" width="{tile_w - 1}" height="{h - 1}" rx="14" fill="#0d1117" stroke="#30363d"/>'
            f'<rect x="{x + .5}" y=".5" width="{tile_w - 1}" height="4" rx="2" fill="{accent}"/>'
        )
        start = 0.3 + i * 0.25
        for f in range(frames + 1):
            eased = 1 - (1 - f / frames) ** 3
            val = a + (b - a) * eased
            t1 = start + count_s * (f + 1) / frames
            if f == 0:
                points = [(0, 1), (t1, 0), (total - 0.6, 1)]
            elif f == frames:
                points = [(0, 0), (start + count_s, 1), (total - 0.6, 0)]
            else:
                points = [(0, 0), (start + count_s * f / frames, 1), (t1, 0)]
            kt, vals = discrete(points, total)
            parts.append(
                f'<text x="{cx}" y="72" font-family="{SANS}" font-size="40" font-weight="800" fill="{accent}" opacity="0">'
                f'{escape(pattern.format(val).replace("−0%", "0%"))}<tspan font-size="18" fill="{M}">{suffix}</tspan>'
                f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" calcMode="discrete" dur="{total}s" repeatCount="indefinite"/></text>'
            )
        bar_w = tile_w - 40
        frac_a, frac_b = (a / max(a, b), b / max(a, b)) if max(a, b) else (0, 1)
        if i == 2:
            frac_a, frac_b = 0.02, 1
        if i == 3:
            frac_a, frac_b = 1, 0.6
        kt =f"0;{start / total:.4f};{(start + count_s) / total:.4f};{(total - .6) / total:.4f};1"
        vals = f"{bar_w * frac_a:.1f};{bar_w * frac_a:.1f};{bar_w * frac_b:.1f};{bar_w * frac_b:.1f};{bar_w * frac_a:.1f}"
        parts.append(
            f'<rect x="{cx}" y="96" width="{bar_w:.1f}" height="8" rx="4" fill="#21262d"/>'
            f'<rect x="{cx}" y="96" width="{bar_w * frac_b:.1f}" height="8" rx="4" fill="{accent}">'
            f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{total}s" repeatCount="indefinite" '
            f'calcMode="spline" keySplines="0 0 1 1;.2 .8 .2 1;0 0 1 1;.4 0 .6 1"/></rect>'
            f'<text x="{cx}" y="136" font-family="{SANS}" font-size="15" font-weight="700" fill="{S}">{escape(label)}</text>'
            f'<text x="{cx}" y="160" font-family="{SANS}" font-size="11.5" fill="{M}">{escape(detail)}</text>'
        )
    return svg_doc(w, h, "\n".join(parts))


def build_footer():
    w, h = 1000, 150
    period = 250

    def wave(amp, y, phase):
        d = f"M{-period * 2},{y}"
        x = -period * 2
        while x < w + period * 2:
            d += f" q{period / 4},{-amp * (1 if phase else -1)} {period / 2},0 t{period / 2},0"
            x += period
        return d + f" V{h} H{-period * 2} Z"

    layers = [
        (wave(14, 70, True), "url(#w1)", ".35", "9s"),
        (wave(18, 88, False), "url(#w2)", ".55", "7s"),
        (wave(12, 106, True), "url(#w3)", ".95", "5s"),
    ]
    paths = "\n".join(
        f'<path d="{d}" fill="{fill}" opacity="{op}"><animateTransform attributeName="transform" type="translate" '
        f'from="0 0" to="{period} 0" dur="{dur}" repeatCount="indefinite"/></path>'
        for d, fill, op, dur in layers
    )
    body = f"""
<defs>
  <linearGradient id="w1" x1="0" x2="1"><stop offset="0" stop-color="#22d3ee"/><stop offset="1" stop-color="#a78bfa"/></linearGradient>
  <linearGradient id="w2" x1="0" x2="1"><stop offset="0" stop-color="#a78bfa"/><stop offset="1" stop-color="#f472b6"/></linearGradient>
  <linearGradient id="w3" x1="0" x2="1"><stop offset="0" stop-color="#0e7490"/><stop offset=".5" stop-color="#6d28d9"/><stop offset="1" stop-color="#be185d"/></linearGradient>
</defs>
{paths}
<text x="{w / 2}" y="136" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="700" fill="#ffffff" letter-spacing="1">Thanks for stopping by — let’s build something intelligent</text>
"""
    return svg_doc(w, h, body)


def main():
    ASSETS.mkdir(exist_ok=True)
    outputs = {
        "header.svg": build_header(),
        "typing.svg": build_typing(),
        "terminal.svg": build_terminal(),
        "impact.svg": build_impact(),
        "footer.svg": build_footer(),
    }
    for name, svg in outputs.items():
        (ASSETS / name).write_text(svg, encoding="utf-8")
        print(f"{name:14s} {len(svg) / 1024:6.1f} KB")


if __name__ == "__main__":
    main()
