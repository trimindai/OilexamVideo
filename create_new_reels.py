#!/usr/bin/env python3
"""
OilExam.tech - 2 New Instagram Reels
Reel 4: "Before vs After" - Split-screen transformation
Reel 5: "Countdown Timer" - Exam is coming urgency
"""

from PIL import Image, ImageDraw, ImageFont
import subprocess, os, math, tempfile, shutil

WIDTH, HEIGHT = 1080, 1920
FPS = 24

# ═══ BRAND COLORS ═══
PRIMARY    = (67, 97, 238)       # #4361EE
MID_BLUE   = (90, 123, 245)
LIGHT_BLUE = (123, 147, 248)
PALE_BLUE  = (168, 186, 255)
DARK_BG    = (26, 35, 50)
WHITE      = (255, 255, 255)
GREEN      = (72, 187, 120)
RED        = (229, 62, 62)
ORANGE     = (246, 173, 85)
PINK       = (237, 100, 166)
DARK_RED   = (120, 30, 30)
YELLOW     = (250, 204, 21)

# ═══ FONTS ═══
FONT_DIR  = "/root/OilexamVideo/fonts"
AR_BLACK  = f"{FONT_DIR}/Tajawal-Black.ttf"
AR_BOLD   = f"{FONT_DIR}/Tajawal-ExtraBold.ttf"
AR_REG    = f"{FONT_DIR}/Tajawal-Regular.ttf"
EN_BOLD   = f"{FONT_DIR}/PlusJakartaSans-Bold.ttf"
EN_REG    = f"{FONT_DIR}/PlusJakartaSans-Regular.ttf"


# ═══ UTILITIES ═══

def gradient_bg(w, h, c1, c2):
    img = Image.new('RGB', (w, h))
    draw = ImageDraw.Draw(img)
    for y in range(h):
        r = y / h
        color = tuple(int(c1[i]*(1-r) + c2[i]*r) for i in range(3))
        draw.line([(0, y), (w, y)], fill=color)
    return img


def radial_gradient(img, cx, cy, radius, center_color, edge_color):
    draw = ImageDraw.Draw(img)
    for r in range(radius, 0, -2):
        ratio = r / radius
        c = tuple(int(center_color[i]*(1-ratio) + edge_color[i]*ratio) for i in range(3))
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=c)


def center_text(draw, text, y, font, fill=WHITE):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = (WIDTH - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)
    return bbox[3] - bbox[1]


