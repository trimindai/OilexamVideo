#!/usr/bin/env python3
"""
OilExam.tech - Realistic iPhone Screen Recording
Looks like a real person holding an iPhone and using the app.
Natural scrolling, tapping with touch ripples, realistic iOS UI.
"""

from pro_utils import *
from PIL import ImageFilter

# ═══ iOS COLORS ═══
IOS_BG = (242, 242, 247)          # iOS system gray6
IOS_WHITE = (255, 255, 255)
IOS_BLACK = (0, 0, 0)
IOS_BLUE = (0, 122, 255)          # iOS system blue
IOS_GREEN = (52, 199, 89)         # iOS system green
IOS_RED = (255, 59, 48)           # iOS system red
IOS_ORANGE = (255, 149, 0)
IOS_PURPLE = (175, 82, 222)
IOS_GRAY = (142, 142, 147)        # iOS system gray
IOS_GRAY2 = (174, 174, 178)
IOS_GRAY3 = (199, 199, 204)
IOS_GRAY4 = (209, 209, 214)
IOS_GRAY5 = (229, 229, 234)
IOS_GRAY6 = (242, 242, 247)
IOS_LABEL = (0, 0, 0)
IOS_SECONDARY = (60, 60, 67)
IOS_TERTIARY = (99, 99, 102)
SITE_BLUE = (59, 130, 246)
SITE_DARK_BLUE = (37, 99, 235)
WA_GREEN = (37, 211, 102)

# Screen dimensions (full bleed - no phone frame, like a real screen recording)
SW, SH = WIDTH, HEIGHT


def draw_ios_status_bar(draw, time_str="9:41", dark=False):
    """Realistic iOS 18 status bar."""
    fg = IOS_WHITE if dark else IOS_BLACK
    y = 14
    # Time
    f_time = ImageFont.truetype(EN_BOLD, 30)
    draw.text((32, y), time_str, font=f_time, fill=fg)

    # Right side icons
    rx = SW - 36
    # Battery
    draw.rounded_rectangle([(rx-44, y+6), (rx-4, y+22)], radius=4, outline=fg, width=2)
    draw.rounded_rectangle([(rx-40, y+9), (rx-10, y+19)], radius=2, fill=fg)
    draw.rounded_rectangle([(rx-2, y+10), (rx, y+18)], radius=1, fill=fg)
    # Signal dots
    for i in range(4):
        bh = 6 + i * 3
        bx = rx - 100 + i * 10
        by = y + 22 - bh
        draw.rounded_rectangle([(bx, by), (bx+6, y+22)], radius=2, fill=fg)
    # WiFi (simple arc)
    wx = rx - 66
    for i in range(3):
        r = 6 + i * 5
        draw.arc([(wx-r, y+20-r), (wx+r, y+20)], start=220, end=320, fill=fg, width=2)


