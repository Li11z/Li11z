"""Generate the animated SVGs for the profile README:
assets/dejong.svg      3D De Jong attractors that assemble from a cloud, rotate and morph
assets/tech-orbit.svg  tech stack labels orbiting on tilted rings
assets/interests.svg   six animated research-interest cards
"""
from pathlib import Path

import math
import numpy as np

PASTELS = ["#5CC9A7", "#5BB5E0", "#FF9F7A", "#FF85A8"]   # mint, sky, peach, pink
CARD, EDGE = "#F8FAFC", "#E3E8EF"
FONT = "'Segoe UI', Helvetica, Arial, sans-serif"

# ---------------------------------------------------------------- De Jong attractors
# x' = sin(a y) - cos(b x),  y' = sin(c x) - cos(d y)
DEJONG = {
    "A": (-2.0, -2.0, -1.2, 2.0),
    "B": (-2.24, 0.43, -0.65, -2.43),
    "C": (1.641, 1.902, 0.316, 1.525),
}
N_POINTS, SIZE, CYCLE = 1400, 420, 30  # points, pixels, seconds per loop


def dejong_points(params, starts, burn=60):
    """Iterate many starting points onto the attractor. Depth z is the previous x
    (a delay embedding), so the front view is the classic 2D De Jong picture."""
    a, b, c, d = params
    x, y = starts[:, 0].copy(), starts[:, 1].copy()
    prev = x
    for _ in range(burn):
        prev = x
        x, y = np.sin(a * y) - np.cos(b * x), np.sin(c * x) - np.cos(d * y)
    return np.stack([x, y, 0.6 * prev], axis=1)


def project(p, yaw_deg, pitch=0.28, scale=70.0):
    yaw = math.radians(yaw_deg)
    x, y, z = p[:, 0], p[:, 1], p[:, 2]
    X = x * math.cos(yaw) - z * math.sin(yaw)
    Z = x * math.sin(yaw) + z * math.cos(yaw)
    Y = y * math.cos(pitch) - Z * math.sin(pitch)
    D = y * math.sin(pitch) + Z * math.cos(pitch)
    k = scale / (1 + 0.05 * D)                      # gentle perspective
    return np.stack([SIZE / 2 + X * k, SIZE / 2 - Y * k], axis=1)


def dots(xy):
    return "".join(f"M{x:.1f} {y:.1f}h.1" for x, y in xy)


def dejong_svg():
    rng = np.random.default_rng(3)
    starts = rng.uniform(-2, 2, size=(N_POINTS, 2))
    cloud = np.column_stack([rng.uniform(-1.8, 1.8, N_POINTS),
                             rng.uniform(-1.8, 1.8, N_POINTS),
                             rng.uniform(-1.1, 1.1, N_POINTS)])
    shapes = {k: dejong_points(v, starts) for k, v in DEJONG.items()}

    # cloud -> A (rotate) -> B (rotate back) -> C (rotate) -> cloud
    frames = [(cloud, 0)]
    frames += [(shapes["A"], yw) for yw in (-35, 0, 35)]
    frames += [(shapes["B"], yw) for yw in (35, 0, -35)]
    frames += [(shapes["C"], yw) for yw in (-35, 0, 35)]
    frames.append((cloud, 0))
    projected = [project(p, yw) for p, yw in frames]

    # morphs ease in and out, rotations run at constant speed
    ease, linear = "0.45 0 0.55 1", "0 0 1 1"
    splines = ";".join([ease, linear, linear, ease, linear, linear, ease, linear, linear, ease])
    times = ";".join(f"{i / (len(frames) - 1):.4f}" for i in range(len(frames)))

    paths = []
    for g, color in enumerate(PASTELS):
        idx = np.arange(g, N_POINTS, len(PASTELS))
        values = ";".join(dots(pr[idx]) for pr in projected)
        paths.append(
            f'<path d="{dots(projected[0][idx])}" fill="none" stroke="{color}" stroke-width="2.4" '
            f'stroke-linecap="round" stroke-opacity="0.9">'
            f'<animate attributeName="d" dur="{CYCLE}s" repeatCount="indefinite" calcMode="spline" '
            f'keyTimes="{times}" keySplines="{splines}" values="{values}"/></path>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {SIZE} {SIZE}" '
            f'width="{SIZE}" height="{SIZE}">'
            f'<rect x="1" y="1" width="{SIZE - 2}" height="{SIZE - 2}" rx="18" fill="{CARD}" '
            f'stroke="{EDGE}" stroke-width="2"/>'
            + "".join(paths) + "</svg>")


