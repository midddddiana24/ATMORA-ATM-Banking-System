"""
ATMORA - Logo Generator
========================
Creates the ATMORA brand logo programmatically using Pillow.

No external image files are required — the logo is drawn with code.
This makes the application self-contained and portable.

Logo design concept:
  - Navy blue circular background with gold border
  - ATM card shape with EMV chip
  - Shield security icon
  - Clean, professional banking aesthetic

Course: CIT 240 – Open Source Programming
"""

import os
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDING_DIR = os.path.join(BASE_DIR, 'assets', 'branding')


# ============================================================
# LOGO DRAWING FUNCTION
# ============================================================

def draw_logo(size: int = 200) -> Image.Image:
    """
    Draw the ATMORA logo as a PIL Image.
    
    Parameters:
        size: Pixel size of the square logo (default 200)
    
    Returns:
        PIL.Image.Image with RGBA mode (transparent background)
    
    Design elements:
        1. Dark navy outer circle with gold ring
        2. ATM card shape with EMV chip grid
        3. Shield security badge below card
    """
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    cx = size // 2
    cy = size // 2
    pad = max(3, size // 50)

    # --------------------------------------------------------
    # 1. OUTER CIRCLE — Navy background with gold border
    # --------------------------------------------------------
    draw.ellipse(
        [pad, pad, size - pad, size - pad],
        fill='#1A2D5A',
        outline='#F5A623',
        width=max(2, size // 50)
    )

    # Inner decorative ring (subtle)
    inner_r = size // 7
    draw.ellipse(
        [inner_r, inner_r, size - inner_r, size - inner_r],
        outline='#263A6A',
        width=max(1, size // 100)
    )

    # --------------------------------------------------------
    # 2. ATM CARD SHAPE
    # --------------------------------------------------------
    card_w = int(size * 0.58)
    card_h = int(size * 0.36)
    card_x1 = cx - card_w // 2
    card_y1 = cy - card_h // 2 - int(size * 0.06)
    card_x2 = card_x1 + card_w
    card_y2 = card_y1 + card_h
    card_r = max(4, size // 30)

    draw.rounded_rectangle(
        [card_x1, card_y1, card_x2, card_y2],
        radius=card_r,
        fill='#1E4A8C',
        outline='#3A72C8',
        width=max(1, size // 80)
    )

    # Magnetic stripe (dark horizontal band at top of card)
    stripe_h = max(6, int(card_h * 0.18))
    draw.rectangle(
        [card_x1, card_y1 + card_r, card_x2, card_y1 + card_r + stripe_h],
        fill='#0A1628'
    )

    # --------------------------------------------------------
    # 3. EMV CHIP (gold grid pattern)
    # --------------------------------------------------------
    chip_w = max(12, int(size * 0.11))
    chip_h = max(10, int(size * 0.09))
    chip_x1 = card_x1 + int(card_w * 0.10)
    chip_y1 = card_y1 + int(card_h * 0.42)
    chip_x2 = chip_x1 + chip_w
    chip_y2 = chip_y1 + chip_h
    chip_r = max(1, size // 100)

    draw.rounded_rectangle(
        [chip_x1, chip_y1, chip_x2, chip_y2],
        radius=chip_r,
        fill='#D4A017',
        outline='#A07810',
        width=1
    )

    # Chip internal grid lines
    for i in range(1, 3):
        gy = chip_y1 + i * chip_h // 3
        draw.line([chip_x1 + 2, gy, chip_x2 - 2, gy], fill='#A07810', width=1)
    for j in range(1, 3):
        gx = chip_x1 + j * chip_w // 3
        draw.line([gx, chip_y1 + 2, gx, chip_y2 - 2], fill='#A07810', width=1)

    # --------------------------------------------------------
    # 4. CONTACTLESS SYMBOL (wifi-style arcs)
    # --------------------------------------------------------
    wave_cx = card_x2 - int(card_w * 0.15)
    wave_cy = card_y1 + int(card_h * 0.55)
    dot_r = max(2, size // 60)
    draw.ellipse(
        [wave_cx - dot_r, wave_cy - dot_r, wave_cx + dot_r, wave_cy + dot_r],
        fill='#90CAF9'
    )
    for arc_r in [int(size * 0.040), int(size * 0.070)]:
        draw.arc(
            [wave_cx - arc_r, wave_cy - arc_r, wave_cx + arc_r, wave_cy + arc_r],
            start=30, end=150,
            fill='#90CAF9',
            width=max(1, size // 70)
        )

    # --------------------------------------------------------
    # 5. CARD NUMBER DOTS (masked card number style)
    # --------------------------------------------------------
    dot_y = card_y2 - int(card_h * 0.25)
    dot_size = max(2, size // 60)
    for group in range(3):  # 3 groups of dots
        for dot in range(4):
            dx = card_x1 + int(card_w * 0.10) + group * int(card_w * 0.24) + dot * (dot_size + 3)
            draw.ellipse([dx, dot_y, dx + dot_size, dot_y + dot_size], fill='#90A4AE')

    # --------------------------------------------------------
    # 6. SHIELD BADGE (security icon below card)
    # --------------------------------------------------------
    sh = int(size * 0.22)  # shield height
    sw = int(sh * 0.80)    # shield width
    sx = cx - sw // 2
    sy = card_y2 + int(size * 0.04)

    # Shield polygon
    shield_pts = [
        (cx, sy + sh),                  # bottom tip
        (sx, sy + int(sh * 0.55)),      # lower-left
        (sx, sy),                       # top-left
        (cx, sy),                       # top-center
        (sx + sw, sy),                  # top-right
        (sx + sw, sy + int(sh * 0.55)), # lower-right
    ]
    draw.polygon(shield_pts, fill='#F5A623')
    draw.line(shield_pts + [shield_pts[0]], fill='#E08C00', width=1)

    # Shield inner (dark fill)
    ip = max(3, size // 50)
    inner_pts = [
        (cx, sy + sh - ip - 1),
        (sx + ip, sy + int(sh * 0.55) - ip // 2),
        (sx + ip, sy + ip),
        (cx, sy + ip),
        (sx + sw - ip, sy + ip),
        (sx + sw - ip, sy + int(sh * 0.55) - ip // 2),
    ]
    draw.polygon(inner_pts, fill='#1A2D5A')

    # Checkmark on shield (✓)
    ck_unit = max(2, int(sh * 0.12))
    ck_x1 = cx - ck_unit * 2
    ck_y1 = sy + int(sh * 0.50)
    ck_xm = cx - ck_unit // 2
    ck_ym = sy + int(sh * 0.66)
    ck_x2 = cx + ck_unit * 2
    ck_y2 = sy + int(sh * 0.34)
    ck_w = max(2, size // 50)
    draw.line([ck_x1, ck_y1, ck_xm, ck_ym], fill='#FFFFFF', width=ck_w)
    draw.line([ck_xm, ck_ym, ck_x2, ck_y2], fill='#FFFFFF', width=ck_w)

    return img


# ============================================================
# PUBLIC API
# ============================================================

def get_logo(size: int = 120) -> Image.Image:
    """Return ATMORA logo as a PIL Image at the given size."""
    logo = draw_logo(200)
    if size != 200:
        logo = logo.resize((size, size), Image.LANCZOS)
    return logo


def save_logo_assets():
    """
    Save logo image files to assets/branding/ directory.
    Called once during app initialization.
    """
    os.makedirs(BRANDING_DIR, exist_ok=True)

    # Save full-size logo (200x200)
    logo_full = draw_logo(200)
    logo_full.save(os.path.join(BRANDING_DIR, 'atmora_logo.png'))

    # Save small logo (64x64)
    logo_small = draw_logo(200).resize((64, 64), Image.LANCZOS)
    logo_small.save(os.path.join(BRANDING_DIR, 'atmora_logo_small.png'))

    # Save icon (48x48 for window icon — convert to RGB for ICO compatibility)
    logo_icon = draw_logo(200).resize((48, 48), Image.LANCZOS)
    logo_icon.save(os.path.join(BRANDING_DIR, 'atmora_icon.png'))
