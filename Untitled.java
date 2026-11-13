"""Generate an animated, self-drawing Lorenz attractor SVG for the profile README."""
from pathlib import Path
import numpy as np


def lorenz(s, sigma=10.0, rho=28.0, beta=8 / 3):
    x, y, z = s
    return np.array([sigma * (y - x), x * (rho - z) - y, x * y - beta * z])


def rk4(f, s, dt, n):
    out = np.empty((n, 3))
    for i in range(n):
        k1 = f(s)
        k2 = f(s + dt / 2 * k1)
        k3 = f(s + dt / 2 * k2)
        k4 = f(s + dt * k3)
        s = s + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        out[i] = s
    return out


traj = rk4(lorenz, np.array([1.0, 1.0, 1.0]), 0.01, 6000)[500::2]  # drop transient, thin points
x, z = traj[:, 0], traj[:, 2]

W = H = 400
PAD = 20
scale = min((W - 2 * PAD) / np.ptp(x), (H - 2 * PAD) / np.ptp(z))
px = (x - x.min()) * scale + (W - np.ptp(x) * scale) / 2
pz = H - ((z - z.min()) * scale + (H - np.ptp(z) * scale) / 2)
d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in zip(px, pz))

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#58A6FF"/>
      <stop offset="100%" stop-color="#BC8CFF"/>
    </linearGradient>
  </defs>
  <style>
    .trace {{
      fill: none; stroke: url(#g); stroke-width: 1.2; stroke-linejoin: round;
      stroke-dasharray: 1; stroke-dashoffset: 1;
      animation: draw 14s ease-in-out infinite;
    }}
    @keyframes draw {{
      0%   {{ stroke-dashoffset: 1; opacity: 1; }}
      75%  {{ stroke-dashoffset: 0; opacity: 1; }}
      92%  {{ stroke-dashoffset: 0; opacity: 1; }}
      100% {{ stroke-dashoffset: 0; opacity: 0; }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .trace {{ animation: none; stroke-dashoffset: 0; }}
    }}
  </style>
  <path class="trace" pathLength="1" d="{d}"/>
</svg>"""

Path("assets").mkdir(exist_ok=True)
Path("assets/lorenz.svg").write_text(svg)
print("wrote assets/lorenz.svg")