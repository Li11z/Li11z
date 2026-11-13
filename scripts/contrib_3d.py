"""Animated 3D contribution graph for the profile README.

Reads your public contribution calendar (the same one visitors see on your
profile, including private counts if you've enabled them) for the current year.
The board is drawn in perspective from a low camera angle, with the latest weeks
pointing toward the viewer. Bar heights follow daily contributions. A snake
wanders the board hunting bars, eating them from the front of the board to the
back; once the board is cleared it grows back and the loop repeats.
The snake's route is reseeded daily. No token needed.
"""
import datetime
import math
import os
import random
import re
import urllib.request
from pathlib import Path

USER = os.environ.get("GH_USER", "Li11z")
TODAY = datetime.date.today()
YEAR = TODAY.year

# ---- camera and look: tweak these to change the view
ELEVATION_DEG = 25   # camera height above the board, in degrees (90 = straight down)
YAW_DEG = -60     # board rotation; negative turns the latest weeks toward the viewer
CAMERA_DIST = 55.0   # perspective strength in cells (bigger = flatter, smaller = more dramatic)
S = 13.0             # pixels per cell at the centre of the board
HMAX = 4.0           # height of the tallest bar, in cells
GAP = 0.12           # gap between bars, in cells

TOPS = ["#E6ECF2", "#C8F0DC", "#A3E4C9", "#8DD3E8", "#7FB8F0"]  # GitHub levels 0-4
SLAB_COLOR, CARD, EDGE, INK = "#E9EFF5", "#F8FAFC", "#E3E8EF", "#7A8699"
FONT = "'Segoe UI', Helvetica, Arial, sans-serif"
STEP_MAX, LAG, REGROW, SEGMENTS, MAX_STEPS = 0.11, 0.11, 1.6, 8, 1500


def fetch_days():
    """Return [(date, count, level)] from the public contributions page."""
    url = f"https://github.com/users/{USER}/contributions?from={YEAR}-01-01&to={YEAR}-12-31"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (contrib-3d)"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")

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


# ---- data -> grid of (week, row); row 0 = front (Saturday), row 6 = back (Sunday)
days = fetch_days()
start = min(d for d, _, _ in days)
first_sunday = start - datetime.timedelta(days=(start.weekday() + 1) % 7)
grid = {}
for date, count, level in days:
    week = (date - first_sunday).days // 7
    weekday = (date.weekday() + 1) % 7
    grid[(week, 6 - weekday)] = (count, level)
NW = max(w for w, _ in grid) + 1
maxc = max((c for c, _ in grid.values()), default=0) or 1
total = sum(c for c, _ in grid.values())
print(f"Board has {total} contributions across {NW} weeks")

# ---- perspective camera
EL, YAW = math.radians(ELEVATION_DEG), math.radians(YAW_DEG)
CX, CY = NW / 2, 3.5


def ground_depth(x, y):
    """How far back a ground point is along the viewing direction (bigger = farther)."""
    return (x - CX) * math.sin(YAW) + (y - CY) * math.cos(YAW)


def cam(x, y, z):
    """World (x = weeks, y = rows, z = up) -> camera space (right, up, forward)."""
    xc, yc = x - CX, y - CY
    xr = xc * math.cos(YAW) - yc * math.sin(YAW)
    yr = xc * math.sin(YAW) + yc * math.cos(YAW)
    fwd = CAMERA_DIST + yr * math.cos(EL) - z * math.sin(EL)
    up = yr * math.sin(EL) + z * math.cos(EL)
    return xr, up, fwd


def raw(x, y, z):
    xr, up, fwd = cam(x, y, z)
    k = S * CAMERA_DIST / fwd
    return xr * k, -up * k


def dist(x, y, z):
    xr, up, fwd = cam(x, y, z)
    return math.sqrt(xr * xr + up * up + fwd * fwd)