def draw_safari_bar(draw, url="oilexam.tech", y=54, scroll_progress=0):
    """iOS Safari address bar."""
    bar_h = 44
    # Compact when scrolled
    if scroll_progress > 0.2:
        bar_h = 36
        y = 50

    draw.rounded_rectangle([(12, y), (SW-12, y+bar_h)], radius=12, fill=IOS_GRAY6)

    f_url = ImageFont.truetype(EN_REG, 17 if bar_h < 44 else 19)
    # Lock icon (simple)
    lock_x = SW//2 - 60
    draw.rounded_rectangle([(lock_x, y+14), (lock_x+10, y+24)], radius=2, outline=IOS_TERTIARY, width=1)
    draw.rounded_rectangle([(lock_x-2, y+20), (lock_x+12, y+30)], radius=2, fill=IOS_TERTIARY)

    bb = draw.textbbox((0,0), url, font=f_url)
    tw = bb[2]-bb[0]
    draw.text((SW//2 - tw//2 + 10, y + (bar_h-20)//2), url, font=f_url, fill=IOS_BLACK)

    return y + bar_h


def draw_touch_ripple(draw, x, y, p, max_r=45):
    """Realistic iOS touch ripple effect."""
    if p <= 0 or p >= 1:
        return
    r = int(max_r * ease_out(p))
    alpha = max(0, 0.35 * (1 - p))
    c = lerp_color(IOS_WHITE, IOS_GRAY3, alpha)
    draw.ellipse([(x-r, y-r), (x+r, y+r)], fill=c)
    # Inner dot
    inner_r = max(1, int(8 * (1 - p)))
    ic = lerp_color(IOS_WHITE, IOS_GRAY, 0.3 * (1 - p))
    draw.ellipse([(x-inner_r, y-inner_r), (x+inner_r, y+inner_r)], fill=ic)


def draw_ios_home_bar(draw, y=None):
    """iOS home indicator bar at bottom."""
    if y is None:
        y = SH - 18
    bar_w = 140
    bx = (SW - bar_w) // 2
    draw.rounded_rectangle([(bx, y), (bx+bar_w, y+5)], radius=3, fill=IOS_BLACK)


# ════════════════════════════════════════════
#  WEBSITE CONTENT DRAWING
# ════════════════════════════════════════════

def draw_site_content(draw, scroll, touch_x=-1, touch_y=-1, touch_p=-1):
    """Draw the full oilexam.tech website content with scroll offset."""
    y = 105 - scroll

    f_logo = ImageFont.truetype(EN_BOLD, 26)
    f_nav = ImageFont.truetype(EN_REG, 17)
    f_hero_big = ImageFont.truetype(EN_BOLD, 38)
    f_hero_blue = ImageFont.truetype(EN_BOLD, 40)
    f_sub = ImageFont.truetype(EN_REG, 18)
    f_btn = ImageFont.truetype(EN_BOLD, 18)
    f_stat_num = ImageFont.truetype(EN_BOLD, 34)
    f_stat_label = ImageFont.truetype(EN_REG, 13)
    f_section_title = ImageFont.truetype(EN_BOLD, 28)
    f_section_sub = ImageFont.truetype(EN_REG, 16)
    f_feat_title = ImageFont.truetype(EN_BOLD, 20)
    f_feat_desc = ImageFont.truetype(EN_REG, 15)
    f_cta_title = ImageFont.truetype(EN_BOLD, 32)
    f_cta_sub = ImageFont.truetype(EN_REG, 16)
    f_footer = ImageFont.truetype(EN_REG, 14)

    # ─── Nav Bar (sticky) ───
    nav_y = max(54, 54)
    # White nav background
    draw.rectangle([(0, 54), (SW, 105)], fill=IOS_WHITE)
    draw.line([(0, 105), (SW, 105)], fill=IOS_GRAY5, width=1)
    draw.text((24, 68), "OilExam", font=f_logo, fill=SITE_BLUE)

    nav_links = [("Quiz", 340), ("Flashcards", 430), ("Pricing", 550)]
    for text, x in nav_links:
        draw.text((x, 72), text, font=f_nav, fill=IOS_TERTIARY)

    # AR button
    draw.rounded_rectangle([(680, 66), (720, 92)], radius=8, fill=IOS_GRAY6)
    f_ar = ImageFont.truetype(EN_REG, 15)
    draw.text((690, 71), "AR", font=f_ar, fill=IOS_BLACK)

    # Sign in
    draw.rounded_rectangle([(740, 64), (830, 94)], radius=8, fill=SITE_BLUE)
    f_sign = ImageFont.truetype(EN_BOLD, 14)
    draw.text((756, 72), "Sign in", font=f_sign, fill=IOS_WHITE)

    # ─── Hero Section ───
    hero_y = y + 40
    cx = SW // 2

    t1 = "Master Your"
    bb1 = draw.textbbox((0,0), t1, font=f_hero_big)
    draw.text((cx - (bb1[2]-bb1[0])//2, hero_y), t1, font=f_hero_big, fill=IOS_BLACK)

    t2 = "English Oil Exam"
    bb2 = draw.textbbox((0,0), t2, font=f_hero_blue)
    draw.text((cx - (bb2[2]-bb2[0])//2, hero_y+48), t2, font=f_hero_blue, fill=SITE_BLUE)

    sub_lines = [
        "Interactive quizzes, flashcards, and",
        "comprehensive study materials.",
    ]
    for i, line in enumerate(sub_lines):
        bb = draw.textbbox((0,0), line, font=f_sub)
        draw.text((cx-(bb[2]-bb[0])//2, hero_y+115+i*26), line, font=f_sub, fill=IOS_TERTIARY)

    # Buttons
    btn_y = hero_y + 190
    # Subscribe Now
    bw1 = 200
    bx1 = cx - bw1 - 10
    draw.rounded_rectangle([(bx1, btn_y), (bx1+bw1, btn_y+48)], radius=12, fill=SITE_BLUE)
    bb_s = draw.textbbox((0,0), "Subscribe Now", font=f_btn)
    draw.text((bx1+(bw1-(bb_s[2]-bb_s[0]))//2, btn_y+14), "Subscribe Now", font=f_btn, fill=IOS_WHITE)

    # View Pricing
    bw2 = 170
    bx2 = cx + 10
    draw.rounded_rectangle([(bx2, btn_y), (bx2+bw2, btn_y+48)], radius=12, outline=IOS_GRAY4, width=2)
    bb_v = draw.textbbox((0,0), "View Pricing", font=f_btn)
    draw.text((bx2+(bw2-(bb_v[2]-bb_v[0]))//2, btn_y+14), "View Pricing", font=f_btn, fill=IOS_BLACK)

    # ─── Stats Section ───
    stats_y = hero_y + 280
    stats = [
        ("157", "Vocabulary", SITE_BLUE),
        ("29", "Reading", IOS_GREEN),
        ("159", "Phrasal Verbs", IOS_PURPLE),
    ]
    stats2 = [
        ("50", "Exam Qs", IOS_ORANGE),
        ("130", "Grammar", IOS_RED),
    ]

    card_w = (SW - 72) // 3
    for i, (num, label, color) in enumerate(stats):
        cx_card = 24 + i * (card_w + 12)
        draw.rounded_rectangle([(cx_card, stats_y), (cx_card+card_w, stats_y+90)],
                               radius=14, fill=IOS_WHITE)
        nb = draw.textbbox((0,0), num, font=f_stat_num)
        draw.text((cx_card+(card_w-(nb[2]-nb[0]))//2, stats_y+12), num, font=f_stat_num, fill=color)
        lb = draw.textbbox((0,0), label, font=f_stat_label)
        draw.text((cx_card+(card_w-(lb[2]-lb[0]))//2, stats_y+58), label, font=f_stat_label, fill=IOS_TERTIARY)

    card_w2 = (SW - 60) // 2
    for i, (num, label, color) in enumerate(stats2):
        cx_card = 24 + i * (card_w2 + 12)
        draw.rounded_rectangle([(cx_card, stats_y+105), (cx_card+card_w2, stats_y+195)],
                               radius=14, fill=IOS_WHITE)
        nb = draw.textbbox((0,0), num, font=f_stat_num)
        draw.text((cx_card+(card_w2-(nb[2]-nb[0]))//2, stats_y+117), num, font=f_stat_num, fill=color)
        lb = draw.textbbox((0,0), label, font=f_stat_label)
        draw.text((cx_card+(card_w2-(lb[2]-lb[0]))//2, stats_y+163), label, font=f_stat_label, fill=IOS_TERTIARY)

    # ─── Features Section ───
    feat_y = stats_y + 240

    t = "Everything You Need"
    bb = draw.textbbox((0,0), t, font=f_section_title)
    draw.text((SW//2-(bb[2]-bb[0])//2, feat_y), t, font=f_section_title, fill=IOS_BLACK)
    t2 = "to Succeed"
    bb2 = draw.textbbox((0,0), t2, font=f_section_title)
    draw.text((SW//2-(bb2[2]-bb2[0])//2, feat_y+35), t2, font=f_section_title, fill=IOS_BLACK)

    st = "All the tools to ace your exam."
    bbs = draw.textbbox((0,0), st, font=f_section_sub)
    draw.text((SW//2-(bbs[2]-bbs[0])//2, feat_y+78), st, font=f_section_sub, fill=IOS_TERTIARY)

    features = [
        ("Interactive Quizzes", "Multiple-choice questions across\nvocabulary, reading, and grammar.", SITE_BLUE, "Q"),
        ("Flashcards", "Phrasal verbs with flip cards.\nEnglish front, Arabic back.", IOS_GREEN, "F"),
        ("Progress Tracking", "Track scores and improvement.\nKnow which topics need practice.", IOS_PURPLE, "P"),
    ]

    for i, (title, desc, color, icon_letter) in enumerate(features):
        fy = feat_y + 120 + i * 150
        # Card
        draw.rounded_rectangle([(24, fy), (SW-24, fy+130)], radius=16, fill=IOS_WHITE)

        # Icon circle
        draw.ellipse([(44, fy+20), (84, fy+60)], fill=lerp_color(color, IOS_WHITE, 0.75))
        f_icon = ImageFont.truetype(EN_BOLD, 24)
        ib = draw.textbbox((0,0), icon_letter, font=f_icon)
        draw.text((64-(ib[2]-ib[0])//2, fy+28), icon_letter, font=f_icon, fill=color)

        draw.text((100, fy+18), title, font=f_feat_title, fill=IOS_BLACK)
        lines = desc.split('\n')
        for j, line in enumerate(lines):
            draw.text((100, fy+50+j*22), line, font=f_feat_desc, fill=IOS_TERTIARY)

    # ─── CTA Section ───
    cta_y = feat_y + 120 + 3*150 + 30
    draw.rounded_rectangle([(24, cta_y), (SW-24, cta_y+200)], radius=20, fill=SITE_BLUE)

    ct1 = "Ready to Start Studying?"
    bbc = draw.textbbox((0,0), ct1, font=f_cta_title)
    draw.text((SW//2-(bbc[2]-bbc[0])//2, cta_y+30), ct1, font=f_cta_title, fill=IOS_WHITE)

    ct2 = "Join now and get access to all"
    ct3 = "study materials and quizzes."
    bbc2 = draw.textbbox((0,0), ct2, font=f_cta_sub)
    bbc3 = draw.textbbox((0,0), ct3, font=f_cta_sub)
    draw.text((SW//2-(bbc2[2]-bbc2[0])//2, cta_y+80), ct2, font=f_cta_sub, fill=lerp_color(SITE_BLUE, IOS_WHITE, 0.85))
    draw.text((SW//2-(bbc3[2]-bbc3[0])//2, cta_y+103), ct3, font=f_cta_sub, fill=lerp_color(SITE_BLUE, IOS_WHITE, 0.85))

    # Subscribe button inside CTA
    sub_bw = 220
    sub_bx = (SW-sub_bw)//2
    sub_by = cta_y + 140
    draw.rounded_rectangle([(sub_bx, sub_by), (sub_bx+sub_bw, sub_by+44)], radius=10, fill=IOS_WHITE)
    bbs2 = draw.textbbox((0,0), "Subscribe Now", font=f_btn)
    draw.text((SW//2-(bbs2[2]-bbs2[0])//2, sub_by+12), "Subscribe Now", font=f_btn, fill=SITE_BLUE)

    # ─── Footer ───
    footer_y = cta_y + 240
    draw.rectangle([(0, footer_y), (SW, footer_y+80)], fill=IOS_WHITE)
    draw.line([(0, footer_y), (SW, footer_y)], fill=IOS_GRAY5, width=1)
    ft1 = "Powered by Trimind Company"
    bbf = draw.textbbox((0,0), ft1, font=f_footer)
    draw.text((SW//2-(bbf[2]-bbf[0])//2, footer_y+15), ft1, font=f_footer, fill=IOS_TERTIARY)
    ft2 = "© 2026 OilExam. All rights reserved."
    bbf2 = draw.textbbox((0,0), ft2, font=f_footer)
    draw.text((SW//2-(bbf2[2]-bbf2[0])//2, footer_y+40), ft2, font=f_footer, fill=IOS_GRAY2)

    # ─── WhatsApp button ───
    wa_x, wa_y = SW - 72, max(SH - 90, footer_y - 60) + scroll
    draw.ellipse([(wa_x, wa_y), (wa_x+52, wa_y+52)], fill=WA_GREEN)
    f_wa = ImageFont.truetype(EN_BOLD, 28)
    draw.text((wa_x+14, wa_y+11), "W", font=f_wa, fill=IOS_WHITE)

    # Touch ripple
    if touch_x > 0 and touch_p > 0:
        draw_touch_ripple(draw, touch_x, touch_y, touch_p)


def draw_quiz_page(draw, scroll, selected=-1, show_result=False, touch_x=-1, touch_y=-1, touch_p=-1):
    """Draw the quiz page."""
    y = 105 - scroll

    f_cat_title = ImageFont.truetype(EN_BOLD, 24)
    f_q_num = ImageFont.truetype(EN_REG, 15)
    f_question = ImageFont.truetype(EN_BOLD, 22)
    f_option = ImageFont.truetype(EN_REG, 19)
    f_feedback = ImageFont.truetype(EN_BOLD, 20)

    # Back nav area
    draw.rectangle([(0, 54), (SW, 105)], fill=IOS_WHITE)
    draw.line([(0, 105), (SW, 105)], fill=IOS_GRAY5, width=1)
    f_back = ImageFont.truetype(EN_REG, 17)
    draw.text((24, 72), "< Back", font=f_back, fill=SITE_BLUE)
    f_page_title = ImageFont.truetype(EN_BOLD, 20)
    bb = draw.textbbox((0,0), "Vocabulary Quiz", font=f_page_title)
    draw.text((SW//2-(bb[2]-bb[0])//2, 72), "Vocabulary Quiz", font=f_page_title, fill=IOS_BLACK)

    # Progress bar
    pb_y = y + 10
    draw.rounded_rectangle([(24, pb_y), (SW-24, pb_y+6)], radius=3, fill=IOS_GRAY5)
    draw.rounded_rectangle([(24, pb_y), (24+int((SW-48)*0.02), pb_y+6)], radius=3, fill=SITE_BLUE)

    # Question number
    draw.text((24, pb_y+16), "Question 1 of 50", font=f_q_num, fill=IOS_TERTIARY)

    # Question card
    qy = pb_y + 50
    draw.rounded_rectangle([(20, qy), (SW-20, qy+130)], radius=16, fill=IOS_WHITE)
    draw.text((40, qy+20), "What does \"downstream\"", font=f_question, fill=IOS_BLACK)
    draw.text((40, qy+50), "mean in the oil industry?", font=f_question, fill=IOS_BLACK)
    # Arabic translation
    f_ar_q = ImageFont.truetype(AR_REG, 18)
    draw.text((40, qy+90), "شنو معنى downstream بصناعة النفط؟", font=f_ar_q, fill=IOS_TERTIARY)

    # Options
    options = [
        ("A", "Refining & Distribution", "التكرير والتوزيع"),
        ("B", "Drilling & Exploration", "الحفر والاستكشاف"),
        ("C", "Pipeline Construction", "بناء الأنابيب"),
        ("D", "Well Maintenance", "صيانة الآبار"),
    ]

    for i, (letter, en_text, ar_text) in enumerate(options):
        oy = qy + 155 + i * 110
        if show_result and i == 0:
            bg = (220, 252, 231)
            border = IOS_GREEN
        elif show_result and i == selected and i != 0:
            bg = (254, 226, 226)
            border = IOS_RED
        elif i == selected and not show_result:
            bg = (219, 234, 254)
            border = SITE_BLUE
        else:
            bg = IOS_WHITE
            border = IOS_GRAY5

        draw.rounded_rectangle([(20, oy), (SW-20, oy+90)], radius=14, fill=bg, outline=border, width=2)

        # Letter badge
        badge_c = IOS_GREEN if (show_result and i == 0) else SITE_BLUE if (i == selected) else IOS_GRAY3
        draw.ellipse([(40, oy+15), (76, oy+51)], fill=badge_c)
        f_letter = ImageFont.truetype(EN_BOLD, 22)
        lb = draw.textbbox((0,0), letter, font=f_letter)
        draw.text((58-(lb[2]-lb[0])//2, oy+19), letter, font=f_letter, fill=IOS_WHITE)

        draw.text((92, oy+14), en_text, font=f_option, fill=IOS_BLACK)
        f_ar_opt = ImageFont.truetype(AR_REG, 16)
        draw.text((92, oy+44), ar_text, font=f_ar_opt, fill=IOS_TERTIARY)

        # Check/X mark
        if show_result and i == 0:
            draw.text((SW-60, oy+20), "✓", font=f_letter, fill=IOS_GREEN)
        elif show_result and i == selected and i != 0:
            draw.text((SW-60, oy+20), "✗", font=f_letter, fill=IOS_RED)

    # Feedback banner
    if show_result:
        fb_y = qy + 155 + 4*110 + 15
        draw.rounded_rectangle([(20, fb_y), (SW-20, fb_y+60)], radius=14, fill=(220, 252, 231))
        bbt = draw.textbbox((0,0), "✓ Correct! Well done!", font=f_feedback)
        draw.text((SW//2-(bbt[2]-bbt[0])//2, fb_y+18), "✓ Correct! Well done!", font=f_feedback, fill=(22, 128, 61))

    if touch_x > 0 and touch_p > 0:
        draw_touch_ripple(draw, touch_x, touch_y, touch_p)


def draw_flashcard_page(draw, flip_p=0, touch_x=-1, touch_y=-1, touch_p=-1):
    """Draw flashcard page with flip."""
    # Nav
    draw.rectangle([(0, 54), (SW, 105)], fill=IOS_WHITE)
    draw.line([(0, 105), (SW, 105)], fill=IOS_GRAY5, width=1)
    f_back = ImageFont.truetype(EN_REG, 17)
    draw.text((24, 72), "< Back", font=f_back, fill=SITE_BLUE)
    f_page_title = ImageFont.truetype(EN_BOLD, 20)
    bb = draw.textbbox((0,0), "Phrasal Verbs", font=f_page_title)
    draw.text((SW//2-(bb[2]-bb[0])//2, 72), "Phrasal Verbs", font=f_page_title, fill=IOS_BLACK)

    # Counter
    f_count = ImageFont.truetype(EN_REG, 16)
    draw.text((SW-100, 74), "1 / 159", font=f_count, fill=IOS_TERTIARY)

    # Card
    card_cx = SW // 2
    card_y = 180
    card_h = 420
    card_full_w = SW - 60

    f_word_en = ImageFont.truetype(EN_BOLD, 52)
    f_word_ar = ImageFont.truetype(AR_BLACK, 56)
    f_phonetic = ImageFont.truetype(EN_REG, 22)
    f_type = ImageFont.truetype(EN_REG, 18)
    f_hint = ImageFont.truetype(EN_REG, 17)
    f_btn = ImageFont.truetype(EN_BOLD, 19)

    if flip_p < 0.5:
        # ENGLISH SIDE
        scale_x = max(0.02, abs(1 - flip_p * 2))
        half_w = int(card_full_w // 2 * scale_x)

        # Card shadow
        if half_w > 20:
            draw.rounded_rectangle(
                [(card_cx-half_w+4, card_y+6), (card_cx+half_w+4, card_y+card_h+6)],
                radius=24, fill=(0, 0, 0, 20))
        draw.rounded_rectangle(
            [(card_cx-half_w, card_y), (card_cx+half_w, card_y+card_h)],
            radius=24, fill=IOS_WHITE)

        if scale_x > 0.4:
            # "ENGLISH" badge
            bw = int(120 * scale_x)
            draw.rounded_rectangle([(card_cx-bw//2, card_y+25), (card_cx+bw//2, card_y+55)],
                                   radius=12, fill=SITE_BLUE)
            if scale_x > 0.6:
                f_badge = ImageFont.truetype(EN_BOLD, 16)
                bbb = draw.textbbox((0,0), "ENGLISH", font=f_badge)
                draw.text((card_cx-(bbb[2]-bbb[0])//2, card_y+32), "ENGLISH", font=f_badge, fill=IOS_WHITE)

            # Word
            word = "Break down"
            wb = draw.textbbox((0,0), word, font=f_word_en)
            draw.text((card_cx-(wb[2]-wb[0])//2, card_y+140), word, font=f_word_en, fill=IOS_BLACK)

            # Type
            draw.text((card_cx-30, card_y+220), "(verb)", font=f_type, fill=IOS_TERTIARY)

            # Phonetic
            ph = "/breɪk daʊn/"
            pb = draw.textbbox((0,0), ph, font=f_phonetic)
            draw.text((card_cx-(pb[2]-pb[0])//2, card_y+260), ph, font=f_phonetic, fill=IOS_GRAY)

            # Tap hint
            h = "Tap to flip"
            hb = draw.textbbox((0,0), h, font=f_hint)
            draw.text((card_cx-(hb[2]-hb[0])//2, card_y+350), h, font=f_hint, fill=IOS_GRAY2)
    else:
        # ARABIC SIDE
        scale_x = max(0.02, (flip_p - 0.5) * 2)
        half_w = int(card_full_w // 2 * scale_x)

        if half_w > 20:
            draw.rounded_rectangle(
                [(card_cx-half_w+4, card_y+6), (card_cx+half_w+4, card_y+card_h+6)],
                radius=24, fill=(0, 0, 0, 20))
        draw.rounded_rectangle(
            [(card_cx-half_w, card_y), (card_cx+half_w, card_y+card_h)],
            radius=24, fill=(239, 246, 255))

        if scale_x > 0.4:
            bw = int(100 * scale_x)
            draw.rounded_rectangle([(card_cx-bw//2, card_y+25), (card_cx+bw//2, card_y+55)],
                                   radius=12, fill=IOS_GREEN)
            if scale_x > 0.6:
                f_badge_ar = ImageFont.truetype(AR_BOLD, 18)
                bba = draw.textbbox((0,0), "عربي", font=f_badge_ar)
                draw.text((card_cx-(bba[2]-bba[0])//2, card_y+30), "عربي", font=f_badge_ar, fill=IOS_WHITE)

            word_ar = "يعطّل / يفكّك"
            wab = draw.textbbox((0,0), word_ar, font=f_word_ar)
            draw.text((card_cx-(wab[2]-wab[0])//2, card_y+130), word_ar, font=f_word_ar, fill=IOS_BLACK)

            eng_small = "Break down"
            f_eng_sm = ImageFont.truetype(EN_REG, 24)
            esb = draw.textbbox((0,0), eng_small, font=f_eng_sm)
            draw.text((card_cx-(esb[2]-esb[0])//2, card_y+220), eng_small, font=f_eng_sm, fill=IOS_TERTIARY)

            meaning = "To stop working / to separate"
            f_mean = ImageFont.truetype(EN_REG, 18)
            mb = draw.textbbox((0,0), meaning, font=f_mean)
            draw.text((card_cx-(mb[2]-mb[0])//2, card_y+270), meaning, font=f_mean, fill=IOS_GRAY)

    # Action buttons
    btn_y = card_y + card_h + 30
    bw_btn = (SW - 72) // 2

    # Needs Review
    draw.rounded_rectangle([(24, btn_y), (24+bw_btn, btn_y+52)], radius=14,
                           fill=(254, 226, 226))
    rbb = draw.textbbox((0,0), "Needs Review", font=f_btn)
    draw.text((24+(bw_btn-(rbb[2]-rbb[0]))//2, btn_y+15), "Needs Review", font=f_btn, fill=IOS_RED)

    # I Know This
    draw.rounded_rectangle([(36+bw_btn, btn_y), (36+bw_btn*2, btn_y+52)], radius=14,
                           fill=(220, 252, 231))
    gbb = draw.textbbox((0,0), "I Know This", font=f_btn)
    draw.text((36+bw_btn+(bw_btn-(gbb[2]-gbb[0]))//2, btn_y+15), "I Know This", font=f_btn, fill=(22, 128, 61))

    # Progress
    prog_y = btn_y + 80
    f_prog = ImageFont.truetype(EN_REG, 15)
    draw.text((24, prog_y), "Progress: 45% mastered", font=f_prog, fill=IOS_TERTIARY)
    draw.rounded_rectangle([(24, prog_y+24), (SW-24, prog_y+32)], radius=4, fill=IOS_GRAY5)
    draw.rounded_rectangle([(24, prog_y+24), (24+int((SW-48)*0.45), prog_y+32)], radius=4, fill=IOS_GREEN)

    if touch_x > 0 and touch_p > 0:
        draw_touch_ripple(draw, touch_x, touch_y, touch_p)


# ════════════════════════════════════════════
#  SCENES
# ════════════════════════════════════════════

def scene_open_safari(p):
    """User opens Safari and types oilexam.tech."""
    img = Image.new('RGB', (SW, SH), IOS_BG)
    draw = ImageDraw.Draw(img)

    draw_ios_status_bar(draw)

    e = ease_out(p * 2)

    if p < 0.3:
        # Safari loading
        bar_y = draw_safari_bar(draw, "oilexam.tech")
        # Loading indicator
        load_w = int((SW-48) * min(1, p / 0.3))
        draw.rounded_rectangle([(24, bar_y+2), (24+load_w, bar_y+5)], radius=2, fill=SITE_BLUE)
    else:
        draw_safari_bar(draw, "oilexam.tech")
        # Page appears
        page_alpha = min(1, (p - 0.3) * 3)
        if page_alpha > 0.1:
            draw_site_content(draw, 0)

    draw_ios_home_bar(draw)
    return img


def scene_scroll_landing(p):
    """Natural scroll through landing page."""
    img = Image.new('RGB', (SW, SH), IOS_BG)
    draw = ImageDraw.Draw(img)

    draw_ios_status_bar(draw)
    draw_safari_bar(draw, "oilexam.tech", scroll_progress=p)

    # Natural scroll with ease
    scroll = int(ease_in_out(p) * 650)
    draw_site_content(draw, scroll)

    draw_ios_home_bar(draw)
    return img


def scene_scroll_features(p):
    """Continue scrolling to features."""
    img = Image.new('RGB', (SW, SH), IOS_BG)
    draw = ImageDraw.Draw(img)

    draw_ios_status_bar(draw)
    draw_safari_bar(draw, "oilexam.tech", scroll_progress=1)

    scroll = 650 + int(ease_in_out(p) * 600)
    draw_site_content(draw, scroll)

    draw_ios_home_bar(draw)
    return img


def scene_tap_quiz(p):
    """User taps on Quiz in nav."""
    img = Image.new('RGB', (SW, SH), IOS_BG)
    draw = ImageDraw.Draw(img)

    draw_ios_status_bar(draw)

    if p < 0.25:
        # Still on landing, finger moves to Quiz
        draw_safari_bar(draw, "oilexam.tech", scroll_progress=1)
        draw_site_content(draw, 1250, touch_x=340, touch_y=80, touch_p=p*4)
    elif p < 0.4:
        # Loading quiz page
        draw_safari_bar(draw, "oilexam.tech/quiz")
        load_w = int((SW-48) * min(1, (p-0.25)/0.15))
        bar_y = 98
        draw.rounded_rectangle([(24, bar_y), (24+load_w, bar_y+3)], radius=2, fill=SITE_BLUE)
    else:
        # Quiz page loaded
        draw_safari_bar(draw, "oilexam.tech/quiz")
        draw_quiz_page(draw, 0)

    draw_ios_home_bar(draw)
    return img


def scene_quiz_interact(p):
    """User reads question and taps answer A."""
    img = Image.new('RGB', (SW, SH), IOS_BG)
    draw = ImageDraw.Draw(img)

    draw_ios_status_bar(draw)
    draw_safari_bar(draw, "oilexam.tech/quiz")

    if p < 0.5:
        # Reading - no selection
        draw_quiz_page(draw, 0)
    elif p < 0.65:
        # Finger moving to option A
        tap_p = (p - 0.5) / 0.15
        touch_y = int(350 + (0) * ease_out(tap_p))
        draw_quiz_page(draw, 0, touch_x=SW//2, touch_y=350, touch_p=tap_p)
    elif p < 0.75:
        # Selected A
        draw_quiz_page(draw, 0, selected=0)
    else:
        # Show result
        draw_quiz_page(draw, 0, selected=0, show_result=True)

    draw_ios_home_bar(draw)
    return img


def scene_go_flashcards(p):
    """Navigate to flashcards."""
    img = Image.new('RGB', (SW, SH), IOS_BG)
    draw = ImageDraw.Draw(img)

    draw_ios_status_bar(draw)

    if p < 0.3:
        # Tap back / flashcards
        draw_safari_bar(draw, "oilexam.tech/quiz")
        draw_quiz_page(draw, 0, selected=0, show_result=True)
    elif p < 0.5:
        # Loading
        draw_safari_bar(draw, "oilexam.tech/flashcards")
        load_w = int((SW-48) * min(1, (p-0.3)/0.2))
        draw.rounded_rectangle([(24, 98), (24+load_w, 101)], radius=2, fill=SITE_BLUE)
    else:
        draw_safari_bar(draw, "oilexam.tech/flashcards")
        draw_flashcard_page(draw, flip_p=0)

    draw_ios_home_bar(draw)
    return img


def scene_flashcard_flip(p):
    """User taps card to flip it."""
    img = Image.new('RGB', (SW, SH), IOS_BG)
    draw = ImageDraw.Draw(img)

    draw_ios_status_bar(draw)
    draw_safari_bar(draw, "oilexam.tech/flashcards")

    if p < 0.3:
        # Viewing English side
        draw_flashcard_page(draw, flip_p=0)
    elif p < 0.35:
        # Tap
        draw_flashcard_page(draw, flip_p=0, touch_x=SW//2, touch_y=400, touch_p=(p-0.3)/0.05)
    elif p < 0.65:
        # Flip animation
        flip = (p - 0.35) / 0.3
        draw_flashcard_page(draw, flip_p=flip)
    else:
        # Arabic side shown
        draw_flashcard_page(draw, flip_p=1.0)

        # User taps "I Know This" at ~80%
        if p > 0.85:
            tp = (p - 0.85) / 0.15
            draw_touch_ripple(draw, SW//2 + 140, 660, tp)

    draw_ios_home_bar(draw)
    return img


def scene_outro_cta(p):
    """Branded CTA outro."""
    return branded_outro(p)


# ════════════════════════════════════════════
#  BUILD
# ════════════════════════════════════════════

def main():
    print("+" + "="*54 + "+")
    print("|  OilExam - Realistic iPhone Screen Recording Reel    |")
    print("+" + "="*54 + "+")

    out_dir = "/root/OilexamVideo"

    build_video("iphone_demo", [
        ("Open Safari",        scene_open_safari,     3.0),
        ("Scroll Landing",     scene_scroll_landing,  3.5),
        ("Scroll Features",    scene_scroll_features, 3.0),
        ("Tap Quiz",           scene_tap_quiz,        3.0),
        ("Quiz Interact",      scene_quiz_interact,   4.5),
        ("Go Flashcards",      scene_go_flashcards,   3.0),
        ("Flashcard Flip",     scene_flashcard_flip,  4.5),
        ("CTA Outro",          scene_outro_cta,       4.0),
    ], f"{out_dir}/pro_reel_iphone_demo.mp4")

    print("\n  IPHONE DEMO REEL COMPLETE!")


if __name__ == "__main__":
    main()
