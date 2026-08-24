from pathlib import Path
import random


OUTPUT = Path("assets/contribution-calendar.svg")

WIDTH = 1000
HEIGHT = 430

random.seed(42)

# Grid dimensions
columns = 26
rows = 7

cell_w = 25
cell_h = 25

start_x = 100
start_y = 130

# Generate fake contribution activity
levels = []

for week in range(columns):
    week_data = []

    for day in range(rows):
        value = random.choices(
            [0, 1, 2, 3, 4],
            weights=[45, 25, 15, 10, 5]
        )[0]

        week_data.append(value)

    levels.append(week_data)


# Some stronger activity clusters
for week, day, level in [
    (3, 2, 3),
    (4, 2, 4),
    (5, 3, 3),
    (8, 1, 4),
    (9, 1, 3),
    (10, 2, 4),
    (14, 4, 3),
    (15, 4, 4),
    (16, 3, 3),
    (19, 5, 4),
    (20, 4, 3),
    (21, 4, 4),
    (23, 2, 3),
]:
    levels[week][day] = level


# GitHub-like activity levels
colors = {
    0: "#161b22",
    1: "#0e4429",
    2: "#006d32",
    3: "#26a641",
    4: "#39d353",
}


def cube(x, y, level):

    height = 8 + level * 10

    top = [
        (x, y),
        (x + cell_w / 2, y - cell_h / 4),
        (x + cell_w, y),
        (x + cell_w / 2, y + cell_h / 4),
    ]

    left = [
        (x, y),
        (x + cell_w / 2, y + cell_h / 4),
        (x + cell_w / 2, y + cell_h / 4 + height),
        (x, y + height),
    ]

    right = [
        (x + cell_w / 2, y + cell_h / 4),
        (x + cell_w, y),
        (x + cell_w, y + height),
        (x + cell_w / 2, y + cell_h / 4 + height),
    ]

    def pts(points):
        return " ".join(
            f"{px:.1f},{py:.1f}"
            for px, py in points
        )

    base = colors[level]

    svg = f"""
    <polygon
        points="{pts(top)}"
        fill="{base}"
        stroke="#30363d"
        stroke-width="0.7"
    />

    <polygon
        points="{pts(left)}"
        fill="{base}"
        opacity="0.72"
        stroke="#30363d"
        stroke-width="0.7"
    />

    <polygon
        points="{pts(right)}"
        fill="{base}"
        opacity="0.88"
        stroke="#30363d"
        stroke-width="0.7"
    />
    """

    return svg


cells = []

for week in range(columns):

    for day in range(rows):

        x = start_x + week * cell_w
        y = start_y + day * cell_h

        level = levels[week][day]

        if level > 0:
            cells.append(
                cube(x, y, level)
            )


# Contribution statistics
total = sum(
    sum(week)
    for week in levels
)

active_days = sum(
    1
    for week in levels
    for value in week
    if value > 0
)


svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>

<rect
    width="100%"
    height="100%"
    fill="#0d1117"
/>

<style>

.title {{
    font-family: sans-serif;
    font-size: 22px;
    font-weight: bold;
    fill: #f0f6fc;
}}

.link {{
    font-family: sans-serif;
    font-size: 18px;
    fill: #58a6ff;
}}

.stat {{
    font-family: sans-serif;
    font-size: 17px;
    fill: #8b949e;
}}

.number {{
    font-family: sans-serif;
    font-size: 18px;
    font-weight: bold;
    fill: #f0f6fc;
}}

</style>

<text
    x="60"
    y="55"
    class="title"
>
📅 Contribution calendar
</text>

<text
    x="60"
    y="90"
    class="link"
>
Contributions calendar
</text>

<!-- Calendar -->

<g>
{''.join(cells)}
</g>

<!-- Statistics -->

<text
    x="780"
    y="155"
    class="number"
>
🔥 Current streak
</text>

<text
    x="780"
    y="180"
    class="stat"
>
12 days
</text>

<text
    x="780"
    y="220"
    class="number"
>
✦ Best streak
</text>

<text
    x="780"
    y="245"
    class="stat"
>
37 days
</text>

<text
    x="780"
    y="285"
    class="number"
>
● Active days
</text>

<text
    x="780"
    y="310"
    class="stat"
>
{active_days}
</text>

<text
    x="780"
    y="350"
    class="number"
>
↑ Contributions
</text>

<text
    x="780"
    y="375"
    class="stat"
>
{total}
</text>

</svg>
"""


OUTPUT.write_text(
    svg,
    encoding="utf-8"
)

print(f"Created: {OUTPUT}")
print(f"Contribution points: {total}")
print(f"Active days: {active_days}")
