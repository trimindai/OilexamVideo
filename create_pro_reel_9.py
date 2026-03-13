#!/usr/bin/env python3
"""
OilExam.tech - Professional Reel 9: Feature Tour
A sleek walkthrough of OilExam's 5 key features with glassmorphism cards.
"""

from pro_utils import *

# ═══ SHARED RESOURCES ═══
particles_main = create_floating_particles(25, seed=900)

# Feature definitions: (number, arabic_label, english_label, accent_color, icon_symbol)
FEATURES = [
    ("157", "سؤال مفردات", "Vocabulary Questions", PRIMARY, "Aa"),
    ("159", "فعل مركّب", "Phrasal Verbs", MID_BLUE, "Ph"),
    ("130", "سؤال قواعد", "Grammar Questions", ORANGE, "Gr"),
    ("29",  "نص قراءة", "Reading Passages", GREEN, "Rd"),
    ("50",  "سؤال اختبار", "Mock Exam Questions", PINK, "Ex"),
]


# ═══════════════════════════════════════════
#  SCENE 1: BRANDED INTRO (2s)
# ═══════════════════════════════════════════
def scene_intro(p):
    return branded_intro(p)


# ═══════════════════════════════════════════
#  SCENE 2: HOOK (3s)
# ═══════════════════════════════════════════
def scene_hook(p):
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    # Radial glow
    glow_p = ease_out(min(1, p * 2))
    radial_gradient(img, WIDTH // 2, HEIGHT // 2 - 100, int(400 * glow_p),
                    lerp_color(DARK_BG, PRIMARY, 0.2), DARK_BG)
    draw = ImageDraw.Draw(img)

    # Particles
    draw_particles(draw, particles_main, p, alpha=0.5)

    # Corner accents
    draw_corner_accents(draw, p, PRIMARY)

    # Main question text
    f_huge = ImageFont.truetype(AR_BLACK, 82)
    bounce_text_ar(draw, "شنو بتحصل عليه؟", SAFE_TOP + 350, f_huge, WHITE, p)

    # Subtitle
    if p > 0.3:
        f_sub = ImageFont.truetype(AR_BOLD, 44)
        sub_p = (p - 0.3) / 0.7
        scale_fade_in(draw, ar("جولة سريعة بالمميزات"), SAFE_TOP + 500, f_sub, PALE_BLUE, sub_p)

    # English subtitle
    if p > 0.45:
        f_en = ImageFont.truetype(EN_REG, 32)
        en_p = (p - 0.45) / 0.55
        scale_fade_in(draw, "Quick Feature Tour", SAFE_TOP + 580, f_en, dim(LIGHT_BLUE, 0.8), en_p)

    # Animated line
    if p > 0.25:
        line_p = ease_out((p - 0.25) * 3)
        lw = int(600 * line_p)
        draw_gradient_line(draw, SAFE_TOP + 470, lw, PRIMARY, MID_BLUE, 3)

    # Sparkle bursts
    if p > 0.5:
        sp = (p - 0.5) * 2
        draw_sparkle_burst(draw, WIDTH // 2 - 200, SAFE_TOP + 400, sp, 8, 100, GOLD)
        draw_sparkle_burst(draw, WIDTH // 2 + 200, SAFE_TOP + 400, sp, 8, 100, GOLD)

    img = add_grain_fast(img, 10)
    return img


# ═══════════════════════════════════════════
#  FEATURE CARD SCENE FACTORY
# ═══════════════════════════════════════════
def make_feature_scene(index):
    number, ar_label, en_label, accent, icon = FEATURES[index]

    def scene(p):
        img = brand_bg(dark_shift=5)
        draw = ImageDraw.Draw(img)

        # Background accent glow
        glow_e = ease_out(min(1, p * 2.5))
        radial_gradient(img, WIDTH // 2, HEIGHT // 2, int(350 * glow_e),
                        lerp_color(DARK_BG, accent, 0.12), DARK_BG)
        draw = ImageDraw.Draw(img)

        # Particles
        draw_particles(draw, particles_main, p + index * 0.3, alpha=0.35)

        # Glassmorphism card with slide-in animation
        card_e = ease_out_back(min(1, p * 3))
        card_y_offset = int((1 - card_e) * 120)

        card_x1 = SAFE_LEFT + 30
        card_y1 = SAFE_TOP + 250 + card_y_offset
        card_x2 = SAFE_RIGHT - 30
        card_y2 = card_y1 + 550

        if card_e > 0.05:
            draw_glass_card(draw, card_x1, card_y1, card_x2, card_y2,
                            radius=28, opacity=0.12, accent_color=accent)

            # Icon circle
            icon_cx = WIDTH // 2
            icon_cy = card_y1 + 100
            icon_r = int(55 * card_e)
            # Glow behind icon
            for r in range(icon_r + 20, icon_r, -1):
                a = 0.15 * (1 - (r - icon_r) / 20)
                gc = lerp_color(DARK_BG, accent, a)
                draw.ellipse([(icon_cx - r, icon_cy - r), (icon_cx + r, icon_cy + r)], fill=gc)
            # Icon circle fill
            draw.ellipse([(icon_cx - icon_r, icon_cy - icon_r),
                          (icon_cx + icon_r, icon_cy + icon_r)], fill=accent)
            # Icon text
            f_icon = ImageFont.truetype(EN_BOLD, 40)
            bbox_icon = draw.textbbox((0, 0), icon, font=f_icon)
            iw = bbox_icon[2] - bbox_icon[0]
            ih = bbox_icon[3] - bbox_icon[1]
            draw.text((icon_cx - iw // 2, icon_cy - ih // 2 - 4), icon, font=f_icon, fill=WHITE)

            # Big number
            f_num = ImageFont.truetype(EN_BOLD, 120)
            num_p = max(0, (p - 0.1) / 0.9)
            if num_p > 0:
                bounce_text(draw, number, card_y1 + 190, f_num, accent, num_p)

            # Arabic label
            f_ar = ImageFont.truetype(AR_BLACK, 56)
            ar_p = max(0, (p - 0.2) / 0.8)
            if ar_p > 0:
                slide_in_right(draw, ar(ar_label), card_y1 + 330, f_ar, WHITE, ar_p)

            # English label
            f_en = ImageFont.truetype(EN_REG, 34)
            en_p = max(0, (p - 0.3) / 0.7)
            if en_p > 0:
                scale_fade_in(draw, en_label, card_y1 + 420, f_en, dim(PALE_BLUE, 0.9), en_p)

            # Decorative gradient line inside card
            if p > 0.35:
                line_p = ease_out((p - 0.35) * 3)
                draw_gradient_line(draw, card_y1 + 480, int(500 * line_p), accent, dim(accent, 0.4), 2)

        # Progress dots at the bottom
        if p > 0.15:
            dot_p = ease_out((p - 0.15) * 4)
            dot_alpha = min(1, dot_p)
            active_c = lerp_color(DARK_BG, accent, dot_alpha)
            draw_progress_dots(draw, SAFE_BOTTOM - 80, index, 5, active_c)

        # Feature number label at top
        f_top = ImageFont.truetype(AR_BOLD, 32)
        if p > 0.05:
            top_a = min(1, (p - 0.05) * 5)
            top_c = lerp_color(DARK_BG, dim(WHITE, 0.6), top_a)
            center_text(draw, ar(f"الميزة {index + 1} من 5"), SAFE_TOP + 60, f_top, top_c)

        # Corner accents
        draw_corner_accents(draw, p, accent, size=40)

        img = add_grain_fast(img, 8)
        return img

    return scene


# ═══════════════════════════════════════════
#  SCENE 8: TOTAL REVEAL (3s)
# ═══════════════════════════════════════════
def scene_total(p):
    img = brand_bg()
    draw = ImageDraw.Draw(img)

    # Big radial glow
    glow_e = ease_out(min(1, p * 2))
    radial_gradient(img, WIDTH // 2, HEIGHT // 2 - 50, int(500 * glow_e),
                    lerp_color(DARK_BG, PRIMARY, 0.25), DARK_BG)
    draw = ImageDraw.Draw(img)

    # Particles (more of them)
    particles_big = create_floating_particles(40, seed=525)
    draw_particles(draw, particles_big, p, alpha=0.5)

    # Corner accents
    draw_corner_accents(draw, p, GOLD, size=70)

    # "Total" label
    f_label = ImageFont.truetype(AR_BLACK, 52)
    if p > 0.05:
        label_p = (p - 0.05) / 0.95
        bounce_text_ar(draw, "المجموع الكامل", SAFE_TOP + 250, f_label, PALE_BLUE, label_p)

    # Counting animation for the big number
    f_huge = ImageFont.truetype(EN_BOLD, 160)
    if p > 0.1:
        count_p = min(1, (p - 0.1) / 0.5)
        count_e = ease_out(count_p)
        current_num = int(525 * count_e)
        num_text = f"{current_num}+"
        bounce_text(draw, num_text, SAFE_TOP + 380, f_huge, WHITE, min(1, (p - 0.1) * 3))

    # Arabic sub-label
    f_sub = ImageFont.truetype(AR_BOLD, 48)
    if p > 0.3:
        sub_p = (p - 0.3) / 0.7
        scale_fade_in(draw, ar("سؤال ونص تدريبي"), SAFE_TOP + 600, f_sub, LIGHT_BLUE, sub_p)

    # English sub-label
    f_en = ImageFont.truetype(EN_REG, 34)
    if p > 0.4:
        en_p = (p - 0.4) / 0.6
        scale_fade_in(draw, "Questions & Passages", SAFE_TOP + 680, f_en, dim(PALE_BLUE, 0.8), en_p)

    # Feature summary cards (mini versions)
    if p > 0.35:
        mini_p = ease_out((p - 0.35) * 2.5)
        f_mini_num = ImageFont.truetype(EN_BOLD, 36)
        f_mini_ar = ImageFont.truetype(AR_BOLD, 26)

        mini_features = [
            ("157", "مفردات", PRIMARY),
            ("159", "أفعال", MID_BLUE),
            ("130", "قواعد", ORANGE),
            ("29", "قراءة", GREEN),
            ("50", "اختبار", PINK),
        ]

        card_w = 150
        total_w = 5 * card_w + 4 * 12
        start_x = (WIDTH - total_w) // 2

        for i, (num, label, color) in enumerate(mini_features):
            delay = i * 0.06
            item_p = max(0, min(1, (mini_p - delay) / 0.7))
            if item_p <= 0:
                continue
            item_e = ease_out_back(item_p)

            cx = start_x + i * (card_w + 12)
            cy = SAFE_TOP + 820
            y_off = int((1 - item_e) * 40)

            # Mini glass card
            alpha_val = min(1, item_e * 2)
            border_c = lerp_color(DARK_BG, color, 0.3 * alpha_val)
            draw_glass_card(draw, cx, cy + y_off, cx + card_w, cy + y_off + 160,
                            radius=16, opacity=0.1 * alpha_val, accent_color=color)

            # Number
            num_c = lerp_color(DARK_BG, color, alpha_val)
            bbox_n = draw.textbbox((0, 0), num, font=f_mini_num)
            nw = bbox_n[2] - bbox_n[0]
            draw.text((cx + (card_w - nw) // 2, cy + y_off + 35), num, font=f_mini_num, fill=num_c)

            # Arabic label
            txt_c = lerp_color(DARK_BG, WHITE, alpha_val * 0.8)
            ar_text = ar(label)
            bbox_a = draw.textbbox((0, 0), ar_text, font=f_mini_ar)
            aw = bbox_a[2] - bbox_a[0]
            draw.text((cx + (card_w - aw) // 2, cy + y_off + 90), ar_text, font=f_mini_ar, fill=txt_c)

    # Sparkle bursts
    if p > 0.15:
        sp = (p - 0.15) * 1.2
        draw_sparkle_burst(draw, WIDTH // 2, SAFE_TOP + 450, sp, 16, 200, GOLD)
    if p > 0.5:
        sp2 = (p - 0.5) * 2
        draw_sparkle_burst(draw, WIDTH // 2 - 150, SAFE_TOP + 350, sp2, 10, 120, PRIMARY)
        draw_sparkle_burst(draw, WIDTH // 2 + 150, SAFE_TOP + 350, sp2, 10, 120, PRIMARY)

    # Gradient line
    if p > 0.25:
        line_p = ease_out((p - 0.25) * 3)
        draw_gradient_line(draw, SAFE_TOP + 760, int(700 * line_p), PRIMARY, GOLD, 3)

    img = add_grain_fast(img, 10)
    return img


# ═══════════════════════════════════════════
#  SCENE 9: BRANDED OUTRO (4s)
# ═══════════════════════════════════════════
def scene_outro(p):
    return branded_outro(p)


# ═══════════════════════════════════════════
#  BUILD
# ═══════════════════════════════════════════
if __name__ == "__main__":
    os.makedirs("/root/OilexamVideo", exist_ok=True)

    scenes = [
        ("Branded Intro",      scene_intro,              2.0),
        ("Hook",               scene_hook,               3.0),
        ("Feature 1: Vocab",   make_feature_scene(0),    2.5),
        ("Feature 2: Phrasal", make_feature_scene(1),    2.5),
        ("Feature 3: Grammar", make_feature_scene(2),    2.5),
        ("Feature 4: Reading", make_feature_scene(3),    2.5),
        ("Feature 5: Mock",    make_feature_scene(4),    2.5),
        ("Total Reveal",       scene_total,              3.0),
        ("Branded Outro",      scene_outro,              4.0),
    ]

    output = "/root/OilexamVideo/pro_reel_9_feature_tour.mp4"
    build_video("reel_9_feature_tour", scenes, output)
    print(f"\nFeature Tour reel ready: {output}")
