import base64, random, os, html

S = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(S, "..", "assets")
os.makedirs(OUT, exist_ok=True)

def b64(name):
    return base64.b64encode(open(os.path.join(S, name), "rb").read()).decode()

CINZEL = f"""
@font-face{{font-family:'Cinzel';font-weight:500;src:url(data:font/woff2;base64,{b64('cinzel500.woff2')}) format('woff2');}}
@font-face{{font-family:'Cinzel';font-weight:700;src:url(data:font/woff2;base64,{b64('cinzel700.woff2')}) format('woff2');}}"""
MONO = f"""
@font-face{{font-family:'JBM';font-weight:400;src:url(data:font/woff2;base64,{b64('jbm400.woff2')}) format('woff2');}}
@font-face{{font-family:'JBM';font-weight:700;src:url(data:font/woff2;base64,{b64('jbm700.woff2')}) format('woff2');}}"""

GOLD, PALE, DIM, EMBER, BG = "#d4af37", "#e8dcb5", "#8a7a52", "#f0a830", "#0b0a07"

GOLD_GRAD = """<linearGradient id="gold" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#f7e9b8"/><stop offset=".55" stop-color="#d4af37"/><stop offset="1" stop-color="#8a6a1c"/></linearGradient>
<filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/>
  <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>"""

def save(name, svg):
    open(os.path.join(OUT, name), "w").write(svg)


def embers(n, w, h, seed):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        x, r = rnd.uniform(40, w - 40), rnd.uniform(0.8, 2.4)
        dur, delay = rnd.uniform(6, 13), -rnd.uniform(0, 13)
        out.append(f'<circle class="e d{i % 3}" cx="{x:.0f}" cy="{h + 10}" r="{r:.1f}" '
                   f'style="animation-duration:{dur:.1f}s;animation-delay:{delay:.1f}s"/>')
    return "\n".join(out)

EMBER_CSS = f""".e{{fill:{EMBER};filter:url(#eb);opacity:0;animation:rise linear infinite}}
.d1{{animation-name:rise1}} .d2{{animation-name:rise2}}
@keyframes rise{{0%{{opacity:0;transform:translate(0,0)}}15%{{opacity:.9}}100%{{opacity:0;transform:translate(30px,-300px)}}}}
@keyframes rise1{{0%{{opacity:0;transform:translate(0,0)}}20%{{opacity:.8}}100%{{opacity:0;transform:translate(-40px,-280px)}}}}
@keyframes rise2{{0%{{opacity:0;transform:translate(0,0)}}10%{{opacity:1}}100%{{opacity:0;transform:translate(10px,-320px)}}}}"""


