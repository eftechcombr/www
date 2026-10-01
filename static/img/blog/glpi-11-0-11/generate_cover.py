#!/usr/bin/env python3
"""
Generate the featured image (1200x630px PNG) for the GLPI 11.0.11 blog post.

Design:
  - Dark navy gradient background (#0c101d -> #18223c) with decorative grid dots
  - A terminal window showcasing the pull command, Helm upgrade, and key release features:
    * GLPI 11.0.11 security fixes (superseding 11.0.10 and fixing plugin regression)
    * Custom Nginx config template with IPv6 toggle (PR #209)
    * Database SSL/TLS encryption support (PR #207)
  - Big title "GLPI 11.0.11 Security Release", subtitle, and EF-TECH branding

Requires: pip install pillow
"""

import os
import sys
import shutil

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    print("Pillow is required. Install it with: pip install pillow")
    sys.exit(1)

WIDTH, HEIGHT = 1200, 630


def find_font(size: int, bold: bool = False, mono: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Try to find a suitable font on the system."""
    candidates = []
    if mono:
        if bold:
            candidates = [
                "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
                "/System/Library/Fonts/Supplemental/PTMono.ttc",
                "/System/Library/Fonts/Supplemental/SFNSMono-Bold.otf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
            ]
        else:
            candidates = [
                "/System/Library/Fonts/Supplemental/Courier New.ttf",
                "/System/Library/Fonts/Supplemental/PTMono.ttc",
                "/System/Library/Fonts/Supplemental/Andale Mono.ttf",
                "/System/Library/Fonts/Supplemental/SFNSMono-Regular.otf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                "/usr/share/fonts/truetype/liberation/LiberationMono.ttf",
            ]
    else:
        if bold:
            candidates = [
                "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
                "/Library/Fonts/Arial Bold.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ]
        else:
            candidates = [
                "/System/Library/Fonts/Supplemental/Arial.ttf",
                "/Library/Fonts/Arial.ttf",
                "/System/Library/Fonts/Helvetica.ttc",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
            ]

    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_terminal_window(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int) -> None:
    """Draw a terminal window with a title bar."""
    shadow_offset = 6
    draw.rounded_rectangle(
        [x + shadow_offset, y + shadow_offset, x + w + shadow_offset, y + h + shadow_offset],
        radius=14, fill=(0, 0, 0, 90)
    )
    # Window body
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=12, fill=(18, 23, 38)
    )
    # Title bar
    draw.rounded_rectangle(
        [x, y, x + w, y + 42], radius=12, fill=(28, 35, 58)
    )
    draw.rectangle([x, y + 30, x + w, y + 42], fill=(28, 35, 58))

    # Traffic light buttons
    for cx, color in [(x + 22, (255, 95, 87)), (x + 48, (255, 189, 46)), (x + 74, (39, 201, 63))]:
        draw.ellipse([cx, y + 14, cx + 14, y + 28], fill=color)

    font_title = find_font(14, bold=True, mono=True)
    draw.text((x + w // 2, y + 21), "eftechcombr/glpi — v11.0.11 (Security Release)",
              fill=(180, 195, 225), font=font_title, anchor="mm")


def create_featured_image(output_path: str) -> None:
    """Create the 1200x630 OG image for the GLPI 11.0.11 post."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), (12, 16, 29, 255))
    draw = ImageDraw.Draw(img)

    # Background gradient #0c101d -> #18223c
    top = (12, 16, 29)
    bottom = (24, 34, 60)
    for i in range(HEIGHT):
        t = i / HEIGHT
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, i), (WIDTH, i)], fill=(r, g, b, 255))

    # Decorative grid dots
    for x in range(0, WIDTH, 32):
        for y in range(0, HEIGHT, 32):
            draw.point((x, y), fill=(70, 90, 140, 50))

    # Terminal window
    tw, th = 980, 360
    tx, ty = (WIDTH - tw) // 2, 28
    draw_terminal_window(draw, tx, ty, tw, th)

    # Terminal text
    font_cmd = find_font(15, bold=True, mono=True)
    font_out = find_font(14, mono=True)
    font_highlight = find_font(14, bold=True, mono=True)

    prompt_x = tx + 32
    line_y = ty + 56

    draw.text((prompt_x, line_y), "$", fill=(52, 211, 153), font=font_cmd)
    draw.text((prompt_x + 18, line_y), " docker pull ghcr.io/eftechcombr/glpi:11.0.11",
              fill=(240, 245, 255), font=font_cmd)
    line_y += 24

    draw.text((prompt_x, line_y), "$", fill=(52, 211, 153), font=font_cmd)
    draw.text((prompt_x + 18, line_y), " helm upgrade --install glpi eftech/glpi --version 2.11.7",
              fill=(240, 245, 255), font=font_cmd)
    line_y += 26

    terminal_lines = [
        ("✔ UPGRADE CRITICAL: GLPI 11.0.11 directly supersedes 11.0.10 (fixes plugins regression)", (248, 113, 113), True),
        ("✔ SECURITY: Patches 6 High + 2 Medium CVEs (Auth bypass, PrivEsc, SQLi, XSS)", (251, 191, 36), True),
        ("✔ NGINX: Custom template support & IPv6 listener disable option (PR #209)", (56, 189, 248), False),
        ("✔ DATABASE: Native MySQL / MariaDB SSL connection support (PR #207)", (56, 189, 248), False),
        ("✔ CLOUD-NATIVE: Hardened non-root containers, Valkey caching & S3 backups ready", (148, 163, 184), False),
        ("✔ STATUS: Built, tested and published for production workloads", (52, 211, 153), True),
    ]

    for text, color, bold in terminal_lines:
        f = font_highlight if bold else font_out
        draw.text((prompt_x, line_y), text, fill=color, font=f)
        line_y += 22

    # Title section below terminal
    title_font = find_font(42, bold=True, mono=False)
    draw.text((WIDTH // 2, ty + th + 66), "GLPI 11.0.11 Security Release",
              fill=(255, 255, 255), font=title_font, anchor="mm")

    subtitle_font = find_font(21, bold=True, mono=False)
    draw.text((WIDTH // 2, ty + th + 118),
              "Critical Security Fixes · Plugin System Fix · Custom Nginx · MySQL SSL",
              fill=(56, 189, 248), font=subtitle_font, anchor="mm")

    info_font = find_font(15, mono=False)
    draw.text((WIDTH // 2, ty + th + 158),
              "EF-TECH Cloud-Native Containers & Helm Charts · Production Ready",
              fill=(156, 163, 175), font=info_font, anchor="mm")

    # EF-TECH branding
    brand_font = find_font(15, bold=True, mono=False)
    draw.text((WIDTH - 36, HEIGHT - 22), "EF-TECH", fill=(96, 165, 250), font=brand_font, anchor="rs")

    final = Image.new("RGB", (WIDTH, HEIGHT), (12, 16, 29))
    final.paste(img, mask=img.split()[3])
    final.save(output_path, "PNG")
    print(f"Image saved to {output_path} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.png")
    create_featured_image(output)

    # Automatically copy to content bundle folders
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
    pt_dir = os.path.join(repo_root, "content", "pt-br", "blog", "glpi-11-0-11")
    en_dir = os.path.join(repo_root, "content", "en", "blog", "glpi-11-0-11")
    os.makedirs(pt_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    shutil.copyfile(output, os.path.join(pt_dir, "cover.png"))
    shutil.copyfile(output, os.path.join(en_dir, "cover.png"))
    print("Copied cover.png to pt-br and en content bundles.")
