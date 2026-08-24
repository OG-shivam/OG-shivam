from pathlib import Path


OUT = Path("assets")
OUT.mkdir(exist_ok=True)


def save(name, title, lines, width=700, height=220):
    rows = []

    y = 95

    for label, value in lines:
        rows.append(
            f"""
            <text x="40" y="{y}" class="label">{label}</text>
            <text x="650" y="{y}" text-anchor="end" class="value">{value}</text>
            """
        )
        y += 42

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg"
width="{width}" height="{height}"
viewBox="0 0 {width} {height}">

<rect width="100%" height="100%" rx="12"
fill="#0d1117" stroke="#30363d"/>

<style>
.title {{
    font: bold 25px sans-serif;
    fill: #58a6ff;
}}

.label {{
    font: 17px sans-serif;
    fill: #c9d1d9;
}}

.value {{
    font: bold 17px sans-serif;
    fill: #f0f6fc;
}}

.small {{
    font: 13px sans-serif;
    fill: #8b949e;
}}
</style>

<text x="40" y="45" class="title">{title}</text>

{''.join(rows)}

<text x="40" y="{height - 15}" class="small">
Demo profile card • generated locally
</text>

</svg>
"""

    (OUT / name).write_text(svg, encoding="utf-8")


save(
    "github-stats.svg",
    "GitHub Stats",
    [
        ("Total contributions", "486"),
        ("Repositories", "11"),
        ("Commits", "342"),
        ("Pull requests", "18"),
    ],
)


save(
    "languages.svg",
    "Most Used Languages",
    [
        ("Python", "32%"),
        ("JavaScript", "24%"),
        ("C++", "18%"),
        ("Java", "14%"),
        ("HTML / CSS", "12%"),
    ],
)


save(
    "streak.svg",
    "Contribution Streak",
    [
        ("Current streak", "12 days"),
        ("Longest streak", "37 days"),
        ("Total active days", "156"),
        ("Best day", "24 commits"),
    ],
)


save(
    "trophies.svg",
    "GitHub Achievements",
    [
        ("Repositories", "11"),
        ("Commits", "342"),
        ("Issues", "26"),
        ("Pull requests", "18"),
    ],
)


print("Created local profile cards:")
print("  assets/github-stats.svg")
print("  assets/languages.svg")
print("  assets/streak.svg")
print("  assets/trophies.svg")