# ---------------------------------------------------------------- tech orbit
RINGS = [  # rx, ry, seconds per turn, clockwise?, pill fill, ink, ring stroke, labels
    (110, 34, 26, True, "#D8F3E8", "#2F6B57", "#A8E6CF",
     ["Python", "C", "C++", "Java", "R", "SQL", "JavaScript"]),
    (190, 58, 38, False, "#DCEEFB", "#2C5F86", "#A9D4F5",
     ["PyTorch", "Hugging Face", "scikit-learn", "LightGBM", "XGBoost", "SHAP", "YOLOv8"]),
    (270, 82, 52, True, "#FFE5D6", "#8A4B2A", "#FFCBB0",
     ["NumPy", "pandas", "PostgreSQL", "FastAPI", "Next.js", "Azure", "Git", "Power BI"]),
]


def tech_orbit_svg():
    W, H = 660, 250
    cx, cy = W / 2, H / 2
    parts = [f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="18" fill="{CARD}" '
             f'stroke="{EDGE}" stroke-width="2"/>']
    for rx, ry, _, _, _, _, stroke, _ in RINGS:
        parts.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="none" '
                     f'stroke="{stroke}" stroke-width="1.5" stroke-dasharray="4 6"/>')
    parts.append(f'<circle cx="{cx}" cy="{cy}" r="24" fill="#FFC8DD" stroke="#FFAFCC" stroke-width="2"/>'
                 f'<text x="{cx}" y="{cy + 5}" text-anchor="middle" font-family="{FONT}" '
                 f'font-size="15" font-weight="600" fill="#2B2D42">Ali</text>')

    for rx, ry, secs, clockwise, fill, ink, stroke, items in RINGS:
        sweep = 1 if clockwise else 0
        # start at the front of the ellipse, go round through the back and return
        path = (f"M{cx},{cy + ry} A{rx},{ry} 0 1 {sweep} {cx},{cy - ry} "
                f"A{rx},{ry} 0 1 {sweep} {cx},{cy + ry}")
        for k, name in enumerate(items):
            begin = f"-{secs * k / len(items):.2f}s"
            timing = f'dur="{secs}s" begin="{begin}" repeatCount="indefinite"'
            w = 7 * len(name) + 20
            parts.append(
                f'<g><animateMotion {timing} path="{path}"/>'
                # smaller and fainter at the back, which reads as depth
                f'<animate attributeName="opacity" values="1;0.4;1" keyTimes="0;0.5;1" {timing}/>'
                f'<g><animateTransform attributeName="transform" type="scale" values="1;0.72;1" '
                f'keyTimes="0;0.5;1" {timing}/>'
                f'<rect x="{-w / 2:.1f}" y="-11" width="{w:.1f}" height="22" rx="11" fill="{fill}" '
                f'stroke="{stroke}" stroke-width="1.2"/>'
                f'<text y="4" text-anchor="middle" font-family="{FONT}" font-size="12" '
                f'fill="{ink}">{name}</text></g></g>')

    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            + "".join(parts) + "</svg>")


# ---------------------------------------------------------------- interest cards
CARD_W, CARD_H, CARD_GAP = 410, 270, 20
INK_DARK, INK_MID, INK_SOFT, GRID = "#2B2D42", "#4A5568", "#7A8699", "#A0AEC0"
EASE = "0.4 0 0.6 1"


def _poly(xs, ys):
    return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in zip(xs, ys))


def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def _caption(x, y, text):
    return f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="10.5" fill="{INK_SOFT}">{text}</text>'


def _card(x, y, tint, edge, title, keywords, link, body):
    return (f'<g transform="translate({x} {y})">'
            f'<rect x="1" y="1" width="{CARD_W - 2}" height="{CARD_H - 2}" rx="16" fill="{tint}" '
            f'stroke="{edge}" stroke-width="2"/>'
            f'<text x="22" y="36" font-family="{FONT}" font-size="17" font-weight="600" '
            f'fill="{INK_DARK}">{title}</text>'
            f'{body}'
            f'<text x="22" y="{CARD_H - 40}" font-family="{FONT}" font-size="12.5" '
            f'fill="{INK_MID}">{keywords}</text>'
            f'<text x="22" y="{CARD_H - 20}" font-family="{FONT}" font-size="12" '
            f'fill="{INK_SOFT}">{link}</text></g>')


