"""Generate the animated SVGs for the profile README:
assets/dejong.svg      3D De Jong attractors that assemble from a cloud, rotate and morph
assets/tech-orbit.svg  tech stack labels orbiting on tilted rings
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


if __name__ == "__main__":
    out = Path("assets")
    out.mkdir(exist_ok=True)
    (out / "dejong.svg").write_text(dejong_svg(), encoding="utf-8")
    (out / "tech-orbit.svg").write_text(tech_orbit_svg(), encoding="utf-8")
    print("wrote assets/dejong.svg and assets/tech-orbit.svg")