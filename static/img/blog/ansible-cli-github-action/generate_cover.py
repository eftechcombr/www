#!/usr/bin/env python3
"""
Generate the featured image (1200x630px PNG) for the Ansible CLI GitHub Action blog post.
Requires: pip install pillow
"""

import os
import sys

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow is required. Install it with: pip install pillow")
    sys.exit(1)

WIDTH, HEIGHT = 1200, 630


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Try to find a suitable monospace font on the system."""
    candidates = []
    if bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/SFNSMono-Bold.otf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        ]
    candidates += [
        "/System/Library/Fonts/Supplemental/SFNSMono-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_terminal_window(draw: ImageDraw, x: int, y: int, w: int, h: int) -> None:
    """Draw a terminal window with title bar."""
    # Window shadow
    shadow_offset = 4
    draw.rounded_rectangle(
        [x + shadow_offset, y + shadow_offset, x + w + shadow_offset, y + h + shadow_offset],
        radius=12, fill=(0, 0, 0, 60)
    )
    # Window body (dark terminal bg)
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=10, fill=(30, 30, 46)
    )
    # Title bar area
    draw.rounded_rectangle(
        [x, y, x + w, y + 42], radius=10, fill=(40, 40, 56)
    )
    # Flatten bottom corners of title bar
    draw.rectangle([x, y + 32, x + w, y + 42], fill=(40, 40, 56))
    # Traffic light buttons
    for cx, color in [(x + 20, (255, 95, 87)), (x + 46, (255, 189, 46)), (x + 72, (39, 201, 63))]:
        draw.ellipse([cx, y + 14, cx + 14, y + 28], fill=color)
    # Title text in title bar
    font_title = find_font(15)
    draw.text((x + w // 2, y + 21), "ansible-cli-github-action — bash", fill=(170, 170, 190),
              font=font_title, anchor="mm")


def draw_ascii_ansible_logo(draw: ImageDraw, x: int, y: int, scale: float = 1.0) -> None:
    """Draw a simple Ansible-style 'A' with an arrow using lines."""
    # Simple stylized "A" with arrow/cycle (like the Ansible logo)
    color = (255, 255, 255)
    s = int(50 * scale)
    # Left leg of A
    draw.line([(x, y + s), (x + s // 2, y)], fill=color, width=max(3, int(4 * scale)))
    # Right leg of A
    draw.line([(x + s // 2, y), (x + s, y + s)], fill=color, width=max(3, int(4 * scale)))
    # Crossbar of A
    draw.line([(x + s // 4, y + s // 2), (x + 3 * s // 4, y + s // 2)], fill=color,
              width=max(2, int(3 * scale)))
    # Arrow/cycle element
    cx, cy = x + s // 2, y - int(12 * scale)
    r = int(16 * scale)
    draw.arc([cx - r, cy - r, cx + r, cy + r], start=0, end=300, fill=(82, 188, 74),
             width=max(2, int(3 * scale)))
    # Arrowhead
    ax = cx + r - 2
    ay = cy - int(r * 0.5)
    draw.polygon([(ax, ay), (ax - 6, ay - 3), (ax - 6, ay + 3)], fill=(82, 188, 74))


def create_featured_image(output_path: str) -> None:
    """Create the 1200x630 OG image."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), (18, 18, 30, 255))
    draw = ImageDraw.Draw(img)

    # Background: subtle gradient (manual bands)
    for i in range(HEIGHT):
        r = int(18 + (i / HEIGHT) * 12)
        g = int(18 + (i / HEIGHT) * 8)
        b = int(30 + (i / HEIGHT) * 16)
        draw.line([(0, i), (WIDTH, i)], fill=(r, g, b, 255))

    # Decorative grid dots
    for x in range(0, WIDTH, 30):
        for y in range(0, HEIGHT, 30):
            draw.point((x, y), fill=(40, 40, 60, 60))

    # Big terminal window (central element)
    tw, th = 940, 380
    tx, ty = (WIDTH - tw) // 2, (HEIGHT - th) // 2 - 10
    draw_terminal_window(draw, tx, ty, tw, th)

    # Terminal content — Ansible command and output
    font_cmd = find_font(22, bold=True)
    font_output = find_font(18)
    font_prompt = find_font(18, bold=True)

    # Prompt line
    prompt_x = tx + 30
    prompt_y = ty + 65
    draw.text((prompt_x, prompt_y), "$", fill=(82, 188, 74), font=font_prompt)

    cmd_text = " ansible-playbook deploy.yml -i inventory.yml"
    draw.text((prompt_x + 20, prompt_y), cmd_text, fill=(240, 240, 250), font=font_cmd)

    # Output lines
    output_lines = [
        ("PLAY", (82, 188, 74), "[Deploy web application]"),
        ("TASK", (82, 188, 74), "[Gathering Facts]  ok: [web-01]"),
        ("TASK", (82, 188, 74), "[Gathering Facts]  ok: [web-02]"),
        ("TASK", (82, 188, 74), "[Install nginx]   changed: [web-01]"),
        ("TASK", (82, 188, 74), "[Install nginx]   changed: [web-02]"),
        ("PLAY", (0, 170, 255), "RECAP"),
        ("", (240, 240, 250), "web-01 : ok=3  changed=2  unreachable=0  failed=0"),
        ("", (240, 240, 250), "web-02 : ok=3  changed=2  unreachable=0  failed=0"),
    ]

    for i, (prefix, color, line) in enumerate(output_lines):
        ly = prompt_y + 42 + i * 34
        if prefix:
            draw.text((prompt_x, ly), prefix, fill=color, font=font_prompt)
            draw.text((prompt_x + 20, ly), line, fill=(240, 240, 250), font=font_output)
        else:
            draw.text((prompt_x, ly), line, fill=color, font=font_output)

    # Title overlay at bottom of terminal
    title_font = find_font(32, bold=True)
    draw.text((WIDTH // 2, ty + th + 40), "Ansible CLI GitHub Action",
              fill=(255, 255, 255), font=title_font, anchor="mm")

    subtitle_font = find_font(16)
    draw.text((WIDTH // 2, ty + th + 78), "Run Ansible commands directly in your GitHub Actions workflows",
              fill=(140, 140, 170), font=subtitle_font, anchor="mm")

    # EF-TECH branding
    brand_font = find_font(14)
    draw.text((WIDTH - 30, HEIGHT - 20), "EF-TECH", fill=(100, 100, 130), font=brand_font, anchor="rs")

    # Small Ansible-style logo near the top-right of the terminal
    draw_ascii_ansible_logo(draw, tx + tw - 80, ty + 55, scale=0.8)

    # Convert to RGB and save as PNG
    final = Image.new("RGB", (WIDTH, HEIGHT), (18, 18, 30))
    final.paste(img, mask=img.split()[3])
    final.save(output_path, "PNG")
    print(f"Image saved to {output_path} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.png")
    create_featured_image(output)
