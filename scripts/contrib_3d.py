"""Animated 3D contribution graph for the profile README.

Reads your public contribution calendar (the same one visitors see on your
profile, including private counts if you've enabled them) for the current year.
Bar heights follow daily contributions. A snake travels the board row by row,
front to back, eating each bar as it passes; then the board grows back.
No token needed: works the same on your PC and in the GitHub Action.
"""
import datetime
import math
import os
import re
import urllib.request
from pathlib import Path

USER = os.environ.get("GH_USER", "Li11z")
YEAR = datetime.date.today().year

# layout: CW = cell spacing, FOOT = bar width, DX/DY = screen shift per row of depth
CW, FOOT, DX, DY, DFOOT, HMAX = 13.0, 10.5, 7.0, 8.0, 0.8, 46.0
OX, MARGIN = 26.0, 14.0
OY = MARGIN + HMAX + 7 * DY
TOPS = ["#E6ECF2", "#C8F0DC", "#A3E4C9", "#8DD3E8", "#7FB8F0"]  # GitHub levels 0-4
STEP, LAG, REGROW, SEGMENTS = 0.07, 0.11, 1.6, 8              # seconds / count
CARD, EDGE, INK = "#F8FAFC", "#E3E8EF", "#7A8699"
FONT = "'Segoe UI', Helvetica, Arial, sans-serif"


def fetch_days():
    """Return [(date, count, level)] from the public contributions page."""
    url = f"https://github.com/users/{USER}/contributions?from={YEAR}-01-01&to={YEAR}-12-31"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (contrib-3d)"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")

    # tooltips hold the counts: "3 contributions on May 2nd." / "No contributions on ..."
    counts_by_id = {}
    for cell_id, text in re.findall(r'<tool-tip[^>]*\bfor="([^"]+)"[^>]*>([^<]*)</tool-tip>', html):
        m = re.match(r"\s*([\d,]+)\s+contribution", text)
        counts_by_id[cell_id] = int(m.group(1).replace(",", "")) if m else 0

    days = []
    for tag in re.findall(r"<td\b[^>]*\bdata-date=[^>]*>", html):
        date = datetime.date.fromisoformat(re.search(r'data-date="([^"]+)"', tag).group(1))
        level_m = re.search(r'data-level="(\d)"', tag)
        id_m = re.search(r'\bid="([^"]+)"', tag)
        level = int(level_m.group(1)) if level_m else 0
        count = counts_by_id.get(id_m.group(1), 0) if id_m else 0
        if count == 0 and level > 0:      # tooltip missing: fall back to the colour level
            count = level
        days.append((date, count, level))
    if not days:
        raise SystemExit("Could not read the contribution calendar (page layout may have changed).")

    header = re.search(r"([\d,]+)\s+contributions?\s+in\s+" + str(YEAR), html)
    if header:
        print(f"Profile shows {header.group(1)} contributions in {YEAR}")
    return days


days = fetch_days()
start = min(d for d, _, _ in days)
first_sunday = start - datetime.timedelta(days=(start.weekday() + 1) % 7)
grid = {}  # (week, row) -> (count, level); row 0 = front (Saturday), row 6 = back (Sunday)
for date, count, level in days:
    week = (date - first_sunday).days // 7
    weekday = (date.weekday() + 1) % 7     # Sunday = 0, like GitHub
    grid[(week, 6 - weekday)] = (count, level)
NW = max(w for w, _ in grid) + 1
maxc = max((c for c, _ in grid.values()), default=0) or 1
total = sum(c for c, _ in grid.values())
print(f"Board has {total} contributions across {NW} weeks")


def P(x, d, h=0.0):
    """Project a point (x along weeks, d rows of depth, h height) onto the screen."""
    return OX + x + d * DX, OY - d * DY - h


def fmt(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def shade(hex_color, factor):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, round(v * factor))) for v in (r, g, b)))


def height(c):
    return 0.0 if c == 0 else 5 + (HMAX - 5) * math.log1p(c) / math.log1p(maxc)


def faces(w, d, h):
    x0, x1, d0, d1 = w * CW, w * CW + FOOT, d, d + DFOOT
    return {"side": [P(x1, d0), P(x1, d1), P(x1, d1, h), P(x1, d0, h)],
            "front": [P(x0, d0), P(x1, d0), P(x1, d0, h), P(x0, d0, h)],
            "top": [P(x0, d0, h), P(x1, d0, h), P(x1, d1, h), P(x0, d1, h)]}


# ---- snake route: front row left to right, next row right to left, and so on
def center(w, d):
    return P(w * CW + FOOT / 2, d + DFOOT / 2)


route = [(-2, 0)]
for d in range(7):
    cols = range(NW) if d % 2 == 0 else range(NW - 1, -1, -1)
    route += [(w, d) for w in cols]
route.append((NW + 1, 6))

