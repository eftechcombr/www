#!/usr/bin/env python3
"""
Generate the featured image (1200x630px PNG) for the Gateway API v1.6 blog post.

Design (same dark-terminal style as the Ansible CLI GitHub Action cover):
  - Dark navy gradient background (#0e1120 -> #1e2a4a) with a grid of dots
  - A terminal window showing `kubectl apply -f gateway.yaml` plus a
    Gateway / TCPRoute YAML snippet
  - Big title "Gateway API v1.6", subtitle "TCPRoute & UDPRoute Graduate
    to Standard", and EF-TECH branding at the bottom right

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
    """Draw a terminal window with a title bar."""
    # Window shadow
    shadow_offset = 4
    draw.rounded_rectangle(
        [x + shadow_offset, y + shadow_offset, x + w + shadow_offset, y + h + shadow_offset],
        radius=12, fill=(0, 0, 0, 60)
    )
    # Window body (dark terminal bg)
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=10, fill=(22, 26, 46)
    )
    # Title bar area
    draw.rounded_rectangle(
        [x, y, x + w, y + 42], radius=10, fill=(32, 38, 64)
    )
    # Flatten bottom corners of title bar
    draw.rectangle([x, y + 32, x + w, y + 42], fill=(32, 38, 64))
    # Traffic light buttons
    for cx, color in [(x + 20, (255, 95, 87)), (x + 46, (255, 189, 46)), (x + 72, (39, 201, 63))]:
        draw.ellipse([cx, y + 14, cx + 14, y + 28], fill=color)
    # Title text in title bar
    font_title = find_font(15)
    draw.text((x + w // 2, y + 21), "gateway-api-v1-6 — bash", fill=(170, 180, 210),
              font=font_title, anchor="mm")


def create_featured_image(output_path: str) -> None:
    """Create the 1200x630 OG image for the Gateway API v1.6 post."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), (14, 17, 32, 255))
    draw = ImageDraw.Draw(img)

    # Background: subtle gradient #0e1120 (top) -> #1e2a4a (bottom)
    top = (14, 17, 32)
    bottom = (30, 42, 74)
    for i in range(HEIGHT):
        t = i / HEIGHT
        r = int(top[0] + (bottom[0] - top[0]) * t)
        g = int(top[1] + (bottom[1] - top[1]) * t)
        b = int(top[2] + (bottom[2] - top[2]) * t)
        draw.line([(0, i), (WIDTH, i)], fill=(r, g, b, 255))

    # Decorative grid dots
    for x in range(0, WIDTH, 30):
        for y in range(0, HEIGHT, 30):
            draw.point((x, y), fill=(70, 84, 130, 60))

    # Terminal window (central element)
    tw, th = 960, 360
    tx, ty = (WIDTH - tw) // 2, 30
    draw_terminal_window(draw, tx, ty, tw, th)

    # Terminal content
    font_cmd = find_font(15, bold=True)
    font_out = find_font(14)
    font_yaml = find_font(14)

    prompt_x = tx + 30
    line_y = ty + 56

    # Command + output lines
    draw.text((prompt_x, line_y), "$", fill=(82, 188, 74), font=font_cmd)
    draw.text((prompt_x + 20, line_y), " kubectl apply -f gateway.yaml", fill=(240, 242, 250), font=font_cmd)
    line_y += 22

    for out_line in [
        "gateway.gateway.networking.k8s.io/tcp-gateway created",
        "tcproute.gateway.networking.k8s.io/database created",
    ]:
        draw.text((prompt_x, line_y), out_line, fill=(120, 170, 255), font=font_out)
        line_y += 22

    # Blank spacer
    line_y += 6

    # YAML snippet — Gateway listener (TCP)
    yaml_lines = [
        ("", "apiVersion: gateway.networking.k8s.io/v1", (225, 230, 245)),
        ("", "kind: Gateway", (225, 230, 245)),
        ("", "spec:", (225, 230, 245)),
        ("", "  listeners:", (225, 230, 245)),
        ("", "    - name: tcp", (225, 230, 245)),
        ("key", "      protocol: TCP", (82, 188, 74)),
        ("", "      port: 3306", (225, 230, 245)),
        ("", "      allowedRoutes:", (225, 230, 245)),
        ("", "        kinds: [TCPRoute]", (225, 230, 245)),
        ("sep", "---", (120, 130, 170)),
        ("", "kind: TCPRoute   # attaches via parentRefs", (225, 230, 245)),
        ("", "spec:", (225, 230, 245)),
        ("", "  parentRefs:", (225, 230, 245)),
        ("", "    - name: tcp-gateway", (225, 230, 245)),
        ("", "  rules:", (225, 230, 245)),
        ("", "    - backendRefs:", (225, 230, 245)),
        ("", "        - name: database, port: 3306", (225, 230, 245)),
    ]

    for kind, text, color in yaml_lines:
        if kind == "sep":
            draw.text((prompt_x, line_y), text, fill=color, font=font_yaml)
        elif kind == "key":
            # Highlight the protocol keyword
            draw.text((prompt_x, line_y), text, fill=color, font=font_yaml, stroke_width=0)
        else:
            draw.text((prompt_x, line_y), text, fill=color, font=font_yaml)
        line_y += 19

    # Title overlay below the terminal
    title_font = find_font(46, bold=True)
    draw.text((WIDTH // 2, ty + th + 66), "Gateway API v1.6",
              fill=(255, 255, 255), font=title_font, anchor="mm")

    subtitle_font = find_font(24, bold=True)
    draw.text((WIDTH // 2, ty + th + 118), "TCPRoute & UDPRoute Graduate to Standard",
              fill=(94, 170, 255), font=subtitle_font, anchor="mm")

    info_font = find_font(15)
    draw.text((WIDTH // 2, ty + th + 156), "v1.6.0  ·  Released June 30, 2026  ·  Kubernetes SIG Network",
              fill=(140, 150, 185), font=info_font, anchor="mm")

    # EF-TECH branding
    brand_font = find_font(14, bold=True)
    draw.text((WIDTH - 30, HEIGHT - 20), "EF-TECH", fill=(100, 110, 145), font=brand_font, anchor="rs")

    # Convert to RGB and save as PNG
    final = Image.new("RGB", (WIDTH, HEIGHT), (14, 17, 32))
    final.paste(img, mask=img.split()[3])
    final.save(output_path, "PNG")
    print(f"Image saved to {output_path} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.png")
    create_featured_image(output)
