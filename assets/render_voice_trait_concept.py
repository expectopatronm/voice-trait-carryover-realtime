from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


OUT = Path(__file__).resolve().with_name("voice_trait_concept.png")
W, H = 1600, 620
BG = "#0b0b0b"
PANEL = "#151515"
BOX = "#202020"
WHITE = "#f5f5f5"
MUTED = "#b8b8b8"
ACCENT = "#d7ff3f"


def font(size: int, bold: bool = False):
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            pass
    return ImageFont.load_default()


TITLE = font(42, True)
HEAD = font(28, True)
BODY = font(22)
SMALL = font(19)
MONO = font(18)


def text_center(draw, xy, text, fnt, fill=WHITE):
    draw.text(xy, text, font=fnt, fill=fill, anchor="mm")


def round_box(draw, xy, title, lines, outline=WHITE):
    draw.rounded_rectangle(xy, radius=22, fill=BOX, outline=outline, width=3)
    x1, y1, x2, y2 = xy
    draw.text(((x1 + x2) / 2, y1 + 42), title, font=HEAD, fill=WHITE, anchor="mm")
    y = y1 + 88
    for line in lines:
        draw.text((x1 + 34, y), line, font=SMALL, fill=MUTED)
        y += 32


def arrow(draw, start, end, color=WHITE):
    draw.line([start, end], fill=color, width=4)
    sx, sy = start
    ex, ey = end
    angle = math.atan2(ey - sy, ex - sx)
    size = 16
    left = (ex - size * math.cos(angle - math.pi / 6), ey - size * math.sin(angle - math.pi / 6))
    right = (ex - size * math.cos(angle + math.pi / 6), ey - size * math.sin(angle + math.pi / 6))
    draw.polygon([end, left, right], fill=color)


def waveform(draw, x1, y, x2, amp=28, color=ACCENT):
    pts = []
    for i in range(x1, x2):
        t = (i - x1) / 26
        env = 0.35 + 0.65 * math.sin((i - x1) / (x2 - x1) * math.pi)
        val = y + math.sin(t) * amp * env + math.sin(t * 2.7) * amp * 0.25 * env
        pts.append((i, val))
    draw.line(pts, fill=color, width=3)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.rounded_rectangle((24, 24, W - 24, H - 24), radius=24, fill=PANEL, outline="#333333", width=2)
    text_center(draw, (W / 2, 70), "A voice trait is response-relevant information in the speech signal", TITLE)

    input_box = (70, 145, 470, 500)
    trait_box = (600, 145, 1000, 500)
    output_box = (1130, 145, 1530, 500)

    round_box(
        draw,
        input_box,
        "Input speech",
        [
            "words + delivery",
            "tone, pace, emphasis",
            "register and syntax",
            "uncertainty or affect",
        ],
        outline="#777777",
    )
    waveform(draw, 125, 430, 415)
    draw.text((125, 462), "spoken user turn", font=MONO, fill=ACCENT)

    round_box(
        draw,
        trait_box,
        "Extracted traits",
        [
            "language: English",
            "register: informal",
            "affect: low energy",
            "prosody: gentle / subdued",
        ],
        outline=ACCENT,
    )
    draw.rounded_rectangle((655, 382, 945, 452), radius=14, fill="#101010", outline=ACCENT, width=2)
    text_center(draw, (800, 417), "compact carryover summary", SMALL, ACCENT)

    round_box(
        draw,
        output_box,
        "Response adaptation",
        [
            "warm, calm stance",
            "short spoken clauses",
            "low-pressure wording",
            "no imitation or diagnosis",
        ],
        outline="#777777",
    )
    waveform(draw, 1185, 430, 1475, amp=20, color=WHITE)
    draw.text((1185, 462), "spoken assistant answer", font=MONO, fill=WHITE)

    arrow(draw, (492, 320), (575, 320), ACCENT)
    arrow(draw, (1022, 320), (1105, 320), ACCENT)
    text_center(draw, (535, 285), "extract", SMALL, ACCENT)
    text_center(draw, (1065, 285), "shape output", SMALL, ACCENT)

    draw.text(
        (W / 2, 555),
        "The semantic answer stays correct; the spoken realization changes to fit the user's delivery.",
        font=BODY,
        fill=MUTED,
        anchor="mm",
    )
    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
