#!/usr/bin/env python3
"""
OilExam.tech - Professional Reel #10: Student Journey
A cinematic story of a student going from confused to confident.
Color progression: RED (struggle) -> BLUE (discovery) -> GREEN (success)
"""

from pro_utils import *
import math

# Pre-create particles for each scene
particles_hook = create_floating_particles(25, seed=100)
particles_struggle = create_floating_particles(20, seed=200)
particles_discovery = create_floating_particles(30, seed=300)
particles_montage = create_floating_particles(20, seed=400)
particles_exam = create_floating_particles(35, seed=500)


# ═══════════════════════════════════════════
#  SCENE 1: BRANDED INTRO (2s)
# ═══════════════════════════════════════════
def scene_intro(p):
    return branded_intro(p)


# ═══════════════════════════════════════════
#  SCENE 2: HOOK — "A Real Success Story" (3s)
# ═══════════════════════════════════════════
def scene_hook(p):
    # Dark-to-light reveal
    brightness = ease_out(min(1, p * 2))
    bg_c1 = lerp_color((5, 5, 10), DARK_BG, brightness)
    bg_c2 = lerp_color((2, 2, 5), DARKER_BG, brightness)
    img = gradient_bg(WIDTH, HEIGHT, bg_c1, bg_c2)
    draw = ImageDraw.Draw(img)

    # Central glow expanding
    glow_p = ease_out(min(1, p * 1.8))
    glow_r = int(500 * glow_p)
    if glow_r > 10:
        radial_gradient(img, WIDTH // 2, HEIGHT // 2 - 100, glow_r,
                        lerp_color(DARKER_BG, PRIMARY, 0.2 * brightness), DARKER_BG)
        draw = ImageDraw.Draw(img)

    # Particles fade in
    draw_particles(draw, particles_hook, p, alpha=0.5 * brightness)

    # Main text: dramatic reveal
    f_main = ImageFont.truetype(AR_BLACK, 82)
    f_sub = ImageFont.truetype(AR_BOLD, 48)

    if p > 0.15:
        tp = (p - 0.15) / 0.85
        bounce_text_ar(draw, "قصة نجاح حقيقية", HEIGHT // 2 - 120, f_main, WHITE, tp)

    # Decorative line
    if p > 0.35:
        line_p = ease_out((p - 0.35) * 3)
        lw = int(600 * line_p)
        draw_gradient_line(draw, HEIGHT // 2 + 10, lw, PRIMARY, GOLD, 4)

    # Subtitle
    if p > 0.5:
        tp = (p - 0.5) / 0.5
        scale_fade_in(draw, ar("من الصفر إلى القمة"), HEIGHT // 2 + 60, f_sub, PALE_BLUE, tp)

    # Sparkle accents
    if p > 0.3:
        sp = (p - 0.3) / 0.7
        draw_sparkle_burst(draw, WIDTH // 2, HEIGHT // 2 - 80, sp * 0.6, count=10, max_radius=250, color=GOLD)

    # Corner accents
    draw_corner_accents(draw, p, PRIMARY)

    img = add_grain_fast(img)
    return img


# ═══════════════════════════════════════════
#  SCENE 3: THE STRUGGLE (3.5s) — Red-toned
# ═══════════════════════════════════════════
def scene_struggle(p):
    # Red-toned dark background
    img = gradient_bg(WIDTH, HEIGHT, (40, 15, 15), (20, 8, 8))
    draw = ImageDraw.Draw(img)

    # Red glow
    radial_gradient(img, WIDTH // 2, HEIGHT // 2, 500,
                    lerp_color((20, 8, 8), RED, 0.12), (20, 8, 8))
    draw = ImageDraw.Draw(img)

    # Red-tinted particles
    red_particles = create_floating_particles(20, seed=201)
    for pt in red_particles:
        pt.color = random.Random(int(pt.x)).choice([RED, (180, 50, 50), (120, 30, 30), ORANGE])
    draw_particles(draw, red_particles, p, alpha=0.4)

    f_title = ImageFont.truetype(AR_BLACK, 62)
    f_item = ImageFont.truetype(AR_BOLD, 50)
    f_x = ImageFont.truetype(EN_BOLD, 60)

    # Title
    if p > 0.05:
        bounce_text_ar(draw, "المعاناة", SAFE_TOP + 50, f_title, RED, (p - 0.05) * 3)

    # Struggle items with X marks sliding in
    items = [
        ("ما عرفت من وين أبدأ", 0.15),
        ("المواد مبعثرة", 0.35),
        ("الوقت يمشي", 0.55),
    ]

    for i, (text, threshold) in enumerate(items):
        if p > threshold:
            tp = (p - threshold) / (1 - threshold)
            y = SAFE_TOP + 250 + i * 160

            # Glass card background
            card_e = ease_out(min(1, tp * 3))
            if card_e > 0.1:
                card_alpha = 0.08 * card_e
                draw_glass_card(draw, SAFE_LEFT + 20, y - 20, SAFE_RIGHT - 20, y + 80,
                                radius=16, opacity=card_alpha,
                                border_color=lerp_color(DARK_BG, RED, 0.15 * card_e))

            # X mark slides in from left
            x_e = ease_out(min(1, tp * 4))
            x_pos = int(SAFE_LEFT + 40 + (1 - x_e) * (-200))
            x_alpha = min(1, x_e * 2)
            x_color = lerp_color((20, 8, 8), RED, x_alpha)
            draw.text((x_pos, y), "X", font=f_x, fill=x_color)

            # Text slides in from right
            slide_in_right(draw, ar(text), y + 5, f_item, WHITE, tp)

    # Pulsing warning glow at bottom
    if p > 0.7:
        pulse = 0.5 + 0.5 * math.sin(p * 15)
        warn_c = lerp_color((20, 8, 8), RED, 0.15 * pulse)
        draw.rectangle([(0, SAFE_BOTTOM - 30), (WIDTH, SAFE_BOTTOM + 30)], fill=warn_c)

    draw_corner_accents(draw, p, RED)
    img = add_grain_fast(img)
    return img


# ═══════════════════════════════════════════
#  SCENE 4: DISCOVERY (2.5s) — Red to Blue transition
# ═══════════════════════════════════════════
def scene_discovery(p):
    # Color transition: red-toned -> blue-toned
    color_t = ease_in_out(min(1, p * 1.5))
    bg_c1 = lerp_color((40, 15, 15), DARK_BG, color_t)
    bg_c2 = lerp_color((20, 8, 8), DARKER_BG, color_t)
    img = gradient_bg(WIDTH, HEIGHT, bg_c1, bg_c2)
    draw = ImageDraw.Draw(img)

    # Growing blue glow (light burst)
    if p > 0.2:
        glow_t = ease_out((p - 0.2) / 0.8)
        glow_r = int(600 * glow_t)
        radial_gradient(img, WIDTH // 2, HEIGHT // 2 - 50, glow_r,
                        lerp_color(DARKER_BG, PRIMARY, 0.3 * glow_t), DARKER_BG)
        draw = ImageDraw.Draw(img)

    # Particles transition color
    draw_particles(draw, particles_discovery, p, alpha=0.5)

    f_solution = ImageFont.truetype(AR_BLACK, 68)
    f_brand = ImageFont.truetype(EN_BOLD, 88)
    f_dot = ImageFont.truetype(EN_BOLD, 88)

    # "Found the solution" text
    if p > 0.1:
        tp = (p - 0.1) / 0.9
        bounce_text_ar(draw, "لقيت الحل", SAFE_TOP + 200, f_solution, WHITE, tp)

    # Brand name appearing with sparkle
    if p > 0.35:
        brand_t = (p - 0.35) / 0.65
        brand_e = ease_out_back(min(1, brand_t * 2))

        brand = "OilExam"
        bbox = draw.textbbox((0, 0), brand, font=f_brand)
        tw = bbox[2] - bbox[0]
        bx = (WIDTH - tw) // 2 - 35
        by = HEIGHT // 2 - 30 - int((1 - brand_e) * 60)

        if brand_e > 0.1:
            alpha = min(1, brand_e * 2)
            c = lerp_color(DARKER_BG, WHITE, alpha)
            draw.text((bx + 4, by + 4), brand, font=f_brand, fill=(0, 0, 0))
            draw.text((bx, by), brand, font=f_brand, fill=c)

            # .tech in brand color
            dot_c = lerp_color(DARKER_BG, PRIMARY, alpha)
            draw.text((bx + tw + 5, by + 4), ".tech", font=f_dot, fill=(0, 0, 0))
            draw.text((bx + tw + 1, by), ".tech", font=f_dot, fill=dot_c)

        # Sparkle burst around brand
        if brand_t > 0.2:
            sp = (brand_t - 0.2) / 0.8
            draw_sparkle_burst(draw, WIDTH // 2, HEIGHT // 2 - 10, sp, count=18, max_radius=300, color=GOLD)

    # Gradient line
    if p > 0.5:
        line_p = ease_out((p - 0.5) * 3)
        draw_gradient_line(draw, HEIGHT // 2 + 100, int(500 * line_p), PRIMARY, MID_BLUE, 3)

    draw_corner_accents(draw, p, PRIMARY)
    img = add_grain_fast(img)
    return img


# ═══════════════════════════════════════════
#  SCENE 5: TRAINING MONTAGE (4s) — Progress bars
# ═══════════════════════════════════════════
def scene_montage(p):
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    # Subtle blue glow
    radial_gradient(img, WIDTH // 2, HEIGHT // 2, 500,
                    lerp_color(DARK_BG, PRIMARY, 0.08), DARK_BG)
    draw = ImageDraw.Draw(img)

    draw_particles(draw, particles_montage, p, alpha=0.3)

    f_title = ImageFont.truetype(AR_BLACK, 58)
    f_cat = ImageFont.truetype(AR_BOLD, 42)
    f_pct = ImageFont.truetype(EN_BOLD, 40)

    # Title
    bounce_text_ar(draw, "رحلة التعلّم", SAFE_TOP + 30, f_title, WHITE, p)

    # Progress bars data
    bars = [
        ("المفردات", 85, PRIMARY, 0.08),
        ("القواعد", 92, ORANGE, 0.25),
        ("القراءة", 78, GREEN, 0.42),
        ("الاختبار", 95, PINK, 0.59),
    ]

    bar_x1 = SAFE_LEFT + 30
    bar_x2 = SAFE_RIGHT - 30
    bar_height = 50
    bar_radius = 25
    bar_width = bar_x2 - bar_x1

    for i, (name, target_pct, color, threshold) in enumerate(bars):
        if p < threshold:
            continue

        tp = (p - threshold) / (1.0 - threshold)
        y_base = SAFE_TOP + 200 + i * 200

        # Slide in from left
        slide_e = ease_out(min(1, tp * 3))
        x_offset = int((1 - slide_e) * (-500))

        # Glass card
        card_y1 = y_base - 15
        card_y2 = y_base + bar_height + 70
        if slide_e > 0.1:
            draw_glass_card(draw, bar_x1 - 10 + x_offset, card_y1,
                            bar_x2 + 10 + x_offset, card_y2,
                            radius=20, opacity=0.1,
                            border_color=lerp_color(DARK_BG, color, 0.2),
                            accent_color=color)

        # Category name (Arabic)
        if slide_e > 0.2:
            name_alpha = min(1, (slide_e - 0.2) * 3)
            name_c = lerp_color(DARK_BG, WHITE, name_alpha)
            name_rendered = ar(name)
            # Right-align the name within the bar area
            name_bbox = draw.textbbox((0, 0), name_rendered, font=f_cat)
            name_w = name_bbox[2] - name_bbox[0]
            draw.text((bar_x2 - name_w + x_offset, y_base - 5), name_rendered,
                      font=f_cat, fill=name_c)

        # Progress bar background
        bar_y = y_base + 50
        bg_bar_c = lerp_color(DARK_BG, (50, 60, 80), slide_e * 0.5)
        draw.rounded_rectangle([(bar_x1 + x_offset, bar_y),
                                 (bar_x2 + x_offset, bar_y + bar_height)],
                                radius=bar_radius, fill=bg_bar_c)

        # Filling progress bar
        if tp > 0.3:
            fill_t = ease_out(min(1, (tp - 0.3) / 0.5))
            fill_pct = fill_t * target_pct / 100
            fill_width = int(bar_width * fill_pct)
            if fill_width > bar_radius * 2:
                # Gradient fill
                for px in range(fill_width):
                    ratio = px / max(fill_width, 1)
                    c = lerp_color(dim(color, 0.7), color, ratio)
                    x = bar_x1 + px + x_offset
                    draw.line([(x, bar_y + 2), (x, bar_y + bar_height - 2)], fill=c)
                # Re-draw rounded ends
                draw.rounded_rectangle([(bar_x1 + x_offset, bar_y),
                                         (bar_x1 + fill_width + x_offset, bar_y + bar_height)],
                                        radius=bar_radius, fill=None, outline=None)
                # Clean fill with proper rounding
                draw.rounded_rectangle([(bar_x1 + x_offset, bar_y),
                                         (bar_x1 + fill_width + x_offset, bar_y + bar_height)],
                                        radius=bar_radius, fill=color)

                # Highlight strip on top
                highlight_c = lerp_color(color, WHITE, 0.2)
                draw.rounded_rectangle([(bar_x1 + 4 + x_offset, bar_y + 4),
                                         (bar_x1 + fill_width - 4 + x_offset, bar_y + bar_height // 2)],
                                        radius=bar_radius - 4, fill=highlight_c)

            # Percentage counter
            current_pct = int(fill_t * target_pct)
            pct_text = f"{current_pct}%"
            pct_c = lerp_color(DARK_BG, WHITE, min(1, fill_t * 2))
            draw.text((bar_x1 + 15 + x_offset, bar_y + 5), pct_text,
                      font=f_pct, fill=pct_c)

    # Progress dots at bottom
    if p > 0.3:
        current_dot = min(3, int((p - 0.3) / 0.18))
        draw_progress_dots(draw, SAFE_BOTTOM - 30, current_dot, 4, PRIMARY)

    draw_corner_accents(draw, p, MID_BLUE)
    img = add_grain_fast(img)
    return img


# ═══════════════════════════════════════════
#  SCENE 6: EXAM DAY (3s) — Green victory
# ═══════════════════════════════════════════
def scene_exam_day(p):
    # Green-tinted background
    green_t = ease_out(min(1, p * 2))
    bg_c1 = lerp_color(DARK_BG, (20, 45, 35), green_t * 0.5)
    bg_c2 = lerp_color(DARKER_BG, (10, 30, 22), green_t * 0.3)
    img = gradient_bg(WIDTH, HEIGHT, bg_c1, bg_c2)
    draw = ImageDraw.Draw(img)

    # Green glow
    glow_r = int(500 * green_t)
    if glow_r > 10:
        radial_gradient(img, WIDTH // 2, HEIGHT // 2 - 100, glow_r,
                        lerp_color(DARKER_BG, GREEN, 0.15 * green_t), DARKER_BG)
        draw = ImageDraw.Draw(img)

    # Celebration particles
    celebration_particles = create_floating_particles(35, seed=501)
    for pt in celebration_particles:
        pt.color = random.Random(int(pt.x * pt.y + 1)).choice([GREEN, GOLD, WHITE, TEAL, YELLOW])
    draw_particles(draw, celebration_particles, p, alpha=0.5)

    f_title = ImageFont.truetype(AR_BLACK, 62)
    f_score = ImageFont.truetype(EN_BOLD, 160)
    f_pass = ImageFont.truetype(AR_BLACK, 90)
    f_sub = ImageFont.truetype(AR_BOLD, 44)

    # "Exam Day" title
    if p > 0.05:
        tp = (p - 0.05) / 0.95
        bounce_text_ar(draw, "يوم الاختبار", SAFE_TOP + 80, f_title, WHITE, tp)

    # Decorative line
    if p > 0.15:
        line_p = ease_out((p - 0.15) * 4)
        draw_gradient_line(draw, SAFE_TOP + 190, int(400 * line_p), GREEN, TEAL, 3)

    # Big score "95%"
    if p > 0.25:
        score_t = (p - 0.25) / 0.75
        score_e = ease_out_elastic(min(1, score_t * 2))

        score_text = "95%"
        bbox = draw.textbbox((0, 0), score_text, font=f_score)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        sx = (WIDTH - tw) // 2
        sy = HEIGHT // 2 - 180 - int((1 - score_e) * 100)

        if score_e > 0.1:
            alpha = min(1, score_e * 1.5)
            # Shadow
            shadow_c = (0, 0, 0)
            draw.text((sx + 6, sy + 6), score_text, font=f_score, fill=shadow_c)
            # Main text
            score_c = lerp_color(DARKER_BG, GREEN, alpha)
            draw.text((sx, sy), score_text, font=f_score, fill=score_c)

        # Sparkle burst around score
        if score_t > 0.3:
            sp = (score_t - 0.3) / 0.7
            draw_sparkle_burst(draw, WIDTH // 2, HEIGHT // 2 - 130, sp,
                               count=20, max_radius=280, color=GOLD)

    # "Passed!" text
    if p > 0.45:
        pass_t = (p - 0.45) / 0.55
        bounce_text_ar(draw, "ناجح!", HEIGHT // 2 + 100, f_pass, GREEN, pass_t)

    # Additional sparkle bursts for celebration
    if p > 0.55:
        cp = (p - 0.55) / 0.45
        draw_sparkle_burst(draw, 250, 600, cp, count=8, max_radius=120, color=YELLOW)
        draw_sparkle_burst(draw, 830, 700, cp * 0.8, count=8, max_radius=120, color=GOLD)
        draw_sparkle_burst(draw, WIDTH // 2, 1200, cp * 0.6, count=10, max_radius=150, color=GREEN)

    # Subtitle
    if p > 0.6:
        sub_t = (p - 0.6) / 0.4
        scale_fade_in(draw, ar("OilExam.tech غيّر حياتي"), HEIGHT // 2 + 280, f_sub, PALE_BLUE, sub_t)

    draw_corner_accents(draw, p, GREEN)
    img = add_grain_fast(img)
    return img


# ═══════════════════════════════════════════
#  SCENE 7: BRANDED OUTRO (4s)
# ═══════════════════════════════════════════
def scene_outro(p):
    return branded_outro(p)


# ═══════════════════════════════════════════
#  BUILD VIDEO
# ═══════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs("/root/OilexamVideo", exist_ok=True)

    scenes = [
        ("Branded Intro", scene_intro, 2.0),
        ("Hook - Real Success Story", scene_hook, 3.0),
        ("The Struggle", scene_struggle, 3.5),
        ("Discovery", scene_discovery, 2.5),
        ("Training Montage", scene_montage, 4.0),
        ("Exam Day", scene_exam_day, 3.0),
        ("Branded Outro", scene_outro, 4.0),
    ]

    output = "/root/OilexamVideo/pro_reel_10_student_journey.mp4"
    build_video("reel_10_student_journey", scenes, output)
    print(f"\nVideo saved to: {output}")