# ---------- banner ----------
W, H = 1200, 320
save("banner.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>{GOLD_GRAD}
<radialGradient id="bg" cx=".5" cy=".55" r=".7"><stop offset="0" stop-color="#211a0c"/><stop offset="1" stop-color="{BG}"/></radialGradient>
<filter id="eb"><feGaussianBlur stdDeviation=".8"/></filter>
<style>{CINZEL}
{EMBER_CSS}
.sig{{fill:none;stroke:{GOLD};stroke-width:1.4;animation:pulse 6s ease-in-out infinite}}
@keyframes pulse{{0%,100%{{opacity:.08}}50%{{opacity:.2}}}}
.t{{font-family:'Cinzel',serif;font-weight:700;font-size:104px;letter-spacing:22px}}
.s{{font-family:'Cinzel',serif;font-weight:500;font-size:17px;letter-spacing:6px;fill:#cbb987}}
</style></defs>
<rect width="{W}" height="{H}" rx="14" fill="url(#bg)"/>
<g class="sig">
  <line x1="600" y1="18" x2="600" y2="302"/>
  <circle cx="600" cy="128" r="92"/>
  <circle cx="600" cy="196" r="58"/>
  <circle cx="600" cy="74" r="38"/>
  <path d="M400 300 A215 215 0 0 1 800 300"/>
  <path d="M455 300 A150 150 0 0 1 745 300"/>
</g>
{embers(34, W, H, 7)}
<text x="611" y="182" text-anchor="middle" class="t" fill="url(#gold)" filter="url(#glow)">LUKE</text>
<g stroke="{GOLD}" stroke-width="1" opacity=".7">
  <line x1="330" y1="222" x2="580" y2="222"/><line x1="620" y1="222" x2="870" y2="222"/></g>
<path d="M600 215 l7 7 -7 7 -7 -7z" fill="{GOLD}"/>
<text x="603" y="262" text-anchor="middle" class="s">COMPUTER SCIENCE · TEXAS STATE · I BUILD THINGS FOR PEOPLE</text>
</svg>""")


# ---------- section headings ----------
def heading(name, text, w=900, h=64, size=24):
    tw = len(text) * size * 0.78 + (len(text) - 1) * 5
    l, r = w / 2 - tw / 2 - 28, w / 2 + tw / 2 + 28
    save(name, f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>{GOLD_GRAD}
<linearGradient id="fl" x1="0" x2="1"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<linearGradient id="fr" x1="1" x2="0"><stop offset="0" stop-color="{GOLD}" stop-opacity="0"/><stop offset="1" stop-color="{GOLD}"/></linearGradient>
<style>{CINZEL}
.h{{font-family:'Cinzel',serif;font-weight:500;font-size:{size}px;letter-spacing:5px}}</style></defs>
<rect x="60" y="{h/2-.5}" width="{l-60:.0f}" height="1" fill="url(#fl)"/>
<rect x="{r:.0f}" y="{h/2-.5}" width="{w-60-r:.0f}" height="1" fill="url(#fr)"/>
<path d="M{l+8:.0f} {h/2} l5 -5 5 5 -5 5z M{r-8:.0f} {h/2} l-5 -5 -5 5 5 5z" fill="{GOLD}"/>
<text x="{w/2+2.5}" y="{h/2+size*0.36:.1f}" text-anchor="middle" class="h" fill="url(#gold)">{html.escape(text)}</text>
</svg>""")

heading("h-legacy.svg", "LEGACY DUNGEONS")
heading("h-quest.svg", "CURRENT QUEST")
heading("h-ashes.svg", "ASHES OF WAR")
heading("h-armaments.svg", "ARMAMENTS")
heading("h-runes.svg", "RUNES ACQUIRED")
heading("footer.svg", "THY STRENGTH BEFITS A CROWN", size=17)


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
    ("Quest", "Locturne (iOS)"),
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
    if c == "▄" and line_no == 9: return GOLD
    if c in "▓▄▀▐▌": return "#7a6338"
    if c == "●": return EMBER
    if c in "()": return GOLD
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
        info_svg.append(f'<text x="{IX}" y="{y}" class="m b"><tspan fill="{GOLD}">luke</tspan><tspan fill="{PALE}">@</tspan><tspan fill="{GOLD}">txst</tspan></text>')
    elif k == "rule":
        info_svg.append(f'<text x="{IX}" y="{y}" class="m" fill="{DIM}">{v}</text>')
    else:
        info_svg.append(f'<text x="{IX}" y="{y}" class="m" xml:space="preserve"><tspan class="b" fill="{GOLD}">{k}</tspan><tspan fill="{DIM}">: </tspan><tspan fill="{PALE}">{html.escape(v)}</tspan></text>')
by = TOP + (len(INFO) + 0.4) * LH
blocks = ["#1a1610", "#4a3f2a", "#8a6a1c", "#b8892a", GOLD, EMBER, "#cbb987", PALE]
for j, c in enumerate(blocks):
    info_svg.append(f'<rect x="{IX + j * 27}" y="{by:.0f}" width="27" height="17" fill="{c}"/>')

save("neofetch.svg", f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {CW_W} {CH}" width="{CW_W}" height="{CH}">
<defs><style>{MONO}
.m{{font-family:'JBM',monospace;font-size:{FS}px}} .b{{font-weight:700}}
.cur{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
</style></defs>
<rect x=".5" y=".5" width="{CW_W-1}" height="{CH-1}" rx="12" fill="#0e0c08" stroke="#3a2f17"/>
<path d="M.5 40 V12.5 a12 12 0 0 1 12 -12 H{CW_W-12.5} a12 12 0 0 1 12 12 V40z" fill="#16130c"/>
<line x1="1" y1="40" x2="{CW_W-1}" y2="40" stroke="#3a2f17"/>
<circle cx="24" cy="20" r="6" fill="#5a4a24"/><circle cx="44" cy="20" r="6" fill="#5a4a24"/><circle cx="64" cy="20" r="6" fill="{GOLD}"/>
<text x="{CW_W/2}" y="25" text-anchor="middle" class="m" fill="{DIM}">luke@txst: ~</text>
<text x="{PADX}" y="68" class="m"><tspan fill="{GOLD}" class="b">[luke@txst ~]$</tspan><tspan fill="{PALE}"> neofetch</tspan></text>
{chr(10).join(art_line(i, l) for i, l in enumerate(ART))}
{chr(10).join(info_svg)}
<text x="{PADX}" y="{CH-22}" class="m"><tspan fill="{GOLD}" class="b">[luke@txst ~]$</tspan><tspan class="cur" fill="{PALE}"> █</tspan></text>
</svg>""")
print("ok", CH)
