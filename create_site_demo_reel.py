#!/usr/bin/env python3
"""
OilExam.tech - Site Demo Reel
Simulated screen recording of browsing the actual website.
Shows: Landing page, scrolling, quiz UI, flashcards, results.
"""

from pro_utils import *

# ═══ SITE COLORS (from actual Tailwind theme) ═══
SITE_BG = (249, 250, 251)       # bg-gray-50
SITE_WHITE = (255, 255, 255)
SITE_BLUE = (59, 130, 246)      # blue-500
SITE_DARK_BLUE = (37, 99, 235)  # blue-600
SITE_TEXT = (17, 24, 39)        # gray-900
SITE_TEXT_LIGHT = (107, 114, 128)  # gray-500
SITE_BORDER = (229, 231, 235)   # gray-200
SITE_GREEN = (34, 197, 94)      # green-500
SITE_RED_BADGE = (239, 68, 68)  # red-500
WA_GREEN = (37, 211, 102)       # WhatsApp green

# Phone frame dimensions
PHONE_X = 40
PHONE_Y = 140
PHONE_W = WIDTH - 80
PHONE_H = HEIGHT - 280
PHONE_R = 40  # corner radius
SCREEN_X = PHONE_X + 12
SCREEN_Y = PHONE_Y + 12
SCREEN_W = PHONE_W - 24
SCREEN_H = PHONE_H - 24


def draw_phone_frame(draw):
    """Draw a phone bezel around the content."""
    # Outer shadow
    draw.rounded_rectangle(
        [(PHONE_X-4, PHONE_Y-4), (PHONE_X+PHONE_W+4, PHONE_Y+PHONE_H+4)],
        radius=PHONE_R+4, fill=(15, 20, 35))
    # Phone body
    draw.rounded_rectangle(
        [(PHONE_X, PHONE_Y), (PHONE_X+PHONE_W, PHONE_Y+PHONE_H)],
        radius=PHONE_R, fill=(20, 20, 22))
    # Screen area
    draw.rounded_rectangle(
        [(SCREEN_X, SCREEN_Y), (SCREEN_X+SCREEN_W, SCREEN_Y+SCREEN_H)],
        radius=PHONE_R-8, fill=SITE_BG)


def draw_status_bar(draw, y_off=0):
    """Draw phone status bar."""
    f = ImageFont.truetype(EN_BOLD, 22)
    bar_y = SCREEN_Y + 8 + y_off
    draw.text((SCREEN_X+20, bar_y), "9:41", font=f, fill=SITE_TEXT)
    # Battery / signal icons (simple)
    bx = SCREEN_X + SCREEN_W - 80
    draw.rounded_rectangle([(bx, bar_y+4), (bx+30, bar_y+16)], radius=3, fill=SITE_TEXT)
    draw.rounded_rectangle([(bx+32, bar_y+7), (bx+35, bar_y+13)], radius=1, fill=SITE_TEXT)


def draw_nav_bar(draw, y_off=0):
    """Draw oilexam.tech navigation bar."""
    nav_y = SCREEN_Y + 40 + y_off
    nav_h = 56
    # Nav background
    draw.rectangle([(SCREEN_X, nav_y), (SCREEN_X+SCREEN_W, nav_y+nav_h)], fill=SITE_WHITE)
    # Bottom border
    draw.line([(SCREEN_X, nav_y+nav_h), (SCREEN_X+SCREEN_W, nav_y+nav_h)], fill=SITE_BORDER, width=1)

    f_logo = ImageFont.truetype(EN_BOLD, 28)
    f_nav = ImageFont.truetype(EN_REG, 20)

    draw.text((SCREEN_X+20, nav_y+14), "OilExam", font=f_logo, fill=SITE_BLUE)

    # Nav links
    links = ["Quiz", "Flashcards", "Pricing"]
    lx = SCREEN_X + 200
    for link in links:
        draw.text((lx, nav_y+18), link, font=f_nav, fill=SITE_TEXT_LIGHT)
        lx += 120

    # AR button
    draw.rounded_rectangle([(SCREEN_X+SCREEN_W-110, nav_y+12), (SCREEN_X+SCREEN_W-70, nav_y+42)],
                           radius=6, fill=SITE_BG)
    draw.text((SCREEN_X+SCREEN_W-104, nav_y+15), "AR", font=f_nav, fill=SITE_TEXT)

    # Sign in
    draw.rounded_rectangle([(SCREEN_X+SCREEN_W-60, nav_y+12), (SCREEN_X+SCREEN_W-10, nav_y+42)],
                           radius=6, fill=SITE_BLUE)
    f_tiny = ImageFont.truetype(EN_REG, 14)
    draw.text((SCREEN_X+SCREEN_W-55, nav_y+19), "Sign in", font=f_tiny, fill=SITE_WHITE)

    return nav_y + nav_h