pts = [center(w, d) for w, d in route]
cum = [0.0]
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    cum.append(cum[-1] + math.hypot(x1 - x0, y1 - y0))
travel = len(route) * STEP
T = travel + 0.6 + REGROW + 0.8
f = travel / T                                   # fraction of the loop spent travelling
r0, r1 = (travel + 0.6) / T, (travel + 0.6 + REGROW) / T
arrive = {cell: f * cum[i] / cum[-1] for i, cell in enumerate(route)}
route_d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)

# ---- base slab
x_lo, x_hi = -6.0, (NW - 1) * CW + FOOT + 4
slab = (f'<polygon points="{fmt([P(x_hi, -0.3), P(x_hi, 7.1), P(x_hi, 7.1, -6), P(x_hi, -0.3, -6)])}" fill="#CFD9E4"/>'
        f'<polygon points="{fmt([P(x_lo, -0.3), P(x_hi, -0.3), P(x_hi, -0.3, -6), P(x_lo, -0.3, -6)])}" fill="#DDE5EE"/>'
        f'<polygon points="{fmt([P(x_lo, -0.3), P(x_hi, -0.3), P(x_hi, 7.1), P(x_lo, 7.1)])}" fill="#EEF3F8"/>')

# ---- bars, drawn back to front, left to right
blocks = []
for d in range(6, -1, -1):
    for w in range(NW):
        if (w, d) not in grid:
            continue
        c, lv = grid[(w, d)]
        top = TOPS[min(lv, 4)]
        if c == 0:
            blocks.append(f'<polygon points="{fmt(faces(w, d, 0)["top"])}" fill="{top}"/>')
            continue
        tall, flat = faces(w, d, height(c)), faces(w, d, 0.0)
        e = max(0.001, arrive[(w, d)] - 0.004)
        times = f"0;{e:.4f};{e + 0.25 / T:.4f};{r0:.4f};{r1:.4f};1"
        for name, fill in (("side", shade(top, 0.78)), ("front", shade(top, 0.9)), ("top", top)):
            t_, f_ = fmt(tall[name]), fmt(flat[name])
            blocks.append(
                f'<polygon points="{t_}" fill="{fill}"><animate attributeName="points" '
                f'dur="{T:.2f}s" repeatCount="indefinite" calcMode="linear" keyTimes="{times}" '
                f'values="{t_};{t_};{f_};{f_};{t_};{t_}"/></polygon>')

# ---- snake: spheres following the route, each segment a little behind the one before
snake = []
for k in range(SEGMENTS - 1, -1, -1):
    r = 5.5 - 2.4 * k / (SEGMENTS - 1)
    s = k * LAG / T
    kp, kt = ("0;1;1", f"0;{f:.4f};1") if k == 0 else ("0;0;1;1", f"0;{s:.4f};{s + f:.4f};1")
    fill = "url(#head)" if k == 0 else f"url(#body{k % 2})"
    snake.append(f'<circle cx="0" cy="{-r:.1f}" r="{r:.1f}" fill="{fill}">'
                 f'<animateMotion dur="{T:.2f}s" repeatCount="indefinite" calcMode="linear" '
                 f'keyPoints="{kp}" keyTimes="{kt}" path="{route_d}"/></circle>')
end = f + SEGMENTS * LAG / T
snake_group = (f'<g opacity="0"><animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" '
               f'values="0;1;1;0;0" keyTimes="0;0.01;{end:.4f};{end + 0.01:.4f};1"/>'
               + "".join(snake) + "</g>")

W = OX + x_hi + 7.1 * DX + 20
H = OY + 30
defs = """<defs>
  <radialGradient id="head" cx="35%" cy="30%" r="70%"><stop offset="0%" stop-color="#FFFFFF"/>
    <stop offset="45%" stop-color="#FFB3C6"/><stop offset="100%" stop-color="#FF7A9C"/></radialGradient>
  <radialGradient id="body0" cx="35%" cy="30%" r="70%"><stop offset="0%" stop-color="#FFFFFF"/>
    <stop offset="50%" stop-color="#FFD6E0"/><stop offset="100%" stop-color="#FF9EB8"/></radialGradient>
  <radialGradient id="body1" cx="35%" cy="30%" r="70%"><stop offset="0%" stop-color="#FFFFFF"/>
    <stop offset="50%" stop-color="#FFE3EA"/><stop offset="100%" stop-color="#FFB3C6"/></radialGradient>
</defs>"""

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W:.0f} {H:.0f}" '
       f'width="{W:.0f}" height="{H:.0f}">{defs}'
       f'<rect x="1" y="1" width="{W - 2:.0f}" height="{H - 2:.0f}" rx="14" fill="{CARD}" '
       f'stroke="{EDGE}" stroke-width="2"/>'
       + slab + "".join(blocks) + snake_group
       + f'<text x="{OX}" y="{H - 9:.0f}" font-family="{FONT}" font-size="11" fill="{INK}">'
         f'{total} contributions in {YEAR}</text></svg>')

Path("dist").mkdir(exist_ok=True)
Path("dist/contrib-3d.svg").write_text(svg, encoding="utf-8")
print("wrote dist/contrib-3d.svg")