def _card_sciml():
    """A guess converging onto the true solution while the loss shrinks."""
    xs = np.linspace(0, 1, 80)
    true = np.exp(-1.5 * xs) * np.sin(3 * np.pi * xs)
    guess = 0.45 * np.sin(7 * xs + 1) + 0.3 * np.sin(13 * xs + 2) + 0.2 * np.cos(19 * xs)
    px = 30 + 350 * xs
    to_y = lambda u: 125 - 55 * u
    stages = [_poly(px, to_y((1 - a) * guess + a * true)) for a in (0, 0.3, 0.6, 0.85, 1.0)]
    values = ";".join(stages + [stages[-1], stages[0]])
    times = "0;0.15;0.3;0.45;0.6;0.88;1"
    splines = ";".join([EASE] * 6)
    data = "".join(f'<circle cx="{px[i]:.1f}" cy="{to_y(true[i]):.1f}" r="3.5" fill="#2F6B57"/>'
                   for i in (6, 18, 31, 45, 58, 72))
    colloc = "".join(
        f'<circle class="blink" cx="{30 + 350 * t:.1f}" cy="196" r="2.5" fill="none" stroke="#5CC9A7" '
        f'stroke-width="1.2" style="animation-delay:{0.15 * k:.2f}s"/>'
        for k, t in enumerate(np.linspace(0.03, 0.97, 14)))
    return (f'<line x1="30" y1="196" x2="380" y2="196" stroke="#CFE9DE"/>'
            f'<path d="{_poly(px, to_y(true))}" fill="none" stroke="{GRID}" stroke-width="1.6" '
            f'stroke-dasharray="5 5"/>'
            f'<path d="{stages[0]}" fill="none" stroke="#5CC9A7" stroke-width="2.8" stroke-linecap="round">'
            f'<animate attributeName="d" dur="9s" repeatCount="indefinite" calcMode="spline" '
            f'keyTimes="{times}" keySplines="{splines}" values="{values}"/></path>'
            + data + colloc +
            f'<text x="300" y="36" font-family="{FONT}" font-size="11" fill="{INK_SOFT}">loss</text>'
            f'<rect x="328" y="28" width="52" height="8" rx="4" fill="#5CC9A7">'
            f'<animate attributeName="width" dur="9s" repeatCount="indefinite" calcMode="spline" '
            f'keyTimes="{times}" keySplines="{splines}" values="52;32;18;9;4;4;52"/></rect>')


def _card_sir():
    """S, I and R curves from an SIR simulation drawing themselves."""
    S, I, R, beta, gamma, dt = 0.99, 0.01, 0.0, 0.32, 0.1, 0.5
    traj = []
    for _ in range(320):
        traj.append((S, I, R))
        new_inf, new_rec = beta * S * I * dt, gamma * I * dt
        S, I, R = S - new_inf, I + new_inf - new_rec, R + new_rec
    traj = np.array(traj)
    px = np.linspace(30, 360, len(traj))
    to_y = lambda v: 192 - 135 * v
    out = ['<line x1="30" y1="192" x2="372" y2="192" stroke="#F5C9D6"/>']
    colors = {"S": "#5BB5E0", "I": "#FF85A8", "R": "#5CC9A7"}
    for k, name in enumerate("SIR"):
        ys = to_y(traj[:, k])
        out.append(f'<path class="draw" pathLength="1" d="{_poly(px, ys)}" fill="none" '
                   f'stroke="{colors[name]}" stroke-width="2.6" stroke-linecap="round"/>')
        if name == "I":   # label the infection curve at its peak
            p = int(np.argmax(traj[:, 1]))
            lx, ly, anchor = px[p], ys[p] - 9, "middle"
        else:
            lx, ly, anchor = 366, ys[-1] + 4, "start"
        out.append(f'<text class="late" x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" '
                   f'font-family="{FONT}" font-size="12" font-weight="600" fill="{colors[name]}">{name}</text>')
    return "".join(out)


