#!/usr/bin/env python3
"""
OilExam.tech - Professional Reel Utilities
Shared module with all 2026 improvements:
- Safe zone compliance
- Arabic reshaping + BiDi
- Particle systems
- Motion typography (typewriter, bounce, kinetic)
- Smooth transitions (zoom, wipe, flash)
- Noise/grain texture
- Glassmorphism cards
- Branded intro/outro
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import arabic_reshaper
from bidi.algorithm import get_display
import math, random, os

WIDTH, HEIGHT = 1080, 1920
FPS = 30  # Upgraded from 24 to 30 for smoother motion

# ═══ SAFE ZONES (2026 Instagram) ═══
SAFE_TOP = 200       # Hook text starts here
SAFE_BOTTOM = 1600   # Nothing below this
SAFE_LEFT = 70
SAFE_RIGHT = 960     # Avoid right 120px (engagement icons)
SAFE_CENTER_X = WIDTH // 2
SAFE_WIDTH = SAFE_RIGHT - SAFE_LEFT

# ═══ BRAND COLORS ═══
PRIMARY    = (67, 97, 238)
MID_BLUE   = (90, 123, 245)
LIGHT_BLUE = (123, 147, 248)
PALE_BLUE  = (168, 186, 255)
DARK_BG    = (26, 35, 50)
DARKER_BG  = (18, 24, 38)
WHITE      = (255, 255, 255)
GREEN      = (72, 187, 120)
RED        = (229, 62, 62)
ORANGE     = (246, 173, 85)
PINK       = (237, 100, 166)
YELLOW     = (250, 204, 21)
GOLD       = (255, 215, 0)
TEAL       = (56, 178, 172)

# ═══ FONTS ═══
FONT_DIR = "/root/OilexamVideo/fonts"
AR_BLACK = f"{FONT_DIR}/Tajawal-Black.ttf"
AR_BOLD  = f"{FONT_DIR}/Tajawal-ExtraBold.ttf"
AR_REG   = f"{FONT_DIR}/Tajawal-Regular.ttf"
EN_BOLD  = f"{FONT_DIR}/PlusJakartaSans-Bold.ttf"
EN_REG   = f"{FONT_DIR}/PlusJakartaSans-Regular.ttf"


# ═══════════════════════════════════════════
#  ARABIC TEXT UTILITIES
# ═══════════════════════════════════════════

def ar(text):
    """Pass through Arabic text as-is. Tajawal font handles shaping natively."""
    return text


# ═══════════════════════════════════════════
#  EASING FUNCTIONS
# ═══════════════════════════════════════════

def ease_out(t):
    return 1 - (1 - min(1.0, t)) ** 3

def ease_in(t):
    t = min(1.0, max(0, t))
    return t * t * t

def ease_in_out(t):
    t = min(1.0, max(0, t))
    return 3*t*t - 2*t*t*t

def ease_out_back(t):
    """Overshoot bounce for pop-in effects."""
    t = min(1.0, max(0, t))
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * pow(t - 1, 3) + c1 * pow(t - 1, 2)

def ease_out_elastic(t):
    """Elastic bounce for dramatic reveals."""
    t = min(1.0, max(0, t))
    if t == 0 or t == 1:
        return t
    return pow(2, -10 * t) * math.sin((t * 10 - 0.75) * (2 * math.pi) / 3) + 1

def ease_out_bounce(t):
    t = min(1.0, max(0, t))
    if t < 1/2.75:
        return 7.5625 * t * t
    elif t < 2/2.75:
        t -= 1.5/2.75
        return 7.5625 * t * t + 0.75
    elif t < 2.5/2.75:
        t -= 2.25/2.75
        return 7.5625 * t * t + 0.9375
    else:
        t -= 2.625/2.75
        return 7.5625 * t * t + 0.984375


# ═══════════════════════════════════════════
#  COLOR UTILITIES
# ═══════════════════════════════════════════

def lerp_color(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))

def alpha_color(color, alpha):
    """Return color blended with DARK_BG at given alpha (0-1)."""
    return lerp_color(DARK_BG, color, alpha)

def brighten(color, factor=1.3):
    return tuple(min(255, int(c * factor)) for c in color)

def dim(color, factor=0.6):
    return tuple(int(c * factor) for c in color)


# ═══════════════════════════════════════════
#  BACKGROUND GENERATORS
# ═══════════════════════════════════════════

def gradient_bg(w, h, c1, c2):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = y / h
        color = tuple(int(c1[i]*(1-r) + c2[i]*r) for i in range(3))
        draw.line([(0, y), (w, y)], fill=color)
    return img

def brand_bg(dark_shift=0):
    c1 = tuple(max(0, c - dark_shift) for c in DARK_BG)
    c2 = tuple(max(0, min(255, c + 15 - dark_shift)) for c in DARK_BG)
    return gradient_bg(WIDTH, HEIGHT, c1, c2)

def radial_gradient(img, cx, cy, radius, center_color, edge_color):
    draw = ImageDraw.Draw(img)
    for r in range(radius, 0, -2):
        ratio = r / radius
        c = tuple(int(center_color[i]*(1-ratio) + edge_color[i]*ratio) for i in range(3))
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=c)


# ═══════════════════════════════════════════
#  NOISE / GRAIN TEXTURE
# ═══════════════════════════════════════════

_grain_cache = {}

def add_grain(img, intensity=15, seed=None):
    """Add subtle film grain texture for depth."""
    key = (img.size, intensity, seed)
    if key not in _grain_cache:
        w, h = img.size
        rng = random.Random(seed if seed else 42)
        grain = Image.new('RGB', (w // 4, h // 4))  # Low res for performance
        pixels = grain.load()
        for y in range(grain.height):
            for x in range(grain.width):
                v = rng.randint(-intensity, intensity)
                pixels[x, y] = (128 + v, 128 + v, 128 + v)
        grain = grain.resize((w, h), Image.NEAREST)
        _grain_cache[key] = grain

    grain = _grain_cache[key]
    from PIL import ImageChops
    # Soft light blend
    result = img.copy()
    rp = result.load()
    gp = grain.load()
    for y in range(0, img.height, 3):  # Skip rows for speed
        for x in range(0, img.width, 3):
            r, g, b = rp[x, y]
            gv = gp[x, y][0] - 128
            rp[x, y] = (
                max(0, min(255, r + gv)),
                max(0, min(255, g + gv)),
                max(0, min(255, b + gv))
            )
    return result


def add_grain_fast(img, intensity=12):
    """Fast grain - only add to every Nth pixel for speed."""
    result = img.copy()
    rp = result.load()
    w, h = img.size
    rng = random.Random(42)
    step = 4
    for y in range(0, h, step):
        for x in range(0, w, step):
            v = rng.randint(-intensity, intensity)
            r, g, b = rp[x, y]
            rp[x, y] = (max(0, min(255, r+v)), max(0, min(255, g+v)), max(0, min(255, b+v)))
    return result


# ═══════════════════════════════════════════
#  PARTICLE SYSTEM
# ═══════════════════════════════════════════

class Particle:
    def __init__(self, x, y, vx, vy, size, color, life):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.size = size
        self.color = color
        self.life = life
        self.max_life = life

def create_floating_particles(count=30, seed=123):
    """Create a set of floating ambient particles."""
    rng = random.Random(seed)
    particles = []
    for _ in range(count):
        particles.append(Particle(
            x=rng.randint(0, WIDTH),
            y=rng.randint(0, HEIGHT),
            vx=rng.uniform(-0.3, 0.3),
            vy=rng.uniform(-0.8, -0.1),
            size=rng.uniform(1.5, 4),
            color=rng.choice([PRIMARY, MID_BLUE, LIGHT_BLUE, PALE_BLUE, WHITE]),
            life=rng.uniform(0.5, 1.0)
        ))
    return particles

def draw_particles(draw, particles, p, alpha=0.7):
    """Draw floating particles at progress p."""
    for pt in particles:
        # Update position based on progress
        x = (pt.x + pt.vx * p * 500) % WIDTH
        y = (pt.y + pt.vy * p * 500) % HEIGHT
        # Pulsing opacity
        pulse = 0.5 + 0.5 * math.sin(p * 8 + pt.x * 0.01)
        a = alpha * pulse * pt.life
        size = pt.size * (0.8 + 0.2 * pulse)
        c = lerp_color(DARK_BG, pt.color, a)
        draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=c)


def draw_sparkle_burst(draw, cx, cy, p, count=12, max_radius=150, color=GOLD):
    """Draw an expanding sparkle burst effect."""
    if p <= 0:
        return
    rng = random.Random(int(cx + cy))
    for i in range(count):
        angle = rng.uniform(0, 2 * math.pi)
        speed = rng.uniform(0.5, 1.0)
        r = max_radius * ease_out(p) * speed
        size = max(1, 4 * (1 - p))  # Shrink as they expand
        x = cx + math.cos(angle) * r
        y = cy + math.sin(angle) * r
        a = max(0, 1 - p)
        c = lerp_color(DARK_BG, color, a)
        draw.ellipse([(x-size, y-size), (x+size, y+size)], fill=c)


# ═══════════════════════════════════════════
#  TEXT RENDERING (Safe Zone Aware)
# ═══════════════════════════════════════════

def center_text(draw, text, y, font, fill=WHITE):
    """Center text horizontally within safe zone."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]

