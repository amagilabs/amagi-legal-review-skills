#!/usr/bin/env python3
"""
make_demo_gif.py — builds assets/demo.gif, a synthetic terminal-style
looping GIF demoing legal-review-lead on the sample NDA, in AmagiLabs
brand colors (cream background / terracotta accent).

Content is paraphrased from examples/example_run.md. Stdlib + Pillow only.
"""
import os
from PIL import Image, ImageDraw, ImageFont

OFF = (246, 244, 241)      # cream background
INK = (22, 22, 22)         # near-black text
CORAL = (210, 122, 115)    # terracotta accent
GOLD = (230, 200, 156)     # gold accent
DIM = (120, 116, 112)      # muted gray-brown for comments

W, H = 860, 480
PAD = 28
LINE_H = 24
FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
FONT = ImageFont.truetype(FONT_PATH, 16)
FONT_BOLD_SIZE = ImageFont.truetype(FONT_PATH, 16)

# (text, color) per line; "" marker lines get a blank row
LINES = [
    ("$ claude run legal-review-lead examples/sample_nda.txt", CORAL),
    ("", None),
    ("> NOT LEGAL ADVICE — attorney work product only.", DIM),
    ("> Review by a licensed attorney before relying on any output.", DIM),
    ("", None),
    ("[1/9] legal-clause-extractor ....... clause map built (12 clauses)", INK),
    ("[2/9] legal-playbook-checker ....... 4 findings vs NDA playbook", INK),
    ("[3/9] legal-jurisdiction-researcher  1 citation verified, 0 flagged", INK),
    ("[4/9] legal-risk-scorer ............ risk matrix ranked", INK),
    ("[5/9] legal-redline-drafter ........ redline drafted (Sec 6)", INK),
    ("[6/9] legal-negotiation-strategist . concession ladder built", INK),
    ("[7/9] legal-client-memo-writer ..... 1-page memo written", INK),
    ("[8/9] legal-adversarial-reviewer ... 0 hallucinated findings", INK),
    ("[9/9] legal-review-lead ............ sign-off package assembled", INK),
    ("", None),
    ("Sec 6 Remedies  [severity 4]", GOLD),
    ("  one-way, uncapped indemnity in a MUTUAL NDA", INK),
    ("  redline: add cap + make indemnity mutual", INK),
    ("", None),
    ("REVIEW.md written -> runs/2026-10-19/", CORAL),
    ("Ready for licensed-attorney sign-off.", CORAL),
]


def render_frame(n_lines_visible, cursor_on):
    img = Image.new("RGB", (W, H), OFF)
    draw = ImageDraw.Draw(img)

    # terminal "window" chrome
    draw.rectangle([0, 0, W - 1, 40], fill=INK)
    for i, c in enumerate([CORAL, GOLD, DIM]):
        draw.ellipse([16 + i * 22, 14, 16 + i * 22 + 12, 26], fill=c)
    draw.text((W / 2 - 110, 10), "legal-review-skills — demo", font=FONT, fill=OFF)

    y = 56
    for i in range(min(n_lines_visible, len(LINES))):
        text, color = LINES[i]
        if text:
            draw.text((PAD, y), text, font=FONT, fill=color)
        y += LINE_H

    # blinking cursor on the last visible line
    if cursor_on and n_lines_visible < len(LINES):
        draw.rectangle([PAD, y, PAD + 9, y + 16], fill=CORAL)

    # thin brand-accent border
    draw.rectangle([0, 0, W - 1, H - 1], outline=CORAL, width=3)
    return img


def main():
    frames = []
    durations = []

    # typing-in effect: reveal one line at a time
    for n in range(1, len(LINES) + 1):
        frames.append(render_frame(n, cursor_on=(n % 2 == 0)))
        durations.append(280)

    # hold on the final, fully-rendered frame
    for _ in range(20):
        frames.append(render_frame(len(LINES), cursor_on=True))
        durations.append(300)

    out_path = os.path.join(os.path.dirname(__file__), "demo.gif")
    frames[0].save(
        out_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True,
    )
    total_s = sum(durations) / 1000
    print(f"wrote {out_path} ({len(frames)} frames, ~{total_s:.1f}s loop)")


if __name__ == "__main__":
    main()
