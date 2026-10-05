import base64, os, html

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, "..", "assets")
os.makedirs(OUT, exist_ok=True)

def b64(name):
    return base64.b64encode(open(os.path.join(S, name), "rb").read()).decode()

INTER = f"""
@font-face{{font-family:'Inter';font-weight:400;src:url(data:font/woff2;base64,{b64('inter400.woff2')}) format('woff2');}}
@font-face{{font-family:'Inter';font-weight:700;src:url(data:font/woff2;base64,{b64('inter700.woff2')}) format('woff2');}}"""
MONO = f"""
@font-face{{font-family:'JBM';font-weight:400;src:url(data:font/woff2;base64,{b64('jbm400.woff2')}) format('woff2');}}
@font-face{{font-family:'JBM';font-weight:700;src:url(data:font/woff2;base64,{b64('jbm700.woff2')}) format('woff2');}}"""

BLUE, PALE, DIM, LIGHT, BG = "#58a6ff", "#c9d1d9", "#8b949e", "#79c0ff", "#0d1117"

def save(name, svg):
    open(os.path.join(OUT, name), "w").write(svg)


# ---------- banner ----------
W, H = 1200, 240
save("banner.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0b2545"/><stop offset="1" stop-color="#0d1117"/></linearGradient>
<linearGradient id="ac" x1="0" x2="1"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="#1f6feb"/></linearGradient>
<style>{INTER}
.t{{font-family:'Inter',sans-serif;font-weight:700;font-size:76px;letter-spacing:-2px;fill:#f0f6fc}}
.s{{font-family:'Inter',sans-serif;font-weight:400;font-size:22px;fill:{DIM}}}
</style></defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<circle cx="1060" cy="40" r="180" fill="{BLUE}" opacity=".07"/>
<circle cx="1120" cy="200" r="120" fill="{BLUE}" opacity=".06"/>
<text x="72" y="122" class="t">Hi, I'm Luke</text>
<rect x="74" y="146" width="64" height="4" rx="2" fill="url(#ac)"/>
<text x="72" y="192" class="s">Computer Science at Texas State · I build things for people</text>
</svg>""")


# ---------- neofetch raccoon ----------
HALF = [
    (r'    .-"-.      ', ' '),
    (r'   / .-. \_.---', '-'),
    (r"   | \ /  '    ", ' '),
    (r"    \ '.'      ", ' '),
    (r'   /           ', ' '),
    (r'  | ▄▄▄▄▄▄▄▄▄▄ ', ' '),
    (r'  | ▐▓▓(●)▓▓▓▌ ', ' '),
    (r'  | ▀▓▓▓▓▓▓▓▀  ', ' '),
    (r'   \           ', ' '),
    (r"    '.        ▄", '▄'),
    (r"      '-.     \ ".rstrip(), '_'),
    (r"         '-.___", '_'),
]
MIR = str.maketrans({'/': '\\', '\\': '/', '(': ')', ')': '(', '▐': '▌', '▌': '▐'})
ART = [l + c + l[::-1].translate(MIR) for l, c in HALF]

INFO = [
    ("title", "luke@txst"),
    ("rule", "---------"),
    ("OS", "Arch Linux x86_64"),
    ("WM", "Hyprland"),
    ("Terminal", "kitty"),
    ("Editor", "Neovim"),
    ("School", "Texas State University"),
    ("Major", "Computer Science, class of '28"),
    ("Languages", "TypeScript, C++, Python"),
    ("Stack", "Next.js, React, Svelte, Expo"),
    ("Games", "Rivaldle, SoulsDoku, CSMdle"),
    ("Traffic", "400K+ pageviews / month"),
    ("Building", "Locturne (iOS)"),
    ("GitHub", "github.com/llyons151"),
]

FS, CW, LH = 15, 9.0, 21
PADX, TOP = 34, 96
ART_W = max(len(l) for l in ART)
IX = PADX + ART_W * CW + 42
CW_W = 900
rows = max(len(ART), len(INFO) + 2)
CH = TOP + rows * LH + 40

def art_color(c, line_no=0):
    if c == "▄" and line_no == 9: return LIGHT
    if c in "▓▄▀▐▌": return "#30588a"
    if c == "●": return LIGHT
    if c in "()": return BLUE
    return PALE

def art_line(i, line):
    y = TOP + 22 + i * 18
    spans, cur, buf = [], None, ""
    for c in line:
        col = art_color(c, i)
        if col != cur and buf:
            spans.append((cur, buf)); buf = ""
        cur = col; buf += c
    if buf: spans.append((cur, buf))
    ts = "".join(f'<tspan fill="{c}">{html.escape(t)}</tspan>' for c, t in spans)
    return f'<text x="{PADX}" y="{y}" class="m" xml:space="preserve">{ts}</text>'

info_svg = []
for i, (k, v) in enumerate(INFO):
    y = TOP + i * LH
    if k == "title":
        info_svg.append(f'<text x="{IX}" y="{y}" class="m b"><tspan fill="{BLUE}">luke</tspan><tspan fill="{PALE}">@</tspan><tspan fill="{BLUE}">txst</tspan></text>')
    elif k == "rule":
        info_svg.append(f'<text x="{IX}" y="{y}" class="m" fill="{DIM}">{v}</text>')
    else:
        info_svg.append(f'<text x="{IX}" y="{y}" class="m" xml:space="preserve"><tspan class="b" fill="{BLUE}">{k}</tspan><tspan fill="{DIM}">: </tspan><tspan fill="{PALE}">{html.escape(v)}</tspan></text>')
by = TOP + (len(INFO) + 0.4) * LH
blocks = ["#0d2847", "#0f3a6b", "#1f6feb", "#388bfd", BLUE, LIGHT, "#a5d6ff", PALE]
for j, c in enumerate(blocks):
    info_svg.append(f'<rect x="{IX + j * 27}" y="{by:.0f}" width="27" height="17" fill="{c}"/>')

save("neofetch.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW_W} {CH}" width="{CW_W}" height="{CH}">
<defs><style>{MONO}
.m{{font-family:'JBM',monospace;font-size:{FS}px}} .b{{font-weight:700}}
.cur{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
</style></defs>
<rect x=".5" y=".5" width="{CW_W-1}" height="{CH-1}" rx="12" fill="#0d1117" stroke="#30363d"/>
<path d="M.5 40 V12.5 a12 12 0 0 1 12 -12 H{CW_W-12.5} a12 12 0 0 1 12 12 V40z" fill="#161b22"/>
<line x1="1" y1="40" x2="{CW_W-1}" y2="40" stroke="#30363d"/>
<circle cx="24" cy="20" r="6" fill="#30363d"/><circle cx="44" cy="20" r="6" fill="#30363d"/><circle cx="64" cy="20" r="6" fill="{BLUE}"/>
<text x="{CW_W/2}" y="25" text-anchor="middle" class="m" fill="{DIM}">luke@txst: ~</text>
<text x="{PADX}" y="68" class="m"><tspan fill="{BLUE}" class="b">[luke@txst ~]$</tspan><tspan fill="{PALE}"> neofetch</tspan></text>
{chr(10).join(art_line(i, l) for i, l in enumerate(ART))}
{chr(10).join(info_svg)}
<text x="{PADX}" y="{CH-22}" class="m"><tspan fill="{BLUE}" class="b">[luke@txst ~]$</tspan><tspan class="cur" fill="{PALE}"> █</tspan></text>
</svg>""")
print("ok", CH)
