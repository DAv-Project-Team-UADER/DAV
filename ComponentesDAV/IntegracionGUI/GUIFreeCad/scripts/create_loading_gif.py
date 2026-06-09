#!/usr/bin/env python3
"""Generate assets/loading.gif for download progress."""

from pathlib import Path

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("Install Pillow: pip install Pillow")
    raise SystemExit(1)

OUT = Path(__file__).resolve().parent.parent / "assets" / "loading.gif"
FRAMES = 12
SIZE = 64


def draw_frame(i: int) -> Image.Image:
    img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = SIZE // 2, SIZE // 2
    for n in range(8):
        angle = (i + n) * 45
        import math

        rad = math.radians(angle)
        x = cx + int(20 * math.cos(rad))
        y = cy + int(20 * math.sin(rad))
        alpha = 40 + n * 25
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill=(74, 144, 217, min(alpha, 255)))
    return img


def main() -> None:
    frames = [draw_frame(i) for i in range(FRAMES)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=80,
        loop=0,
        disposal=2,
    )
    print("Created", OUT)


if __name__ == "__main__":
    main()