X_LO, X_HI, Y_LO, Y_HI, SLAB = -0.4, NW + 0.4, -0.4, 7.4, 0.5
corners = [raw(x, y, z) for x in (X_LO, X_HI) for y in (Y_LO, Y_HI) for z in (-SLAB, HMAX)]
MARGIN = 20
OFF_X = MARGIN - min(p[0] for p in corners)
OFF_Y = MARGIN + 10 - min(p[1] for p in corners)
W = max(p[0] for p in corners) + OFF_X + MARGIN
H = max(p[1] for p in corners) + OFF_Y + MARGIN + 6


def P(x, y, z=0.0):
    sx, sy = raw(x, y, z)
    return sx + OFF_X, sy + OFF_Y


def fmt(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def area(poly):
    return sum(x0 * y1 - x1 * y0 for (x0, y0), (x1, y1) in zip(poly, poly[1:] + poly[:1]))


def shade(hex_color, factor):
    r, g, b = (int(hex_color[i:i + 2], 16) for i in (1, 3, 5))
    return "#{:02X}{:02X}{:02X}".format(*(max(0, min(255, round(v * factor))) for v in (r, g, b)))


def box_faces(x0, x1, y0, y1, z0, z1, visible=None):
    """Faces of a box as (polygon, tone): camera-facing sides first, then the top.
    Pass `visible` to reuse another box's side selection so animations line up."""
    sides = [((x0, y0), (x1, y0), 0.88), ((x1, y1), (x0, y1), 0.88),
             ((x1, y0), (x1, y1), 0.74), ((x0, y1), (x0, y0), 0.74)]
    quad = lambda a, b: [P(*a, z0), P(*b, z0), P(*b, z1), P(*a, z1)]
    if visible is None:   # a side faces the camera when its screen winding is clockwise
        visible = [i for i, (a, b, _) in enumerate(sides) if area(quad(a, b)) < -1e-6]
    faces = [(quad(sides[i][0], sides[i][1]), sides[i][2]) for i in visible]
    faces.append(([P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1)], 1.0))
    return faces, visible


def height(c):
    return 0.0 if c == 0 else 0.6 + (HMAX - 0.6) * math.log1p(c) / math.log1p(maxc)


# ---- snake: random-ish hunt, always eating the nearest remaining bar first
rnd = random.Random(TODAY.toordinal())
bars = {cell for cell, (c, _) in grid.items() if c > 0}
depth = lambda cell: ground_depth(cell[0] + 0.5, cell[1] + 0.5)
manhattan = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])

