#!/usr/bin/env python3
"""Render the GitHub social preview from Global FDE brand tokens."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1280, 640
INK = "#121212"
PAPER = "#FFFDF9"
SAND = "#F4EBDD"
ORANGE = "#FF5A36"
GRAY = "#6B6B68"
FONT_PATHS = [
    Path("/System/Library/Fonts/SFNS.ttf"),
    Path("/System/Library/Fonts/Helvetica.ttc"),
    Path("/System/Library/Fonts/Supplemental/Arial.ttf"),
]
FONT = next(path for path in FONT_PATHS if path.exists())


def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONT), size=size)


def main() -> None:
    image = Image.new("RGB", (WIDTH, HEIGHT), INK)
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((70, 72, 220, 80), radius=4, fill=ORANGE)
    draw.text((70, 108), "GLOBAL FDE / OPEN KNOWLEDGE", font=font(30), fill=PAPER)
    draw.text((70, 205), "Awesome Global FDE", font=font(76), fill=PAPER)
    draw.text((70, 314), "Resources, field practices, cases, and tools", font=font(36), fill=SAND)
    draw.text((70, 363), "for Forward Deployed Engineers.", font=font(36), fill=SAND)
    draw.line((70, 515, 700, 515), fill=GRAY, width=16)
    draw.arc((650, 345, 900, 525), start=0, end=90, fill=GRAY, width=16)
    draw.line((828, 345, 880, 386), fill=ORANGE, width=16)
    draw.line((880, 386, 828, 427), fill=ORANGE, width=16)
    slogan = "From Frontier AI to Real-World Impact."
    draw.text((1210, 545), slogan, font=font(28), fill=ORANGE, anchor="ra")
    output = ROOT / "assets" / "social-preview.png"
    image.save(output, optimize=True)
    print(output)


if __name__ == "__main__":
    main()