def _card_attribution():
    """A pixel image with an attribution heatmap and feature-importance bars."""
    cols, rows, cell, gx, gy = 14, 10, 10, 30, 72
    out = [_caption(gx, 64, "input"), _caption(215, 64, "attribution")]
    heat = []
    for r in range(rows):
        for c in range(cols):
            v = math.exp(-((c - 8.5) ** 2 + (r - 4.5) ** 2) / 8) + 0.5 * math.exp(-((c - 3) ** 2 + (r - 7) ** 2) / 4)
            out.append(f'<rect x="{gx + c * cell}" y="{gy + r * cell}" width="{cell - 1}" height="{cell - 1}" '
                       f'rx="2" fill="{_mix("#EEF2F6", "#8896A8", min(v, 1))}"/>')
            a = math.exp(-((c - 9) ** 2 + (r - 4) ** 2) / 5)
            if a > 0.08:
                heat.append((a, c, r))
    heat.sort(reverse=True)   # most important pixels light up first
    for rank, (a, c, r) in enumerate(heat):
        out.append(f'<rect class="heat" x="{gx + c * cell}" y="{gy + r * cell}" width="{cell - 1}" '
                   f'height="{cell - 1}" rx="2" fill="#FF6F91" fill-opacity="{min(a, 0.85):.2f}" '
                   f'style="animation-delay:{0.035 * rank:.2f}s"/>')
    feats = [("edge", 1.0), ("texture", 0.72), ("shape", 0.5), ("colour", 0.3), ("background", 0.12)]
    shades = ["#FF85A8", "#FF9F7A", "#FFB38A", "#FFC8A8", "#FFD9C4"]
    for i, (name, v) in enumerate(feats):
        y, w, s = 76 + i * 21, 92 * v, 0.05 + 0.05 * i
        out.append(f'<text x="215" y="{y + 9}" font-family="{FONT}" font-size="11" fill="{INK_MID}">{name}</text>'
                   f'<rect x="285" y="{y}" width="0" height="11" rx="5.5" fill="{shades[i]}">'
                   f'<animate attributeName="width" dur="8s" repeatCount="indefinite" '
                   f'keyTimes="0;{s:.2f};{s + 0.2:.2f};0.85;1" values="0;0;{w:.1f};{w:.1f};0"/></rect>')
    return "".join(out)


def _card_behavior():
    """A pose skeleton that waves, with action probabilities updating as it moves."""
    idle = {"neck": (105, 88), "ls": (91, 94), "rs": (119, 94), "le": (85, 118), "re": (125, 118),
            "lw": (83, 141), "rw": (127, 141), "lh": (97, 143), "rh": (113, 143),
            "lk": (95, 170), "rk": (115, 170), "la": (93, 197), "ra": (117, 197)}

    def pose(**changes):
        p = dict(idle)
        p.update(changes)
        return p

    up = pose(re=(138, 82), rw=(146, 60))
    left = pose(re=(138, 82), rw=(134, 59))
    right = pose(re=(138, 82), rw=(157, 65))
    frames = [idle, idle, up, left, right, left, right, up, idle, idle]
    times = "0;0.12;0.25;0.35;0.45;0.55;0.65;0.72;0.85;1"
    timing = (f'dur="8s" repeatCount="indefinite" calcMode="spline" keyTimes="{times}" '
              f'keySplines="{";".join([EASE] * (len(frames) - 1))}"')
    seq = lambda joint, axis: ";".join(str(f[joint][axis]) for f in frames)
    bones = [("neck", "ls"), ("neck", "rs"), ("ls", "le"), ("le", "lw"), ("rs", "re"), ("re", "rw"),
             ("neck", "lh"), ("neck", "rh"), ("lh", "rh"), ("lh", "lk"), ("lk", "la"),
             ("rh", "rk"), ("rk", "ra")]
    out = ['<rect x="60" y="54" width="108" height="152" rx="6" fill="none" stroke="#9BC4E2" '
           'stroke-dasharray="4 4"/>',
           f'<text x="65" y="67" font-family="{FONT}" font-size="10" fill="{INK_SOFT}">person</text>',
           '<circle cx="105" cy="76" r="9" fill="#FFFFFF" stroke="#5BB5E0" stroke-width="2"/>']
    for a, b in bones:
        out.append(f'<line x1="{idle[a][0]}" y1="{idle[a][1]}" x2="{idle[b][0]}" y2="{idle[b][1]}" '
                   f'stroke="#9BC4E2" stroke-width="2.4" stroke-linecap="round">'
                   f'<animate attributeName="x1" values="{seq(a, 0)}" {timing}/>'
                   f'<animate attributeName="y1" values="{seq(a, 1)}" {timing}/>'
                   f'<animate attributeName="x2" values="{seq(b, 0)}" {timing}/>'
                   f'<animate attributeName="y2" values="{seq(b, 1)}" {timing}/></line>')
    for joint, (jx, jy) in idle.items():
        out.append(f'<circle cx="{jx}" cy="{jy}" r="3.2" fill="#5BB5E0">'
                   f'<animate attributeName="cx" values="{seq(joint, 0)}" {timing}/>'
                   f'<animate attributeName="cy" values="{seq(joint, 1)}" {timing}/></circle>')
    probs = {
        "waving":   [0.08, 0.08, 0.55, 0.85, 0.90, 0.92, 0.93, 0.70, 0.15, 0.08],
        "standing": [0.82, 0.82, 0.38, 0.11, 0.07, 0.06, 0.05, 0.24, 0.75, 0.82],
        "walking":  [0.06, 0.06, 0.04, 0.02, 0.02, 0.01, 0.01, 0.04, 0.06, 0.06],
        "sitting":  [0.04, 0.04, 0.03, 0.02, 0.01, 0.01, 0.01, 0.02, 0.04, 0.04],
    }
    shades = ["#5BB5E0", "#8ECDF0", "#B5DDF5", "#D3EAF8"]
    out.append(_caption(205, 70, "predicted action"))
    for i, (name, ps) in enumerate(probs.items()):
        y = 84 + i * 24
        widths = ";".join(f"{110 * p:.1f}" for p in ps)
        out.append(f'<text x="205" y="{y + 9}" font-family="{FONT}" font-size="11" fill="{INK_MID}">{name}</text>'
                   f'<rect x="262" y="{y}" width="{110 * ps[0]:.1f}" height="11" rx="5.5" fill="{shades[i]}">'
                   f'<animate attributeName="width" values="{widths}" {timing}/></rect>')
    return "".join(out)