def center_text_in_region(draw, text, x1, x2, y, font, fill=WHITE):
    """Center text within a horizontal region."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    x = x1 + (x2 - x1 - tw) // 2
    draw.text((x, y), text, font=font, fill=fill)


def ease_out(t):
    return 1 - (1 - min(1.0, t)) ** 3


def ease_in_out(t):
    t = min(1.0, t)
    return 3*t*t - 2*t*t*t


def lerp_color(c1, c2, t):
    t = max(0, min(1, t))
    return tuple(int(c1[i]*(1-t) + c2[i]*t) for i in range(3))


def brand_bg(dark_shift=0):
    c1 = tuple(max(0, c - dark_shift) for c in DARK_BG)
    c2 = tuple(max(0, min(255, c + 15 - dark_shift)) for c in DARK_BG)
    return gradient_bg(WIDTH, HEIGHT, c1, c2)


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
        "-preset", "medium", "-crf", "20",
        "-movflags", "+faststart", output
    ], check=True, capture_output=True)


def build_video(name, scenes, output):
    print(f"\n{'='*55}")
    print(f"  Building: {name}")
    print(f"{'='*55}")
    frame_dir = tempfile.mkdtemp(prefix=f"reel_{name}_")
    idx = 0
    total_dur = 0
    for sname, func, dur in scenes:
        print(f"  > {sname} ({dur}s)...")
        idx = render_scene(func, dur, frame_dir, idx)
        total_dur += dur
    print(f"  Total: {idx} frames / {total_dur}s")
    print(f"  Encoding MP4...")
    encode_video(frame_dir, output)
    shutil.rmtree(frame_dir)
    size = os.path.getsize(output) / (1024*1024)
    print(f"  Done: {output} ({size:.1f} MB)")


# ════════════════════════════════════════════════════════════════
#  REEL 4: "Before vs After" - قبل وبعد OilExam
#  Concept: Left side = red/dark (struggle), Right side = green/bright (success)
#  Then the "after" side takes over the whole screen
# ════════════════════════════════════════════════════════════════

def r4_hook(p):
    """Hook: Split screen teaser - قبل و بعد"""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARK_BG)
    draw = ImageDraw.Draw(img)
    e = ease_out(p * 3)

    # Animated diagonal split line
    split_x = WIDTH // 2
    angle_offset = int(40 * math.sin(p * 6))

    # Left side - dark red gradient
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        c = lerp_color((40, 15, 15), (80, 25, 30), ratio)
        draw.line([(0, y), (split_x + angle_offset, y)], fill=c)

    # Right side - dark green/blue gradient
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        c = lerp_color((15, 35, 30), (20, 55, 50), ratio)
        draw.line([(split_x + angle_offset, y), (WIDTH, y)], fill=c)

    # Divider line with glow
    for dx in range(-6, 7):
        intensity = max(0, 1 - abs(dx) / 6)
        c = lerp_color(DARK_BG, WHITE, intensity * 0.8 * e)
        draw.line([(split_x + angle_offset + dx, 0),
                   (split_x + angle_offset + dx, HEIGHT)], fill=c)

    f_ar = ImageFont.truetype(AR_BLACK, 90)
    f_ar2 = ImageFont.truetype(AR_BLACK, 75)
    f_vs = ImageFont.truetype(EN_BOLD, 60)

    if e > 0.2:
        # "Before" on left
        center_text_in_region(draw, "قبل", 0, split_x, int(750 + (1-e)*80), f_ar, RED)
        # "After" on right
        center_text_in_region(draw, "بعد", split_x, WIDTH, int(750 + (1-e)*80), f_ar, GREEN)

    if e > 0.5:
        # VS in the middle
        bbox = draw.textbbox((0, 0), "VS", font=f_vs)
        tw = bbox[2] - bbox[0]
        draw.text((split_x + angle_offset - tw//2, 920), "VS", font=f_vs, fill=YELLOW)

    if p > 0.5:
        a = min(1, (p - 0.5) * 4)
        c = lerp_color(DARK_BG, WHITE, a)
        center_text(draw, "OilExam.tech", int(1150), f_ar2, c)

    if p > 0.7:
        f_sub = ImageFont.truetype(AR_REG, 44)
        a = min(1, (p - 0.7) * 4)
        c = lerp_color(DARK_BG, PALE_BLUE, a)
        center_text(draw, "شوف الفرق بنفسك", 1300, f_sub, c)

    return img


def r4_before(p):
    """Before OilExam - The struggle side"""
    # Dark reddish background
    img = gradient_bg(WIDTH, HEIGHT, (35, 15, 15), (55, 22, 25))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(AR_BLACK, 70)
    f_body = ImageFont.truetype(AR_BOLD, 48)
    f_icon = ImageFont.truetype(EN_BOLD, 48)

    e = ease_out(p * 2.5)

    # Red glow at top
    radial_gradient(img, WIDTH//2, 200, int(200*e), (100, 30, 30), (35, 15, 15))
    draw = ImageDraw.Draw(img)

    center_text(draw, "قبل OilExam", 200, f_title, RED)

    if p > 0.08:
        lw = int(400 * min(1, (p - 0.08) * 5))
        draw.line([(WIDTH//2 - lw//2, 300), (WIDTH//2 + lw//2, 300)], fill=RED, width=3)

    struggles = [
        ("تدرس بدون خطة واضحة", "X"),
        ("ما تعرف مستواك الحقيقي", "X"),
        ("تضيّع وقت على مواد قديمة", "X"),
        ("توتر وقلق قبل الاختبار", "X"),
        ("نتيجة أقل من المطلوب", "X"),
    ]

    for i, (text, icon) in enumerate(struggles):
        th = i * 0.13 + 0.12
        if p > th:
            a = min(1, (p - th) * 5)
            ep = ease_out((p - th) * 3)
            y = 400 + i * 200

            xo = int((1 - ep) * 250)

            # Card background
            card_bg = lerp_color((35, 15, 15), (60, 25, 28), a)
            draw.rounded_rectangle([(60 + xo, y), (WIDTH - 60, y + 150)],
                                   radius=18, fill=card_bg)

            # Red accent bar on right
            draw.rounded_rectangle([(WIDTH - 75, y + 15), (WIDTH - 60, y + 135)],
                                   radius=6, fill=lerp_color((35, 15, 15), RED, a))

            # X icon circle
            icon_c = lerp_color((35, 15, 15), RED, a)
            draw.ellipse([(90 + xo, y + 35), (160 + xo, y + 105)], fill=icon_c)
            # X mark
            cx_i, cy_i = 125 + xo, y + 70
            xc = lerp_color((35, 15, 15), WHITE, a)
            draw.line([(cx_i - 14, cy_i - 14), (cx_i + 14, cy_i + 14)], fill=xc, width=3)
            draw.line([(cx_i - 14, cy_i + 14), (cx_i + 14, cy_i - 14)], fill=xc, width=3)

            # Text
            text_c = lerp_color((35, 15, 15), WHITE, a)
            bb = draw.textbbox((0, 0), text, font=f_body)
            tw = bb[2] - bb[0]
            draw.text((WIDTH - 100 - tw + xo, y + 42), text, font=f_body, fill=text_c)

    # Sad emoji at bottom
    if p > 0.85:
        f_sad = ImageFont.truetype(AR_BLACK, 80)
        a = min(1, (p - 0.85) * 6)
        c = lerp_color((35, 15, 15), RED, a)
        center_text(draw, "النتيجة: رسوب", 1500, f_sad, c)

    return img


def r4_transition(p):
    """Dramatic transition - wipe from red to green"""
    img = Image.new('RGB', (WIDTH, HEIGHT))
    draw = ImageDraw.Draw(img)

    e = ease_in_out(p)
    wipe_x = int(WIDTH * e)

    # Left: green side (revealed)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        c = lerp_color((15, 40, 35), (20, 60, 50), ratio)
        if wipe_x > 0:
            draw.line([(0, y), (min(wipe_x, WIDTH), y)], fill=c)

    # Right: red side (being wiped away)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        c = lerp_color((35, 15, 15), (55, 22, 25), ratio)
        if wipe_x < WIDTH:
            draw.line([(wipe_x, y), (WIDTH, y)], fill=c)

    # Bright wipe edge
    for dx in range(-15, 16):
        x = wipe_x + dx
        if 0 <= x < WIDTH:
            intensity = max(0, 1 - abs(dx) / 15)
            c = lerp_color(DARK_BG, PRIMARY, intensity)
            draw.line([(x, 0), (x, HEIGHT)], fill=c)

    f_ar = ImageFont.truetype(AR_BLACK, 100)
    if 0.3 < p < 0.8:
        a = min(1, (p - 0.3) * 4) * min(1, (0.8 - p) * 4)
        c = lerp_color(DARK_BG, WHITE, a)
        center_text(draw, "الحين مع", HEIGHT // 2 - 100, f_ar, c)

    f_brand = ImageFont.truetype(EN_BOLD, 90)
    if p > 0.5:
        a = min(1, (p - 0.5) * 3)
        c = lerp_color(DARK_BG, PRIMARY, a)
        center_text(draw, "OilExam", HEIGHT // 2 + 40, f_brand, c)

    return img


def r4_after(p):
    """After OilExam - The success side"""
    img = gradient_bg(WIDTH, HEIGHT, (15, 35, 30), (20, 55, 50))
    draw = ImageDraw.Draw(img)

    f_title = ImageFont.truetype(AR_BLACK, 70)
    f_body = ImageFont.truetype(AR_BOLD, 48)

    e = ease_out(p * 2.5)

    # Green glow at top
    radial_gradient(img, WIDTH//2, 200, int(200*e), (30, 90, 60), (15, 35, 30))
    draw = ImageDraw.Draw(img)

    center_text(draw, "بعد OilExam", 200, f_title, GREEN)

    if p > 0.08:
        lw = int(400 * min(1, (p - 0.08) * 5))
        draw.line([(WIDTH//2 - lw//2, 300), (WIDTH//2 + lw//2, 300)], fill=GREEN, width=3)

    benefits = [
        "خطة دراسية واضحة ومنظمة",
        "تعرف مستواك بالضبط",
        "مواد محدّثة ومركّزة",
        "ثقة كاملة يوم الاختبار",
        "نتيجة تفتح لك الباب",
    ]

    for i, text in enumerate(benefits):
        th = i * 0.13 + 0.12
        if p > th:
            a = min(1, (p - th) * 5)
            ep = ease_out((p - th) * 3)
            y = 400 + i * 200

            xo = int((1 - ep) * 250)

            # Card background
            card_bg = lerp_color((15, 35, 30), (25, 50, 45), a)
            draw.rounded_rectangle([(60 + xo, y), (WIDTH - 60, y + 150)],
                                   radius=18, fill=card_bg)

            # Green accent bar on right
            draw.rounded_rectangle([(WIDTH - 75, y + 15), (WIDTH - 60, y + 135)],
                                   radius=6, fill=lerp_color((15, 35, 30), GREEN, a))

            # Checkmark circle
            icon_c = lerp_color((15, 35, 30), GREEN, a)
            draw.ellipse([(90 + xo, y + 35), (160 + xo, y + 105)], fill=icon_c)
            # Checkmark
            cx_i, cy_i = 125 + xo, y + 70
            xc = lerp_color((15, 35, 30), WHITE, a)
            draw.line([(cx_i - 16, cy_i), (cx_i - 4, cy_i + 14)], fill=xc, width=3)
            draw.line([(cx_i - 4, cy_i + 14), (cx_i + 16, cy_i - 10)], fill=xc, width=3)

            # Text
            text_c = lerp_color((15, 35, 30), WHITE, a)
            bb = draw.textbbox((0, 0), text, font=f_body)
            tw = bb[2] - bb[0]
            draw.text((WIDTH - 100 - tw + xo, y + 42), text, font=f_body, fill=text_c)

    if p > 0.85:
        f_pass = ImageFont.truetype(AR_BLACK, 80)
        a = min(1, (p - 0.85) * 6)
        c = lerp_color((15, 35, 30), GREEN, a)
        center_text(draw, "النتيجة: نجاح", 1500, f_pass, c)

    return img


def r4_cta(p):
    """CTA for Before/After reel"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(AR_BLACK, 85)
    f_brand = ImageFont.truetype(EN_BOLD, 72)
    f_btn = ImageFont.truetype(AR_BLACK, 50)
    f_ar = ImageFont.truetype(AR_BOLD, 42)
    f_small = ImageFont.truetype(EN_REG, 32)

    e = ease_out(p * 3)
    pulse = 0.88 + 0.12 * math.sin(p * 10)

    radial_gradient(img, WIDTH//2, 450, int(300*e), (35, 55, 85), DARK_BG)
    draw = ImageDraw.Draw(img)

    center_text(draw, "غيّر نتيجتك", int(280 + (1-e)*80), f_huge, WHITE)

    if p > 0.12:
        center_text(draw, "!اليوم مو باچر", 420, f_huge, GREEN)

    if p > 0.25:
        center_text(draw, "oilexam.tech", 600, f_brand, PRIMARY)

    if p > 0.35:
        bw, bh = 720, 130
        bx, by = (WIDTH - bw) // 2, 750
        btn_color = tuple(int(c * pulse) for c in GREEN)
        draw.rounded_rectangle([(bx-4, by-4), (bx+bw+4, by+bh+4)],
                               radius=65, fill=btn_color)
        draw.rounded_rectangle([(bx, by), (bx+bw, by+bh)],
                               radius=62, fill=GREEN)
        center_text(draw, "ابدأ الحين", by + 30, f_btn, WHITE)

    if p > 0.5:
        items = ["525+ سؤال وتمرين", "بطاقات تعليمية", "تتبع مستواك", "نتائج فورية"]
        for i, item in enumerate(items):
            th = 0.5 + i * 0.07
            if p > th:
                a = min(1, (p - th) * 5)
                y = 980 + i * 80
                c_dot = lerp_color(DARK_BG, GREEN, a)
                c_txt = lerp_color(DARK_BG, WHITE, a)
                draw.text((280, y), "✓", font=f_ar, fill=c_dot)
                draw.text((340, y), item, font=f_ar, fill=c_txt)

    if p > 0.7:
        center_text(draw, "الرابط بالبايو", 1400, f_ar, ORANGE)
        center_text(draw, "Powered by Trimind Company", 1650, f_small, (80, 95, 120))

    return img


# ════════════════════════════════════════════════════════════════
#  REEL 5: "Countdown Timer" - اختبارك قرّب!
#  Concept: Ticking clock, days counting down, what can you learn
#  in each category before the exam
# ════════════════════════════════════════════════════════════════

def r5_hook(p):
    """Hook: Ticking clock - اختبارك قرّب"""
    img = Image.new('RGB', (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)

    e = ease_out(p * 3)

    # Animated clock circle
    cx, cy = WIDTH // 2, HEIGHT // 2 - 200
    clock_r = int(280 * e)

    if clock_r > 10:
        # Outer ring
        draw.ellipse([(cx - clock_r, cy - clock_r),
                      (cx + clock_r, cy + clock_r)],
                     outline=PRIMARY, width=8)

        # Inner ring
        inner_r = clock_r - 20
        if inner_r > 10:
            draw.ellipse([(cx - inner_r, cy - inner_r),
                          (cx + inner_r, cy + inner_r)],
                         outline=MID_BLUE, width=3)

        # Clock hand - rotating
        angle = -math.pi/2 + p * 2 * math.pi * 3  # 3 rotations
        hand_len = clock_r - 40
        hx = cx + int(math.cos(angle) * hand_len)
        hy = cy + int(math.sin(angle) * hand_len)
        draw.line([(cx, cy), (hx, hy)], fill=RED, width=5)

        # Center dot
        draw.ellipse([(cx - 10, cy - 10), (cx + 10, cy + 10)], fill=RED)

        # Tick marks
        for i in range(12):
            tick_angle = -math.pi/2 + (i / 12) * 2 * math.pi
            t_inner = clock_r - 35
            t_outer = clock_r - 10
            x1 = cx + int(math.cos(tick_angle) * t_inner)
            y1 = cy + int(math.sin(tick_angle) * t_inner)
            x2 = cx + int(math.cos(tick_angle) * t_outer)
            y2 = cy + int(math.sin(tick_angle) * t_outer)
            w = 4 if i % 3 == 0 else 2
            draw.line([(x1, y1), (x2, y2)], fill=WHITE, width=w)

    f_ar = ImageFont.truetype(AR_BLACK, 90)
    f_ar2 = ImageFont.truetype(AR_BLACK, 70)

    if e > 0.3:
        center_text(draw, "اختبارك قرّب", cy + clock_r + 80, f_ar, WHITE)

    if p > 0.4:
        a = min(1, (p - 0.4) * 4)
        c = lerp_color((0, 0, 0), RED, a)
        center_text(draw, "!الوقت يمشي", cy + clock_r + 200, f_ar2, c)

    if p > 0.65:
        f_sub = ImageFont.truetype(AR_REG, 44)
        a = min(1, (p - 0.65) * 4)
        c = lerp_color((0, 0, 0), PALE_BLUE, a)
        center_text(draw, "بس لا تشيل هم...", 1550, f_sub, c)

    return img


def r5_days_left(p):
    """Countdown numbers - dramatic day counter"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_num = ImageFont.truetype(EN_BOLD, 280)
    f_ar = ImageFont.truetype(AR_BLACK, 60)
    f_sub = ImageFont.truetype(AR_BOLD, 48)

    e = ease_out(p * 2)

    # Show countdown from 30 to a target number
    # Animate through numbers
    if p < 0.6:
        # Counting down phase
        num = max(7, int(30 - 23 * (p / 0.6)))
        num_str = str(num)
        scale = 1 + 0.05 * math.sin(p * 40)  # Tick effect
    else:
        num_str = "7"
        scale = 1

    # Big glow behind number
    glow_c = RED if int(num_str) > 14 else ORANGE if int(num_str) > 7 else PRIMARY
    radial_gradient(img, WIDTH//2, HEIGHT//2 - 250, int(320 * e),
                    lerp_color(DARK_BG, glow_c, 0.3), DARK_BG)
    draw = ImageDraw.Draw(img)

    # Number
    font_size = int(280 * scale)
    f_dynamic = ImageFont.truetype(EN_BOLD, max(100, font_size))
    nb = draw.textbbox((0, 0), num_str, font=f_dynamic)
    nw = nb[2] - nb[0]
    nh = nb[3] - nb[1]
    nx = (WIDTH - nw) // 2
    ny = HEIGHT // 2 - 300 - nh // 2
    # Shadow
    draw.text((nx + 4, ny + 4), num_str, font=f_dynamic, fill=(0, 0, 0))
    draw.text((nx, ny), num_str, font=f_dynamic, fill=glow_c)

    center_text(draw, "يوم باقي", HEIGHT // 2 - 50, f_ar, WHITE)

    if p > 0.6:
        a = min(1, (p - 0.6) * 3)
        c = lerp_color(DARK_BG, PRIMARY, a)
        center_text(draw, "٧ أيام تكفي مع OilExam", HEIGHT // 2 + 80, f_sub, c)

    # Urgency bar at bottom
    if p > 0.7:
        bar_y = 1500
        bar_w = int(800 * min(1, (p - 0.7) * 4))
        bx = (WIDTH - 800) // 2
        draw.rounded_rectangle([(bx, bar_y), (bx + 800, bar_y + 20)],
                               radius=10, fill=(40, 50, 70))
        draw.rounded_rectangle([(bx, bar_y), (bx + bar_w, bar_y + 20)],
                               radius=10, fill=PRIMARY)

    return img


def r5_day_plan(p, day_num, title, items, color, items_en):
    """Show what you can master each day"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_day = ImageFont.truetype(EN_BOLD, 48)
    f_day_num = ImageFont.truetype(EN_BOLD, 140)
    f_title = ImageFont.truetype(AR_BLACK, 58)
    f_item = ImageFont.truetype(AR_BOLD, 42)
    f_item_en = ImageFont.truetype(EN_REG, 32)

    e = ease_out(p * 3)

    # Day circle at top
    cx, cy = WIDTH // 2, 280
    circle_r = int(120 * e)
    if circle_r > 10:
        draw.ellipse([(cx - circle_r, cy - circle_r),
                      (cx + circle_r, cy + circle_r)], fill=color)
        # Day number
        if e > 0.3:
            center_text(draw, "DAY", cy - 70, f_day, WHITE)
            nb = draw.textbbox((0, 0), str(day_num), font=f_day_num)
            nw = nb[2] - nb[0]
            draw.text(((WIDTH - nw) // 2, cy - 30), str(day_num),
                      font=f_day_num, fill=WHITE)

    # Title
    if e > 0.4:
        center_text(draw, title, 450, f_title, color)
        # Divider
        lw = int(500 * min(1, (p - 0.3) * 5))
        draw.line([(WIDTH//2 - lw//2, 530), (WIDTH//2 + lw//2, 530)],
                  fill=color, width=2)

    # Items
    for i, (item_ar, item_en) in enumerate(zip(items, items_en)):
        th = 0.3 + i * 0.12
        if p > th:
            a = min(1, (p - th) * 5)
            ep = ease_out((p - th) * 3)
            y = 600 + i * 200

            xo = int((1 - ep) * 200)

            # Card
            card_c = lerp_color(DARK_BG, (35, 48, 68), a)
            draw.rounded_rectangle([(80 + xo, y), (WIDTH - 80, y + 160)],
                                   radius=16, fill=card_c)

            # Color dot
            dot_c = lerp_color(DARK_BG, color, a)
            draw.ellipse([(WIDTH - 140, y + 30), (WIDTH - 100, y + 70)], fill=dot_c)

            # Arabic text (RTL)
            text_c = lerp_color(DARK_BG, WHITE, a)
            bb = draw.textbbox((0, 0), item_ar, font=f_item)
            tw = bb[2] - bb[0]
            draw.text((WIDTH - 160 - tw + xo, y + 25), item_ar,
                      font=f_item, fill=text_c)

            # English sub
            en_c = lerp_color(DARK_BG, PALE_BLUE, a)
            eb = draw.textbbox((0, 0), item_en, font=f_item_en)
            ew = eb[2] - eb[0]
            draw.text((WIDTH - 160 - ew + xo, y + 90), item_en,
                      font=f_item_en, fill=en_c)

    # Progress bar at bottom
    progress = day_num / 7
    bar_y = 1600
    bx = (WIDTH - 800) // 2
    draw.rounded_rectangle([(bx, bar_y), (bx + 800, bar_y + 16)],
                           radius=8, fill=(40, 50, 70))
    bar_w = int(800 * progress)
    if bar_w > 8:
        draw.rounded_rectangle([(bx, bar_y), (bx + bar_w, bar_y + 16)],
                               radius=8, fill=color)

    # Day indicators
    for i in range(7):
        dx = bx + int(800 * (i / 6))
        dc = color if i < day_num else (50, 60, 80)
        draw.ellipse([(dx - 6, bar_y + 30), (dx + 6, bar_y + 42)], fill=dc)

    return img


def r5_day1(p):
    return r5_day_plan(p, 1, "المفردات الأساسية",
        ["١٥٧ كلمة من اختبار النفط", "بطاقات إنجليزي ← عربي", "تمارين تفاعلية"],
        PRIMARY,
        ["157 Oil exam vocabulary words", "English-Arabic flashcards", "Interactive exercises"])


def r5_day3(p):
    return r5_day_plan(p, 3, "القواعد والأفعال",
        ["١٣٠ سؤال قواعد", "١٥٩ فعل مركّب", "تدريب عملي"],
        ORANGE,
        ["130 grammar questions", "159 phrasal verbs", "Practical drills"])


def r5_day5(p):
    return r5_day_plan(p, 5, "القراءة والفهم",
        ["٢٩ نص قراءة", "أسئلة فهم المقروء", "استراتيجيات القراءة"],
        GREEN,
        ["29 reading passages", "Comprehension questions", "Reading strategies"])


def r5_day7(p):
    return r5_day_plan(p, 7, "الاختبار التجريبي",
        ["٥٠ سؤال محاكاة", "وقت محدد مثل الحقيقي", "نتيجتك الفورية"],
        PINK,
        ["50 mock exam questions", "Timed like the real exam", "Instant results"])


def r5_ready(p):
    """You're ready! Celebration scene"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_ar = ImageFont.truetype(AR_BLACK, 85)
    f_ar2 = ImageFont.truetype(AR_BLACK, 65)
    f_num = ImageFont.truetype(EN_BOLD, 200)

    e = ease_out(p * 2.5)

    # Big green glow
    radial_gradient(img, WIDTH//2, HEIGHT//2 - 200, int(350*e),
                    lerp_color(DARK_BG, GREEN, 0.35), DARK_BG)
    draw = ImageDraw.Draw(img)

    # Animated percentage going up
    if p < 0.5:
        pct = int(65 + 30 * ease_out(p * 2))
    else:
        pct = 95
        # Pulse effect
        pulse_scale = 1 + 0.03 * math.sin((p - 0.5) * 20)
        f_num = ImageFont.truetype(EN_BOLD, int(200 * pulse_scale))

    pct_str = f"{pct}%"
    nb = draw.textbbox((0, 0), pct_str, font=f_num)
    nw = nb[2] - nb[0]
    nx = (WIDTH - nw) // 2
    draw.text((nx + 4, 404), pct_str, font=f_num, fill=(0, 0, 0))
    draw.text((nx, 400), pct_str, font=f_num, fill=GREEN)

    center_text(draw, "جاهز للاختبار", 700, f_ar, WHITE)

    if p > 0.4:
        a = min(1, (p - 0.4) * 4)
        c = lerp_color(DARK_BG, GREEN, a)
        center_text(draw, "!بس ٧ أيام مع OilExam", 830, f_ar2, c)

    # Animated checkmarks appearing
    checks = [
        ("المفردات", PRIMARY),
        ("القواعد", ORANGE),
        ("القراءة", GREEN),
        ("الاختبار", PINK),
    ]
    f_check = ImageFont.truetype(AR_BOLD, 44)
    for i, (label, color) in enumerate(checks):
        th = 0.5 + i * 0.08
        if p > th:
            a = min(1, (p - th) * 5)
            y = 1000 + i * 90
            gc = lerp_color(DARK_BG, GREEN, a)
            tc = lerp_color(DARK_BG, WHITE, a)
            bb = draw.textbbox((0, 0), label, font=f_check)
            tw = bb[2] - bb[0]
            total_w = tw + 60
            sx = (WIDTH - total_w) // 2
            draw.text((sx, y), "✓", font=f_check, fill=gc)
            draw.text((sx + 50, y), label, font=f_check, fill=tc)

    return img


def r5_cta(p):
    """CTA for Countdown reel"""
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    f_huge = ImageFont.truetype(AR_BLACK, 80)
    f_brand = ImageFont.truetype(EN_BOLD, 72)
    f_btn = ImageFont.truetype(AR_BLACK, 50)
    f_ar = ImageFont.truetype(AR_BOLD, 42)
    f_small = ImageFont.truetype(EN_REG, 32)
    f_timer = ImageFont.truetype(EN_BOLD, 48)

    e = ease_out(p * 3)
    pulse = 0.88 + 0.12 * math.sin(p * 10)

    radial_gradient(img, WIDTH//2, 420, int(300*e), (40, 55, 90), DARK_BG)
    draw = ImageDraw.Draw(img)

    # Ticking timer text
    center_text(draw, "الوقت ما ينتظر", int(240 + (1-e)*80), f_huge, WHITE)

    if p > 0.1:
        center_text(draw, "!ابدأ خطتك الحين", 380, f_huge, PRIMARY)

    if p > 0.2:
        center_text(draw, "oilexam.tech", 550, f_brand, WHITE)

    if p > 0.3:
        bw, bh = 720, 130
        bx, by = (WIDTH - bw) // 2, 700
        btn_color = tuple(int(c * pulse) for c in PRIMARY)
        draw.rounded_rectangle([(bx-4, by-4), (bx+bw+4, by+bh+4)],
                               radius=65, fill=btn_color)
        draw.rounded_rectangle([(bx, by), (bx+bw, by+bh)],
                               radius=62, fill=PRIMARY)
        center_text(draw, "سجّل الحين", by + 30, f_btn, WHITE)

    if p > 0.45:
        items = [
            "٧ أيام = جاهز للاختبار",
            "525+ سؤال وتمرين",
            "خطة دراسية كاملة",
            "مجاني وسهل",
        ]
        for i, item in enumerate(items):
            th = 0.45 + i * 0.07
            if p > th:
                a = min(1, (p - th) * 5)
                y = 940 + i * 80
                c_dot = lerp_color(DARK_BG, PRIMARY, a)
                c_txt = lerp_color(DARK_BG, WHITE, a)
                draw.text((280, y), "▸", font=f_ar, fill=c_dot)
                draw.text((330, y), item, font=f_ar, fill=c_txt)

    if p > 0.7:
        center_text(draw, "الرابط بالبايو", 1400, f_ar, ORANGE)
        center_text(draw, "Powered by Trimind Company", 1650, f_small, (80, 95, 120))

    return img


# ════════════════════════════════════════════════════════════════
#  BUILD
# ════════════════════════════════════════════════════════════════

def main():
    print("+" + "="*54 + "+")
    print("|  OilExam.tech - 2 New Instagram Reels               |")
    print("|  Reel 4: Before vs After  |  Reel 5: Countdown      |")
    print("+" + "="*54 + "+")
    print(f"Resolution: {WIDTH}x{HEIGHT} | FPS: {FPS}")

    out_dir = "/root/OilexamVideo"

    # Reel 4: Before vs After
    build_video("reel4_before_after", [
        ("Hook - قبل وبعد",      r4_hook,        4.0),
        ("Before - المعاناة",     r4_before,      5.0),
        ("Transition",            r4_transition,  2.5),
        ("After - النجاح",        r4_after,       5.0),
        ("CTA",                   r4_cta,         5.0),
    ], f"{out_dir}/reel_new_4_before_after.mp4")

    # Reel 5: Countdown Timer
    build_video("reel5_countdown", [
        ("Hook - الساعة",         r5_hook,        4.0),
        ("Days Left",             r5_days_left,   4.0),
        ("Day 1 - مفردات",       r5_day1,        3.5),
        ("Day 3 - قواعد",        r5_day3,        3.5),
        ("Day 5 - قراءة",        r5_day5,        3.5),
        ("Day 7 - اختبار",       r5_day7,        3.5),
        ("Ready - جاهز",         r5_ready,       4.0),
        ("CTA",                   r5_cta,         5.0),
    ], f"{out_dir}/reel_new_5_countdown.mp4")

    print("\n+" + "="*54 + "+")
    print("|         BOTH NEW REELS COMPLETE!                     |")
    print("+" + "="*54 + "+")


if __name__ == "__main__":
    main()
