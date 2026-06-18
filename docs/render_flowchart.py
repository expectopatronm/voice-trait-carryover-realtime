from __future__ import annotations

from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "voice_trait_carryover_flow.png"

W, H = 1600, 1080
BG = "#050505"
BOX = "#111111"
WHITE = "#f5f5f5"
MUTED = "#bdbdbd"


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE = font(42, True)
HEAD = font(28, True)
BODY = font(23)
SMALL = font(20)


def centered_text(draw: ImageDraw.ImageDraw, box, lines, fnt, fill=WHITE, spacing=8):
    x1, y1, x2, y2 = box
    if isinstance(lines, str):
        lines = [lines]
    heights = []
    widths = []
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
    total_h = sum(heights) + spacing * (len(lines) - 1)
    y = y1 + ((y2 - y1) - total_h) / 2
    for line, width, height in zip(lines, widths, heights):
        draw.text((x1 + ((x2 - x1) - width) / 2, y), line, font=fnt, fill=fill)
        y += height + spacing


def wrap_to(text: str, width: int) -> list[str]:
    return textwrap.wrap(text, width=width)


def round_box(draw, xy, lines, fnt=BODY, radius=18):
    draw.rounded_rectangle(xy, radius=radius, fill=BOX, outline=WHITE, width=3)
    centered_text(draw, xy, lines, fnt)


def diamond(draw, center, size, lines):
    cx, cy = center
    w, h = size
    pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
    draw.polygon(pts, fill=BOX, outline=WHITE)
    draw.line(pts + [pts[0]], fill=WHITE, width=3)
    centered_text(draw, (cx - w / 2 + 70, cy - h / 2 + 35, cx + w / 2 - 70, cy + h / 2 - 35), lines, BODY)


def arrow(draw, start, end, label: str | None = None):
    draw.line([start, end], fill=WHITE, width=4)
    sx, sy = start
    ex, ey = end
    if abs(ex - sx) > abs(ey - sy):
        direction = 1 if ex > sx else -1
        head = [(ex, ey), (ex - direction * 18, ey - 10), (ex - direction * 18, ey + 10)]
    else:
        direction = 1 if ey > sy else -1
        head = [(ex, ey), (ex - 10, ey - direction * 18), (ex + 10, ey - direction * 18)]
    draw.polygon(head, fill=WHITE)
    if label:
        bbox = draw.textbbox((0, 0), label, font=SMALL)
        tx = (sx + ex) / 2 - (bbox[2] - bbox[0]) / 2
        ty = (sy + ey) / 2 - 32
        draw.rectangle((tx - 8, ty - 4, tx + (bbox[2] - bbox[0]) + 8, ty + (bbox[3] - bbox[1]) + 6), fill=BG)
        draw.text((tx, ty), label, font=SMALL, fill=WHITE)


def poly_arrow(draw, points, label: str | None = None):
    for a, b in zip(points, points[1:]):
        draw.line([a, b], fill=WHITE, width=4)
    arrow(draw, points[-2], points[-1], label=None)
    if label:
        x, y = points[1]
        draw.text((x + 10, y - 34), label, font=SMALL, fill=WHITE)


def main():
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)

    draw.text((W / 2, 42), "Voice Trait Carryover at a Tool Boundary", font=TITLE, fill=WHITE, anchor="mm")

    top = (500, 105, 1100, 185)
    extract = (420, 245, 1180, 345)
    decision_center = (800, 470)

    round_box(draw, top, "Latest spoken user turn", HEAD)
    arrow(draw, (800, 185), (800, 245))
    round_box(draw, extract, ["Extract response-relevant speech traits", "language, register, affect, prosody, tempo, articulation"], BODY)
    arrow(draw, (800, 345), (800, 380))
    diamond(draw, decision_center, (520, 180), ["Does the answer need", "a domain tool?"])

    direct = (95, 610, 570, 735)
    carry = (685, 610, 1115, 735)
    domain = (1160, 610, 1505, 735)
    echo = (685, 805, 1115, 910)
    final = (395, 970, 1205, 1040)

    poly_arrow(draw, [(540, 510), (330, 560), (330, 610)], "No")
    round_box(draw, direct, ["Direct answer", "Use the extracted traits immediately"], BODY)

    poly_arrow(draw, [(1060, 510), (900, 560), (900, 610)], "Yes")
    round_box(draw, carry, ["Ancillary carryover tool", "store_voice_traits_summary_and_response(...)", "arguments preserve trait state"], SMALL)

    poly_arrow(draw, [(1060, 510), (1332, 560), (1332, 610)], None)
    round_box(draw, domain, ["Domain tools", "weather, search, navigation,", "messages, etc."], SMALL)

    arrow(draw, (900, 735), (900, 805))
    round_box(draw, echo, ["No-op protocol echo", "same normalized summary dictionary"], SMALL)

    poly_arrow(draw, [(330, 735), (330, 945), (640, 945), (640, 970)])
    poly_arrow(draw, [(900, 910), (900, 945), (800, 945), (800, 970)])
    poly_arrow(draw, [(1332, 735), (1332, 945), (960, 945), (960, 970)])
    round_box(draw, final, "Final spoken answer preserves speech adaptation", HEAD)

    draw.text((W / 2, 1060), "The semantic tool result and the speech-adaptive response plan meet again before the final answer.", font=SMALL, fill=MUTED, anchor="mm")

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