def _card_decisions():
    """A finite-state machine cycling through its states, next to a GOAP planner
    that builds a plan backward from its goal and then carries it out."""
    timing = 'dur="8s" repeatCount="indefinite"'
    out = ['<defs><marker id="fsmArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
           'markerHeight="6" orient="auto"><path d="M0 0 L10 5 L0 10 Z" fill="#7FBFC4"/></marker></defs>',
           _caption(30, 62, "finite-state machine"), _caption(228, 62, "GOAP plan")]

    # ---- finite-state machine: idle -> patrol -> chase -> search -> idle
    states = [("idle", 70, 92), ("patrol", 175, 92), ("chase", 175, 168), ("search", 70, 168)]
    edges = [((108, 92), (137, 92)), ((175, 108), (175, 152)),
             ((137, 168), (108, 168)), ((70, 152), (70, 108))]
    for (x1, y1), (x2, y2) in edges:
        out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#7FBFC4" stroke-width="1.6" '
                   f'marker-end="url(#fsmArrow)"/>')
    loop = "M70 92 L175 92 L175 168 L70 168 L70 92"
    out.append(f'<circle cx="0" cy="0" r="4.5" fill="#FF85A8"><animateMotion {timing} calcMode="linear" '
               f'keyPoints="0;0;0.290;0.290;0.5;0.5;0.790;0.790;1" '
               f'keyTimes="0;0.175;0.25;0.425;0.5;0.675;0.75;0.925;1" path="{loop}"/></circle>')
    for k, (name, cx, cy) in enumerate(states):
        if k == 0:
            vals, kt = "1;1;0;0;1", "0;0.175;0.2;0.925;1"
        else:
            a = 0.25 * k
            vals, kt = "0;0;1;1;0;0", f"0;{a - 0.025:.3f};{a:.3f};{a + 0.175:.3f};{a + 0.2:.3f};1"
        out.append(f'<rect x="{cx - 35}" y="{cy - 13}" width="70" height="26" rx="13" fill="#FFFFFF" '
                   f'stroke="#9ED9DC" stroke-width="1.5"/>'
                   f'<rect x="{cx - 35}" y="{cy - 13}" width="70" height="26" rx="13" fill="#7FD3D8" opacity="0">'
                   f'<animate attributeName="opacity" values="{vals}" keyTimes="{kt}" {timing}/></rect>'
                   f'<text x="{cx}" y="{cy + 4}" text-anchor="middle" font-family="{FONT}" font-size="11.5" '
                   f'fill="{INK_DARK}">{name}</text>')

    # ---- GOAP: plan built backward from the goal, then executed forward
    steps = [("get axe", 2, 74), ("chop wood", 4, 104), ("light fire", 1, 134)]
    appear = {"light fire": 0.18, "chop wood": 0.30, "get axe": 0.42}
    execute = {"get axe": 0.55, "chop wood": 0.65, "light fire": 0.75}
    fade = lambda a: f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{a:.2f};{a + 0.04:.2f};0.94;1" {timing}/>'
    check = lambda x, y: f'<path d="M{x - 4} {y} L{x - 1} {y + 3} L{x + 4} {y - 3}" fill="none" stroke="#2F6B57" stroke-width="1.8" stroke-linecap="round"/>'
    for name, cost, y in steps:
        a, e = appear[name], execute[name]
        out.append(f'<g opacity="0">{fade(a)}'
                   f'<rect x="228" y="{y}" width="152" height="22" rx="6" fill="#FFFFFF" stroke="#9ED9DC" stroke-width="1.5"/>'
                   f'<g opacity="0">{fade(e)}<rect x="228" y="{y}" width="152" height="22" rx="6" fill="#BFEBD9"/>'
                   f'{check(366, y + 11)}</g>'
                   f'<text x="238" y="{y + 15}" font-family="{FONT}" font-size="11.5" fill="{INK_DARK}">{name}</text>'
                   f'<text x="345" y="{y + 15}" text-anchor="end" font-family="{FONT}" font-size="10" '
                   f'fill="{INK_SOFT}">cost {cost}</text>'
                   f'<line x1="304" y1="{y + 23}" x2="304" y2="{y + 29}" stroke="#7FBFC4" stroke-width="1.6" '
                   f'marker-end="url(#fsmArrow)"/></g>')
    out.append(f'<g opacity="0">{fade(0.05)}'
               f'<rect x="228" y="166" width="152" height="24" rx="12" fill="#FFE5D6" stroke="#FFCBB0" stroke-width="1.5"/>'
               f'<g opacity="0">{fade(0.85)}<rect x="228" y="166" width="152" height="24" rx="12" fill="#FFB38A"/></g>'
               f'<text x="304" y="182" text-anchor="middle" font-family="{FONT}" font-size="11.5" font-weight="600" '
               f'fill="{INK_DARK}">goal: stay warm</text></g>')
    return "".join(out)