pos = min(((w, d) for w in range(NW) for d in range(7)), key=depth)   # nearest corner
prev, target = None, None
walk = [pos]
remaining = bars - {pos}
while remaining and len(walk) < MAX_STEPS:
    frontier = min(depth(c) for c in remaining)
    if target not in remaining or depth(target) > frontier + 1e-9:
        target = rnd.choice([c for c in remaining if depth(c) <= frontier + 1e-9])
    options = [(pos[0] + dx, pos[1] + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    # never step behind an uneaten bar, so nothing in front of the snake should hide it
    options = [o for o in options if 0 <= o[0] < NW and 0 <= o[1] < 7 and depth(o) <= frontier + 1e-9]
    choices = [o for o in options if o != prev] or options
    if not choices:
        break
    nxt = min(choices, key=lambda o: manhattan(o, target) + rnd.uniform(0, 1.6))
    prev, pos = pos, nxt
    walk.append(pos)
    remaining.discard(pos)
if len(walk) < 2:
    walk.append((max(pos[0] - 1, 0), pos[1]) if pos[0] > 0 else (1, pos[1]))

pts = [P(w + 0.5, d + 0.5) for w, d in walk]
cum = [0.0]
for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
    cum.append(cum[-1] + max(math.hypot(x1 - x0, y1 - y0), 1e-3))
step = min(STEP_MAX, 36 / len(walk))
travel = len(walk) * step
T = travel + 0.6 + REGROW + 0.8
f = travel / T
r0, r1 = (travel + 0.6) / T, (travel + 0.6 + REGROW) / T
arrive = {}
for i, cell in enumerate(walk):
    arrive.setdefault(cell, f * cum[i] / cum[-1])    # first visit = when it gets eaten
route_d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
scales = [CAMERA_DIST / cam(w + 0.5, d + 0.5, 0)[2] for w, d in walk]   # nearer = bigger

# ---- slab
parts = []
for poly, tone in box_faces(X_LO, X_HI, Y_LO, Y_HI, -SLAB, 0)[0]:
    parts.append(f'<polygon points="{fmt(poly)}" fill="{shade(SLAB_COLOR, tone)}"/>')

# ---- bars, painted far to near
for cell in sorted(grid, key=lambda c: dist(c[0] + 0.5, c[1] + 0.5, 0), reverse=True):
    w, d = cell
    c, lv = grid[cell]
    top = TOPS[min(lv, 4)]
    x0, x1, y0, y1 = w + GAP, w + 1 - GAP, d + GAP, d + 1 - GAP
    if c == 0:
        tile = box_faces(x0, x1, y0, y1, 0, 0, visible=[])[0][-1][0]
        parts.append(f'<polygon points="{fmt(tile)}" fill="{top}"/>')
        continue
    tall, vis = box_faces(x0, x1, y0, y1, 0, height(c))
    flat, _ = box_faces(x0, x1, y0, y1, 0, 0.0, visible=vis)
    for (t_poly, tone), (f_poly, _) in zip(tall, flat):
        t_, f_ = fmt(t_poly), fmt(f_poly)
        fill = shade(top, tone)
        if cell in arrive:
            e = max(0.001, arrive[cell] - 0.004)
            times = f"0;{e:.4f};{e + 0.25 / T:.4f};{r0:.4f};{r1:.4f};1"
            parts.append(
                f'<polygon points="{t_}" fill="{fill}"><animate attributeName="points" '
                f'dur="{T:.2f}s" repeatCount="indefinite" calcMode="linear" keyTimes="{times}" '
                f'values="{t_};{t_};{f_};{f_};{t_};{t_}"/></polygon>')
        else:
            parts.append(f'<polygon points="{t_}" fill="{fill}"/>')

# ---- snake spheres: follow the route, lag behind each other, grow as they come closer
snake = []
for k in range(SEGMENTS - 1, -1, -1):
    r = 5.5 - 2.4 * k / (SEGMENTS - 1)
    s = k * LAG / T
    move_times = [s + f * cv / cum[-1] for cv in cum]
    if k == 0:
        kp, kt = "0;1;1", f"0;{f:.4f};1"
        sc_times, sc_vals = move_times + [1.0], scales + [scales[-1]]
    else:
        kp, kt = "0;0;1;1", f"0;{s:.4f};{s + f:.4f};1"
        sc_times, sc_vals = [0.0] + move_times + [1.0], [scales[0]] + scales + [scales[-1]]
    fill = "url(#head)" if k == 0 else f"url(#body{k % 2})"
    snake.append(
        f'<g><animateMotion dur="{T:.2f}s" repeatCount="indefinite" calcMode="linear" '
        f'keyPoints="{kp}" keyTimes="{kt}" path="{route_d}"/>'
        f'<g><animateTransform attributeName="transform" type="scale" dur="{T:.2f}s" '
        f'repeatCount="indefinite" calcMode="linear" '
        f'keyTimes="{";".join(f"{t:.5f}" for t in sc_times)}" '
        f'values="{";".join(f"{v:.3f}" for v in sc_vals)}"/>'
        f'<circle cx="0" cy="{-r:.1f}" r="{r:.1f}" fill="{fill}"/></g></g>')
end = f + SEGMENTS * LAG / T
parts.append(f'<g opacity="0"><animate attributeName="opacity" dur="{T:.2f}s" repeatCount="indefinite" '
             f'values="0;1;1;0;0" keyTimes="0;0.01;{end:.4f};{end + 0.01:.4f};1"/>'
             + "".join(snake) + "</g>")

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
       + "".join(parts)
       + f'<text x="{MARGIN}" y="{H - MARGIN + 4:.0f}" font-family="{FONT}" font-size="11" '
         f'fill="{INK}">{total} contributions in {YEAR}</text></svg>')

Path("dist").mkdir(exist_ok=True)
Path("dist/contrib-3d.svg").write_text(svg, encoding="utf-8")
print(f"wrote dist/contrib-3d.svg (snake takes {len(walk)} steps)")