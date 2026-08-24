from PIL import Image, ImageEnhance
from pathlib import Path
import argparse


def create_portrait(
    input_file,
    output_file,
    width=160,
    spacing=5,
    max_radius=2.5,
    animate=True,
):
    image = Image.open(input_file).convert("RGB")

    # Crop around the subject
    w, h = image.size

    left = int(w * 0.08)
    top = int(h * 0.02)
    right = int(w * 0.92)
    bottom = int(h * 0.96)

    image = image.crop((left, top, right, bottom))

    # Improve colors and contrast
    image = ImageEnhance.Color(image).enhance(1.4)
    image = ImageEnhance.Contrast(image).enhance(1.35)
    image = ImageEnhance.Sharpness(image).enhance(1.5)

    # Resize
    aspect = image.height / image.width
    height = max(1, int(width * aspect * 0.55))

    image = image.resize(
        (width, height),
        Image.Resampling.LANCZOS
    )

    pixels = image.load()

    svg_width = width * spacing
    svg_height = height * spacing

    circles = []

    for y in range(height):
        for x in range(width):

            r, g, b = pixels[x, y]

            brightness = (
                0.299 * r +
                0.587 * g +
                0.114 * b
            )

            if brightness < 10:
                continue

            normalized = brightness / 255.0

            radius = 0.45 + (
                normalized * max_radius
            )

            cx = x * spacing + spacing / 2
            cy = y * spacing + spacing / 2

            opacity = 0.35 + (
                normalized * 0.65
            )

            color = f"rgb({r},{g},{b})"

            if animate:

                delay = (
                    (x / width) * 0.8 +
                    (y / height) * 1.2
                )

                circle = f"""
<circle
    cx="{cx:.2f}"
    cy="{cy:.2f}"
    r="{radius:.2f}"
    fill="{color}"
    opacity="0"
>
    <animate
        attributeName="opacity"
        from="0"
        to="{opacity:.3f}"
        begin="{delay:.2f}s"
        dur="0.6s"
        fill="freeze"
    />
</circle>
"""

            else:

                circle = f"""
<circle
    cx="{cx:.2f}"
    cy="{cy:.2f}"
    r="{radius:.2f}"
    fill="{color}"
    opacity="{opacity:.3f}"
/>
"""

            circles.append(circle)

    svg = f"""<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{svg_width}"
    height="{svg_height}"
    viewBox="0 0 {svg_width} {svg_height}"
>

<rect
    width="100%"
    height="100%"
    fill="#0d1117"
/>

<g>
{''.join(circles)}
</g>

</svg>
"""

    Path(output_file).write_text(
        svg,
        encoding="utf-8"
    )

    print(f"Created: {output_file}")
    print(f"Canvas: {svg_width} x {svg_height}")
    print(f"Dots: {len(circles)}")


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("input")

    parser.add_argument(
        "-o",
        "--output",
        default="assets/portrait.svg"
    )

    parser.add_argument(
        "--width",
        type=int,
        default=160
    )

    parser.add_argument(
        "--spacing",
        type=int,
        default=5
    )

    parser.add_argument(
        "--radius",
        type=float,
        default=2.5
    )

    parser.add_argument(
        "--no-animation",
        action="store_true"
    )

    args = parser.parse_args()

    create_portrait(
        args.input,
        args.output,
        width=args.width,
        spacing=args.spacing,
        max_radius=args.radius,
        animate=not args.no_animation
    )


if __name__ == "__main__":
    main()