def center_text_ar(draw, text, y, font, fill=WHITE):
    """Center Arabic text with proper reshaping."""
    bidi_text = ar(text)
    return center_text(draw, bidi_text, y, font, fill)

def text_shadow(draw, text, x, y, font, fill=WHITE, shadow_color=(0,0,0), offset=4):
    """Draw text with drop shadow."""
    draw.text((x+offset, y+offset), text, font=font, fill=shadow_color)
    draw.text((x, y), text, font=font, fill=fill)

def center_text_shadow(draw, text, y, font, fill=WHITE, shadow_offset=4):
    """Center text with drop shadow."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x+shadow_offset, y+shadow_offset), text, font=font, fill=(0,0,0))
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]

def center_text_ar_shadow(draw, text, y, font, fill=WHITE, shadow_offset=4):
    """Center Arabic text with shadow."""
    bidi_text = ar(text)
    return center_text_shadow(draw, bidi_text, y, font, fill, shadow_offset)


# ═══════════════════════════════════════════
#  MOTION TYPOGRAPHY
# ═══════════════════════════════════════════

def typewriter_text(draw, text, y, font, fill, p, chars_per_sec=15):
    """Typewriter effect - letters appear one by one."""
    total_chars = len(text)
    visible = int(total_chars * min(1, p * chars_per_sec / total_chars))
    partial = text[:visible]
    if partial:
        center_text(draw, partial, y, font, fill)
    # Blinking cursor
    if p < 1.0 and int(p * 8) % 2 == 0:
        bbox = draw.textbbox((0, 0), partial + "|", font=font)
        tw = bbox[2] - bbox[0]
        cx = (WIDTH + tw) // 2
        draw.text((cx - 10, y), "|", font=font, fill=fill)

def bounce_text(draw, text, y_target, font, fill, p):
    """Text pops in oversized then bounces to final size. Returns the y used."""
    e = ease_out_back(min(1, p * 2.5))
    # Scale simulation via y offset (overshoot then settle)
    y_offset = int((1 - e) * 80)
    y = y_target - y_offset
    if e > 0.05:
        alpha = min(1, e * 2)
        c = lerp_color(DARK_BG, fill, alpha)
        center_text(draw, text, y, font, c)
    return y

def bounce_text_ar(draw, text, y_target, font, fill, p):
    """Arabic bounce text."""
    bidi_text = ar(text)
    return bounce_text(draw, bidi_text, y_target, font, fill, p)

def slide_in_right(draw, text, y, font, fill, p, distance=400):
    """Text slides in from right side."""
    e = ease_out(min(1, p * 3))
    x_offset = int((1 - e) * distance)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2 + x_offset
    alpha = min(1, e * 2)
    c = lerp_color(DARK_BG, fill, alpha)
    draw.text((x, y), text, font=font, fill=c)

def slide_in_left(draw, text, y, font, fill, p, distance=400):
    """Text slides in from left side."""
    e = ease_out(min(1, p * 3))
    x_offset = int((1 - e) * -distance)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2 + x_offset
    alpha = min(1, e * 2)
    c = lerp_color(DARK_BG, fill, alpha)
    draw.text((x, y), text, font=font, fill=c)

def scale_fade_in(draw, text, y, font, fill, p):
    """Fade in with subtle scale effect."""
    e = ease_out(min(1, p * 3))
    alpha = min(1, e * 1.5)
    c = lerp_color(DARK_BG, fill, alpha)
    y_adj = y + int((1 - e) * 30)
    center_text(draw, text, y_adj, font, c)


# ═══════════════════════════════════════════
#  GLASSMORPHISM CARD
# ═══════════════════════════════════════════

def draw_glass_card(draw, x1, y1, x2, y2, radius=24, opacity=0.15, border_color=None, accent_color=None):
    """Draw a glassmorphism-style card (frosted glass look)."""
    # Semi-transparent card
    card_color = lerp_color(DARK_BG, WHITE, opacity)
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius, fill=card_color)

    # Subtle inner border (top and left = lighter)
    if border_color is None:
        border_color = lerp_color(DARK_BG, WHITE, 0.08)
    draw.rounded_rectangle([(x1, y1), (x2, y2)], radius=radius,
                           outline=border_color, width=1)

    # Top accent line
    if accent_color:
        draw.rounded_rectangle([(x1+2, y1+2), (x2-2, y1+6)],
                               radius=3, fill=accent_color)

    # Subtle highlight on top edge
    highlight = lerp_color(card_color, WHITE, 0.1)
    draw.line([(x1+radius, y1+1), (x2-radius, y1+1)], fill=highlight, width=1)


# ═══════════════════════════════════════════
#  BRANDED INTRO / OUTRO
# ═══════════════════════════════════════════

def branded_intro(p):
    """Professional 2-second branded intro animation."""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARKER_BG)
    draw = ImageDraw.Draw(img)

    e = ease_out_back(min(1, p * 2.5))

    # Central glow
    glow_r = int(350 * e)
    if glow_r > 5:
        radial_gradient(img, WIDTH//2, HEIGHT//2-100, glow_r,
                        lerp_color(DARKER_BG, PRIMARY, 0.25), DARKER_BG)
        draw = ImageDraw.Draw(img)

    # Logo text with bounce
    f_brand = ImageFont.truetype(EN_BOLD, 96)
    f_dot = ImageFont.truetype(EN_BOLD, 96)

    if e > 0.1:
        # "OilExam" with shadow
        brand = "OilExam"
        bbox = draw.textbbox((0, 0), brand, font=f_brand)
        tw = bbox[2] - bbox[0]
        bx = (WIDTH - tw) // 2 - 40
        by = HEIGHT//2 - 150 - int((1-e)*60)

        # Shadow
        draw.text((bx+4, by+4), brand, font=f_brand, fill=(0,0,0))
        draw.text((bx, by), brand, font=f_brand, fill=WHITE)

        # ".tech" in brand color
        dot_text = ".tech"
        draw.text((bx + tw + 5, by+4), dot_text, font=f_dot, fill=(0,0,0))
        draw.text((bx + tw + 1, by), dot_text, font=f_dot, fill=PRIMARY)

    # Animated line under brand
    if p > 0.3:
        line_e = ease_out((p - 0.3) * 4)
        lw = int(500 * line_e)
        ly = HEIGHT//2 - 20
        # Gradient line
        for i in range(lw):
            ratio = i / max(lw, 1)
            c = lerp_color(PRIMARY, MID_BLUE, ratio)
            x = WIDTH//2 - lw//2 + i
            draw.line([(x, ly), (x, ly+3)], fill=c)

    # Tagline
    if p > 0.45:
        a = min(1, (p - 0.45) * 4)
        f_tag = ImageFont.truetype(AR_BOLD, 44)
        c = lerp_color(DARKER_BG, PALE_BLUE, a)
        center_text_ar(draw, "أتقن اختبارك بكل سهولة", HEIGHT//2 + 30, f_tag, c)

    # Powered by
    if p > 0.6:
        a = min(1, (p - 0.6) * 4)
        f_small = ImageFont.truetype(EN_REG, 28)
        c = lerp_color(DARKER_BG, (60, 75, 100), a)
        center_text(draw, "Powered by Trimind Company", SAFE_BOTTOM - 40, f_small, c)

    # Particles
    particles = create_floating_particles(15, seed=99)
    draw_particles(draw, particles, p, alpha=0.4)

    return img


def branded_outro(p, extra_text=""):
    """Professional CTA outro with pulsing button."""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(AR_BLACK, 78)
    f_brand = ImageFont.truetype(EN_BOLD, 72)
    f_btn = ImageFont.truetype(AR_BLACK, 48)
    f_ar = ImageFont.truetype(AR_BOLD, 42)
    f_small = ImageFont.truetype(EN_REG, 30)

    e = ease_out(p * 3)
    pulse = 0.88 + 0.12 * math.sin(p * 12)

    # Background glow
    radial_gradient(img, WIDTH//2, 500, int(320*e), lerp_color(DARK_BG, PRIMARY, 0.2), DARK_BG)
    draw = ImageDraw.Draw(img)

    # Main CTA text
    bounce_text_ar(draw, "لا تطوّف!", SAFE_TOP + 120, f_huge, WHITE, p)

    if p > 0.1:
        bounce_text_ar(draw, "سجّل الحين!", SAFE_TOP + 250, f_huge, PRIMARY, p - 0.1)

    # Brand
    if p > 0.2:
        a = min(1, (p-0.2)*4)
        center_text_shadow(draw, "oilexam.tech", SAFE_TOP + 420, f_brand,
                          lerp_color(DARK_BG, WHITE, a))

    # Pulsing CTA button
    if p > 0.3:
        bw, bh = 700, 120
        bx, by = (WIDTH-bw)//2, SAFE_TOP + 560
        # Outer glow
        glow_c = tuple(int(c * pulse * 0.6) for c in PRIMARY)
        draw.rounded_rectangle([(bx-8, by-8), (bx+bw+8, by+bh+8)],
                               radius=64, fill=glow_c)
        # Button
        btn_c = tuple(int(c * pulse) for c in PRIMARY)
        draw.rounded_rectangle([(bx, by), (bx+bw, by+bh)],
                               radius=60, fill=btn_c)
        # Highlight on top
        draw.rounded_rectangle([(bx+4, by+4), (bx+bw-4, by+bh//2)],
                               radius=56, fill=lerp_color(btn_c, WHITE, 0.08))
        center_text_ar(draw, "اشترك الحين", by + 28, f_btn, WHITE)

    # Feature list
    if p > 0.45:
        items = ["اختبارات تفاعلية", "بطاقات إنجليزي-عربي", "تتبع تقدّمك", "نتائج فورية"]
        for i, item in enumerate(items):
            th = 0.45 + i * 0.07
            if p > th:
                a = min(1, (p-th)*5)
                y = SAFE_TOP + 760 + i * 80
                c_dot = lerp_color(DARK_BG, GREEN, a)
                c_txt = lerp_color(DARK_BG, WHITE, a)
                f_check = ImageFont.truetype(AR_BOLD, 38)
                draw.text((220, y), "✓", font=f_check, fill=c_dot)
                draw.text((280, y), ar(item), font=f_check, fill=c_txt)

    # Bio link
    if p > 0.7:
        a = min(1, (p-0.7)*4)
        c = lerp_color(DARK_BG, ORANGE, a)
        center_text_ar(draw, "الرابط بالبايو", SAFE_BOTTOM - 120, f_ar, c)

    # Powered by
    if p > 0.75:
        a = min(1, (p-0.75)*4)
        c = lerp_color(DARK_BG, (70, 85, 110), a)
        center_text(draw, "Powered by Trimind Company", SAFE_BOTTOM - 40, f_small, c)

    # Particles
    particles = create_floating_particles(20, seed=77)
    draw_particles(draw, particles, p, alpha=0.3)

    return img


# ═══════════════════════════════════════════
#  TRANSITIONS
# ═══════════════════════════════════════════

def transition_flash(img1_func, img2_func, p, flash_color=WHITE):
    """White/color flash transition between two scenes."""
    if p < 0.4:
        return img1_func(0.8 + p * 0.5)
    elif p < 0.55:
        # Flash
        flash_p = (p - 0.4) / 0.15
        img = img2_func(0.0)
        overlay = Image.new('RGB', (WIDTH, HEIGHT), flash_color)
        alpha = 1 - flash_p
        return Image.blend(img, overlay, alpha)
    else:
        return img2_func((p - 0.55) / 0.45)


def transition_zoom(img_func_out, img_func_in, p):
    """Zoom-in transition between scenes."""
    if p < 0.45:
        return img_func_out(0.7 + p * 0.6)
    elif p < 0.55:
        # Brief flash
        flash_p = (p - 0.45) / 0.1
        img = brand_bg()
        draw = ImageDraw.Draw(img)
        radial_gradient(img, WIDTH//2, HEIGHT//2, int(600*(1-flash_p)),
                        lerp_color(DARK_BG, PRIMARY, 0.5), DARK_BG)
        return img
    else:
        return img_func_in((p - 0.55) / 0.45)


# ═══════════════════════════════════════════
#  DECORATIVE ELEMENTS
# ═══════════════════════════════════════════

def draw_corner_accents(draw, p, color=PRIMARY, size=60):
    """Draw animated corner accent lines."""
    e = ease_out(min(1, p * 3))
    s = int(size * e)
    w = 3
    a = min(1, e)
    c = lerp_color(DARK_BG, color, a * 0.5)

    # Top-left
    draw.line([(SAFE_LEFT, SAFE_TOP), (SAFE_LEFT + s, SAFE_TOP)], fill=c, width=w)
    draw.line([(SAFE_LEFT, SAFE_TOP), (SAFE_LEFT, SAFE_TOP + s)], fill=c, width=w)

    # Top-right
    draw.line([(SAFE_RIGHT, SAFE_TOP), (SAFE_RIGHT - s, SAFE_TOP)], fill=c, width=w)
    draw.line([(SAFE_RIGHT, SAFE_TOP), (SAFE_RIGHT, SAFE_TOP + s)], fill=c, width=w)

    # Bottom-left
    draw.line([(SAFE_LEFT, SAFE_BOTTOM), (SAFE_LEFT + s, SAFE_BOTTOM)], fill=c, width=w)
    draw.line([(SAFE_LEFT, SAFE_BOTTOM), (SAFE_LEFT, SAFE_BOTTOM - s)], fill=c, width=w)

    # Bottom-right
    draw.line([(SAFE_RIGHT, SAFE_BOTTOM), (SAFE_RIGHT - s, SAFE_BOTTOM)], fill=c, width=w)
    draw.line([(SAFE_RIGHT, SAFE_BOTTOM), (SAFE_RIGHT, SAFE_BOTTOM - s)], fill=c, width=w)


def draw_progress_dots(draw, y, current, total, active_color=PRIMARY, inactive_color=None):
    """Draw navigation dots at the bottom."""
    if inactive_color is None:
        inactive_color = (40, 52, 72)
    spacing = 40
    start_x = WIDTH//2 - (total * spacing) // 2
    for i in range(total):
        x = start_x + i * spacing
        if i <= current:
            draw.ellipse([(x-6, y-6), (x+6, y+6)], fill=active_color)
        else:
            draw.ellipse([(x-4, y-4), (x+4, y+4)], fill=inactive_color)


def draw_gradient_line(draw, y, width, color1, color2, thickness=3):
    """Draw a horizontal gradient line centered."""
    x_start = (WIDTH - width) // 2
    for i in range(width):
        ratio = i / max(width, 1)
        c = lerp_color(color1, color2, ratio)
        draw.line([(x_start + i, y), (x_start + i, y + thickness)], fill=c)


# ═══════════════════════════════════════════
#  VIDEO BUILD UTILITIES
# ═══════════════════════════════════════════

import subprocess, tempfile, shutil

def render_scene(func, dur, frame_dir, start_idx):
    n = int(dur * FPS)
    for i in range(n):
        p = i / n
        img = func(p)
        img.save(os.path.join(frame_dir, f"frame_{start_idx+i:05d}.png"))
    return start_idx + n

def encode_video(frame_dir, output):
    subprocess.run([
        "ffmpeg", "-y", "-framerate", str(FPS),
        "-i", os.path.join(frame_dir, "frame_%05d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-preset", "medium", "-crf", "18",
        "-movflags", "+faststart", output
    ], check=True, capture_output=True)

def build_video(name, scenes, output):
    print(f"\n{'='*55}")
    print(f"  Building: {name}")
    print(f"{'='*55}")
    frame_dir = tempfile.mkdtemp(prefix=f"pro_{name}_")
    idx = 0
    total_dur = 0
    for sname, func, dur in scenes:
        print(f"  > {sname} ({dur}s)...")
        idx = render_scene(func, dur, frame_dir, idx)
        total_dur += dur
    print(f"  Total: {idx} frames / {total_dur:.1f}s @ {FPS}fps")
    print(f"  Encoding MP4...")
    encode_video(frame_dir, output)
    shutil.rmtree(frame_dir)
    size = os.path.getsize(output) / (1024*1024)
    print(f"  Done: {output} ({size:.1f} MB)")