def _cube(cx, cy, size, n=40):
    """A flat-shaded cube spinning under a fixed light (Lambert shading, back-face culling)."""
    tilt_x, tilt_z = math.radians(25), math.radians(12)
    light = np.array([-0.45, 0.7, 0.55])
    light /= np.linalg.norm(light)

    def rot(v, th):
        x, y, z = v
        x, z = x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th)        # spin
        y, z = y * math.cos(tilt_x) - z * math.sin(tilt_x), y * math.sin(tilt_x) + z * math.cos(tilt_x)  # tilt
        x, y = x * math.cos(tilt_z) - y * math.sin(tilt_z), x * math.sin(tilt_z) + y * math.cos(tilt_z)  # roll
        return np.array([x, y, z])

    hues = {0: ("#C9673F", "#FFDCC9"), 1: ("#2F9474", "#D2F2E6"), 2: ("#2F7FB3", "#D6ECFA")}
    thetas = [2 * math.pi * i / n for i in range(n + 1)]
    timing = 'dur="8s" repeatCount="indefinite" calcMode="linear"'
    out = [f'<ellipse cx="{cx}" cy="{cy + size * 1.75:.1f}" rx="{size * 1.2:.1f}" ry="6" fill="#DCEBD0" opacity="0.8"/>']
    for axis in range(3):
        for sign in (-1, 1):
            b, c = [i for i in range(3) if i != axis]
            corners = []
            for u, v in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                p = [0, 0, 0]
                p[axis], p[b], p[c] = sign, u, v
                corners.append(p)
            normal = [0, 0, 0]
            normal[axis] = sign
            dark, lit = hues[axis]
            frames, fills, ops = [], [], []
            for th in thetas:
                rc = [rot(p, th) for p in corners]
                rn = rot(normal, th)
                frames.append(" ".join(f"{cx + size * q[0]:.1f},{cy - size * q[1]:.1f}" for q in rc))
                fills.append(_mix(dark, lit, 0.25 + 0.75 * max(0.0, float(rn @ light))))
                ops.append("1" if rn[2] > 0 else "0")       # hide faces turned away from the viewer
            out.append(f'<polygon points="{frames[0]}" fill="{fills[0]}" opacity="{ops[0]}" stroke="#FFFFFF" '
                       f'stroke-width="1.2" stroke-linejoin="round">'
                       f'<animate attributeName="points" values="{";".join(frames)}" {timing}/>'
                       f'<animate attributeName="fill" values="{";".join(fills)}" {timing}/>'
                       f'<animate attributeName="opacity" values="{";".join(ops)}" {timing}/></polygon>')
    return "".join(out)


