from pathlib import Path
import math


OUTPUT = Path("assets/skill-radar.svg")


def point(cx, cy, radius, angle):
    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)
    return x, y


def polygon(points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def radar(cx, cy, radius, labels, values, color="#39d353"):
    count = len(labels)

    parts = []

    # Background rings
    for level in range(1, 6):
        r = radius * level / 5
        pts = []

        for i in range(count):
            angle = -math.pi / 2 + (2 * math.pi * i / count)
            pts.append(point(cx, cy, r, angle))

        parts.append(
            f'<polygon points="{polygon(pts)}" '
            f'fill="none" stroke="#30363d" stroke-width="1"/>'
        )

    # Axes and labels
    for i, label in enumerate(labels):
        angle = -math.pi / 2 + (2 * math.pi * i / count)

        x, y = point(cx, cy, radius, angle)

        parts.append(
            f'<line x1="{cx}" y1="{cy}" '
            f'x2="{x:.1f}" y2="{y:.1f}" '
            f'stroke="#30363d" stroke-width="1"/>'
        )

        lx, ly = point(cx, cy, radius + 28, angle)

        anchor = "middle"

        if lx < cx - 10:
            anchor = "end"
        elif lx > cx + 10:
            anchor = "start"

        parts.append(
            f'<text x="{lx:.1f}" y="{ly:.1f}" '
            f'text-anchor="{anchor}" '
            f'class="label">{label}</text>'
        )

    # Skill polygon
    skill_points = []

    for i, value in enumerate(values):
        angle = -math.pi / 2 + (2 * math.pi * i / count)
        r = radius * value / 100
        skill_points.append(point(cx, cy, r, angle))

    parts.append(
        f'<polygon points="{polygon(skill_points)}" '
        f'fill="{color}" fill-opacity="0.25" '
        f'stroke="{color}" stroke-width="3"/>'
    )

    # Skill points
    for x, y in skill_points:
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" '
            f'fill="{color}"/>'
        )

    return "\n".join(parts)


skills = [
    "C++",
    "Python",
    "DSA",
    "AI",
    "DBMS",
    "Web",
    "Git/Linux",
]

skill_values = [
    72,
    78,
    65,
    55,
    70,
    58,
    75,
]


languages = [
    "Python",
    "C++",
    "JavaScript",
    "Java",
    "HTML/CSS",
]

language_values = [
    80,
    72,
    55,
    48,
    60,
]


left_chart = radar(
    270,
    225,
    145,
    skills,
    skill_values,
)

right_chart = radar(
    770,
    225,
    145,
    languages,
    language_values,
)


svg = f'''<svg xmlns="http://www.w3.org/2000/svg"
width="1040"
height="470"
viewBox="0 0 1040 470">

<rect width="1040" height="470"
rx="12"
fill="#0d1117"
stroke="#30363d"/>

<style>
.title {{
    font: bold 18px sans-serif;
    fill: #f0f6fc;
}}

.label {{
    font: 12px sans-serif;
    fill: #c9d1d9;
}}
</style>

<text x="270" y="35"
text-anchor="middle"
class="title">
Skill Radar
</text>

<text x="770" y="35"
text-anchor="middle"
class="title">
Language Mix
</text>

<line x1="520" y1="55"
x2="520" y2="445"
stroke="#30363d"/>

{left_chart}

{right_chart}

</svg>
'''

OUTPUT.write_text(svg, encoding="utf-8")

print(f"Created: {OUTPUT}")