def draw_hero_section(draw, y_start, scroll=0):
    """Draw the hero section of the landing page."""
    y = y_start - scroll + 30

    f_hero = ImageFont.truetype(EN_BOLD, 42)
    f_sub = ImageFont.truetype(EN_REG, 22)
    f_btn = ImageFont.truetype(EN_BOLD, 22)

    # Hero title
    cx = SCREEN_X + SCREEN_W // 2

    # "Master Your"
    t1 = "Master Your"
    bb1 = draw.textbbox((0,0), t1, font=f_hero)
    draw.text((cx - (bb1[2]-bb1[0])//2, y), t1, font=f_hero, fill=SITE_TEXT)

    # "English Oil Exam"
    t2 = "English Oil Exam"
    bb2 = draw.textbbox((0,0), t2, font=f_hero)
    draw.text((cx - (bb2[2]-bb2[0])//2, y+50), t2, font=f_hero, fill=SITE_BLUE)

    # Subtitle
    sub1 = "Interactive quizzes, flashcards, and"
    sub2 = "comprehensive study materials."
    f_sub_text = ImageFont.truetype(EN_REG, 20)
    bb_s1 = draw.textbbox((0,0), sub1, font=f_sub_text)
    bb_s2 = draw.textbbox((0,0), sub2, font=f_sub_text)
    draw.text((cx - (bb_s1[2]-bb_s1[0])//2, y+120), sub1, font=f_sub_text, fill=SITE_TEXT_LIGHT)
    draw.text((cx - (bb_s2[2]-bb_s2[0])//2, y+148), sub2, font=f_sub_text, fill=SITE_TEXT_LIGHT)

    # Buttons
    btn_y = y + 200
    # Subscribe Now
    bw1 = 220
    bx1 = cx - bw1 - 10
    draw.rounded_rectangle([(bx1, btn_y), (bx1+bw1, btn_y+48)], radius=10, fill=SITE_BLUE)
    bb_btn = draw.textbbox((0,0), "Subscribe Now", font=f_btn)
    draw.text((bx1 + (bw1-(bb_btn[2]-bb_btn[0]))//2, btn_y+12), "Subscribe Now", font=f_btn, fill=SITE_WHITE)

    # View Pricing
    bw2 = 180
    bx2 = cx + 10
    draw.rounded_rectangle([(bx2, btn_y), (bx2+bw2, btn_y+48)], radius=10, outline=SITE_BORDER, width=2)
    bb_vp = draw.textbbox((0,0), "View Pricing", font=f_btn)
    draw.text((bx2 + (bw2-(bb_vp[2]-bb_vp[0]))//2, btn_y+12), "View Pricing", font=f_btn, fill=SITE_TEXT)

    return y + 280


def draw_stats_section(draw, y_start, scroll=0):
    """Draw the stats cards."""
    y = y_start - scroll

    f_num = ImageFont.truetype(EN_BOLD, 36)
    f_label = ImageFont.truetype(EN_REG, 16)

    stats = [
        ("157", "Vocabulary\nQuestions", SITE_BLUE),
        ("29", "Reading\nPassages", (16, 185, 129)),
        ("159", "Phrasal\nVerbs", (168, 85, 247)),
        ("50", "Exam\nQuestions", (245, 158, 11)),
        ("130", "Grammar\nQuestions", (239, 68, 68)),
    ]

    # Two rows layout
    card_w = (SCREEN_W - 60) // 3
    card_h = 100
    for i, (num, label, color) in enumerate(stats):
        row = i // 3
        col = i % 3
        if i >= 3:
            col = i - 3
            card_w_2 = (SCREEN_W - 50) // 2
            cx = SCREEN_X + 20 + col * (card_w_2 + 10)
            cw = card_w_2
        else:
            cx = SCREEN_X + 20 + col * (card_w + 10)
            cw = card_w
        cy = y + row * (card_h + 12)

        draw.rounded_rectangle([(cx, cy), (cx+cw, cy+card_h)], radius=12, fill=SITE_WHITE)
        # Number
        nb = draw.textbbox((0,0), num, font=f_num)
        draw.text((cx + (cw-(nb[2]-nb[0]))//2, cy+10), num, font=f_num, fill=color)
        # Label (first line only for space)
        first_line = label.split('\n')[0]
        lb = draw.textbbox((0,0), first_line, font=f_label)
        draw.text((cx + (cw-(lb[2]-lb[0]))//2, cy+60), first_line, font=f_label, fill=SITE_TEXT_LIGHT)

    return y + card_h * 2 + 30


def draw_features_section(draw, y_start, scroll=0):
    """Draw the features section."""
    y = y_start - scroll

    f_title = ImageFont.truetype(EN_BOLD, 30)
    f_sub = ImageFont.truetype(EN_REG, 18)
    f_feat_title = ImageFont.truetype(EN_BOLD, 22)
    f_feat_desc = ImageFont.truetype(EN_REG, 16)

    cx = SCREEN_X + SCREEN_W // 2

    t = "Everything You Need"
    bb = draw.textbbox((0,0), t, font=f_title)
    draw.text((cx-(bb[2]-bb[0])//2, y), t, font=f_title, fill=SITE_TEXT)

    t2 = "to Succeed"
    bb2 = draw.textbbox((0,0), t2, font=f_title)
    draw.text((cx-(bb2[2]-bb2[0])//2, y+38), t2, font=f_title, fill=SITE_TEXT)

    features = [
        ("Interactive Quizzes", "Test your knowledge with\nmultiple-choice questions.\nGet instant feedback.", SITE_BLUE),
        ("Flashcards", "Study phrasal verbs with\nflip cards. English front,\nArabic back.", (16, 185, 129)),
        ("Progress Tracking", "Track your scores and\nimprovement over time.", (168, 85, 247)),
    ]

    for i, (title, desc, color) in enumerate(features):
        fy = y + 100 + i * 170
        # Card
        draw.rounded_rectangle(
            [(SCREEN_X+15, fy), (SCREEN_X+SCREEN_W-15, fy+150)],
            radius=14, fill=SITE_WHITE)
        # Color accent
        draw.rounded_rectangle(
            [(SCREEN_X+15, fy), (SCREEN_X+21, fy+150)],
            radius=4, fill=color)
        # Icon circle
        draw.ellipse([(SCREEN_X+40, fy+15), (SCREEN_X+80, fy+55)], fill=lerp_color(color, SITE_WHITE, 0.7))
        draw.ellipse([(SCREEN_X+50, fy+25), (SCREEN_X+70, fy+45)], fill=color)

        draw.text((SCREEN_X+95, fy+20), title, font=f_feat_title, fill=SITE_TEXT)
        # Description (first line)
        first_line = desc.split('\n')[0]
        draw.text((SCREEN_X+95, fy+55), first_line, font=f_feat_desc, fill=SITE_TEXT_LIGHT)
        second_line = desc.split('\n')[1] if '\n' in desc else ""
        if second_line:
            draw.text((SCREEN_X+95, fy+78), second_line, font=f_feat_desc, fill=SITE_TEXT_LIGHT)

    return y + 100 + 3*170 + 20


def draw_whatsapp_btn(draw):
    """Draw WhatsApp floating button."""
    bx = SCREEN_X + SCREEN_W - 70
    by = SCREEN_Y + SCREEN_H - 70
    draw.ellipse([(bx, by), (bx+50, by+50)], fill=WA_GREEN)
    # Simple chat icon
    f_wa = ImageFont.truetype(EN_BOLD, 28)
    draw.text((bx+13, by+10), "W", font=f_wa, fill=SITE_WHITE)


def draw_cursor(draw, x, y, size=20):
    """Draw a cursor/touch indicator."""
    draw.ellipse([(x-size, y-size), (x+size, y+size)],
                 fill=lerp_color(SITE_BLUE, SITE_WHITE, 0.5), outline=SITE_BLUE, width=2)
    # Inner dot
    draw.ellipse([(x-5, y-5), (x+5, y+5)], fill=SITE_BLUE)


# ════════════════════════════════════════════
#  QUIZ UI SIMULATION
# ════════════════════════════════════════════

def draw_quiz_ui(draw, y_off, question_p=0, selected=-1, show_correct=False):
    """Draw a quiz question UI."""
    y = SCREEN_Y + 100 + y_off

    f_q_num = ImageFont.truetype(EN_BOLD, 18)
    f_question = ImageFont.truetype(EN_BOLD, 24)
    f_option = ImageFont.truetype(EN_REG, 20)

    # Question card
    draw.rounded_rectangle(
        [(SCREEN_X+15, y), (SCREEN_X+SCREEN_W-15, y+120)],
        radius=14, fill=SITE_WHITE)

    draw.text((SCREEN_X+30, y+15), "Question 1 of 50", font=f_q_num, fill=SITE_TEXT_LIGHT)
    draw.text((SCREEN_X+30, y+45), "What does \"downstream\"", font=f_question, fill=SITE_TEXT)
    draw.text((SCREEN_X+30, y+75), "mean in the oil industry?", font=f_question, fill=SITE_TEXT)

    # Progress bar
    pb_y = y - 30
    draw.rounded_rectangle([(SCREEN_X+15, pb_y), (SCREEN_X+SCREEN_W-15, pb_y+8)],
                           radius=4, fill=SITE_BORDER)
    draw.rounded_rectangle([(SCREEN_X+15, pb_y), (SCREEN_X+15+int(SCREEN_W*0.02), pb_y+8)],
                           radius=4, fill=SITE_BLUE)

    # Options
    options = [
        "A) Refining & Distribution",
        "B) Drilling & Exploration",
        "C) Pipeline Construction",
        "D) Well Maintenance",
    ]

    for i, opt in enumerate(options):
        oy = y + 150 + i * 80
        if show_correct and i == 0:
            bg = (220, 252, 231)  # green-100
            border = SITE_GREEN
        elif show_correct and i == selected and i != 0:
            bg = (254, 226, 226)  # red-100
            border = SITE_RED_BADGE
        elif i == selected:
            bg = (219, 234, 254)  # blue-100
            border = SITE_BLUE
        else:
            bg = SITE_WHITE
            border = SITE_BORDER

        draw.rounded_rectangle(
            [(SCREEN_X+15, oy), (SCREEN_X+SCREEN_W-15, oy+60)],
            radius=12, fill=bg, outline=border, width=2)
        draw.text((SCREEN_X+35, oy+18), opt, font=f_option, fill=SITE_TEXT)

        if show_correct and i == 0:
            draw.text((SCREEN_X+SCREEN_W-55, oy+18), "✓", font=f_option, fill=SITE_GREEN)


# ════════════════════════════════════════════
#  FLASHCARD UI SIMULATION
# ════════════════════════════════════════════

def draw_flashcard_ui(draw, y_off, flip_progress=0):
    """Draw a flashcard UI."""
    y = SCREEN_Y + 120 + y_off

    f_cat = ImageFont.truetype(EN_BOLD, 20)
    f_word = ImageFont.truetype(EN_BOLD, 48)
    f_ar_word = ImageFont.truetype(AR_BLACK, 52)
    f_hint = ImageFont.truetype(EN_REG, 18)
    f_btn = ImageFont.truetype(EN_BOLD, 20)

    # Category badge
    draw.rounded_rectangle([(SCREEN_X+15, y-50), (SCREEN_X+200, y-15)],
                           radius=8, fill=SITE_BLUE)
    draw.text((SCREEN_X+30, y-45), "Phrasal Verbs", font=f_cat, fill=SITE_WHITE)

    # Counter
    draw.text((SCREEN_X+SCREEN_W-120, y-45), "1 / 159", font=f_cat, fill=SITE_TEXT_LIGHT)

    # Card
    card_h = 350
    if flip_progress < 0.5:
        # English side
        scale = 1 - flip_progress * 2
        card_cx = SCREEN_X + SCREEN_W // 2
        half_w = int((SCREEN_W // 2 - 20) * max(0.02, scale))
        draw.rounded_rectangle(
            [(card_cx - half_w, y), (card_cx + half_w, y + card_h)],
            radius=20, fill=SITE_WHITE)
        if scale > 0.3:
            # English word
            word = "Break down"
            bb = draw.textbbox((0,0), word, font=f_word)
            tw = bb[2]-bb[0]
            draw.text((card_cx-tw//2, y+130), word, font=f_word, fill=SITE_TEXT)
            # Hint
            hint = "Tap to flip"
            hb = draw.textbbox((0,0), hint, font=f_hint)
            draw.text((card_cx-(hb[2]-hb[0])//2, y+250), hint, font=f_hint, fill=SITE_TEXT_LIGHT)
    else:
        # Arabic side
        scale = (flip_progress - 0.5) * 2
        card_cx = SCREEN_X + SCREEN_W // 2
        half_w = int((SCREEN_W // 2 - 20) * max(0.02, scale))
        draw.rounded_rectangle(
            [(card_cx - half_w, y), (card_cx + half_w, y + card_h)],
            radius=20, fill=(239, 246, 255))
        if scale > 0.3:
            word = "يعطّل / يفكّك"
            bb = draw.textbbox((0,0), word, font=f_ar_word)
            tw = bb[2]-bb[0]
            draw.text((card_cx-tw//2, y+130), word, font=f_ar_word, fill=SITE_TEXT)
            eng = "Break down"
            eb = draw.textbbox((0,0), eng, font=f_hint)
            draw.text((card_cx-(eb[2]-eb[0])//2, y+220), eng, font=f_hint, fill=SITE_TEXT_LIGHT)

    # Action buttons below card
    btn_y = y + card_h + 30
    # "Needs Review" red
    bw = (SCREEN_W - 50) // 2
    draw.rounded_rectangle([(SCREEN_X+15, btn_y), (SCREEN_X+15+bw, btn_y+50)],
                           radius=10, fill=(254, 226, 226))
    bb_r = draw.textbbox((0,0), "Needs Review", font=f_btn)
    draw.text((SCREEN_X+15+(bw-(bb_r[2]-bb_r[0]))//2, btn_y+14), "Needs Review", font=f_btn, fill=SITE_RED_BADGE)

    # "I Know This" green
    draw.rounded_rectangle([(SCREEN_X+25+bw, btn_y), (SCREEN_X+25+bw*2, btn_y+50)],
                           radius=10, fill=(220, 252, 231))
    bb_g = draw.textbbox((0,0), "I Know This", font=f_btn)
    draw.text((SCREEN_X+25+bw+(bw-(bb_g[2]-bb_g[0]))//2, btn_y+14), "I Know This", font=f_btn, fill=(22, 163, 74))


# ════════════════════════════════════════════
#  SCENES
# ════════════════════════════════════════════

_particles = create_floating_particles(12, seed=55)

def scene_intro(p):
    """Branded intro."""
    return branded_intro(p)


def scene_landing_page(p):
    """Show the landing page with scroll."""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARKER_BG)
    draw = ImageDraw.Draw(img)

    draw_phone_frame(draw)

    # Clip area
    scroll = int(ease_in_out(max(0, (p - 0.4) / 0.6)) * 300)

    draw_status_bar(draw)
    nav_bottom = draw_nav_bar(draw)
    draw_hero_section(draw, nav_bottom, scroll)
    stats_bottom = draw_stats_section(draw, nav_bottom + 290, scroll)
    draw_whatsapp_btn(draw)

    # Subtle scroll indicator
    if p < 0.35:
        a = 0.5 + 0.5 * math.sin(p * 8)
        indicator_y = SCREEN_Y + SCREEN_H - 30
        c = lerp_color(SITE_BG, SITE_TEXT_LIGHT, a)
        f_scroll = ImageFont.truetype(EN_REG, 16)
        t = "scroll down"
        bb = draw.textbbox((0,0), t, font=f_scroll)
        draw.text((SCREEN_X + SCREEN_W//2 - (bb[2]-bb[0])//2, indicator_y), t, font=f_scroll, fill=c)

    return img


def scene_landing_features(p):
    """Continue scrolling to features section."""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARKER_BG)
    draw = ImageDraw.Draw(img)

    draw_phone_frame(draw)

    scroll = 300 + int(ease_in_out(p) * 500)

    draw_status_bar(draw)
    draw_nav_bar(draw)
    nav_bottom = SCREEN_Y + 96
    draw_hero_section(draw, nav_bottom, scroll)
    stats_bottom = draw_stats_section(draw, nav_bottom + 290, scroll)
    draw_features_section(draw, stats_bottom + 30, scroll - 300)
    draw_whatsapp_btn(draw)

    return img


def scene_quiz_browse(p):
    """Show quiz interface - browsing a question."""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARKER_BG)
    draw = ImageDraw.Draw(img)

    draw_phone_frame(draw)
    draw_status_bar(draw)
    draw_nav_bar(draw)

    # Quiz UI
    draw_quiz_ui(draw, 0, p, selected=-1)

    # Cursor moving to option A
    if p > 0.6:
        cursor_p = (p - 0.6) / 0.4
        cx = SCREEN_X + SCREEN_W // 2
        cy_start = SCREEN_Y + 500
        cy_end = SCREEN_Y + 280
        cy = int(cy_start + (cy_end - cy_start) * ease_out(cursor_p))
        draw_cursor(draw, cx, cy)

    draw_whatsapp_btn(draw)
    return img


def scene_quiz_answer(p):
    """Show selecting answer and getting it correct."""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARKER_BG)
    draw = ImageDraw.Draw(img)

    draw_phone_frame(draw)
    draw_status_bar(draw)
    draw_nav_bar(draw)

    if p < 0.3:
        # Selected option A
        draw_quiz_ui(draw, 0, 1, selected=0, show_correct=False)
        draw_cursor(draw, SCREEN_X + SCREEN_W // 2, SCREEN_Y + 280)
    else:
        # Show correct
        draw_quiz_ui(draw, 0, 1, selected=0, show_correct=True)

        # Correct banner
        if p > 0.4:
            a = min(1, (p - 0.4) * 4)
            banner_y = SCREEN_Y + SCREEN_H - 120
            bc = lerp_color(SITE_BG, (220, 252, 231), a)
            draw.rounded_rectangle(
                [(SCREEN_X+15, banner_y), (SCREEN_X+SCREEN_W-15, banner_y+60)],
                radius=12, fill=bc)
            f_correct = ImageFont.truetype(EN_BOLD, 24)
            tc = lerp_color(SITE_BG, (22, 163, 74), a)
            bb = draw.textbbox((0,0), "Correct! Well done!", font=f_correct)
            draw.text((SCREEN_X + SCREEN_W//2 - (bb[2]-bb[0])//2, banner_y+16),
                      "Correct! Well done!", font=f_correct, fill=tc)

    draw_whatsapp_btn(draw)
    return img


def scene_flashcard(p):
    """Show flashcard with flip animation."""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARKER_BG)
    draw = ImageDraw.Draw(img)

    draw_phone_frame(draw)
    draw_status_bar(draw)
    draw_nav_bar(draw)

    # Flip timing
    if p < 0.4:
        flip = 0
    elif p < 0.6:
        flip = (p - 0.4) / 0.2
    else:
        flip = 1.0

    draw_flashcard_ui(draw, 0, flip)

    # Tap indicator
    if 0.3 < p < 0.5:
        draw_cursor(draw, SCREEN_X + SCREEN_W // 2, SCREEN_Y + 350)

    draw_whatsapp_btn(draw)
    return img


def scene_results(p):
    """Show progress/results screen."""
    img = Image.new('RGB', (WIDTH, HEIGHT), DARKER_BG)
    draw = ImageDraw.Draw(img)

    draw_phone_frame(draw)
    draw_status_bar(draw)
    draw_nav_bar(draw)

    y = SCREEN_Y + 110

    f_title = ImageFont.truetype(EN_BOLD, 28)
    f_score = ImageFont.truetype(EN_BOLD, 72)
    f_label = ImageFont.truetype(EN_REG, 20)
    f_cat = ImageFont.truetype(EN_BOLD, 20)
    f_pct = ImageFont.truetype(EN_BOLD, 20)

    # Title
    draw.text((SCREEN_X+20, y), "Your Progress", font=f_title, fill=SITE_TEXT)

    # Score circle
    circle_cx = SCREEN_X + SCREEN_W // 2
    circle_cy = y + 150
    circle_r = 80

    # Background ring
    draw.ellipse([(circle_cx-circle_r, circle_cy-circle_r),
                  (circle_cx+circle_r, circle_cy+circle_r)],
                 outline=SITE_BORDER, width=10)

    # Fill ring
    score = int(92 * ease_out(min(1, p * 2)))
    fill_angle = int(360 * score / 100)
    # Approximate with arc segments
    for deg in range(fill_angle):
        angle = math.radians(deg - 90)
        x = circle_cx + int(math.cos(angle) * circle_r)
        y_pt = circle_cy + int(math.sin(angle) * circle_r)
        draw.ellipse([(x-5, y_pt-5), (x+5, y_pt+5)], fill=SITE_GREEN)

    # Score text
    score_str = f"{score}%"
    sb = draw.textbbox((0,0), score_str, font=f_score)
    draw.text((circle_cx-(sb[2]-sb[0])//2, circle_cy-30), score_str, font=f_score, fill=SITE_TEXT)

    # Category bars
    categories = [
        ("Vocabulary", 88, SITE_BLUE),
        ("Phrasal Verbs", 91, (168, 85, 247)),
        ("Grammar", 95, (245, 158, 11)),
        ("Reading", 85, (16, 185, 129)),
    ]

    bar_start_y = y + 290
    for i, (cat, target, color) in enumerate(categories):
        by = bar_start_y + i * 80
        cur = int(target * ease_out(min(1, max(0, (p - 0.2 - i*0.1)) * 3)))

        draw.text((SCREEN_X+20, by), cat, font=f_cat, fill=SITE_TEXT)
        draw.text((SCREEN_X+SCREEN_W-60, by), f"{cur}%", font=f_pct, fill=color)

        # Bar
        bar_y = by + 30
        bar_w = SCREEN_W - 40
        draw.rounded_rectangle([(SCREEN_X+20, bar_y), (SCREEN_X+20+bar_w, bar_y+12)],
                               radius=6, fill=SITE_BORDER)
        fill_w = int(bar_w * cur / 100)
        if fill_w > 6:
            draw.rounded_rectangle([(SCREEN_X+20, bar_y), (SCREEN_X+20+fill_w, bar_y+12)],
                                   radius=6, fill=color)

    draw_whatsapp_btn(draw)
    return img


def scene_outro(p):
    """Branded outro."""
    return branded_outro(p)


# ════════════════════════════════════════════
#  BUILD
# ════════════════════════════════════════════

def main():
    print("+" + "="*54 + "+")
    print("|  OilExam.tech - Site Demo Reel                       |")
    print("|  Simulated screen recording of the live website      |")
    print("+" + "="*54 + "+")

    out_dir = "/root/OilexamVideo"

    build_video("site_demo", [
        ("Branded Intro",       scene_intro,           2.0),
        ("Landing Page",        scene_landing_page,    4.0),
        ("Features Scroll",     scene_landing_features,3.0),
        ("Quiz - Browse",       scene_quiz_browse,     3.5),
        ("Quiz - Answer",       scene_quiz_answer,     3.5),
        ("Flashcard Flip",      scene_flashcard,       4.0),
        ("Results / Progress",  scene_results,         4.0),
        ("Branded Outro",       scene_outro,           4.0),
    ], f"{out_dir}/pro_reel_site_demo.mp4")

    print("\n  SITE DEMO REEL COMPLETE!")


if __name__ == "__main__":
    main()