def _platformer():
    """Platforms drop into place, then a character hops across them collecting gems."""
    plats = [(178, 182, 48), (232, 158, 44), (288, 134, 44), (342, 160, 44)]
    slot, jump, start = 0.18, 0.13, 0.22
    timing = 'dur="9s" repeatCount="indefinite"'
    out = ['<line x1="176" y1="200" x2="388" y2="200" stroke="#CFE6BF" stroke-width="2"/>']
    for i, (x, y, w) in enumerate(plats):              # level "built" one platform at a time
        d = 0.02 + 0.035 * i
        kt = f"0;{d:.3f};{d + 0.05:.3f};0.9;1"
        out.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="{kt}" {timing}/>'
                   f'<animateTransform attributeName="transform" type="translate" '
                   f'values="0 -24;0 -24;0 0;0 0;0 0" keyTimes="{kt}" {timing}/>'
                   f'<rect x="{x}" y="{y}" width="{w}" height="10" rx="5" fill="#B9E8C8" '
                   f'stroke="#8FD3A6" stroke-width="1.5"/></g>')

    feet = [(x + w / 2, y) for x, y, w in plats]
    pts, bounds, apexes = [feet[0]], [0], []
    for (x0, y0), (x1, y1) in zip(feet, feet[1:]):     # parabolic jumps between platforms
        hgt = 28 + abs(y1 - y0) / 2
        for k in range(1, 17):
            t = k / 16
            pts.append((x0 + (x1 - x0) * t, y0 + (y1 - y0) * t - 4 * hgt * t * (1 - t)))
        apexes.append(pts[bounds[-1] + 8])
        bounds.append(len(pts) - 1)
    cum = [0.0]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        cum.append(cum[-1] + math.hypot(bx - ax, by - ay))
    frac = [cum[b] / cum[-1] for b in bounds]

    kp, kt = ["0", "0"], ["0", f"{start:.3f}"]
    squash = [("0", "1 1"), (f"{start - 0.01:.3f}", "1 1")]
    for k in range(len(plats) - 1):
        t0 = start + slot * k
        kt += [f"{t0 + jump:.3f}", f"{t0 + slot:.3f}"]
        kp += [f"{frac[k + 1]:.4f}", f"{frac[k + 1]:.4f}"]
        squash += [(f"{t0:.3f}", "0.85 1.2"), (f"{t0 + jump / 2:.3f}", "1 1"),
                   (f"{t0 + jump:.3f}", "1.3 0.7"), (f"{t0 + jump + 0.03:.3f}", "1 1")]
        gx_, gy_ = apexes[k]
        m = t0 + jump / 2                               # gem pops when the character reaches it
        out.append(f'<g transform="translate({gx_:.1f} {gy_ - 10:.1f})"><g opacity="0">'
                   f'<animate attributeName="opacity" values="0;0;1;1;0;0" '
                   f'keyTimes="0;0.17;0.2;{m:.3f};{m + 0.02:.3f};1" {timing}/>'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" '
                   f'dur="1.6s" repeatCount="indefinite"/>'
                   f'<path d="M0 -6 L5 0 L0 6 L-5 0 Z" fill="#7EC8E3"/></g></g>')
    kp.append("1")
    kt.append("1")
    squash.append(("1", "1 1"))
    route = _poly(*zip(*pts))
    out.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" '
               f'keyTimes="0;0.19;0.21;0.9;1" {timing}/>'
               f'<animateMotion {timing} calcMode="linear" keyPoints="{";".join(kp)}" '
               f'keyTimes="{";".join(kt)}" path="{route}"/>'
               f'<g><animateTransform attributeName="transform" type="scale" {timing} calcMode="linear" '
               f'keyTimes="{";".join(t for t, _ in squash)}" values="{";".join(v for _, v in squash)}"/>'
               f'<rect x="-7" y="-14" width="14" height="14" rx="4" fill="#FF85A8"/>'
               f'<circle cx="-2.5" cy="-9" r="1.5" fill="#FFFFFF"/>'
               f'<circle cx="2.5" cy="-9" r="1.5" fill="#FFFFFF"/></g></g>')
    return "".join(out)


