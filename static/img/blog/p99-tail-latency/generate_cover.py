#!/usr/bin/env python3
"""
Generate the featured image (1200x630px PNG) for the P99 & Tail Latency blog post.
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


def find_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Try to find a suitable monospace or sans font on the system."""
    candidates = []
    if bold:
        candidates = [
            "/System/Library/Fonts/Supplemental/SFNSMono-Bold.otf",
            "/System/Library/Fonts/SFNS-Bold.otf",
            "/Library/Fonts/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
            "/usr/share/fonts/truetype/ubuntu/UbuntuMono-B.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationMono-Bold.ttf",
        ]
    candidates += [
        "/System/Library/Fonts/Supplemental/SFNSMono-Regular.otf",
        "/System/Library/Fonts/SFNS.ttf",
        "/Library/Fonts/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationMono.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_card(draw: ImageDraw, x: int, y: int, w: int, h: int, title: str = "") -> None:
    """Draw a modern dark card with title bar."""
    # Shadow
    draw.rounded_rectangle(
        [x + 4, y + 4, x + w + 4, y + h + 4],
        radius=12, fill=(0, 0, 0, 80)
    )
    # Body
    draw.rounded_rectangle(
        [x, y, x + w, y + h], radius=10, fill=(18, 24, 38)
    )
    # Header bar
    draw.rounded_rectangle(
        [x, y, x + w, y + 38], radius=10, fill=(28, 36, 56)
    )
    draw.rectangle([x, y + 28, x + w, y + 38], fill=(28, 36, 56))
    
    # Traffic light dots
    for cx, color in [(x + 18, (255, 95, 87)), (x + 40, (255, 189, 46)), (x + 62, (39, 201, 63))]:
        draw.ellipse([cx, y + 13, cx + 12, y + 25], fill=color)
        
    if title:
        font_title = find_font(13, bold=True)
        draw.text((x + w // 2, y + 19), title, fill=(160, 175, 205), font=font_title, anchor="mm")


def create_featured_image(output_path: str) -> None:
    """Create the 1200x630 OG image."""
    img = Image.new("RGBA", (WIDTH, HEIGHT), (11, 15, 25, 255))
    draw = ImageDraw.Draw(img)

    # Background gradient
    top_color = (11, 15, 25)
    bottom_color = (22, 32, 54)
    for i in range(HEIGHT):
        t = i / HEIGHT
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        draw.line([(0, i), (WIDTH, i)], fill=(r, g, b, 255))

    # Grid dots
    for x in range(0, WIDTH, 28):
        for y in range(0, HEIGHT, 28):
            draw.point((x, y), fill=(60, 80, 120, 50))

    # Left Card: PromQL Query & Distribution Metrics
    cw1, ch1 = 540, 360
    cx1, cy1 = 45, 35
    draw_card(draw, cx1, cy1, cw1, ch1, "prometheus-tail-latency — promql")

    font_code_bold = find_font(13, bold=True)
    font_code = find_font(13)
    font_val = find_font(13, bold=True)

    # PromQL code
    py = cy1 + 52
    draw.text((cx1 + 20, py), "# PromQL: Cálculo de Latência P99", fill=(100, 120, 150), font=font_code)
    py += 22
    draw.text((cx1 + 20, py), "histogram_quantile(0.99,", fill=(130, 180, 255), font=font_code_bold)
    py += 20
    draw.text((cx1 + 40, py), "sum(rate(http_duration_bucket[5m]))", fill=(240, 240, 250), font=font_code)
    py += 20
    draw.text((cx1 + 40, py), "by (le)", fill=(240, 240, 250), font=font_code)
    py += 20
    draw.text((cx1 + 20, py), ")", fill=(130, 180, 255), font=font_code_bold)
    py += 30

    # Separator line
    draw.line([(cx1 + 20, py), (cx1 + cw1 - 20, py)], fill=(40, 50, 75), width=1)
    py += 15

    # Visual Percentiles Bars
    percentiles = [
        ("P50 (Mediana)", "45 ms", 0.15, (52, 199, 89)),     # Green
        ("P90", "120 ms", 0.35, (50, 173, 230)),            # Blue
        ("P95", "210 ms", 0.50, (255, 204, 0)),             # Yellow
        ("P99 (Tail)", "890 ms", 0.85, (255, 149, 0)),      # Orange
        ("P99.9 (Max)", "2.4 s", 1.00, (255, 59, 48)),      # Red
    ]

    for label, val, ratio, bar_color in percentiles:
        draw.text((cx1 + 20, py), label, fill=(200, 210, 230), font=font_code)
        draw.text((cx1 + 175, py), val, fill=bar_color, font=font_val)
        
        # Bar track
        bx = cx1 + 245
        bw = 265
        bh = 12
        draw.rounded_rectangle([bx, py + 2, bx + bw, py + 2 + bh], radius=6, fill=(35, 45, 68))
        # Bar fill
        fill_w = max(12, int(bw * ratio))
        draw.rounded_rectangle([bx, py + 2, bx + fill_w, py + 2 + bh], radius=6, fill=bar_color)
        
        py += 26

    # Right Card: The Average Trap vs Reality
    cw2, ch2 = 540, 360
    cx2, cy2 = 615, 35
    draw_card(draw, cx2, cy2, cw2, ch2, "por que a media engana.log")

    py2 = cy2 + 55
    font_bold_lg = find_font(16, bold=True)
    font_body = find_font(14)
    
    draw.text((cx2 + 25, py2), "⚠️ A Armadilha da Média Aritmética", fill=(255, 204, 0), font=font_bold_lg)
    py2 += 30

    stats_lines = [
        ("Cenário:", "10.000 requisições / segundo"),
        ("Média Geral:", "65 ms  (Parece perfeito!)"),
        ("P50 (50%):", "40 ms  (Excelente experiência)"),
        ("P99 (1% mais lento):", "890 ms  (Experiência degradada)"),
        ("Impacto em escala:", "100 req/s sofrem lentidão severa"),
    ]

    for label, text in stats_lines:
        draw.text((cx2 + 25, py2), label, fill=(140, 160, 195), font=font_body)
        highlight = (255, 100, 100) if "P99" in label or "Impacto" in label else (230, 235, 250)
        draw.text((cx2 + 185, py2), text, fill=highlight, font=font_code_bold)
        py2 += 26

    py2 += 12
    # Alert box inside right card
    draw.rounded_rectangle([cx2 + 20, py2, cx2 + cw2 - 20, py2 + 70], radius=8, fill=(32, 42, 65))
    draw.text((cx2 + 35, py2 + 14), "💡 Em arquitetura de microsserviços:", fill=(100, 210, 255), font=font_code_bold)
    draw.text((cx2 + 35, py2 + 38), "1 chamada do usuário toca 20+ serviços.", fill=(210, 220, 240), font=font_body)
    draw.text((cx2 + 35, py2 + 54), "A probabilidade de atingir o P99 salta para ~18%!", fill=(255, 180, 100), font=font_code)

    # Big Title Section at the Bottom
    title_font = find_font(38, bold=True)
    draw.text((WIDTH // 2, 440), "P99 e Latência de Cauda (Tail Latency)",
              fill=(255, 255, 255), font=title_font, anchor="mm")

    subtitle_font = find_font(20, bold=True)
    draw.text((WIDTH // 2, 485), "Por que a média engana e como dominar a performance em sistemas distribuídos",
              fill=(94, 180, 255), font=subtitle_font, anchor="mm")

    badge_font = find_font(14)
    draw.text((WIDTH // 2, 525), "SRE  ·  Observabilidade  ·  Percentis  ·  SLA/SLO  ·  Microsserviços",
              fill=(145, 165, 200), font=badge_font, anchor="mm")

    # EF-TECH branding
    brand_font = find_font(15, bold=True)
    draw.text((WIDTH - 45, HEIGHT - 25), "EF-TECH", fill=(120, 140, 180), font=brand_font, anchor="rs")

    # Save PNG
    final = Image.new("RGB", (WIDTH, HEIGHT), (11, 15, 25))
    final.paste(img, mask=img.split()[3])
    final.save(output_path, "PNG")
    print(f"Image saved to {output_path} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    output = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cover.png")
    create_featured_image(output)
    
    # Also copy to content directories
    root_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../../"))
    pt_dir = os.path.join(root_dir, "content/pt-br/blog/p99-tail-latency")
    en_dir = os.path.join(root_dir, "content/en/blog/p99-tail-latency")
    
    os.makedirs(pt_dir, exist_ok=True)
    os.makedirs(en_dir, exist_ok=True)
    
    shutil.copyfile(output, os.path.join(pt_dir, "cover.png"))
    shutil.copyfile(output, os.path.join(en_dir, "cover.png"))
    print("Copied cover.png to pt-br and en content folders.")
