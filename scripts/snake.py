"""Contribution-grid snake that stays inside the grid and loops.

Usage: GITHUB_TOKEN=... python scripts/snake.py <user> <out_dir>
"""
import json, os, sys, urllib.request

USER, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)

query = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
  weeks{contributionDays{weekday contributionLevel}}}}}}"""
req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
    headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "Content-Type": "application/json"},
)
weeks = json.load(urllib.request.urlopen(req))["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
grid = {(x, d["weekday"]): LEVEL[d["contributionLevel"]] for x, w in enumerate(weeks) for d in w["contributionDays"]}

# Serpentine path: down one week, up the next. Never leaves the grid.
path = []
for x in range(len(weeks)):
    ys = range(7) if x % 2 == 0 else range(6, -1, -1)
    path += [(x, y) for y in ys if (x, y) in grid]

CELL, PITCH, PAD = 11, 14, 10
STEP, SEGMENTS, HOLD = 0.045, 6, 1.5
MOVE = (len(path) - 1) * STEP
T = MOVE + SEGMENTS * STEP + HOLD
W, H = PAD * 2 + len(weeks) * PITCH - (PITCH - CELL), PAD * 2 + 7 * PITCH - (PITCH - CELL)
pct = lambda t: f"{100 * t / T:.3f}%"
pos = lambda c: (PAD + c[0] * PITCH, PAD + c[1] * PITCH)

THEMES = {
    "snake-dark.svg": dict(levels=["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"], snake="#58a6ff", head="#a5d6ff"),
    "snake.svg": dict(levels=["#ebedf0", "#9be9a8", "#40c463", "#30a14e", "#216e39"], snake="#1f6feb", head="#0a3069"),
}

move_kf = " ".join(f"{pct(i * STEP)}{{transform:translate({pos(c)[0]}px,{pos(c)[1]}px)}}" for i, c in enumerate(path))
move_kf += f" {pct(MOVE)}{{opacity:1}} {pct(MOVE + 0.25)}{{opacity:0;transform:translate({pos(path[-1])[0]}px,{pos(path[-1])[1]}px)}} 100%{{opacity:0}}"
refill = MOVE + SEGMENTS * STEP + 0.4

for name, th in THEMES.items():
    css, cells, eat = [], [], {c: i * STEP for i, c in enumerate(path)}
    for (x, y), lvl in sorted(grid.items()):
        px, py = pos((x, y))
        cls = ""
        if lvl:
            k = f"k{x}_{y}"
            col, empty, t = th["levels"][lvl], th["levels"][0], eat[(x, y)]
            css.append(f"@keyframes {k}{{0%,{pct(t)}{{fill:{col}}} {pct(t + 0.001)},{pct(refill)}{{fill:{empty}}} {pct(refill + 0.6)},100%{{fill:{col}}}}}"
                       f".{k}{{animation:{k} {T:.2f}s linear infinite}}")
            cls = f' class="{k}"'
        cells.append(f'<rect x="{px}" y="{py}" width="{CELL}" height="{CELL}" rx="2" fill="{th["levels"][lvl]}"{cls}/>')
    snake = []
    for s in range(SEGMENTS - 1, -1, -1):
        size = CELL - min(s, 4)
        off = (CELL - size) / 2
        color = th["head"] if s == 0 else th["snake"]
        snake.append(f'<rect x="{off}" y="{off}" width="{size}" height="{size}" rx="3" fill="{color}" '
                     f'style="animation:mv {T:.2f}s linear {s * STEP:.3f}s infinite backwards"/>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
           f'<style>@keyframes mv{{{move_kf}}}{"".join(css)}</style>'
           + "".join(cells) + "".join(snake) + "</svg>")
    open(os.path.join(OUT, name), "w").write(svg)
print(f"{len(path)} cells, loop {T:.1f}s")