def _card_graphics():
    """A shaded rotating cube (rendering) beside a self-building platformer level (game design)."""
    return (_caption(34, 62, "rendering") + _caption(178, 62, "level and game feel")
            + _cube(95, 130, 33) + _platformer())


def interests_svg():
    W, H = 2 * CARD_W + CARD_GAP, 3 * CARD_H + 2 * CARD_GAP
    style = """<style>
  .draw { stroke-dasharray: 1; stroke-dashoffset: 1; animation: draw 9s ease-in-out infinite; }
  .late { opacity: 0; animation: late 9s ease-in-out infinite; }
  .heat { animation: heat 8s ease-in-out infinite both; }
  .blink { animation: blink 2.4s ease-in-out infinite; }
  @keyframes draw { 0% { stroke-dashoffset: 1; opacity: 1; } 60% { stroke-dashoffset: 0; opacity: 1; }
                    90% { stroke-dashoffset: 0; opacity: 1; } 100% { stroke-dashoffset: 0; opacity: 0; } }
  @keyframes late { 0%, 55% { opacity: 0; } 65%, 88% { opacity: 1; } 100% { opacity: 0; } }
  @keyframes heat { 0% { opacity: 0; } 20%, 80% { opacity: 1; } 92%, 100% { opacity: 0; } }
  @keyframes blink { 0%, 100% { opacity: 0.25; } 50% { opacity: 1; } }
  @media (prefers-reduced-motion: reduce) {
    * { animation: none !important; }
    .draw { stroke-dashoffset: 0; } .late, .heat { opacity: 1; }
  }
</style>"""
    col2 = CARD_W + CARD_GAP
    row = lambda i: i * (CARD_H + CARD_GAP)
    cards = [
        _card(0, row(0), "#EFFAF5", "#CFEBDD", "Scientific machine learning",
              "PINNs · neural operators · neural ODEs · SINDy",
              "Studying: Julia SciML, Diffrax, PySINDy, PySR", _card_sciml()),
        _card(col2, row(0), "#FFF1F5", "#F8D3DE", "ML and DL for health and biology",
              "epidemic models · medical imaging · biosignals",
              "Shows up in: epidemic waves PDE model, mathematical biology", _card_sir()),
        _card(0, row(1), "#FFF5EE", "#F8DCCB", "Interpretability",
              "attribution maps · SHAP · interpretable models",
              "Shows up in: SHAP analysis in the Toronto safety project", _card_attribution()),
        _card(col2, row(1), "#EFF7FD", "#CFE4F5", "Artificial behavior intelligence",
              "pose estimation · action recognition · intent prediction",
              "Shows up in: pose estimation in jersey number recognition", _card_behavior()),
        _card(0, row(2), "#ECFAFA", "#C7EDEE", "Game AI and decision-making",
              "behavioral AI · GOAP · finite-state machines",
              "Exploring: decision-making systems for game characters", _card_decisions()),
        _card(col2, row(2), "#F3FAEC", "#D6ECC4", "Game design and computer graphics",
              "rendering · shading · level design · game feel",
              "Exploring: real-time rendering and small game prototypes", _card_graphics()),
    ]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">'
            + style + "".join(cards) + "</svg>")


if __name__ == "__main__":
    out = Path("assets")
    out.mkdir(exist_ok=True)
    (out / "dejong.svg").write_text(dejong_svg(), encoding="utf-8")
    (out / "tech-orbit.svg").write_text(tech_orbit_svg(), encoding="utf-8")
    (out / "interests.svg").write_text(interests_svg(), encoding="utf-8")
    print("wrote assets/dejong.svg, assets/tech-orbit.svg and assets/interests.svg")